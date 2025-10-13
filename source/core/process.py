from source.core.api_logic import ( compare_api_ymme, compare_api_vin_profile, compare_api_vehicle_profile,
compare_api_dtcs_definition, compare_api_oem_livedata, compare_api_oem_module_name, compare_api_option_list )

from source.utils.utils import setup_logger
logger = setup_logger()

def process_api(name, input_file, output_file):
    match name:
        case "YMME":
            compare_api_ymme(input_file, output_file)
        case "VIN Profile":
            compare_api_vin_profile(input_file, output_file)
        case "Vehicle Profile":
            compare_api_vehicle_profile(input_file, output_file)
        case "DTCs Definition":
            compare_api_dtcs_definition(input_file, output_file)
        case "OEM LiveData":
            compare_api_oem_livedata(input_file, output_file)
        case "OEM Module Name":
            compare_api_oem_module_name(input_file, output_file)
        case "Option List":
            compare_api_option_list(input_file, output_file)
        case _:
            logger.warning(f"No matching API found for name: {name}")