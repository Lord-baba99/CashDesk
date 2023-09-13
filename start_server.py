import os
import subprocess
import time

# Chemin vers votre environnement virtuel
VENV_PATH = "venv"

# Nom du fichier de verrouillage
LOCK_FILE = os.path.join(VENV_PATH, "server.lock")

# Vérifiez si le fichier de verrouillage existe
if os.path.exists(LOCK_FILE):
    # Le serveur est déjà en cours d'exécution. Ouvrir le navigateur.
    subprocess.Popen(["start", "", "http://localhost:8001"], shell=True)
else:
    # Créez le fichier de verrouillage
    open(LOCK_FILE, 'w').close()

    # Activez l'environnement virtuel
    activate_command = os.path.join(VENV_PATH, "Scripts", "activate")
    subprocess.Popen(activate_command, shell=True)

    # Démarrez le serveur Django en arrière-plan
    server_command = "python manage.py runserver 8001"
    subprocess.Popen(server_command, shell=True)

    # Attendez quelques secondes pour que le serveur démarre
    time.sleep(5)

    # Ouvrez le navigateur à l'adresse localhost:8001
    subprocess.Popen(["start", "", "http://localhost:8001"], shell=True)

    # Supprimez le fichier de verrouillage une fois que le serveur s'est arrêté
    os.remove(LOCK_FILE)

# Attendez quelques secondes pour que l'utilisateur puisse voir le message
time.sleep(5)
