import json
from datetime import datetime

from app_paths import CATALOG_DIR


CATALOG_FILE = CATALOG_DIR / "catalog.json"


class CatalogManager:
    def __init__(self):
        CATALOG_DIR.mkdir(parents=True, exist_ok=True)
        self.records = self.load_records()

    def load_records(self):
        if not CATALOG_FILE.exists():
            return []
        try:
            data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        return data if isinstance(data, list) else []

    def save_records(self):
        CATALOG_FILE.write_text(json.dumps(self.records, indent=2), encoding="utf-8")

    def next_catalog_id(self):
        year = datetime.now().year
        prefix = f"WPS-{year}-"
        max_number = 0
        for record in self.records:
            catalog_id = str(record.get("catalog_number", ""))
            if catalog_id.startswith(prefix):
                try:
                    max_number = max(max_number, int(catalog_id.rsplit("-", 1)[1]))
                except ValueError:
                    continue
        return f"{prefix}{max_number + 1:06d}"

    def upsert(self, project):
        catalog_number = project.get("catalog_number") or self.next_catalog_id()
        project["catalog_number"] = catalog_number
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")

        for index, record in enumerate(self.records):
            if record.get("catalog_number") == catalog_number:
                self.records[index] = project
                self.save_records()
                return project

        project["created_at"] = project.get("created_at") or datetime.now().isoformat(timespec="seconds")
        self.records.append(project)
        self.save_records()
        return project

    def search(self, query):
        query = query.lower().strip()
        if not query:
            return list(self.records)
        searchable_fields = ("catalog_number", "artist_name", "artwork_title", "copyright_owner", "approval_status")
        return [
            record
            for record in self.records
            if any(query in str(record.get(field, "")).lower() for field in searchable_fields)
        ]
