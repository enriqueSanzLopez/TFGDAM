from django.core.management.base import BaseCommand
from Gestor.factories import GroupFactory, UserFactory
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Inseminar la bbdd con los datos iniciales"

    def handle(self, *args, **kwargs):
        # Crear grupo "administradores"
        administradores_group = GroupFactory(desc_group="administradores")
        self.stdout.write(f"Grupo creado: {administradores_group.desc_group}")

        # Crear usuario "admin"
        administrador_user = UserFactory(
            name="admin",
            email="admin@admin.com",
            password=make_password("1234"),
            real_name="Administrador",
            group=administradores_group
        )
        self.stdout.write(f"Usuario creado: {administrador_user.name}, Grupo: {administrador_user.group.desc_group}")
