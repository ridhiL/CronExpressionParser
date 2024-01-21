import sys
from parser.utils import get_range_values, get_values_for_multipart_data, get_values_for_incremental_data
from parser.config import *

sys.tracebacklimit = 0  # to avoid traceback info while raising errors


class CronExpressionParser:
    def __init__(self, cron_expression):
        self.cron_expression = cron_expression
        self.cron_fields = list()
        self.command = ''

    def cron_parse(self):
        # CRON EXPRESSION FORMAT: <minute> <hour> <day-of-month> <month> <day-of-week> <command>
        field_strings = self.cron_expression.split(' ', 5)   # taking 5 as expression contains 6 parts
        self.command = field_strings[-1]
        for idx, field in enumerate(field_strings[:-1]):
            field_name = CRON_FIELD_NAMES[idx]
            cron_field = CronFieldParser(field_name, field)
            cron_field.field_parse()
            self.cron_fields.append(cron_field)
        return self

    def get_cron_output(self):
        table = []
        for field in self.cron_fields:
            value = ' '.join(str(field_value) for field_value in field.values)
            table.append(f"{field.cron_field_name:<14}{value}")

        table.append(f"{'command':<14}{self.command}")

        return "\n".join(table)


class CronFieldParser:
    def __init__(self, cron_field_name, cron_field_val):
        self.cron_field_name = cron_field_name
        self.cron_field_val = cron_field_val
        self.values = list()

    def field_parse(self):
        if self.cron_field_val == ANY_VALUE:
            # Any value case
            return

        elif self.cron_field_val == ALL_VALUE:
            self.values = list(
                range(EXTREME_FIELD_VALUES[self.cron_field_name]["min"],
                      EXTREME_FIELD_VALUES[self.cron_field_name]["max"] + 1)
            )

        elif MULTIPLE_VALUE_SEPARATOR in self.cron_field_val:
            parts = self.cron_field_val.split(MULTIPLE_VALUE_SEPARATOR)
            self.values = get_values_for_multipart_data(self, parts)

        elif RANGE_SEPARATOR in self.cron_field_val:
            self.values = get_range_values(self.cron_field_name, self.cron_field_val)

        elif INCREMENT_SEPARATOR in self.cron_field_val:
            step_parts = self.cron_field_val.split(INCREMENT_SEPARATOR)
            self.values = get_values_for_incremental_data(self, step_parts)

        else:
            if not self.cron_field_val.isdigit():
                raise ValueError(f"Cron field value for '{self.cron_field_name}' is not in numerical format.")
            if (EXTREME_FIELD_VALUES[self.cron_field_name]["min"] > int(self.cron_field_val) or
                    int(self.cron_field_val) > EXTREME_FIELD_VALUES[self.cron_field_name]["max"]):
                raise ValueError(f"Cron field value for '{self.cron_field_name}' field is off limits.")

            self.values = [int(self.cron_field_val)]

        return self
