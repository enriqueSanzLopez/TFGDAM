from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator

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
    name=models.CharField(max_length=50, null=False, blank=False)
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
class Connection(models.Model):
    db_type = models.CharField(max_length=20, null=False, blank=False)
    host=models.TextField(null=False, blank=False, unique=True)
    port = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(65535)])
    name=models.TextField(null=False, blank=False, unique=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections')
    created_at=models.DateTimeField(null=False, blank=False, auto_now_add=True)
    updated_at=models.DateTimeField(null=False, blank=False, auto_now=True)

