# PuzzleProof Studio FAQ

## Installation

### How do I install PuzzleProof Studio on Windows?

Unzip `PuzzleProofStudio-v0.1.3.2-Windows.zip`, open the `PuzzleProofStudio` folder, and double-click `PuzzleProofStudio.exe`. You do not need to install Python and you do not need to use PowerShell.

### What should I do if Windows SmartScreen appears?

During Early Access, the app may be unsigned. Choose More Info, then Run Anyway only if the ZIP came directly from BayouFinds / Wonder Piece Studio.

## Licensing

### How do I activate a license?

Place your private license file named `license.json` in the `licenses` folder next to `PuzzleProofStudio.exe`, then close and reopen the app.

### Where does license.json go?

Put it here after extracting the ZIP:

`PuzzleProofStudio\licenses\license.json`

### What happens if I do not have a license file yet?

During Early Access, the app can use the included sample license so testing is not blocked.

## Projects

### How do I create a project?

Open the Project tab, enter the artist name, artwork title, contact details, copyright owner, approval status, and project notes. Click Save Project before exporting artwork or generating print files.

### Where are project records saved?

Project JSON files are saved in the `jobs` folder. Catalog metadata is saved in `catalog\catalog.json`.

## Artwork

### How do I import artwork?

Open the Image Conversion tab, choose the source artwork file, select the production output preset, choose PNG, JPG, or DOCX, confirm the artwork placement mode, then run the export action.

DOCX is the default because it is available as transition comfort for users who are comfortable printing from Microsoft Word. PNG and JPG are available for direct image workflows. The main goal is eliminating repeated resizing, cropping, and positioning for Puzzle Print, Box Insert, and Box Sticker / Label outputs.

### Why does my export have borders or letterboxing?

`Fit Entire Artwork / Preserve Full Image` is the default artwork placement mode. It preserves the full source image when the artwork shape does not match the selected output preset. Borders or letterboxing are expected in this mode. Use `Fill Puzzle Area / Crop to Fill` only when you intentionally want the image to fill the whole production area and accept that parts of the artwork may be cropped.

After export, PuzzleProof shows the selected preset, output format, artwork placement mode, full saved path, suggested printer type, and file/folder opening actions.

Suggested printer guidance:

- Puzzle Print: Sublimation printer / sublimation paper
- Box Insert: Standard printer / regular paper
- Box Sticker / Label: Sticker paper or label printer

### My artwork import or export failed. What should I check?

Confirm the source image still exists, the file is a supported image format, and the app has permission to write into the `exports` folder.

## Printing

### How do I generate print files?

Save the project, then open the Printing tab and choose the document or production package you need. Generated HTML files are saved in the `exports` folder.

### Does PuzzleProof Studio print directly to my printer?

The current workflow creates print-ready files for review. Native printer selection is not part of this Early Access build.

## Catalog

### How do I find a saved project?

Use the Catalog tab to search by artist name, artwork title, or catalog ID. Use Show All to reset filters.

## Support

### How do I find support links?

Open Help > FAQ for support links, Help > Contact Support to start an email, Help > Report Issue for the issue tracker, or Help > Product Website for the product page.

### Where are logs saved?

Logs are saved in the `logs` folder next to `PuzzleProofStudio.exe`. Use Help > Open Logs Folder to open that folder.

### What should I do if the app will not launch?

Re-extract the ZIP into a normal folder such as Documents, confirm `PuzzleProofStudio.exe` is still inside the `PuzzleProofStudio` folder, and try again. If it still will not launch, send the latest file from the `logs` folder plus your Windows version to support.

### How do I contact support?

Use Help > Contact Support, copy the Support tab information, and include the steps that led to the problem.

## Links

### Product Website

https://puzzleproof-studio.netlify.app/

### BayouFinds

https://www.bayoufinds.com

### GitHub Repository

https://github.com/dewaynecox123456-lang/puzzleproof-studio

### Bug Reports

https://github.com/dewaynecox123456-lang/puzzleproof-studio/issues
