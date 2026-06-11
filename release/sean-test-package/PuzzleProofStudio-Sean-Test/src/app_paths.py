from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT_DIR / "VERSION"

JOBS_DIR = ROOT_DIR / "jobs"
CATALOG_DIR = ROOT_DIR / "catalog"
EXPORTS_DIR = ROOT_DIR / "exports"
LOGS_DIR = ROOT_DIR / "data" / "logs"
SETTINGS_DIR = ROOT_DIR / "data" / "settings"
BACKUPS_DIR = ROOT_DIR / "data" / "backups"
LICENSES_DIR = ROOT_DIR / "licenses"
TEMPLATES_DIR = ROOT_DIR / "assets" / "templates"
SAMPLE_IMAGES_DIR = ROOT_DIR / "assets" / "sample-images"
ICONS_DIR = ROOT_DIR / "assets" / "icons"
LINUX_ICON_FILE = ICONS_DIR / "puzzleproof-icon.xbm"


def ensure_app_dirs():
    for path in (
        JOBS_DIR,
        CATALOG_DIR,
        EXPORTS_DIR,
        LOGS_DIR,
        SETTINGS_DIR,
        BACKUPS_DIR,
        LICENSES_DIR,
        TEMPLATES_DIR,
        SAMPLE_IMAGES_DIR,
        ICONS_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


def get_version():
    try:
        value = VERSION_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "0.1.0-EarlyAccess"
    for line in value.splitlines():
        line = line.strip()
        if line:
            return line
    return "0.1.0-EarlyAccess"
