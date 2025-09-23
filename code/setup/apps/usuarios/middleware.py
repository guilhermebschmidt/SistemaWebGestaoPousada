# setup/apps/usuarios/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

#Middleware para exigir autenticação em rotas privadas
class LoginRequiredMiddleware:
   def __init__(self, get_response):
        self.get_response = get_response

   def __call__(self, request):
        public_paths = [
            reverse('account_login'),   
            reverse('account_logout'),  
            reverse('account_signup'),  
            reverse('admin:index'),     
        ]

        if not request.user.is_authenticated and not any(request.path.startswith(p) for p in public_paths):
            return redirect('account_login')

        response = self.get_response(request)
        return response