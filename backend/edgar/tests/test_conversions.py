from django.test import TestCase
from pandas import Series
import pandas
from edgar.conversions import FUNCTION_LOOKUP
from parameterized import parameterized
from pandas.testing import assert_series_equal
import unittest

invalid_conversion_cases = [
    (
        "datetime64[ns]",
        Series(["2024-03-19T01:30:54Z", "19/03/2024 12:30:45"]),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T01:30:54Z", "Foo", 1]),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T01:30:54Z", "2022-12-19T12:12:45Z", 1]),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T01:30:54Z", "2022-14-19T12:12:45Z"]),
    ),
    ("int16", Series(["32768", "-32769"])),
    (
        "int32",
        Series(["2147483648", "-2147483649"]),
    ),
    (
        "int64",
        Series(["9223372036854775808", "-9223372036854775809"]),
    ),
    (
        "float32",
        Series(["1.5", "text", None]),
    ),
    (
        "float64",
        Series(["1.5", "text", None]),
    ),
    (
        "complex128",
        Series(["1.5+2j", "text", None]),
    ),
    (
        "timedelta64[ns]",
        Series(["1:00:00", "text", None]),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19", "text", None]),
    ),
    (
        "category",
        Series(["a", "b", "c"]),
    ),
    (
        "bool",
        Series(["foo", "false", "True", "False", 1, 0]),
    ),
    (
        "bool",
        Series(["Foo", "Alice", "Boo"]),
    ),
    (
        "bool",
        Series([10, 100, 1000]),
    ),
    (
        "bool",
        Series([0, 1, 1000]),
    ),
]

valid_conversion_test_cases = [
    (
        "int8",
        Series(["0", "127", "-127"]),
        Series([0, 127, -127], dtype="int8"),
    ),
    (
        "int8",
        Series(["127", "-127"]),
        Series([127, -127], dtype="int8"),
    ),
    (
        "int16",
        Series(["0", "32767", "-32768"]),
        Series([0, 32767, -32768], dtype="int16"),
    ),
    (
        "int32",
        Series(["0", "2147483647", "-2147483648"]),
        Series([0, 2147483647, -2147483648], dtype="int32"),
    ),
    (
        "int64",
        Series(["0", "9223372036854775807", "-9223372036854775808"]),
        Series([0, 9223372036854775807, -9223372036854775808], dtype="int64"),
    ),
    (
        "float32",
        Series(["1.5", "2.5", "3.5"]),
        Series([1.5, 2.5, 3.5], dtype="float32"),
    ),
    (
        "float64",
        Series(["1.5", "2.5", "3.5"]),
        Series([1.5, 2.5, 3.5], dtype="float64"),
    ),
    (
        "complex128",
        Series(["1.5+2j", "3.5-4j", "5+6j"]),
        Series(
            [complex("1.5+2j"), complex("3.5-4j"), complex("5+6j")], dtype="complex128"
        ),
    ),
    (
        "timedelta64[ns]",
        Series(["1 days", "2 days", "3 days"]),
        Series(
            [
                pandas.to_timedelta("1 day"),
                pandas.to_timedelta("2 day"),
                pandas.to_timedelta("3 day"),
            ],
            dtype="timedelta64[ns]",
        ),
    ),
    (
        "timedelta64[ns]",
        Series(["3 days, 5:30:10", None]),
        Series([pandas.to_timedelta("3 days, 5:30:10"), None], dtype="timedelta64[ns]"),
    ),
    (
        "timedelta64[ns]",
        Series(["1:15:30"]),
        Series([pandas.to_timedelta("1:15:30")], dtype="timedelta64[ns]"),
    ),
    (
        "timedelta64[ns]",
        Series(["1D", None]),
        Series([pandas.to_timedelta("1D"), None], dtype="timedelta64[ns]"),
    ),
    (
        "timedelta64[ns]",
        Series(["1h30min"]),
        Series([pandas.to_timedelta("1h30min")], dtype="timedelta64[ns]"),
    ),
    (
        "timedelta64[ns]",
        Series(["1h30min", "1D", None, "3"]),
        Series(
            [
                pandas.to_timedelta("1h30min"),
                pandas.to_timedelta("1D"),
                None,
                pandas.to_timedelta("3"),
            ],
            dtype="timedelta64[ns]",
        ),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19", "2024-03-20", "2024-03-21"]),
        Series(
            [
                pandas.to_datetime("2024-03-19"),
                pandas.to_datetime("2024-03-20"),
                pandas.to_datetime("2024-03-21"),
            ]
        ),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T01:30:54Z", "2022-12-19T12:12:45Z", None]),
        Series(
            [
                pandas.to_datetime("2024-03-19T01:30:54Z"),
                pandas.to_datetime("2022-12-19T12:12:45Z"),
                None,
            ],
        ),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T12:30:45+03:00", "2021-06-19T14:30:45+03:00"]),
        Series(
            [
                pandas.to_datetime("2024-03-19T12:30:45+03:00"),
                pandas.to_datetime("2021-06-19T14:30:45+03:00"),
            ],
        ),
    ),
    (
        "datetime64[ns]",
        Series(["2024-03-19T12:30:45", "2022-12-19T12:12:45"]),
        Series(
            [
                pandas.to_datetime("2024-03-19T12:30:45"),
                pandas.to_datetime("2022-12-19T12:12:45"),
            ],
        ),
    ),
    (
        "datetime64[ns]",
        Series(["Mar 19 2024 12:30:45", "Mar 19 2014 12:35:45"]),
        Series(
            [
                pandas.to_datetime("Mar 19 2024 12:30:45"),
                pandas.to_datetime("Mar 19 2014 12:35:45"),
            ],
        ),
    ),
    (
        "datetime64[ns]",
        Series(["19/03/2024 12:30:45", "15/02/2021 11:32:15"]),
        Series(
            [
                pandas.to_datetime("19/03/2024 12:30:45"),
                pandas.to_datetime("15/02/2021 11:32:15"),
            ],
        ),
    ),
    (
        "object",
        Series(["text", "123", "2024-03-19"]),
        Series(["text", "123", "2024-03-19"], dtype="object"),
    ),
    (
        "category",
        Series(["ab", "bb", "bb", "bb"]),
        Series(["ab", "bb", "bb", "bb"], dtype="category"),
    ),
    (
        "bool",
        Series([True, False, True]),
        Series([True, False, True], dtype="bool"),
    ),
    ("bool", Series([True, False]), Series([True, False], dtype="bool")),
    (
        "bool",
        Series([True, False, None]),
        Series([True, False, None], dtype="bool"),
    ),
    (
        "bool",
        Series(["true", "false"]),
        Series([True, False], dtype="bool"),
    ),
    (
        "bool",
        Series(["TRUE", "FALSE"]),
        Series([True, False], dtype="bool"),
    ),
    (
        "bool",
        Series([1, 0]),
        Series([True, False], dtype="bool"),
    ),
    (
        "bool",
        Series(["true", "false"]),
        Series([True, False], dtype="bool"),
    ),
    ("bool", Series(["yes", "no"]), Series([True, False], dtype="bool")),
    ("bool", Series(["on", "off"]), Series([True, False], dtype="bool")),
    ("bool", Series(["T", "F"]), Series([True, False], dtype="bool")),
    (
        "bool",
        Series(["true", "false", "T", "F", 0, 1, True, False]),
        Series([True, False, True, False, False, True, True, False], dtype="bool"),
    ),
]


class TestConversionFunctions(TestCase):
    """
    A test suite for conversion functions.
    """

    @parameterized.expand(invalid_conversion_cases)
    def test_invalid_conversions(self, conversion_to_test, series):
        """
        Tests invalid conversions.

        Parameters:
            conversion_to_test (str): The type of conversion to test.
            series (Series): The input series to be converted.

        """
        conversion = FUNCTION_LOOKUP[conversion_to_test]
        with self.assertRaises(ValueError):
            conversion(series)

    @parameterized.expand(valid_conversion_test_cases)
    def test_valid_conversions(self, conversion_to_test, series, expected_output):
        """
        Tests valid conversions.

        Parameters:
            conversion_to_test (str): The type of conversion to test.
            series (Series): The input series to be converted.
            expected_output (Series): The expected output series after conversion.

        """
        conversion = FUNCTION_LOOKUP[conversion_to_test]
        result = conversion(series)

        self.assertIsInstance(result, Series)
        assert_series_equal(result, expected_output)


if __name__ == "__main__":
    unittest.main()
