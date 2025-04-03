from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Gestor.models import User, Group, Permission
import logging
from datetime import datetime
from django.shortcuts import get_object_or_404

logger = logging.getLogger('django')

# Create your views here.

def get_permissions_from_user(session):
    if 'user_id' in session:
        # Obtener el usuario
        user = User.objects.filter(id=session['user_id']).first()
        if user:
            # Obtener el grupo
            group = Group.objects.filter(id=user.group_id).first()
            if group:
                # Obtener los permisos asociados al grupo
                return group.permissions.all()
    return None

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
        permissions = get_permissions_from_user(request.session)
        return render(request, 'main.html', {'permissions': permissions})
    else:
        return redirect('inicio')

def users_view(request):
    if 'user_id' in request.session:
        permissions = get_permissions_from_user(request.session)
        acceso=False
        for permiso in permissions:
            if permiso.value=='usuarios':
                acceso=True
                break
        if acceso!=True:
            return redirect('inicio')
        return render(request, 'users/index.html', {'permissions': permissions})
    else:
        return redirect('inicio')
    
def users_create_view(request):
    if 'user_id' in request.session:
        permissions = get_permissions_from_user(request.session)
        acceso=False
        for permiso in permissions:
            if permiso.value=='usuarios':
                acceso=True
                break
        if acceso!=True:
            return redirect('inicio')
        return render(request, 'users/create.html', {'permissions': permissions})
    else:
        return redirect('inicio')
    
def users_edit_view(request):
    if 'user_id' in request.session:
        permissions = get_permissions_from_user(request.session)
        acceso=False
        for permiso in permissions:
            if permiso.value=='usuarios':
                acceso=True
                break
        if acceso!=True:
            return redirect('inicio')
        return render(request, 'users/edit.html', {'permissions': permissions})
    else:
        return redirect('inicio')

def group_view(request):
    if 'user_id' in request.session:
        permissions = get_permissions_from_user(request.session)
        acceso=False
        for permiso in permissions:
            if permiso.value=='usuarios':
                acceso=True
                break
        if acceso!=True:
            return redirect('inicio')
        return render(request, 'users/group.html', {'permissions': permissions})
    else:
        return redirect('inicio')
    
def customize_view(request):
    if 'user_id' in request.session:
        permissions = get_permissions_from_user(request.session)
        acceso=False
        for permiso in permissions:
            if permiso.value=='personalizacion':
                acceso=True
                break
        if acceso!=True:
            return redirect('inicio')
        return render(request, 'customize.html', {'permissions': permissions})
    else:
        return redirect('inicio')