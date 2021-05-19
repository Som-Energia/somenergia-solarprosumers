from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from somsolet.models.choices_options import ITEM_STATUS


class StagesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def list(self, request):

        result = [
            {
                'stageId': stageId,
                'stageName': stageName,
            } for stageId, stageName in ITEM_STATUS]

        return Response(result)
