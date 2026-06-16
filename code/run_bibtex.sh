#!/usr/bin/env bash
set -euo pipefail
if command -v bibtex >/dev/null 2>&1 && bibtex --version >/dev/null 2>&1; then
  exec bibtex "$@"
elif command -v bibtex.original >/dev/null 2>&1; then
  exec bibtex.original "$@"
elif command -v bibtex8 >/dev/null 2>&1; then
  exec bibtex8 "$@"
else
  echo "No working BibTeX executable found." >&2
  exit 127
fi
