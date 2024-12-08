from django import forms
from django.forms import inlineformset_factory
from .models import Producto, Talla

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio','imagen', 'cod_proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file',}),
            'cod_proveedor': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'imagen': 'imagen',
            'cod_proveedor': 'Proveedor',     
        }
TallaFormSet = inlineformset_factory(Producto, Talla, fields=('talla', 'cantidad'), extra=1, can_delete=True)

class TallaForm(forms.ModelForm):
    class Meta:
        model = Talla
        fields = ['talla', 'cantidad']