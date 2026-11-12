# 📱 PhoneSearch - Phone Intelligence & Anti-Scam OSINT Tool

Tools intelijen nomor telepon dan pendeteksi penipuan/spam berbasis CLI interaktif. Dilengkapi validasi standar internasional, deteksi operator & HLR Indonesia, mesin penilaian risiko penipuan (Risk Engine), crowdsourced community reporting, dan live OSINT reconnaissance.

---

## 📦 Instalasi Dependensi

Pastikan modul yang dibutuhkan sudah terinstall (terutama jika menggunakan Conda / Virtualenv):

```bash
pip install -r requirements.txt
```

Atau install langsung:
```bash
pip install phonenumbers rich requests beautifulsoup4
```

---

## ✨ Fitur-Fitur Utama

### 1. 🔍 Phone Intelligence & HLR Reconnaissance (Tahap 1)
* **Validasi Standar Internasional:** Format `E.164`, `Nasional`, `Internasional`, dan `RFC3966`.
* **Deteksi Operator Indonesia:** Telkomsel, Indosat Ooredoo, XL Axiata, Tri (3), Smartfren, AXIS, serta telepon rumah (PSTN Telkom).
* **HLR (Home Location Register):** Estimasi wilayah dan kota pendaftaran kartu SIM berdasarkan prefix.
* **Direct Profiling:** Link chat WhatsApp langsung tanpa simpan kontak (`wa.me`) dan link profil Telegram.
* **OSINT Search & Google Dorks:** Query pencarian otomatis untuk mencari jejak nomor di media sosial, database kebocoran file (PDF/Excel), dan forum jual-beli.
* **Live Web Recon:** Otomatis mengambil snippet / cuplikan dari search engine jika nomor pernah disebut di situs publik.

### 2. 🛡️ Spam & Scam Checker (Tahap 2)
* **Scam & Fraud Database Lokal:** Database nomor penipuan dengan kategori terstruktur (Modus Kurir Paket APK, CS Bank Palsu / Phishing OTP, Loker Freelance / Like Video Palsu, Pinjol Ilegal / Teror, Telemarketing).
* **Risk Scoring Engine (0 - 100%):** Kalkulasi tingkat bahaya secara cerdas dari rekam jejak komunitas, temuan sentimen web, dan anomali tipe nomor (VoIP/Virtual).
* **Visual Risk Meter & Rekomendasi:** Indikator visual meter risiko (`LOW`, `MEDIUM`, `HIGH`) disertai panduan tindakan (misal: "BLOKIR SEGERA", "WASPADA JANGAN BAGIKAN OTP").
* **Community Crowdsourced Reporting:** Laporkan nomor penipu baru langsung dari terminal agar masuk ke database lokal.
* **Top Scammer Watchlist:** Tampilkan daftar nomor penipuan dan spammer yang paling banyak dilaporkan.

---

## 🚀 Panduan Penggunaan

### 1. Mode Interaktif (Tanya-Jawab Terminal)
```bash
python3 phonesearch.py
```
Di mode ini, kamu bisa:
* Masukkan nomor telepon apa saja untuk diinvestigasi.
* Ketik **`report`** atau **`lapor`** untuk melaporkan nomor penipu baru.
* Ketik **`top`** untuk melihat daftar nomor penipuan teratas.
* Ketik **`exit`** atau **`q`** untuk keluar.

---

### 2. Investigasi Langsung Satu Nomor
```bash
python3 phonesearch.py 081299990001
```
Atau nomor luar negeri:
```bash
python3 phonesearch.py +14155552671
```

---

### 3. Laporkan Nomor Penipu / Spam Baru
```bash
python3 phonesearch.py --report 081234567890
```
Kamu akan dipandu memilih kategori kejahatan, tag modus, dan kronologi singkat.

---

### 4. Lihat Daftar Nomor Penipuan Terbanyak Dilaporkan
```bash
python3 phonesearch.py --list-scams
```

---

### 5. Scan Batch dari File Daftar Nomor & Export JSON
```bash
python3 phonesearch.py -f samples.txt -o hasil_scan.json --no-web
```

---

## 📁 Struktur Project
```text
phonesearch/
├── phonesearch.py             # CLI entrypoint utama
├── requirements.txt           # Dependensi Python
├── samples.txt                # File contoh nomor untuk uji coba
├── data/
│   └── scam_database.json     # Database lokal penipuan & spam komunitas
├── core/
│   ├── analyzer.py            # Parser format telekomunikasi & libphonenumber
│   ├── hlr_indonesia.py       # Database prefix operator & HLR wilayah Indonesia
│   ├── osint_footprint.py     # Generator link direct chat, lookup & Google Dorks
│   ├── web_search.py          # Live web search engine & dorking crawler
│   ├── scam_db.py             # Pengelola database penipuan & reporting
│   ├── risk_engine.py         # Kalkulator skor risiko (Risk Score 0-100%)
│   └── ui.py                  # Tampilan Rich visual (Tabel, Gauge Meter, Badges)
└── README.md                  # Dokumentasi project
```
