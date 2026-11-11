# PowerShell запуск сервера визитки MAXSAV4
$ErrorActionPreference = "Stop"

Write-Host "🌟 Запуск MAXSAV4 Pro-Maker Hub..." -ForegroundColor Cyan

$ScriptDir = $PSScriptRoot
$VenvPython = "$ScriptDir\..\Golos control\venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    $VenvPython = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
}

Write-Host "Используется Python: $VenvPython" -ForegroundColor Green
& $VenvPython "$ScriptDir\server.py"
