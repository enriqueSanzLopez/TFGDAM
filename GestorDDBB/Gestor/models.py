from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from cryptography.fernet import Fernet
from datetime import datetime


# Create your models here.
#Modelo para estilos personalizados en la aplicacion
class CustomStyle(models.Model):
    main_color=models.CharField(max_length=50, null=True, blank=True)
    secondary_color=models.CharField(max_length=50, null=True, blank=True)
    text_color=models.CharField(max_length=50, null=True, blank=True)
    text_size=models.IntegerField(null=True, blank=True)
    company_name=models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone=models.TextField(null=True, blank=True)
    other_code=models.TextField(null=True, blank=True)
    imagen=models.TextField(null=True, blank=True)

#Modelo para indicar grupo
class Group(models.Model):
    desc_group=models.TextField(null=False, blank=False, unique=True)
    permissions=models.ManyToManyField('Permission', related_name='groups')
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)

#Modelo para indicar usuario
class User(models.Model):
    name=models.CharField(max_length=255, null=False, blank=False, unique=True)
    real_name=models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password=models.TextField(null=False, blank=False)
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    group=models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)
    def verify_password(self, raw_password):
        # return self.password == make_password(raw_password, salt=None)
        return True

#Modelo para indicar los posibles permisos de la aplicacion
class Permission(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False, unique=True)
    value=models.TextField(null=True, blank=True)
    order=models.IntegerField(null=True, blank=True)
    # groups=models.ManyToManyField('Group', related_name='permissions')
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)

#Modelo para enumerados
class Enumerate(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False, unique=True)
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)

#Modelo para valores de enumerados
class Value(models.Model):
    placeholder=models.TextField(null=True, blank=True)
    value=models.TextField(null=True, blank=True)
    order=models.IntegerField(null=True, blank=True)
    enumerate=models.ForeignKey(Enumerate, on_delete=models.CASCADE, related_name='values')
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)

#Modelo de conexiones para usuario
# ENCRYPTION_KEY = Fernet.generate_key()
ENCRYPTION_KEY = 'fPqzIn80Wrf_PF8O8uMCVpO5VkmndDhWxhc7-oGOiCE='
cipher = Fernet(ENCRYPTION_KEY)
class Connection(models.Model):
    token=models.CharField(max_length=256, null=False, blank=False, unique=True, default=str(uuid.uuid4()))
    db_type = models.CharField(max_length=256, null=False, blank=False)
    host=models.TextField(null=False, blank=False)
    db_name=models.TextField(null=False, blank=False, default="abcd")
    port = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections')
    name=models.TextField(null=False, blank=False)
    password=models.TextField(null=False, blank=False, default="1234")
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)
    def save(self, *args, **kwargs):
        # Generar un token único si no existe
        if not self.token:
            self.token = str(self.user.id)+str(uuid.uuid4())+str(datetime.now())
        # Encriptar los datos sensibles antes de guardarlos
        self.host = cipher.encrypt(self.host.encode()).decode()
        self.db_name = cipher.encrypt(self.db_name.encode()).decode()
        self.db_type = cipher.encrypt(self.db_type.encode()).decode()
        self.name = cipher.encrypt(self.name.encode()).decode()
        self.password = cipher.encrypt(self.password.encode()).decode()
        super().save(*args, **kwargs)
    def decrypt_data(self):
        # Desencriptar los datos sensibles
        return {
            "host": cipher.decrypt(self.host.encode()).decode(),
            "db_name": cipher.decrypt(self.db_name.encode()).decode(),
            "db_type": cipher.decrypt(self.db_type.encode()).decode(),
            "name": cipher.decrypt(self.name.encode()).decode(),
            "password": cipher.decrypt(self.password.encode()).decode(),
        }
    def get_connections_front(self):
        return {
            "id": self.id,
            "host": cipher.decrypt(self.host.encode()).decode(),
            "db_name": cipher.decrypt(self.db_name.encode()).decode(),
        }
    def get_connections_back(self):
        connections = self.user.connections.all().values("id", "host", "name", "db_type", "password", "db_name")
        return {
            "id": self.id,
            "host": cipher.decrypt(self.host.encode()).decode(),
            "db_name": cipher.decrypt(self.db_name.encode()).decode(),
            "name": cipher.decrypt(self.name.encode()).decode(),
            "db_type": cipher.decrypt(self.db_type.encode()).decode(),
            "password": cipher.decrypt(self.password.encode()).decode(),
        }

