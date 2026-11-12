from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

BANNER_ART = r"""
 [bold cyan] ____  _   _  ___  _   _ _____ ____  _____    _    ____   ____ _   _ [/bold cyan]
 [bold cyan]|  _ \| | | |/ _ \| \ | | ____/ ___|| ____|  / \  |  _ \ / ___| | | |[/bold cyan]
 [bold cyan]| |_) | |_| | | | |  \| |  _| \___ \|  _|   / _ \ | |_) | |   | |_| |[/bold cyan]
 [bold cyan]|  __/|  _  | |_| | |\  | |___ ___) | |___ / ___ \|  _ <| |___|  _  |[/bold cyan]
 [bold cyan]|_|   |_| |_|\___/|_| \_|_____|____/|_____/_/   \_\_| \_\\____|_| |_|[/bold cyan]
 [dim]-- Phone Intelligence & OSINT Reconnaissance Tool (v1.0) --[/dim]
"""

def print_banner():
    console.print(BANNER_ART)

def display_analysis(data: dict, osint: dict):
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

    # 3. Direct Platform Links
    if osint and osint.get("platforms"):
        plat_table = Table(box=box.ROUNDED, expand=True, title="⚡ [bold green]Akses Langsung & Profiling[/bold green]")
        plat_table.add_column("Platform", style="green", width=25)
        plat_table.add_column("Tautan / URL", style="blue")
        plat_table.add_column("Deskripsi", style="dim")

        for item in osint["platforms"]:
            plat_table.add_row(item["name"], item["url"], item["description"])
        
        console.print(plat_table)

    # 4. Caller ID & Public Reputation Lookups
    if osint and osint.get("reputation_lookups"):
        rep_table = Table(box=box.ROUNDED, expand=True, title="🛡️ [bold yellow]Caller ID & Cek Reputasi Publik[/bold yellow]")
        rep_table.add_column("Layanan", style="yellow", width=25)
        rep_table.add_column("Link Pencarian", style="blue")
        rep_table.add_column("Keterangan", style="dim")

        for rep in osint["reputation_lookups"]:
            rep_table.add_row(rep["name"], rep["url"], rep["description"])

        console.print(rep_table)

    # 5. OSINT Google Dorks
    if osint and osint.get("google_dorks"):
        dork_table = Table(box=box.ROUNDED, expand=True, title="🔎 [bold red]Google Dorks (Investigasi OSINT)[/bold red]")
        dork_table.add_column("Fokus Investigasi", style="red", width=25)
        dork_table.add_column("Direct Search Link", style="blue")
        
        for dork in osint["google_dorks"]:
            dork_table.add_row(dork["title"], dork["search_url"])
            
        console.print(dork_table)

