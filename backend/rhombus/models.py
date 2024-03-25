from django.core.exceptions import ValidationError
from django.db import models
from rhombus.conversions import SUPPORTED_TYPES


class File(models.Model):
    """
    Model to store information about uploaded files.
    """

    file = models.FileField(upload_to="uploads/")
    file_name = models.CharField(max_length=255)
    number_of_records = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)


def validate_data_type(value: str) -> None:
    """
    Validates whether the provided data type is supported.

    Args:
        value (str): The data type to validate.

    Raises:
        ValidationError: If the data type is not supported.
    """
    if value not in SUPPORTED_TYPES:
        raise ValidationError(
            f"{value} is not a supported data type. Please select from {SUPPORTED_TYPES}"
        )


class Column(models.Model):
    """
    Model to represent columns associated with files.
    """

    file = models.ForeignKey(File, related_name="columns", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50)

    class Meta:
        unique_together = ("file", "name")

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure data_type validation and uniqueness check.
        """
        validate_data_type(self.data_type)
        existing_columns = Column.objects.filter(file=self.file, name=self.name)
        if self.pk:
            existing_columns = existing_columns.exclude(pk=self.pk)
        if existing_columns.exists():
            raise ValidationError("Column with this name already exists for the file.")
        super().save(*args, **kwargs)
