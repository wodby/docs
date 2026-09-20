"""Offline regression checks for machine-readable documentation exports."""

import unittest
import hashlib
import json
from types import SimpleNamespace
from unittest.mock import patch

import agent_docs
import check_agent_contract as contract


class AgentDocsTests(unittest.TestCase):
    def test_markdown_preserves_content_without_page_chrome(self):
        html = '''<h2>Safety<a class="headerlink" href="#safety">¶</a></h2>
        <div class="admonition warning"><p class="admonition-title">Warning</p><p>Do not delete data.</p></div>
        <pre><code>echo "$TOKEN"\n</code></pre>
        <table><tr><th>Scope</th><th>Use</th></tr><tr><td>read</td><td>Inspect</td></tr></table>
        <a href="../../tasks/#jobs-and-steps">Tasks</a><img src="../diagram.png" alt="Diagram">
        <script>secret-ui-code</script>'''
        result = agent_docs.clean_markdown(html, "https://wodby.com/docs/2.0/agents/clients/")
        for expected in ['Do not delete data.', 'echo "$TOKEN"', '| Scope | Use |',
                         'https://wodby.com/docs/2.0/tasks/#jobs-and-steps', '```']:
            self.assertIn(expected, result)
        self.assertNotIn('¶', result)
        self.assertNotIn('secret-ui-code', result)

    def test_tabs_keep_labels_with_examples(self):
        html = '''<div class="tabbed-set"><input id="tab"/>
        <div class="tabbed-labels"><label>macOS</label><label>Windows</label></div>
        <div class="tabbed-content"><div class="tabbed-block"><pre>first</pre></div>
        <div class="tabbed-block"><pre>second</pre></div></div></div>'''
        result = agent_docs.clean_markdown(html, "https://wodby.com/docs/2.0/")
        self.assertLess(result.index('macOS'), result.index('first'))
        self.assertLess(result.index('first'), result.index('Windows'))
        self.assertLess(result.index('Windows'), result.index('second'))

    def test_collapsed_details_are_fully_exported(self):
        html = '''<details><summary>Optional setup</summary><p>Keep this instruction.</p>
        <pre><code>example-command</code></pre>
        <details><summary>Nested details</summary><p>Keep the warning.</p></details></details>'''
        result = agent_docs.clean_markdown(html, "https://wodby.com/docs/2.0/dev/mcp/")
        for text in ['**Optional setup**', 'Keep this instruction.', 'example-command',
                     '**Nested details**', 'Keep the warning.']:
            self.assertIn(text, result)
        self.assertNotIn('<details', result)

    def test_alternates_and_nested_urls(self):
        page = SimpleNamespace(file=SimpleNamespace(dest_uri="agents/clients/index.html"))
        self.assertEqual(agent_docs.markdown_uri(page), "agents/clients/index.md")
        result = agent_docs.on_post_page('<head></head>', page=page,
                                         config={"site_url": "https://wodby.com/docs/2.0"})
        self.assertIn('https://wodby.com/docs/2.0/agents/clients/index.md', result)
        self.assertIn('https://wodby.com/docs/2.0/llms.txt', result)

    def test_index_stays_in_wodby2_documentation(self):
        pages = {path: {"title": path, "uri": path}
                 for paths in agent_docs.INDEX_SECTIONS.values() for path in paths}
        result = agent_docs.build_index(pages, "https://wodby.com/docs/2.0")
        self.assertNotIn('/solutions/', result)
        self.assertNotIn('/docs/1.0/', result)
        self.assertIn('agents/workflows/migrate.md', result)
        with self.assertRaises(KeyError):
            agent_docs.build_index({}, "https://wodby.com/docs/2.0")


class ContractTests(unittest.TestCase):
    def test_public_url_boundary(self):
        contract.validate_public_url(contract.PUBLIC_SKILLS)
        contract.validate_public_url(contract.PUBLIC_SKILLS + "/0.2.0/index.json")
        for url in ["http://mcp.wodby.com/agent-skills", "https://example.com/agent-skills",
                    "https://mcp.wodby.com/mcp", "https://mcp.wodby.com/agent-skills-other"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                contract.validate_public_url(url)

    def test_redirect_is_checked_before_following(self):
        with self.assertRaises(ValueError):
            contract.PublicSkillRedirectHandler().redirect_request(
                None, None, 302, "Found", {}, "https://example.com/account")

    def run_fixture(self, *, bad_hash=False, unknown_tool=False, missing_skill=False):
        """Exercise live checks entirely offline with a synthetic public distribution."""
        names = contract.documented_names((contract.DOCS / "agents/skills.md").read_text(), r"wodby2-[a-z-]+")
        content = b"Use `get_nonexistent_contract_tool`." if unknown_tool else b"Use `get_wodby_guidance`."
        digest = "invalid" if bad_hash else hashlib.sha256(content).hexdigest()
        selected = sorted(names)[1:] if missing_skill else sorted(names)
        index = {"version": "fixture", "skills": [
            {"name": name, "url": f"/agent-skills/fixture/{name}/SKILL.md", "sha256": digest}
            for name in selected]}

        def document(url):
            if url == contract.PUBLIC_SKILLS:
                return b"[Index](/agent-skills/fixture/index.json)"
            if url.endswith("index.json"):
                return json.dumps(index).encode()
            return content

        with patch.object(contract, "public_document", side_effect=document), patch("builtins.print"):
            contract.check(live=True)

    def test_matching_distribution(self):
        self.run_fixture()

    def test_inventory_hash_and_tool_drift_fail(self):
        for option, message in [("bad_hash", "Hash mismatch"), ("unknown_tool", "undocumented tools"),
                                ("missing_skill", "Skill inventory drift")]:
            with self.subTest(option=option), self.assertRaisesRegex(ValueError, message):
                self.run_fixture(**{option: True})


if __name__ == "__main__":
    unittest.main()
