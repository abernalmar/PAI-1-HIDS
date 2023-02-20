from save_files import *
import os
import threading
from report import *
from time import time
import sys, signal

def sig_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)
start_time = time()

dicc = save_files()
elapsed_time = time() - start_time
print("Elapsed time: %.10f seconds." % elapsed_time)

current_path = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(current_path+"/resources")


def timer():
    threading.Timer(2, timer).start()
    for file in FILES:
        check_data = check_digest(file, dicc)
        if len(check_data) > 0:
            write_log(check_data)

remove_log_content()
timer()
populate_html()

'''
-sig_handler: Esta función maneja las señales y se utiliza para detener el programa de forma segura 
cuando se recibe una señal SIGINT (por ejemplo, al presionar Ctrl + C en la terminal). 
Imprime un mensaje de salida y luego llama a sys.exit para terminar el programa.

-save_files: Esta función se utiliza para crear un diccionario que contiene la información de cada
archivo en un directorio. El diccionario tiene como claves los nombres de los archivos y como 
valores una tupla que contiene el hash SHA-256 del archivo y la fecha y hora de la última modificación.

-check_digest: Esta función se utiliza para verificar si se han producido cambios en un archivo
desde la última vez que se comprobó. Compara el hash SHA-256 actual del archivo con el hash almacenado 
en el diccionario creado por save_files. Si los hash no coinciden, devuelve una tupla que contiene el 
nombre del archivo, la fecha y hora de la última modificación y la cadena "File changed". Si los hash 
coinciden, no devuelve nada.

-write_log: Esta función se utiliza para escribir un registro en un archivo de registro cuando se 
detecta un cambio en un archivo.

-remove_log_content: Esta función se utiliza para vaciar el contenido del archivo de registro.

-timer: Esta función se utiliza para programar una tarea que se ejecutará cada 2 segundos. 
Cada vez que se ejecuta, recorre todos los archivos en el directorio y verifica si alguno ha 
cambiado desde la última comprobación. Si se detecta un cambio, se escribe un registro en el
archivo de registro utilizando la función write_log.

-populate_html: Esta función se utiliza para generar un archivo HTML que muestra el contenido 
del archivo de registro en una tabla.
'''