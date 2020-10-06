from rest_framework import viewsets
from rest_framework.response import Response
from somsolet.choices_options import ITEM_STATUS


class StagesViewSet(viewsets.ViewSet):

    def list(self, request):

        result = [
            {
                'stageId': stageId,
                'stageName': stageName,
            } for stageId, stageName in ITEM_STATUS]

        return Response(result)
