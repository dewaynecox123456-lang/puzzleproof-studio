# PuzzleProof Studio Test Plan

Version target: `0.1.0-EarlyAccess`

Run the app from the project root:

```bash
bash scripts/run-linux.sh
```

## 1. License Test

Expected result: license status displays `Active`.

Steps:

1. Confirm `licenses/sample-license.json` exists.
2. Confirm no private `licenses/license.json` is required for the app to launch.
3. Launch the app.
4. Verify the splash screen shows license status.
5. Open the Support tab.
6. Verify Support info includes license status and expiration date.

## 2. Project Save Test

Expected result: a project JSON file is saved under `jobs/`, and `catalog/catalog.json` is created or updated.

Steps:

1. Open the Project tab.
2. Enter Artist Name, Artwork Title, Copyright Owner, and optional notes.
3. Leave Catalog Number blank.
4. Click Save Project.
5. Verify the confirmation dialog shows the saved project JSON path and catalog path.
6. Verify the Catalog Number field was auto-filled.
7. Verify a project folder exists under `jobs/`.
8. Verify `catalog/catalog.json` contains the saved catalog record.

## 3. Catalog Search Test

Expected result: matching records display cleanly in the Catalog table.

Steps:

1. Open the Catalog tab.
2. Search by Artist Name.
3. Search by Artwork Title.
4. Search by Catalog ID.
5. Combine two fields, such as Artist Name and Artwork Title.
6. Click Show All.
7. Verify the matching record count updates.
8. Verify columns show Catalog ID, Artist, Artwork, Approval, Manufacturing Ready, and Updated.

## 4. Print Output Test

Expected result: generated HTML files are saved under `exports/` and are easy to find.

Steps:

1. Open the Printing tab.
2. Confirm the exports folder path is visible.
3. Generate one print document.
4. Verify the success dialog shows the generated HTML file path.
5. Click Open Exports Folder.
6. Verify the generated HTML file is present.
7. Generate a production package.
8. Verify multiple HTML files are created in `exports/`.

## 5. Preset Output Workflow Test

Expected result: preset production outputs are generated from one customer image without manual resizing or cropping.

Steps:

1. Open the Image Conversion tab.
2. Import one PNG or JPG customer image.
3. Confirm the default output format is `DOCX`.
4. Confirm the default artwork placement is `Fit Entire Artwork / Preserve Full Image`.
5. Import a portrait or mismatched-aspect image and export `Puzzle Print` as `DOCX`.
6. Verify the output preserves the full artwork. Letterboxing or borders are acceptable; unseen artwork must not be lost.
7. Verify the export success details show `Puzzle Print`, `DOCX`, the artwork placement mode, the full saved path, and `Sublimation printer / sublimation paper`.
8. Select `Box Insert`, choose `DOCX`, and export.
9. Verify the export success details show `Box Insert`, `DOCX`, the artwork placement mode, the full saved path, and `Standard printer / regular paper`.
10. Select `Box Sticker / Label`, choose `DOCX`, and export.
11. Verify the export success details show `Box Sticker / Label`, `DOCX`, the artwork placement mode, the full saved path, and `Sticker paper or label printer`.
12. Verify all three DOCX files are created in `exports/`.
13. Verify the DOCX files open in Microsoft Word on Windows.
14. Choose `PNG` or `JPG` for one preset and confirm image output also preserves the full artwork in fit mode.
15. Select `Fill Puzzle Area / Crop to Fill`, export one test file, and confirm the app warns: `This mode may crop parts of the artwork. Continue?`
16. Click Open File, Open Latest Export, and Open Output Folder and confirm each action works.
17. Confirm the output folder is clear and contains the generated preset files.

Note: The Word check validates DOCX transition compatibility only. The core workflow requirement is preset-based output generation that removes repeated resizing, cropping, and positioning.

## Regression Checks

- App launches.
- Splash appears.
- Main window opens.
- Project, Image Conversion, Catalog, Printing, Support, and About tabs render.
- License still shows `Active`.
- No private `licenses/license.json` is committed.
- No batch processing, social media package generation, inventory, supply tracking, accounting, shipping, CRM, cloud database, or web rewrite features are present.
