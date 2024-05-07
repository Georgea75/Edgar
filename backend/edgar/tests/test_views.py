from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from pathlib import Path
from parameterized import parameterized
from edgar.conversions import SUPPORTED_TYPES
from edgar.models import File, Column

TEST_FILE_DIRECTORY = Path(__file__).resolve().parent / "test_files"


class TestViews(TestCase):
    """
    A test suite for the Views
    """

    def setUp(self) -> None:
        """
        Set up necessary objects for tests.
        """
        self.client: Client = Client()
        file_instance: File = File.objects.create(
            file=str(TEST_FILE_DIRECTORY) + "/test_data.csv",
            file_name="test_data",
            number_of_records=3,
            uploaded_at=timezone.now(),
        )
        Column.objects.create(file=file_instance, name="Foo", data_type="int8")
        Column.objects.create(file=file_instance, name="Bar", data_type="object")

    @parameterized.expand(
        [
            (Path(TEST_FILE_DIRECTORY / "test_format_csv.csv"),),
            (Path(TEST_FILE_DIRECTORY / "test_format_excel.xlsx"),),
        ]
    )
    def test_post_sheet(self, filepath: Path) -> None:
        """
        Test the post_sheet view with supported file formats (csv and xlsx).

        """
        with open(filepath, "rb") as file:
            response = self.client.post(reverse("sheet-post"), {"file": file})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_sheet(self) -> None:
        """
        This test function simulates requesting a sheet using the get_sheet view and verifies
        that the response status code is HTTP 200 OK.

        """
        response = self.client.get(reverse("sheet-get", kwargs={"sheet_id": "1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_supported_types(self) -> None:
        """
        This test function simulates requesting supported data types using the supported-data-types view
        and verifies that the response status code is HTTP 200 OK and the returned types match the expected ones.

        """
        response = self.client.get(reverse("supported-data-types"))
        returned_types: list[str] = response.json()["supported_types"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(returned_types, SUPPORTED_TYPES)
