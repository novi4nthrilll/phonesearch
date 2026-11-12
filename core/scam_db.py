import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "scam_database.json"

CATEGORIES = {
    "SCAM_MALWARE": "Penipuan Malware / APK (Kurir, Tilang, Undangan Palsu)",
    "SCAM_PHISHING": "Phishing & CS Bank Palsu (Minta OTP / Rekening)",
    "SCAM_JOB": "Loker Freelance Palsu / Like Video & Deposit",
    "PINJOL_TEROR": "Pinjol Ilegal & Teror Debt Collector",
    "TELEMARKETING": "Spam Telemarketing & Robot Call Agresif",
    "SCAM_UNDIAN": "Penipuan Menang Undian / Hadiah Palsu",
    "OTHER_SUSPICIOUS": "Aktivitas Mencurigakan Lainnya",
}


def _clean_digits(number: str) -> str:
    """Extract only digit characters from a string."""
    return "".join(c for c in number if c.isdigit())


def _normalize_subscriber(number: str) -> str:
    """
    Extracts the subscriber digits (without country code or leading zero).
    '08123456789' → '8123456789'
    '+6281234567890' → '81234567890'
    '6281234567890' → '81234567890'
    """
    digits = _clean_digits(number)
    if not digits:
        return ""
    # Strip Indonesia country code '62' prefix
    if digits.startswith("62") and len(digits) > 10:
        digits = digits[2:]
    # Strip leading zero
    if digits.startswith("0") and len(digits) > 9:
        digits = digits[1:]
    return digits


class ScamDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._cache: dict | None = None
        self._cache_mtime: float = 0.0
        self._ensure_db()

    def _ensure_db(self):
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            default_data = {
                "database_version": "1.0",
                "updated_at": datetime.now().strftime("%Y-%m-%d"),
                "records": [],
            }
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)

    def _load_data(self) -> dict:
        """Load JSON with simple mtime-based cache to avoid redundant disk reads."""
        try:
            current_mtime = self.db_path.stat().st_mtime
            if self._cache is not None and current_mtime == self._cache_mtime:
                return self._cache
            with open(self.db_path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
            self._cache_mtime = current_mtime
            return self._cache
        except Exception:
            return {"database_version": "1.0", "records": []}

    def _save_data(self, data: dict):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        # Invalidate cache so next _load_data re-reads
        self._cache = None

    def lookup(self, number: str) -> tuple[dict | None, dict | None]:
        """
        Looks up a phone number in the scam database.
        Returns (record, data) tuple where data is the full loaded dict,
        so callers who need to modify + save can use the same object.
        """
        subscriber = _normalize_subscriber(number)
        if not subscriber or len(subscriber) < 7:
            return None, None

        data = self._load_data()
        for rec in data.get("records", []):
            rec_sub_e164 = _normalize_subscriber(rec.get("number", ""))
            rec_sub_nat = _normalize_subscriber(rec.get("national", ""))

            if subscriber == rec_sub_e164 or subscriber == rec_sub_nat:
                return rec, data

        return None, data

    def add_report(self, number: str, category: str, tag: str, comment: str = "", risk_level: str = "HIGH") -> dict:
        """
        Submits a new crowdsourced scam report or updates existing one.
        """
        existing, data = self.lookup(number)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if existing:
            existing["reports_count"] = existing.get("reports_count", 1) + 1
            existing["risk_level"] = risk_level
            existing["last_reported"] = now_str
            if category:
                existing["category"] = category
            if tag and tag not in existing.get("tags", []):
                existing.setdefault("tags", []).append(tag)
            if comment and comment not in existing.get("comments", []):
                existing.setdefault("comments", []).append(comment)
            self._save_data(data)
            return existing

        # Build normalized national & E.164 for new record
        subscriber = _normalize_subscriber(number)
        clean_nat = "0" + subscriber
        clean_e164 = "+62" + subscriber

        new_record = {
            "number": clean_e164,
            "national": clean_nat,
            "category": category or "OTHER_SUSPICIOUS",
            "risk_level": risk_level,
            "reports_count": 1,
            "tags": [tag] if tag else ["Dilaporkan Pengguna"],
            "comments": [comment] if comment else [],
            "last_reported": now_str,
        }
        if data is None:
            data = self._load_data()
        data.setdefault("records", []).append(new_record)
        data["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        self._save_data(data)
        return new_record

    def list_all_records(self, sort_by_reports: bool = True) -> list:
        data = self._load_data()
        records = data.get("records", [])
        if sort_by_reports:
            records = sorted(records, key=lambda x: x.get("reports_count", 0), reverse=True)
        return records
