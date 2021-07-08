from rest_framework.response import Response


class MakeResponseMixin:
    def make_response(self, results_query, request):
        response = Response({
            'data': {
                'count': results_query.count(),
                'results': [
                    self.serializer_class(
                        result, context={'request': request}
                    ).data for result in results_query
                ]
            }
        })
        return response

    def make_empty_response(self):
        response = Response({
            'data': {
                'count': 0,
                'results': []
            }
        })
        return response
