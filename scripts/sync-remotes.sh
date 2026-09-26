#!/usr/bin/env bash

set -euo pipefail

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "Sync aborted: check out the main branch first." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Sync aborted: commit or stash local changes first." >&2
  exit 1
fi

git fetch origin main
git fetch overleaf main

if ! git merge-base --is-ancestor origin/main main; then
  echo "Sync aborted: origin/main contains changes not present locally." >&2
  exit 1
fi

if ! git merge-base --is-ancestor overleaf/main main; then
  echo "Sync aborted: overleaf/main contains changes not present locally." >&2
  exit 1
fi

git push origin main
git push overleaf main

echo "GitHub and Overleaf are synchronized with local main."
