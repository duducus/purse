#!/bin/bash

# Activa el entorno virtual de Python
echo "Activando entorno virtual..."
source /home/tolarian-django/tolarianenv/bin/activate

# Ejecuta las migraciones
echo "Ejecutando migraciones..."
python3 manage.py migrate

# Crea las migraciones necesarias
echo "Creando migraciones..."
python3 manage.py makemigrations

# Reinicia Gunicorn
echo "Reiniciando Gunicorn..."
sudo systemctl restart gunicorn

# Recarga Nginx
echo "Recargando Nginx..."
sudo systemctl reload nginx

echo "¡Script ejecutado con éxito!"

