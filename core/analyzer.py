import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from core.hlr_indonesia import lookup_indonesia_operator

NUMBER_TYPE_MAP = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line (Telepon Kabel)",
    phonenumbers.PhoneNumberType.MOBILE: "Mobile (Seluler)",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line / Mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free (Bebas Pulsa)",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
    phonenumbers.PhoneNumberType.VOIP: "VoIP (Voice over IP)",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    phonenumbers.PhoneNumberType.PAGER: "Pager",
    phonenumbers.PhoneNumberType.UAN: "UAN (Universal Access Number)",
    phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
    phonenumbers.PhoneNumberType.UNKNOWN: "Unknown Type",
}


def analyze_phone_number(raw_input: str, default_region: str = "ID") -> dict:
    """
    Parses and extracts deep technical, carrier, and geopolitical details for a phone number.
    """
    raw_cleaned = raw_input.strip()

    # Auto-prefix '+' ONLY if input is exactly country-code + subscriber pattern
    # e.g. "628123456789" (12-13 digits starting with 62) — NOT short numbers like "6234567"
    if raw_cleaned.startswith("62") and not raw_cleaned.startswith("+62") and len(raw_cleaned) >= 11:
        raw_cleaned = "+" + raw_cleaned

    try:
        parsed_num = phonenumbers.parse(raw_cleaned, default_region)
    except phonenumbers.NumberParseException as e:
        return {
            "success": False,
            "raw_input": raw_input,
            "error": str(e),
        }

    is_valid = phonenumbers.is_valid_number(parsed_num)
    is_possible = phonenumbers.is_possible_number(parsed_num)
    region_code = phonenumbers.region_code_for_number(parsed_num) or "UNKNOWN"

    # Standard telecom formats
    e164 = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164)
    international = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    national = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.NATIONAL)
    rfc3966 = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.RFC3966)

    # Carrier & Geolocation from Google libphonenumber
    geo_desc = geocoder.description_for_number(parsed_num, "id") or geocoder.description_for_number(parsed_num, "en") or "Unknown"
    carrier_name = carrier.name_for_number(parsed_num, "id") or carrier.name_for_number(parsed_num, "en") or "Unknown"
    tz_list = list(timezone.time_zones_for_number(parsed_num)) or ["Unknown"]

    num_type_enum = phonenumbers.number_type(parsed_num)
    type_str = NUMBER_TYPE_MAP.get(num_type_enum, "Unknown")

    # Indonesia Deep HLR Inspection
    id_hlr_info = None
    if region_code == "ID":
        id_hlr_info = lookup_indonesia_operator(national)
        # If libphonenumber carrier is empty or generic, fill from Indonesian HLR DB
        if carrier_name == "Unknown" and id_hlr_info["operator"] not in ("Unknown", "Unknown / Unregistered Prefix", "Unknown / Terlalu Pendek"):
            carrier_name = id_hlr_info["operator"]

    return {
        "success": True,
        "raw_input": raw_input,
        "is_valid": is_valid,
        "is_possible": is_possible,
        "country_code": parsed_num.country_code,
        "national_number": str(parsed_num.national_number),
        "region_code": region_code,
        "formats": {
            "e164": e164,
            "international": international,
            "national": national,
            "rfc3966": rfc3966,
        },
        "carrier": carrier_name,
        "location": geo_desc,
        "timezones": tz_list,
        "number_type": type_str,
        "indonesia_hlr": id_hlr_info,
    }
