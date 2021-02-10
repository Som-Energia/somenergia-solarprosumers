from rest_framework.views import APIView

from somrenkonto.models import RenkontoEvent
from somsolet.models import Engineering
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.common.mixins import MakeResponseMixin
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class RenkontoEventView(MakeResponseMixin, APIView):
    # permission_classes = [SomsoletAPIModelPermissions]

    serializer_class = RenkontoEventSerializer

    def get(self, request, engineering_id):
        engineering = Engineering.engineerings.get_engineering_by_id(engineering_id)
        if not engineering:
            return Response([])

        events = RenkontoEvent.events.engineering_events(engineering_id)

        response = self.make_response(events)
        return response
