# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def home(request):
    saldo = 0
    saldo_regalo = 0
    if request.user.is_authenticated:
        saldo = request.user.saldo
        saldo_regalo = request.user.saldo_regalo
    return render(request, 'core/home.html', {'saldo': saldo, 'saldo_regalo': saldo_regalo})

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
