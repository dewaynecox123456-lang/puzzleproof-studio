# Known Issues

## Active

### Windows SmartScreen may warn on first launch

Early Access builds are unsigned. Windows may show a SmartScreen warning until a signed installer is available.

Workaround: Only run the package if it came directly from BayouFinds / Wonder Piece Studio.

### No MSI installer yet

The current Windows release is a portable ZIP package.

Workaround: Extract the ZIP and double-click `PuzzleProofStudio.exe`.

### Local JSON catalog only

Catalog storage is local to the extracted app folder and is not multi-user or cloud-synced.

Workaround: Treat this build as a single-user testing workflow.

## Resolved

### Tester package required Python

Resolved in `PuzzleProofStudio-v0.1.0-Windows.zip`. The customer package includes `PuzzleProofStudio.exe` and the bundled runtime.

### Tester package required PowerShell launch

Resolved in `PuzzleProofStudio-v0.1.0-Windows.zip`. Testers launch by double-clicking the EXE.
