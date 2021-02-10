from rest_framework.views import APIView
from rest_framework.response import Response

from somrenkonto.models import RenkontoEvent
from somsolet.models import Engineering
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class RenkontoEventView(APIView):
    # permission_classes = [SomsoletAPIModelPermissions]

    def get(self, request, engineering_id):
        engineering = Engineering.engineerings.get_engineering_by_id(engineering_id)
        if not engineering:
            return Response([])
        
        events = RenkontoEvent.events.engineering_events(engineering_id)
        response = [RenkontoEventSerializer(event) for event in events]

        return Response(response)
