"""Publish documentation-only discovery and Markdown from rendered page content."""

from html import escape
from pathlib import Path, PurePosixPath
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from markdownify import markdownify


# Curated entry points, not a second copy of the documentation navigation.
INDEX_SECTIONS = {
    "Start here": ["index.md", "agents/index.md", "apps/app-vs-environment-vs-service.md", "glossary.md"],
    "Using agents": [
        "agents/clients.md", "agents/permissions.md", "agents/skills.md",
        "agents/workflows/migrate.md", "agents/workflows/staging.md",
        "agents/workflows/troubleshoot.md", "agents/troubleshooting.md",
    ],
    "Technical interfaces": ["dev/mcp.md", "dev/mcp/tools.md", "dev/api.md", "dev/sdks.md", "dev/cli.md"],
    "Operate applications": [
        "tasks.md", "apps/deploys.md", "apps/observability.md", "apps/imports.md",
        "apps/backups.md", "apps/stack.md", "stacks/updates.md", "access-control.md",
    ],
    "Reusable definitions": ["services/index.md", "services/create.md", "stacks/create.md", "providers/index.md"],
}

_pages = {}

INDEX_TITLES = {
    "index.md": "Wodby 2 overview",
    "agents/index.md": "Agent quickstart",
    "services/index.md": "Services overview",
    "services/create.md": "Create a service",
    "stacks/create.md": "Create a stack",
    "providers/index.md": "Providers overview",
    "apps/stack.md": "Application stack configuration",
    "stacks/updates.md": "Stack updates",
}


def on_pre_build(*, config):
    """Reset state on every build, including repeated development builds."""
    _pages.clear()


def markdown_uri(page):
    """Place the alternate beside the rendered page, including directory indexes."""
    return str(PurePosixPath(page.file.dest_uri).with_suffix(".md"))


def clean_markdown(content, canonical_url):
    """Keep page content, tables, warnings and examples without navigation or UI controls."""
    soup = BeautifulSoup(content, "html.parser")
    for element in soup.select("a.headerlink, script, style, input, button"):
        element.decompose()
    # Keep tab names next to their content instead of a detached list of all tab labels.
    for group in soup.select(".tabbed-set"):
        labels = group.select(":scope > .tabbed-labels > label")
        blocks = group.select(":scope > .tabbed-content > .tabbed-block")
        for label, block in zip(labels, blocks):
            title = soup.new_tag("p")
            bold = soup.new_tag("strong")
            bold.string = label.get_text(" ", strip=True)
            title.append(bold)
            block.insert(0, title)
        for labels_container in group.select(":scope > .tabbed-labels"):
            labels_container.decompose()
    for element in soup.find_all(["a", "img"]):
        attribute = "href" if element.name == "a" else "src"
        if element.get(attribute):
            element[attribute] = urljoin(canonical_url, element[attribute])
    text = markdownify(str(soup), heading_style="ATX", bullets="-", strip_pre=None)
    return f"Source: {canonical_url}\n\n{text.strip()}\n"


def on_page_content(html, *, page, config, files):
    """Convert after MkDocs expands includes and resolves documentation links."""
    canonical = urljoin(config["site_url"].rstrip("/") + "/", page.url)
    _pages[page.file.src_uri] = {
        "title": page.title,
        "uri": markdown_uri(page),
        "markdown": clean_markdown(html, canonical),
    }
    return html


def on_post_page(output, *, page, config):
    """Advertise alternates so discovery does not depend on guessing a URL."""
    base = config["site_url"].rstrip("/") + "/"
    alternate = escape(urljoin(base, markdown_uri(page)), quote=True)
    index = escape(urljoin(base, "llms.txt"), quote=True)
    links = f'<link rel="alternate" type="text/markdown" href="{alternate}">\n'
    links += f'<link rel="describedby" type="text/plain" href="{index}">\n'
    return output.replace("</head>", links + "</head>", 1)


def build_index(pages, site_url):
    """Fail builds if a curated entry was removed or renamed without updating discovery."""
    base = site_url.rstrip("/") + "/"
    lines = [
        "# Wodby 2 documentation", "",
        "> Self-contained technical guidance for deploying and operating applications on Wodby 2.", "",
        "These docs apply to Wodby 2, not Wodby 1. Start with the agent quickstart for agent-assisted work.",
        "Use live MCP tool schemas for available operations and inputs. Guidance does not authorize changes.",
        "Markdown links below contain the same page content as the HTML docs, without site navigation.",
        "",
    ]
    for heading, paths in INDEX_SECTIONS.items():
        lines.extend([f"## {heading}", ""])
        for path in paths:
            page = pages[path]
            title = INDEX_TITLES.get(path, page["title"])
            lines.append(f'- [{title}]({urljoin(base, page["uri"])})')
        lines.append("")
    lines.extend([
        "## Schemas", "",
        f"- [OpenAPI JSON]({urljoin(base, 'api/openapi.json')})",
        f"- [OpenAPI YAML]({urljoin(base, 'api/openapi.yaml')})", "",
    ])
    return "\n".join(lines)


def on_post_build(*, config):
    """Write generated artifacts only into the build output, never into source docs."""
    root = Path(config["site_dir"])
    for page in _pages.values():
        target = root / page["uri"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page["markdown"], encoding="utf-8")
    (root / "llms.txt").write_text(build_index(_pages, config["site_url"]), encoding="utf-8")
