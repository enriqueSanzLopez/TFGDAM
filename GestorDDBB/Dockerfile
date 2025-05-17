# Imagen base ligera con Python 3.11
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    unixodbc-dev \
    gnupg \
    curl \
    libsasl2-dev \
    libldap2-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala el driver ODBC para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo el contenido del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el contenedor
EXPOSE 8000

# Comando por defecto para arrancar Django con Gunicorn
CMD ["gunicorn", "GestorDDBB.wsgi:application", "--bind", "0.0.0.0:8000"]
