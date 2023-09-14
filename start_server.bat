@echo off

REM Chemin vers votre environnement virtuel
set VENV_PATH=venv

REM Nom du fichier de verrouillage
set LOCK_FILE=%VENV_PATH%\server.lock

REM Vérifiez si le fichier de verrouillage existe
if exist "%LOCK_FILE%" (
    REM Le serveur est déjà en cours d'exécution. Ouvrir le navigateur.
    start "" "http://localhost:8001"
) else (
    REM Créez le fichier de verrouillage
    echo. > "%LOCK_FILE%"
    
    REM Activez l'environnement virtuel
    call %VENV_PATH%\Scripts\activate
    
    REM Démarrez le serveur Django en arrière-plan
    start /b python manage.py runserver 8001
    
    REM Attendez quelques secondes pour que le serveur démarre
    timeout /t 10
    
    REM Ouvrez le navigateur à l'adresse localhost:8001
    start "" "http://localhost:8001"
    
    
)

REM Attendez quelques secondes pour que l'utilisateur puisse voir le message
timeout /t 5
