"""Offline regression checks for per-page meta descriptions."""

import re
import unittest
from pathlib import Path
from types import SimpleNamespace

import page_descriptions as descriptions

ROOT = Path(__file__).resolve().parents[1]
SITES = {"1.0": ROOT / "1.0" / "docs", "2.0": ROOT / "2.0" / "docs"}
# A description is shown as plain text, so links, code spans and emphasis would appear as raw characters.
MARKDOWN = re.compile(r"`|\*\*|\]\(|<[a-z/]")


def source_description(path):
    """Return the description in a source page's front matter, or an empty string when it has none."""
    front_matter = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    written = re.search(r"^description:\s*(.+)$", front_matter.group(1), re.M) if front_matter else None
    if not written:
        return ""
    value = written.group(1).strip()
    return value[1:-1] if value[:1] in "\"'" and value[-1:] == value[:1] else value


def page(**meta):
    return SimpleNamespace(meta=dict(meta))


class PageDescriptionTests(unittest.TestCase):
    def test_opening_paragraph_becomes_plain_text(self):
        html = '''<h1 id="deploys">Deployments<a class="headerlink" href="#deploys">¶</a></h1>
        <div class="admonition warning"><p class="admonition-title">Warning</p><p>Skipped note.</p></div>
        <p><img alt="Diagram" src="diagram.png"></p>
        <p>Deployments can target <strong>all services</strong> in an
        <a href="../environments/">app environment</a><sup id="fnref:1"><a href="#fn:1">1</a></sup>
        or only <code>selected</code> services, and every deployment is recorded as a task.</p>
        <p>Not needed.</p>'''
        self.assertEqual(
            descriptions.describe(html),
            "Deployments can target all services in an app environment or only selected services, "
            "and every deployment is recorded as a task.",
        )

    def test_short_paragraphs_are_joined(self):
        html = '''<p>A stack is the blueprint for an application</p>
        <table><tr><td><p>Skipped cell.</p></td></tr></table>
        <ul><li><p>Skipped item.</p></li></ul>
        <h2>Services</h2>
        <p>It defines which services the app uses and the default configuration for those services.</p>'''
        self.assertEqual(
            descriptions.describe(html),
            "A stack is the blueprint for an application. "
            "It defines which services the app uses and the default configuration for those services.",
        )

    def test_list_introduction_is_finished_by_its_items(self):
        html = '''<p>A user can have:</p>
        <ul><li>an organization role</li><li><p>team memberships.</p><ul><li>nested</li></ul></li></ul>
        <p>Use the command:</p><pre><code>wodby ci build</code></pre>
        <p>These layers answer different questions about what a user can see and change.</p>'''
        self.assertEqual(
            descriptions.describe(html),
            "A user can have: an organization role; team memberships. Use the command. "
            "These layers answer different questions about what a user can see and change.",
        )

    def test_long_text_ends_on_a_sentence_or_a_whole_word(self):
        sentence = "Wodby collects metrics for clusters, nodes, namespaces, app environments and app services."
        self.assertEqual(descriptions.shorten(f"{sentence} Open them from the cluster page. {sentence}"),
                         f"{sentence} Open them from the cluster page.")
        cut = descriptions.shorten("word " * 20 + "before, " + "longer-word " * 10)
        self.assertLessEqual(len(cut), descriptions.MAX_LENGTH)
        self.assertTrue(cut.endswith("longer-word…"), cut)
        self.assertEqual(descriptions.shorten("word " * 30 + "last, " + "x" * 50), "word " * 30 + "last…")

    def test_front_matter_description_wins(self):
        written = page(description='Written by hand for "Apps" & stacks. ')
        descriptions.on_page_content("<p>Derived text.</p>", page=written, config={}, files=None)
        self.assertEqual(written.meta["description"], "Written by hand for &quot;Apps&quot; &amp; stacks.")

    def test_derived_description_is_safe_in_the_tag(self):
        derived = page()
        html = '<p>Open <code>Apps &gt; [App]</code> &amp; set "Replicas" to the app\'s <b>&lt;count&gt;</b>.</p>'
        self.assertEqual(descriptions.on_page_content(html, page=derived, config={}, files=None), html)
        self.assertEqual(derived.meta["description"],
                         "Open Apps &gt; [App] &amp; set &quot;Replicas&quot; to the app's &lt;count&gt;.")

    def test_page_without_text_keeps_the_site_description(self):
        empty = page()
        html = '<h1>Reference</h1><table><tr><td><p>Cell.</p></td></tr></table><pre><code>code</code></pre>'
        descriptions.on_page_content(html, page=empty, config={}, files=None)
        self.assertNotIn("description", empty.meta)

    def test_every_source_page_has_a_description_of_the_right_length(self):
        problems = []
        for path in sorted(path for docs in SITES.values() for path in docs.rglob("*.md")):
            name = str(path.relative_to(ROOT))
            description = source_description(path)
            if not description:
                problems.append(f"{name}: no description in the front matter")
            elif not descriptions.MIN_LENGTH <= len(description) <= descriptions.MAX_LENGTH:
                problems.append(f"{name}: description is {len(description)} characters, expected "
                                f"{descriptions.MIN_LENGTH} to {descriptions.MAX_LENGTH}")
            elif MARKDOWN.search(description):
                problems.append(f"{name}: description contains Markdown")
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
