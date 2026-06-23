"""Add generated static reference pages to the MkDocs sitemap."""

from __future__ import annotations

import gzip
from datetime import date
from pathlib import Path
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
REFERENCE_DIRS = ("api", "cli")


def on_post_build(*, config) -> None:
    site_url = config.get("site_url")
    if not site_url:
        return

    site_dir = Path(config["site_dir"])
    sitemap_path = site_dir / "sitemap.xml"
    if not sitemap_path.is_file():
        return

    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    loc_tag = f"{{{SITEMAP_NS}}}loc"
    existing_urls = {
        loc.text
        for loc in root.iter(loc_tag)
        if loc.text
    }

    added = 0
    for page_path in generated_reference_pages(site_dir):
        loc = urljoin(site_url, canonical_page_url(site_dir, page_path))
        if loc in existing_urls:
            continue

        url = ET.SubElement(root, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(url, loc_tag).text = loc
        ET.SubElement(url, f"{{{SITEMAP_NS}}}lastmod").text = lastmod(page_path)
        existing_urls.add(loc)
        added += 1

    if not added:
        return

    ET.register_namespace("", SITEMAP_NS)
    ET.indent(tree, space="    ")
    tree.write(sitemap_path, encoding="UTF-8", xml_declaration=True)

    gzip_path = sitemap_path.with_suffix(".xml.gz")
    with sitemap_path.open("rb") as source, gzip.open(gzip_path, "wb") as target:
        target.write(source.read())


def generated_reference_pages(site_dir: Path) -> list[Path]:
    pages: list[Path] = []
    for dirname in REFERENCE_DIRS:
        reference_dir = site_dir / dirname
        if reference_dir.is_dir():
            pages.extend(sorted(reference_dir.rglob("*.html")))
    return pages


def canonical_page_url(site_dir: Path, page_path: Path) -> str:
    relative_path = page_path.relative_to(site_dir)
    if page_path.name == "index.html":
        return f"{relative_path.parent.as_posix()}/"
    return relative_path.as_posix()


def lastmod(page_path: Path) -> str:
    return date.fromtimestamp(page_path.stat().st_mtime).isoformat()
