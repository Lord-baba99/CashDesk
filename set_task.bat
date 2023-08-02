@echo off

set "task_name=GestCaisse"
set "script_path=.\start_server.bat"

REM Vérifier si la tâche existe déjà
schtasks /query /tn "%task_name%" > nul 2>&1
if %errorlevel% neq 0 (
    REM La tâche n'existe pas, donc la créer
    schtasks /create /tn "%task_name%" /sc onstart /tr "%~dp0%script_path%"
    echo Tâche planifiée créée avec succès.
) else (
    REM La tâche existe déjà, ne rien faire
    echo La tâche planifiée existe déjà.
)
