from django import forms
from .models import RegistroDeArchivo, SerieDocumental, SubserieDocumental
from django.utils.timezone import now
from django.forms import DateInput
from django import forms
from .models import FUID, RegistroDeArchivo
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User  # IMPORTAR User
# from .forms import FichaPacienteForm




class RegistroDeArchivoForm(forms.ModelForm):
    codigo_serie = forms.ModelChoiceField(
        queryset=SerieDocumental.objects.all(),
        empty_label="Seleccione una serie"
    )
    codigo_subserie = forms.ModelChoiceField(
        queryset=SubserieDocumental.objects.none(),
        empty_label="Seleccione una subserie"
    )

    # Hacemos opcionales los campos en el formulario
    caja = forms.CharField(required=False)
    carpeta = forms.CharField(required=False)
    tomo_legajo_libro = forms.CharField(required=False)
    numero_folios = forms.IntegerField(required=False)
    tipo = forms.CharField(required=False)
    cantidad = forms.IntegerField(required=False)
    ubicacion = forms.CharField(required=False)
    cantidad_documentos_electronicos = forms.IntegerField(required=False)
    tamano_documentos_electronicos = forms.CharField(required=False)

    class Meta:
        model = RegistroDeArchivo
        # Excluimos explícitamente el campo 'creado_por'
        exclude = ['creado_por']
        widgets = {
            'fecha_archivo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_inicial': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Si es un nuevo registro
            self.fields['fecha_archivo'].initial = now().date()

        # Configuración dinámica del queryset de subseries
        if 'codigo_serie' in self.data:
            try:
                serie_id = int(self.data.get('codigo_serie'))
                self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.filter(serie_id=serie_id)
            except (ValueError, TypeError):
                self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.none()
        elif self.instance.pk and self.instance.codigo_serie:
            self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.filter(serie_id=self.instance.codigo_serie.id)
        else:
            self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        soporte_fisico = cleaned_data.get('soporte_fisico')
        soporte_electronico = cleaned_data.get('soporte_electronico')

        # Si soporte físico no está seleccionado, asignar valores predeterminados
        if not soporte_fisico:
            cleaned_data['caja'] = "N/A"
            cleaned_data['carpeta'] = "N/A"
            cleaned_data['tomo_legajo_libro'] = "N/A"
            cleaned_data['numero_folios'] = 0
            cleaned_data['tipo'] = "N/A"
            cleaned_data['cantidad'] = 0

        # Si soporte electrónico no está seleccionado, asignar valores predeterminados
        if not soporte_electronico:
            cleaned_data['ubicacion'] = "N/A"
            cleaned_data['cantidad_documentos_electronicos'] = 0
            cleaned_data['tamano_documentos_electronicos'] = "N/A"

        return cleaned_data

class FUIDForm(forms.ModelForm):
    # Campos y configuración del formulario
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Filtrar por Usuario",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_inicio = forms.DateField(
        required=False,
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin = forms.DateField(
        required=False,
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    registros = forms.ModelMultipleChoiceField(
        queryset=RegistroDeArchivo.objects.none(),  
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Registros Asociados"
    )

    elaborado_por_nombre = forms.CharField(
        required=False,
        max_length=255,
        label="Elaborado Por (Nombre)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    elaborado_por_cargo = forms.CharField(
        required=False,
        max_length=255,
        label="Elaborado Por (Cargo)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    elaborado_por_lugar = forms.CharField(
        required=False,
        max_length=255,
        label="Elaborado Por (Lugar)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    elaborado_por_fecha = forms.DateField(
        required=False,
        label="Elaborado Por (Fecha)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    entregado_por_nombre = forms.CharField(
        required=False,
        max_length=255,
        label="Entregado Por (Nombre)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    entregado_por_cargo = forms.CharField(
        required=False,
        max_length=255,
        label="Entregado Por (Cargo)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    entregado_por_lugar = forms.CharField(
        required=False,
        max_length=255,
        label="Entregado Por (Lugar)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    entregado_por_fecha = forms.DateField(
        required=False,
        label="Entregado Por (Fecha)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    recibido_por_nombre = forms.CharField(
        required=False,
        max_length=255,
        label="Recibido Por (Nombre)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    recibido_por_cargo = forms.CharField(
        required=False,
        max_length=255,
        label="Recibido Por (Cargo)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    recibido_por_lugar = forms.CharField(
        required=False,
        max_length=255,
        label="Recibido Por (Lugar)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    recibido_por_fecha = forms.DateField(
        required=False,
        label="Recibido Por (Fecha)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = FUID
        fields = [
            'entidad_productora', 'unidad_administrativa', 'oficina_productora', 'objeto',
            'registros',
            'elaborado_por_nombre', 'elaborado_por_cargo', 'elaborado_por_lugar', 'elaborado_por_fecha',
            'entregado_por_nombre', 'entregado_por_cargo', 'entregado_por_lugar', 'entregado_por_fecha',
            'recibido_por_nombre', 'recibido_por_cargo', 'recibido_por_lugar', 'recibido_por_fecha'
        ]
        widgets = {
            'entidad_productora': forms.Select(attrs={'class': 'form-select'}),
            'unidad_administrativa': forms.Select(attrs={'class': 'form-select'}),
            'oficina_productora': forms.Select(attrs={'class': 'form-select'}),
            'objeto': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Usuario autenticado
        # No es necesario asignar self.instance aquí, ModelForm ya lo hace
        super().__init__(*args, **kwargs)

        # Configura el queryset de registros
        if self.instance and self.instance.pk:
            registros_actuales = self.instance.registros.all()
            registros_disponibles = RegistroDeArchivo.objects.filter(fuids__isnull=True)
            self.fields['registros'].queryset = registros_actuales | registros_disponibles
        else:
            self.fields['registros'].queryset = RegistroDeArchivo.objects.filter(fuids__isnull=True)


    

from django import forms
from .models import FichaPaciente

class FichaPacienteForm(forms.ModelForm):
    class Meta:
        model = FichaPaciente
        fields = '__all__'
        widgets = {
            'primer_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el primer nombre',
                'autofocus': 'autofocus',  # Enfocar este campo automáticamente
            }),
            'segundo_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el segundo nombre (opcional)',
            }),
            'primer_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el primer apellido',
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el segundo apellido (opcional)',
            }),
            'num_identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación único',
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Mostrar un selector de fecha
            }),
            'primer_nombre_padre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el primer nombre del padre',
            }),
            'segundo_nombre_padre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo nombre del padre (opcional)',
            }),
            'primer_apellido_padre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el primer apellido del padre',
            }),
            'segundo_apellido_padre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Segundo apellido del padre (opcional)',
            }),
            'Numero_historia_clinica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de historia clínica único',
            }),
            'caja': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de caja',
            }),
            'carpeta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de carpeta',
            }), 
        }

    def clean_Numero_historia_clinica(self):
        numero_historia_clinica = self.cleaned_data.get('Numero_historia_clinica')
        if FichaPaciente.objects.filter(Numero_historia_clinica=numero_historia_clinica).exists():
            raise forms.ValidationError("El número de historia clínica ya está registrado. Por favor, verifica los datos.")
        return numero_historia_clinica

    def clean_num_identificacion(self):
        num_identificacion = self.cleaned_data.get('num_identificacion')
        if FichaPaciente.objects.filter(num_identificacion=num_identificacion).exists():
            raise forms.ValidationError("El número de identificación ya está registrado. Por favor, verifica los datos.")
        return num_identificacion

        




# hasta aca servia a las 4 `pm martes 10....................................................`
# class RegistroDeArchivoForm(forms.ModelForm):
#     codigo_serie = forms.ModelChoiceField(
#         queryset=SerieDocumental.objects.all(),
#         empty_label="Seleccione una serie"
#     )
#     codigo_subserie = forms.ModelChoiceField(
#         queryset=SubserieDocumental.objects.none(),
#         empty_label="Seleccione una subserie"
#     )

#     class Meta:
#         model = RegistroDeArchivo
#         fields = '__all__'
# .............................................................................................



# from django import forms
# from .models import RegistroDeArchivo, SubserieDocumental, SerieDocumental

# class RegistroDeArchivoForm(forms.ModelForm):
#     class Meta:
#         model = RegistroDeArchivo
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['codigo_serie'].queryset = SerieDocumental.objects.all()
#         self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.none()

#         if 'codigo_serie' in self.data:
#             try:
#                 serie_id = int(self.data.get('codigo_serie'))
#                 self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.filter(serie_id=serie_id)
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['codigo_subserie'].queryset = SubserieDocumental.objects.filter(serie=self.instance.codigo_serie)
