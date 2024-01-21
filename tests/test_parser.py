import pytest
from parser.cron_parser import CronExpressionParser, CronFieldParser


cron_expression = "*/15 0 1,15 * 1-5 /usr/bin/find"
cron_output = """minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find"""


class TestCronExpressionParser():
    @pytest.fixture
    def parser(self):
        return CronExpressionParser(cron_expression)

    def test_cron_parse(self, parser):
        parser.cron_parse()
        assert len(parser.cron_fields) == 5

    def test_get_cron_output(self, parser):
        parser.cron_parse()
        output = parser.get_cron_output()
        assert output == cron_output


class TestCronFieldParser:
    @pytest.fixture
    def parser(self):
        return CronFieldParser("minute", "*")

    def test_cron_field_parse_any_val(self, parser):
        parser.cron_field_val = "?"
        parser.field_parse()
        assert parser.values == []

    def test_cron_field_parse_all_val(self, parser):
        parser.cron_field_name = "month"
        parser.field_parse()
        assert parser.values == list(range(1, 13))

    def test_cron_field_parse_multiple_val(self, parser):
        parser.cron_field_name, parser.cron_field_val = "hour", "1,3,5"
        parser.field_parse()
        assert parser.values == [1, 3, 5]

    def test_cron_field_parse_range(self, parser):
        parser.cron_field_name, parser.cron_field_val = "hour", "9-11"
        parser.field_parse()
        assert parser.values == [9, 10, 11]

    def test_cron_field_parse_increment(self, parser):
        parser.cron_field_name, parser.cron_field_val = "minute", "*/10"
        parser.field_parse()
        assert parser.values == [0, 10, 20, 30, 40, 50]

    def test_cron_field_numerical_off_limit(self, parser):
        parser.cron_field_val = "60"
        with pytest.raises(ValueError):
            parser.field_parse()

    def test_cron_field_non_numerical(self, parser):
        parser.cron_field_val = "abc"
        with pytest.raises(ValueError):
            parser.field_parse()

    def test_cron_field_numerical_valid(self, parser):
        parser.cron_field_val = "6"
        parser.field_parse()
        assert parser.values == [6]