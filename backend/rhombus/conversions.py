from typing import Callable
from re import compile

import pandas
from pandas import Series

"""
Functions for coercing types in a pandas DataFrame.

These functions provide utilities to coerce the types of columns in a pandas DataFrame
to specific types such as numeric, datetime, or categorical.

To add a conversion function, it needs to be registered using the decorators provided in this module.
Any registered conversion function should either raise an exception if the conversion fails or
successfully convert the pandas Series.
"""

FUNCTIONS = []
FUNCTION_LOOKUP = {}
SUPPORTED_TYPES = []

ALLOWED_NONE_TYPES = [
    "nan",
    "na",
    "n/a",
    "none",
    "null",
    "missing",
    "miss",
    "unknow",
    "unk",
    "-999",
    "not available",
]


def register_conversion(order: int, type_name: str) -> Callable:
    """
    Register a conversion function.

    Parameters:
    - order: The order in which the function should be registered.
    - type_name: The type that the converter is being registered for.

    Returns:
    - decorator: The actual decorator function.
    """

    def decorator(func: Callable) -> Callable:
        """
        Decorator function to register a conversion function.

        Parameters:
        - func: The conversion function to register.

        Returns:
        - func: The registered conversion function.
        """
        FUNCTIONS.append((order, func))
        FUNCTION_LOOKUP[type_name] = func
        SUPPORTED_TYPES.append(type_name)
        FUNCTIONS.sort(key=lambda x: x[0])
        return func

    return decorator


def parse_supported_none_values(series: Series) -> Series:
    """
    Parses a pandas Series to replace specific string representations with None.

    Parameters:
    - series (pandas.Series): The pandas Series to parse.

    Returns:
    - pandas.Series: A new pandas Series with values replaced by None where applicable.

    """
    return Series(
        [
            None if str(value).lower() in ALLOWED_NONE_TYPES else value
            for value in series
        ]
    )


@register_conversion(order=0, type_name="bool")
def bool(column: Series, force: bool = False) -> Series:
    """
    Convert a column to boolean type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to boolean.
    """
    bool_variable_map = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
        "yes": True,
        "no": False,
        "t": True,
        "f": False,
        "on": True,
        "off": False,
        "none": None,
    }

    try:
        column = parse_supported_none_values(column)
        return Series(
            [bool_variable_map[str(val).lower()] for val in column], dtype="bool"
        )
    except KeyError as e:
        raise ValueError(f"Unable to convert column '{column.name}' to bool: {e}")


@register_conversion(order=1, type_name="category")
def category(column: Series, force: bool = False, threshold: float = 0.5) -> Series:
    """
    Convert a column to categorical type if the uniqueness ratio is less than a specified threshold.

    Parameters:
    - column (pandas.Series): The column to convert.
    - threshold (float): The uniqueness ratio threshold for conversion. Default is 0.5.

    Returns:
    - pandas.Categorical: The converted column if the uniqueness ratio is less than the threshold,
                          otherwise returns the original column.

    Raises:
    - ValueError: If unable to convert any value to categorical.
    """
    if force:
        unique_ratio = 0.0
    else:
        unique_ratio = len(column.unique()) / len(column)

    if unique_ratio <= threshold:
        column = parse_supported_none_values(column)
        return Series(column, dtype="category")
    else:
        raise ValueError(f"Unable to convert column '{column.name}' to categorical")


@register_conversion(order=2, type_name="int8")
def int8(column: Series, force: bool = False) -> Series:
    """
    Convert a column to int8 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to int8.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("int8", errors="raise")
        if not force:
            if (
                not column.values.astype(int).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to int8 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to int8: {e}")


@register_conversion(order=3, type_name="int16")
def int16(column: Series, force: bool = False) -> Series:
    """
    Convert a column to int16 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to int16.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("int16", errors="raise")

        if not force:
            if (
                not column.values.astype(int).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to int16 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to int16: {e}")


@register_conversion(order=4, type_name="int32")
def int32(column: Series, force: bool = False) -> Series:
    """
    Convert a column to int32 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to int32.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("int32", errors="raise")
        if not force:
            if (
                not column.values.astype(int).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to int32 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to int32: {e}")


@register_conversion(order=5, type_name="int64")
def int64(column: Series, force: bool = False) -> Series:
    """
    Convert a column to int64 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to int64.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("int64", errors="raise")
        if not force:
            if (
                not column.values.astype(int).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to int64 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to int64: {e}")


@register_conversion(order=6, type_name="float32")
def float32(column: Series, force: bool = False) -> Series:
    """
    Convert a column to float32 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to float32.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("float32", errors="raise")
        if not force:
            if (
                not column.values.astype(float).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to float32 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to float32: {e}")


@register_conversion(order=7, type_name="float64")
def float64(column: Series, force: bool = False) -> Series:
    """
    Convert a column to float64 type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to float64.
    """
    try:
        column = parse_supported_none_values(column)
        converted_column = column.astype("float64", errors="raise")
        if not force:
            if (
                not column.values.astype(float).tolist()
                == converted_column.values.tolist()
            ):
                raise ValueError("Conversion to float64 resulted in different values.")

        return converted_column

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to float64: {e}")


@register_conversion(order=8, type_name="complex128")
def complex128(column: Series, force: bool = False) -> Series:
    """
    Convert a column to complex numbers.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to complex number.
    """

    pattern = compile(r"^\s*([-+]?\d*\.?\d+)\s*([-+])\s*([-+]?\d*\.?\d*)j?\s*$")

    def function_complex(x):
        if x is None:
            return None
        elif pattern.match(str(x)):
            return complex(x)
        else:
            raise ValueError(f"Invalid value: {x}")

    try:
        column = parse_supported_none_values(column)
        return Series([function_complex(x) for x in column], dtype=complex)

    except Exception as e:
        raise ValueError(
            f"Unable to convert column '{column.name}' to complex numbers: {e}"
        )


@register_conversion(order=9, type_name="timedelta64[ns]")
def timedelta(column: Series, force: bool = False) -> Series:
    """
    Convert a column to timedelta type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to timedelta.
    """

    try:
        return pandas.to_timedelta(column)

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to timedelta: {e}")


@register_conversion(order=10, type_name="datetime64[ns]")
def datetime(column: Series, force: bool = False) -> Series:
    """
    Convert a column to datetime type.

    Parameters:
    - column (pandas.Series): The column to convert.

    Returns:
    - pandas.Series: The converted column.

    Raises:
    - ValueError: If unable to convert any value to datetime.
    """

    try:
        return pandas.to_datetime(column)

    except Exception as e:
        raise ValueError(f"Unable to convert column '{column.name}' to datetime: {e}")


@register_conversion(order=11, type_name="object")
def object(column: Series, force: bool = False) -> Series:
    """
    Convert the values in the column to object type.

    Parameters:
        column (pandas.Series): The column to be converted.

    Returns:
        pandas.Series: The converted column.

    Raises:
        ValueError: If the conversion fails.
    """
    try:
        column = parse_supported_none_values(column)
        return column.astype("object")
    except Exception:
        raise ValueError("Conversion to object type failed.")
