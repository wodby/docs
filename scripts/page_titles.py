"""Give each page a browser and search title that names its subject, taken from the page's heading."""

from html import escape

from bs4 import BeautifulSoup


def on_page_content(html, *, page, config, files):
    """Title the page before the theme renders its head; a title set in front matter wins.

    Without this the theme falls back to the navigation label, which is written to be read inside the menu
    ("Overview", "Updates") and says nothing on its own in a browser tab or a search result.
    """
    title = str(page.meta.get("title") or "").strip() or heading(html)
    if title:
        # The theme writes the value into the page as is, so it must already be safe there.
        page.meta["title"] = escape(title, quote=False)
    return html


def heading(html):
    """Return the page's first top-level heading as plain text, or an empty string when the page has none."""
    soup = BeautifulSoup(html, "html.parser")
    first = soup.find("h1")
    if first is None:
        return ""
    # The permalink anchor, footnote markers and images are not part of the heading's text.
    for element in first.select("a.headerlink, sup, img"):
        element.decompose()
    return " ".join(first.get_text().split())
