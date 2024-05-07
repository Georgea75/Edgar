import pandas
from rest_framework import serializers
from edgar.conversions import SUPPORTED_TYPES
from edgar.models import File, Column
from edgar.infer_data_types import infer_and_convert_data_types


class ColumnSerializer(serializers.ModelSerializer):
    """
    Serializer for the Column Model
    """

    class Meta:
        model = Column
        fields = [
            "id",
            "file",
            "name",
            "data_type",
        ]

    def validate_data_type(self, value: str) -> str:
        """
        Validates the data type against the list of supported types.

        Args:
            value (str): The data type to validate.

        Returns:
            str: The validated data type.

        Raises:
            serializers.ValidationError: If the data type is not supported.
        """
        if value not in SUPPORTED_TYPES:
            raise serializers.ValidationError(
                f"{value} is not a supported data type. Please select from {SUPPORTED_TYPES}"
            )
        return value


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for the File model.
    """

    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "file",
            "file_name",
            "number_of_records",
            "uploaded_at",
            "columns",
        ]
        read_only_fields = ["uploaded_at"]


class GetFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the File model used for retrieving data.
    """

    columns = ColumnSerializer(many=True, read_only=True)
    rows = serializers.ListField(child=serializers.DictField(), read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "file",
            "file_name",
            "number_of_records",
            "uploaded_at",
            "columns",
            "rows",
        ]
        read_only_fields = ["uploaded_at"]

    def to_representation(self, instance: File) -> dict[str, any]:
        """
        Custom representation method to include rows data.

        Args:
            instance (File): The File instance to serialize.

        Returns:
            dict[str, Any]: Serialized representation of the File instance.
        """
        start_index = int(self.context.get("start_index", 0)) + 1
        num_records = int(self.context.get("num_records", None))

        data = super().to_representation(instance)
        columns_data = data.get("columns", [])

        if instance.file.name.endswith(".csv"):
            dataframe = pandas.read_csv(
                instance.file,
                nrows=num_records,
                skiprows=start_index,
                names=[col["name"] for col in columns_data],
            )
        else:
            dataframe = pandas.read_excel(
                instance.file,
                nrows=num_records,
                skiprows=start_index,
                names=[col["name"] for col in columns_data],
            )

        dataframe = infer_and_convert_data_types(
            dataframe,
            {col["name"]: col["data_type"] for col in columns_data},
        )

        dataframe = dataframe.where(dataframe.notnull())
        # Convert all values to string for ease of serialization the recast is done to prove the functionaility
        dataframe = dataframe.astype(str)
        data["rows"] = dataframe.to_dict(orient="records")

        return data


class SupportedTypesSerializer(serializers.Serializer):
    """
    Serializer for listing supported data types.
    """

    supported_types = serializers.ListField(child=serializers.CharField())
