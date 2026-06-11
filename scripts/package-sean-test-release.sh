#!/usr/bin/env bash
set -euo pipefail

APP_NAME="PuzzleProofStudio"
ZIP_NAME="PuzzleProofStudio-v0.1.0-Windows.zip"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist/$APP_NAME"
EXE_PATH="$DIST_DIR/$APP_NAME.exe"
RELEASE_DIR="$ROOT_DIR/release"
ZIP_PATH="$RELEASE_DIR/$ZIP_NAME"

cd "$ROOT_DIR"

if [ ! -f "$EXE_PATH" ]; then
  cat >&2 <<MESSAGE
Missing required Windows executable:
  $EXE_PATH

Build it first on Windows:
  powershell -ExecutionPolicy Bypass -File scripts\\build-windows.ps1 -Zip
MESSAGE
  exit 1
fi

mkdir -p "$RELEASE_DIR"
rm -f "$ZIP_PATH"

for required in README.txt FAQ.txt INSTALL.txt LICENSE_SETUP.txt; do
  if [ ! -f "$required" ]; then
    echo "Missing required customer file: $required" >&2
    exit 1
  fi
  cp "$required" "$DIST_DIR/$required"
done

mkdir -p "$DIST_DIR/exports" "$DIST_DIR/jobs" "$DIST_DIR/catalog" "$DIST_DIR/licenses" "$DIST_DIR/data/settings"
cp "licenses/sample-license.json" "$DIST_DIR/licenses/sample-license.json"
rm -f "$DIST_DIR/licenses/license.json"
[ -f "$DIST_DIR/catalog/catalog.json" ] || printf '[]\n' > "$DIST_DIR/catalog/catalog.json"

(
  cd "$ROOT_DIR/dist"
  zip -qr "$ZIP_PATH" "$APP_NAME"
)

entries="$(unzip -Z1 "$ZIP_PATH")"

for required in \
  "$APP_NAME/$APP_NAME.exe" \
  "$APP_NAME/README.txt" \
  "$APP_NAME/FAQ.txt" \
  "$APP_NAME/INSTALL.txt" \
  "$APP_NAME/LICENSE_SETUP.txt"; do
  if ! grep -Fx "$required" <<<"$entries" >/dev/null; then
    echo "Customer package validation failed: missing $required" >&2
    exit 1
  fi
done

blocked="$(grep -E '(^|/)src/|(^|/)requirements\.txt$|(^|/)scripts/|(^|/)license\.json$' <<<"$entries" || true)"
if [ -n "$blocked" ]; then
  echo "Customer package validation failed. Blocked files found:" >&2
  echo "$blocked" >&2
  exit 1
fi

echo "Created: $ZIP_PATH"
echo "Validation passed: customer ZIP includes EXE and support docs without src/ or requirements.txt."
