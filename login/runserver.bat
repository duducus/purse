@echo off
REM Ejecutar makemigrations
echo Ejecutando makemigrations...
python manage.py makemigrations

REM Ejecutar migrate
echo Ejecutando migrate...
python manage.py migrate

REM Ejecutar runserver
echo Iniciando el servidor de desarrollo...
python manage.py runserver
