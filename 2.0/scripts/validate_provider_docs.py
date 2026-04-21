#!/usr/bin/env python3
"""Validate that provider manifest files have matching provider docs pages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_MANIFESTS_DIR = Path.home() / "Projects" / "backend" / "pkg" / "provider" / "manifests"
DEFAULT_DOCS_DIR = Path(__file__).resolve().parents[1] / "docs" / "providers"

# Pages in providers/ that are concept or group-overview pages rather than provider pages.
NON_PROVIDER_DOC_STEMS = {
    "index",
    "kubernetes",
    "databases",
    "storage",
    "git",
    "ci",
    "registry",
    "smtp",
    "vpn",
    "variable",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that backend provider manifests and provider docs pages stay in sync.",
    )
    parser.add_argument(
        "--manifests-dir",
        type=Path,
        default=DEFAULT_MANIFESTS_DIR,
        help=f"Path to provider manifests (default: {DEFAULT_MANIFESTS_DIR})",
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=DEFAULT_DOCS_DIR,
        help=f"Path to provider docs pages (default: {DEFAULT_DOCS_DIR})",
    )
    return parser.parse_args()


def load_manifest_stems(manifests_dir: Path) -> set[str]:
    if not manifests_dir.is_dir():
        raise FileNotFoundError(f"Manifests directory not found: {manifests_dir}")
    return {path.stem for path in manifests_dir.glob("*.yml")}


def load_provider_doc_stems(docs_dir: Path) -> set[str]:
    if not docs_dir.is_dir():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")
    return {
        path.stem
        for path in docs_dir.glob("*.md")
        if path.stem not in NON_PROVIDER_DOC_STEMS
    }


def main() -> int:
    args = parse_args()
    try:
        manifest_stems = load_manifest_stems(args.manifests_dir)
        provider_doc_stems = load_provider_doc_stems(args.docs_dir)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    missing_docs = sorted(manifest_stems - provider_doc_stems)
    orphan_docs = sorted(provider_doc_stems - manifest_stems)

    print(f"Provider manifests: {len(manifest_stems)}")
    print(f"Provider docs: {len(provider_doc_stems)}")

    if not missing_docs and not orphan_docs:
        print("OK: provider docs and backend manifests are in sync.")
        return 0

    if missing_docs:
        print("\nMissing docs pages for manifests:")
        for stem in missing_docs:
            print(f"- {stem}.yml -> {stem}.md")

    if orphan_docs:
        print("\nDocs pages without matching manifests:")
        for stem in orphan_docs:
            print(f"- {stem}.md")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
