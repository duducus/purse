from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=10, required=False)
    apellidos = forms.CharField(required= False)
    class Meta:
        model = CustomUser
        fields = ('username','apellidos','email', 'telefono', 'password1', 'password2')  # Incluir los campos deseados

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username','apellidos', 'email', 'telefono', 'password')  # Puedes ajustar los campos según tus necesidades
