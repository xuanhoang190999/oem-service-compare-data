import json
import os
from datetime import datetime

CONFIG_PATH = os.path.join(os.getcwd(), "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Cannot find config file: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    required_keys = ["GRAPHQL_API_URL", "REST_API_URL", "APIS"]
    for key in required_keys:
        if key not in config:
            raise KeyError(f"Missing required config key: {key}")

    return config

def get_output_run_dir(base_dir="output"):
    today = datetime.now().strftime("%Y%m%d")
    date_dir = os.path.join(base_dir, today)

    run_index = 1
    while True:
        run_dir = os.path.join(date_dir, f"{run_index}")
        if not os.path.exists(run_dir):
            os.makedirs(run_dir, exist_ok=True)
            return run_dir
        run_index += 1

_config = load_config()

GRAPHQL_API_URL = _config["GRAPHQL_API_URL"]
REST_API_URL = _config["REST_API_URL"]
# IS_IGNORE_SORT = _config.get("Ignore_Sort", False)

APIS = [api for api in _config["APIS"] if api.get("enabled", True)]

INPUT_DIR = os.path.join(os.getcwd(), "input")
OUTPUT_DIR = get_output_run_dir(os.path.join(os.getcwd(), "output"))

print(f"Loaded config: {CONFIG_PATH}")
print(f"GraphQL: {GRAPHQL_API_URL}")
print(f"REST: {REST_API_URL}")
print(f"OUTPUT_DIR: {OUTPUT_DIR}")
# print(f"IGNORE SORT: {IS_IGNORE_SORT}")
print(f"Enabled APIs: {[a['name'] for a in APIS]}")
