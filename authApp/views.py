from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

def signup(request):
    data = {
        'form': UserCreationForm,
        'nombre': 'Registrarse'
    }

    if request.method == 'POST':
        if request.POST['password1'] != request.POST['password2']:
            data['alert'] = {
                'type': 'error',
                'title': 'Error!',
                'text': 'Las contraseñas no coinciden. Por favor, verifica.'
            }
            return render(request, 'registration/registro.html', data)

        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            data['alert'] = {
                'type': 'success',
                'title': 'Cuenta creada con éxito!',
                'text': 'Te has registrado exitosamente y estás logueado.'
            }
            return redirect('listar_productos')
        except IntegrityError:
            data['alert'] = {
                'type': 'error',
                'title': 'Error!',
                'text': 'Ya existe un usuario con ese nombre.'
            }
            return render(request, 'registration/login.html', data)
    return render(request, 'registration/registro.html', data)

def signin(request):
    data = {
        "form": AuthenticationForm,
        "title": "Iniciar sesión",
        "error": "Usuario o contraseña incorrectos, intente de nuevo."
    }
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            data['alert'] = {
                'type': 'error',
                'title': 'Error!',
                'text': 'Usuario o contraseña incorrectos.'
            }
        else:
            login(request, user)
            return redirect('catalogo')
    return render(request, 'registration/login.html', data)



def cerrarSesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('iniciar_sesion')
