@echo off
echo Configurando Git...
"C:\Program Files\Git\cmd\git.exe" init
"C:\Program Files\Git\cmd\git.exe" config user.email "bot@alexa.com"
"C:\Program Files\Git\cmd\git.exe" config user.name "AlexaBot"
echo Adicionando arquivos...
"C:\Program Files\Git\cmd\git.exe" add .
echo Criando commit...
"C:\Program Files\Git\cmd\git.exe" commit -m "Upload Automatico"
echo Configurando repositorio remoto...
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote remove origin
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/PedroHenriqueFariasMedeiros/alexa-dj.git
echo Enviando para o GitHub (Pode abrir uma janela de login)...
"C:\Program Files\Git\cmd\git.exe" push -u origin main --force
echo.
echo PROCESSO FINALIZADO! Se apareceu "Success" ou urls acima, deu certo.
pause
