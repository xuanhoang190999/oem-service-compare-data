import requests

REST_API_BASE_URL = "http://18.142.11.42:5672/api"

def call_rest_get(endpoint: str, params: dict = None):
    url = f"{REST_API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params={k: v for k, v in (params or {}).items() if v not in [None, ""]})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as ex:
        print(f"[REST GET Error] {url}: {ex}")
        return None
    except ValueError as ex:
        print(f"[Parse Error] Cannot read file JSON: {ex}")
        return None

def call_rest_post(endpoint: str, data: dict = None):
    url = f"{REST_API_BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as ex:
        print(f"[REST POST Error] {url}: {ex}")
        return None
    except ValueError as ex:
        print(f"[Parse Error] Cannot read file JSON: {ex}")
        return None

def get_ymme_rest(market: str, year=None, make=None, model=None, engine=None,
                  trim=None, manufacturer=None, _make=None, option=None, procedure=None):
    params = {
        "db_market": market,
        "year": year,
        "make": make,
        "model": model,
        "engine": engine,
        "trim": trim,
        "manufacturer": manufacturer,
        "_make": _make,
        "option": option,
        "procedure": procedure
    }

    return call_rest_get("ymme", params)

def decode_vin_rest(vin: str):
    params = {"vin": vin}
    return call_rest_get("decode_vin", params)

def vin_profile_rest(raw64: str, language: int = 1):
    data = {
        "raw": raw64,
        "language": language
    }

    return call_rest_post("vehicleinfo", data)

def vehicle_profile_rest(vin: str):
    params = {
        "vin": vin
    }
    return call_rest_get("vehicle_profile", params)

def dtcs_definition_rest(raw64: str):
    data = {
        "raw64": raw64,
        "language": 1
    }

    return call_rest_post("report", data)