from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from somsolet.models import Project, Engineering
from somsolet.models.choices_options import ProjectStatus
from somsolet_api.common.permissions import SomsoletAPIModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import DjangoModelPermissions  # TODO: Custom class

from somsolet_api.serializer import (
    SignatureStageSerializer,
    PermitStageSerializer,
    LegalRegistrationStageSerializer,
    LegalizationStageSerializer,
    PrereportStageSerializer,
    ReportStageSerializer,
    OfferStageSerializer,
    SecondInvoiceStageSerializer,
    DeliveryCertificateStageSerializer,
)

from somsolet_api.views.project import ProjectGateKeeperMixin


class StagesListViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        result = [
            {
                "stageId": stageId,
                "stageName": stageName,
            }
            for stageId, stageName in ProjectStatus.choices
        ]

        return Response(result)


class StagesBaseViewSet(viewsets.ModelViewSet, ProjectGateKeeperMixin):
    permission_classes = [SomsoletAPIModelPermissions]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Project.objects.all().order_by("name")
        user = self.request.user

        if user.is_superuser:
            # OV
            client_dni = self.request.headers.get("dni")
            project = self.request.query_params.get("projectId")
            if client_dni:
                return queryset.filter(client__dni=client_dni)
            elif project:
                return queryset.filter(id=project)
            return Project.objects.none()
        else:
            # Engineering

            return queryset.filter(engineering__user=user)

    def patch(self, request, *args, **kwargs):
        project_id = self.request.query_params.get("projectId")
        project = Project.projects.get_project(project_id, self.request.user)

        serializer = self.serializer_class(project, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if project.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(project, self.project_stage).set_check(request.data.get("is_checked"))
        project.status = getattr(project, self.project_stage).get_status()
        project.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        project_id = self.request.query_params.get("projectId")
        project = Project.projects.get_project(project_id, self.request.user)

        serializer = self.serializer_class(project, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if project.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        getattr(project, self.project_stage).update_upload(request.data.get("upload"))
        project.status = getattr(project, self.project_stage).get_status()
        project.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PrereportViewSet(StagesBaseViewSet):
    serializer_class = PrereportStageSerializer
    allowed_status = ["registered", "prereport", "prereport review"]
    project_stage = "prereport"


class ReportViewSet(StagesBaseViewSet):
    serializer_class = ReportStageSerializer
    allowed_status = ["prereport", "report", "report review"]
    project_stage = "report"


class OfferViewSet(StagesBaseViewSet):
    serializer_class = OfferStageSerializer
    allowed_status = ["report", "offer review", "offer accepted"]
    project_stage = "offer"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)


class OfferAcceptedViewSet(StagesBaseViewSet):
    serializer_class = OfferStageSerializer
    allowed_status = ["offer review", "offer accepted"]
    project_stage = "offer_accepted"

    def put(self, request, *args, **kwargs):
        return Response("Put is not allowed", status=status.HTTP_400_BAD_REQUEST)


class SignatureViewSet(StagesBaseViewSet):
    serializer_class = SignatureStageSerializer
    allowed_status = ["offer accepted", "signature"]
    project_stage = "signature"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)


class PermitViewSet(StagesBaseViewSet):
    serializer_class = PermitStageSerializer
    allowed_status = ["signature", "permit"]
    project_stage = "permit"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)


class SecondInvoiceViewSet(StagesBaseViewSet):
    serializer_class = SecondInvoiceStageSerializer
    allowed_status = ["end installation", "second invoice"]
    project_stage = "second_invoice"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)


class LegalRegistrationViewSet(StagesBaseViewSet):
    serializer_class = LegalRegistrationStageSerializer
    allowed_status = ["end installation", "legal registration"]
    project_stage = "legal_registration"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)


class LegalizationViewSet(StagesBaseViewSet):
    serializer_class = LegalizationStageSerializer
    allowed_status = ["last payment", "legalization"]
    project_stage = "legalization"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        project_id = self.request.query_params.get("projectId")
        project = Project.projects.get_project(project_id, self.request.user)

        serializer = self.serializer_class(project, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if project.status not in self.allowed_status:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        file_types = request.data.keys()
        if "rac_file" in file_types:
            getattr(project, self.project_stage).update_rac(
                request.data.get("rac_file")
            )
        if "ritsic_file" in file_types:
            getattr(project, self.project_stage).update_ritsic(
                request.data.get("ritsic_file")
            )
        if "cie_file" in file_types:
            getattr(project, self.project_stage).update_cie(
                request.data.get("cie_file")
            )
        project.status = getattr(project, self.project_stage).get_status()
        project.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryCertificateViewSet(StagesBaseViewSet):
    serializer_class = DeliveryCertificateStageSerializer
    allowed_status = ["date installation set", "end installation"]
    project_stage = "delivery_certificate"

    def patch(self, request, *args, **kwargs):
        return Response("Patch is not allowed", status=status.HTTP_400_BAD_REQUEST)
