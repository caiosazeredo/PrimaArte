@echo off
echo.
echo 🎨 ================================================
echo    PRIMA ARTE - INICIANDO SERVIDOR
echo ================================================
echo.
echo Verificando dependências...
pip install -r requirements.txt
echo.
echo Iniciando servidor Flask...
echo Acesse: http://localhost:5000
echo Admin: http://localhost:5000/admin (senha: primaarte2025)
echo.
echo Para parar: Ctrl+C
echo.
python app.py
pause
