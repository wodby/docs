"""Check docs against public skill artifacts without credentials or account operations."""

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


DOCS = Path(__file__).resolve().parents[1] / "docs"
PUBLIC_SKILLS = "https://mcp.wodby.com/agent-skills"
TOOL_PATTERN = r"`((?:get|list|find|show|prepare|validate|create|update|start|read|stop|wait|diagnose|import|deploy|run|repeat|delete|cancel|sync|reconcile|upgrade|scale|duplicate|redeploy)_[a-z0-9_]+)`"


def documented_names(text, pattern):
    """Read contract names from table rows, not incidental prose references."""
    return set(re.findall(r"^\| `(" + pattern + r")` \|", text, re.MULTILINE))


def validate_public_url(url):
    """Reject URLs outside the public distribution before issuing a request."""
    parsed = urlparse(url)
    if (parsed.scheme != "https" or parsed.netloc != "mcp.wodby.com"
            or not (parsed.path == "/agent-skills" or parsed.path.startswith("/agent-skills/"))):
        raise ValueError(f"Not a public skill URL: {url}")


class PublicSkillRedirectHandler(HTTPRedirectHandler):
    """Validate redirects before urllib follows them, not after a response arrives."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def public_document(url):
    """Limit reads to the public skill distribution; never follow account URLs."""
    validate_public_url(url)
    request = Request(url, headers={"User-Agent": "WodbyDocsCheck/1.0", "Accept": "text/markdown, application/json"})
    with build_opener(PublicSkillRedirectHandler()).open(request, timeout=30) as response:
        data = response.read(2_000_001)
    if len(data) > 2_000_000:
        raise ValueError("Unexpectedly large skill document")
    return data


def check(live=False):
    """Check local references; optionally detect drift in currently published skills."""
    tools = documented_names((DOCS / "dev/mcp/tools.md").read_text(), r"[a-z0-9_]+")
    skills = documented_names((DOCS / "agents/skills.md").read_text(), r"wodby2-[a-z-]+")
    errors = []
    for path in (DOCS / "agents").rglob("*.md"):
        text = path.read_text()
        missing = set(re.findall(TOOL_PATTERN, text)) - tools
        if missing:
            errors.append(f"{path.relative_to(DOCS)}: undocumented tools {sorted(missing)}")
        for target in re.findall(r"\]\((https?://[^)]+)\)", text):
            parsed = urlparse(target)
            if parsed.netloc in {"wodby.com", "www.wodby.com"} and not parsed.path.startswith("/docs/2.0/"):
                errors.append(f"{path.relative_to(DOCS)}: non-documentation Wodby link {target}")
    if live:
        landing = public_document(PUBLIC_SKILLS).decode()
        match = re.search(r"\]\((/agent-skills/[^)]+/index\.json)\)", landing)
        if not match:
            raise ValueError("Public skill index link not found")
        index = json.loads(public_document(urljoin(PUBLIC_SKILLS, match[1])))
        published = {skill["name"] for skill in index["skills"]}
        if published != skills:
            errors.append(f"Skill inventory drift: missing={sorted(published-skills)}, obsolete={sorted(skills-published)}")
        for skill in index["skills"]:
            content = public_document(urljoin(PUBLIC_SKILLS, skill["url"]))
            if hashlib.sha256(content).hexdigest() != skill["sha256"]:
                errors.append(f"Hash mismatch: {skill['name']}")
            missing = set(re.findall(TOOL_PATTERN, content.decode())) - tools
            if missing:
                errors.append(f"{skill['name']}: undocumented tools {sorted(missing)}")
        print(f"Checked public skill bundle {index['version']} ({len(published)} skills)")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Checked {len(skills)} documented skills and {len(tools)} tool descriptions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Compare with public skill distribution (no authentication)")
    check(parser.parse_args().live)
