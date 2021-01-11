from rest_framework import viewsets
from somrenkonto.models import RenkontoEvent
from somsolet_api.serializer import RenkontoEventSerializer
from somsolet_api.common.permissions import SomsoletAPIModelPermissions


class RenkontoEventViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]

    queryset = RenkontoEvent.objects.all().order_by('date_start')
    serializer_class = RenkontoEventSerializer

    def get_queryset(self):
        user = self.request.headers.get('dni')
        return RenkontoEvent.objects.filter(project__client__dni=user)
