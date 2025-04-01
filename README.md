# TFGDAM
Repositorio generado para guardar el TFG de DAM 2025

Lista de comandos:

Ejecutar la aplicación para pruebas:
    python manage.py runserver

La ruta será: http://localhost:8000/

Generar migraciones para los modelos:
    python manage.py makemigrations

Generar tablas de la base de datos:
    python manage.py migrate

Insertar registros iniciales en la aplicación:
    python manage.py seed_database

Registrar cambios en archivos estáticos:
    python manage.py collectstatic