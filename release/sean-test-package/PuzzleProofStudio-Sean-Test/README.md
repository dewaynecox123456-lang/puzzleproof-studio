# PuzzleProof Studio

Version: 0.1.0-EarlyAccess

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
- Image Conversion tab for PNG/JPG imports and Puzzle, Sticker, or Insert exports
- Catalog tab backed by JSON records
- Printing tab that creates print-ready HTML files
- Support and About tabs
- Offline license check using `licenses/license.json` or `licenses/sample-license.json`

## Manufacturing Sizes

- Puzzle Image: 8.83 x 11.77 inches at 300 DPI
- Sticker Image: 4.37 x 5.10 inches at 300 DPI
- Insert Image: 3.75 x 5.00 inches at 300 DPI

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

## Windows Packaging

Windows packaging is prepared for a first PyInstaller test on Windows 10/11. `scripts/build-windows.sh` prints the recommended Windows build steps, and detailed notes are in `docs/windows-build-notes.md`.

Do not treat the Windows executable as complete until it has been built and tested on Windows 10/11. Windows 7 support is best-effort because modern Python and PyInstaller support is limited there.

## Support

Website: https://bayoufinds.com

Support: support@bayoufinds.com
