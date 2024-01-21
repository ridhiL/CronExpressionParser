import pytest
from parser.utils import get_values_for_incremental_data, get_range_values, get_values_for_multipart_data
from parser.cron_parser import CronFieldParser


@pytest.fixture
def parser():
    return CronFieldParser("minute", "*")


def test_get_increment_values(parser):
    step_parts = ["0", "15"]
    _output = get_values_for_incremental_data(parser, step_parts)
    assert _output == [0, 15, 30, 45]


def test_get_incremental_values_for_invalid_length(parser):
    step_parts = ["1", "2", "4"]
    with pytest.raises(ValueError):
        get_values_for_incremental_data(parser, step_parts)


def test_get_incremental_values_for_invalid_value(parser):
    step_parts = ["1", "24"]
    parser.cron_field_name = "hour"
    with pytest.raises(ValueError):
        get_values_for_incremental_data(parser, step_parts)


def test_get_range_values():
    field_name, range_str = "minute", "1-5"
    _output = get_range_values(field_name, range_str)
    assert _output == [1, 2, 3, 4, 5]


def test_get_range_values_for_non_numerical_range():
    field_name, range_str = "minute", "abc-5"
    with pytest.raises(ValueError):
        get_range_values(field_name, range_str)


def test_get_range_values_for_invalid_range():
    field_name, range_str = "minute", "0-60"
    with pytest.raises(ValueError):
        get_range_values(field_name, range_str)


def test_cron_field_parse_multiple_with_range(parser):
    parser.cron_field_name, parts = "day of week", ["0-3", "5-6"]
    output = get_values_for_multipart_data(parser, parts)
    assert output == [0, 1, 2, 3, 5, 6]


def test_cron_field_parse_multiple_with_increment(parser):
    parts = ["0/15","20"]
    output = sorted(get_values_for_multipart_data(parser, parts))
    assert output == [0, 15, 20, 30, 45]


def test_cron_field_multiple_numerical(parser):
    parts = ["1", "5", "10"]
    output = get_values_for_multipart_data(parser, parts)
    assert output == [1, 5, 10]

