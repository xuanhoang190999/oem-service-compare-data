import requests
from source.config.settings import REST_API_URL

def call_rest_api(endpoint: str, params: dict = None, headers: dict = None, timeout: int = 30, method: str = "GET", body: dict = None):
    try:
        url = REST_API_URL.rstrip("/") + "/" + endpoint.lstrip("/")

        default_headers = {
            "Content-Type": "application/json"
        }

        if headers:
            default_headers.update(headers)

        method = method.upper()
        if method == "GET":
            response = requests.get(url, params=params, headers=default_headers, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=body, headers=default_headers, timeout=timeout)
        elif method == "PUT":
            response = requests.put(url, json=body, headers=default_headers, timeout=timeout)
        elif method == "DELETE":
            response = requests.delete(url, headers=default_headers, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"[REST API Error] {e}")
        return None
