@echo off
echo ========================================
echo   DÉMARRAGE DE TOUS LES SERVICES
echo ========================================
echo.

:: Vérifier que PostgreSQL est en cours d'exécution
echo Vérification de PostgreSQL...
sc query PostgreSQL | findstr /C:"RUNNING" >nul
if errorlevel 1 (
    echo PostgreSQL n'est pas démarré. Démarrage...
    net start PostgreSQL
) else (
    echo PostgreSQL est déjà en cours d'exécution
)

:: Attendre que PostgreSQL soit prêt (3 secondes)
timeout /t 3 /nobreak >nul

echo.
echo Lancement des services...

:: Démarrer le service Users dans une nouvelle fenêtre
echo   - Service Users (port 5001)
start "Users Service" cmd /c "cd services\users && python app.py"

:: Attendre un peu pour éviter les conflits de ports
timeout /t 2 /nobreak >nul

:: Démarrer le service Tasks dans une nouvelle fenêtre
echo   - Service Tasks (port 5002)
start "Tasks Service" cmd /c "cd services\tasks && python app.py"

:: Attendre un peu
timeout /t 2 /nobreak >nul

:: Démarrer le Frontend dans une nouvelle fenêtre
echo   - Frontend Service (port 5000)
start "Frontend Service" cmd /c "cd services\frontend && python app.py"

echo.
echo ========================================
echo TOUS LES SERVICES ONT ÉTÉ LANCÉS
echo ========================================
echo.
echo Services disponibles :
echo   - Frontend : http://localhost:5000
echo   - Users API : http://localhost:5001
echo   - Tasks API : http://localhost:5002
echo.
echo PostgreSQL :
echo   - Users DB : usersdb
echo   - Tasks DB : tasksdb
echo   - Utilisateur : postgres
echo   - Port : 5432
echo.
echo  Commandes utiles :
echo   - Arrêter : fermez les fenêtres
echo   - Voir les logs : chaque fenêtre affiche ses logs
echo   - Tester : ouvrez http://localhost:5000 dans votre navigateur
echo.
pause