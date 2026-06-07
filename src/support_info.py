import platform

from app_paths import LOGS_DIR, ROOT_DIR, get_version


SUPPORT_EMAIL = "support@bayoufinds.com"
WEBSITE = "https://bayoufinds.com"


def build_support_info(license_status):
    return {
        "Software": "PuzzleProof Studio",
        "Version": get_version(),
        "License Status": license_status.state,
        "License Expiration": license_status.expires_date,
        "Support Email": SUPPORT_EMAIL,
        "Website": WEBSITE,
        "Operating System": f"{platform.system()} {platform.release()}",
        "App Folder": str(ROOT_DIR),
        "Logs Folder": str(LOGS_DIR),
    }


def format_support_info(info):
    return "\n".join(f"{key}: {value}" for key, value in info.items())
