#!/usr/bin/env bash
set -euo pipefail

cat <<'MESSAGE'
PuzzleProof Studio Windows packaging guide

This helper does not build a Windows executable from Linux. Use it as the
checklist for Sean's first Windows 10/11 packaging test on a Windows machine.

Recommended first-pass Windows build:

  1. Install Python 3.11 or 3.12 for Windows from python.org.
     Enable "Add python.exe to PATH" during install.

  2. From the PuzzleProof Studio project folder, create a virtual environment:

       py -3.12 -m venv .venv
       .venv\Scripts\activate

     If Python 3.12 is not installed, use:

       py -3.11 -m venv .venv
       .venv\Scripts\activate

  3. Install runtime and packaging dependencies:

       python -m pip install --upgrade pip
       python -m pip install -r requirements.txt
       python -m pip install pyinstaller

  4. Smoke-test the app before packaging:

       python src\main.py

  5. Build the executable:

       pyinstaller --noconfirm --clean --windowed ^
         --name PuzzleProofStudio ^
         --icon assets\icons\puzzleproof-icon.ico ^
         --add-data "VERSION;." ^
         --add-data "assets;assets" ^
         --add-data "licenses;licenses" ^
         src\main.py

     If assets\icons\puzzleproof-icon.ico has not been generated yet, omit
     the --icon line for the first smoke test. Convert
     assets\icons\puzzleproof-icon.svg to .ico before release-candidate zips.

  6. Test the built app:

       dist\PuzzleProofStudio\PuzzleProofStudio.exe

Expected output location:

  dist\PuzzleProofStudio\

Release zip for Sean after Windows 10/11 smoke testing:

  powershell Compress-Archive -Path dist\PuzzleProofStudio -DestinationPath PuzzleProofStudio-v0.2.0-beta-windows.zip -Force

Do not treat the Windows package as complete until it has launched on Windows
10 and Windows 11, displayed an Active license, and rendered every tab.

Windows 7 is best-effort only. Modern Python and PyInstaller releases have
limited or dropped Windows 7 support, so validate Windows 10/11 first.

See docs/windows-build-notes.md for the full notes.
MESSAGE
