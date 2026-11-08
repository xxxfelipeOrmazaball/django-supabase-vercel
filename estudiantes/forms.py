from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej. Camila Pérez'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ej. camila@correo.cl'}),
        }
