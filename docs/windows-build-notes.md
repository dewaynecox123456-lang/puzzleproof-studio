# PuzzleProof Studio Windows Build Notes

Version target: `0.1.0-EarlyAccess`

These notes prepare the Windows packaging path for Sean testing. A Windows executable is not complete until it has been built and tested on Windows.

## First Testing Target

Validate on Windows 10 and Windows 11 first.

Windows 7 support is best-effort because modern Python and PyInstaller releases have limited or dropped Windows 7 support. Do not block the first Sean test package on Windows 7 unless a specific Windows 7 machine must be supported.

## Recommended Build Environment

- Windows 10 or Windows 11
- Python 3.11 or 3.12 from python.org
- Project files copied or cloned locally
- PowerShell or Command Prompt

During Python installation, enable `Add python.exe to PATH`.

## Build Steps

From the PuzzleProof Studio project folder:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-windows.ps1
```

That script creates `.venv-build-windows`, installs `requirements.txt` and PyInstaller, runs `python -m py_compile src\main.py`, and builds:

```text
dist\PuzzleProofStudio\PuzzleProofStudio.exe
```

To also create a portable zip:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-windows.ps1 -Zip
```

The PyInstaller package includes:

- `assets`
- `licenses\sample-license.json`
- `docs`
- `catalog`
- `exports`
- `VERSION`
- `README.txt`
- `INSTALL.txt`
- `LICENSE_SETUP.txt`
- `FAQ.txt`

To perform the same build manually after creating and activating a Windows virtual environment:

```bat
pyinstaller --noconfirm --clean --windowed ^
  --name PuzzleProofStudio ^
  --icon assets\icons\puzzleproof-icon.ico ^
  --distpath dist ^
  --workpath build\pyinstaller ^
  --specpath build\pyinstaller ^
  --add-data "VERSION;." ^
  --add-data "assets;assets" ^
  --add-data "licenses\sample-license.json;licenses" ^
  --add-data "docs;docs" ^
  --add-data "catalog;catalog" ^
  --add-data "exports;exports" ^
  --add-data "README.txt;." ^
  --add-data "INSTALL.txt;." ^
  --add-data "LICENSE_SETUP.txt;." ^
  --add-data "FAQ.txt;." ^
  src\main.py
```

If `assets\icons\puzzleproof-icon.ico` has not been created yet, omit the `--icon` line for the first smoke test. The placeholder source art is in `assets\icons\puzzleproof-icon.svg`; convert that SVG to a Windows `.ico` before a release candidate.

Run the packaged app:

```bat
dist\PuzzleProofStudio\PuzzleProofStudio.exe
```

## Sean Test Checklist

- App launches without a console window.
- Title bar says exactly `PuzzleProof Studio v0.1.0-EarlyAccess`.
- Splash screen appears with cream background, dark green frame, large puzzle icon, PuzzleProof Studio title, Professional Puzzle Production Suite subtitle, BayouFinds / Wonder Piece Studio, version badge, license status card, bayou footer, and loading progress.
- License status displays `Active`.
- Project, Image Conversion, Catalog, Printing, Support, and About tabs render.
- A new project can be saved.
- Existing sample license is bundled and found.
- Support info clearly shows version, license status, OS, app folder, and logs folder.
- App icon appears in the Windows title bar/taskbar after the `.ico` is included.

## Packaging Notes

The first pass should use PyInstaller's folder output at `dist\PuzzleProofStudio\`. A single-file executable can be evaluated later, but folder output is easier to inspect and debug during Early Access.

If assets or license files are missing in the packaged app, confirm the `--add-data` entries use Windows semicolon syntax:

```bat
--add-data "source;destination"
```

Linux and macOS use a colon for `--add-data`, but these notes are for a Windows build machine.

The build intentionally includes `licenses\sample-license.json` instead of the entire `licenses` folder so a private `licenses\license.json` is not accidentally bundled.

## Icon Plan

- Keep placeholder files under `assets\icons\`.
- Use `assets\icons\puzzleproof-icon.svg` as the editable source concept.
- Generate `assets\icons\puzzleproof-icon.ico` for Windows packaging.
- Keep `assets\icons\puzzleproof-icon.xbm` for the lightweight Linux Tkinter window icon.
- Pass the Windows icon to PyInstaller with `--icon assets\icons\puzzleproof-icon.ico`.

## Release Zip Handoff

After Windows 10/11 smoke testing passes, zip the folder output, not just the `.exe`:

```bat
powershell Compress-Archive -Path dist\PuzzleProofStudio -DestinationPath PuzzleProofStudio-v0.1.0-EarlyAccess-windows.zip -Force
```

Sean should receive:

- `PuzzleProofStudio-v0.1.0-EarlyAccess-windows.zip`
- A short note that this is an Early Access Windows 10/11 test build
- The expected launch path after unzip: `PuzzleProofStudio\PuzzleProofStudio.exe`
- The Sean test checklist above

## MSI Installer

MSI packaging requires Windows tooling such as the WiX Toolset or Visual Studio installer tooling. This Linux development environment cannot produce or validate a Windows MSI. Prepare and test the portable EXE package first, then follow `docs/msi-installer-notes.md` on a Windows machine if an MSI installer is required.

## Not Complete Until Tested

Do not claim the Windows build is complete until the executable has been produced on Windows and the Sean test checklist has passed on Windows 10/11.
