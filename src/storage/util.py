
def get_operator(value: str) -> str:
    operators = ["<", ">", "<=", ">=", "="]

    for op in operators:
        if op in value:
            return op

    raise ValueError("No operator ['=', '<', '>', '<=', '>='] has been passed!")


def split_op_value_into_strings(value: str):
    operator = get_operator(value)
    key, value = value.split(operator)
    return key, value, operator


def split_range_value_into_strings(value: str):
    range_a, range_b = value.split('-')
    return int(range_a), int(range_b)


def json_digit_string_keys_to_ints(json_data: dict) -> dict:
    """Turn any numeral string keys ("1", "2" etc.) into actual Python integers"""
    for key in list(json_data.keys()):
        if isinstance(json_data[key], dict):
            json_data[key] = {int(k) if k.isdigit() else k: v for k, v in json_data[key].items()}

    return json_data
