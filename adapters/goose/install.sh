#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ADAPTER_ROOT="$REPO_ROOT/adapters/goose"
GOOSE_CONFIG_DIR="$HOME/.config/goose"
RECIPE_DIR="$GOOSE_CONFIG_DIR/t4h-recipes"

command -v goose >/dev/null 2>&1 || {
  echo "Goose CLI is not installed." >&2
  exit 2
}

python3 "$REPO_ROOT/compiler/compile_adapters.py" --check
mkdir -p "$RECIPE_DIR" "$HOME/bin"
find "$RECIPE_DIR" -mindepth 1 -maxdepth 1 -type f -name 't4h-*.yaml' -delete
cp "$ADAPTER_ROOT/generated/recipes/"*.yaml "$RECIPE_DIR/"
sed "s|^ROOT=.*|ROOT=\"$REPO_ROOT\"|" "$ADAPTER_ROOT/bin/t4h-goose" > "$HOME/bin/t4h-goose"
chmod +x "$HOME/bin/t4h-goose"

if goose recipe validate --help >/dev/null 2>&1; then
  while IFS= read -r -d '' recipe; do
    goose recipe validate "$recipe"
  done < <(find "$RECIPE_DIR" -type f -name '*.yaml' -print0)
fi

echo "Goose adapter installed from T4H Agent Operating Contract."
echo "Contract:  $REPO_ROOT/contract"
echo "Recipes:   $RECIPE_DIR"
echo "Entrypoint: $HOME/bin/t4h-goose"
