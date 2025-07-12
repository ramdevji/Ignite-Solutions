from typing import Optional


def parse_comma_separated_list(param_string: Optional[str]) -> list[str]:
    if not param_string:
        return []
    return [item.strip().lower() for item in param_string.split(',') if item.strip()]


def parse_int_list(param_string: Optional[str]) -> list[int]:
    if not param_string:
        return []

    int_list = []
    for item in param_string.split(','):
        try:
            int_list.append(int(item.strip()))
        except ValueError:
            continue
    return int_list
