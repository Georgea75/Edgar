import pandas as pd
from edgar.infer_data_types import infer_and_convert_data_types
from django.test import TestCase
from typing import Dict
import unittest


class TestInferAndConvertDataTypes(TestCase):
    """
    Test cases for the infer_and_convert_data_types function.
    """

    def setUp(self) -> None:
        """
        Set up test data.
        """
        self.dataframe: pd.DataFrame = pd.DataFrame(
            {
                "int8": [12, 1, 2, 34, 12, 2, 9],
                "boolean": ["0", "1", 0, 1, "0", "1", "0"],
                "int16": [1209, "11", "0", "12", "12", "45", "95"],
                "category": ["foo", "bar", "baz", "bar", "baz", "foo", "foo"],
            }
        )

    def test_all_forced_convert(self) -> None:
        """
        Test all columns forced conversion.
        """
        conversion: Dict[str, str] = {
            "int8": "int32",
            "boolean": "object",
            "int16": "int64",
            "category": "object",
        }

        result: pd.DataFrame = infer_and_convert_data_types(self.dataframe, conversion)

        self.assertEqual(result.dtypes["int8"], "int32")
        self.assertEqual(result.dtypes["boolean"], "object")
        self.assertEqual(result.dtypes["int16"], "int64")
        self.assertEqual(result.dtypes["category"], "object")

    def test_invalid_type_force(self) -> None:
        """
        Test invalid type conversion.
        """
        conversion: Dict[str, str] = {"category": "foo"}
        with self.assertRaises(KeyError):
            result: pd.DataFrame = infer_and_convert_data_types(
                self.dataframe, conversion
            )

    def test_failed_forced_convert(self) -> None:
        """
        Test failed forced conversion.
        """
        conversion: Dict[str, str] = {"category": "int8"}
        with self.assertRaises(ValueError):
            result: pd.DataFrame = infer_and_convert_data_types(
                self.dataframe, conversion
            )

    def test_all_automatic_convert(self) -> None:
        """
        Test all columns automatic conversion.
        """
        result: pd.DataFrame = infer_and_convert_data_types(self.dataframe)

        self.assertEqual(result.dtypes["int8"], "int8")
        self.assertEqual(result.dtypes["boolean"], "bool")
        self.assertEqual(result.dtypes["int16"], "int16")
        self.assertEqual(result.dtypes["category"], "category")

    def test_mixed_forced_automatic_convert(self) -> None:
        """
        Test if a mix of forced and automatic conversion works within the same conversion.
        """
        conversion: Dict[str, str] = {"boolean": "int8"}
        result: pd.DataFrame = infer_and_convert_data_types(self.dataframe, conversion)

        self.assertEqual(result.dtypes["int8"], "int8")
        self.assertEqual(result.dtypes["boolean"], "int8")
        self.assertEqual(result.dtypes["int16"], "int16")
        self.assertEqual(result.dtypes["category"], "category")


if __name__ == "__main__":
    unittest.main()
