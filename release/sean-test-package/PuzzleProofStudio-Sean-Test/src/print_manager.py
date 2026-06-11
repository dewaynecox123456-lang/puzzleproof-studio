from datetime import datetime
import html

from app_paths import EXPORTS_DIR, TEMPLATES_DIR


class PrintManager:
    def __init__(self):
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def create_document(self, document_type, project):
        safe_type = document_type.lower().replace(" ", "-")
        catalog = project.get("catalog_number") or "draft"
        path = EXPORTS_DIR / f"{catalog}-{safe_type}.html"
        path.write_text(self._render_html(document_type, project), encoding="utf-8")
        return path

    def create_production_package(self, project):
        paths = []
        for document_type in ("Artist Release", "Copyright Form", "Production Sheet", "Sticker", "Insert", "Puzzle Cover"):
            paths.append(self.create_document(document_type, project))
        return paths

    def _render_html(self, document_type, project):
        rows = "\n".join(
            f"<tr><th>{html.escape(label)}</th><td>{html.escape(str(value or ''))}</td></tr>"
            for label, value in (
                ("Catalog Number", project.get("catalog_number")),
                ("Artist", project.get("artist_name")),
                ("Artwork", project.get("artwork_title")),
                ("Copyright Owner", project.get("copyright_owner")),
                ("Approval Status", project.get("approval_status")),
                ("Manufacturing Ready", project.get("manufacturing_ready")),
                ("Project Origin", project.get("project_origin")),
                ("Generated", datetime.now().isoformat(timespec="seconds")),
            )
        )
        notes = html.escape(project.get("project_notes", ""))
        return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{html.escape(document_type)} - PuzzleProof Studio</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #202020; }}
    h1 {{ margin-bottom: 0; }}
    .subtitle {{ color: #555; margin-top: 6px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 24px; }}
    th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ width: 220px; background: #f1f1f1; }}
    .signature {{ margin-top: 56px; border-top: 1px solid #333; width: 360px; padding-top: 8px; }}
  </style>
</head>
<body>
  <h1>{html.escape(document_type)}</h1>
  <div class="subtitle">PuzzleProof Studio - Artist-to-Puzzle Production Utility</div>
  <table>{rows}</table>
  <h2>Notes</h2>
  <p>{notes}</p>
  <div class="signature">Artist / Authorized Representative Signature</div>
</body>
</html>
"""
