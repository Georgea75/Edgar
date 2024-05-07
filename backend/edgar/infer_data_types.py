from typing import Generator
from pandas import DataFrame
from edgar.conversions import FUNCTIONS, FUNCTION_LOOKUP


def infer_and_convert_data_types(
    dataframe: DataFrame, supplied_types: dict[str, str] = {}
) -> DataFrame:
    """
    Infer and convert data types of columns in a pandas DataFrame based on supplied types or inferred types.

    Parameters:
    - dataframe (DataFrame): The pandas DataFrame for which data types need to be inferred and converted.
    - supplied_types (Optional[dict[str, str]]): A dictionary containing column names as keys and their
        respective desired data types as values. If provided, these types will be used for conversion.
        Defaults to None.

    Returns:
    - DataFrame: The pandas DataFrame with inferred and converted data types.

    Raises:
    - TypeError: Raises a type error if the data type is not supported.


    """
    for column_name in dataframe.columns:
        if column_name in supplied_types.keys():
            try:
                type_name = supplied_types[column_name]
                conversion_function = FUNCTION_LOOKUP[type_name]
                dataframe[column_name] = conversion_function(
                    dataframe[column_name], force=True
                )

            except AttributeError as e:
                raise TypeError(
                    f"Invalid type conversion: '{type_name}' is not a supported data type."
                )
        elif any(apply_type_checkers(dataframe, column_name)):
            continue

    return dataframe


def apply_type_checkers(
    dataframe: DataFrame, column_name: str
) -> Generator[bool, None, None]:
    """
    A generator function that applies type checkers on a DataFrame series to infer its type.

    Parameters:
    - dataframe (DataFrame): The pandas DataFrame to apply data checks on.
    - column_name (str): The name of the column in the DataFrame to perform data checks on.

    Yields:
    - bool: A boolean value indicating whether the data checks were successfully applied (`True`)
        or not (`False`) for each conversion function.

    Notes:
        This generator iterates through a list of conversion functions, attempting to apply each one to
        the specified column of the DataFrame. If a conversion is successful, it yields `True` and stops
        further iterations. If none of the conversion functions are successful, it yields `False`.
    """
    for conversion in FUNCTIONS:
        try:
            dataframe[column_name] = conversion[1](dataframe[column_name])
            yield True

        except Exception as e:
            continue
    yield False
