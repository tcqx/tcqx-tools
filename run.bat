@echo off
title TCQX Terminal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo [ ERR ] Python n'est pas installe ou n'est pas dans le PATH.
    echo Installez Python depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

python -c "import rich" >nul 2>nul
if errorlevel 1 (
    echo [ SYSTEM ] Installation des dependances...
    python -m pip install -r requirements.txt
)

python main.py

if errorlevel 1 (
    echo.
    echo [ ERR ] Le programme s'est arrete avec une erreur.
    pause
)
