import base64
import struct

def string_to_byte_array(hex_string: str):
    return bytes.fromhex(hex_string)

def decode_service_check_data(payload_data_bytes: bytes):
    num_offset = 0
    number_of_item = payload_data_bytes[num_offset]
    num_offset += 1

    items = []
    for _ in range(number_of_item):
        # eOfmItem: 2 bytes (Int16)
        e_ofm_item_bytes = payload_data_bytes[num_offset:num_offset+2]
        num_offset += 2

        # sItemId: 2 bytes (Int16)
        item_id_bytes = payload_data_bytes[num_offset:num_offset+2]
        item_id = struct.unpack("<h", item_id_bytes)[0]
        num_offset += 2

        # fItemValue: 8 bytes
        item_value_bytes = payload_data_bytes[num_offset:num_offset+8]
        num_offset += 8

        # blItemSup: 1 byte
        item_sup = payload_data_bytes[num_offset]
        num_offset += 1

        items.append({
            "EOfmItemData": e_ofm_item_bytes,
            "ItemId": item_id,
            "ItemIdData": item_id_bytes,
            "ItemValue": item_value_bytes,
            "ItemSup": item_sup
        })

    return items

def get_payloads_by_service_check_raw(vin: str, service_check_raw: str):
    payload_bytes = string_to_byte_array(service_check_raw)
    items = decode_service_check_data(payload_bytes)

    payloads = []
    for item in items:
        combined = item["ItemIdData"] + item["ItemValue"]
        payloads.append(base64.b64encode(combined).decode("ascii"))

    return payloads