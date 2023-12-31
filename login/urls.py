from django.urls import path
from . import views

app_name = 'login'  

urlpatterns = [
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/actualizar/', views.perfil_actualizar, name='perfil_actualizar'),
    path('perfil/cargar_imagen/', views.cargar_imagen, name='cargar_imagen'),
]

