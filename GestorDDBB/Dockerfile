FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    pkg-config \
    libpq-dev \
    libmariadb-dev-compat \
    default-libmysqlclient-dev \
    libssl-dev \
    zlib1g-dev \
    unixodbc-dev \
    libsasl2-dev \
    libldap2-dev \
    gnupg \
    curl \
    && apt-get remove -y libodbc2 unixodbc-common libodbcinst2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar ODBC y drivers de Microsoft SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto para Gunicorn
EXPOSE 8000

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "GestorDDBB.wsgi:application", "--bind", "0.0.0.0:8000"]
