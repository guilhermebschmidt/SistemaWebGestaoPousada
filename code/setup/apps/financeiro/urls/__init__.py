from .titulo import urlpatterns as titulo_urls
from .categoria import urlpatterns as categoria_urls

app_name = 'financeiro'

urlpatterns = titulo_urls + categoria_urls