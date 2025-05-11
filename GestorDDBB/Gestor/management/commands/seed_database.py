from django.core.management.base import BaseCommand
from Gestor.factories import GroupFactory, UserFactory, PermissionFactory, EnumerateFactory, ValueFactory
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
            order=3
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
        
        edicion_permission = PermissionFactory(
            name="Edicion",
            value="edicion",
            order=4
        )
        administradores_group.permissions.add(edicion_permission)
        self.stdout.write(f"Permiso creado: {edicion_permission.name}, Asociado a Grupo: {administradores_group.desc_group}")

        # Crear usuario "admin"
        administrador_user = UserFactory(
            name="admin",
            email="admin@admin.com",
            password=make_password("1234"),
            real_name="Administrador",
            group=administradores_group
        )
        self.stdout.write(f"Usuario creado: {administrador_user.name}, Grupo: {administrador_user.group.desc_group}")

        #Crear enumerado de tipos de conexion
        connection_enumerate=EnumerateFactory(
            name='Tipos de Conexión'
        )

        postgre_enumerate_value=ValueFactory(
            placeholder='PostgreSQL',
            value='django.db.backends.postgresql',
            order=1,
            enumerate=connection_enumerate
        )

        mysql_enumerate_value=ValueFactory(
            placeholder='MySQL',
            value='django.db.backends.mysql',
            order=2,
            enumerate=connection_enumerate
        )

        sqlite3_enumerate_value=ValueFactory(
            placeholder='SQLite',
            value='django.db.backends.sqlite3',
            order=3,
            enumerate=connection_enumerate
        )

        sql_enumerate_value=ValueFactory(
            placeholder='SQL',
            value='mssql',
            order=4,
            enumerate=connection_enumerate
        )

        django_enumerate_value=ValueFactory(
            placeholder='MongoDB',
            value='djongo',
            order=5,
            enumerate=connection_enumerate
        )
        self.stdout.write(f"Enumerado de conexiones creado creado: {connection_enumerate.name}")