from django.shortcuts import redirect
from django.conf import settings
#Middleware para exigir autenticação em rotas privadas
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        public_paths = [
            "/",  # home/index
            "/accounts/login/",
            "/accounts/signup/",
            "/accounts/logout/",
            "/accounts/password/reset/",
            "/accounts/password/change/",
        ]
        
        if not request.user.is_authenticated and not any(path.startswith(p) for p in public_paths):
            return redirect("/accounts/login/")

        return self.get_response(request)
