from rest_framework import status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from somsolet.models import Project
from somsolet.models.choices_options import ITEM_STATUS
from somsolet_api.common.permissions import SomsoletAPIModelPermissions

from somsolet_api.serializer import (SignatureStageSerializer, PermitStageSerializer,
                                     LegalRegistrationStageSerializer, LegalizationStageSerializer,
                                     PrereportStageSerializer, ReportStageSerializer, OfferStageSerializer,
                                     SecondInvoiceStageSerializer, DeliveryCertificateStageSerializer)


class StagesListViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def list(self, request):

        result = [
            {
                'stageId': stageId,
                'stageName': stageName,
            } for stageId, stageName in ITEM_STATUS]

        return Response(result)


class StagesBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        queryset = Project.objects.all().order_by('name')

        user = self.request.headers.get('dni')
        project = self.request.query_params.get('projectId')

        if user:
            return queryset.filter(client__dni=user)
        elif project:
            return queryset.filter(id=project)
        else:
            return queryset

    def patch(self, request, *args, **kwargs):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if instance.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(instance, self.project_stage).set_check(request.data.get('is_checked'))
        instance.status = getattr(instance, self.project_stage).get_status()
        instance.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if instance.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(instance, self.project_stage).update_upload(request.data.get('upload'))
        instance.status = getattr(instance, self.project_stage).get_status()
        instance.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrereportViewSet(StagesBaseViewSet):

    serializer_class = PrereportStageSerializer
    allowed_status = ['registered', 'prereport', 'prereport review']
    project_stage = 'prereport'


class ReportViewSet(StagesBaseViewSet):

    serializer_class = ReportStageSerializer
    allowed_status = ['prereport', 'report', 'report review']
    project_stage = 'report'


class OfferViewSet(StagesBaseViewSet):

    serializer_class = OfferStageSerializer
    allowed_status = ['report', 'offer review', 'offer accepted']
    project_stage = 'offer'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class SecondInvoiceViewSet(StagesBaseViewSet):

    serializer_class = SecondInvoiceStageSerializer
    allowed_status = ['end installation', 'second invoice']
    project_stage = 'second_invoice'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class SignatureViewSet(StagesBaseViewSet):

    serializer_class = SignatureStageSerializer
    allowed_status = ['offer', 'signature']
    project_stage = 'signature'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class PermitViewSet(StagesBaseViewSet):

    serializer_class = PermitStageSerializer
    allowed_status = ['signature', 'permit']
    project_stage = 'permit'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class LegalRegistrationViewSet(StagesBaseViewSet):

    serializer_class = LegalRegistrationStageSerializer
    allowed_status = ['end installation', 'legal registration']
    project_stage = 'legal_registration'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class LegalizationViewSet(StagesBaseViewSet):

    serializer_class = LegalizationStageSerializer
    allowed_status = ['last payment', 'legalization']
    project_stage = 'legalization'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if instance.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        file_types = request.data.keys()
        if 'rac_file' in file_types:
            getattr(instance, self.project_stage).update_rac(request.data.get('rac_file'))
        if 'ritsic_file' in file_types:
            getattr(instance, self.project_stage).update_ritsic(request.data.get('ritsic_file'))
        if 'cie_file' in file_types:
            getattr(instance, self.project_stage).update_cie(request.data.get('cie_file'))
        instance.status = getattr(instance, self.project_stage).get_status()
        instance.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryCertificateViewSet(StagesBaseViewSet):

    serializer_class = DeliveryCertificateStageSerializer
    allowed_status = ['date installation set', 'end installation']
    project_stage = 'delivery_certificate'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)
