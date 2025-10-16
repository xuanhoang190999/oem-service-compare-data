import os
import logging
from datetime import datetime
import pandas as pd

LOG_DIR = os.path.join(os.getcwd(), "logs")

def setup_logger(name="compare_logger"):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filename = datetime.now().strftime("%Y%m%d") + ".log"
    log_path = os.path.join(LOG_DIR, log_filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_path, encoding="utf-8")
        ch = logging.StreamHandler()

        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger

def timestamp_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_int(value):
    if pd.isna(value):
        return None
    try:
        return int(value)
    except:
        return None

def normalize_for_compare(rest_resp, graphql_resp, key=None):
    if isinstance(rest_resp, dict) and key in rest_resp:
        rest_resp = rest_resp[key]
    if rest_resp is None:
        rest_resp = []

    if isinstance(graphql_resp, dict) and key in graphql_resp:
        graphql_resp = graphql_resp[key]
    if graphql_resp is None:
        graphql_resp = []

    return rest_resp, graphql_resp

def get_object_by_key(resp, key=None):
    if not key or not isinstance(resp, (dict, list)):
        return resp

    keys = key.split(".")

    current = resp
    for k in keys:
        if isinstance(current, dict):
            matched_key = next((kk for kk in current.keys() if kk.lower() == k.lower()), None)
            if matched_key is not None:
                current = current[matched_key]
            else:
                return None
        elif isinstance(current, list):
            if k.isdigit() and int(k) < len(current):
                current = current[int(k)]
            else:
                return None
        else:
            return None

    return current

def get_language(lan: str):
    match lan:
        case "Unknown":
            return 0
        case "US":
            return 1
        case "MX":
            return 2
        case "FR":
            return 3
        case "VN":
            return 6
        case _:
            return 1
