@echo off
::Nombre del entorno virtual
set VIRTUAL_ENV_NAME=PruebaTecWVargas

::Ruta del entorno virtual
set "VIRTUAL_ENV_PATH=%USERPROFILE%\Documents\%VIRTUAL_ENV_NAME%"

::Activar entorno virtual
call "%VIRTUAL_ENV_PATH%\Scripts\activate.bat"

::Ejecutar el código de python
python "C:\Users\Wilson\PruebaTecnica\main.py"
pause >nul