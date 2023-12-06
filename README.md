# English:

## Getting information by shipping status.

This project has as objective to made alerts by the user behavior.

Currently, this has twice ways for gets the information, the first is though a CSV and the other one it is by SQL query, but the last is not working yet.
If you want to connect by SQL you should be following the instruction in the code, where you need to comment or uncomment the lines describe in the `main.py`, however you also need to prepare the database connection and the columns the same in the CSV file.

The connection string is in `initParameters.json`, you have to replace the variable the following way:

```json
"stringConn" : "dbname='postgres' user='postgres' password='password' host='localhost' port='5432'"
```
The 'OrderQuery' is working, but inactive; also, you have to replace the table query with the project table.  

The 'UserQuery' is not working, but this should contain the query for inner join the user data with the shipped order. User data should contain email address and will send an email, but you have to configure the email parameters in `initParameters.json`, the function `alerts.py` is ready for working.

For another hand, if you want to run by CSV file, you don't need to modify nothing in `main.py`.

## Requirements

- Python 3.x
- Pip

## Installation:

1. Clone the repo:

   ```bash
   git clone https://github.com/wandresvr/TechnicalTest.git
   ```

2. You should find out the `ConfigEnviroment.bat` file, then you run it, this file will create the virtual environment called 'PruebaTecWVargas' (Sorry, Spanish) and it will install dependencies in `requirements.txt` file. This is only for Windows users, because others OS is not available. I recommend you create for those with 'Anaconda'.

## Execution:

1. For to manually run, you need to run the `trigger.bat` file. 

2. for to run by scheduled task, you need type in console the following command:

```bash
schtasks /create /tn "TaskName" /tr "C:\Path\To\Run\trigger.bat" /sc daily /st HH:mm
```

You have to replace the path with the trigger path and put the hours to run it.

# Español:

## Extracción de información basada en pedidos.

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