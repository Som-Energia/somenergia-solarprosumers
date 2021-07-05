from rest_framework.response import Response


class MakeResponseMixin:
    def make_response(self, results_query):
        serializer = self.serializer_class()
        response = Response({
            'data': {
                'count': results_query.count(),
                'results': [
                    serializer.get_data(result.id) for result in results_query
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
