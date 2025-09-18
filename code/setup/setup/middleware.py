from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware para exigir autenticação em rotas privadas.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Rotas públicas (não exigem login)
        public_paths = [
            "/",  # home/index
            "/accounts/login/",
            "/accounts/signup/",
            "/accounts/logout/",
            "/accounts/password/reset/",
            "/accounts/password/change/",
        ]

        # Se usuário não está autenticado e não está numa rota pública → redireciona para login
        if not request.user.is_authenticated and not any(path.startswith(p) for p in public_paths):
            return redirect("/accounts/login/")

        # Caso contrário, segue o fluxo normal
        return self.get_response(request)
