# forms.py
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=10, required=False)
    apellidos = forms.CharField(required=False)
    saldo = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, required=False)  # Campo opcional

    class Meta:
        model = CustomUser
        fields = ('username', 'apellidos', 'email', 'telefono', 'password1', 'password2', 'saldo')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'apellidos', 'email', 'telefono', 'password', 'saldo')
