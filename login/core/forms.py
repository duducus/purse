from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')  # Solo incluir nombre de usuario y contraseñas