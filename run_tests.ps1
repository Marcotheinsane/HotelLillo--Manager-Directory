# Script para ejecutar pruebas del módulo Habitaciones
# Buscar entorno virtual

if (Test-Path ".\venv\Scripts\python.exe") {
    $pythonPath = ".\venv\Scripts\python.exe"
    Write-Host "Entorno virtual encontrado"
}
elseif (Test-Path ".\env\Scripts\python.exe") {
    $pythonPath = ".\env\Scripts\python.exe"
    Write-Host "Entorno virtual (env) encontrado"
}
else {
    $pythonPath = "python.exe"
    Write-Host "Usando Python global"
}

Write-Host "Ejecutando migraciones..."
&$pythonPath manage.py migrate

Write-Host "Ejecutando pruebas..."
&$pythonPath manage.py test apps.habitaciones.tests

Write-Host "Completado"
