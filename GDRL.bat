@echo off

echo Iniciando servidor com ambiente virtual...
cd /d "%~dp0"

.\.venv\Scripts\python.exe serverInterface.py
pause
