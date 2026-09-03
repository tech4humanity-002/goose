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

# Optionally create/update the canonical private GitHub recipe repository automatically.
# This is enabled by default for the requested T4H bootstrap; set T4H_AUTO_CREATE_REPO=0 to skip.
if [[ "${T4H_AUTO_CREATE_REPO:-1}" == "1" ]] && command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    OWNER="${T4H_GITHUB_OWNER:-TML-4PM}"
    REPO="${T4H_GITHUB_REPO:-T4H-goose-recipes}"
    FULL="$OWNER/$REPO"
    if ! gh repo view "$FULL" >/dev/null 2>&1; then
      (cd "$INSTALL_DIR" && gh repo create "$FULL" --private --source . --remote origin --push)
    elif [[ -d "$INSTALL_DIR/.git" ]]; then
      git -C "$INSTALL_DIR" remote get-url origin >/dev/null 2>&1 || git -C "$INSTALL_DIR" remote add origin "git@github.com:$FULL.git"
      git -C "$INSTALL_DIR" push -u origin main
    fi
    git -C "$INSTALL_DIR" tag -f v1.1.0 2>/dev/null || true
    git -C "$INSTALL_DIR" push origin v1.1.0 2>/dev/null || true
    export T4H_GOOSE_REPO_URL="${T4H_GOOSE_REPO_URL:-https://github.com/$FULL.git}"
    export GOOSE_RECIPE_GITHUB_REPO="$FULL"
  else
    echo "WARN: gh is installed but not authenticated; remote recipe repo creation skipped." >&2
  fi
fi

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
exec goose "$@"
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
