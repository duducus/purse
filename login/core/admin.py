from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
from io import TextIOWrapper
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = [
        'username', 'apellidos', 'email', 'telefono', 'saldo', 'saldo_regalo', 'codigo', 
        'puntos_pase_pkm', 'puntos_pase_yugioh', 'puntos_pase_magic', 'puntos_pase_heroclix', 
        'foto', 'pop_ID', 'konami_ID', 'correo_arena'
    ]
    readonly_fields = ['get_saldo', 'foto_display']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'email', 'telefono', 'saldo', 'saldo_regalo', 'foto', 'foto_display', 
                'pop_ID', 'konami_ID', 'correo_arena'
            )
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'apellidos', 'email', 'telefono', 'password1', 'password2', 'saldo', 'pop_ID', 'konami_ID', 'correo_arena'),
        }),
    )

    def foto_display(self, obj):
        if obj.foto:
            return format_html(f'<img src="{obj.foto.url}" width="100" height="100" />')
        return "No image available"

    foto_display.short_description = 'Foto de usuario'

    def get_saldo(self, obj):
        return obj.saldo

    get_saldo.short_description = 'Saldo'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-upload/', self.admin_site.admin_view(self.bulk_upload), name='bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "El archivo debe ser un CSV.")
                return redirect("admin:bulk_upload")

            try:
                data = TextIOWrapper(csv_file.file, encoding='utf-8-sig')
                reader = csv.DictReader(data)
                
                for row in reader:
                    user = CustomUser(
                        username=row['username'],
                        apellidos=row['apellidos'],
                        email=row['email'],
                        telefono=row['telefono'],
                        saldo=row.get('saldo', 0),
                        pop_ID=row.get('pop_ID', ''),
                        konami_ID=row.get('konami_ID', ''),
                        correo_arena=row.get('correo_arena', '')
                    )
                    user.set_password(row['password1'])
                    user.save()
                messages.success(request, "Usuarios importados exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
            return redirect("admin:bulk_upload")

        return render(request, "admin/bulk_upload.html")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = 'admin/core/customuser/bulk-upload/'
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(CustomUser, CustomUserAdmin)
