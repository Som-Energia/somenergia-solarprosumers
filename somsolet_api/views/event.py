from rest_framework.views import APIView
from rest_framework.response import Response

from somrenkonto.models import RenkontoEvent
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class RenkontoEventView(APIView):
    # permission_classes = [SomsoletAPIModelPermissions]

    def get(self, request, engineering_id):
        response = []
        return Response(response)
        