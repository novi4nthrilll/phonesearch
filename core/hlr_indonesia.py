"""
HLR & Operator Database for Indonesian Phone Numbers
Maps prefix and sub-prefix to Operator, Product Brand, and Estimated Region/City.
"""

OPERATOR_PREFIXES = {
    # Telkomsel
    "0811": {"operator": "Telkomsel", "brand": "Kartu Halo (Pascabayar)", "type": "Mobile"},
    "0812": {"operator": "Telkomsel", "brand": "simPATI / Halo", "type": "Mobile"},
    "0813": {"operator": "Telkomsel", "brand": "simPATI", "type": "Mobile"},
    "0821": {"operator": "Telkomsel", "brand": "simPATI", "type": "Mobile"},
    "0822": {"operator": "Telkomsel", "brand": "simPATI / Loop", "type": "Mobile"},
    "0823": {"operator": "Telkomsel", "brand": "Kartu As", "type": "Mobile"},
    "0851": {"operator": "Telkomsel", "brand": "by.U / Kartu As", "type": "Mobile"},
    "0852": {"operator": "Telkomsel", "brand": "Kartu As", "type": "Mobile"},
    "0853": {"operator": "Telkomsel", "brand": "Kartu As", "type": "Mobile"},

    # Indosat Ooredoo Hutchison (IM3)
    "0814": {"operator": "Indosat Ooredoo", "brand": "Indosat M2 (Broadband)", "type": "Data"},
    "0815": {"operator": "Indosat Ooredoo", "brand": "Matrix / Mentari", "type": "Mobile"},
    "0816": {"operator": "Indosat Ooredoo", "brand": "Matrix / Mentari", "type": "Mobile"},
    "0855": {"operator": "Indosat Ooredoo", "brand": "Matrix (Pascabayar)", "type": "Mobile"},
    "0856": {"operator": "Indosat Ooredoo", "brand": "IM3", "type": "Mobile"},
    "0857": {"operator": "Indosat Ooredoo", "brand": "IM3", "type": "Mobile"},
    "0858": {"operator": "Indosat Ooredoo", "brand": "Mentari / IM3", "type": "Mobile"},

    # Indosat Ooredoo Hutchison (Tri / 3)
    "0895": {"operator": "Tri (3) Indonesia", "brand": "3 (Tri)", "type": "Mobile"},
    "0896": {"operator": "Tri (3) Indonesia", "brand": "3 (Tri)", "type": "Mobile"},
    "0897": {"operator": "Tri (3) Indonesia", "brand": "3 (Tri)", "type": "Mobile"},
    "0898": {"operator": "Tri (3) Indonesia", "brand": "3 (Tri)", "type": "Mobile"},
    "0899": {"operator": "Tri (3) Indonesia", "brand": "3 (Tri)", "type": "Mobile"},

    # XL Axiata
    "0817": {"operator": "XL Axiata", "brand": "XL Prabayar / Prioritas", "type": "Mobile"},
    "0818": {"operator": "XL Axiata", "brand": "XL Prabayar", "type": "Mobile"},
    "0819": {"operator": "XL Axiata", "brand": "XL Prabayar", "type": "Mobile"},
    "0859": {"operator": "XL Axiata", "brand": "XL Prabayar", "type": "Mobile"},
    "0877": {"operator": "XL Axiata", "brand": "XL Prabayar", "type": "Mobile"},
    "0878": {"operator": "XL Axiata", "brand": "XL Prabayar", "type": "Mobile"},

    # AXIS (XL Axiata)
    "0831": {"operator": "AXIS (XL Axiata)", "brand": "AXIS", "type": "Mobile"},
    "0832": {"operator": "AXIS (XL Axiata)", "brand": "AXIS", "type": "Mobile"},
    "0833": {"operator": "AXIS (XL Axiata)", "brand": "AXIS", "type": "Mobile"},
    "0838": {"operator": "AXIS (XL Axiata)", "brand": "AXIS", "type": "Mobile"},

    # Smartfren
    "0881": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0882": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0883": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0884": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0885": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0886": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0887": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0888": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
    "0889": {"operator": "Smartfren", "brand": "Smartfren", "type": "Mobile"},
}

# Regional area codes for Indonesian Fixed Lines (PSTN)
AREA_CODES_INDONESIA = {
    "021": "Jabodetabek, Banten (Jakarta, Bogor, Depok, Tangerang, Bekasi)",
    "022": "Bandung, Cimahi (Jawa Barat)",
    "0231": "Cirebon (Jawa Barat)",
    "0232": "Kuningan (Jawa Barat)",
    "0233": "Majalengka (Jawa Barat)",
    "0234": "Indramayu (Jawa Barat)",
    "024": "Semarang (Jawa Tengah)",
    "0251": "Bogor (Jawa Barat)",
    "0252": "Lebak (Banten)",
    "0253": "Pandeglang (Banten)",
    "0254": "Serang, Cilegon (Banten)",
    "0260": "Subang (Jawa Barat)",
    "0261": "Sumedang (Jawa Barat)",
    "0262": "Garut (Jawa Barat)",
    "0263": "Cianjur (Jawa Barat)",
    "0264": "Purwakarta (Jawa Barat)",
    "0265": "Tasikmalaya, Ciamis, Banjar (Jawa Barat)",
    "0266": "Sukabumi (Jawa Barat)",
    "0267": "Karawang (Jawa Barat)",
    "0271": "Surakarta / Solo (Jawa Tengah)",
    "0272": "Klaten (Jawa Tengah)",
    "0273": "Wonogiri (Jawa Tengah)",
    "0274": "DI Yogyakarta (Yogyakarta, Sleman, Bantul, Gunungkidul, Kulon Progo)",
    "0275": "Purworejo (Jawa Tengah)",
    "0276": "Boyolali (Jawa Tengah)",
    "0281": "Purwokerto, Banyumas (Jawa Tengah)",
    "0282": "Cilacap (Jawa Tengah)",
    "0283": "Tegal, Brebes (Jawa Tengah)",
    "0284": "Pemalang (Jawa Tengah)",
    "0285": "Pekalongan, Batang (Jawa Tengah)",
    "0291": "Kudus, Demak, Jepara (Jawa Tengah)",
    "0293": "Magelang (Jawa Tengah)",
    "0298": "Salatiga (Jawa Tengah)",
    "031": "Surabaya, Sidoarjo, Gresik (Jawa Timur)",
    "0321": "Mojokerto, Jombang (Jawa Timur)",
    "0331": "Jember (Jawa Timur)",
    "0333": "Banyuwangi (Jawa Timur)",
    "0341": "Malang, Batu (Jawa Timur)",
    "0342": "Blitar (Jawa Timur)",
    "0343": "Pasuruan (Jawa Timur)",
    "0351": "Madiun, Ngawi, Magetan (Jawa Timur)",
    "0354": "Kediri (Jawa Timur)",
    "0361": "Denpasar, Badung, Gianyar, Tabanan (Bali)",
    "0370": "Mataram, Lombok Barat (NTB)",
    "0380": "Kupang (NTT)",
    "061": "Medan, Binjai, Deli Serdang (Sumatera Utara)",
    "0651": "Banda Aceh (Aceh)",
    "0711": "Palembang (Sumatera Selatan)",
    "0721": "Bandar Lampung (Lampung)",
    "0741": "Jambi (Jambi)",
    "0751": "Padang, Pariaman (Sumatera Barat)",
    "0761": "Pekanbaru (Riau)",
    "0778": "Batam (Kepulauan Riau)",
    "0511": "Banjarmasin, Banjarbaru (Kalimantan Selatan)",
    "0541": "Samarinda (Kalimantan Timur)",
    "0542": "Balikpapan (Kalimantan Timur)",
    "0561": "Pontianak (Kalimantan Barat)",
    "0411": "Makassar, Maros, Gowa (Sulawesi Selatan)",
    "0431": "Manado, Tomohon (Sulawesi Utara)",
    "0451": "Palu (Sulawesi Tengah)",
    "0911": "Ambon (Maluku)",
    "0967": "Jayapura (Papua)",
}

# Detailed HLR mapping samples for Indonesia Mobile (Telkomsel/Indosat/XL)
HLR_PREFIX_SAMPLES = {
    # Telkomsel 0812 / 0813 / 0821 regions
    "08111": "Jakarta / Jabodetabek",
    "08112": "Jawa Tengah & DIY (Semarang, Solo, Jogja)",
    "08113": "Jawa Timur (Surabaya, Malang)",
    "08114": "Sulawesi & Maluku",
    "08115": "Kalimantan (Balikpapan, Banjarmasin)",
    "08116": "Sumatera Bagian Utara (Medan, Aceh)",
    "08117": "Sumatera Bagian Selatan & Tengah (Palembang, Pekanbaru)",
    "08118": "Jakarta / Jabodetabek",
    "08119": "Jakarta / Jabodetabek",
    "08121": "Jabodetabek / Banten",
    "08122": "Jawa Barat (Bandung & sekitarnya)",
    "08123": "Jawa Timur / Bali / Nusa Tenggara",
    "08124": "Sulawesi / Papua / Maluku",
    "08125": "Kalimantan",
    "08126": "Sumatera Bagian Utara / Riau",
    "08127": "Sumatera Bagian Selatan / Barat",
    "08128": "Jabodetabek",
    "08129": "Jabodetabek / Banten",
    "08131": "Jabodetabek / Jakarta",
    "08132": "Jawa Tengah / DIY",
    "08133": "Jawa Timur / Bali",
    "08134": "Sulawesi / Maluku / Papua",
    "08135": "Kalimantan",
    "08136": "Sumatera Utara / Aceh",
    "08137": "Sumatera Selatan / Lampung",
    "08138": "Jabodetabek / Banten",
    "08139": "Jawa Tengah / Solo / Jogja",
    "08211": "Jabodetabek / Banten",
    "08212": "Jabodetabek / Jawa Barat",
    "08213": "Jawa Tengah / DIY",
    "08214": "Jawa Timur / Bali",
    "08217": "Sumatera Barat / Riau",
    "08218": "Sumatera Selatan / Lampung",
    "08526": "Sumatera Utara / Riau",
    "08527": "Sumatera Bagian Selatan",
    "08536": "Sumatera Bagian Utara",

    # Indosat 0815 / 0816 / 0856 / 0857
    "08151": "Jakarta / Jabodetabek",
    "08152": "Kalimantan",
    "08153": "Sumatera",
    "08154": "Jawa Tengah / Banyumas",
    "08155": "Jawa Timur",
    "08156": "Jawa Barat / Bandung",
    "08157": "DI Yogyakarta & Solo",
    "08158": "Jakarta / Tangerang",
    "08159": "Jakarta / Bekasi",
    "08561": "Jakarta / Tangerang",
    "08562": "Jawa Tengah / Solo / Jogja",
    "08563": "Jawa Timur (Surabaya)",
    "08564": "Jawa Tengah (Semarang)",
    "08565": "Kalimantan",
    "08566": "Sumatera Utara (Medan)",
    "08567": "Jakarta / Bogor / Depok",
    "08568": "Bekasi / Cikarang",
    "08569": "Banten / Tangerang",
    "08571": "Jabodetabek",
    "08572": "Jawa Barat / Cirebon / Bandung",
    "08573": "Jawa Timur (Malang / Kediri)",
    "08574": "Jawa Tengah (Purwokerto / Solo)",
    "08575": "Kalimantan / Sulawesi",
    "08576": "Sumatera",
    "08578": "Jabodetabek",

    # XL 0817 / 0818 / 0819 / 0877 / 0878
    "08171": "Jabodetabek",
    "08172": "Jawa Barat (Bandung)",
    "08174": "Jawa Tengah / Semarang",
    "08175": "Jawa Timur / Bali / Lombok",
    "08176": "Jakarta",
    "08177": "Banten / Tangerang",
    "08178": "Jakarta Selatan / Depok",
    "08179": "DI Yogyakarta",
    "08181": "Jabodetabek",
    "08182": "Jawa Tengah / Solo",
    "08183": "Jawa Timur (Surabaya)",
    "08184": "Kalimantan",
    "08185": "Bali / Nusa Tenggara",
    "08186": "Sumatera",
    "08777": "Banten / Serang / Tangerang",
    "08778": "Jabodetabek",
    "08787": "Jabodetabek / Jawa Barat",
    "08788": "Jabodetabek",
}


def lookup_indonesia_operator(national_number: str) -> dict:
    """
    Given a national phone number starting with '0' (e.g. '08123456789' or '0211234567'),
    lookup operator, brand, type, and estimated region.
    """
    cleaned = national_number.replace("-", "").replace(" ", "").strip()
    if not cleaned.startswith("0"):
        cleaned = "0" + cleaned

    if len(cleaned) < 3:
        return {
            "operator": "Unknown / Terlalu Pendek",
            "brand": "Unknown",
            "type": "Unknown",
            "prefix": cleaned,
            "estimated_region": "Unknown",
        }

    # 1. Check Mobile Prefixes (4 digits: 08xx)
    prefix_4 = cleaned[:4]
    if prefix_4 in OPERATOR_PREFIXES:
        meta = OPERATOR_PREFIXES[prefix_4].copy()

        # Check HLR for region estimation (5 digits are more specific)
        prefix_5 = cleaned[:5]
        region = HLR_PREFIX_SAMPLES.get(prefix_5, "Indonesia (Wilayah spesifik bervariasi / Alokasi Nasional)")

        meta["estimated_region"] = region
        meta["prefix"] = prefix_4
        return meta

    # 2. Check Fixed-Line Area Codes (PSTN)
    # Try longer (4-digit) codes first, then shorter (3-digit)
    for length in (4, 3):
        area_code = cleaned[:length]
        if area_code in AREA_CODES_INDONESIA:
            return {
                "operator": "Telkom Indonesia (PSTN / Fixed Line)",
                "brand": "Telepon Rumah / Kantor",
                "type": "Fixed Line",
                "prefix": area_code,
                "estimated_region": AREA_CODES_INDONESIA[area_code],
            }

    return {
        "operator": "Unknown / Unregistered Prefix",
        "brand": "Unknown",
        "type": "Unknown",
        "prefix": cleaned[:4],
        "estimated_region": "Unknown",
    }
