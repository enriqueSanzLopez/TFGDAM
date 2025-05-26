from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from Gestor.models import User, Group, Permission, CustomStyle, Connection, Enumerate, Value
import logging
from datetime import datetime
from django.shortcuts import get_object_or_404
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import json
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db import connections, OperationalError, DEFAULT_DB_ALIAS
from django.conf import settings
from babel import Locale, negotiate_locale
from django.utils.translation import get_language
from babel.support import Translations
import re
import pymongo
from django.db.utils import ConnectionDoesNotExist
from django.db.utils import ConnectionHandler
from pymongo import MongoClient

logger = logging.getLogger('django')

translations = Translations.load('translations', locales=['es'])
translations.install()
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
    lang = request.COOKIES.get('lang', 'es')
    translations = Translations.load('translations', locales=[lang])
    translations.install()
    logger.info('Lenguaje: '+lang)
    if request.user.is_authenticated:
        return redirect('main')
    else:
        customStyle=CustomStyle.objects.first()
        other_code=''
        if customStyle is None:
            ''
        else:
            other_code=customStyle.other_code
        contexto = {
            "iniciar_sesion": translations.gettext("iniciar_sesion"),
            "usuario": translations.gettext("usuario"),
            "password": translations.gettext("password"),
            "other_code": other_code
        }
        return render(request, 'login.html', contexto)

@csrf_protect
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
        lang = request.COOKIES.get('lang', 'es')
        translations = Translations.load('translations', locales=[lang])
        translations.install()
        permissions = get_permissions_from_user(request.session)
        connectionsName=Enumerate.objects.get(name="Tipos de Conexión")
        connections=Value.objects.filter(enumerate=connectionsName).order_by('order')
        inicio=translations.gettext("inicio")
        personalizacion=translations.gettext("personalizacion")
        usuarios=translations.gettext("usuarios")
        logout=translations.gettext("logout")
        ddbb=translations.gettext("data_base")
        port=translations.gettext("puerto")
        password=translations.gettext("password")
        saveConnection=translations.gettext("save_connection")
        cancelar=translations.gettext("cancelar")
        usuario=translations.gettext("usuario")
        customStyle=CustomStyle.objects.first()
        other_code=''
        if customStyle is None:
            ''
        else:
            other_code=customStyle.other_code
        return render(request, 'main.html', {'permissions': permissions,
                                             'user_id': request.session.get('user_id'),
                                             'connections': connections,
                                             'nav_inicio': inicio,
                                             'nav_personalizacion': personalizacion,
                                             'nav_usuarios': usuarios,
                                             'nav_logout': logout,
                                             'usuario': usuario,
                                             'ddbb': ddbb,
                                             'port': port,
                                             'password': password,
                                             'saveConnection': saveConnection,
                                             'cancelar': cancelar,
                                             'other_code': other_code})
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
        lang = request.COOKIES.get('lang', 'es')
        translations = Translations.load('translations', locales=[lang])
        translations.install()
        users = User.objects.all()
        groups = Group.objects.all()
        permissions=Permission.objects.all().order_by('order')
        inicio=translations.gettext("inicio")
        personalizacion=translations.gettext("personalizacion")
        usuarios=translations.gettext("usuarios")
        logout=translations.gettext("logout")
        grupos=translations.gettext("grupos")
        grupo=translations.gettext("grupo")
        permisos=translations.gettext("permisos")
        crearUsuario=translations.gettext('crear_usuario')
        crearGrupo=translations.gettext('crear_grupo')
        usuario=translations.gettext("usuario")
        realName=translations.gettext('real_name')
        nombre=translations.gettext('nombre')
        crearPermiso=translations.gettext('crear_permiso')
        valor=translations.gettext('valor')
        orden=translations.gettext('orden')
        deletePhrase=translations.gettext('delete_phrase')
        delete=translations.gettext('delete')
        cancelar=translations.gettext("cancelar")
        changePassword=translations.gettext('change_password')
        password=translations.gettext('password')
        guardarCambios=translations.gettext('save_changes')
        repeatPassword=translations.gettext('repeat_password')
        groupName=translations.gettext('group_name')
        groupDeleteMessage=translations.gettext('group_delete_message')
        permissionName=translations.gettext('permission_name')
        permissionValue=translations.gettext('permission_value')
        customStyle=CustomStyle.objects.first()
        other_code=''
        if customStyle is None:
            ''
        else:
            other_code=customStyle.other_code
        return render(request, 'users/index.html',
                      {'permissions': permissions,
                        'users': users,
                        'groups': groups,
                        'permissions': permissions,
                        'nav_inicio': inicio,
                        'nav_personalizacion': personalizacion,
                        'nav_usuarios': usuarios,
                        'nav_logout': logout,
                        'grupos': grupos,
                        'permisos': permisos,
                        'crearUsuario': crearUsuario,
                        'usuario': usuario,
                        'realName': realName, 
                        'grupo': grupo,
                        'crearGrupo': crearGrupo,
                        'nombre': nombre,
                        'crearPermiso': crearPermiso,
                        'valor': valor,
                        'orden': orden,
                        'deletePhrase': deletePhrase,
                        'delete': delete,
                        'cancelar': cancelar,
                        'changePassword': changePassword,
                        'password': password,
                        'guardarCambios': guardarCambios,
                        'repeatPassword': repeatPassword,
                        'groupName': groupName,
                        'groupDeleteMessage': groupDeleteMessage,
                        'permissionName': permissionName,
                        'permissionValue': permissionValue,
                        'other_code': other_code})
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
        lang = request.COOKIES.get('lang', 'es')
        translations = Translations.load('translations', locales=[lang])
        translations.install()
        custom = CustomStyle.objects.first()
        inicio=translations.gettext("inicio")
        personalizacion=translations.gettext("personalizacion")
        usuarios=translations.gettext("usuarios")
        logout=translations.gettext("logout")
        additionalCSS=translations.gettext("additional_CSS")
        customizeCSS=translations.gettext("customize")
        saveChanges=translations.gettext("save_changes")
        customStyle=CustomStyle.objects.first()
        other_code=''
        if customStyle is None:
            ''
        else:
            other_code=customStyle.other_code
        return render(request, 'customize.html', {'permissions': permissions, 'custom': {
                'company_name': custom.company_name if custom and custom.company_name else '',
                'email': custom.email if custom and custom.email else '',
                'telephone': custom.telephone if custom and custom.telephone else '',
                'text_size': custom.text_size if custom and custom.text_size else '',
                'text_color': custom.text_color if custom and custom.text_color else '#000000',
                'main_color': custom.main_color if custom and custom.main_color else '#000000',
                'secondary_color': custom.secondary_color if custom and custom.secondary_color else '#000000',
                'other_code': custom.other_code if custom and custom.other_code else '',
            },
            'nav_inicio': inicio, 'nav_personalizacion': personalizacion, 'nav_usuarios': usuarios, 'nav_logout': logout, 'additionalCSS': additionalCSS, 'customizeCSS': customizeCSS, 'saveChanges': saveChanges,
            'other_code': other_code})
    else:
        return redirect('inicio')

@csrf_protect    
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

@csrf_protect
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

@csrf_protect
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

@csrf_protect
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

@csrf_protect
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

@csrf_protect
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

@csrf_protect
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

@csrf_protect
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
    
#Metodos de API
def get_csrf(request):
    try:
        return JsonResponse({
                'status': 'success',
                'message': 'Token recuperado',
                'token': get_token(request)
            })
    except Exception as e:
        return JsonResponse({
                'status': 'error',
                'message': str(e)
                })

# def get_temp_connection(db_config):
#     return ConnectionHandler({'default': db_config})['default']


def get_temp_connection(db_config):
    # Detectamos si es MongoDB para manejar distinto
    if db_config['ENGINE'].lower() in ('pymongo', 'mongodb'):
        # Crear cliente pymongo usando datos del config
        host = db_config.get('HOST', 'localhost')
        port = int(db_config.get('PORT', 27017))
        user = db_config.get('USER')
        password = db_config.get('PASSWORD')
        dbname = db_config.get('NAME')
        
        # Construir argumentos de conexion segun si hay usuario y password
        if user and password:
            # URI con autenticacion
            mongo_uri = f"mongodb://{user}:{password}@{host}:{port}/{dbname}"
            client = MongoClient(mongo_uri)
        else:
            client = MongoClient(host=host, port=port)
        
        return TempConnectionMongo(client)
    
    # Para bases SQL, usar la conexion estandar de Django
    return ConnectionHandler({'default': db_config})['default']


class TempConnectionMongo:
    def __init__(self, client):
        # simulamos atributo connection.client para mantener la compatibilidad
        self.connection = type('obj', (), {'client': client})()
    def close(self):
        self.connection.client.close()

@csrf_protect
def test_connection(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            engine = body.get('db_engine', '').strip().lower()
            if not isinstance(engine, str):
                return JsonResponse({'status': 'error', 'message': 'ENGINE debe ser una cadena de texto'})

            db_config = {
                'ENGINE': engine,
                'NAME': body.get('db_name'),
                'USER': body.get('name'),
                'PASSWORD': body.get('password'),
                'HOST': body.get('host'),
                'PORT': body.get('port'),
                'OPTIONS': {},
                'TIME_ZONE': settings.TIME_ZONE,
                'CONN_HEALTH_CHECKS': True,
                'CONN_MAX_AGE': 60,
                'AUTOCOMMIT': True,
                'ATOMIC_REQUESTS': True,
            }

            temp_connection = get_temp_connection(db_config)
            try:
                with temp_connection.cursor() as cursor:
                    cursor.execute('SELECT 1')
            finally:
                temp_connection.close()

            user = User.objects.filter(id=body.get('user')).first()
            connection_instance = Connection(
                user=user,
                db_type=engine,
                host=body.get('host'),
                db_name=body.get('db_name'),
                port=body.get('port'),
                name=body.get('name'),
                password=body.get('password')
            )
            connection_instance.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Conexión exitosa',
                'token': connection_instance.token
            })
        except OperationalError as e:
            logger.info('Error: '+str(e))
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@csrf_protect
def list_connections(request):
    if request.method=='POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(id=body.get('user')).first()
            connections = Connection.objects.filter(user=user)
            conexiones_serializadas = list(connections.values())
            decrypted_connections = [conn.get_connections_front() for conn in connections]
            return JsonResponse({
                'status': 'success',
                'conexiones': decrypted_connections
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
                })
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@csrf_protect
def delete_connection(request):
    if request.method=='POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(id=body.get('user')).first()
            connection=Connection.objects.filter(id=body.get('id')).filter(user=user).first()
            if connection:
                connection.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Conexión borrada'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
                })

    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@csrf_protect
def list_tables(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
    
    try:
        body = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(id=body.get('user')).first()
        if not user:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado.'}, status=404)
        
        connections_list = Connection.objects.filter(user=user)
        tables_list = []

        for connection in connections_list:
            try:
                decrypted_data = connection.decrypt_data()
                db_type = decrypted_data["db_type"].strip().lower()

                db_config = {
                    'ENGINE': db_type,
                    'NAME': decrypted_data["db_name"],
                    'USER': decrypted_data.get("name"),
                    'PASSWORD': decrypted_data.get("password"),
                    'HOST': decrypted_data.get("host"),
                    'PORT': connection.port,
                    'OPTIONS': {},
                    'TIME_ZONE': settings.TIME_ZONE,
                    'CONN_HEALTH_CHECKS': True,
                    'CONN_MAX_AGE': 60,
                    'AUTOCOMMIT': True,
                    'ATOMIC_REQUESTS': False,
                }

                temp_connection = get_temp_connection(db_config)

                if db_type == 'django.db.backends.postgresql':
                    consulta = """
                        SELECT schemaname || '.' || tablename AS table_name
                        FROM pg_catalog.pg_tables
                        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                        ORDER BY table_name
                    """
                    with temp_connection.cursor() as cursor:
                        cursor.execute(consulta)
                        tables = cursor.fetchall()

                elif db_type == 'django.db.backends.mysql':
                    consulta = """
                        SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME) AS table_name
                        FROM information_schema.tables
                        WHERE TABLE_TYPE = 'BASE TABLE'
                        ORDER BY table_name
                    """
                    with temp_connection.cursor() as cursor:
                        cursor.execute(consulta)
                        tables = cursor.fetchall()

                elif db_type in ('mssql', 'django.db.backends.mssql'):
                    consulta = """
                        SELECT TABLE_SCHEMA + '.' + TABLE_NAME AS table_name
                        FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_TYPE = 'BASE TABLE'
                        ORDER BY table_name
                    """
                    with temp_connection.cursor() as cursor:
                        cursor.execute(consulta)
                        tables = cursor.fetchall()

                elif db_type == 'django.db.backends.sqlite3':
                    consulta = """
                        SELECT name AS table_name
                        FROM sqlite_master
                        WHERE type='table'
                        ORDER BY name
                    """
                    with temp_connection.cursor() as cursor:
                        cursor.execute(consulta)
                        tables = cursor.fetchall()

                elif db_type in ('pymongo', 'mongodb'):
                    client = temp_connection.connection.client
                    db = client[decrypted_data["db_name"]]
                    collection_names = db.list_collection_names()
                    tables = [(name,) for name in collection_names]

                else:
                    logger.warning(f'Base de datos no soportada: {db_type}')
                    tables = []

                for table in tables:
                    tables_list.append({
                        "id_conexion": connection.id,
                        "nombre_tabla": table[0]
                    })

                temp_connection.close()

            except Exception as e1:
                logger.error(f"Error en la conexión {connection.id}: {e1}")
                continue

        return JsonResponse({
            'status': 'success',
            'tables': tables_list,
        })

    except Exception as e:
        logger.exception("Error general en list_tables")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@csrf_protect
def view_edit_permission(request):
    if request.method=='POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(id=body.get('user')).first()
            #Conseguir los permisos del usuario
            edicion=False
            for permiso in user.group.permissions.all():
                if permiso.value == 'edicion':
                    edicion = True
                    break
            return JsonResponse({
                'status': 'success',
                'edicion': edicion
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
                })
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
    
@csrf_protect
def query_table(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(id=body.get('user')).first()
            connection = Connection.objects.filter(id=body.get('connection_id'), user=user).first()
            if not connection:
                return JsonResponse({'status': 'error', 'message': 'Conexión no encontrada'})
            table_name = body.get('table')
            columns = body.get('columns', '*')
            filters = body.get('filters', '')
            ordering = body.get('ordering', '')

            if not isinstance(table_name, str) or not re.match(r'^[\w\.\"]+$', table_name):
                return JsonResponse({'status': 'error', 'message': 'Nombre de tabla inválido'})

            if columns != '*' and not re.match(r'^[\w\,\s]+$', columns):
                return JsonResponse({'status': 'error', 'message': 'Columnas inválidas'})

            decrypted_data = connection.decrypt_data()
            db_type = decrypted_data["db_type"].strip().lower()

            db_config = {
                'ENGINE': db_type,
                'NAME': decrypted_data["db_name"],
                'USER': decrypted_data.get("name"),
                'PASSWORD': decrypted_data.get("password"),
                'HOST': decrypted_data.get("host"),
                'PORT': connection.port,
                'OPTIONS': {},
                'TIME_ZONE': settings.TIME_ZONE,
                'CONN_HEALTH_CHECKS': True,
                'CONN_MAX_AGE': 60,
                'AUTOCOMMIT': True,
                'ATOMIC_REQUESTS': True,
            }

            temp_connection = get_temp_connection(db_config)

            if db_type in ('pymongo', 'mongodb'):
                try:
                    db = temp_connection.connection.client[decrypted_data["db_name"]]
                    collection = db[table_name]
                    mongo_filters = json.loads(filters) if filters else {}
                    projection = {col.strip(): 1 for col in columns.split(',')} if columns != '*' else None
                    sort_fields = json.loads(ordering) if ordering else None
                    cursor = collection.find(mongo_filters, projection)
                    if sort_fields:
                        cursor = cursor.sort(sort_fields)
                    results = list(cursor)
                    for doc in results:
                        doc['_id'] = str(doc['_id'])

                    return JsonResponse({
                        'status': 'success',
                        'data': results
                    })
                finally:
                    temp_connection.close()

            else:
                if '.' in table_name:
                    schema, table = table_name.split('.', 1)
                    if db_type == 'django.db.backends.mysql':
                        safe_table_name = f'`{schema.replace("`", "``")}`.`{table.replace("`", "``")}`'
                    else:
                        escaped_schema = schema.replace('"', '""')
                        escaped_table = table.replace('"', '""')
                        safe_table_name = f'"{escaped_schema}"."{escaped_table}"'
                else:
                    if db_type == 'django.db.backends.mysql':
                        safe_table_name = f'`{table_name.replace("`", "``")}`'
                    else:
                        escaped_table = table_name.replace('"', '""')
                        safe_table_name = f'"{escaped_table}"'

                query = f"SELECT {columns} FROM {safe_table_name}"
                if filters:
                    query += f" WHERE {filters}"
                if ordering:
                    query += f" ORDER BY {ordering}"

                results = []
                with temp_connection.cursor() as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    col_names = [desc[0] for desc in cursor.description]
                    for row in rows:
                        results.append(dict(zip(col_names, row)))

                temp_connection.close()

                return JsonResponse({
                    'status': 'success',
                    'data': results
                })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@csrf_protect
def console_api(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(id=body.get('user')).first()
            connection = Connection.objects.filter(id=body.get('connection_id'), user=user).first()

            edicion = any(perm.value == 'edicion' for perm in user.group.permissions.all())
            if not edicion:
                return JsonResponse({'status': 'error', 'message': 'No tienes los permisos adecuados.'}, status=405)

            query = body.get('query', '').strip()
            if not query:
                return JsonResponse({'status': 'error', 'message': 'No se recibió una consulta.'})

            decrypted_data = connection.decrypt_data()
            db_type = decrypted_data["db_type"].strip().lower()

            db_config = {
                'ENGINE': db_type,
                'NAME': decrypted_data["db_name"],
                'USER': decrypted_data.get("name"),
                'PASSWORD': decrypted_data.get("password"),
                'HOST': decrypted_data.get("host"),
                'PORT': connection.port,
                'OPTIONS': {},
                'TIME_ZONE': settings.TIME_ZONE,
                'CONN_HEALTH_CHECKS': True,
                'CONN_MAX_AGE': 60,
                'AUTOCOMMIT': True,
                'ATOMIC_REQUESTS': True,
            }

            temp_connection = get_temp_connection(db_config)

            if db_type in ('pymongo', 'mongodb'):
                try:
                    db = temp_connection.connection.client[decrypted_data["db_name"]]

                    # Eliminar prefijo "db." si lo trae
                    if query.startswith("db."):
                        query = query[3:]

                    # Ejecutar la consulta
                    result = eval(f"db.{query}")

                    # Convertir a lista si es iterable
                    if hasattr(result, 'to_list'):
                        result = result.to_list(length=None)
                    elif hasattr(result, '__iter__') and not isinstance(result, dict):
                        result = list(result)

                    # Convertir ObjectId
                    def convert(doc):
                        if isinstance(doc, dict):
                            doc = dict(doc)
                            if '_id' in doc:
                                doc['_id'] = str(doc['_id'])
                        return doc

                    if isinstance(result, list):
                        result = [convert(r) for r in result]
                    elif isinstance(result, dict):
                        result = convert(result)

                    return JsonResponse({'status': 'success', 'data': result})

                finally:
                    temp_connection.close()

            else:
                with temp_connection.cursor() as cursor:
                    cursor.execute(query)

                    if cursor.description:
                        rows = cursor.fetchall()
                        col_names = [desc[0] for desc in cursor.description]
                        results = [dict(zip(col_names, row)) for row in rows]
                        return JsonResponse({'status': 'success', 'type': 'select', 'data': results})
                    command_status = getattr(cursor, 'statusmessage', 'Consulta ejecutada.')
                    return JsonResponse({
                        'status': 'success',
                        'type': 'command',
                        'message': 'Consulta ejecutada correctamente.',
                        'rowcount': cursor.rowcount,
                        'command_status': str(command_status)
                    })

        except Exception as e:
            logger.error(f"Error al ejecutar la consulta: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
