"""Give each page its own meta description, taken from the page's opening text."""

from html import escape

from bs4 import BeautifulSoup


# Search engines show roughly this many characters of a description.
MAX_LENGTH = 160
# Keep adding paragraphs until the description is at least this long.
MIN_LENGTH = 110
# A paragraph inside one of these is a note, a table cell, a list item or an example, not the page's opening text.
ASIDE_TAGS = {"details", "table", "li", "dd", "blockquote", "figure"}
ASIDE_CLASSES = {"admonition", "tabbed-set", "footnote"}
# Left behind at the end of a description cut in the middle of a sentence.
DANGLING = " ,;:-–—(/"


def on_page_content(html, *, page, config, files):
    """Describe the page before the theme renders its head; a description set in front matter wins."""
    if not page.meta.get("description"):
        description = describe(html)
        if description:
            # The theme writes the value into a double-quoted attribute as is, so it must already be safe there.
            page.meta["description"] = escape(description, quote=False).replace('"', "&quot;")
    return html


def describe(html):
    """Return the page's opening paragraphs as plain text, or an empty string when the page has none."""
    soup = BeautifulSoup(html, "html.parser")
    # Heading anchors, footnote markers, images and scripts are not prose.
    for element in soup.select("a.headerlink, sup, img, script, style"):
        element.decompose()
    for line_break in soup.find_all("br"):
        line_break.replace_with(" ")
    description = ""
    for paragraph in soup.find_all("p"):
        if is_aside(paragraph):
            continue
        sentence = plain_text(paragraph)
        if not sentence:
            continue
        if sentence.endswith(":"):
            # A paragraph that introduces a list is finished by its items; any other lead-in becomes a sentence.
            items = list_items(paragraph.find_next_sibling())
            sentence = f"{sentence} {'; '.join(items)}." if items else sentence[:-1] + "."
        elif sentence[-1] not in ".!?…":
            sentence += "."
        description = f"{description} {sentence}".strip()
        if len(description) >= MIN_LENGTH:
            break
    return shorten(description)


def plain_text(element):
    """Return the element's text on one line, without markup."""
    return " ".join(element.get_text().split())


def list_items(element):
    """Return the top-level items of a list as plain text; anything that is not a list has none."""
    if element is None or element.name not in ("ul", "ol"):
        return []
    items = []
    for item in element.find_all("li", recursive=False):
        for nested in item.find_all(["ul", "ol"]):
            nested.decompose()
        text = plain_text(item).rstrip(".;,:")
        if text:
            items.append(text)
    return items


def is_aside(paragraph):
    """Tell whether the paragraph sits inside a note, table, list, quote, tab or footnote."""
    for parent in paragraph.parents:
        if parent.name in ASIDE_TAGS or ASIDE_CLASSES.intersection(parent.get("class") or []):
            return True
    return False


def shorten(text):
    """Fit the text into MAX_LENGTH, ending on a full sentence when one fits and on a whole word otherwise."""
    if len(text) <= MAX_LENGTH:
        return text
    cut = text[:MAX_LENGTH + 1]
    sentence_end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
    if sentence_end >= MIN_LENGTH - 1:
        return cut[:sentence_end + 1]
    cut = text[:MAX_LENGTH]
    cut = cut[:cut.rfind(" ")].rstrip(DANGLING)
    return cut + "…"
