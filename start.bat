@echo off
chcp 65001 > nul
title MAXSAV4 Pro-Maker Hub Web Server

echo ========================================================
echo   🌟 MAXSAV4 PRO-MAKER HUB (Визитка & 3D WebXR Studio)
echo ========================================================
echo.

set SCRIPT_DIR=%~dp0
set PYTHON_EXE=%SCRIPT_DIR%..\Golos control\venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python.exe
)

echo [OK] Запуск веб-сервера через %PYTHON_EXE%...
"%PYTHON_EXE%" "%SCRIPT_DIR%server.py"

pause
