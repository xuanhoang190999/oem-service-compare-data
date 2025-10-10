import pandas as pd
import requests
from source.config.settings import GRAPHQL_API_URL

def call_graphql(query: str):
    payload = {"query": query}
    response = requests.post(GRAPHQL_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("data")
    else:
        print(f"[GraphQL Error] {response.status_code}: {response.text}")
        return None

def get_ymme_graphql(market: str, year=None, make=None, model=None, trim=None, option=None):
    params = [f'db_market: "{market}"']

    if pd.notna(year):
        params.append(f"year: {int(year)}")
    if pd.notna(make):
        params.append(f"make: {int(make)}")
    if pd.notna(model):
        params.append(f"model: {int(model)}")
    if pd.notna(trim):
        params.append(f"trim: {int(trim)}")
    if pd.notna(option):
        params.append(f"option: {int(option)}")

    param_str = ", ".join(params)

    query = f"""{{
        ymmes({param_str}) {{
            text
            enum
        }}
    }}"""

    return call_graphql(query)

def vin_profile_graphql(raw64: str):
    query = f"""
    {{
        report(raw64: "{raw64}", language: 1) {{
            vinProfile {{
                vin
                year
                make
                manufacturer
                model
                engine
                trim
                option
                transmission
                bodyCode
                _make_enum
                year_enum
                make_enum
                manufacturer_enum
                model_enum
                engine_enum
                trim_enum
                option_enum
                transmission_enum
                bodyCode_enum
            }}
        }}
    }}
    """

    return call_graphql(query)

def vehicle_profile_graphql(vin: str):
    query = f"""
    {{
        getProfile(vin: "{vin}", compress: true) {{
            profile_base64
            profile_crc32
            profile_size
        }}
    }}
    """

    return call_graphql(query)

def dtcs_definition_graphql(raw64: str):
    query = f"""
    {{
        report(raw64: "{raw64}", language: 1) {{
                dtcs {{
                    code
                    definition
                    type
                    recommendstatus
                    systemName
                    system_enum
                    subsystemName
                    subsystem_enum
                    modulename
                    severity
                }}
            }}
    }}
    """

    return call_graphql(query)

def oem_livedata_graphql (
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
    query = ""
    payload_str = "[" + ",".join(f'"{p}"' for p in payloads) + "]"

    if vin is not None:
        query = f"""
        {{
            oemLiveItems(vin: "{vin}", payloads: {payload_str}, language: {language}, unitSystem: {unit_system}) {{
                data {{
                    itemid
                    itemname
                    itemname_enum
                    itemdescription
                    value
                    unit
                    text
                    itemdescription_enum
                }}
            }}
        }}
        """
    else:
        query = f"""
        {{
            oemLiveItems(
                year: {year},
                make: {make},
                model: {model},
                engine: {engine},
                trim: {trim},
                option: {option},
                payloads: [{payload_str}],
                language: {language},
                unitSystem: {unit_system}
            ) {{
                data {{
                    itemid
                    itemname
                    itemdescription
                    value
                    unit
                    text
                    itemdescription_enum
                }}
            }}
        }}
        """

    return call_graphql(query)

def oem_module_name_graphql(make: int, type_str: str, ids: list[int]):

    ids_str = ",".join(str(x) for x in ids)

    query = f"""
    {{
        enums(make: {make}, type: "{type_str}", ids: [{ids_str}]) {{
            edges {{
                node {{
                    key
                    value
                    english
                    spanish
                    french
                }}
            }}
        }}
    }}
    """

    return call_graphql(query)

def option_list_graphql(vin: str):
    query = f"""
    {{
        getOptionList (vin: "{vin}") {{
            data {{
                option_enum
                option1
                option2
                option3
            }}
        }}
    }}
    """

    return call_graphql(query)