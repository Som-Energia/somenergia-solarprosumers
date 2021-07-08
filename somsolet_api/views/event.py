from rest_framework import permissions
from rest_framework.views import APIView

from somrenkonto.models import RenkontoEvent
from somsolet.models import Engineering
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.common.mixins import MakeResponseMixin


class RenkontoEventView(MakeResponseMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = RenkontoEventSerializer

    def get(self, request, engineering_id):
        if not self._engineering_exists(engineering_id):
            return self.make_empty_response()

        events = self._get_engineering_events(engineering_id)

        response = self.make_response(events, request)
        return response

    def _engineering_exists(self, engineering_id):
        return Engineering.engineerings.get_engineering_by_id(engineering_id) is not None

    def _get_engineering_events(self, engineering_id):
        return RenkontoEvent.events.engineering_events(engineering_id)
