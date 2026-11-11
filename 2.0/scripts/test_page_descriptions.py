"""Offline regression checks for per-page meta descriptions."""

import unittest
from types import SimpleNamespace

import page_descriptions as descriptions


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
        written = page(description="Written by hand.")
        descriptions.on_page_content("<p>Derived text.</p>", page=written, config={}, files=None)
        self.assertEqual(written.meta["description"], "Written by hand.")

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


if __name__ == "__main__":
    unittest.main()
