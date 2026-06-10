# PuzzleProof Studio MSI Installer Notes

MSI packaging should be done on Windows after the portable PyInstaller package has already been built and smoke-tested.

## Prerequisites

- Windows 10 or Windows 11
- A successful portable build at `dist\PuzzleProofStudio\PuzzleProofStudio.exe`
- WiX Toolset 4 or newer, or another Windows MSI packaging tool

## Recommended Flow

1. Build the portable executable package:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\build-windows.ps1 -Zip
   ```

2. Launch and smoke-test:

   ```powershell
   .\dist\PuzzleProofStudio\PuzzleProofStudio.exe
   ```

3. Confirm the package includes the required folders:

   - `assets`
   - `licenses`
   - `docs`
   - `catalog`
   - `exports`
   - `VERSION`

4. Use WiX or equivalent installer tooling to package `dist\PuzzleProofStudio` as the application directory.

## Linux Limitation

This repository can prepare the PyInstaller build script on Linux, but a real Windows MSI should not be treated as complete until it has been built and tested on Windows. MSI validation depends on Windows installer services and Windows-specific packaging tools.
