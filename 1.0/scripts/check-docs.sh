#!/bin/sh

set -eu

log_file="$(mktemp)"
trap 'rm -f "$log_file"' EXIT

if ! mkdocs build --strict "$@" >"$log_file" 2>&1; then
    cat "$log_file"
    exit 1
fi

cat "$log_file"

if grep -Eq 'does not contain an anchor|not found (in|among) (the )?documentation files' "$log_file"; then
    echo "Documentation contains a broken local page or anchor link." >&2
    exit 1
fi
