
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
