#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.chrome.options import Options

from datetime import datetime
import time

import shutil
import configparser

import smtplib
from email.message import EmailMessage
import mimetypes

from PIL import Image
import io

import os




def envia_email (email, asunto, body, pantallazo=None):
    # Email settings
    sender_email = "izix.notificaciones@gmail.com"
    receiver_email = email
    password = pass_email_notif

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    if pantallazo:
        
        image_path = pantallazo
        ctype, encoding = mimetypes.guess_type(image_path)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        with open(image_path, 'rb') as fp:
            msg.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=image_path.split("/")[-1])

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg, from_addr=sender_email, to_addrs=[receiver_email])
        print("\nEmail enviado al usuario")
    except Exception as e:
        print(f"Failed to send email: {e}")







def save_screenshot(driver):
    screenshot_as_png = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot_as_png))
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGB")
    image.save(screenshot_path, 'JPEG', quality=85)


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
    envio_email = True
    print ("     envio_email: " + str(envio_email))
    
   
    # Initialize the configparser
    config = configparser.ConfigParser()
    # Read the configuration file
    config.read(config_path)

    # Now, extract the variables from the configuration file
    log = config['Paths']['log']                            # path al fichero local de logado
    screenshot_path = config['Paths']['screenshot_path']    # path al fichero local con pantallazo
    pass_email_notif = config['Settings']['pass_email_notif']                  # contraseña de email de notificaciones
    email_admin = config['Settings']['email_admin']                  # email de notificaciones
    url_evotempo = config['Paths']['url_evotempo']                            # url de la página de fichaje

    print ("\nInicia el fichaje\n")    
    
    Intentos_max = 3
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





