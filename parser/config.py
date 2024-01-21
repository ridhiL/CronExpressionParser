ALL_VALUE = '*'
ANY_VALUE = '?'
MULTIPLE_VALUE_SEPARATOR = ','
RANGE_SEPARATOR = '-'
INCREMENT_SEPARATOR = '/'
CRON_FIELD_NAMES = ["minute", "hour", "day of month", "month", "day of week"]
EXTREME_FIELD_VALUES = {
    "minute": {
        "min": 0,
        "max": 59
    },
    "hour": {
        "min": 0,
        "max": 23
    },
    "day of month": {
        "min": 1,
        "max": 31
    },
    "month": {
        "min": 1,
        "max": 12
    },
    "day of week": {
        "min": 0,
        "max": 6
    }
}