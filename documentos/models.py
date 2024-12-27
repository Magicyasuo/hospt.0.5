from django.db import models
from django.contrib.auth.models import User

class SerieDocumental(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class SubserieDocumental(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    serie = models.ForeignKey(SerieDocumental, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} - {self.nombre} (Serie: {self.serie.nombre})"


class EntidadProductora(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class UnidadAdministrativa(models.Model):
    nombre = models.CharField(max_length=255)
    entidad_productora = models.ForeignKey(EntidadProductora, on_delete=models.CASCADE, related_name='unidades')

    def __str__(self):
        return f"{self.nombre} ({self.entidad_productora.nombre})"


class OficinaProductora(models.Model):
    nombre = models.CharField(max_length=255)
    unidad_administrativa = models.ForeignKey(UnidadAdministrativa, on_delete=models.CASCADE, related_name='oficinas')

    def __str__(self):
        return f"{self.nombre} ({self.unidad_administrativa.nombre})"


class Objeto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class FUID(models.Model):
    # Campos existentes
    entidad_productora = models.ForeignKey(EntidadProductora, on_delete=models.SET_NULL, null=True)
    unidad_administrativa = models.ForeignKey(UnidadAdministrativa, on_delete=models.SET_NULL, null=True)
    oficina_productora = models.ForeignKey(OficinaProductora, on_delete=models.SET_NULL, null=True)
    objeto = models.ForeignKey(Objeto, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fuids')
    registros = models.ManyToManyField('RegistroDeArchivo', related_name='fuids', blank=True)

    # Nuevos campos
    # Elaborado Por
    elaborado_por_nombre = models.CharField(max_length=255, null=True, blank=True)  # Nombres y apellidos
    elaborado_por_cargo = models.CharField(max_length=255, null=True, blank=True)   # Cargo
    elaborado_por_lugar = models.CharField(max_length=255, null=True, blank=True)   # Lugar
    elaborado_por_fecha = models.DateField(null=True, blank=True)                   # Fecha

    # Entregado
    entregado_por_nombre = models.CharField(max_length=255, null=True, blank=True)  # Nombres y apellidos
    entregado_por_cargo = models.CharField(max_length=255, null=True, blank=True)   # Cargo
    entregado_por_lugar = models.CharField(max_length=255, null=True, blank=True)   # Lugar
    entregado_por_fecha = models.DateField(null=True, blank=True)                   # Fecha

    # Recibido Por
    recibido_por_nombre = models.CharField(max_length=255, null=True, blank=True)   # Nombres y apellidos
    recibido_por_cargo = models.CharField(max_length=255, null=True, blank=True)    # Cargo
    recibido_por_lugar = models.CharField(max_length=255, null=True, blank=True)    # Lugar
    recibido_por_fecha = models.DateField(null=True, blank=True)                    # Fecha

    class Meta:
        permissions = [
            ("view_own_fuid", "Puede ver sus propios FUIDs"),
            ("edit_own_fuid", "Puede editar sus propios FUIDs"),
            ("delete_own_fuid", "Puede eliminar sus propios FUIDs"),
        ]
    

    def __str__(self):
        return f"FUID #{self.id} - {self.entidad_productora.nombre if self.entidad_productora else 'Sin Entidad'}"



class RegistroDeArchivo(models.Model):  
    numero_orden = models.CharField(max_length=50)  # Identificador único
    codigo = models.CharField(max_length=50, blank=True, null=True)
    codigo_serie = models.ForeignKey(SerieDocumental, on_delete=models.CASCADE, related_name="registros")
    codigo_subserie = models.ForeignKey(SubserieDocumental, on_delete=models.CASCADE, blank=True, null=True, related_name="registros")
    unidad_documental = models.CharField(max_length=255)
    fecha_archivo = models.DateField(blank=True, null=True)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    soporte_fisico = models.BooleanField(default=False)
    soporte_electronico = models.BooleanField(default=False)
    caja = models.CharField(max_length=50, blank=True, null=True)
    carpeta = models.CharField(max_length=50, blank=True, null=True)
    tomo_legajo_libro = models.CharField(max_length=50, blank=True, null=True)
    numero_folios = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255)
    cantidad_documentos_electronicos = models.IntegerField(null=True, blank=True)
    tamano_documentos_electronicos = models.CharField(max_length=50, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("view_own_registro", "Puede ver sus propios registros"),
            ("edit_own_registro", "Puede editar sus propios registros"),
            ("delete_own_registro", "Puede eliminar sus propios registros"),
        ]

    def __str__(self):
        return f"{self.numero_orden} - {self.unidad_documental or 'Sin Nombre'}"
    

    


class PermisoUsuarioSerie(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    serie = models.ForeignKey(SerieDocumental, on_delete=models.CASCADE)
    permiso_crear = models.BooleanField(default=False)
    permiso_editar = models.BooleanField(default=False)
    permiso_consultar = models.BooleanField(default=True)
    permiso_eliminar = models.BooleanField(default=False)

    def __str__(self):
        return f"Permisos de {self.usuario.username} sobre {self.serie.nombre}"


class FichaPaciente (models.Model):
    consecutivo = models.AutoField(primary_key=True)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    num_identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    primer_nombre_padre = models.CharField(max_length=50, blank=True, null=True)
    segundo_nombre_padre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido_padre = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido_padre = models.CharField(max_length=50, blank=True, null=True)
    Numero_historia_clinica = models.CharField(max_length=20, unique=True)
    caja = models.CharField(max_length=20)
    carpeta = models.CharField(max_length=20)
    tipo_identificacion = models.CharField(max_length=20, default='Cedula de Ciudadania')
    sexo = models.CharField(max_length=10, default='Masculino')
    activo = models.BooleanField(default=True)

    

    def __str__(self):
        return f"Ficha del paciente  {self.primer_nombre} con identificacion {self.num_identificacion}"
    

    # models.py

from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    oficina = models.ForeignKey(OficinaProductora, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.oficina.nombre}"


