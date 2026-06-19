# Changelog

## 0.1.3.2-SeanValidation

- Defaulted artwork placement to `Fit Entire Artwork / Preserve Full Image`.
- Preserved the full source artwork for DOCX, PNG, and JPG exports when artwork aspect ratio does not match the selected production preset.
- Kept `Fill Puzzle Area / Crop to Fill` available for intentional crop-to-fill output.
- Added a warning before crop-to-fill export: `This mode may crop parts of the artwork. Continue?`
- Added artwork placement mode to export summary, status output, and the Export Complete dialog.
- Added `scripts/validate_crop_safe_export.py` to verify crop-safe PNG and DOCX fit exports.

## 0.1.2-Candidate

- Status: Feature Complete.
- Pending: Windows Customer Validation.
- Risk: Low.
- Customer impact: High.
- Polished the preset export workflow around Puzzle Print, Box Insert, and Box Sticker / Label outputs.
- Defaulted Image Conversion output format to DOCX for transition comfort.
- Added export success details with preset, format, saved path, and suggested printer guidance.

## 0.1.0-EarlyAccess

- Added first working Python/Tkinter scaffold.
- Added offline license checking with sample license fallback.
- Added project metadata, approval status, catalog number, and origin fields.
- Added JSON catalog storage using `WPS-YYYY-000001` IDs.
- Added Pillow-based image export presets for production output sizes.
- Added production-focused preset outputs for Puzzle Print, Box Insert, and Box Sticker / Label.
- Added DOCX export compatibility as transition comfort for users moving away from Word-based manual setup.
- Added optional copyright overlay placement.
- Added print-ready HTML document generation.
- Added Support and About screens.
- Added Fedora run script and Windows packaging placeholder.
