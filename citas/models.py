"""
Modelos de la app "citas".

Cada clase representa una tabla de la base de datos, siguiendo el diagrama
entidad-relación del proyecto. Django crea automáticamente la clave primaria
"id" en cada modelo, salvo en Paciente, que usa el DNI.
"""

from django.db import models


class Paciente(models.Model):
    """Persona que se atiende en la clínica. El DNI es la clave primaria."""

    dni = models.CharField(max_length=8, primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"


class Odontologo(models.Model):
    """Profesional que atiende las citas."""

    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'odontólogo'
        verbose_name_plural = 'odontólogos'

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


class Consultorio(models.Model):
    """Sala donde se realiza la atención."""

    # Valores permitidos para el estado (valor guardado, texto mostrado).
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'En mantenimiento'),
    ]

    numero_sala = models.CharField(max_length=10)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def __str__(self):
        return f"Sala {self.numero_sala}"


class Tratamiento(models.Model):
    """Servicio que ofrece la clínica, con su costo base."""

    nombre_servicio = models.CharField(max_length=100)
    costo_base = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre_servicio


class Cita(models.Model):
    """Cita de un paciente con un odontólogo en un consultorio."""

    ESTADOS = [
        ('programada', 'Programada'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    ]

    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programada')

    # PROTECT: impide borrar un paciente, odontólogo o consultorio
    # que ya tenga citas registradas.
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
    odontologo = models.ForeignKey(Odontologo, on_delete=models.PROTECT)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.PROTECT)

    class Meta:
        # Las citas se listan ordenadas por fecha y hora.
        ordering = ['fecha', 'hora']

        # Evita citas duplicadas: un odontólogo o un consultorio no pueden
        # tener dos citas a la misma fecha y hora. Las citas canceladas
        # no cuentan, así el horario queda libre de nuevo.
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'hora', 'odontologo'],
                condition=~models.Q(estado='cancelada'),
                name='unique_odontologo_fecha_hora',
            ),
            models.UniqueConstraint(
                fields=['fecha', 'hora', 'consultorio'],
                condition=~models.Q(estado='cancelada'),
                name='unique_consultorio_fecha_hora',
            ),
        ]

    def __str__(self):
        return f"{self.paciente} - {self.fecha} {self.hora}"


class CitaDetalle(models.Model):
    """Tratamiento realizado dentro de una cita (relación cita-tratamiento)."""

    # CASCADE: si se elimina la cita, sus detalles se eliminan con ella.
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='detalles')
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.PROTECT)
    observaciones = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'detalle de cita'
        verbose_name_plural = 'detalles de cita'

    def __str__(self):
        return f"{self.cita} - {self.tratamiento}"
