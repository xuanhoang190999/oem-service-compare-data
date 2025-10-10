import json
import os

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

_config = load_config()

GRAPHQL_API_URL = _config["GRAPHQL_API_URL"]
REST_API_URL = _config["REST_API_URL"]

APIS = [api for api in _config["APIS"] if api.get("enabled", True)]

INPUT_DIR = os.path.join(os.getcwd(), "input")
OUTPUT_DIR = os.path.join(os.getcwd(), "output")

print(f"Loaded config: {CONFIG_PATH}")
print(f"GraphQL: {GRAPHQL_API_URL}")
print(f"REST: {REST_API_URL}")
print(f"Enabled APIs: {[a['name'] for a in APIS]}")
