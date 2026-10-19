# Documentation checks

The normal documentation build image supplies MkDocs and its plugins. Install the additional Markdown export
dependency from `requirements-agent-docs.txt` in the same Python environment before building Wodby 2 docs.

From the repository root:

```sh
python3 -m pip install -r 2.0/requirements-agent-docs.txt
python3 -m unittest discover -s 2.0/scripts -p 'test_agent_docs.py'
python3 2.0/scripts/check_agent_contract.py
cd 2.0
mkdocs build --strict
```

`agent_docs.py` generates clean Markdown from rendered page content, after includes and links are processed. It writes
an `index.md` alongside each directory-style HTML page, adds alternate/discovery links to HTML, and generates the
docs-only `llms.txt`. Collapsible sections are expanded in Markdown, including their labels and nested content.
Output belongs in the build directory, not the source tree. Update `INDEX_SECTIONS` when curated
entry points move; the build fails for a missing entry. Wodby 1 has a separate build and is not included.

Run `python3 2.0/scripts/check_agent_contract.py --live` to compare the skill table with the current public distribution,
verify skill hashes, and ensure tool names referenced by those skills have descriptions. The check fetches public
guidance only and needs no account credential. It does not prove complete tool/schema parity or exercise account
operations. Review the live `tools/list` contract in an authorized integration test when changing tool behavior.

The agent-documentation workflow runs these checks on pull requests and can also be run manually to detect later
skill drift. It fails if the public distribution cannot be checked rather than reporting unverified parity as success.
