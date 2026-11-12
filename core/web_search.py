import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
}


def is_online(host: str = "8.8.8.8", port: int = 53, timeout: float = 1.2) -> bool:
    """Fast check to verify if system has active outbound internet access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)  # instance-level timeout, not global
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def query_duckduckgo_html(query_str: str, max_results: int = 4, timeout: int = 4) -> list:
    """
    Performs a live query on DuckDuckGo HTML engine and extracts organic snippets.
    """
    url = "https://html.duckduckgo.com/html/"
    payload = {"q": query_str}

    try:
        response = requests.post(url, data=payload, headers=HEADERS, timeout=timeout)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for el in soup.select(".result"):
            title_el = el.select_one(".result__title a")
            if not title_el:
                continue

            snippet_el = el.select_one(".result__snippet")
            url_el = el.select_one(".result__url")

            title = title_el.get_text(strip=True)
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""

            # Resolve actual URL from DuckDuckGo redirect wrapper
            href = title_el.get("href", "")
            actual_url = href
            if "uddg=" in href:
                parsed_qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if "uddg" in parsed_qs:
                    actual_url = parsed_qs["uddg"][0]
            elif url_el:
                raw_u = url_el.get_text(strip=True)
                actual_url = ("https://" + raw_u) if not raw_u.startswith("http") else raw_u

            results.append({
                "title": title,
                "snippet": snippet,
                "url": actual_url,
            })

            if len(results) >= max_results:
                break

        return results
    except Exception:
        return []


def search_number_live(formats: dict, check_scam: bool = True) -> dict:
    """
    Searches the live web for traces of the given phone number.
    """
    if not is_online():
        return {
            "connected": False,
            "error": "Tidak ada koneksi internet (Offline mode)",
            "categories": {},
        }

    e164 = formats.get("e164", "")
    national = formats.get("national", "").replace(" ", "").replace("-", "")

    if not national and not e164:
        return {"connected": False, "error": "Invalid format", "categories": {}}

    # Build search term (prefer both formats if available)
    if e164 and national:
        search_term = f'"{national}" OR "{e164}"'
    else:
        search_term = f'"{national or e164}"'

    categories = {}
    connected = False

    try:
        # Dork 1: Direct Web Mentions (Exact Match)
        res_exact = query_duckduckgo_html(search_term, max_results=4)
        if res_exact:
            categories["Pencarian Umum & Web Mention"] = res_exact

        # Dork 2: Scam & Fraud Warnings Online
        if check_scam:
            query_scam = f'"{national}" (penipuan OR penipu OR scam OR spam OR waspada)'
            res_scam = query_duckduckgo_html(query_scam, max_results=3)
            if res_scam:
                categories["Indikasi Penipuan / Laporan Spam Online"] = res_scam

        # Dork 3: Social Media & Marketplace Presence
        query_social = f'"{national}" (facebook.com OR instagram.com OR twitter.com OR olx.co.id)'
        res_social = query_duckduckgo_html(query_social, max_results=3)
        if res_social:
            categories["Sosial Media & Forum Publik"] = res_social

        connected = bool(categories)
    except Exception:
        pass

    return {
        "connected": connected,
        "error": None if connected else "Tidak ada jejak publik ditemukan atau dibatasi oleh provider.",
        "categories": categories,
    }
