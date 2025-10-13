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

# Use library: DeepDiff
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

# Custom comparison function
def custom_compare_api_responses(graphql_resp, rest_resp, row_index=1):
    differences = []
    
    if graphql_resp is None and rest_resp is None:
        graphql_resp = {}
        rest_resp = {}
    elif graphql_resp and rest_resp is None:
        differences.append({
            "Row Index": "",
            "Field": f"",
            "Status": "Rest Response is NULL",
            "REST": "",
            "GRAPHQL": ""
        })
        return differences
    elif rest_resp and graphql_resp is None:
        differences.append({
            "Row Index": "",
            "Field": f"",
            "Status": "GraphQL Response is NULL",
            "REST": "",
            "GRAPHQL": ""
        })
        return differences
        
    if isinstance(graphql_resp, list) and isinstance(rest_resp, list):
        max_len = max(len(graphql_resp), len(rest_resp))
        for i in range(max_len):
            g_item = graphql_resp[i] if i < len(graphql_resp) else None
            r_item = rest_resp[i] if i < len(rest_resp) else None

            if g_item is None:
                differences.append({
                    "Row Index": "",
                    "Field": f"[{i}]",
                    "Status": "Missing in GraphQL",
                    "REST": str(r_item),
                    "GRAPHQL": ""
                })
                continue

            if r_item is None:
                differences.append({
                    "Row Index": "",
                    "Field": f"[{i}]",
                    "Status": "Missing in REST",
                    "REST": "",
                    "GRAPHQL": str(g_item)
                })
                continue

            all_fields = sorted(set(g_item.keys()).union(r_item.keys()))
            for field in all_fields:
                g_has = field in g_item
                r_has = field in r_item
                g_val = g_item.get(field)
                r_val = r_item.get(field)

                if g_has and not r_has:
                    differences.append({
                        "Row Index": "",
                        "Field": f"[{i}].{field}",
                        "Status": "Missing in REST",
                        "REST": "",
                        "GRAPHQL": g_val
                    })
                    continue

                if r_has and not g_has:
                    differences.append({
                        "Row Index": "",
                        "Field": f"[{i}].{field}",
                        "Status": "Missing in GraphQL",
                        "REST": r_val,
                        "GRAPHQL": ""
                    })
                    continue

                if g_val != r_val:
                    differences.append({
                        "Row Index": "",
                        "Field": f"[{i}].{field}",
                        "Status": "Different",
                        "REST": r_val,
                        "GRAPHQL": g_val
                    })
    elif isinstance(graphql_resp, dict) and isinstance(rest_resp, dict):
        all_fields = sorted(set(graphql_resp.keys()).union(rest_resp.keys()))
        for field in all_fields:
            g_has = field in graphql_resp
            r_has = field in rest_resp

            if not g_has:
                differences.append({
                    "Row Index": "",
                    "Field": field,
                    "Status": "Missing in GraphQL",
                    "REST": rest_resp.get(field),
                    "GRAPHQL": ""
                })
            elif not r_has:
                differences.append({
                    "Row Index": "",
                    "Field": field,
                    "Status": "Missing in REST",
                    "REST": "",
                    "GRAPHQL": graphql_resp.get(field)
                })
            else:
                g_val, r_val = graphql_resp.get(field), rest_resp.get(field)
                if g_val != r_val:
                    differences.append({
                        "Row Index": "",
                        "Field": field,
                        "Status": "Different",
                        "REST": r_val,
                        "GRAPHQL": g_val
                    })
    else:
        differences.append({
            "Row Index": "",
            "Field": "root",
            "Status": "Type mismatch",
            "REST": str(type(rest_resp)),
            "GRAPHQL": str(type(graphql_resp))
        })

    return differences

# Custom comparison function sorting option
def custom_compare_ignore_sort_api_responses(graphql_resp, rest_resp, row_index=1, is_ignore_sort=False, object_id=None):
    differences = []

    if graphql_resp is None:
        graphql_resp = []
    if rest_resp is None:
        rest_resp = []

    if object_id is None:
        is_ignore_sort = False

    def to_dict_by_id(lst):
        if not isinstance(lst, list):
            return {}
        d = {}
        for i, item in enumerate(lst):
            if isinstance(item, dict) and object_id in item:
                d[str(item[object_id])] = (i, item)
        return d

    if isinstance(graphql_resp, list) and isinstance(rest_resp, list):
        g_dict = to_dict_by_id(graphql_resp)
        r_dict = to_dict_by_id(rest_resp)

        print("g_dict:", g_dict)

        all_ids = sorted(set(g_dict.keys()).union(r_dict.keys()))

        for obj_id in all_ids:
            g_entry = g_dict.get(obj_id)
            r_entry = r_dict.get(obj_id)

            g_index = g_entry[0] if g_entry else None
            r_index = r_entry[0] if r_entry else None

            g_item = g_entry[1] if g_entry else None
            r_item = r_entry[1] if r_entry else None

            # Missing cases
            if g_item is None:
                differences.append({
                    "Row Index": row_index,
                    "Field": f"[{r_index}]",
                    "Status": "Missing in GraphQL 1",
                    "REST": str(r_item),
                    "GRAPHQL": ""
                })
                continue

            if r_item is None:
                differences.append({
                    "Row Index": row_index,
                    "Field": f"[{g_index}]",
                    "Status": "Missing in REST 2",
                    "REST": "",
                    "GRAPHQL": str(g_item)
                })
                continue

            # Check position mismatch
            if not is_ignore_sort and g_index is not None and g_index != r_index:
                print(g_index, r_index, g_item, r_item)

                differences.append({
                    "Row Index": row_index,
                    "Field": f"[{r_index}]",
                    "Status": "Missing in GraphQL 3",
                    "REST": str(r_item),
                    "GRAPHQL": ""
                })
            elif not is_ignore_sort and r_index is not None and g_index != r_index:
                differences.append({
                    "Row Index": row_index,
                    "Field": f"[{g_index}]",
                    "Status": "Missing in Rest 4",
                    "REST": "",
                    "GRAPHQL": str(g_item)
                })

            # Compare fields
            all_fields = sorted(set(g_item.keys()).union(r_item.keys()))
            for field in all_fields:
                g_has = field in g_item
                r_has = field in r_item

                if not g_has:
                    differences.append({
                        "Row Index": row_index,
                        "Field": f"[{g_index}].{field}",
                        "Status": "Missing in GraphQL",
                        "REST": r_item.get(field),
                        "GRAPHQL": ""
                    })
                elif not r_has:
                    differences.append({
                        "Row Index": row_index,
                        "Field": f"[{r_index}].{field}",
                        "Status": "Missing in REST",
                        "REST": "",
                        "GRAPHQL": g_item.get(field)
                    })
                else:
                    g_val, r_val = g_item.get(field), r_item.get(field)
                    if g_val != r_val:
                        differences.append({
                            "Row Index": row_index,
                            "Field": f"[{g_index or r_index}].{field}",
                            "Status": "DIFFERENT",
                            "REST": r_val,
                            "GRAPHQL": g_val
                        })

    elif isinstance(graphql_resp, dict) and isinstance(rest_resp, dict):
        all_fields = sorted(set(graphql_resp.keys()).union(rest_resp.keys()))
        for field in all_fields:
            g_has = field in graphql_resp
            r_has = field in rest_resp

            if not g_has:
                differences.append({
                    "Row Index": row_index,
                    "Field": field,
                    "Status": "Missing in GraphQL",
                    "REST": rest_resp.get(field),
                    "GRAPHQL": ""
                })
            elif not r_has:
                differences.append({
                    "Row Index": row_index,
                    "Field": field,
                    "Status": "Missing in REST",
                    "REST": "",
                    "GRAPHQL": graphql_resp.get(field)
                })
            else:
                g_val, r_val = graphql_resp.get(field), rest_resp.get(field)
                if g_val != r_val:
                    differences.append({
                        "Row Index": row_index,
                        "Field": field,
                        "Status": "Different",
                        "REST": r_val,
                        "GRAPHQL": g_val
                    })

    else:
        differences.append({
            "Row Index": row_index,
            "Field": "root",
            "Status": "Type mismatch",
            "REST": str(type(rest_resp)),
            "GRAPHQL": str(type(graphql_resp))
        })

    return differences
