from django.test import TestCase
from django.core.exceptions import ValidationError
from edgar.models import File, Column


class FileModelTestCase(TestCase):
    def test_file_creation(self):
        """
        Test whether a File object can be created successfully.
        """
        file_obj = File.objects.create(
            file="example.csv", file_name="example", number_of_records=10
        )
        self.assertIsNotNone(file_obj)
        self.assertEqual(file_obj.file, "example.csv")
        self.assertEqual(file_obj.file_name, "example")
        self.assertEqual(file_obj.number_of_records, 10)


class ColumnModelTestCase(TestCase):
    def setUp(self):
        """
        Create a File object to associate with Column objects.
        """
        self.file_obj = File.objects.create(
            file="example.csv", file_name="example", number_of_records=10
        )

    def test_column_creation(self):
        """
        Test whether a Column object can be created successfully.
        """
        column_obj = Column.objects.create(
            file=self.file_obj, name="Column1", data_type="int8"
        )
        self.assertIsNotNone(column_obj)
        self.assertEqual(column_obj.file, self.file_obj)
        self.assertEqual(column_obj.name, "Column1")
        self.assertEqual(column_obj.data_type, "int8")

    def test_invalid_data_type(self):
        """
        Test whether trying to create a Column object with an invalid data type raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            Column.objects.create(
                file=self.file_obj, name="InvalidColumn", data_type="invalid_type"
            )

    def test_unique_column_name_per_file(self):
        """
        Test whether trying to create a Column object with a duplicate name for the same File raises a ValidationError.
        """
        Column.objects.create(
            file=self.file_obj, name="UniqueColumn", data_type="object"
        )

        with self.assertRaises(ValidationError):
            Column.objects.create(
                file=self.file_obj, name="UniqueColumn", data_type="int8"
            )
