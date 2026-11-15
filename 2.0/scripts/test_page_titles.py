"""Offline regression checks for per-page titles."""

import re
import unittest
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import page_titles as titles

DOCS = Path(__file__).resolve().parents[1] / "docs"
# Labels that only make sense inside the navigation menu.
MENU_ONLY = {"overview", "create", "updates", "types", "template", "managed", "configuration"}


def page(**meta):
    return SimpleNamespace(meta=dict(meta))


def source_title(path):
    """Return the title a source page ends up with: its front-matter title, else its first heading."""
    text = path.read_text(encoding="utf-8")
    front_matter = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if front_matter:
        explicit = re.search(r"^title:\s*(.+)$", front_matter.group(1), re.M)
        if explicit:
            return explicit.group(1).strip().strip("\"'")
        text = text[front_matter.end():]
    first_heading = re.search(r"^# (.+)$", text, re.M)
    return first_heading.group(1).strip() if first_heading else ""


class PageTitleTests(unittest.TestCase):
    def test_heading_becomes_plain_text(self):
        html = '''<p>Lead-in.</p>
        <h1 id="backups">Application <code>backups</code><sup>1</sup>
        <a class="headerlink" href="#backups" title="Permanent link">¶</a></h1>
        <h1 id="second">Second heading</h1>'''
        self.assertEqual(titles.heading(html), "Application backups")
        self.assertEqual(titles.heading("<h2>Only a section</h2><p>Text.</p>"), "")

    def test_heading_is_used_when_front_matter_has_no_title(self):
        subject = page()
        titles.on_page_content("<h1>Build &amp; deploy</h1>", page=subject, config={}, files=None)
        self.assertEqual(subject.meta["title"], "Build &amp; deploy")

    def test_front_matter_title_wins(self):
        subject = page(title=" Connect an AI client <now> ")
        titles.on_page_content("<h1>MCP</h1>", page=subject, config={}, files=None)
        self.assertEqual(subject.meta["title"], "Connect an AI client &lt;now&gt;")

    def test_page_without_a_heading_keeps_its_navigation_label(self):
        subject = page()
        titles.on_page_content("<p>Text only.</p>", page=subject, config={}, files=None)
        self.assertNotIn("title", subject.meta)

    def test_source_pages_have_distinct_titles_that_name_their_subject(self):
        by_title = defaultdict(list)
        for path in sorted(DOCS.rglob("*.md")):
            title = source_title(path)
            name = str(path.relative_to(DOCS))
            self.assertTrue(title, f"{name} has no heading and no title")
            self.assertNotIn(title.lower(), MENU_ONLY, f"{name} is titled with a menu label")
            by_title[title.lower()].append(name)
        repeated = {title: paths for title, paths in by_title.items() if len(paths) > 1}
        self.assertEqual(repeated, {})

    def test_catalog_and_provider_pages_say_what_they_are(self):
        for path in sorted((DOCS / "stacks" / "catalog").glob("*/index.md")):
            expected = "stacks" if path.parent.name == "system" else " stack guide"
            self.assertTrue(source_title(path).endswith(expected), path)
        concept_pages = {"index", "wodby-blob-storage"}
        for path in sorted((DOCS / "providers").glob("*.md")):
            if path.stem not in concept_pages:
                self.assertIn("provider", source_title(path).lower(), path)


if __name__ == "__main__":
    unittest.main()
