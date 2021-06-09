from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from somsolet.models.choices_options import ITEM_STATUS
from somsolet.models import Project

from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import SignatureFileSerializer


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
        if serializer.is_valid():
            getattr(instance, self.stage).set_check(request.data.get('is_checked'))
            serializer.save()
            return Response(serializer.data)

    def put(self, request, format=None):
        instance = Project.objects.get(
            id=request.query_params.get('projectId')
        )
        serializer = self.serializer_class(
            instance,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            getattr(instance, self.stage).update_upload(request.data.get('upload'))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignatureViewSet(StagesBaseViewSet):

    serializer_class = SignatureFileSerializer
    stage = 'signature'
