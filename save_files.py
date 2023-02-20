import hashlib
import os
from datetime import datetime


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(CURRENT_PATH+"/resources")
DICC_HASH = dict()
alg_cript = input("Algoritmo criptográfico a usar (SHA-256 (default), SHA-512, SHA3-256, SHA3-512): ")

#Obtener el nombre del archivo sin su extensión.
def get_name(file):
    return os.path.splitext(file)[0]

#Obtener la extensión del archivo.
def get_extension(file):
    return os.path.splitext(file)[1]

#Guardar los hash de los archivos en el diccionario global
def save_files():
    for f in FILES:
        file_path = CURRENT_PATH + "/resources/" + f
        extension = get_extension(f)
        name = get_name(f)
        if not DICC_HASH.get(extension):
            DICC_HASH[extension] = {name: digest(file_path,alg_cript)}
        else:
            DICC_HASH[extension][name] = digest(file_path,alg_cript)
    return DICC_HASH

#Verifica si el archivo especificado tiene el mismo hash SHA-256 que el valor hash almacenado en el diccionario.
#Si los hash no coinciden, devuelve una tupla que contiene el nombre del archivo, la fecha y hora de la última modificación y la cadena "File changed".
#Si los hash coinciden, no devuelve nada.
def check_digest(file, dicc):
    file_path = './resources/' + file
    extension = get_extension(file)
    name = get_name(file)
    actual_hexdigest = digest(file_path,alg_cript)
    original_hexdigest = dicc[extension][name]
    if actual_hexdigest != original_hexdigest:
        date_time_obj = datetime.now()
        timestamp = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")
        return [timestamp, name+extension, actual_hexdigest]
    return []

#Borra el contenido de changes.log
def remove_log_content():
    with open(CURRENT_PATH+"/changes.log", "w") as f:
        f.truncate()

#Escribe una entrada en un archivo de registro ('changes.log') que contiene la fecha y hora de la comprobación, el nombre del archivo comprobado y el resultado de la comprobación
def write_log(check_data):
    try:
        with open(CURRENT_PATH+'/changes.log', 'r+') as f:
            line_found = any(check_data[1] + ', ' + check_data[2] + '\n' in line for line in f)
            if not line_found:
                f.seek(0, os.SEEK_END)
                f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')
    except:
        with open(CURRENT_PATH+'/changes.log', 'a') as f:
            f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')

#La función digest(path) calcula el hash SHA-256 de un archivo que se encuentra en la ruta especificada por el parámetro path.
def digest(path,alg):
    BLOCK_SIZE = 65536
    file_hash = hashlib.sha256()
    if alg=="SHA-512":
        file_hash = hashlib.sha512()
    elif alg=="SHA3-256":
        file_hash = hashlib.sha3_256()
    elif alg=="SHA3-512":
        file_hash = hashlib.sha3_512()
    with open(path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()
