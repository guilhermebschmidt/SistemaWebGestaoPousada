from django import forms
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ChangePasswordForm,
    ResetPasswordForm, 
    ResetPasswordKeyForm
)

#Form com configurações dos widgets dos templates de autenticação

# Classe que aplica o Tailwind/daisyui aos forms herdeiros
class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_input_class = "input input-bordered w-full shadow-sm rounded-lg"
        checkbox_class = "checkbox"

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                widget.attrs.update({"class": text_input_class})
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs.update({"class": checkbox_class})

class CustomLoginForm(StyleFormMixin, LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.fields['login'].label = "Email"
        self.fields['login'].widget.attrs.update({"placeholder": "Digite seu email"})
        self.fields['login'].error_messages.update({
                'password_mismatch': 'As senhas digitadas não conferem. Tente novamente.',
                'required': 'Este campo é obrigatório.',
                })
        
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

class CustomChangePasswordForm(StyleFormMixin,ChangePasswordForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].label = "Senha Atual"
        self.fields['oldpassword'].widget.attrs.update({
            "placeholder": "Digite sua senha atual"
        })
        
        self.fields['password1'].label = "Nova Senha"
        self.fields['password1'].widget.attrs.update({
            "placeholder": "Digite a nova senha"
        })

        self.fields['password2'].label = "Confirme a Nova Senha"
        self.fields['password2'].widget.attrs.update({
            "placeholder": "Confirme a nova senha"
        })
    
class CustomResetPasswordForm(StyleFormMixin, ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = "Email"
        self.fields['email'].widget.attrs.update({"placeholder": "Digite seu e-mail de cadastro"})

class CustomResetPasswordFromKeyForm(StyleFormMixin, ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'new_password1' in self.fields:
            self.fields['new_password1'].label = "Nova Senha"
            self.fields['new_password1'].widget.attrs.update({"placeholder": "Crie sua nova senha"})
            self.fields['new_password1'].help_text = "Sua senha deve ter no mínimo 8 caracteres."

            self.fields['new_password1'].error_messages.update({
                'password_too_short': 'Senha muito curta. O mínimo é 8 caracteres.',
                'password_common': 'Esta senha é muito comum. Por favor, escolha uma mais segura.',
            })

        if 'new_password1' in self.fields:
            self.fields['new_password2'].label = "Confirme a Nova Senha"
            self.fields['new_password2'].widget.attrs.update({"placeholder": "Confirme sua nova senha"})
            self.fields['new_password2'].help_text = "Repita a senha exatamente como você digitou acima."

            self.fields['new_password2'].error_messages.update({
                'password_mismatch': 'As senhas digitadas não conferem. Tente novamente.',
                'required': 'Este campo é obrigatório.',
                })