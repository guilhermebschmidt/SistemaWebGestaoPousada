from django.shortcuts import redirect
from django.urls import reverse, resolve, NoReverseMatch


#Middleware para exigir autenticação em rotas privadas
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_url_names = [
            'account_login',
            'account_logout',
            'account_reset_password',
            'account_reset_password_done',
            'account_reset_password_from_key',
            'account_reset_password_from_key_done',
        ]
        self.public_admin_path = reverse('admin:index')

    def __call__(self, request):
        # admin
        if request.path.startswith(self.public_admin_path):
            return self.get_response(request)
        # usuario não logado
        if not request.user.is_authenticated:
            try:
                current_url_name = resolve(request.path_info).url_name
                if current_url_name not in self.public_url_names:
                    return redirect('account_login')
            except NoReverseMatch:
                # URL inválida
                return redirect('account_login')

        response = self.get_response(request)
        return response