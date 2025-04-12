from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Gestor.models import User, Group, Permission, CustomStyle
import logging
from datetime import datetime
from django.shortcuts import get_object_or_404
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile

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
        users = User.objects.all()
        groups = Group.objects.all()
        permissions=Permission.objects.all().order_by('order')
        return render(request, 'users/index.html', {'permissions': permissions, 'users': users, 'groups': groups, 'permissions': permissions})
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
        custom = CustomStyle.objects.first()
        return render(request, 'customize.html', {'permissions': permissions, 'custom': {
                'company_name': custom.company_name if custom and custom.company_name else '',
                'email': custom.email if custom and custom.email else '',
                'telephone': custom.telephone if custom and custom.telephone else '',
                'text_size': custom.text_size if custom and custom.text_size else '',
                'text_color': custom.text_color if custom and custom.text_color else '#000000',
                'main_color': custom.main_color if custom and custom.main_color else '#000000',
                'secondary_color': custom.secondary_color if custom and custom.secondary_color else '#000000',
                'other_code': custom.other_code if custom and custom.other_code else '',
            },})
    else:
        return redirect('inicio')
    
def customize_process(request):
    if request.method == 'POST':
        try:
            if 'user_id' in request.session:
                permissions = get_permissions_from_user(request.session)
                acceso = False
                for permiso in permissions:
                    if permiso.value == 'personalizacion':
                        acceso = True
                        break
                if acceso != True:
                    return redirect('inicio')
                
                custom = CustomStyle.objects.first()
                imagen_file = request.FILES.get('imagen')
                imagen_base64 = None
                # Procesamiento del archivo de imagen en base64
                if imagen_file:
                    try:
                        imagen_base64 = base64.b64encode(imagen_file.read()).decode('utf-8')
                    except Exception as e:
                        logger.error(f"Error al procesar la imagen: {str(e)}")
                        imagen_base64 = ""
                if custom is None:
                    # No existe el registro, se crea uno nuevo
                    custom = CustomStyle(
                        main_color=request.POST.get('main_color'),
                        secondary_color=request.POST.get('secondary_color'),
                        text_color=request.POST.get('text_color'),
                        text_size=request.POST.get('text_size'),
                        company_name=request.POST.get('company_name'),
                        email=request.POST.get('email'),
                        telephone=request.POST.get('telephone'),
                        other_code=request.POST.get('other_code'),
                        imagen=imagen_base64
                    )
                    custom.save()
                else:
                    # Existe el registro, luego se actualiza
                    if imagen_base64!="":
                        custom.imagen = imagen_base64
                    custom.main_color = request.POST.get('main_color')
                    custom.secondary_color = request.POST.get('secondary_color')
                    custom.text_color = request.POST.get('text_color')
                    custom.text_size = request.POST.get('text_size')
                    custom.company_name = request.POST.get('company_name')
                    custom.email = request.POST.get('email')
                    custom.telephone = request.POST.get('telephone')
                    custom.other_code = request.POST.get('other_code')
                    custom.save()
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"{current_time} - Personalización: {request.session['user_id']}")
                return redirect('customize')
        except Exception as e:
            logger.error(f"Error en customize_process: {str(e)}")
            return redirect('customize')
    else:
        return redirect('inicio')

def create_user(request):
    if request.method == 'POST':
        try:
            if 'user_id' in request.session:
                permissions = get_permissions_from_user(request.session)
                acceso = False
                for permiso in permissions:
                    if permiso.value == 'usuarios':
                        acceso = True
                        break
                if acceso != True:
                    return redirect('inicio')
                if request.POST.get('id')=='new':
                    #Se tiene que crear al usuario
                    user=User(
                        name=request.POST.get('name'),
                        email=request.POST.get('email'),
                        real_name=request.POST.get('real_name'),
                        password=request.POST.get('password'),
                        group=Group.objects.get(id=request.POST.get('group'))
                    )
                    user.save()
                else:
                    #Se tiene que actualizar al usuario
                    user=User.objects.get(id=request.POST.get('id'))
                    user.name=request.POST.get('name')
                    user.email=request.POST.get('email')
                    user.real_name=request.POST.get('real_name')
                    user.group=Group.objects.get(id=request.POST.get('group'))
                    user.save()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en create_user: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def change_password(request):
    if request.method == 'POST':
        try:
            if 'user_id' in request.session:
                permissions = get_permissions_from_user(request.session)
                acceso = False
                for permiso in permissions:
                    if permiso.value == 'usuarios':
                        acceso = True
                        break
                if acceso != True:
                    return redirect('inicio')
                #Se tiene que actualizar al usuario
                user=User.objects.get(id=request.POST.get('cambio_id'))
                user.password=request.POST.get('cambio_password')
                user.save()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en change_password: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def delete_user(request):
    if request.method == 'POST':
        try:
            if 'user_id' in request.session:
                permissions = get_permissions_from_user(request.session)
                acceso = False
                for permiso in permissions:
                    if permiso.value == 'usuarios':
                        acceso = True
                        break
                if acceso != True:
                    return redirect('inicio')
                user=User.objects.get(id=request.POST.get('borrar_id'))
                user.delete()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en delete_user: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def create_permission(request):
    if request.method == 'POST':
        try:
            permissions = get_permissions_from_user(request.session)
            acceso = False
            user = User.objects.filter(id=request.session['user_id']).first()
            for permiso in permissions:
                if permiso.value == 'usuarios':
                    acceso = True
                    break
            if acceso != True:
                return redirect('inicio')
            if request.POST.get('permission_id')=='new':
                #Se tiene que crear
                permission=Permission(
                    name=request.POST.get('permission_name'),
                    value=request.POST.get('permission_value'),
                    order=request.POST.get('permission_order')
                    )
                permission.save()
            else:
                #Se tiene que actualizar
                permission=Permission.objects.get(id=request.POST.get('permission_id'))
                permission.name=request.POST.get('permission_name')
                permission.value=request.POST.get('permission_value')
                permission.order=request.POST.get('permission_order')
                permission.save()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en create_permission: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def delete_permission(request):
    if request.method == 'POST':
        try:
            permissions = get_permissions_from_user(request.session)
            acceso = False
            for permiso in permissions:
                if permiso.value == 'usuarios':
                    acceso = True
                    break
            if acceso != True:
                return redirect('inicio')
            permission=Permission.objects.get(id=request.POST.get('permission_borrar_id'))
            permission.delete()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en delete_permission: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def delete_group(request):
    if request.method == 'POST':
        try:
            permissions = get_permissions_from_user(request.session)
            acceso = False
            for permiso in permissions:
                if permiso.value == 'usuarios':
                    acceso = True
                    break
            if acceso != True:
                return redirect('inicio')
            group=Group.objects.get(id=request.POST.get('group_borrar_id'))
            group.delete()
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en delete_group: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')

def create_group(request):
    if request.method == 'POST':
        try:
            permissions = get_permissions_from_user(request.session)
            acceso = False
            for permiso in permissions:
                if permiso.value == 'usuarios':
                    acceso = True
                    break
            if acceso != True:
                return redirect('inicio')
            if request.POST.get('group_id')=='new':
                group=Group(
                    desc_group=request.POST.get('group_name')
                )
                group.save()
            else:
                group=Group.objects.get(id=request.POST.get('group_id'))
                group.desc_group=request.POST.get('group_name')
                group.save()
            permission_ids = request.POST.getlist('permissions')
            group.permissions.clear()
            for perm_id in permission_ids:
                try:
                    permission = Permission.objects.get(id=perm_id)
                    group.permissions.add(permission)  # Asignar permisos
                except Permission.DoesNotExist:
                    continue
            return redirect('users')
        except Exception as e:
            logger.error(f"Error en create_group: {str(e)}")
            return redirect('users')
    else:
        return redirect('users')