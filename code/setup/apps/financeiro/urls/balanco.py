from django.urls import path
from ..views.balanco import balanco_financeiro

urlpatterns = [
    path('balanco/', balanco_financeiro, name='balanco_financeiro'),
]