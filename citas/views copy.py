"""
Vistas de la app "citas".

Una vista recibe la petición del navegador, trabaja con los modelos
y devuelve una plantilla HTML.
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView

from .forms import CitaForm, PacienteForm
from .models import Cita


class CitaListView(ListView):
    """Lista las citas, con filtro opcional por fecha (?fecha=AAAA-MM-DD)."""

    model = Cita
    template_name = 'citas/cita_lista.html'
    context_object_name = 'citas'

    def get_queryset(self):
        # select_related trae paciente, odontólogo y consultorio en una sola
        # consulta, en lugar de una consulta por cada fila.
        qs = super().get_queryset().select_related('paciente', 'odontologo', 'consultorio')
        fecha = self.request.GET.get('fecha')
        if fecha:
            qs = qs.filter(fecha=fecha)
        return qs


class CitaCreateView(CreateView):
    """Muestra el formulario de registro de cita y la guarda."""

    form_class = CitaForm
    template_name = 'citas/form.html'
    success_url = reverse_lazy('cita_lista')  # Destino tras guardar.
    extra_context = {'titulo': 'Registrar cita'}

    def form_valid(self, form):
        # Se ejecuta solo cuando el formulario es válido.
        messages.success(self.request, 'Cita registrada.')
        return super().form_valid(form)


class PacienteCreateView(CreateView):
    """Muestra el formulario de registro de paciente y lo guarda."""

    form_class = PacienteForm
    template_name = 'citas/form.html'
    success_url = reverse_lazy('cita_nueva')  # Lleva a registrar su cita.
    extra_context = {'titulo': 'Registrar paciente'}

    def form_valid(self, form):
        messages.success(self.request, 'Paciente registrado. Ya puedes crear su cita.')
        return super().form_valid(form)


@require_POST  # Solo acepta POST: cancelar cambia datos y no debe hacerse con un enlace.
def cita_cancelar(request, pk):
    """Cambia el estado de una cita a "cancelada" (no la borra)."""
    cita = get_object_or_404(Cita, pk=pk)
    cita.estado = 'cancelada'
    cita.save()
    messages.info(request, 'Cita cancelada.')
    return redirect('cita_lista')
