import json
import re
from datetime import datetime

from app_paths import JOBS_DIR


class ProjectManager:
    def __init__(self):
        JOBS_DIR.mkdir(parents=True, exist_ok=True)

    def slug(self, value):
        value = value.strip().lower() or "untitled-project"
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-") or "untitled-project"

    def project_folder(self, project):
        catalog = project.get("catalog_number") or datetime.now().strftime("draft-%Y%m%d-%H%M%S")
        title = self.slug(project.get("artwork_title", "untitled-project"))
        return JOBS_DIR / f"{catalog}-{title}"

    def save(self, project):
        folder = self.project_folder(project)
        folder.mkdir(parents=True, exist_ok=True)
        project["project_folder"] = str(folder)
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        path = folder / "project.json"
        path.write_text(json.dumps(project, indent=2), encoding="utf-8")
        return path

    def manufacturing_ready_errors(self, project):
        errors = []
        if project.get("approval_status") != "Approved":
            errors.append("Artist approval must be Approved.")
        if not project.get("source_image"):
            errors.append("Source image must be imported.")
        if not project.get("copyright_owner"):
            errors.append("Copyright owner must be assigned.")
        if not project.get("export_files"):
            errors.append("At least one export must be generated.")
        return errors
