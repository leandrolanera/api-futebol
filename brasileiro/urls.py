from django.urls import path
from . import views

app_name = 'brasileiro'

urlpatterns = [
    path('importacao/', views.importacao, name="importacao"),
]