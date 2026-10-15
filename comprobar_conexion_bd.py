"""
Comprueba la conexión con la base de datos PostgreSQL configurada en Django
(por ejemplo, Neon). Usa la misma configuración que la aplicación
(clinica.settings -> DATABASE_URL), así que si esto funciona, la app también
puede conectarse.

Uso, desde la carpeta del proyecto (con el entorno virtual activado):

    python comprobar_conexion_bd.py

Imprime "Conexión exitosa" si logra conectar y ejecutar una consulta de prueba,
o "Conexión fallida" junto con el error en caso contrario.
Devuelve el código de salida 0 si la conexión fue exitosa y 1 si falló.
"""

import os
import sys

# Asegura que los acentos se impriman bien en consolas de Windows.
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except (AttributeError, ValueError):
    pass

# Debe apuntar al mismo módulo de configuración que usa manage.py.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinica.settings')


def comprobar_conexion():
    """Intenta conectarse a la base de datos y ejecutar una consulta simple."""

    try:
        import django
        django.setup()

        from django.conf import settings
        from django.db import connection

        # Consulta de prueba: obliga a abrir una conexión real a la base de datos.
        with connection.cursor() as cursor:
            cursor.execute('SELECT version();')
            version = cursor.fetchone()[0]

    except Exception as error:  # pylint: disable=broad-except
        print('Conexión fallida')
        print(f'  Error: {type(error).__name__}: {error}')
        return 1

    db = settings.DATABASES['default']
    print('Conexión exitosa')
    print(f'  Motor    : {db["ENGINE"]}')
    print(f'  Host     : {db["HOST"]}')
    print(f'  Base     : {db["NAME"]}')
    print(f'  Usuario  : {db["USER"]}')
    print(f'  Servidor : {version.split(",")[0]}')
    return 0


if __name__ == '__main__':
    sys.exit(comprobar_conexion())
