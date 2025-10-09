import base64

def build_oem_module_raw_data(vin_profile_raw: str, oem_module_raws: list) -> str:
    def string_to_byte_array(hex_str: str) -> bytes:
        return bytes.fromhex(hex_str)
    
    def convert_int_to_bytes(length: int) -> bytes:
        return length.to_bytes(2, byteorder='big')[::-1]

    def convert_long_to_bytes(length: int) -> bytes:
        return length.to_bytes(4, byteorder='big')[::-1]
    
    def append_buffer_segment(module: int, segment_type: int, raw_bytes: bytes, data_buffer: bytearray):
        if raw_bytes is None:
            return
        segment = bytearray()
        segment.append(module)
        segment.extend(convert_int_to_bytes(segment_type))
        segment.extend(convert_long_to_bytes(len(raw_bytes)))
        segment.extend(raw_bytes)
        data_buffer.extend(segment)
    
    vin_bytes = string_to_byte_array(vin_profile_raw)
    
    oem_bytes = bytearray()
    oem_bytes.append(len(oem_module_raws))
    for oem_hex in oem_module_raws:
        oem_bytes.extend(string_to_byte_array(oem_hex))
    
    final_buffer = bytearray()
    append_buffer_segment(0, 1, vin_bytes, final_buffer)
    append_buffer_segment(0, 8, oem_bytes, final_buffer)
    
    return base64.b64encode(final_buffer).decode()

oemModuleRawData = build_oem_module_raw_data(vinProfileRaw, oemModuleRaws)
