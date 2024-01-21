import sys
from parser.config import *

sys.tracebacklimit = 0  # to avoid traceback info while raising errors


def get_values_for_multipart_data(field, parts):
    values = []
    for part in parts:
        if INCREMENT_SEPARATOR in part:
            step_parts = part.split(INCREMENT_SEPARATOR)
            values.extend(get_values_for_incremental_data(field, step_parts))
        elif RANGE_SEPARATOR in part:
            _values = get_range_values(field.cron_field_name, part)
            values.extend(_values)
        else:
            values.append(int(part))
    return values


def get_values_for_incremental_data(field, step_parts):
    if len(step_parts) != 2:
        raise ValueError(f"Invalid cron field value for '{field.cron_field_name}': {field.cron_field_val}")
    if step_parts[0] == ALL_VALUE:
        _min, step = EXTREME_FIELD_VALUES[field.cron_field_name]["min"], int(step_parts[1])
    else:
        if not step_parts[0].isdigit() or not step_parts[1].isdigit():
            # for invalid value provided for increment start
            raise ValueError(f"Invalid cron field value for '{field.cron_field_name}': {field.cron_field_val}")
        _min, step = map(int, step_parts)
    if int(step_parts[1]) > EXTREME_FIELD_VALUES[field.cron_field_name]["max"]:
        raise ValueError(f"Cron field value for '{field.cron_field_name}' is off limits.")
    _values = []
    field_max = EXTREME_FIELD_VALUES[field.cron_field_name]["max"]
    for value in range(_min, field_max + 1, step):
        if (value - _min) % step == 0:
            _values.append(value)
    return _values


def get_range_values(field_name, range_str):
    start, end = range_str.split("-")
    if not start.isdigit() or not end.isdigit():
        raise ValueError(f"Incorrect field range given for '{field_name}' field.")
    if int(start) < EXTREME_FIELD_VALUES[field_name]["min"] or int(end) > EXTREME_FIELD_VALUES[field_name]["max"]:
        raise ValueError(f"Invalid Range provided for '{field_name}' field.")
    return list(range(int(start), int(end) + 1))

