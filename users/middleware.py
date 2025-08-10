class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, 'new_access_token'):
            response.set_cookie(
                key='access_token',
                value=request.new_access_token,
                httponly=True,
                secure=False,  # True in production with HTTPS
                samesite='Lax',
            )
        return response
