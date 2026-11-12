# 📱 PhoneSearch - Phone Intelligence & OSINT Reconnaissance CLI

Tools intelijen nomor telepon berbasis CLI interaktif untuk validasi standar telekomunikasi internasional, deteksi operator & HLR (Home Location Register) Indonesia, serta profiling OSINT digital.

---

## ✨ Fitur Utama (Tahap 1)

1. **Global Telecom & E.164 Standard Analysis:**
   - Deteksi format: `E.164`, `Internasional`, `Nasional`, dan `RFC3966`.
   - Validasi status nomor (`VALID` atau `INVALID / NON-STANDARD`).
   - Tipe nomor: Mobile (Seluler), Fixed Line (Telepon Rumah), VoIP, Toll-Free, dll.
   - Deteksi Negara, Kode Panggilan, & Zona Waktu (Timezone).

2. **Indonesia Deep HLR & Operator Intelligence:**
   - Deteksi operator seluler Indonesia: **Telkomsel**, **Indosat Ooredoo**, **XL Axiata**, **Tri (3)**, **Smartfren**, dan **AXIS**.
   - Identifikasi brand/produk (simPATI, Kartu Halo, by.U, IM3, XL Prioritas, dll.).
   - Deteksi kode area telepon kabel (PSTN Telkom) untuk puluhan kota di Indonesia (021, 022, 031, dll.).
   - Estimasi wilayah/kota pendaftaran kartu (HLR Lookup).

3. **Digital Footprint & OSINT Links:**
   - **Direct Platform Connect:** Buka WhatsApp Direct Chat (`wa.me`) dan profil Telegram tanpa simpan kontak.
   - **Public Reputation Repositories:** Link lookup cepat ke Truecaller, Sync.me, dan Kredibel.co.id.
   - **Automated Google Dorks:** Query otomatis untuk melacak jejak nomor di media sosial (FB, IG, X, LinkedIn, TikTok), file leak (PDF/Excel/Database), dan forum jual-beli.

4. **CLI User Experience (Rich TUI):**
   - Mode Interaktif dengan live terminal prompt.
   - Mode scan langsung per nomor.
   - Mode batch file (`-f`) dan export JSON (`-o`).

---

## 🚀 Cara Menjalankan

### 1. Mode Interaktif (Tanya-Jawab)
```bash
python3 phonesearch.py
```
Masukkan nomor telepon langsung di prompt terminal. Ketik `exit` atau `q` untuk keluar.

### 2. Scan Langsung Satu Nomor
```bash
python3 phonesearch.py 081288889999
```
Atau nomor internasional:
```bash
python3 phonesearch.py +14155552671
```

### 3. Batch Scan dari File Teks & Simpan ke JSON
```bash
python3 phonesearch.py -f samples.txt -o hasil_scan.json
```

---

## 📁 Struktur Direktori
```text
phonesearch/
├── phonesearch.py           # Entrypoint CLI utama
├── samples.txt              # Contoh daftar nomor telepon untuk pengujian
├── core/
│   ├── __init__.py
│   ├── analyzer.py          # Parser libphonenumber & validasi format
│   ├── hlr_indonesia.py     # Database prefix operator & HLR wilayah Indonesia
│   ├── osint_footprint.py   # Generator link OSINT & Google Dorks
│   └── ui.py                # Visualisasi terminal interaktif (Rich)
└── README.md
```

