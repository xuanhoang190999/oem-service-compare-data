import pandas as pd
from source.utils.excel_io import read_input_excel, write_output_excel
from source.utils.utils import setup_logger, safe_int, normalize_for_compare, get_object_by_key

from source.config.graphql_common import ( get_ymme_graphql, vin_profile_graphql, vehicle_profile_graphql, 
dtcs_definition_graphql, oem_livedata_graphql, oem_module_name_graphql, option_list_graphql )

from source.config.rest_common import ( get_ymme_rest, decode_vin_rest, vin_profile_rest, vehicle_profile_rest,
dtcs_definition_rest, oem_livedata_rest, oem_module_name_rest, option_list_rest )

from source.core.compare import compare_api_responses
from source.core.raw import build_oem_module_raw_data
from source.core.payload import get_payloads_by_service_check_raw

from source.utils.utils import setup_logger
logger = setup_logger()

def compare_api_ymme(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")
            vin_info_response = decode_vin_rest(vin)

            if vin_info_response is None:
                raise ValueError("Invalid VIN decode response from REST API")

            market = row.get("Market")
            year = safe_int(vin_info_response.get("year_enum"))
            make = safe_int(vin_info_response.get("make_enum"))
            model = safe_int(vin_info_response.get("model_enum"))
            trim = safe_int(vin_info_response.get("trim_enum"))
            option = safe_int(vin_info_response.get("option_enum"))

            graphql_response = get_ymme_graphql(
                market=market, year=year, make=make, model=model, trim=trim, option=option
            )
            rest_response = get_ymme_rest(
                market=market, year=year, make=make, model=model, trim=trim, option=option
            )

            rest_norm, graphql_norm = normalize_for_compare(rest_response, graphql_response, key="ymmes")
            differences = compare_api_responses(graphql_norm, rest_norm, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_vin_profile(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")
            vin_profile_raw = row.get("VINProfile")

            oem_module_raw_data = build_oem_module_raw_data(vin_profile_raw, [])

            graphql_response = vin_profile_graphql(raw64=oem_module_raw_data)
            # rest_response = vin_profile_rest(raw64=oem_module_raw_data, language=1)
            rest_response = decode_vin_rest(vin=vin)

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "report.vinProfile")

            differences = compare_api_responses(graphql_norm, rest_response, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_vehicle_profile(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")

            graphql_response = vehicle_profile_graphql(vin=vin)
            rest_response = vehicle_profile_rest(vin=vin)

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "data.getProfile")

            differences = compare_api_responses(graphql_norm, rest_response, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_dtcs_definition(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")
            vin_profile_raw = row.get("VINProfile")
            oem_module_buffer_raw = row.get("OEMModuleBuffer")
            oem_module_buffer_raw_list = oem_module_buffer_raw.split(",")

            oem_module_raw_data = build_oem_module_raw_data(vin_profile_raw, oem_module_buffer_raw_list)

            graphql_response = dtcs_definition_graphql(raw64=oem_module_raw_data)
            rest_response = dtcs_definition_rest(raw64=oem_module_raw_data)

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "report.dtcs")

            differences = compare_api_responses(graphql_norm, rest_response, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_oem_livedata(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")
            service_check_raw = row.get("Payload")

            # decode payloads by service_check_raw
            payloads = get_payloads_by_service_check_raw(vin, service_check_raw)

            graphql_response = oem_livedata_graphql (
                vin=vin,
                payloads=payloads,
                language=1,
                unit_system=1
            )
            
            rest_response = oem_livedata_rest(
                vin=vin,
                payloads=payloads,
                language=1,
                unit_system=1
            )

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "oemLiveItems.data")

            differences = compare_api_responses(graphql_norm, rest_norm, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_oem_module_name(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")
            type_str = row.get("Type")
            ids_str = row.get("Ids")

            vin_info_response = decode_vin_rest(vin)

            if vin_info_response is None:
                raise ValueError("Invalid VIN decode response from REST API")

            make = vin_info_response.get("make_enum")
            ids = [int(x) for x in ids_str.split(",")]

            graphql_response = oem_module_name_graphql(
                make=make,
                type_str=type_str,
                ids=ids
            )
            
            rest_response = oem_module_name_rest(
                make=make,
                type_str=type_str,
                ids=ids
            )

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "enums.edges")

            differences = compare_api_responses(graphql_norm, rest_norm, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results

def compare_api_option_list(input_file, output_file):
    df_input = read_input_excel(input_file)
    all_results = []

    for idx, row in df_input.iterrows():
        logger.info(f"--- Row {idx + 1}: Processing {row.to_dict()} ---")

        try:
            vin = row.get("VIN")

            graphql_response = option_list_graphql(vin=vin)
            rest_response = option_list_rest(vin=vin)

            rest_norm = rest_response
            graphql_norm = get_object_by_key(graphql_response, "getOptionList.data")

            differences = compare_api_responses(graphql_norm, rest_norm, row_index=idx + 1)

            rowDefault = {
                    "RowIndex": idx + 1,
                    "VIN": vin,
                    "Field": "Responses",
                    "Status": "",
                    "REST": "",
                    "GRAPHQL": "",
                    "Rest Response": rest_norm,
                    "GraphQL Response": graphql_norm
                }

            if not differences:
                rowDefault["Status"] = "Match"
            else:
                rowDefault["Status"] = "Not Match"

            all_results.append(rowDefault)
                
            if differences:
                all_results.extend(differences)

        except Exception as ex:
            logger.error(f"Error in row: {idx + 1}: {ex}")
            all_results.append({
                "RowIndex": "",
                "VIN": "",
                "Field": "",
                "Status": f"ERROR: {ex}",
                "REST": "",
                "GRAPHQL": ""
            })

    df_output = pd.DataFrame(all_results)
    write_output_excel(df_output, output_file)
    return all_results