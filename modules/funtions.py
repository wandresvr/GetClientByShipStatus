"""
Author: Wilson Vargas
Date created: 13/11/2023
contact: w.andres.vr@gmail.com

Dependecies:
- Pandas
- psycopg2
- cryptography
- logging

Use: Functions of the code.
"""



import pandas as pd
import psycopg2 as psycopg
from cryptography.fernet import Fernet
import logging
import os
import json


def GetLogName():
    """
    Gets complete path of log file
    
    
    
    """
    logDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    logDirectory = os.path.dirname(logDirectory)
    if not os.path.exists(logDirectory):
        os.makedirs(logDirectory)

    return os.path.join(logDirectory, "logFile.log")


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename=GetLogName(),
    #filemode='a'
)

 ##############################################

def GetInitParameters():

    jsonDirectory = os.path.dirname(os.path.abspath(__file__))
    jsonDirectory = os.path.dirname(jsonDirectory)
    jsonPath = os.path.join(jsonDirectory, "initParameters.json")

    with open(jsonPath, 'r') as jsonFile:
        Initparameters = json.load(jsonFile)
    return Initparameters



 ##############################################

def ProcessDfInChunks(df, processingFuntion, chunkSize=10000, returned=False, **kwargs):

    """
    Processes a dataframe in chunks, this uses a function for define operation.

    Args:
    - df (pandas dataframe): Dataframe to use in chunks.
    - processingFuntion (function): Funtion that process in chunks.
    - chunksize (int): Max value to load in each chunk (1000 is predefinied).
        
    - kwargs: I'ts very import pass the arguments here if you need aditionals arguments for processingFuntion.

    Returns:s
    it doesn't any return because dataframe is modified directly.
    """


    logging.info("Procesando por fragmentos (chunks) la función '{}'...".format(processingFuntion.__name__))

    chunkList = []
    totalchunks = len(df) // chunkSize + 1 #Get total chunks

    #Logs according to data size
    if len(df) > chunkSize:
        logging.info("Se procesarán '{0}' registros en fragmentos de '{1}'.".format(len(df), chunkSize))
    else:
        logging.info("Se procesarán '{}' registros.".format(len(df)))

    for i in range(totalchunks): #Process each chunk
        chunkStart = i * chunkSize
        chunkEnd = chunkStart + chunkSize
        chunk = df.iloc[chunkStart:chunkEnd]

        logging.info("Procesando el {:.2f}% de la información".format(chunkSize*i*100/len(df)))

        kwargs["start"] = chunkStart #Pass arguments in ProcessingFuntion
        kwargs["end"] = chunkEnd
        processingFuntion(chunk, **kwargs)

        if returned is True:
            chunkList.append(chunk)
    
    logging.info("El procesado fue exitoso.")
    
    if len(chunkList) != 0:
        return pd.concat(chunkList, ignore_index=True)


##############################################
    
def CreateMonthByDate(df, columnNameDate, columnName='shipping_month', start=None, end=None):
        
    """
    Creates a column with the month date
    
    Args:
    - df (Pandas dataframe): Dataframe to be convert.
    - columnNameDate (str): Name of the column dataframe that contain the dates.
    - columnName (str): Name of the column dataframe that store the month dates.
    - start (int): Specific the initial chunk the dataframe. Only uses when be use in chunks.
    - end (int): Specific the initial chunk the dataframe. Only uses when be use in chunks.
    
    Returns:
    it doesn't any return because dataframe is modified directly.
    """
    logging.info(f"Creando mes en la columna de '{columnName}' a partir de '{columnNameDate}'")

    # When is not used a chunk, modify all dataframe
    if start is None:
        start= 0
    if end is None:
        end= len(df)
        logging.warning("Se está cargando el dataframe completo, la memoria puede ser excedida si se manejan volumenes grandes de datos")

    df.loc[start:end, columnName] = pd.to_datetime(df[columnNameDate], errors='coerce').dt.month #Get shipping month from date, ignores no date format

    logging.info("Creación de la columna mes completada")

##############################################

def FilterByMonth(df , monthDay, columnName='shipping_month'):
    """
     Selects a month and extracts it from the dataframe
    
    Args:
    - df (Pandas dataframe): Dataframe used.
    - monthDay (int): Month select
    - column name (str): Column with month. is predefinied

    Returns:
    - New dataframe with only month indicated
    """

    logging.info("Agrupando por el mes '{}'...".format(monthDay))
    return df.loc[df[columnName] == monthDay].copy()

##############################################

def CredentialsEncrypt(credentialString):
    """
    Encrypts strings for secure uses

    Args:
    - CredentialString (str): String of credential (not encrypted)

    Return:
    - CredentialEncrypted: Variable encrypted
    - key: it's neccesary for to use credential
    """

    key =  Fernet.generate_key()
    cipher = Fernet(key)
    credentialEncrypted = cipher.encrypt(credentialString.encode())
    return credentialEncrypted, key

##############################################

def CredentialsDecript(credentialEncrypted, key):
    """
    Decrypts secure strings

    Args:
    - CredentialEncrypted (str encrypted): secure credential
    - key (str): it's necessary for to decrypt a string

    Return:
    - CredentialDencrypted: Credential decrypted (Only use in where is neccesary, not assign to another variable)
    """

    cipher = Fernet(key)
    return cipher.decrypt(credentialEncrypted).decode()

##############################################

def DataBaseToDataFrame(connectionString, query):

    """
    Handler of obtain data from a database (PostgreSQL- Redshift)

    Args:
    - connectionString (Encrypted) : Value with string connection to database.
    - Query (str) : SQL sentences for extract data from database.

    Return:
    - df (Pandas dataframe): If everything is good return a dataframe.
    - error (str): Return true if had an error.
    """
    
    try:
        logging.info("Conectando a la base de datos...")
        conn = psycopg.connect(connectionString)
        logging.info("La conexión a la base de datos fue exitosa.")
        df = GetDataFromQuery(query, conn)
        error = False

    except Exception as e:
        logging.error("La conexión a la base de datos falló.")
        logging.error(f'Error en la función: {e}', exc_info=True)
        error = True
        df = pd.DataFrame() #Empty dataframe

    finally:
        #Close the database connection
        if conn is not None:
            conn.close()
            logging.info("La conexión a la base de datos fue cerrada.")

    return df, error

##############################################


def GetDataFromQuery(query, conn):

    """
    Gets data from a database (PostgreSQL- Redshift) by chunks

    Args:
    - connectionString (Encrypted) : Value with string connection to database.
    - Query (str) : SQL sentences for extract data from database.

    Return:
    - df (Pandas dataframe): Return a dataframe.

    """
    logging.info("Obteniendo información de la base de datos...")
    
    processedChunks = []

    #Counts values in result
    queryCount = conn.cursor()
    queryCount.execute("SELECT COUNT(*) FROM ({})".format(query))

    countResult = queryCount.fetchone()

    #validates if query has results
    if countResult is not None:

        logging.info("Se van a obtener {} resultados de la base de datos.". format(countResult[0]))

        counter = 0

        for chunk in pd.read_sql_query(query, conn, chunksize=10000):
                processedChunks.append(chunk)
                counter += 1

                logging.info("Obteniendo el {:.2f}% de la información".format(len(chunk) * counter * 100 / countResult[0]))

        df = pd.concat(processedChunks, ignore_index=True)

        logging.info("Información obtenida con éxito.")

        return df
    else:
        logging.warning("No se obtuvo ningún resultado con los criterios de busqueda.")
        return pd.DataFrame() #Empty dataframe

##############################################

def GetDataFromCsv(path, delimiter=','):
 
    """
    Gets data from CSV
    
    Args:
    - path (str): CSV path file
    
    Return:
        - df (Pandas dataframe): If everything is good return a dataframe.
        - error (str): Return true if had an error.
    """

    logging.info("Obteniendo información desde el CSV: '{}'".format(path))

    try:
        df = pd.read_csv(path, delimiter=delimiter)
        error = False
        logging.info("Información obtenida con éxito.")
    except Exception as e:
        logging.error(f'Error en la función: {e}', exc_info=True)
        error = f'{e}'
        df = pd.DataFrame() #Create empty dataframe
    
    return df, error

##############################################


def filterData(df):
    """
    Filters data like a SQL query, is will be use only for simulate results in a database.

    args:
    - df (Pandas dataframe): Dataframe to will filter.

    Return:
    - result (Pandas dataframe): Dataframe filtered.
    """
    logging.info("Filtrando información según las condiciones indicadas...")
    
    groupedDf = df.groupby(['shipping_month',
        'order_vendor_dbname',
        'shipping_status' #Group by for Shipping month, order vendor id and status
        ]).agg( month_count=('shipping_month', 'size'), status_count=('shipping_status', 'size')).reset_index() #Count repeated values of shipping month and status 

    condition = (
    (groupedDf['month_count'] > 1) &
    (
        ((groupedDf['shipping_status'] == 'returned') & (groupedDf['status_count'] >= 2)) |
        ((groupedDf['shipping_status'] == 'cancelled') & (groupedDf['status_count'] >= 3)) #Get values with status match
    )
)

    result = groupedDf[condition]

    logging.info("Filtrado con éxito.")

    return result

##############################################

def InnerData(df1, df2, onColumnName):

    """
    Merge a couple dataframes by inner join.

    Args:
    - df1 (Pandas dataframe): dataframe 1 to merge
    - df2 (Pandas dataframe): dataframe 2 to merge
    - onColumnName (str): Column name by inner join

    Return
    - A new merged dataframe
    
    
    """

     # When is not used a chunk, modify all dataframe
    if start is None:
        start= 0
    if end is None:
        end= len(df1)
        logging.warning("Se está cargando el dataframe completo, la memoria puede ser excedida si se manejan volumenes grandes de datos")

    return pd.merge(df1, df2, on=onColumnName, how='inner')