#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GOOSE_CONFIG_DIR="${HOME}/.config/goose"
INSTALL_DIR="$GOOSE_CONFIG_DIR/t4h-goose"
RECIPE_DIR="$GOOSE_CONFIG_DIR/t4h-recipes"
mkdir -p "$GOOSE_CONFIG_DIR" "$HOME/bin" "$RECIPE_DIR"

if ! command -v goose >/dev/null 2>&1; then
  echo "Goose CLI is not installed." >&2
  echo "Install Goose, then rerun this installer." >&2
  exit 2
fi

rm -rf "$INSTALL_DIR"
cp -R "$ROOT" "$INSTALL_DIR"

# Installation is deliberately local-only. Repository creation, commits, tags and
# pushes are release operations and must never occur as an installer side effect.

# Prefer a canonical GitHub recipe repository when configured; otherwise use the bundled recipes.
if [[ -n "${T4H_GOOSE_REPO_URL:-}" ]]; then
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  if command -v git >/dev/null 2>&1; then
    git clone --depth 1 "$T4H_GOOSE_REPO_URL" "$TMP/repo"
    rm -rf "$RECIPE_DIR"/*
    cp -R "$TMP/repo/recipes"/* "$RECIPE_DIR/"
    cp "$TMP/repo/registry/recipe-index.yaml" "$GOOSE_CONFIG_DIR/t4h-recipe-index.yaml" 2>/dev/null || true
  else
    echo "git is required for T4H_GOOSE_REPO_URL" >&2
    exit 3
  fi
else
  rm -rf "$RECIPE_DIR"/*
  cp -R "$INSTALL_DIR/recipes"/* "$RECIPE_DIR/"
  cp "$INSTALL_DIR/registry/recipe-index.yaml" "$GOOSE_CONFIG_DIR/t4h-recipe-index.yaml"
fi

# Add the permanent T4H recipe directory without destroying an existing user path.
if [[ -n "${GOOSE_RECIPE_PATH:-}" ]]; then
  export GOOSE_RECIPE_PATH="$RECIPE_DIR:$GOOSE_RECIPE_PATH"
else
  export GOOSE_RECIPE_PATH="$RECIPE_DIR"
fi

WRAPPER="$HOME/bin/t4h-goose"
cat > "$WRAPPER" <<'WRAP'
#!/usr/bin/env bash
set -euo pipefail
export GOOSE_RECIPE_PATH="$HOME/.config/goose/t4h-recipes${GOOSE_RECIPE_PATH:+:$GOOSE_RECIPE_PATH}"
ARGS=()
if [[ -n "${T4H_BAD_MCP_URI:-}" && -n "${T4H_BAD_MCP_CMD:-}" ]]; then
  echo "Set only one of T4H_BAD_MCP_URI or T4H_BAD_MCP_CMD." >&2
  exit 64
elif [[ -n "${T4H_BAD_MCP_URI:-}" ]]; then
  ARGS+=(--with-streamable-http-extension "$T4H_BAD_MCP_URI")
elif [[ -n "${T4H_BAD_MCP_CMD:-}" ]]; then
  ARGS+=(--with-extension "$T4H_BAD_MCP_CMD")
fi
exec goose "${ARGS[@]}" "$@"
WRAP
chmod +x "$WRAPPER"

# Project hints are copied only when absent.
if [[ -d .git && ! -e .goosehints ]]; then cp "$INSTALL_DIR/.goosehints" .goosehints; fi

# Validate every recipe when the installed Goose CLI supports validation.
if goose recipe validate --help >/dev/null 2>&1; then
  while IFS= read -r -d '' recipe; do
    goose recipe validate "$recipe"
  done < <(find "$RECIPE_DIR" -type f -name '*.yaml' -print0)
fi

echo "T4H Goose installed."
echo "Recipe path: $GOOSE_RECIPE_PATH"
echo "List:        goose recipe list --verbose"
echo "Review:      goose run --recipe t4h-recipe-review-worker.yaml --params review_date=$(date +%F)"
echo "Doctor:      $INSTALL_DIR/scripts/doctor.sh"
