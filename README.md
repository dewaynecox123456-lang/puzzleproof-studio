# PuzzleProof Studio

Version: 0.1.3.2-SeanValidation

v0.1.3.1 SeanValidation includes an export user experience update and refreshed application artwork.
v0.1.3.2 SeanValidation makes export placement crop-safe by default. The Image Conversion tab now defaults to `Fit Entire Artwork / Preserve Full Image`, which preserves the full source artwork in DOCX, PNG, and JPG exports. `Fill Puzzle Area / Crop to Fill` remains available, but the app warns that it may crop parts of the artwork before continuing.

PuzzleProof Studio is a desktop utility for the BayouFinds / Wonder Piece Studio artist-to-puzzle workflow. It creates project records, tracks artist permission, imports artwork, exports manufacturing-sized images, stores catalog metadata, and creates print-ready production documents.

## Run on Fedora

Install the OS Tkinter package first if it is not already present:

```bash
sudo dnf install python3-tkinter
```

```bash
bash scripts/run-linux.sh
```

The script creates `.venv`, installs `requirements.txt`, and runs `src/main.py`.

## Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

## Current Scope

- Splash screen with version, copyright, and license status
- Project tab for artist/project metadata and approval tracking
- Image Conversion tab for one customer image import and preset Puzzle Print, Box Insert, or Box Sticker / Label exports
- Catalog tab backed by JSON records
- Printing tab that creates print-ready HTML files
- Support and About tabs
- Help menu with FAQ, support links, documentation, issue reporting, and product website links
- Offline license check using `licenses/license.json` or `licenses/sample-license.json`

## Manufacturing Sizes

- Puzzle Print: 8.83 x 11.77 inches at 300 DPI
- Box Sticker / Label: 4.37 x 5.10 inches at 300 DPI
- Box Insert: 3.75 x 5.00 inches at 300 DPI

## Preset Output Workflow

PuzzleProof Studio exports preset production outputs from one customer image so users do not have to repeatedly resize, crop, and position artwork for every order. Word is Sean's current manual workaround, not a technical requirement for the product.

- DOCX output is retained as transition comfort for users moving away from Word-based manual setup.
- PNG and JPG output remain available for direct print-ready image workflows.
- The current workflow is limited to one customer image and the three production outputs above. Batch processing and social media package generation are intentionally out of scope.

The Image Conversion tab defaults to DOCX for Sean's current comfort level, while keeping PNG and JPG available for direct image workflows. Artwork placement defaults to `Fit Entire Artwork / Preserve Full Image` so mismatched or portrait artwork is not cropped. After each export, the app shows the selected preset, output format, artwork placement mode, full saved path, suggested printer type, and export-opening actions.

Suggested printer guidance:

- Puzzle Print: Sublimation printer / sublimation paper
- Box Insert: Standard printer / regular paper
- Box Sticker / Label: Sticker paper or label printer

## Folder Structure

- `src/` - application code
- `jobs/` - saved project folders
- `catalog/` - catalog JSON data
- `exports/` - exported images and print-ready files
- `licenses/` - offline license files
- `assets/templates/` - document templates
- `data/settings/` - app settings
- `data/logs/` - support logs folder
- `docs/` - product and handoff documentation
- `docs/FAQ.md` - single source for built-in FAQ viewer content

## Windows Packaging

Windows packaging is prepared for a first PyInstaller test on Windows 10/11. `scripts/build-windows.sh` prints the recommended Windows build steps, and detailed notes are in `docs/windows-build-notes.md`.

Do not treat the Windows executable as complete until it has been built and tested on Windows 10/11. Windows 7 support is best-effort because modern Python and PyInstaller support is limited there.

## Support

Website: https://puzzleproof-studio.netlify.app/

BayouFinds: https://www.bayoufinds.com

Support: support@bayoufinds.com
