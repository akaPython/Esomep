from django import forms
from .models import (
    Bien, Cargo, Departamento, Caracteristica, Empleado, RolUsuario,
    Solicitud, SolicitudBien, Usuario, Resguardo
)

class BienForm(forms.ModelForm):
    class Meta:
        model = Bien
        fields = '__all__'
        widgets = {
            'fecha_de_registro': forms.DateInput(attrs={'type': 'date'}),
            'fecha_desincorporacion': forms.DateInput(attrs={'type': 'date'}),
        }

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = Caracteristica
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'fecha_de_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Empleado


class RolUsuarioForm(forms.ModelForm):
    class Meta:
        model = RolUsuario
        fields = '__all__'



class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }



class ResguardoForm(forms.ModelForm):
    class Meta:
        model = Resguardo
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

######################################################################

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['tipo_de_solicitud', 'descripcion_solicitud']

class SolicitudBienForm(forms.ModelForm):
    class Meta:
        model = SolicitudBien
        fields = ['descripcion_bien', 'cantidad']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Empleado, Cargo, Departamento

class EmpleadoRegistroForm(UserCreationForm):
    es_jefe_bienes = forms.BooleanField(required=False)
    cedula = forms.CharField(max_length=20)
    telefono = forms.CharField(max_length=20)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all())
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
    estado = forms.ChoiceField(choices=Empleado.ESTADO_CHOICES)
    fecha_de_ingreso = forms.DateField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'es_jefe_bienes', 'cedula', 'telefono', 'cargo', 'departamento', 'estado', 'fecha_de_ingreso']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Empleado.objects.create(
                user=user,
                es_jefe_bienes=self.cleaned_data.get('es_jefe_bienes', False),
                cedula=self.cleaned_data['cedula'],
                nombres=self.cleaned_data['first_name'],
                apellidos=self.cleaned_data['last_name'],
                cargo=self.cleaned_data['cargo'],
                departamento=self.cleaned_data['departamento'],
                estado=self.cleaned_data['estado'],
                telefono=self.cleaned_data['telefono'],
                fecha_de_ingreso=self.cleaned_data['fecha_de_ingreso']
            )
        return user