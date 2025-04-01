from django.core.management.base import BaseCommand
from Gestor.factories import GroupFactory, UserFactory, PermissionFactory
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Inseminar la bbdd con los datos iniciales"

    def handle(self, *args, **kwargs):
        # Crear grupo "administradores"
        administradores_group = GroupFactory(desc_group="administradores")
        self.stdout.write(f"Grupo creado: {administradores_group.desc_group}")

        lectura_permission = PermissionFactory(
            name="Lectura",
            value="lectura",
            order=1
        )
        administradores_group.permissions.add(lectura_permission)
        self.stdout.write(f"Permiso creado: {lectura_permission.name}, Asociado a Grupo: {administradores_group.desc_group}")

        personalizacion_permission = PermissionFactory(
            name="Personalizacion",
            value="personalizacion",
            order=2
        )
        administradores_group.permissions.add(personalizacion_permission)
        self.stdout.write(f"Permiso creado: {personalizacion_permission.name}, Asociado a Grupo: {administradores_group.desc_group}")

        usuarios_permission = PermissionFactory(
            name="Usuarios",
            value="usuarios",
            order=2
        )
        administradores_group.permissions.add(usuarios_permission)
        self.stdout.write(f"Permiso creado: {usuarios_permission.name}, Asociado a Grupo: {administradores_group.desc_group}")

        # Crear usuario "admin"
        administrador_user = UserFactory(
            name="admin",
            email="admin@admin.com",
            password=make_password("1234"),
            real_name="Administrador",
            group=administradores_group
        )
        self.stdout.write(f"Usuario creado: {administrador_user.name}, Grupo: {administrador_user.group.desc_group}")
