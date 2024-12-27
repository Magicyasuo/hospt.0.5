# from documentos.models import RegistroDeArchivo, SerieDocumental, SubserieDocumental
# from django.contrib.auth.models import User
# from datetime import date, timedelta
# import random

# def crear_registros():
#     # Obtener usuario creador o crear uno si no existe
#     user, created = User.objects.get_or_create(username="testuser")
#     if created:
#         user.set_password("password123")
#         user.save()

#     # Obtener todas las series
#     series = SerieDocumental.objects.all()

#     # Verificar si hay series disponibles
#     if not series.exists():
#         print("No hay series disponibles. Por favor, crea series primero.")
#         return

#     # Generar registros
#     for i in range(100):  # Número de registros a crear
#         # Seleccionar una serie al azar
#         serie = random.choice(series)

#         # Seleccionar una subserie relacionada, si existe
#         subseries = SubserieDocumental.objects.filter(serie=serie)
#         subserie = random.choice(subseries) if subseries.exists() else None

#         # Crear el registro
#         RegistroDeArchivo.objects.create(
#             numero_orden=f"REG-{i+1:04d}",
#             codigo=f"CODE-{i+1:04d}",
#             codigo_serie=serie,
#             codigo_subserie=subserie,
#             unidad_documental=f"Unidad Documental {i+1}",
#             fecha_archivo=date.today() - timedelta(days=random.randint(0, 1000)),
#             soporte_fisico=random.choice([True, False]),
#             soporte_electronico=random.choice([True, False]),
#             tipo=random.choice(["Tipo A", "Tipo B", "Tipo C"]),
#             cantidad=random.randint(1, 100),
#             ubicacion=f"Ubicación {i+1}",
#             creado_por=user  # Asignar el usuario creador
#         )

#     print("Registros creados correctamente.")


from documentos.models import FichaPaciente
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

def crear_fichas_pacientes():
    # Obtener usuario creador o crear uno si no existe
    user, created = User.objects.get_or_create(username="testuser")
    if created:
        user.set_password("password123")
        user.save()

    nombres = ["Carlos", "Ana", "Juan", "María", "Luis", "Sofía", "Pedro", "Lucía", "José", "Elena"]
    apellidos = ["García", "Martínez", "Rodríguez", "López", "Pérez", "Gómez", "Díaz", "Hernández", "Ruiz", "Morales"]

    tipos_identificacion = [
        "Cédula de Ciudadanía",
        "Tarjeta de Identidad",
        "Pasaporte",
        "Registro Civil"
    ]
    generos = ["Masculino", "Femenino"]

    # Crear 100 fichas de pacientes
    for i in range(100):
        # Generar nombre y apellido aleatorios
        primer_nombre = random.choice(nombres)
        segundo_nombre = random.choice(nombres) if random.random() > 0.5 else ""
        primer_apellido = random.choice(apellidos)
        segundo_apellido = random.choice(apellidos) if random.random() > 0.5 else ""

        # Generar fecha de nacimiento aleatoria
        fecha_nacimiento = date.today() - timedelta(days=random.randint(5000, 30000))

        # Crear ficha de paciente
        FichaPaciente.objects.create(
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            num_identificacion=f"ID-{i+1:05d}",
            fecha_nacimiento=fecha_nacimiento,
            primer_nombre_padre=random.choice(nombres),
            segundo_nombre_padre=random.choice(nombres) if random.random() > 0.5 else "",
            primer_apellido_padre=random.choice(apellidos),
            segundo_apellido_padre=random.choice(apellidos) if random.random() > 0.5 else "",
            Numero_historia_clinica=f"HC-{i+1:05d}",
            caja=str(random.randint(1, 50)),
            carpeta=str(random.randint(1, 100)),
            tipo_identificacion=random.choice(tipos_identificacion),
            sexo=random.choice(generos),
            activo=random.choice([True, False])
        )

    print("Fichas de pacientes creadas correctamente.")

# from documentos.crear_registros import crear_fichas_pacientes
# crear_fichas_pacientes()
