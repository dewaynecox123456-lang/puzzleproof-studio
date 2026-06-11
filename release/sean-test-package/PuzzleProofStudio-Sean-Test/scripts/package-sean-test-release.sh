#!/usr/bin/env bash
set -euo pipefail

PACKAGE_NAME="puzzleproof-studio-v0.1.0-build3.1-sean-test"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE_DIR="$ROOT_DIR/release"
STAGING_DIR="$RELEASE_DIR/$PACKAGE_NAME"
ZIP_PATH="$RELEASE_DIR/$PACKAGE_NAME.zip"

cd "$ROOT_DIR"

mkdir -p "$RELEASE_DIR"
rm -rf "$STAGING_DIR" "$ZIP_PATH"
mkdir -p "$STAGING_DIR"

copy_path() {
  local source="$1"
  local destination="$STAGING_DIR/$source"

  if [ ! -e "$source" ]; then
    echo "Missing required release file: $source" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$destination")"
  cp -R "$source" "$destination"
}

copy_path "src"
copy_path "assets"
copy_path "docs/test-plan.md"
copy_path "docs/windows-build-notes.md"
copy_path "docs/release-checklist-sean.md"
copy_path "README.md"
copy_path "LICENSE_NOTES.md"
copy_path "VERSION"
copy_path "requirements.txt"
copy_path "scripts/run-linux.sh"
copy_path "scripts/build-windows.sh"
copy_path "licenses/sample-license.json"

cat > "$STAGING_DIR/RELEASE_NOTES.txt" <<'NOTES'
PuzzleProof Studio v0.1.0-Build3.1 Sean Test Release

EARLY ACCESS WARNING
This is an Early Access test build for Sean validation. It is intended for
workflow testing, packaging testing, and feedback. It is not a final production
release.

VERSION
0.1.0-Build3.1 Sean Test

WHAT WORKS
- Fedora launch path with bash scripts/run-linux.sh
- Tkinter desktop interface
- Offline license loading with sample fallback
- Active sample license display
- Project save with auto-generated Catalog ID
- Project JSON output under jobs/
- Catalog update in catalog/catalog.json
- Catalog search by Artist Name, Artwork Title, and Catalog ID
- Image conversion/export workflow
- Print-ready HTML document generation
- Open Exports Folder action
- Support and About screens

KNOWN LIMITATIONS
- Windows executable must still be built and tested on Windows 10/11.
- Windows 7 support is best-effort due to modern Python/PyInstaller limits.
- Print document templates are functional but basic.
- Catalog storage is local JSON, not a multi-user database.
- No cloud activation or online sync is included.
- No inventory, supply tracking, accounting, shipping, or CRM features are included.

WHERE TO PUT LICENSE.JSON
For a private/offline license, place the file here after unzipping:

  licenses/license.json

Do not commit or share private license.json files. If no private license is
present, the app falls back to licenses/sample-license.json for Early Access
testing.

SUPPORT
support@bayoufinds.com
NOTES

find "$STAGING_DIR" \( -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" \) -prune -exec rm -rf {} +
rm -rf "$STAGING_DIR/.git" "$STAGING_DIR/.venv" "$STAGING_DIR/data/logs" "$STAGING_DIR/data/backups" "$STAGING_DIR/jobs" "$STAGING_DIR/exports"
rm -f "$STAGING_DIR/licenses/license.json"

(
  cd "$RELEASE_DIR"
  zip -qr "$ZIP_PATH" "$PACKAGE_NAME"
)

echo "Created: $ZIP_PATH"

if unzip -Z1 "$ZIP_PATH" | grep -E '(^|/)(\.git|\.venv|__pycache__)(/|$)|\.py[co]$|(^|/)licenses/license\.json$|(^|/)(jobs|exports)(/|$)|(^|/)data/(logs|backups)(/|$)' >/dev/null; then
  echo "Release validation failed: excluded files were found in the zip." >&2
  unzip -Z1 "$ZIP_PATH" | grep -E '(^|/)(\.git|\.venv|__pycache__)(/|$)|\.py[co]$|(^|/)licenses/license\.json$|(^|/)(jobs|exports)(/|$)|(^|/)data/(logs|backups)(/|$)' >&2
  exit 1
fi

echo "Validation passed: no private license, cache, or local runtime files found."
rm -rf "$STAGING_DIR"
echo "Cleaned staging folder."
