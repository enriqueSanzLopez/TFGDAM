from django.contrib import admin
from .models import CustomStyle
from .models import Group
from .models import User
from .models import Permission
from .models import Enumerate
from .models import Value
from .models import Connection

# Register your models here.
@admin.register(CustomStyle)
class CustomStyleAdmin(admin.ModelAdmin):
    list_display=('company_name', 'email', 'telephone', 'main_color', 'secondary_color', 'text_color', 'text_size', 'other_code')
    list_editable=('company_name', 'email', 'telephone', 'main_color', 'secondary_color', 'text_color', 'text_size', 'other_code')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields=('desc_group', 'created_at', 'updated_at')
    list_display=('desc_group', 'created_at', 'updated_at')
    list_editable=('desc_group')
    ordering=('-updated_at')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields=('name', 'real_name', 'email', 'created_at', 'updated_at')
    list_filter = ('group')
    list_display=('name', 'real_name', 'email', 'group', 'created_at', 'updated_at')
    list_editable=('name', 'real_name', 'email', 'group')
    ordering=('group', 'name', '-updated_at')

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields=('name', 'value', 'created_at', 'updated_at')
    list_display=('name', 'value', 'order', 'created_at', 'updated_at')
    list_editable=('name', 'value', 'order')
    ordering=('name')

@admin.register(Enumerate)
class EnumerateAdmin(admin.ModelAdmin):
    search_fields=('name', 'created_at', 'updated_at')
    list_display=('name', 'created_at', 'updated_at')
    list_editable=('name')
    ordering=('name')

@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    search_fields=('placeholder', 'value', 'created_at', 'updated_at')
    list_filter = ('enumerate')
    list_display=('placeholder', 'enumerate', 'value', 'order', 'created_at', 'updated_at')
    list_editable=('placeholder', 'enumerate', 'value', 'order')
    ordering=('enumerate', 'order')

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    search_fields=('db_type', 'host', 'created_at', 'updated_at')
    list_filter = ('user')
    list_display=('db_type', 'host', 'port', 'name', 'user', 'created_at', 'updated_at')
    list_editable=('db_type', 'host', 'port', 'name', 'user')
    ordering=('user', 'db_type', 'host')