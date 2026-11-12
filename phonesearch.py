#!/usr/bin/env python3
"""
PhoneSearch - Phone Intelligence & OSINT Reconnaissance CLI
Author: novi4nth
"""

import sys
import argparse
import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

from core.analyzer import analyze_phone_number
from core.osint_footprint import generate_osint_footprint
from core.web_search import search_number_live
from core.scam_db import ScamDatabase, CATEGORIES
from core.risk_engine import calculate_risk
from core.ui import print_banner, display_analysis, display_scam_list

console = Console()
scam_db = ScamDatabase()

def process_number(target: str, default_country: str = "ID", search_web: bool = True) -> dict:
    data = analyze_phone_number(target, default_region=default_country)
    osint = generate_osint_footprint(data) if data.get("success") else {}
    
    if data.get("success") and search_web:
        with console.status("[bold cyan]Mencari jejak nomor di internet (Live Web Recon)...[/bold cyan]", spinner="dots"):
            osint["live_web"] = search_number_live(data["formats"])

    risk = calculate_risk(data, osint, scam_db)
    return {"data": data, "osint": osint, "risk": risk}

def report_number_flow(target_number: str = None):
    """Interactive flow to report a spam/scam phone number."""
    print_banner()
    console.print("🚨 [bold red]Formulir Laporan Nomor Penipuan / Spam Komunitas[/bold red]\n")
    
    if not target_number:
        target_number = Prompt.ask("[bold yellow]Masukkan nomor telepon yang ingin dilaporkan[/bold yellow]")
    
    target_number = target_number.strip()
    if not target_number:
        console.print("[red]Nomor telepon tidak boleh kosong.[/red]")
        return

    # Category choices
    cat_keys = list(CATEGORIES.keys())
    console.print("\n[bold cyan]Pilih Kategori Penipuan / Spam:[/bold cyan]")
    for idx, key in enumerate(cat_keys, 1):
        console.print(f" [{idx}] {CATEGORIES[key]}")

    choice = Prompt.ask("\n[bold green]Pilihan kategori (1-7)[/bold green]", choices=[str(i) for i in range(1, len(cat_keys) + 1)], default="1")
    selected_category = cat_keys[int(choice) - 1]

    tag = Prompt.ask("[bold green]Tag / Label Singkat[/bold green] (contoh: Kurir J&T APK, CS BCA Palsu, Pinjol AdaPundi)")
    comment = Prompt.ask("[bold green]Kronologi / Modus Singkat[/bold green] (opsional, tekan enter untuk lewati)")

    record = scam_db.add_report(
        number=target_number,
        category=selected_category,
        tag=tag.strip(),
        comment=comment.strip(),
        risk_level="HIGH" if selected_category != "TELEMARKETING" else "MEDIUM"
    )

    console.print(f"\n[bold green]✔ Laporan berhasil disimpan ke database komunitas![/bold green]")
    console.print(f"Nomor: [bold yellow]{record.get('national')}[/bold yellow] | Total Laporan: [bold red]{record.get('reports_count')}x[/bold red]\n")

def run_interactive_mode(default_country: str, search_web: bool = True):
    print_banner()
    console.print("[bold yellow]Mode Interaktif Aktif.[/bold yellow]")
    console.print("• Ketik nomor telepon untuk investigasi.")
    console.print("• Ketik [bold red]'report'[/bold red] untuk melaporkan nomor penipu.")
    console.print("• Ketik [bold cyan]'top'[/bold cyan] untuk melihat daftar top scammer.")
    console.print("• Ketik [bold dim]'exit'[/bold dim] atau [bold dim]'q'[/bold dim] untuk keluar.\n")
    
    while True:
        try:
            target = Prompt.ask("[bold green]Masukkan nomor telepon / perintah[/bold green]")
            target = target.strip()
            
            if not target:
                continue
            if target.lower() in ("exit", "q", "quit"):
                console.print("\n[dim]Terima kasih telah menggunakan PhoneSearch! Tetap waspada terhadap kejahatan siber 👋[/dim]")
                break
            if target.lower() in ("report", "lapor"):
                report_number_flow()
                continue
            if target.lower() in ("top", "list", "scams"):
                display_scam_list(scam_db.list_all_records())
                console.print("\n" + "─" * 60 + "\n")
                continue

            result = process_number(target, default_country, search_web=search_web)
            display_analysis(result["data"], result["osint"], result["risk"])
            console.print("\n" + "─" * 60 + "\n")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Keluar dari PhoneSearch.[/dim]")
            break

def run_batch_file(file_path: str, default_country: str, output_path: str = None, search_web: bool = False):
    p = Path(file_path)
    if not p.is_file():
        console.print(f"[bold red]File tidak ditemukan:[/bold red] {file_path}")
        sys.exit(1)

    with open(p, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    console.print(f"[bold cyan]Memproses {len(lines)} nomor dari file:[/bold cyan] {file_path}\n")
    
    all_results = []
    for num in lines:
        result = process_number(num, default_country, search_web=search_web)
        display_analysis(result["data"], result["osint"], result["risk"])
        console.print("\n" + "─" * 60 + "\n")
        all_results.append(result)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        console.print(f"[bold green]✔ Hasil export batch disimpan ke:[/bold green] {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="PhoneSearch - Phone Intelligence & OSINT Reconnaissance CLI"
    )
    parser.add_argument("number", nargs="?", help="Nomor telepon yang ingin dianalisis (misal: 08123456789 atau +62812...)")
    parser.add_argument("-c", "--country", default="ID", help="Default ISO Country code untuk nomor lokal (default: ID)")
    parser.add_argument("-f", "--file", help="Jalankan batch scan dari file teks (.txt / list nomor per baris)")
    parser.add_argument("-o", "--output", help="Simpan hasil analisis ke file JSON")
    parser.add_argument("--no-web", action="store_true", help="Nonaktifkan live web search (hanya format & HLR lookup cepat)")
    parser.add_argument("--report", nargs="?", const="prompt", help="Laporkan nomor penipuan / spam baru ke database komunitas")
    parser.add_argument("--list-scams", action="store_true", help="Tampilkan daftar nomor penipuan terbanyak dilaporkan")

    args = parser.parse_args()
    search_web = not args.no_web

    if args.list_scams:
        print_banner()
        display_scam_list(scam_db.list_all_records())
        return

    if args.report:
        report_target = None if args.report == "prompt" else args.report
        report_number_flow(report_target)
        return

    if args.file:
        print_banner()
        run_batch_file(args.file, args.country, args.output, search_web=search_web)
    elif args.number:
        print_banner()
        result = process_number(args.number, args.country, search_web=search_web)
        display_analysis(result["data"], result["osint"], result["risk"])
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            console.print(f"\n[bold green]✔ Hasil disimpan ke:[/bold green] {args.output}")
    else:
        run_interactive_mode(args.country, search_web=search_web)

if __name__ == "__main__":
    main()
