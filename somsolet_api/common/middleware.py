class ResponseStateMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response_ok = response.status_code < 400
        response.data.update({'state': response_ok})

        return response
