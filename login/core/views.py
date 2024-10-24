# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from torneos.models import InscripcionTorneo
from intercambios.models import Intercambio
from django.db.models import Q
from .models import CustomUser, Movimiento
from .forms import CustomUserCreationForm
from barcode import Code128
from barcode.writer import ImageWriter
from django.http import HttpResponse, JsonResponse
import io
from django.db.models import CharField, Value
from django.db.models.functions import Lower
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # Redirigir manualmente al dashboard
    
@login_required
def home(request):
    """
    saldo = request.user.saldo if request.user.is_authenticated else 0
    saldo_regalo = request.user.saldo_regalo if request.user.is_authenticated else 0
    puntos_pase_pkm = request.user.puntos_pase_pkm if request.user.is_authenticated else 0
    puntos_pase_yugioh = request.user.puntos_pase_yugioh if request.user.is_authenticated else 0
    puntos_pase_magic = request.user.puntos_pase_magic if request.user.is_authenticated else 0
    puntos_pase_heroclix = request.user.puntos_pase_heroclix if request.user.is_authenticated else 0
    return render(request, 'core/home.html', {
        'saldo': saldo,
        'saldo_regalo': saldo_regalo,
        'puntos_pase_pkm': puntos_pase_pkm,
        'puntos_pase_yugioh' : puntos_pase_yugioh,
        'puntos_pase_magic': puntos_pase_magic,
        'puntos_pase_heroclix': puntos_pase_heroclix
    })
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirige al dashboard si el usuario está autenticado
    return render(request, 'core/home.html')
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
                'posicion': inscripcion.posicion,
                'juego' : inscripcion.torneo.juego
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

    premios_normales_heroclix = [
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', 
        '', '', '', '', '', '', '', '', '', ''
    ]
    premios_premium_heroclix = [
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
        'premios_normales_heroclix': premios_normales_heroclix,
        'premios_premium_heroclix': premios_premium_heroclix,
        'puntos_pase_pkm': request.user.puntos_pase_pkm,
        'puntos_pase_yugioh': request.user.puntos_pase_yugioh,
        'puntos_pase_magic': request.user.puntos_pase_magic,
        'puntos_pase_heroclix': request.user.puntos_pase_heroclix
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
            user = form.save()  # Aquí guardamos el formulario y obtenemos el usuario recién creado
            codigo = user.codigo  # Accedemos al código del usuario recién creado
            return redirect(f'/usuarios/search/?codigo={codigo}')  # Redirige al dashboard u otra vista después de crear el usuario
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/create_user.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def users_list(request):
    usuarios = CustomUser.objects.annotate(
        username_lower=Lower('username')
    ).order_by('username_lower')
    return render(request, 'core/users_list.html', {'usuarios': usuarios})

def generate_barcode(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    barcode_number = user.codigo
    barcode = Code128(barcode_number, writer=ImageWriter())
    
    buffer = io.BytesIO()
    barcode.write(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    return response

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def manage_points(request):
    if request.method == 'POST':
        codigo_usuario = request.POST.get('codigo_usuario')
        puntos_pokemon = int(request.POST.get('puntos_pokemon', 0))
        puntos_yugioh = int(request.POST.get('puntos_yugioh', 0))
        puntos_magic = int(request.POST.get('puntos_magic', 0))
        puntos_heroclix = int(request.POST.get('puntos_heroclix', 0))
        concepto = request.POST.get('concepto', '')

        try:
            user = CustomUser.objects.get(codigo=codigo_usuario)
        except CustomUser.DoesNotExist:
           
            return redirect('manage_points')

        # Actualizar puntos del usuario
        user.puntos_pase_pkm = max(user.puntos_pase_pkm + puntos_pokemon, 0)
        user.puntos_pase_yugioh = max(user.puntos_pase_yugioh + puntos_yugioh, 0)
        user.puntos_pase_magic = max(user.puntos_pase_magic + puntos_magic, 0)
        user.puntos_pase_heroclix = max(user.puntos_pase_heroclix + puntos_heroclix, 0)
        user.save()

        # Registrar movimiento
        Movimiento.objects.create(
            user=user,
            puntos_pokemon=puntos_pokemon,
            puntos_yugioh=puntos_yugioh,
            puntos_magic=puntos_magic,
            puntos_heroclix=puntos_heroclix,
            concepto=concepto
        )
        return redirect('movimientos_list')

    return render(request, 'core/manage_points.html')

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def movimientos_list(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'core/movimientos_list.html', {'movimientos': movimientos})

@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/unauthorized/')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')  # Redirige a la vista de la lista de usuarios
    return redirect('users_list')  # Redirige a la vista de la lista de usuarios si el método no es POST

def search_users(request):
    query = request.GET.get('codigo', '').strip()  # Obtener el código y eliminar espacios en blanco

    if query:  # Si hay un valor en la búsqueda
        try:
            # Búsqueda por código exacto o por coincidencia parcial en el nombre de usuario
            usuarios = CustomUser.objects.filter(
                Q(codigo=query) | Q(username__icontains=query)
            )
            no_results = not usuarios.exists()  # Establece no_results si no hay usuarios
        except ValueError:
            usuarios = CustomUser.objects.none()  # No hay resultados
            no_results = True
    else:
        # Cuando la consulta está vacía, recargamos la página sin filtrar
        usuarios = CustomUser.objects.all()  # Muestra todos los usuarios
        no_results = False  # No hay error, solo mostramos la lista completa

    return render(request, 'core/users_list.html', {'usuarios': usuarios, 'no_results': no_results})

def buscar_usuario(request):
    codigo = request.GET.get('codigo')
    if codigo:
        try:
            usuario = CustomUser.objects.get(codigo=codigo)
            return JsonResponse({'nombre': usuario.username})
        except CustomUser.DoesNotExist:
            return JsonResponse({'nombre': None})
    return JsonResponse({'nombre': None})