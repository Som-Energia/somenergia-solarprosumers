from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework import status


def not_found_response():
    return Response(
        {
            "data": [],
            "message": "Not found",
        },
        status=status.HTTP_404_NOT_FOUND,
    )


def validation_error_response(serializer):
    errors = [
        {"field": field, "reasons": reasons}
        for field, reasons in serializer.errors.items()
    ]
    return Response(
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": _("There are incorrect fields in the request"),
                "data": errors,
            }
        },
        status=status.HTTP_400_BAD_REQUEST,
    )
