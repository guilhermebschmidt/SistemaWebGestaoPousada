from django import forms
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.crypto import get_random_string

#Form com configurações dos widgets dos templates de autenticação

# Classe que aplica o Tailwind/daisyui aos forms herdeiros
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        text_input_class = "input input-bordered w-full"
        checkbox_class = "checkbox"

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                widget.attrs.update({"class": text_input_class})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": checkbox_class})

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields['login'].label = "Email"
        self.fields['login'].widget.attrs.update({"placeholder": "Digite seu email"})
        
        self.fields['password'].label = "Senha"
        self.fields['password'].widget.attrs.update({"placeholder": "Digite sua senha"})
        
        self.fields['remember'].label = "Lembre-me"

"""class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            return user"""

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].label = "Senha Atual"
        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite sua senha atual"
        })
        self.fields['password1'].label = "Nova Senha"
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Digite a nova senha"
        })
        self.fields['password2'].label = "Confirme a Nova Senha"
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Confirme a nova senha"
        })
    
class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs.update({"placeholder": "Digite seu e-mail de cadastro"})

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Nova Senha"
        self.fields['new_password1'].widget.attrs.update({"placeholder": "Crie sua nova senha"})

        self.fields['new_password2'].label = "Confirme a Nova Senha"
        self.fields['new_password2'].widget.attrs.update({"placeholder": "Confirme sua nova senha"})