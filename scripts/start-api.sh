#!/bin/sh
# Script de orquestacion para el arranque del contenedor de la API.
# Este script asegura que la base de datos este actualizada antes de lanzar el servidor.

# El comando 'set -e' hace que el script se detenga inmediatamente si algun paso falla
set -e

# Mensaje de aviso en el log del contenedor
echo "Waiting for PostgreSQL..."

# Bucle que chequea la conexion al host 'postgres' en el puerto 5432
until pg_isready -h postgres -p 5432 -U postgres; do
  
  # Si falla la conexion, espera 2 segundos y reintenta
  sleep 2

done

# PASO 1: Sincronizacion de la base de datos
# Ejecuta 'alembic upgrade head' para aplicar todas las revisiones pendientes en Postgres
echo "Applying database migrations..."
alembic upgrade head

# PASO 2: Inicio del servidor de aplicaciones
# Lanza uvicorn apuntando al objeto 'app' en 'app.main'
# Se configura host 0.0.0.0 para que sea accesible desde fuera del contenedor
echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000