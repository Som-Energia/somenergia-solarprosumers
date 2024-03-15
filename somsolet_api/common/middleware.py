from rest_framework.response import Response


class ResponseStateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, Response):
            response_ok = response.status_code < 400
            try:
                response.data.update({"state": response_ok})
            except AttributeError:
                response.data = {
                    "state": response_ok,
                    "data": {"count": len(response.data), "results": response.data},
                }

        return response
