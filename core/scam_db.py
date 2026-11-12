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

class ScamDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            default_data = {
                "database_version": "1.0",
                "updated_at": datetime.now().strftime("%Y-%m-%d"),
                "records": []
            }
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=2, ensure_ascii=False)

    def _load_data(self) -> dict:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"database_version": "1.0", "records": []}

    def _save_data(self, data: dict):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _clean_digits(self, number: str) -> str:
        return "".join(c for c in number if c.isdigit())

    def lookup(self, number: str) -> dict | None:
        """
        Looks up a phone number in the scam database.
        Matches by raw string, E.164 (+62...), national (08...), or raw digits.
        """
        digits = self._clean_digits(number)
        if not digits:
            return None

        data = self._load_data()
        for rec in data.get("records", []):
            rec_digits_e164 = self._clean_digits(rec.get("number", ""))
            rec_digits_nat = self._clean_digits(rec.get("national", ""))

            # Match exact digits or suffix matching (e.g. 62812xxx matches 0812xxx)
            if digits in (rec_digits_e164, rec_digits_nat):
                return rec
            if len(digits) >= 9:
                # Compare trailing 9 digits (handles 0812 vs 62812 vs +62812)
                if rec_digits_e164.endswith(digits[-9:]) or rec_digits_nat.endswith(digits[-9:]):
                    return rec

        return None

    def add_report(self, number: str, category: str, tag: str, comment: str = "", risk_level: str = "HIGH") -> dict:
        """
        Submits a new crowdsourced scam report or updates existing one.
        """
        clean_num = number.strip()
        clean_nat = "0" + self._clean_digits(clean_num)[-10:] if len(self._clean_digits(clean_num)) >= 10 else clean_num
        clean_e164 = "+62" + clean_nat[1:] if clean_nat.startswith("0") else ("+" + self._clean_digits(clean_num))

        data = self._load_data()
        existing = self.lookup(clean_num)
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
        else:
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

