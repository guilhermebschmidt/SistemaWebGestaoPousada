from .titulo import urlpatterns as titulo_urls
from .categoria import urlpatterns as categoria_urls
from .balanco import urlpatterns as balanco_urls

app_name = 'financeiro'

# concatena todas as sub-urls do app (títulos, categorias, balanço e relatórios)
urlpatterns = titulo_urls + categoria_urls + balanco_urls 