@echo off
echo.
echo ==========================================================
echo           ATUALIZANDO PROJETO DO GITHUB
echo ==========================================================
echo.

REM 1. Ativa o ambiente virtual (so para garantir que o git/comandos funcionem)
call .\venv\Scripts\activate.bat

REM 2. Puxa as ultimas mudancas
echo [GIT] Puxando ultimas mudancas (git pull)...
git pull

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao puxar. Verifique a conexao.
) ELSE (
    echo.
    echo [SUCESSO] Projeto atualizado!
)

echo.
echo [LIMPEZA] Instalando dependencias (pip install -r)...
pip install -r requirements.txt

echo.
echo [STATUS] Checando migrações pendentes...
python manage.py migrate --check

echo.
echo ==========================================================
call .\venv\Scripts\deactivate.bat
pause