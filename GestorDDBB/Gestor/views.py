from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Gestor.models import User
import logging
from datetime import datetime
logger = logging.getLogger('django')

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
        username = request.POST['name']
        password = request.POST['password']
        #Intenta autenticar para validar al usuario
        try:
            user = User.objects.get(name=username)
            if user.verify_password(password):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"{current_time} - Inicio de sesión: {user.id}")
                request.session['user_id'] = user.id
                return redirect('main')
            else:
                return redirect('inicio')
        except User.DoesNotExist:
            return redirect('inicio')
        except Exception:
            return redirect('inicio')
    return redirect('inicio')

def logout_view(request):
    request.session.flush()
    return redirect('inicio')

def main_view(request):
    if 'user_id' in request.session:
        return render(request, 'main.html')
    else:
        return redirect('inicio')