@echo off
SETLOCAL EnableDelayedExpansion

REM --- SCRIPT PARA SALVAR E ENVIAR MUDANÇAS PARA O GITHUB ---

echo.
echo ==========================================================
echo               INICIANDO BACKUP PARA O GITHUB
echo ==========================================================
echo.

REM 1. Ativa o ambiente virtual
call .\venv\Scripts\activate.bat

REM 2. Adiciona todas as mudancas (novos arquivos e modificados)
echo [GIT] Adicionando todas as mudancas (git add .)...
git add .

REM 3. Pega a data e hora para a mensagem do commit
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set datan=%%a-%%b-%%c
)
for /f "tokens=1-2 delims=:" %%a in ('time /t') do (
    set timen=%%a%%b
)
REM A CORRECAO: Mensagem sem acento e entre aspas para o Git
set msg="Backup Automatico - %datan% %timen%"

REM 4. Faz o commit com a mensagem automatica
echo.
echo [GIT] Criando o commit: !msg!
REM Chamando com 'call' e aspas duplas para garantir que o CMD nao quebre
call git commit -m !msg!

IF %ERRORLEVEL% NEQ 0 (
    REM O ERRORLEVEL 1 geralmente significa "Nothing to commit" se o 'git commit' foi chamado
    echo.
    echo [ALERTA] Nenhuma mudanca para commitar.
    echo.
    goto FIM
)

REM 5. Envia o commit para o GitHub
echo.
echo [GIT] Enviando para o GitHub (git push)...
git push

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao enviar para o GitHub. Verifique a conexao ou credenciais.
) ELSE (
    echo.
    echo [SUCESSO] Backup concluido e enviado!
)

:FIM
echo.
echo ==========================================================
call .\venv\Scripts\deactivate.bat
pause