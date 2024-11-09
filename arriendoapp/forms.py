from django import forms
from .models import Inmueble, Usuario, Region, Comuna, SolicitudArriendo
from django.contrib.auth.forms import UserCreationForm

# Formulario para crear un inmueble
class InmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.none(), empty_label="Comuna")

    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'banos', 'direccion', 'region', 'comuna', 'tipo_inmueble', 'precio_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()
        
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.region:
            self.fields['comuna'].queryset = self.instance.region.comuna_set.order_by('nombre')
                        
# Formulario para crear un usuario
class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']


# Formulario para editar un usuario
class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'direccion', 'telefono', 'tipo_usuario', 'email']
        
    
class SolicitudArriendoForm(forms.ModelForm):
    class Meta:
        model = SolicitudArriendo
        fields = ['mensaje']