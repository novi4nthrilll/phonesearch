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

    raw_input = analysis_data.get("raw_input", "")
    e164 = analysis_data.get("formats", {}).get("e164", "")
    national = analysis_data.get("formats", {}).get("national", "")

    score = 0
    factors = []
    
    # 1. Check Local Scam Database
    db_record = scam_db.lookup(e164) or scam_db.lookup(national) or scam_db.lookup(raw_input)
    
    if db_record:
        reports = db_record.get("reports_count", 1)
        category = db_record.get("category", "")
        cat_desc = CATEGORIES.get(category, category)

        if category in ("SCAM_MALWARE", "SCAM_PHISHING", "SCAM_JOB", "PINJOL_TEROR", "SCAM_UNDIAN"):
            added = min(70 + (reports * 2), 95)
            score += added
            factors.append(f"🚨 Terdaftar di database penipuan komunitas: {cat_desc} ({reports} laporan)")
        elif category == "TELEMARKETING":
            added = min(40 + (reports * 2), 65)
            score += added
            factors.append(f"📞 Terdaftar sebagai spam telemarketing agresif ({reports} laporan)")
        else:
            score += 50
            factors.append(f"⚠️ Dilaporkan mencurigakan oleh komunitas ({reports} laporan)")
    
    # 2. Check Live Web Search Results
    live_web = osint_data.get("live_web", {}) if osint_data else {}
    categories = live_web.get("categories", {})
    
    if "Indikasi Penipuan / Laporan Spam Online" in categories:
        items = categories["Indikasi Penipuan / Laporan Spam Online"]
        if items:
            score += 35
            factors.append(f"🌐 Ditemukan {len(items)} cuplikan laporan penipuan/waspada pada pencarian internet")

    # Check suspicious keywords in any snippet
    suspicious_keywords = ["penipu", "penipuan", "scam", "apk resi", "teror", "minta otp", "pinjol"]
    snippet_matches = 0
    for cat_items in categories.values():
        for itm in cat_items:
            text = (itm.get("title", "") + " " + itm.get("snippet", "")).lower()
            if any(kw in text for kw in suspicious_keywords):
                snippet_matches += 1

    if snippet_matches > 0 and not db_record:
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

    # Cap score at 100
    score = min(max(score, 5), 100)

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

