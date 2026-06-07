# PuzzleProof Studio Landing Site

Dedicated Netlify-ready static landing site for PuzzleProof Studio early access.

PuzzleProof Studio is software for puzzle makers, artists, Etsy sellers, and small creative businesses. The site presents the product, explains the limited early-access offer, links to Payhip, and collects optional access requests through Netlify Forms.

Current footer branding:

- PuzzleProof Studio
- Built by BayouFinds
- Powered by Wonder Piece Studio
- PuzzleProof Studio is a BayouFinds product.
- © 2026 BayouFinds.com. All Rights Reserved.

## File Structure

```text
site/puzzleproof/
├── assets/
│   ├── icons/
│   │   ├── puzzleproof-icon.svg
│   │   └── puzzleproof-og.png
│   ├── screenshots/
│   │   ├── candidate-homepage.png
│   │   ├── candidate-intake-form.png
│   │   └── candidate-project-output.png
│   └── team/
│       ├── dewayne.png
│       └── sean.png
├── index.html
├── intake.html
├── success.html
├── styles.css
├── script.js
└── README.md
```

## Preview Locally

From this directory:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

From the repo root:

```bash
cd site/puzzleproof
python3 -m http.server 8080
```

## Netlify Deploy Notes

- No build command is required.
- Set the Netlify publish directory to `site/puzzleproof/`.
- The early-access request form uses Netlify Forms with `data-netlify="true"`.
- The project intake form uses Netlify Forms with `data-netlify="true"` and `enctype="multipart/form-data"` for artwork/reference uploads.
- The project intake form posts to `/success.html`.
- After deployment, submit one test request for each form and confirm both appear in the Netlify dashboard.

## Testing Forms

Local preview confirms layout and field behavior, but Netlify Forms submissions and file uploads must be tested after deploying to Netlify.

Local layout test:

1. Run `python3 -m http.server 8080`.
2. Open `http://localhost:8080`.
3. Navigate to `intake.html`.
4. Confirm the Project Intake Form renders on desktop and mobile widths.
5. Confirm required fields, dropdowns, checkbox, and file picker are visible.

Netlify deployment test:

1. Deploy the site to Netlify.
2. Submit the early-access request form.
3. Submit the project intake form with a small test image upload.
4. Confirm both submissions appear in the Netlify Forms dashboard.
5. Confirm the uploaded file is attached to the intake submission.

## Placeholder Replacements

These screenshots were extracted from a temporary screencast and should be replaced after a clean re-record.

Before public launch, replace:

- GitHub placeholder links marked in `index.html`
- Facebook placeholder link marked in `index.html`
- Contact email placeholder marked in `index.html`
- Temporary app screenshots in `assets/screenshots/`
- OpenGraph URL placeholder marked in `index.html` and `intake.html`
- PuzzleProof icon assets if a final production mark replaces the current early-access icon

## Launch Checklist

1. Replace GitHub placeholder.
2. Replace Facebook placeholder.
3. Replace temporary screencast screenshots after a clean re-record.
4. Confirm favicon, navbar icon, footer icon, and OpenGraph image.
5. Test Payhip button: `https://bayoufinds.com/b/x98IV`.
6. Test Netlify form.
7. Test Netlify intake form submission and file upload.
8. Confirm `/success.html` loads after deployed form submission.
9. Confirm mobile layout.
10. Commit changes.
11. Deploy to Netlify.
