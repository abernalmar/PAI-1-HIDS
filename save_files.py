import hashlib
import os
from datetime import datetime

# Global variables
FILES = os.listdir('./resources')
global DICC_HASH
DICC_HASH = dict()

def get_name(file):
    return os.path.splitext(file)[0]

def get_extension(file):
    return os.path.splitext(file)[1]

def save_files():
    for f in FILES:
        file_path = './resources/' + f
        extension = get_extension(f)
        name = get_name(f)
        if not DICC_HASH.get(extension):
            DICC_HASH[extension] = {name: digest(file_path)}
        else:
            DICC_HASH[extension][name] = digest(file_path)
    return DICC_HASH

#Verifica si el archivo especificado tiene el mismo hash SHA-256 que el valor hash almacenado en el diccionario.
def check_digest(file, dicc):
    file_path = './resources/' + file
    extension = get_extension(file)
    name = get_name(file)
    actual_hexdigest = digest(file_path)
    original_hexdigest = dicc[extension][name]
    if actual_hexdigest != original_hexdigest:
        date_time_obj = datetime.now()
        timestamp = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")
        return [timestamp, name+extension, actual_hexdigest]
    return []

def remove_log_content():
    with open("changes.log", "w") as f:
        f.truncate()

#Escribe una entrada en un archivo de registro ('changes.log') que contiene la fecha y hora de la comprobación, el nombre del archivo comprobado y el resultado de la comprobación
def write_log(check_data):
    try:
        with open('changes.log', 'r+') as f:
            line_found = any(check_data[1] + ', ' + check_data[2] + '\n' in line for line in f)
            if not line_found:
                f.seek(0, os.SEEK_END)
                f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')
    except:
        with open('changes.log', 'a') as f:
            f.write(check_data[0] + ', ' + check_data[1] + ', ' + check_data[2] + '\n')

#La función digest(path) calcula el hash SHA-256 de un archivo que se encuentra en la ruta especificada por el parámetro path.
def digest(path):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    with open(path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()