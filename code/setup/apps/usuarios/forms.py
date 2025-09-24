from django import forms
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from django.utils.crypto import get_random_string
#configuração dos widgets dos templates de autenticação

class CustomLoginForm(LoginForm):

    login = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite seu email"
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite sua senha"
        })
    )
    remember = forms.BooleanField(
        label="Lembre-me",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox"})
    )

class CustomSignupForm(SignupForm):

    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite seu nome"
        })
    )
    last_name = forms.CharField(
        label="Sobrenome",
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite seu sobrenome"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite seu email"
        })
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite sua senha"
        })
    )

    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Confirme sua senha"
        })
    )
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        base_username = f"{user.first_name.lower()}.{user.last_name.lower()}"
        random_suffix = get_random_string(length=4)  # para evitar duplicidade
        user.username = f"{base_username}{random_suffix}"
        user.save()
        return user

class CustomChangePasswordForm(ChangePasswordForm):
    oldpassword = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite sua senha atual"
        })
    )

    password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite a nova senha"
        })
    )

    password2 = forms.CharField(
        label="Confirme a Nova Senha",
        widget=forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Confirme a nova senha"
        })
    )

    def save(self, *args, **kwargs):
        """
        Salva a nova senha do usuário.
        """
        return super().save(*args, **kwargs)