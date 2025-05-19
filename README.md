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

Compilar traducciones:
    pybabel compile -d translations

Instalación:
    Para la instalación, se asume que el usuario tiene una instalación de Docker funcional. Los comandos se van a explicar para el sistema operativo Windows. En caso de trabajar con un entorno Ubuntu, es posible, que los comandos de docker-exec, se tengan que lanzar como docker exec dado que algunas distribuciones de Docker tienen pequeñas variaciones en sus comandos.

    Generación de los contenedores Docker:
        La carpeta GestorDDBB contiene en su interior los archivos docker-compose.yml y Dockerfile encargados de la generación de los contenedores. Los parámetros de estos, dependen del archivo .env, el cual puede modificarse para cambiar datos de conexión o puertos de uso, encontrado en la misma carpeta. Para lanzar estos contenedores, se necesita lanzar el siguiente comando:
            docker-compose up -d
        
        Se puede comprobar que la aplicación funciona correctamente funciona correctamente listando los contenedores de Docker, donde ahora debería haber dos contenedores nuevos llamados: gestorddbb-db-1 gestorddbb-web-1. Los cuales deberían estar en marcha.

        Seguidamente, se debe migrar la base de datos, para lo cual, se deben lanzar los siguientes comandos:
            docker-compose exec web python manage.py makemigrations
            docker-compose exec web python manage.py migrate
            docker-compose exec web python manage.py seed_database
        
        Guardar los cambios de archivos estáticos:
            docker-compose exec web python manage.py collectstatic --noinput
    
    Conexión con servicios locales:
        Para conectar con servicios locales, es necesario cambiar localhost por: host.docker.internal, por ejemplo si fuera a conectar a localhost:8080, tendría que hacerlo a host.docker.internal:8080