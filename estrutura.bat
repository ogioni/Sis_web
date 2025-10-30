@echo off
SETLOCAL EnableDelayedExpansion

echo.
echo ==========================================================
echo      Gerando ESTRUTURA LIMPA do projeto Sis_web
echo ==========================================================
echo.

REM 1. Oculta temporariamente as pastas desnecessarias (ruido)
echo [INFO] Ocultando pastas de 'ruido' (venv, .git, .vscode)...
if exist "venv" ( attrib +h venv /S /D > nul )
if exist ".git" ( attrib +h .git /S /D > nul )
if exist ".vscode" ( attrib +h .vscode /S /D > nul )

echo [INFO] Ocultando todas as pastas __pycache__...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        attrib +h "%%d" /S /D > nul
    )
)

REM 2. Gera a arvore (agora limpa)
echo [INFO] Gerando a arvore de arquivos do projeto...
tree /F /A > Sis_web_Estrutura_Limpa.txt

REM 3. Restaura a visibilidade das pastas (MUITO IMPORTANTE!)
echo [INFO] Restaurando a visibilidade das pastas...
if exist "venv" ( attrib -h venv /S /D > nul )
if exist ".git" ( attrib -h .git /S /D > nul )
if exist ".vscode" ( attrib -h .vscode /S /D > nul )

for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        attrib -h "%%d" /S /D > nul
    )
)

echo.
echo ==========================================================
echo [SUCESSO] Arquivo 'Sis_web_Estrutura_Limpa.txt' gerado!
echo ==========================================================
echo.
pause