FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para PostgreSQL y compilacion
#RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y build-essential libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos e instala las librerias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el codigo fuente del proyecto al contenedor
COPY . .

# CAMBIO APLICADO: Asegura que el script de arranque tenga permisos de ejecucion
RUN chmod +x /app/scripts/start-api.sh

# Informa que el contenedor escuchara en el puerto 8000
EXPOSE 8000

# Punto de entrada por defecto que ejecuta las migraciones y lanza la API
CMD ["/app/scripts/start-api.sh"]