from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Gestor.models import User

# Create your views here.
def login_view(request):
    #Comprueba si el usuario ha iniciado sesion
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return render(request, 'login.html')

def login_controller(request):
    #Comprueba el metodo de envio
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Intenta autenticar para validar al usuario
        try:
            user = User.objects.get(name=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('main')
            else:
                return render(request, 'login.html', {'error': 'Credenciales inválidas'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return redirect('inicio')

@login_required(login_url='/')
def logout_view(request):
    request.session.flush()
    return redirect('inicio')

@login_required(login_url='/')
def main_view(request):
    #Comprueba si el usuario ha iniciado sesion
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect('inicio')
