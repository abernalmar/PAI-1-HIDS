from save_files import *
import os
import threading
from time import time
import sys, signal
from report import *
from report_mensual import *

#Para poder salir del programa al hacer Ctrl + C en la terminal
def sig_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)
start_time = time()

#saves_files:crear un diccionario que contiene la información de cada archivo. Claves: nombres de los archivos, Valores: tupla que contiene el hash SHA-256 del archivo y la fecha y hora de la última modificación.
dicc = save_files()
#Tiempo transcurrido
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)

current_path = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(current_path+"/resources")

#Cada 2 segundos, recorre todos los archivos en el directorio y verifica si alguno ha cambiado desde la última comprobación.
#Si se detecta un cambio, se escribe un registro en el archivo de registro utilizando la función write_log.
def timer():
    threading.Timer(2, timer).start()
    for file in FILES:
        check_data = check_digest(file, dicc)
        if len(check_data) > 0:
            write_log(check_data)

remove_log_content()
timer()
populate_html()
populate_html_mensual()


