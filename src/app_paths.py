import sys
from pathlib import Path


def _resource_root():
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent.parent


def _app_root():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return _resource_root()


RESOURCE_ROOT = _resource_root()
ROOT_DIR = _app_root()
VERSION_FILE = RESOURCE_ROOT / "VERSION"

JOBS_DIR = ROOT_DIR / "jobs"
CATALOG_DIR = ROOT_DIR / "catalog"
EXPORTS_DIR = ROOT_DIR / "exports"
LOGS_DIR = ROOT_DIR / "logs"
SETTINGS_DIR = ROOT_DIR / "data" / "settings"
BACKUPS_DIR = ROOT_DIR / "data" / "backups"
LICENSES_DIR = ROOT_DIR / "licenses"
BUNDLED_LICENSES_DIR = RESOURCE_ROOT / "licenses"
TEMPLATES_DIR = RESOURCE_ROOT / "assets" / "templates"
SAMPLE_IMAGES_DIR = RESOURCE_ROOT / "assets" / "sample-images"
ICONS_DIR = RESOURCE_ROOT / "assets" / "icons"
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
