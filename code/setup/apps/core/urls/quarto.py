from django.urls import path
import apps.core.views as quarto

app_name = 'quarto'

urlpatterns = [
    path('', quarto.listar , name='listar'),  # esse será /quartos/
    path('novo/', quarto.form_quarto, name='criar'),
    path('<int:pk>/editar/', quarto.form_quarto, name='editar'),
    path('<int:pk>/excluir/', quarto.excluir, name='excluir'),
    path('<int:pk>/mudar-status/', quarto.mudar_status_quarto, name='mudar_status')
]