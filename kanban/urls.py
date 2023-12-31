from django.urls import path
from . import views

app_name = 'kanvan' 

urlpatterns = [
    path('', views.kanban, name='kanban'),
    path('actualizar/', views.actualizar, name='actualizar'),
    path('motivo/', views.motivo, name='motivo'),
    path('historial/<uuid:publicacion_id>/', views.historial, name='historial'),
]
