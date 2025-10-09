from deepdiff import DeepDiff

def get_value_from_path(obj, path):
    try:
        parts = path.replace("root", "").strip(".").split("[")
        current = obj
        for p in parts:
            if not p:
                continue
            key = p.strip("]'")
            if key.isdigit():
                current = current[int(key)]
            else:
                current = current.get(key)
        return current
    except Exception:
        return None

def normalize_response(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            return data

    if isinstance(data, dict):
        return {k: normalize_response(v) for k, v in data.items() if k != "__typename"}

    if isinstance(data, list):
        return [normalize_response(v) for v in data]

    return data

def compare_api_responses(graphql_resp, rest_resp, row_index=1):
    rest_resp = normalize_response(rest_resp)
    graphql_resp = normalize_response(graphql_resp)
    differences = []

    diff = DeepDiff(rest_resp, graphql_resp, ignore_order=True)
    if not diff:
        return differences

    for change_type, changes in diff.items():
        if change_type in ('dictionary_item_added', 'iterable_item_added'):
            for path in changes:
                new_val = get_value_from_path(graphql_resp, path)
                differences.append({
                    "Field": path,
                    "Status": "Missing in REST",
                    "REST": "",
                    "GRAPHQL": str(new_val)
                })

        elif change_type in ('dictionary_item_removed', 'iterable_item_removed'):
            for path in changes:
                old_val = get_value_from_path(rest_resp, path)
                differences.append({
                    "Field": path,
                    "Status": "Missing in GraphQL",
                    "REST": str(old_val),
                    "GRAPHQL": ""
                })

        elif change_type == "values_changed":
            for path, val in changes.items():
                old_val = val.get("old_value", "")
                new_val = val.get("new_value", "")
                differences.append({
                    "Field": path,
                    "Status": "DIFFERENT",
                    "REST": str(old_val),
                    "GRAPHQL": str(new_val)
                })

    return differences
