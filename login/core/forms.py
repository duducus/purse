from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Producto
from django import forms
from django.utils.crypto import get_random_string  # Para generar una contraseña aleatoria

class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=10, required=False)
    apellidos = forms.CharField(required=False)
    saldo = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, required=False)  # Campo opcional

    class Meta:
        model = CustomUser
        fields = ('username', 'apellidos', 'email', 'telefono', 'saldo')  # No incluimos password1 ni password2

    def save(self, commit=True):
        user = super().save(commit=False)
        # Generar una contraseña por defecto o aleatoria
        default_password = get_random_string(length=12)  # Generar una contraseña aleatoria
        user.set_password(default_password)  # Asignar la contraseña
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'apellidos', 'email', 'telefono', 'password', 'saldo','foto')

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'precio', 'tag']