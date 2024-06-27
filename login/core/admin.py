from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'saldo', 'saldo_regalo', 'codigo', 'puntos_pase_pkm', 'puntos_pase_yugioh', 'puntos_pase_magic']
    readonly_fields = ['get_saldo']

    def get_saldo(self, obj):
        return obj.saldo

    get_saldo.short_description = 'Saldo'

admin.site.register(CustomUser, CustomUserAdmin)