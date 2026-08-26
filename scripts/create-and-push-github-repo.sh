#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER="${T4H_GITHUB_OWNER:-TML-4PM}"
REPO="${T4H_GITHUB_REPO:-T4H-goose-recipes}"
FULL="$OWNER/$REPO"
cd "$ROOT"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required to create the remote repository automatically." >&2
  echo "Install/authenticate gh, then rerun this script." >&2
  exit 2
fi
gh auth status >/dev/null
if ! gh repo view "$FULL" >/dev/null 2>&1; then
  gh repo create "$FULL" --private --source . --remote origin --push
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "git@github.com:$FULL.git"
  git push -u origin main
fi

git tag -f v1.1.0
git push origin v1.1.0

echo "Canonical recipe repository: $FULL"
echo "Version tag: v1.1.0"
