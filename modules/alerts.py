"""
Author: Wilson Vargas
Date created: 13/11/2023
contact: w.andres.vr@gmail.com

Dependecies:
- Pandas
- psycopg2
- cryptography
- logging

Use: Functions of the alerts in the code.
"""
import logging
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .funtions import GetInitParameters


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename=GetLogName(),
    #filemode='a'
)

def SendEmail(recipients, subject, body, html=False):

    emailParameters = GetInitParameters

    logging.info("Enviando correo...")

    # Config Gmail SMTP
    smtpServer = emailParameters['smtp_server']
    port = emailParameters['smtp_port']
    user = emailParameters['smtp_user']
    passw = emailParameters['smtp_passw']

    # Build the message
    message = MIMEMultipart()
    message['From'] = user
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    #validate if is HTML format
    if html is True:
        message.attach(MIMEText(body, 'plain'))
    else:
         message.attach(MIMEText(body, 'html'))

    # Init SMTP
    try:
        with smtplib.SMTP(smtpServer, port) as server:
            server.starttls()  # Secure mode (TLS)
            server.login(user, passw)

            # Send mail
            server.sendmail(user, recipients, message.as_string())

        logging("Correo enviado con éxito.")

    except Exception as e:
        logging.error("Ocurrió un error al enviar el correo.")
        logging.error(f'Error en la función: {e}', exc_info=True)
        pass


