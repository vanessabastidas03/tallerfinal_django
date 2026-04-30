from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        # Excluimos 'promedio' porque se calcula automáticamente
        exclude = ['promedio']
        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Juan Pérez',
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1234567890',
            }),
            'asignatura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Matemáticas',
            }),
            'nota1': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01', 'min': '0', 'max': '5',
            }),
            'nota2': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01', 'min': '0', 'max': '5',
            }),
            'nota3': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01', 'min': '0', 'max': '5',
            }),
        }
        labels = {
            'nombre_estudiante': 'Nombre del Estudiante',
            'identificacion' : 'Identificación',
            'asignatura' : 'Asignatura',
            'nota1' : 'Nota 1',
            'nota2' : 'Nota 2',
            'nota3' : 'Nota 3',
        }
class RegistroForm(forms.Form):
    """Formulario simple de registro de usuario."""
    username = forms.CharField(max_length=150,
widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Contraseña',
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar contraseña',
widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
