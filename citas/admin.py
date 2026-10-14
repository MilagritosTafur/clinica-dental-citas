"""
Configuración del panel de administración (/admin).
"""

from django.contrib import admin

from .models import Cita, CitaDetalle, Consultorio, Odontologo, Paciente, Tratamiento


class CitaDetalleInline(admin.TabularInline):
    """Permite agregar los tratamientos desde la misma pantalla de la cita."""

    model = CitaDetalle
    extra = 1  # Una fila vacía lista para completar.


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    # Columnas que se muestran en el listado.
    list_display = ('fecha', 'hora', 'paciente', 'odontologo', 'consultorio', 'estado')
    # Filtros laterales.
    list_filter = ('estado', 'fecha', 'odontologo')
    inlines = [CitaDetalleInline]


# Modelos sin configuración especial.
admin.site.register([Paciente, Odontologo, Consultorio, Tratamiento])
