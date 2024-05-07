from django.test import TestCase
from rest_framework.exceptions import ValidationError
from edgar.models import File
from django.utils import timezone
from edgar.serializers import (
    ColumnSerializer,
    FileSerializer,
    SupportedTypesSerializer,
)
from pathlib import Path
from django.core.files.base import ContentFile


class ColumnSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.file = File.objects.create(
            file="/test_data.csv",
            file_name="test_data",
            number_of_records=3,
            uploaded_at=timezone.now(),
        )

    def test_valid_data_type(self) -> None:
        """
        Test whether a valid data type passes validation.
        """
        serializer = ColumnSerializer(
            data={
                "data_type": "int8",
                "file": self.file.pk,
                "name": self.file.file_name,
            }
        )

        self.assertTrue(serializer.is_valid())

    def test_invalid_data_type(self) -> None:
        """
        Test whether an invalid data type raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            serializer = ColumnSerializer(
                data={
                    "data_type": "INVALID",
                    "file": self.file.pk,
                    "name": self.file.file_name,
                }
            )
            serializer.is_valid(raise_exception=True)


class FileSerializerTestCase(TestCase):
    def test_file_serializer(self) -> None:
        """
        Test whether the FileSerializer serializes data properly.
        """

        file_path = Path(__file__).resolve().parent / "test_files" / "test_data.csv"

        with open(file_path, "rb") as file:
            file_object = ContentFile(file.read(), name=file_path.name)
            serializer = FileSerializer(
                data={
                    "file": file_object,
                    "file_name": file_object.name,
                    "number_of_records": 3,
                }
            )
            self.assertTrue(serializer.is_valid(raise_exception=True))


class SupportedTypesSerializerTestCase(TestCase):
    def test_supported_types_serializer(self) -> None:
        """
        Test whether the SupportedTypesSerializer serializes data properly.
        """
        serializer = SupportedTypesSerializer(
            data={"supported_types": ["int8", "object"]}
        )
        self.assertTrue(serializer.is_valid())
