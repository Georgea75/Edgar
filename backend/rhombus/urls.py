from django.urls import path
from rhombus.views import post_sheet, get_sheet, get_supported_types, update_column_type


urlpatterns = [
    path("sheets/", post_sheet, name="sheet-post"),
    path("sheets/<int:sheet_id>/", get_sheet, name="sheet-get"),
    path(
        "columns/<int:column_id>",
        update_column_type,
        name="column-update",
    ),
    path(
        "supported-types/",
        get_supported_types,
        name="supported-data-types",
    ),
]
