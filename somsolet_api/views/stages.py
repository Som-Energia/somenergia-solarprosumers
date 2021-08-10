from rest_framework import status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from somsolet.models import Project
from somsolet.models.choices_options import ITEM_STATUS
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (SignatureFileSerializer, PermitFileSerializer,
                                     LegalRegistrationFileSerializer, LegalizationFileSerializer,
                                     PrereportFileSerializer)


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

        if instance.status not in self.allowed_stages:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(instance, self.stage).set_check(request.data.get('is_checked'))
        instance.status = getattr(instance, self.stage).get_status()
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

        if instance.status not in self.allowed_stages:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(instance, self.stage).update_upload(request.data.get('upload'))
        instance.status = getattr(instance, self.stage).get_status()
        instance.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrereportViewSet(StagesBaseViewSet):

    serializer_class = PrereportFileSerializer
    allowed_stages = ['registered', 'prereport', 'prereport review']
    stage = 'prereport'


class SignatureViewSet(StagesBaseViewSet):

    serializer_class = SignatureFileSerializer
    allowed_stages = ['offer', 'signature']
    stage = 'signature'


class PermitViewSet(StagesBaseViewSet):

    serializer_class = PermitFileSerializer
    allowed_stages = ['signature', 'permit']
    stage = 'permit'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class LegalRegistrationViewSet(StagesBaseViewSet):

    serializer_class = LegalRegistrationFileSerializer
    allowed_stages = ['end installation', 'legal registration']
    stage = 'legal_registration'

    def patch(self, request, *args, **kwargs):
        return Response('Patch is not allowed', status=status.HTTP_400_BAD_REQUEST)


class LegalizationViewSet(StagesBaseViewSet):

    serializer_class = LegalizationFileSerializer
    allowed_stages = ['last payment', 'legalization']
    stage = 'legalization'

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

        if instance.status not in self.allowed_stages:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        file_types = request.data.keys()
        if 'rac_file' in file_types:
            getattr(instance, self.stage).update_rac(request.data.get('rac_file'))
        if 'ritsic_file' in file_types:
            getattr(instance, self.stage).update_ritsic(request.data.get('ritsic_file'))
        if 'cie_file' in file_types:
            getattr(instance, self.stage).update_cie(request.data.get('cie_file'))
        instance.status = getattr(instance, self.stage).get_status()
        instance.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
