# Sean Test Release Checklist

Package target: `PuzzleProofStudio-v0.1.3.2-Windows.zip`

## Before Sending

1. Build the release zip from a clean working copy:

   ```bash
   bash scripts/package-sean-test-release.sh
   ```

2. Confirm the script reports no private license, cache, or runtime files.
3. Confirm the package contains `licenses/sample-license.json`.
4. Confirm `licenses/license.json` is not included.
5. Confirm `RELEASE_NOTES.txt` is included.

## Fedora Smoke Test

1. Unzip the package into a temporary folder.
2. Run:

   ```bash
   bash scripts/run-linux.sh
   ```

3. Verify the app launches.
4. Verify the license shows `Active`.
5. Verify all tabs render.
6. Save a test project.
7. Search the Catalog by Artist Name, Artwork Title, and Catalog ID.
8. Generate one print-ready HTML file.
9. Use Open Exports Folder to find the generated file.
10. In Image Conversion, confirm DOCX is the default output format.
11. Confirm artwork placement defaults to `Fit Entire Artwork / Preserve Full Image`.
12. Export a portrait or mismatched-aspect image to DOCX and confirm the full artwork is visible.
13. Select `Fill Puzzle Area / Crop to Fill` and confirm the crop warning appears before export.

## Windows Handoff

Send Sean the release zip and ask him to test Windows 10/11 first. Windows 7 is best-effort only.

Sean should unzip the package, follow `docs/windows-build-notes.md`, and run the app before packaging:

```bat
python src\main.py
```

After PyInstaller packaging, Sean should launch:

```bat
dist\PuzzleProofStudio\PuzzleProofStudio.exe
```

## Do Not Include

- `.git`
- `.venv`
- `__pycache__`
- `licenses/license.json`
- local `jobs/`
- local `exports/`
- `data/logs/`
- `data/backups/`
