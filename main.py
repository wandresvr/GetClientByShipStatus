"""
Author: Wilson Vargas
Date created: 13/11/2023
contact: w.andres.vr@gmail.com

Dependecies:
- Pandas
- logging
- sys

Use: Main of the code.

Description: 
Gets informatión from a source such as database or CSV file, then applies the folliwng filters: 
filters by month then get only shipping_status in 'cancelled' or 'returned' 
and whether finds it twice or trhee times in the same month (depending of status).

The next step is generate alerts by each register.

Note: Due the data it could be very large, its using chunk and pandas for process efficiently.
"""


from modules.funtions import *
from modules.alerts import *
import sys
import logging
import os

#Logging instructions 


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename=GetLogName(),
    #filemode='a'
)


def BusinessProcessInExistingData(data):

    """
    Executes the business process in existing data by chunks (it is an alternative to using a Query in database).
    The process consists separe data by month and applies the filters like a query
    
    args*
    - data (Pandas dataframe): Data to filter

    Return:
    - Return a appended dataframe with the final data to process.
    """
    
    logging.warning("Filtrando información basado en las condiciones determinadas de manera simulada...")

    months = list(range(1, 13)) #Create a list with number of month of year
    AllMonthsFilteredList = [] 

    #create a empty column
    data = data.assign(shipping_month=pd.Series([None] * len(data)))

    #Process the data by chunk, using the Convert data 
    ProcessDfInChunks(data, processingFuntion=CreateMonthByDate, columnNameDate='shipping_date')

    #Iterates in each month o year and get filtered data and concat a new daframe
    for month in months:
        dataFilterByMonth= FilterByMonth(data , month, columnName='shipping_month')

        #print(str(month), dataFilterByMonth.head())
    
        #ignores empty data in a month
        if dataFilterByMonth.empty:
            logging.info("No existen datos para el mes.")
            continue
        
        dataAllFiltered = filterData(dataFilterByMonth)[['order_vendor_dbname', 'shipping_status', 'shipping_month']]

        #ignores empty data filter in the month
        if dataAllFiltered.empty:
            logging.info("No se encontró información con los criterios de busqueda en el mes.")
            continue
        

        AllMonthsFilteredList.append(dataAllFiltered)

    if len(AllMonthsFilteredList) == 0:
        logging.warning("No se obtuvo ningún resultado con los criterios de busqueda.")
        return None
    else:
        logging.info("Información filtrada con éxito.")
        return pd.concat(AllMonthsFilteredList, ignore_index=True)
    

def main():

    logging.info("Comenzando el proceso")

    ####### Input variables

    #String connection to database, provide a correct conection to the database
    #stringConn = "dbname='postgres' user='postgres' password='password' host='localhost' port='5432'"

    #Get init parameters
    parameters = GetInitParameters()
    stringConn = parameters['string_connection']

    # (NOT modify) Query to extract orders with business logic process of extraction data, please change with correct datatable 
    OrderQuery = """Select order_vendor_dbname, shipping_status, EXTRACT(MONTH FROM shipping_date) as shipping_month
                FROM Public."Orders"
                GROUP BY order_vendor_dbname, shipping_status, EXTRACT(MONTH FROM shipping_date)
                HAVING COUNT(to_char(shipping_date, 'MONTH')) > 1 AND
                ((shipping_status = 'returned' AND Count(shipping_status) >= 2) OR
                (shipping_status = 'cancelled' AND Count(shipping_status) >= 3) )"""
    

    #Possible query for get users to send alert
    UserQuery = """SELECT * FROM Public."Users" """

    
    #Encript string connection
    creds, key = CredentialsEncrypt(stringConn)


    """Comment if database connection is used"""

    path = logDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_envios_challenge.csv")
    #path = "C:\\Users\\Wilson\\Downloads\\db_envios_challenge.csv" #Alternative for simulate a database

    

    ######## If and error o doesn't exist data, stops process 

    logging.info("Obteniendo información de pedidos...")

    """Uncomnent when use the database connection"""
    #data, error = DataBaseToDataFrame(CredentialsDecript(creds,key), OrderQuery)

    """Comment if database connection is used"""
    data, error = GetDataFromCsv(path) #Used only for simulate database without query

    if error is True:
        logging.error("No es posible acceder a la información.")
        sys.exit()
    elif data.empty:
        logging.error("No se encontraron datos.")
        sys.exit()

    """Comment if database connection is used"""
    data = BusinessProcessInExistingData(data)

    if data is None:
        print("No se encontraron datos.")
        sys.exit()
    
    #print(data.head())

    #THIS PART OF CODE IS BUILDING BECAUSE IT'S ONLY FOR A TEST, MAYBE THEY SOME THINGS COULD FAIL.
    # PLEASE UNCOMMENT UNDER YOUR OWN RESPONSIBILITY

    #For to use, you have to valide:
    # 
    #  'UserQuery' variable is a working query and get at least 'order_vendor_dbname' and emails as 'user_emails'
    #  'SendMail' function has its true parameters (host, port, passw, etc)
    #  'SendMail' function has a valid connection (No MFA, Token, secretId, etc)  

    """
    ######### Gets info of users and merge data of orders and users (Is not available yet), 

    logging.info("Obteniendo información de clientes...")
    
    dataUsers, error = DataBaseToDataFrame(CredentialsDecript(creds,key), OrderQuery)

    if error is True:
        logging.error("No es posible acceder a la información.")
        sys.exit()
    elif dataUsers.empty:
        logging.error("No se encontraron datos.")
        sys.exit()
    if dataUsers is None:
        print("No se encontraron datos.")
        sys.exit()

    #Merge data of orders and users by chunks
    dataInfo = ProcessDfInChunks(data, processingFuntion=InnerData, returned=True, df2=dataUsers, onColumnName='order_vendor_dbname')

    ############# send email to all clients

    recipies = dataInfo['user_email'].tolist()
    body = "Hi, according our information you have orders cancelled or returned in a month, please contact with support."
    subject = "Your order have an update"
    SendEmail(recipies, subject, body)


    """

    logging.info("Proceso finalizado.")




if __name__ == "__main__":
    main()





