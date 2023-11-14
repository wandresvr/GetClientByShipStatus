@echo off

echo Creando entorno virtual con dependencias...

:: Configura el nombre de tu entorno virtual
set VIRTUAL_ENV_NAME=PruebaTecWVargas

echo Creando entorno virtual con nombre %VIRTUAL_ENV_NAME% ...

:: Crea el entorno virtual
set "VIRTUAL_ENV_PATH=%USERPROFILE%\Documents\%VIRTUAL_ENV_NAME%"

echo Creando entorno virtual en %VIRTUAL_ENV_PATH% ...

:: Verifica si la carpeta ya existe
if not exist "%VIRTUAL_ENV_PATH%" (
    echo Creando la carpeta de destino...
    mkdir "%VIRTUAL_ENV_PATH%" || (
        echo No se pudo crear la carpeta de destino.
        pause
        exit /b 1
    )
) else (
    echo La carpeta de destino ya existe.
)

echo Creando el entorno en la ruta %VIRTUAL_ENV_PATH% ...
python -m venv "%VIRTUAL_ENV_PATH%" || (
    echo No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

:: Activa el entorno virtual
echo Activando entorno para cargar dependencias...
call "%VIRTUAL_ENV_PATH%\Scripts\activate.bat"

:: Instala las dependencias desde requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt

:: Muestra un mensaje de finalización
echo.
echo Entorno virtual creado y dependencias instaladas. Para activar el entorno, ejecuta: "%VIRTUAL_ENV_PATH%\Scripts\activate.bat"
echo Presione enter para salir
pause >nul
