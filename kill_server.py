import subprocess
import re


# Commande pour lister les processus Python avec CMD.EXE dans le titre de la fenêtre
command = 'tasklist /FI "IMAGENAME eq python.exe" /V /FI "WINDOWTITLE eq C:\\Windows\\system32\\cmd.exe"'

# Exécutez la commande et capturez la sortie
output = subprocess.check_output(command, shell=True, universal_newlines=True, encoding='utf-8', errors='ignore')
print("output :")
print(output)

# Utilisez une expression régulière pour extraire le PID
print("PID")
pid_match = re.search(r'python\.exe\s+(\d+)', output)

if pid_match:
    pid = pid_match.group(1)
    print(f"Le PID du processus Python est : {pid}")
    # Commande pour tuer le serveur Django sur le port 8001
    kill_command = f"taskkill /pid {pid}"
    # Exécutez la commande
    subprocess.call(kill_command, shell=True)
    
    print('Serveur mis en arret !!!')
    # Supprimer le lockfile
    del_lock_file = 'del venv\\server.lock'
    subprocess.call(del_lock_file, shell=True)

else:
    print("Processus Python non trouvé.")
