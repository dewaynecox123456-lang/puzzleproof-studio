# Codex Build Prompt: PuzzleProof Studio

You are working inside this project:

~/BayouFinds/products/puzzleproof-studio

Read and follow:

- docs/specification.md
- assets/legal/feature-governance-policy.md
- VERSION

Build the first working scaffold for PuzzleProof Studio v0.1.0-EarlyAccess.

## Product Summary

PuzzleProof Studio is a small desktop application for Sean’s artist-to-puzzle workflow.

It must help Sean:

- Create artist/project records
- Track artist permission
- Import artwork photos
- Convert images into required manufacturing sizes
- Add copyright/branding overlays
- Save projects to catalog
- Reprint previous jobs
- Print release forms, inserts, stickers, puzzle covers, and production sheets
- Use the same BayouFinds offline license model as our other software

Manufacturing sizes come from Sean’s puzzle image sizing document:

- Puzzle Image: 8.83 inches wide x 11.77 inches high
- Sticker Image: 4.37 inches wide x 5.10 inches high
- Insert Image: 3.75 inches wide x 5.00 inches high
- Default DPI: 300

## Development Rules

Do not overbuild.

Do not add unrelated features.

Every feature must support at least one:

- Protect the artist
- Protect Sean
- Improve production
- Improve cataloging
- Improve printing
- Improve reprints
- Improve manufacturing

If a feature does not support the workflow, do not add it.

## Technical Direction

Use Python.

Preferred stack:

- Python 3
- Tkinter or PySide6
- Pillow for image processing
- JSON for catalog/project storage

Keep it portable.

Develop on Fedora 42.

Prepare for Windows 7 through Windows 11 compatibility.

Avoid anything that requires cloud services or online activation.

## Required Files To Create

Create or update:

- src/main.py
- src/license_manager.py
- src/catalog_manager.py
- src/image_processor.py
- src/print_manager.py
- src/project_manager.py
- src/support_info.py
- requirements.txt
- README.md
- LICENSE_NOTES.md
- docs/changelog.md
- assets/legal/feature-governance-policy.md
- assets/templates/artist-release-template.md
- assets/templates/copyright-template.md
- assets/templates/production-sheet-template.md
- assets/templates/certificate-template.md
- scripts/run-linux.sh
- scripts/build-windows.sh
- licenses/sample-license.json
- data/settings/app-settings.json

## Application UI

Create a basic desktop GUI with:

### Splash Screen

Show for 2-3 seconds.

Display:

- PuzzleProof Studio
- Artist-to-Puzzle Production Utility
- Version 0.1.0-EarlyAccess
- BayouFinds / Wonder Piece Studio
- License status
- © 2026 Wonder Piece Studio. All Rights Reserved.

### Main Window

Use tabs or navigation buttons:

1. Project
2. Image Conversion
3. Catalog
4. Printing
5. Support
6. About

## Project Tab

Fields:

- Artist Name
- Artwork Title
- Contact Information
- Copyright Owner
- Company Name
- Project Notes
- Approval Status
- Catalog Number
- Project Origin

Project Origin options:

- Artist Submission
- Company Project
- BayouFinds Original
- Wonder Piece Studio Original

Approval Status options:

- Draft
- Pending
- Approved
- Revoked

Buttons:

- New Project
- Save Project
- Open Project Folder
- Generate Artist Release
- Mark Manufacturing Ready

Manufacturing Ready may only be true if:

- Artist approval exists
- Source image exists
- Copyright owner exists
- Exports exist

## Image Conversion Tab

Features:

- Import source image
- Select export type:
  - Puzzle
  - Sticker
  - Insert
- Apply crop/resize
- Add optional copyright text
- Add optional logo/branding
- Export PNG
- Export JPG

Default copyright text:

© 2026 Wonder Piece Studio. All Rights Reserved.

Copyright placement:

- Bottom Right
- Bottom Left
- Bottom Center

Options:

- Font size
- Opacity
- Text color if simple to implement

Export dimensions at 300 DPI:

Puzzle:
8.83 x 11.77 inches

Sticker:
4.37 x 5.10 inches

Insert:
3.75 x 5.00 inches

## Catalog Tab

Catalog records should use JSON.

Catalog ID format:

WPS-YYYY-000001

Store:

- Catalog ID
- Artist
- Artwork
- Copyright Owner
- Project Origin
- Approval Status
- Manufacturing Ready Status
- Export files
- Print history
- Reprint count
- Last printed date
- Notes

Functions:

- Search catalog
- Open project
- Re-export
- Reprint
- View project metadata

## Printing Tab

Support:

- Print Artist Release
- Print Copyright Form
- Print Production Sheet
- Print Sticker
- Print Insert
- Print Puzzle Cover
- Print Production Package
- Save as PDF where possible

If true native printing is too much for first pass, create print-ready PDF/HTML files and open them from the app.

Do not block the project on perfect printing.

## Support Tab

Display:

- Software name
- Version
- License status
- License expiration
- Support email
- Website
- Operating system
- App folder
- Logs folder

Buttons:

- Open Logs Folder
- Open Project Folder
- Copy Support Info

Contact:

Website:
https://bayoufinds.com

Support Email:
support@bayoufinds.com

## About Tab

Display:

PuzzleProof Studio

Artist-to-Puzzle Production Utility

Built for Sean’s artist-to-puzzle workflow.

Developed by BayouFinds / Wonder Piece Studio.

Website:
https://bayoufinds.com

Support:
support@bayoufinds.com

Copyright:
© 2026 Wonder Piece Studio. All Rights Reserved.

License:
Offline yearly license using license.json.

## Licensing

Implement a simple offline license checker.

Use:

licenses/license.json

If missing, fall back to:

licenses/sample-license.json

License fields:

- product
- licensed_to
- license_key
- issued_date
- expires_date
- status
- seats
- notes

Do not use online activation.

Display warnings when:

- License missing
- License expired
- License expiring within 30 days

Do not make license failure crash the app during Early Access.

## BayouFinds Sample Artwork

Create placeholder support for:

assets/sample-images/bayou-sunset-sample.png

If file does not exist, show placeholder text in the UI:

Bayou Sunset sample image not installed yet.

This image will be a BayouFinds original gift/sample puzzle.

## Documentation

Update README.md with:

- What the app does
- How to run on Fedora
- How to install dependencies
- How to package for Windows later
- Folder structure
- Version
- Support info

Update LICENSE_NOTES.md with:

- Offline licensing explanation
- No online activation
- Yearly license model
- Seller-side ledger concept

Update docs/changelog.md with:

0.1.0-EarlyAccess initial scaffold.

## Scripts

scripts/run-linux.sh:

- Create virtual environment if missing
- Install requirements
- Run src/main.py

scripts/build-windows.sh:

- Placeholder script
- Explain that Windows packaging will use PyInstaller later
- Do not claim final Windows build is complete

## Acceptance Criteria

After build, I should be able to run:

bash scripts/run-linux.sh

And see:

- Splash screen
- Main app window
- Project tab
- Image conversion tab
- Catalog tab
- Printing tab
- Support tab
- About tab

The app should not crash if no image or license exists.

Use clean code.

Keep it simple.

Do not add AI, CRM, accounting, social media, or unrelated features.
