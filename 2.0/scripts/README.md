# Documentation checks

The normal documentation build image supplies MkDocs and its plugins. Install the additional Markdown export
dependency from `requirements-agent-docs.txt` in the same Python environment before building Wodby 2 docs.

From the repository root:

```sh
python3 -m pip install -r 2.0/requirements-agent-docs.txt
python3 -m unittest discover -s 2.0/scripts -p 'test_*.py'
python3 2.0/scripts/check_agent_contract.py
cd 2.0
mkdocs build --strict
```

`agent_docs.py` generates clean Markdown from rendered page content, after includes and links are processed. It writes
an `index.md` alongside each directory-style HTML page, adds alternate/discovery links to HTML, and generates the
docs-only `llms.txt`. Collapsible sections are expanded in Markdown, including their labels and nested content.
Output belongs in the build directory, not the source tree. Update `INDEX_SECTIONS` when curated
entry points move; the build fails for a missing entry. Wodby 1 has a separate build and is not included.

Every page has a `description` in its front matter: one or two plain sentences of 110 to 160 characters that say what
the page covers. Search engines show it under the page title, so write one for each new page and update it when the
page's subject changes. Write plain text without Markdown; quote the value if it contains `: ` or ` #`.

`page_descriptions.py` writes that text into the page's `<meta name="description">`. For a page without a
`description`, it uses the page's opening paragraphs as plain text instead, cut to about 160 characters at the end of a
sentence or a word; a paragraph that introduces a list is completed with the list items, and notes, tables, lists and
code are skipped. `site_description` remains the fallback for a page with no paragraph text.

Run `python3 2.0/scripts/check_agent_contract.py --live` to compare the skill table with the current public distribution,
verify skill hashes, and ensure tool names referenced by those skills have descriptions. The check fetches public
guidance only and needs no account credential. It recognizes tool names by their leading verb in `TOOL_VERBS`, so add
the verb when documenting a tool that starts with a new one; a test fails until then. It does not prove complete
tool/schema parity or exercise account operations. Review the live `tools/list` contract in an authorized integration test when changing tool behavior.

The agent-documentation workflow runs these checks on pull requests and can also be run manually to detect later
skill drift. It fails if the public distribution cannot be checked rather than reporting unverified parity as success.
