"""
Risk Scoring Engine for Phone Numbers
Calculates Risk Score (0 - 100%), Threat Level, and Actionable Recommendations.
"""

from core.scam_db import ScamDatabase, CATEGORIES


def calculate_risk(analysis_data: dict, osint_data: dict, scam_db: ScamDatabase) -> dict:
    """
    Evaluates risk factors from community reports, web mentions, and technical indicators.
    """
    if not analysis_data.get("success"):
        return {
            "score": 0,
            "level": "UNKNOWN",
            "badge": "[dim]UNKNOWN[/dim]",
            "factors": ["Gagal menganalisis nomor telepon"],
            "recommendation": "Periksa kembali format nomor.",
            "db_record": None,
        }

    e164 = analysis_data.get("formats", {}).get("e164", "")

    score = 0
    factors = []

    # 1. Check Local Scam Database (single lookup — fuzzy matching is internal)
    db_record, _ = scam_db.lookup(e164)

    if db_record:
        reports = db_record.get("reports_count", 1)
        category = db_record.get("category", "")
        cat_desc = CATEGORIES.get(category, category)

        if category in ("SCAM_MALWARE", "SCAM_PHISHING", "SCAM_JOB", "PINJOL_TEROR", "SCAM_UNDIAN"):
            score += min(70 + (reports * 2), 95)
            factors.append(f"🚨 Terdaftar di database penipuan komunitas: {cat_desc} ({reports} laporan)")
        elif category == "TELEMARKETING":
            score += min(40 + (reports * 2), 65)
            factors.append(f"📞 Terdaftar sebagai spam telemarketing agresif ({reports} laporan)")
        else:
            score += 50
            factors.append(f"⚠️ Dilaporkan mencurigakan oleh komunitas ({reports} laporan)")

    # 2. Check Live Web Search Results
    live_web = osint_data.get("live_web", {}) if osint_data else {}
    categories = live_web.get("categories", {})

    scam_web_items = categories.get("Indikasi Penipuan / Laporan Spam Online", [])
    if scam_web_items:
        score += 35
        factors.append(f"🌐 Ditemukan {len(scam_web_items)} cuplikan laporan penipuan/waspada pada pencarian internet")

    # Check suspicious keywords in any snippet (only add if not already in DB)
    if not db_record:
        suspicious_keywords = ("penipu", "penipuan", "scam", "apk resi", "teror", "minta otp", "pinjol")
        snippet_matches = 0
        for cat_items in categories.values():
            for itm in cat_items:
                text = (itm.get("title", "") + " " + itm.get("snippet", "")).lower()
                if any(kw in text for kw in suspicious_keywords):
                    snippet_matches += 1

        if snippet_matches > 0:
            score += min(snippet_matches * 10, 30)
            factors.append(f"🔍 Terdeteksi kata kunci mencurigakan ('penipu/scam/otp/apk') pada {snippet_matches} hasil web")

    # 3. Technical & Telecom Indicators
    num_type = analysis_data.get("number_type", "")
    if "VoIP" in num_type:
        score += 15
        factors.append("📡 Tipe nomor VoIP (Voice over IP) - Sering dipakai anonim/spammer")

    if not analysis_data.get("is_valid"):
        score += 20
        factors.append("⚠️ Format nomor tidak valid menurut standar telekomunikasi")

    # Cap score at 0-100 (no artificial minimum)
    score = min(score, 100)

    # Determine Threat Level & Recommendations
    if score >= 65:
        level = "HIGH"
        badge = "[bold red]BAHAYA / TINGGI (HIGH RISK) 🚨[/bold red]"
        recommendation = "JANGAN ANGKAT / BLOKIR! Waspadai pengiriman file .apk, permintaan kode OTP, atau transfer uang."
    elif score >= 35:
        level = "MEDIUM"
        badge = "[bold yellow]WASPADA / SEDANG (MEDIUM RISK) ⚠️[/bold yellow]"
        recommendation = "Hati-hati terhadap tawaran produk mencurigakan atau desakan mengatasnamakan instansi."
    else:
        level = "LOW"
        badge = "[bold green]AMAN / RENDAH (LOW RISK) 🛡️[/bold green]"
        recommendation = "Belum ditemukan riwayat laporan penipuan atau indikasi negatif pada nomor ini."
        if not factors:
            factors.append("Tidak ada rekam jejak mencurigakan yang terdeteksi.")

    return {
        "score": score,
        "level": level,
        "badge": badge,
        "factors": factors,
        "recommendation": recommendation,
        "db_record": db_record,
    }
