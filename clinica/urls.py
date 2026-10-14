"""
Rutas principales del proyecto.

Cada app define sus propias rutas en su archivo urls.py y aquí
solo se enlazan con include().
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel de administración de Django.
    path('admin/', admin.site.urls),

    # Todas las rutas de la app "citas" cuelgan de la raíz del sitio.
    path('', include('citas.urls')),
]
