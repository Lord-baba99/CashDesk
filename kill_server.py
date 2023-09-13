import subprocess
import re

"""

# Commande pour tuer le serveur Django sur le port 8001
command = f"taskkill /F /FI WINDOWTITLE eq *:8001*"

# Exécutez la commande
subprocess.call(command, shell=True)

 """

# Commande pour lister les processus Python avec CMD.EXE dans le titre de la fenêtre
command = 'tasklist /FI "IMAGENAME eq python.exe" /V /FI "WINDOWTITLE eq C:\\Windows\\system32\\cmd.exe"'

# Exécutez la commande et capturez la sortie
output = subprocess.check_output(command, shell=True, universal_newlines=True)

# Utilisez une expression régulière pour extraire le PID
pid_match = re.search(r'python\.exe\s+(\d+)', output)

if pid_match:
    pid = pid_match.group(1)
    print(f"Le PID du processus Python est : {pid}")
else:
    print("Processus Python non trouvé.")
