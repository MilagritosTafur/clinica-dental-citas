"""
Formularios de la app "citas".

Un ModelForm genera el formulario a partir de un modelo y aplica
sus validaciones de forma automática.
"""

from datetime import date

from django import forms

from .models import Cita, Paciente


class BootstrapMixin:
    """Agrega las clases de Bootstrap a todos los campos del formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            es_lista = isinstance(field.widget, forms.Select)
            field.widget.attrs['class'] = 'form-select' if es_lista else 'form-control'


class PacienteForm(BootstrapMixin, forms.ModelForm):
    """Formulario para registrar un paciente."""

    class Meta:
        model = Paciente
        fields = ['dni', 'nombre', 'apellido', 'telefono', 'correo']

    def clean_dni(self):
        """El DNI debe tener exactamente 8 dígitos."""
        dni = self.cleaned_data['dni']
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener 8 dígitos.')
        return dni


class CitaForm(BootstrapMixin, forms.ModelForm):
    """Formulario para registrar una cita."""

    class Meta:
        model = Cita
        # "estado" no se muestra: toda cita nueva queda como "programada".
        fields = ['paciente', 'odontologo', 'consultorio', 'fecha', 'hora']
        widgets = {
            # Selectores nativos de fecha y hora del navegador.
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_fecha(self):
        """No se permite registrar citas en fechas pasadas."""
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise forms.ValidationError('No se puede registrar una cita en una fecha pasada.')
        return fecha
