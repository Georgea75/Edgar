import pandas
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError as SerializerValidationError
from rest_framework.request import HttpRequest
from rest_framework.response import Response

from edgar.models import File, Column
from edgar.serializers import (
    FileSerializer,
    ColumnSerializer,
    GetFileSerializer,
    SupportedTypesSerializer,
)
from edgar.conversions import SUPPORTED_TYPES, FUNCTION_LOOKUP
from edgar.infer_data_types import infer_and_convert_data_types


@api_view(["POST"])
def post_sheet(request: HttpRequest) -> Response:
    """
    POST endpoint for uploading a spreadsheet file and processing its data.

    Args:
        request (HttpRequest): The HTTP request object containing the uploaded file.

    Returns:
        Response: A Response object containing the serialized data of the uploaded file,
        along with its associated columns, if successful. Returns an error response with
        appropriate status codes in case of failure.

    Raises:
        pd.errors.ParserError: If there's an error parsing the uploaded file.
        Exception: If an unexpected error occurs during file processing.
    """
    file_object = request.data.get("file")

    if file_object is None:
        return Response(
            {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        dataframe = (
            pandas.read_csv(file_object)
            if file_object.name.endswith(".csv")
            else pandas.read_excel(file_object)
        )

        dataframe = infer_and_convert_data_types(dataframe)

        file_serializer = FileSerializer(
            data={
                "file": file_object,
                "file_name": file_object.name,
                "number_of_records": len(dataframe),
            }
        )

        if file_serializer.is_valid():
            file_instance = file_serializer.save()
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        for column_name, data_type in dataframe.dtypes.items():
            column_serializer = ColumnSerializer(
                data={
                    "file": file_instance.id,
                    "name": column_name,
                    "data_type": data_type.name,
                }
            )
            if column_serializer.is_valid():
                column_serializer.save()
            else:
                return Response(
                    column_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(file_serializer.data, status=status.HTTP_201_CREATED)

    except pandas.errors.ParserError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    except UnicodeDecodeError as e:
        return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_sheet(request: HttpRequest, sheet_id: str) -> Response:
    """
    Retrieve details of a specific spreadsheet file.

    Args:
        request (HttpRequest): The HTTP request object.
        sheet_id (str): The unique identifier of the spreadsheet file.

    Returns:
        Response: A Response object containing serialized data of the requested
        spreadsheet file.

    Raises:
        Http404: If the requested file with the specified sheet_id does not exist
        in the database.
    """

    file_instance = get_object_or_404(File, id=sheet_id)

    start_index = request.query_params.get("start_index", 0)
    num_records = request.query_params.get(
        "num_records", file_instance.number_of_records
    )

    serializer = GetFileSerializer(
        file_instance, context={"start_index": start_index, "num_records": num_records}
    )

    return Response(serializer.data)


@api_view(["GET"])
def get_supported_types(request: HttpRequest) -> Response:
    """
    Retrieves a list of supported types.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A Response object containing serialized data of supported types.

    """
    try:
        serializer = SupportedTypesSerializer({"supported_types": SUPPORTED_TYPES})
        return Response(serializer.data)
    except Exception as e:
        error_message = (
            "Internal server error occurred while retrieving supported types."
        )
        return Response(
            {"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PUT"])
def update_column_type(request: HttpRequest, column_id: int) -> Response:
    """
    Update the data type of a column in a spreadsheet file.

    Args:
        request (HttpRequest): The HTTP request object.
        column_id (int): The Id of the column to update.

    Returns:
        Response: A Response object indicating the result of the column type update.

    Raises:
        SerializerValidationError: If there's an error during serializer validation.
        ValueError: If the provided column type is invalid or if there's an error during conversion.
        Exception: If an unexpected error occurs during the update process.

    """
    try:

        new_type = request.data.get("data_type", None)
        column_instance = get_object_or_404(Column, pk=column_id)
        file_instance = get_object_or_404(File, pk=column_instance.file.id)

        serializer = ColumnSerializer(
            instance=column_instance, data={"data_type": new_type}, partial=True
        )

        serializer.is_valid(raise_exception=True)

        conversion_function = FUNCTION_LOOKUP[new_type]

        if file_instance.file.name.endswith(".csv"):
            dataframe = pandas.read_csv(
                file_instance.file, usecols=[column_instance.name]
            )
        else:
            dataframe = pandas.read_excel(
                file_instance.file, usecols=[column_instance.name]
            )

        conversion_function(dataframe[column_instance.name], force=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    except SerializerValidationError as e:
        return Response(
            {"error": str(e), "column_type": column_instance.data_type},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except ValueError as e:

        column_instance = get_object_or_404(Column, pk=column_id)
        column = ColumnSerializer(instance=column_instance)

        return Response(column.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {
                "error": "Update failed for unknown reasons.",
                "column_type": column_instance.data_type,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
