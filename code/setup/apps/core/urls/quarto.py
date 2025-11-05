from django.urls import path
import apps.core.views as quarto

app_name = 'quarto'

urlpatterns = [
    path('', quarto.listar , name='listar'),  # esse será /quartos/
    path('novo/', quarto.form_quarto, name='criar'),
    # alias 'form' esperado pelos testes (create and edit)
    path('form/', quarto.form_quarto, name='form'),
    path('form/<int:quarto_id>/', quarto.form_quarto, name='form'),
    path('<int:pk>/editar/', quarto.form_quarto, name='editar'),
    path('<int:pk>/excluir/', quarto.excluir, name='excluir'),
    path('<int:quarto_id>/excluir/', quarto.excluir, name='excluir'),
    path('<int:pk>/mudar-status/', quarto.mudar_status_quarto, name='mudar_status')
]