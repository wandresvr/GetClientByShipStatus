# Prueba Técnica

Este proyecto tiene como finalidad generar alertas basadas en comportamiento de usuario.

Actualmente cuenta con dos formas de obtenerse la información, una es mediante el CSV suministrado y la otra es mediante la conexión a base de datos, que aún no está prepara.
Para conectarse a la base de datos es necesario comentar las lineas de código y descomentar como se indica dentro del archivo `main.py`, sin embargo hay que configurar la conexión a base de datos y asegurarse que las columnas de la tabla sean iguales a las del CSV suministrado.

El string de conexión se encuentra en el archivo de parametros dentro de `initParameters.json`, reemplace dentro de la variable según corresponda.

```json
"stringConn" : "dbname='postgres' user='postgres' password='password' host='localhost' port='5432'"
```

la variable 'OrderQuery' es un query funcional, se debe reemplazar el nombre de la tabla por la que apunta en la base de datos.

la variable 'UserQuery' no es funcional, se supone que esta trae la data de los usuarios, cruzandola con las ordenes para posteriormente enviar un correo como alerta, dicho correo también debe configurarse, en el archivo `initParameters.json` se encuentran los valores a ajustar, la función se encuentra en el archivo `alerts.py` lista con los parametros indicados.

Por otro lado, para obtener la información de manera simulada (como se propone en la prueba) no es necesario comentar alguna linea, sin embargo si se debe comentar lineas de código que usan este método simulado cuando se hace ya uso de la base de datos, al igual que antes, `main.py` tiene las instrucciones de que se debe comentar y que no.

## Requisitos

- Python 3.x
- Pip

## Instalación

1. Clone este repositorio:

   ```bash
   git clone https://github.com/wandresvr/TechnicalTest.git
   ```

2. Dirijase a la carpeta del proyecto y ubique el archivo `ConfigEnviroment.bat` y ejecutelo, este creará el entorno virtual de nombre 'PruebaTecWVargas' e instalará las dependencias que se encuentran en el archivo `requirements.txt`, tenga en cuenta que esto es para usuarios Windows, si usa otros sistemas como MAC o de LINUX, cree el entorno manualmente al igual que sus dependencias, ya que la dockerización aún no está disponible. También puede crear el entorno de manera sencilla usando 'Anaconda'.

## Ejecución

1. Para ejecutar manualmente, ejecuta el archivo `trigger.bat`.

2. Para ejecutar mediante una tarea programa, basta ejecutar en consola el siguiente comando:

```bash
schtasks /create /tn "NombreDeLaTarea" /tr "C:\Ruta\A\Tu\Ejecutar_Script.bat" /sc daily /st HH:mm
```
Reemplaza el nombre de la tarea por el que quieras, ubica la ruta de `trigger.bat` y coloque la hora a la que quieres que se ejecute.
Este ejecutara el script diariamente a la hora indicada.