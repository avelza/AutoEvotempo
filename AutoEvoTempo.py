#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.chrome.options import Options

from datetime import datetime
import time

import configparser

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import mimetypes

from PIL import Image
import io

import os




def envia_email (email, asunto, body, pantallazo=None):
    # Email settings
    sender_email = email_notif
    password = pass_email_notif
    receiver_email = email
    

    # Create the email message
    if pantallazo:
        msg = MIMEMultipart('related')
        msg['Subject'] = asunto
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # HTML body with image
        html_body = f"""
        <html>
            <body>
                <p>{body}</p>
                <img src="cid:image1" style="width: 50%; height: auto;">
            </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

        # Open the screenshot image to embed
        image_path = pantallazo
        ctype, encoding = mimetypes.guess_type(image_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        
        maintype, subtype = ctype.split("/", 1)
        with open(image_path, 'rb') as fp:
            img = MIMEImage(fp.read(), _subtype=subtype)
            img.add_header('Content-ID', '<image1>')  # Use this 'Content-ID' in the HTML img src
            msg.attach(img)
    else:
        msg = EmailMessage()
        msg['Subject'] = asunto
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(body)

    # Send the message via SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email enviado")
    except Exception as e:
        print(f"Fallo al enviar el email: {e}")



def save_screenshot(driver):
    screenshot_as_png = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot_as_png))
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGB")
    
    # Calcula tamaño reducido (50% of the original size)
    original_width, original_height = image.size
    new_width = original_width // 2
    new_height = original_height // 2
    
    # Redimensiona la imagen
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # guarda la imagen resultante
    resized_image.save(screenshot_path, 'JPEG', quality=85)


def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def abrir_pagina(driver):
    driver.get (url_evotempo)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@src='/ka/apps/wm/assets/logo.svg']"))
        )
        # print("Page has rendered and the specific element is present.")
        print ("-> página abierta")
    except TimeoutException:
        print("-> No se ha podido cargar la página")
        raise TimeoutException ("Timeout en carga de página EvoTempo")

def clicar_iniciar (driver):
    try:
        # Espera hasta que el elemento sea clicable
        iniciar_turno_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'clock_action') and .//span[contains(text(), 'Iniciar turno')]]"))
        )
        # Hacer clic en el elemento una vez que está disponible
        iniciar_turno_btn.click()
        print ("-> botón clicado")
    except TimeoutException:
        print("-> El botón para iniciar turno no estuvo disponible después de 10 segundos.")
        raise TimeoutException ("Timeout, botón de Iniciar Turno no disponible")

def clicar_iniciar2 (driver):
    try:
        # Wait for up to 10 seconds for the button to be clickable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-action='clock-in']"))
        )
        # Click the button
        button.click()
        print("-> botón clicado")
    except TimeoutException:
        print("-> Timed out waiting for the button to become clickable.")
        raise TimeoutException ("Timeout, segundo botón de Iniciar Turno no disponible")
    except NoSuchElementException:
        print("-> The button was not found on the page.")
        raise
    except Exception as e:
        print(f"-> An unexpected error occurred: {e}")
        raise

def ficha ():
    # abre página
    driver = setup_driver()
    try:
        print ("abriendo página")
        abrir_pagina(driver)
          
        print ("clicando en Inicar Turno")
        clicar_iniciar (driver)

        print ("clicar otra vez en la siguiente página")
        clicar_iniciar2 (driver)

        resultado = "OK"

    
    except TimeoutException as e:
        resultado = "ERROR timeout: " + str(e)
        print(resultado)
            
    except Exception as e:
        resultado = "ERROR: " + str(e)
        print(resultado)

   
    # guarda un pantallazo
    print (f"Resultado del fichaje de hoy: " + resultado)
    print ("guardando pantallazo\n")
    time.sleep (2)
    save_screenshot(driver)

    
    # driver.delete_all_cookies()
    driver.quit()

    return resultado




######################################################################################

# Código principal



if __name__ == "__main__":

    print ("\n\nInicio\n")
  
    # Ajustes
    print ("Ajustes:")
    config_dir = os.getenv('evotempo_path')    # extraigo el path del fichero de config de variables de entorno os
    config_path = config_dir + '/config.txt' # if config_dir else None
    if config_path:
        print(f"     evotempo_path:{config_path}")
    else:
        print("     evotempo_path: environment variable not set.")
    
    # Initialize the configparser
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read(config_path)

    try:
        # Now, extract the variables from the configuration file
        url_evotempo = config['Paths']['url_evotempo']                            # url de la página de fichaje
        log = config['Paths']['log']                            # path al fichero local de logado
        screenshot_path = config['Paths']['screenshot_path']    # path al fichero local con pantallazo
        pass_email_notif = config['Settings']['pass_email_notif']                  # contraseña de email de notificaciones
        envio_email = config.getboolean('Settings', 'envio_email')                 # envio de notificaciones por email
        email_admin = config['Settings']['email_admin']                  # email de admin
        email_notif = config['Settings']['email_notif']                  # email de notificaciones
        
        print ("     envio_email: " + str(envio_email))
    except configparser.NoSectionError:
        # Handle the case where the section is not found
        print('Error, falta una sección en el fichero de config')
    except configparser.NoOptionError:
        # Handle the case where the option within the section is not found
        print('Error, falta una opción en el fichero de config')

    print ("\nInicia el fichaje\n")    
    
    Intentos_max = 1
    intentos = 0
    while intentos < Intentos_max:
        print ("Intento: ", intentos+1)
        resultado = ficha ()
        if resultado == "OK":
            break
        else:
            intentos += 1
            if intentos == Intentos_max:
                    print ("Intentos máximos alcanzados")
        
        
    # guarda en log
    print("guardando el log")
    entrada_log = f"{datetime.now().strftime('%Y-%m-%d, %H:%M:%S')}, \t\tresultado: {resultado} \n"

    # Asegúrate de que el log.txt existe, si no, lo creas, y añades entrada de log
    try:
        with open(log, 'r') as file:
            original_content = file.read()
        with open(log, 'w') as file:
            file.write(entrada_log + original_content)      # para escribir la última entrada arriba
    except FileNotFoundError:
        with open(log, 'w') as file:
            file.write(entrada_log)

    # envía un correo con el resultado
    body = f"Resultado del fichaje automático: " + resultado
    asunto = "Fichaje automático EvoTempo"
    # print ("enviando resumen a admin")
    if envio_email:
        envia_email (email_admin, asunto, body, screenshot_path)

    print ("\nFin\n")





