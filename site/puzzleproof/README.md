# PuzzleProof Studio Landing Site

Netlify-ready static product landing page for PuzzleProof Studio.

The homepage is customer-facing and aimed at small puzzle makers, custom gift shops, artists, and production partners. The primary message is: turn one customer image into print-ready puzzle production assets faster.

## Customer Page Sections

- Hero: product name, production software positioning, setup-time reduction
- What It Does: customer image import, Puzzle Print, Box Insert, Box Sticker / Label, DOCX/PNG/JPG export
- Built From Real Workflow: Wonder Piece Studio beta testing with Sean Watkins
- Download / Early Access: latest release link and current build
- FAQ: Windows, DOCX, production printing, and runtime questions
- Contact: BayouFinds / Wonder Piece Studio support

## File Structure

```text
site/puzzleproof/
├── assets/
│   ├── icons/
│   ├── screenshots/
│   └── team/
├── index.html
├── intake.html
├── success.html
├── _redirects
├── styles.css
├── script.js
└── README.md
```

## Preview Locally

From the repo root:

```bash
cd site/puzzleproof
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Netlify Deploy Notes

- No build command is required.
- Set the Netlify publish directory to `site/puzzleproof/`.
- `_redirects` maps older `/thank-you` and `/success` paths to `/success.html`.
- Local preview confirms layout only. Netlify form handling must be tested after deployment.

## Launch Checklist

1. Confirm latest release link opens the current GitHub release.
2. Confirm support email link opens a new email.
3. Confirm homepage layout on desktop and mobile widths.
4. Confirm `/success.html` still loads.
5. Confirm `intake.html` still loads if linked from another campaign.
6. Replace OpenGraph URL placeholder when the final production domain is live.
