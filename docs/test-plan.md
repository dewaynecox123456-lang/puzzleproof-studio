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

## Regression Checks

- App launches.
- Splash appears.
- Main window opens.
- Project, Image Conversion, Catalog, Printing, Support, and About tabs render.
- License still shows `Active`.
- No private `licenses/license.json` is committed.
- No inventory, supply tracking, accounting, shipping, CRM, cloud database, or web rewrite features are present.
