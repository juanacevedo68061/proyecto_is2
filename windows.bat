@echo off

:: Crear un entorno virtual
python -m venv virtual

:: Activar el entorno virtual
call virtual\Scripts\activate
python -m pip install --upgrade pip
pip cache purge


:: Instalar las dependencias del proyecto desde el archivo requirements.txt
pip install -r requirements.txt

:: Realizar migraciones en la base de datos
python manage.py makemigrations canvan administracion roles cms login publicaciones
python manage.py migrate

:: Mensaje de finalización
echo Configuración y migraciones completadas.