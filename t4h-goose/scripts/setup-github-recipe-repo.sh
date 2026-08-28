#!/usr/bin/env bash
set -euo pipefail
# Creates/initialises a local Git repository ready to push to the intended GitHub repo.
# Remote creation requires authenticated GitHub CLI or GitHub connector support on the user's machine.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if [[ ! -d .git ]]; then git init -b main; fi
git add .
git commit -m "feat: T4H Goose recipes v1.1.0" || true
echo "Local recipe repository ready at $ROOT"
echo "Set a remote and push with:"
echo "  git remote add origin git@github.com:TML-4PM/T4H-goose-recipes.git"
echo "  git push -u origin main"
