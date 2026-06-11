# PuzzleProof Studio License Notes

PuzzleProof Studio uses the standard BayouFinds offline licensing model.

- License data is stored locally in `licenses/license.json`.
- If that file is missing during Early Access, the app falls back to `licenses/sample-license.json`.
- There is no online activation.
- There is no cloud license check.
- License validation is local and non-fatal during Early Access.
- Licenses support yearly expiration dates.
- Seller-side records should be kept in a separate BayouFinds license ledger.

Expected license fields:

```json
{
  "product": "PuzzleProof Studio",
  "licensed_to": "Customer Name",
  "license_key": "OFFLINE-KEY",
  "issued_date": "2026-01-01",
  "expires_date": "2026-12-31",
  "status": "active",
  "seats": 1,
  "notes": "Seller ledger reference"
}
```

The app displays license status on the splash screen, support screen, and about/license areas. It warns for missing, expired, invalid, or soon-to-expire licenses without crashing the Early Access build.
