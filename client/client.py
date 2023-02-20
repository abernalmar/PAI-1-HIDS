import uuid
import os
import hashlib
from colorama import Fore, init, Style
init()

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
FILES = os.listdir(CURRENT_PATH+"/resources")
alg_cript = input("Algoritmo criptográfico a usar (SHA-256 (default), SHA-512, SHA3-256, SHA3-512): ")

def token():
  token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
  if(alg_cript=="SHA-512" or alg_cript=="SHA3-512"):
    token=str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")+str(uuid.uuid4()).replace("-","")
  return token

def digest(path,alg):
    BLOCK_SIZE = 65536 
    file_hash = hashlib.sha256()
    if alg=="SHA-512":
        file_hash = hashlib.sha512()
    elif alg=="SHA3-256":
        file_hash = hashlib.sha3_256()
    elif alg=="SHA3-512":
        file_hash = hashlib.sha3_512()
    with open(CURRENT_PATH+"/resources/"+path, 'rb') as f: 
        fb = f.read(BLOCK_SIZE) 
        while len(fb) > 0: 
            file_hash.update(fb) 
            fb = f.read(BLOCK_SIZE)
    return file_hash.hexdigest()

def rotar_izquierda(cadena, posiciones):
  return cadena[posiciones:] + cadena[:posiciones]

def challenge(hash,token):
        mac = hex(int(hash, 16) + int(token, 16))[2:]
        mac_rot13= rotar_izquierda(mac, 13)
        mac_par=mac_rot13[1::2]
        mac_sim=''.join(reversed(mac_par))
        return mac_sim

for file in FILES:
        hash = digest(file,alg_cript)
        filename= file
        tokenization=token()
        mac=challenge(hash,tokenization)

        with open(CURRENT_PATH + '/../communication.txt', 'w') as f:
          f.write("-- CLIENT -- \n")
          f.write("FILE: "+filename+'\n')
          f.write("HASH: "+hash+'\n')
          f.write("TOKEN: "+ tokenization+'\n')
        f.close()
        mac_server=""
        hash_server=""
        error=""
        while True:
          with open(CURRENT_PATH + '/../communication.txt', 'r') as f:
            for linea in f:
              if "-- SERVER --" in linea:
                for linea in f:
                  try:
                    if linea.startswith("VERIFICATION FAILED"):
                      error=linea
                    if linea.startswith("HASH_FROM_SERVER:"):
                      hash_server=linea.split(":")[1].strip()
                    if linea.startswith("MAC_FROM_SERVER:"):
                      mac_server=linea.split(":")[1].strip()
                  except:
                    print("Something went wrong ...")
          if(hash_server!=""):
            break
          f.close()
        if(mac_server==mac and error==""):
          print(Style.RESET_ALL + filename + " →" , Fore.GREEN + "INTEGRITY OK")
        else:
          print(Style.RESET_ALL + filename+" →" , Fore.RED + "INTEGRITY FAIL")

'''
Este programa se encarga de realizar la integridad de los archivos de la carpeta "resources" 
utilizando diferentes algoritmos criptográficos, y luego se comunica con un servidor para 
verificar la integridad de los archivos. Para hacer esto, el programa sigue los siguientes pasos:

-Obtiene el directorio actual y los archivos en la carpeta "resources".
-Solicita al usuario que ingrese el algoritmo criptográfico que se utilizará para la integridad (SHA-256, SHA-512, SHA3-256 o SHA3-512).
-Define una función para generar un token único utilizando la biblioteca uuid.
-Define una función para calcular el hash del archivo utilizando el algoritmo seleccionado.
-Define una función para generar un código de autenticación (MAC) a partir del hash y el token utilizando 
operaciones como rotación a la izquierda, concatenación y reversión de cadenas.
-Para cada archivo en la carpeta "resources", el programa calcula el hash y el MAC y los escribe en un 
archivo "communication.txt" para enviarlos al servidor.
-El programa espera a recibir una respuesta del servidor en el archivo "communication.txt", incluyendo 
el hash calculado por el servidor y el MAC generado por el servidor.
-El programa verifica si el hash y el MAC recibidos del servidor coinciden con los que se calcularon 
localmente. Si la verificación falla, se informa al usuario que la integridad ha fallado para ese archivo. 
Si la verificación es exitosa, se informa al usuario que la integridad es correcta para ese archivo.
'''