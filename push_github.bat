@echo off
REM Script pour pousser le projet sur GitHub

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  PUSH VERS GITHUB - Investment Portfolio Optimizer            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Vérifier le status
echo 📊 Status du repository...
git status
echo.

REM Ajouter tous les fichiers
echo 📝 Ajout des fichiers...
git add .
echo ✓ Fichiers ajoutés
echo.

REM Commiter
echo 💬 Commit en cours...
git commit -m "Final: Investment Portfolio Optimizer - Force Brute vs Dynamic Programming with interactive menu"
echo ✓ Commit effectué
echo.

REM Pousser
echo 🚀 Push vers GitHub...
git push origin main
echo ✓ Push effectué!
echo.

echo ╔════════════════════════════════════════════════════════════════╗
echo ║  ✅ Projet poussé avec succès sur GitHub!                    ║
echo ║  Email: djibsek@gmail.com                                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

pause
