import requests
import json
from source.config.settings import GRAPHQL_API_URL

def call_graphql_api(query: str, variables: dict = None, headers: dict = None, timeout: int = 30):
    try:
        payload = {"query": query, "variables": variables or {}}

        default_headers = {
            "Content-Type": "application/json"
        }

        if headers:
            default_headers.update(headers)

        response = requests.post(
            GRAPHQL_API_URL,
            json=payload,
            headers=default_headers,
            timeout=timeout
        )

        # If status != 200 -> throw exception
        response.raise_for_status() 
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"[GraphQL Error] {e}")
        return None
