"""
Rutas de la app "citas".

El parámetro name permite referirse a cada ruta desde las plantillas
con {% url 'nombre' %}, sin escribir la dirección completa.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.CitaListView.as_view(), name='cita_lista'),
    path('nueva/', views.CitaCreateView.as_view(), name='cita_nueva'),
    path('<int:pk>/cancelar/', views.cita_cancelar, name='cita_cancelar'),
    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_nuevo'),
]
