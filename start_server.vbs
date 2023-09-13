Set objShell = CreateObject("WScript.Shell")

' Chemin complet vers le script Python que vous souhaitez exécuter
PythonScriptPath = ".\start_server.py"

' Exécutez le script Python en utilisant la commande Python
objShell.Run "python " & PythonScriptPath, 0, True
