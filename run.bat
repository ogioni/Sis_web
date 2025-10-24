@echo off
echo Ativando ambiente virtual...
call .\venv\Scripts\activate.bat

echo Iniciando servidor Django...
python manage.py runserver

echo Servidor finalizado. Desativando ambiente...
call .\venv\Scripts\deactivate.bat
pause