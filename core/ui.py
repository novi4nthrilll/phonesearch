from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

BANNER_ART = r"""
 [bold cyan] ____  _   _  ___  _   _ _____ ____  _____    _    ____   ____ _   _ [/bold cyan]
 [bold cyan]|  _ \| | | |/ _ \| \ | | ____/ ___|| ____|  / \  |  _ \ / ___| | | |[/bold cyan]
 [bold cyan]| |_) | |_| | | | |  \| |  _| \___ \|  _|   / _ \ | |_) | |   | |_| |[/bold cyan]
 [bold cyan]|  __/|  _  | |_| | |\  | |___ ___) | |___ / ___ \|  _ <| |___|  _  |[/bold cyan]
 [bold cyan]|_|   |_| |_|\___/|_| \_|_____|____/|_____/_/   \_\_| \_\\____|_| |_|[/bold cyan]
 [dim]-- Phone Intelligence & OSINT Reconnaissance Tool (v2.0) --[/dim]
"""

def print_banner():
    console.print(BANNER_ART)

def render_risk_bar(score: int, total_blocks: int = 20) -> str:
    """Renders a colored ASCII risk gauge bar."""
    filled = int((score / 100) * total_blocks)
    empty = total_blocks - filled
    
    if score >= 65:
        color = "red"
    elif score >= 35:
        color = "yellow"
    else:
        color = "green"
        
    bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
    return f"{bar} [{color}]{score}%[/{color}]"

def display_analysis(data: dict, osint: dict, risk: dict = None):
    """
    Renders rich formatted panels and tables for phone reconnaissance results.
    """
    if not data.get("success"):
        console.print(Panel(
            f"[bold red]❌ Gagal Menganalisis Nomor:[/bold red] {data.get('error', 'Unknown Error')}\n"
            f"[dim]Input:[/dim] {data.get('raw_input')}",
            title="[bold red]Error[/bold red]",
            border_style="red"
        ))
        return

    # Header Status Badge
    is_valid = data.get("is_valid")
    status_badge = "[bold green]VALID ✅[/bold green]" if is_valid else "[bold red]INVALID / NON-STANDARD ⚠️[/bold red]"
    country_badge = f"[bold yellow]{data.get('region_code')} (+{data.get('country_code')})[/bold yellow]"
    
    # 1. Main Specs Table
    spec_table = Table(box=box.ROUNDED, expand=True, title="📱 [bold cyan]Informasi Telekomunikasi[/bold cyan]")
    spec_table.add_column("Parameter", style="cyan", width=22)
    spec_table.add_column("Nilai", style="white")

    spec_table.add_row("Status Validitas", status_badge)
    spec_table.add_row("Format E.164", f"[bold green]{data['formats']['e164']}[/bold green]")
    spec_table.add_row("Format Internasional", data['formats']['international'])
    spec_table.add_row("Format Nasional", data['formats']['national'])
    spec_table.add_row("Negara / Teritori", f"{country_badge} - {data['location']}")
    spec_table.add_row("Tipe Nomor", data['number_type'])
    spec_table.add_row("Zona Waktu", ", ".join(data['timezones']))

    # 2. Operator & HLR Information
    op_table = Table(box=box.ROUNDED, expand=True, title="📡 [bold magenta]Operator & HLR Intelligence[/bold magenta]")
    op_table.add_column("Attribut", style="magenta", width=22)
    op_table.add_column("Detail", style="white")

    op_table.add_row("Operator / Carrier", f"[bold bright_magenta]{data.get('carrier')}[/bold bright_magenta]")
    
    hlr = data.get("indonesia_hlr")
    if hlr:
        op_table.add_row("Brand Produk", hlr.get("brand", "-"))
        op_table.add_row("Tipe Layanan", hlr.get("type", "-"))
        op_table.add_row("Prefix Terdeteksi", f"[bold yellow]{hlr.get('prefix', '-')}[/bold yellow]")
        op_table.add_row("Estimasi Wilayah (HLR)", f"[bold green]{hlr.get('estimated_region', '-')}[/bold green]")
    else:
        op_table.add_row("Lokasi Registrasi", data.get("location", "Global"))

    console.print(spec_table)
    console.print(op_table)

    # 3. Risk & Fraud Assessment (Feature 2)
    if risk:
        border = "red" if risk["level"] == "HIGH" else ("yellow" if risk["level"] == "MEDIUM" else "green")
        risk_content = []
        
        # Risk Score Meter
        bar_str = render_risk_bar(risk["score"])
        risk_content.append(f"Tingkat Risiko : {risk['badge']}")
        risk_content.append(f"Indeks Skor    : {bar_str}\n")
        
        # Risk factors
        risk_content.append("[bold]Faktor Analisis:[/bold]")
        for f in risk["factors"]:
            risk_content.append(f"  • {f}")

        # Community Database Tagging if found
        db_rec = risk.get("db_record")
        if db_rec:
            tags = " ".join([f"[black on yellow] #{t} [/black on yellow]" for t in db_rec.get("tags", [])])
            risk_content.append(f"\n[bold]Tag Komunitas:[/bold] {tags}")
            if db_rec.get("comments"):
                risk_content.append("\n[bold]Laporan / Modus dari Korban:[/bold]")
                for c in db_rec["comments"][:3]:
                    risk_content.append(f'  💬 "[dim italic]{c}[/dim italic]"')

        # Actionable recommendation
        risk_content.append(f"\n[bold cyan]Rekomendasi Tindakan:[/bold cyan]\n👉 {risk['recommendation']}")

        console.print(Panel(
            "\n".join(risk_content),
            title="🛡️ [bold]Evaluasi Risiko & Deteksi Penipuan (Spam/Scam Engine)[/bold]",
            border_style=border,
            box=box.ROUNDED,
        ))

    # 4. Direct Platform Links
    if osint and osint.get("platforms"):
        plat_table = Table(box=box.ROUNDED, expand=True, title="⚡ [bold green]Akses Langsung & Profiling[/bold green]")
        plat_table.add_column("Platform", style="green", width=25)
        plat_table.add_column("Tautan / URL", style="blue")
        plat_table.add_column("Deskripsi", style="dim")

        for item in osint["platforms"]:
            plat_table.add_row(item["name"], item["url"], item["description"])
        
        console.print(plat_table)

    # 5. Caller ID & Public Reputation Lookups
    if osint and osint.get("reputation_lookups"):
        rep_table = Table(box=box.ROUNDED, expand=True, title="🛡️ [bold yellow]Caller ID & Cek Reputasi Publik[/bold yellow]")
        rep_table.add_column("Layanan", style="yellow", width=25)
        rep_table.add_column("Link Pencarian", style="blue")
        rep_table.add_column("Keterangan", style="dim")

        for rep in osint["reputation_lookups"]:
            rep_table.add_row(rep["name"], rep["url"], rep["description"])

        console.print(rep_table)

    # 6. OSINT Google Dorks
    if osint and osint.get("google_dorks"):
        dork_table = Table(box=box.ROUNDED, expand=True, title="🔎 [bold red]Google Dorks (Investigasi OSINT)[/bold red]")
        dork_table.add_column("Fokus Investigasi", style="red", width=25)
        dork_table.add_column("Direct Search Link", style="blue")
        
        for dork in osint["google_dorks"]:
            dork_table.add_row(dork["title"], dork["search_url"])
            
        console.print(dork_table)

    # 7. Live Web Reconnaissance (Hasil Pencarian Langsung dari Internet)
    if osint and "live_web" in osint:
        live = osint["live_web"]
        if live.get("connected") and live.get("categories"):
            console.print("\n🌐 [bold green]Hasil Pencarian Jejak Langsung di Internet (Live Search Recon):[/bold green]")
            for cat_name, items in live["categories"].items():
                cat_table = Table(box=box.SIMPLE_HEAD, expand=True, title=f"[bold cyan]📁 {cat_name}[/bold cyan]")
                cat_table.add_column("Judul / Snippet", style="white", ratio=3)
                cat_table.add_column("Tautan Sumber", style="blue", ratio=2)

                for itm in items:
                    content_text = f"[bold]{itm['title']}[/bold]\n[dim]{itm['snippet']}[/dim]"
                    cat_table.add_row(content_text, itm['url'])
                console.print(cat_table)
        elif not live.get("connected"):
            console.print(Panel(
                "[yellow]Mode Offline / Tidak terhubung ke live web search.[/yellow]\n"
                "[dim]Gunakan daftar Google Dorks di atas untuk membuka hasil pencarian lengkap secara langsung di browser lo.[/dim]",
                title="[bold yellow]ℹ️ Info Live Search[/bold yellow]",
                border_style="yellow"
            ))

def display_scam_list(records: list):
    """Displays top reported scam numbers from the database."""
    table = Table(box=box.ROUNDED, expand=True, title="🚨 [bold red]Daftar Nomor Penipuan & Spam Terbanyak Dilaporkan[/bold red]")
    table.add_column("No", style="dim", width=4)
    table.add_column("Nomor Telepon", style="bold yellow", width=18)
    table.add_column("Kategori Modus", style="cyan", width=25)
    table.add_column("Laporan", style="red", width=10)
    table.add_column("Tag / Label Komunitas", style="white")
    table.add_column("Terakhir Dilaporkan", style="dim", width=20)

    for idx, rec in enumerate(records, 1):
        tags_str = ", ".join(rec.get("tags", []))
        table.add_row(
            str(idx),
            f"{rec.get('national', '-')} ({rec.get('number', '-')})",
            rec.get("category", "-"),
            f"{rec.get('reports_count', 1)}x",
            tags_str,
            rec.get("last_reported", "-")
        )

    console.print(table)
