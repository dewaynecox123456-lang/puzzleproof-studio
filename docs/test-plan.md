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
4. Select `Puzzle Print`, choose `DOCX`, and export.
5. Verify the export success details show `Puzzle Print`, `DOCX`, the full saved path, and `Sublimation printer / sublimation paper`.
6. Select `Box Insert`, choose `DOCX`, and export.
7. Verify the export success details show `Box Insert`, `DOCX`, the full saved path, and `Standard printer / regular paper`.
8. Select `Box Sticker / Label`, choose `DOCX`, and export.
9. Verify the export success details show `Box Sticker / Label`, `DOCX`, the full saved path, and `Sticker paper or label printer`.
10. Verify all three DOCX files are created in `exports/`.
11. Verify the DOCX files open in Microsoft Word on Windows.
12. Choose `PNG` or `JPG` for one preset and confirm image output is created for direct image workflows.
13. Click Open Output Folder and confirm it opens the generated file's folder or the `exports/` folder.
14. Confirm the output folder is clear and contains the generated preset files.

Note: The Word check validates DOCX transition compatibility only. The core workflow requirement is preset-based output generation that removes repeated resizing, cropping, and positioning.

## Regression Checks

- App launches.
- Splash appears.
- Main window opens.
- Project, Image Conversion, Catalog, Printing, Support, and About tabs render.
- License still shows `Active`.
- No private `licenses/license.json` is committed.
- No batch processing, social media package generation, inventory, supply tracking, accounting, shipping, CRM, cloud database, or web rewrite features are present.
