import requests
from source.config.settings import REST_API_URL

def call_rest_get(endpoint: str, params: dict = None):
    url = f"{REST_API_URL}/{endpoint}"
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
    url = f"{REST_API_URL}/{endpoint}"
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

def dtcs_definition_rest(raw64: str, language: int):
    data = {
        "raw64": raw64,
        "language": language
    }

    return call_rest_post("report", data)

def oem_livedata_rest (
    payloads: list[str],
    language: int = 1,
    unit_system: int = 1,
    vin: str = None,
    year: int = None,
    make: str = None,
    model: str = None,
    engine: str = None,
    trim: str = None,
    option: str = None
):
    payload_str = "[" + ",".join(f'"{p}"' for p in payloads) + "]"

    params = {
        "payloads": payload_str,
        "language": language,
        "unitSystem": unit_system,
        "vin": vin,
        "year": year,
        "make": make,
        "model": model,
        "engine": engine,
        "trim": trim,
        "option": option
    }

    return call_rest_get("livedata_items", params)

def oem_module_name_rest(make: int, type_str: str, ids: list[int]):
    ids_str = "[" + ",".join(str(x) for x in ids) + "]"

    params = {
        "make": make,
        "type": type_str,
        "ids": ids_str
    }

    return call_rest_get("enumeration", params)

def option_list_rest(vin: str):
    params = {
        "vin": vin
    }

    return call_rest_get("option_list", params)