import urllib.parse

def generate_osint_footprint(analysis_result: dict) -> dict:
    """
    Generates OSINT lookup links, communication endpoints, and search engine dorks.
    """
    if not analysis_result.get("success"):
        return {}

    e164 = analysis_result["formats"]["e164"]
    clean_digits = e164.lstrip("+")
    national = analysis_result["formats"]["national"].replace(" ", "").replace("-", "")
    intl = analysis_result["formats"]["international"]

    # 1. Direct Messaging / Platform Links
    platforms = [
        {
            "name": "WhatsApp Direct Chat",
            "url": f"https://wa.me/{clean_digits}",
            "description": "Buka chat WhatsApp langsung tanpa simpan kontak",
        },
        {
            "name": "Telegram Quick Link",
            "url": f"https://t.me/+{clean_digits}",
            "description": "Cek akun Telegram yang terhubung dengan nomor ini",
        },
    ]

    # 2. Public Reputation & Caller ID Search Queries
    reputation_lookups = [
        {
            "name": "Truecaller Search",
            "url": f"https://www.truecaller.com/search/{clean_digits}",
            "description": "Pencarian identitas publik via Truecaller Web",
        },
        {
            "name": "Sync.me Search",
            "url": f"https://sync.me/search/?number={clean_digits}",
            "description": "Direktori Caller ID global & reverse phone lookup",
        },
    ]

    if analysis_result.get("region_code") == "ID":
        reputation_lookups.append({
            "name": "Kredibel.co.id (Cek Penipuan Indonesia)",
            "url": f"https://www.kredibel.co.id/search/phone/{national}",
            "description": "Cek rekam jejak laporan penipuan di komunitas Indonesia",
        })

    # 3. Google Dorks (Pre-built queries for recon)
    dorks = []
    
    # Dork 1: Social Media Search
    social_query = f'(site:facebook.com | site:instagram.com | site:twitter.com | site:x.com | site:linkedin.com | site:tiktok.com) ("{national}" | "{e164}" | "{intl}")'
    dorks.append({
        "title": "Jejak Media Sosial (FB, IG, X, LinkedIn, TikTok)",
        "dork": social_query,
        "search_url": f"https://www.google.com/search?q={urllib.parse.quote(social_query)}",
    })

    # Dork 2: Leaks & Documents (PDF, Excel, Pastes)
    leaks_query = f'(filetype:pdf | filetype:xlsx | filetype:csv | site:pastebin.com | site:github.com) ("{national}" | "{e164}")'
    dorks.append({
        "title": "Dokumen Publik, Database, & Paste Leak",
        "dork": leaks_query,
        "search_url": f"https://www.google.com/search?q={urllib.parse.quote(leaks_query)}",
    })

    # Dork 3: Marketplace & Forum Jual-Beli (khusus ID jika nomor Indonesia)
    if analysis_result.get("region_code") == "ID":
        market_query = f'(site:olx.co.id | site:kaskus.co.id | site:carousell.app) ("{national}" | "{e164}")'
        dorks.append({
            "title": "Forum Jual-Beli & Iklan Baris",
            "dork": market_query,
            "search_url": f"https://www.google.com/search?q={urllib.parse.quote(market_query)}",
        })

    return {
        "platforms": platforms,
        "reputation_lookups": reputation_lookups,
        "google_dorks": dorks,
    }

