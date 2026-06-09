import os
import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
BASE_CURRENCY    = "USD"   # Universal base — all costs stored in USD

DESTINATION_CURRENCIES = {
    # USA
    "New York":          {"code": "USD", "symbol": "$",   "name": "US Dollar"},
    # Europe
    "Paris":             {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Barcelona":         {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Rome":              {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Amsterdam":         {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Lisbon":            {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Vienna":            {"code": "EUR", "symbol": "€",   "name": "Euro"},
    "Prague":            {"code": "CZK", "symbol": "Kč",  "name": "Czech Koruna"},
    "London":            {"code": "GBP", "symbol": "£",   "name": "British Pound"},
    "Zurich":            {"code": "CHF", "symbol": "Fr",  "name": "Swiss Franc"},
    # Middle East
    "Dubai":             {"code": "AED", "symbol": "د.إ", "name": "UAE Dirham"},
    "Istanbul":          {"code": "TRY", "symbol": "₺",   "name": "Turkish Lira"},
    "Cairo":             {"code": "EGP", "symbol": "E£",  "name": "Egyptian Pound"},
    "Marrakech":         {"code": "MAD", "symbol": "MAD", "name": "Moroccan Dirham"},
    # Asia
    "Tokyo":             {"code": "JPY", "symbol": "¥",   "name": "Japanese Yen"},
    "Bali":              {"code": "IDR", "symbol": "Rp",  "name": "Indonesian Rupiah"},
    "Bangkok":           {"code": "THB", "symbol": "฿",   "name": "Thai Baht"},
    "Phuket":            {"code": "THB", "symbol": "฿",   "name": "Thai Baht"},
    "Singapore":         {"code": "SGD", "symbol": "S$",  "name": "Singapore Dollar"},
    "Kuala Lumpur":      {"code": "MYR", "symbol": "RM",  "name": "Malaysian Ringgit"},
    "New Delhi":         {"code": "INR", "symbol": "₹",   "name": "Indian Rupee"},
    "Mumbai":            {"code": "INR", "symbol": "₹",   "name": "Indian Rupee"},
    # Oceania
    "Sydney":            {"code": "AUD", "symbol": "A$",  "name": "Australian Dollar"},
    "Vancouver":         {"code": "CAD", "symbol": "C$",  "name": "Canadian Dollar"},
    "Toronto":           {"code": "CAD", "symbol": "C$",  "name": "Canadian Dollar"},
    # Americas
    "Cancun":            {"code": "MXN", "symbol": "MX$", "name": "Mexican Peso"},
    "Rio de Janeiro":    {"code": "BRL", "symbol": "R$",  "name": "Brazilian Real"},
    "Buenos Aires":      {"code": "ARS", "symbol": "AR$", "name": "Argentine Peso"},
    # Africa — East
    "Nairobi":           {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Maasai Mara":       {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Diani Beach":       {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Amboseli":          {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Mombasa":           {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Lamu":              {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Mount Kenya":       {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Lake Nakuru":       {"code": "KES", "symbol": "KSh", "name": "Kenyan Shilling"},
    "Serengeti":         {"code": "TZS", "symbol": "TSh", "name": "Tanzanian Shilling"},
    "Zanzibar":          {"code": "TZS", "symbol": "TSh", "name": "Tanzanian Shilling"},
    "Victoria Falls":    {"code": "USD", "symbol": "$",   "name": "US Dollar"},
    "Kigali":            {"code": "RWF", "symbol": "RF",  "name": "Rwandan Franc"},
    "Addis Ababa":       {"code": "ETB", "symbol": "Br",  "name": "Ethiopian Birr"},
    # Africa — West
    "Lagos":             {"code": "NGN", "symbol": "₦",   "name": "Nigerian Naira"},
    "Accra":             {"code": "GHS", "symbol": "GH₵", "name": "Ghanaian Cedi"},
    # Africa — South
    "Cape Town":         {"code": "ZAR", "symbol": "R",   "name": "South African Rand"},
    # Indian Ocean
    "Maldives":          {"code": "USD", "symbol": "$",   "name": "US Dollar"},
}

SUPPORTED_CURRENCIES = {
    "USD": {"symbol": "$",    "name": "US Dollar 🇺🇸"},
    "EUR": {"symbol": "€",    "name": "Euro 🇪🇺"},
    "GBP": {"symbol": "£",    "name": "British Pound 🇬🇧"},
    "JPY": {"symbol": "¥",    "name": "Japanese Yen 🇯🇵"},
    "AUD": {"symbol": "A$",   "name": "Australian Dollar 🇦🇺"},
    "CAD": {"symbol": "C$",   "name": "Canadian Dollar 🇨🇦"},
    "CHF": {"symbol": "Fr",   "name": "Swiss Franc 🇨🇭"},
    "AED": {"symbol": "د.إ",  "name": "UAE Dirham 🇦🇪"},
    "INR": {"symbol": "₹",    "name": "Indian Rupee 🇮🇳"},
    "CNY": {"symbol": "¥",    "name": "Chinese Yuan 🇨🇳"},
    "SGD": {"symbol": "S$",   "name": "Singapore Dollar 🇸🇬"},
    "MYR": {"symbol": "RM",   "name": "Malaysian Ringgit 🇲🇾"},
    "THB": {"symbol": "฿",    "name": "Thai Baht 🇹🇭"},
    "IDR": {"symbol": "Rp",   "name": "Indonesian Rupiah 🇮🇩"},
    "KES": {"symbol": "KSh",  "name": "Kenyan Shilling 🇰🇪"},
    "TZS": {"symbol": "TSh",  "name": "Tanzanian Shilling 🇹🇿"},
    "ZAR": {"symbol": "R",    "name": "South African Rand 🇿🇦"},
    "NGN": {"symbol": "₦",    "name": "Nigerian Naira 🇳🇬"},
    "GHS": {"symbol": "GH₵",  "name": "Ghanaian Cedi 🇬🇭"},
    "RWF": {"symbol": "RF",   "name": "Rwandan Franc 🇷🇼"},
    "ETB": {"symbol": "Br",   "name": "Ethiopian Birr 🇪🇹"},
    "UGX": {"symbol": "USh",  "name": "Ugandan Shilling 🇺🇬"},
    "TRY": {"symbol": "₺",    "name": "Turkish Lira 🇹🇷"},
    "EGP": {"symbol": "E£",   "name": "Egyptian Pound 🇪🇬"},
    "MAD": {"symbol": "MAD",  "name": "Moroccan Dirham 🇲🇦"},
    "MXN": {"symbol": "MX$",  "name": "Mexican Peso 🇲🇽"},
    "BRL": {"symbol": "R$",   "name": "Brazilian Real 🇧🇷"},
    "ARS": {"symbol": "AR$",  "name": "Argentine Peso 🇦🇷"},
    "CZK": {"symbol": "Kč",   "name": "Czech Koruna 🇨🇿"},
}


def get_exchange_rates(base_currency="USD"):
    """Fetch live exchange rates from base currency."""
    try:
        url      = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == "success":
                return {
                    "success":      True,
                    "rates":        data["conversion_rates"],
                    "base":         base_currency,
                    "last_updated": data.get("time_last_update_utc", "N/A"),
                }
            return {"success": False, "error": data.get("error-type", "Unknown error")}
        elif response.status_code == 401:
            return {"success": False, "error": "Invalid API key."}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No internet connection."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def convert_currency(amount, from_currency, to_currency, rates):
    """Convert amount using pre-fetched rates based on from_currency."""
    if from_currency == to_currency:
        return amount
    rate = rates.get(to_currency)
    if rate is None:
        return None
    return amount * rate


def get_destination_currency(destination):
    """Return local currency info for a destination."""
    return DESTINATION_CURRENCIES.get(
        destination,
        {"code": "USD", "symbol": "$", "name": "US Dollar"},
    )


def format_currency(amount, currency_code):
    """Format a number as currency with symbol."""
    if amount is None:
        return "N/A"
    info   = SUPPORTED_CURRENCIES.get(currency_code, {"symbol": currency_code})
    symbol = info["symbol"]
    if abs(amount) >= 1_000_000:
        return f"{symbol}{amount/1_000_000:.1f}M"
    elif abs(amount) >= 1_000:
        return f"{symbol}{amount:,.0f}"
    else:
        return f"{symbol}{amount:.2f}"