# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import logout
from torneos.models import InscripcionTorneo
from intercambios.models import Intercambio
from django.db.models import Sum
from .models import CustomUser, Movimiento
from .forms import CustomUserCreationForm
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    saldo = request.user.saldo if request.user.is_authenticated else 0
    saldo_regalo = request.user.saldo_regalo if request.user.is_authenticated else 0
    puntos_pase_pkm = request.user.puntos_pase_pkm if request.user.is_authenticated else 0
    puntos_pase_yugioh = request.user.puntos_pase_yugioh if request.user.is_authenticated else 0
    puntos_pase_magic = request.user.puntos_pase_magic if request.user.is_authenticated else 0
    return render(request, 'core/home.html', {
        'saldo': saldo,
        'saldo_regalo': saldo_regalo,
        'puntos_pase_pkm': puntos_pase_pkm,
        'puntos_pase_yugioh' : puntos_pase_yugioh,
        'puntos_pase_magic': puntos_pase_magic
    })

@login_required
def informacion(request):
    torneos_usuario = []
    intercambios_usuario = []

    if request.user.is_authenticated:
        inscripciones = InscripcionTorneo.objects.filter(jugador=request.user)
        for inscripcion in inscripciones:
            torneos_usuario.append({
                'nombre': inscripcion.torneo.nombre,
                'entrada': inscripcion.entrada,
                'premio': inscripcion.premio,
                'posicion': inscripcion.posicion
            })

        intercambios = Intercambio.objects.filter(usuario=request.user)
        for intercambio in intercambios:
            intercambios_usuario.append({
                'articulo': intercambio.articulo,
                'monto': intercambio.monto
            })

    return render(request, 'core/informacion.html', {
        'torneos_usuario': torneos_usuario,
        'intercambios_usuario': intercambios_usuario
    })

@login_required
def pase_batalla(request):
    puntos_rango = [(i, i + 10) for i in range(10, 501, 10)]

    premios_normales_pkm = [
        'Pistola Evolucionadora', '', 'Pokochos', '', '', '', '', '', '', 'Paquete de fichas', 
        '', '', '', 'Super Rod', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', 'Playera de la tienda',
        '', '', '', '', '', '', '', '', 'Pistola evolucionadora', '', 
        'Paquete de dados chicos', '', '', '', '', 'Pokochos', '', 'Super Rod', '', 'Dados especiales'
    ]
    
    premios_premium_pkm = [
        'Paquete de micas', 'Super Rod', '', 'Stickers', '', '', 'Paquete de dados chicos', 'Pikachu Liga', '', '', 
        '', 'Booster Pack', '', '', '', 'Pokochos', '', 'Pistola Evolucionadora', '', 'Lata con inserto', 
        '', '', '', 'Stickers', 'Booster Pack', '', '', '', '', 'Playera de la tienda', 
        '', 'Pikachu Liga', '', '', '', '', 'Booster Pack', 'Pikachu Premio', '', '', 
        'Pokochos', 'Pistola Evolucionadora', '', 'Super Rod', 'Pikachu Premio', '', '', '', 'ETB', 'Dados especiales'
    ]

    premios_normales_yugioh = [
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', ''
    ]
    premios_premium_yugioh = [
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', ''
    ]
    
    premios_normales_magic = [
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', ''
    ]
    premios_premium_magic = [
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', ''
    ]

    return render(request, 'core/pase_batalla.html', {
        'puntos_rango': puntos_rango,
        'premios_normales_pkm': premios_normales_pkm,
        'premios_premium_pkm': premios_premium_pkm,
        'premios_normales_yugioh': premios_normales_yugioh,
        'premios_premium_yugioh': premios_premium_yugioh,
        'premios_normales_magic': premios_normales_magic,
        'premios_premium_magic': premios_premium_magic,
        'puntos_pase_pkm': request.user.puntos_pase_pkm,
        'puntos_pase_yugioh': request.user.puntos_pase_yugioh,
        'puntos_pase_magic': request.user.puntos_pase_magic
    })
def products(request):
    user_authenticated = request.user.is_authenticated
    context = {'user_authenticated': user_authenticated}
    if user_authenticated:
        # Agrega cualquier dato específico para usuarios autenticados aquí
        pass
    return render(request, 'core/products.html', context)

def exit(request):
    logout(request)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirige al dashboard u otra vista después de crear el usuario
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/create_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def users_list(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'core/users_list.html', {'usuarios': usuarios})

def generate_qr(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    saldo_info = f"Usuario: {user.username}\nSaldo: {user.saldo}"
    qr = qrcode.make(saldo_info)
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def manage_points(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        puntos_pokemon = int(request.POST.get('puntos_pokemon', 0))
        puntos_yugioh = int(request.POST.get('puntos_yugioh', 0))
        puntos_magic = int(request.POST.get('puntos_magic', 0))
        concepto = request.POST.get('concepto', '')

        user = CustomUser.objects.get(id=user_id)

        user.puntos_pase_pkm = max(user.puntos_pase_pkm + puntos_pokemon, 0)
        user.puntos_pase_yugioh = max(user.puntos_pase_yugioh + puntos_yugioh, 0)
        user.puntos_pase_magic = max(user.puntos_pase_magic + puntos_magic, 0)
        user.save()

        Movimiento.objects.create(
            user=user,
            puntos_pokemon=puntos_pokemon,
            puntos_yugioh=puntos_yugioh,
            puntos_magic=puntos_magic,
            concepto=concepto
        )

        return redirect('manage_points')

    return render(request, 'core/manage_points.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def movimientos_list(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'core/movimientos_list.html', {'movimientos': movimientos})