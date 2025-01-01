from django.contrib import admin
from .models import (
    SerieDocumental, SubserieDocumental, RegistroDeArchivo, PermisoUsuarioSerie, 
    EntidadProductora, UnidadAdministrativa, OficinaProductora, Objeto, FUID, FichaPaciente
)


@admin.register(SerieDocumental)
class SerieDocumentalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')


@admin.register(SubserieDocumental)
class SubserieDocumentalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'serie')
    list_filter = ('serie',)
    search_fields = ('codigo', 'nombre')


@admin.register(RegistroDeArchivo)
class RegistroDeArchivoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_orden', 'unidad_documental', 'fecha_archivo', 
        'creado_por', 'ubicacion', 'soporte_fisico', 'soporte_electronico'
    )
    list_filter = ('soporte_fisico', 'soporte_electronico', 'fecha_archivo', 'creado_por')
    search_fields = ('numero_orden', 'unidad_documental', 'ubicacion', 'notas')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información General', {
            'fields': ('numero_orden', 'codigo_serie', 'codigo_subserie', 'unidad_documental','fecha_archivo', 
                        'fecha_inicial', 'fecha_final', 'notas')
        }),
        ('Soporte', {
            'fields': ('soporte_fisico', 'soporte_electronico', 'caja', 'carpeta', 
                       'tomo_legajo_libro', 'numero_folios', 'cantidad', 'ubicacion')
        }),
        ('Información Electrónica', {
            'fields': ('cantidad_documentos_electronicos', 'tamano_documentos_electronicos')
        }),
        ('Metadatos', {
            'fields': ('creado_por', 'fecha_creacion')
        }),
    )


@admin.register(PermisoUsuarioSerie)
class PermisoUsuarioSerieAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'serie', 'permiso_crear', 'permiso_editar', 'permiso_consultar', 'permiso_eliminar')
    list_filter = ('serie', 'usuario')


@admin.register(EntidadProductora)
class EntidadProductoraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(UnidadAdministrativa)
class UnidadAdministrativaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entidad_productora')
    list_filter = ('entidad_productora',)
    search_fields = ('nombre', 'entidad_productora__nombre')


@admin.register(OficinaProductora)
class OficinaProductoraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad_administrativa')
    list_filter = ('unidad_administrativa',)
    search_fields = ('nombre', 'unidad_administrativa__nombre')


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(FUID)
class FUIDAdmin(admin.ModelAdmin):
    list_display = ('id', 'entidad_productora', 'unidad_administrativa', 'oficina_productora', 'objeto', 'creado_por', 'fecha_creacion')
    list_filter = ('entidad_productora', 'unidad_administrativa', 'oficina_productora', 'objeto', 'creado_por')
    search_fields = ('id', 'entidad_productora__nombre', 'unidad_administrativa__nombre', 'oficina_productora__nombre', 'objeto__nombre')
    filter_horizontal = ('registros',)  # Para administrar el ManyToManyField

@admin.register(FichaPaciente)
class FichaPacienteAdmin(admin.ModelAdmin):
    list_display = ('consecutivo', 'primer_nombre', 'primer_apellido', 'num_identificacion', 'Numero_historia_clinica', 'activo')
    list_filter = ('activo', 'sexo', 'tipo_identificacion')
    search_fields = ('primer_nombre', 'primer_apellido', 'num_identificacion', 'Numero_historia_clinica')

# @admin.register(PerfilUsuario)
# class PerfilUsuarioAdmin(admin.ModelAdmin):
#     list_display = ('user', 'oficina')
#     search_fields = ('user__username', 'oficina__nombre')