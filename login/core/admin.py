from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['username','apellidos', 'email', 'telefono', 'saldo', 'saldo_regalo', 'codigo', 'puntos_pase_pkm', 'puntos_pase_yugioh', 'puntos_pase_magic', 'puntos_pase_heroclix']
    readonly_fields = ['get_saldo']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'telefono')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','apellidos','email', 'telefono', 'password1', 'password2'),
        }),
    )

    def get_saldo(self, obj):
        return obj.saldo

    get_saldo.short_description = 'Saldo'

admin.site.register(CustomUser, CustomUserAdmin)
