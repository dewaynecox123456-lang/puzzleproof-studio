import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from app_paths import BUNDLED_LICENSES_DIR, LICENSES_DIR


@dataclass
class LicenseStatus:
    state: str
    message: str
    data: dict
    expires_date: str

    @property
    def display(self):
        return f"{self.state}: {self.message}"


class LicenseManager:
    def __init__(self):
        self.primary_path = LICENSES_DIR / "license.json"
        self.sample_path = LICENSES_DIR / "sample-license.json"
        self.bundled_sample_path = BUNDLED_LICENSES_DIR / "sample-license.json"

    def load_license(self):
        if self.primary_path.exists():
            path = self.primary_path
        elif self.sample_path.exists():
            path = self.sample_path
        else:
            path = self.bundled_sample_path
        if not path.exists():
            return LicenseStatus(
                "Missing",
                "No license file found. Early Access will continue.",
                {},
                "Unknown",
            )

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return LicenseStatus("Invalid", f"License could not be read: {exc}", {}, "Unknown")

        return self._evaluate(data)

    def _evaluate(self, data):
        status = str(data.get("status", "unknown")).strip() or "unknown"
        expires_text = str(data.get("expires_date", "")).strip()
        if status.lower() not in {"active", "sample", "early-access"}:
            return LicenseStatus("Warning", f"License status is {status}.", data, expires_text or "Unknown")

        try:
            expires = datetime.strptime(expires_text, "%Y-%m-%d").date()
        except ValueError:
            return LicenseStatus("Warning", "License expiration date is missing or invalid.", data, expires_text or "Unknown")

        today = date.today()
        if expires < today:
            return LicenseStatus("Expired", f"License expired on {expires.isoformat()}. Early Access will continue.", data, expires.isoformat())

        if expires <= today + timedelta(days=30):
            return LicenseStatus("Expiring Soon", f"License expires on {expires.isoformat()}.", data, expires.isoformat())

        return LicenseStatus("Active", f"Licensed to {data.get('licensed_to', 'Unknown')}.", data, expires.isoformat())
