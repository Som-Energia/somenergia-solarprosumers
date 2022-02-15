from rest_framework import status, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from schedule.models import Calendar
from somsolet.models import Project, Technical_details, Engineering
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from somsolet_api.serializer import (DownloadCchSerializer,
                                     FirstInvoiceSerializer,
                                     LastInvoiceSerializer, ProjectSerializer,
                                     RenkontoEventSerializer,
                                     TechnicalDetailsSerializer)
from somsolet_api.shortcuts import (not_found_response,
                                    validation_error_response)

class ProjectGateKeeperMixin:

    def get_queryset_ov_switch(self):
        queryset = Project.objects.all().order_by('name')
        user = self.request.user

        if user.is_superuser:
            # OV
            client_dni = self.request.headers.get('dni')
            campaign = self.request.query_params.get('campaignId')
            project = self.request.query_params.get('projectId')

            if client_dni:
                return queryset.filter(client__dni=client_dni)
            elif campaign:
                return queryset.filter(campaign__id=campaign)
            elif project:
                return queryset.filter(id=project)
            else:
                # TODO should we return none or not joana?
                #return Project.objects.none()
                return queryset
        else:
            # Engineering
            try:
                engineering = Engineering.objects.get(user=user)
            except Engineering.DoesNotExist:
                # user has no engineering: unauthorized
                engineering = None

            return queryset.filter(engineering=engineering)

    def get_project_ov_switch(self):
        queryset = Project.objects.all().order_by('name')
        user = self.request.user
        project = self.request.query_params.get('projectId')

        if user.is_superuser:
            # OV
            if project:
                return Project.objects.filter(id=project).first()
            else:
                return None
        else:
            # Engineering
            engineering = Engineering.objects.filter(user=user).first()

            return queryset.filter(id=project, engineering=engineering).first()

class ProjectViewSet(viewsets.ModelViewSet, ProjectGateKeeperMixin):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    renderer_classes = [JSONRenderer]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return super(ProjectViewSet, self).get_queryset_ov_switch()


    @action(detail=True, methods=['put'], name='set_technical_visit')
    def set_technical_visit(self, request, pk):
        project = Project.projects.get_project(pk, request.user)
        if not project:
            return not_found_response()
        technical_visit = RenkontoEventSerializer(
            data=request.data, partial=True, context={'request': request}
        )
        if not technical_visit.is_valid():
            return validation_error_response(technical_visit)

        calendar = Calendar.objects.get_calendar_for_object(project.engineering.user)

        event = technical_visit.set_technical_visit(
            calendar=calendar,
            project=project,
        )

        return Response(technical_visit.to_representation(event))


class FirstInvoiceViewSet(viewsets.ModelViewSet, ProjectGateKeeperMixin):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    serializer_class = FirstInvoiceSerializer

    def get_queryset(self):
        return super(FirstInvoiceViewSet, self).get_queryset_ov_switch()

    def patch(self, request, *args, **kwargs):
        project = self.get_project_ov_switch()
        
        if not project:
            return Response({
                'data': [],
                'message': 'Not found',
            }, status=status.HTTP_404_NOT_FOUND)

        invoice = self.serializer_class(
            project,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            project.update_is_paid_first_invoice(request.data.get('is_paid_first_invoice'))
            invoice.save()
            return Response(invoice.data)

    def put(self, request, format=None):
        project = self.get_project_ov_switch()

        if not project:
            return Response({
                'data': [],
                'message': 'Not found',
            }, status=status.HTTP_404_NOT_FOUND)

        invoice = self.serializer_class(
            project,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            project.update_upload_first_invoice(request.data.get('upload_first_invoice'))
            invoice.save()
            return Response(invoice.data, status=status.HTTP_200_OK)
        else:
            return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)


class LastInvoiceViewSet(viewsets.ModelViewSet, ProjectGateKeeperMixin):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    serializer_class = LastInvoiceSerializer

    def get_queryset(self):
        return super(LastInvoiceViewSet, self).get_queryset_ov_switch()

    def patch(self, request, *args, **kwargs):
        project = self.get_project_ov_switch()

        if not project:
            return Response({
                'data': [],
                'message': 'Not found',
            }, status=status.HTTP_404_NOT_FOUND)

        invoice = self.serializer_class(
            project,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            project.update_is_paid_last_invoice(request.data.get('is_paid_last_invoice'))
            invoice.save()
            return Response(invoice.data)

    def put(self, request, format=None):
        project = self.get_project_ov_switch()

        if not project:
            return Response({
                'data': [],
                'message': 'Not found',
            }, status=status.HTTP_404_NOT_FOUND)

        invoice = self.serializer_class(
            project,
            data=request.data,
            partial=True
        )
        if invoice.is_valid():
            project.update_upload_last_invoice(request.data.get('upload_last_invoice'))
            invoice.save()
            return Response(invoice.data, status=status.HTTP_200_OK)
        else:
            return Response(invoice.errors, status=status.HTTP_400_BAD_REQUEST)


class CchDownloadViewSet(viewsets.ModelViewSet, ProjectGateKeeperMixin):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    serializer_class = DownloadCchSerializer

    def get_queryset(self):
        return super(CchDownloadViewSet, self).get_queryset_ov_switch()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DownloadCchSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class TechnicalDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    serializer_class = TechnicalDetailsSerializer

    def get_queryset(self):
        queryset = Technical_details.objects.all()
        user = self.request.user
        
        if user.is_superuser:
            # OV
            client_dni = self.request.headers.get('dni')
            campaign = self.request.query_params.get('campaignId')
            project = self.request.query_params.get('projectId')

            if client_dni:
                return queryset.filter(client__dni=client_dni)
            elif campaign:
                return queryset.filter(campaign__id=campaign)
            elif project:
                return queryset.filter(id=project)
            else:
                return Project.objects.none()
        else:
            return queryset