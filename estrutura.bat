@echo off
echo Gerando estrutura de pastas e arquivos do projeto Sis_web...

rem O comando 'tree' gera a arvore.
rem /F lista os arquivos alem das pastas.
rem /A usa caracteres simples (ASCII) para as linhas.
rem Removemos o /O:N que causou o erro.
tree /F /A > Sis_web_Estrutura.txt

echo.
echo Arquivo 'Sis_web_Estrutura.txt' gerado com sucesso!
