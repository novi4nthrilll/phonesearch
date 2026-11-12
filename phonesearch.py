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
from core.ui import print_banner, display_analysis

console = Console()

def process_number(target: str, default_country: str = "ID") -> dict:
    data = analyze_phone_number(target, default_region=default_country)
    osint = generate_osint_footprint(data) if data.get("success") else {}
    return {"data": data, "osint": osint}

def run_interactive_mode(default_country: str):
    print_banner()
    console.print("[bold yellow]Mode Interaktif Aktif.[/bold yellow] Ketik [bold cyan]'exit'[/bold cyan] atau [bold cyan]'q'[/bold cyan] untuk keluar.\n")
    
    while True:
        try:
            target = Prompt.ask("[bold green]Masukkan nomor telepon[/bold green] (contoh: 08123456789 / +62812... / +1...)")
            target = target.strip()
            
            if not target:
                continue
            if target.lower() in ("exit", "q", "quit"):
                console.print("\n[dim]Terima kasih telah menggunakan PhoneSearch! Sampai jumpa 👋[/dim]")
                break

            result = process_number(target, default_country)
            display_analysis(result["data"], result["osint"])
            console.print("\n" + "─" * 60 + "\n")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Keluar dari PhoneSearch.[/dim]")
            break

def run_batch_file(file_path: str, default_country: str, output_path: str = None):
    p = Path(file_path)
    if not p.is_file():
        console.print(f"[bold red]File tidak ditemukan:[/bold red] {file_path}")
        sys.exit(1)

    with open(p, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    console.print(f"[bold cyan]Memproses {len(lines)} nomor dari file:[/bold cyan] {file_path}\n")
    
    all_results = []
    for num in lines:
        result = process_number(num, default_country)
        display_analysis(result["data"], result["osint"])
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

    args = parser.parse_args()

    if args.file:
        print_banner()
        run_batch_file(args.file, args.country, args.output)
    elif args.number:
        print_banner()
        result = process_number(args.number, args.country)
        display_analysis(result["data"], result["osint"])
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            console.print(f"\n[bold green]✔ Hasil disimpan ke:[/bold green] {args.output}")
    else:
        run_interactive_mode(args.country)

if __name__ == "__main__":
    main()

