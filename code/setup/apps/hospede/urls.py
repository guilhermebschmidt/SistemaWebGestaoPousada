from django.urls import path
from apps.hospede.views import hospede, hospede_create, hospede_update, hospede_delete, hospede_search, hospede_detail, hospede_list



urlpatterns = [
    path('hospedes/', hospede, name='hospedes' ),
    path('hospede_create/', hospede_create, name='hospede_create'),
    path('hospede_update/<str:cpf>/', hospede_update, name='hospede_update'),
    path('hospede_delete/<str:cpf>/', hospede_delete, name='hospede_delete'),
    path('hospede_search/', hospede_search, name='hospede_search'),
    path('hospede_detail/<str:cpf>/', hospede_detail, name='hospede_detail'),
    path('hospede_list/', hospede_list, name='hospede_list'),
]
