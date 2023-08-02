@echo off

REM Chemin vers votre environnement virtuel
set VENV_PATH=venv\

REM Activez l'environnement virtuel
call %VENV_PATH%\Scripts\activate

REM Démarrez le serveur Django
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8001
