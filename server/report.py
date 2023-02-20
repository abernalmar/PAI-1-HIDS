import threading
import datetime
from datetime import datetime
import os

current_path=os.path.dirname(os.path.abspath(__file__))

PERIOD = 20

#Esta la podemos refatorizar para no repetir código
def create_table_html(headers,report, data):
    pre_existing_template="<!DOCTYPE html>" + "<html>" + "<head>" + "<style>"
    pre_existing_template+="table, th, td {border: 1px solid black;border-collapse: collapse;border-spacing:8px}"
    pre_existing_template+="</style>" + "</head>"
    pre_existing_template+="<body>" + "<strong>" + "REPORT DATE: " + report + "</strong>" 
    pre_existing_template+="<table style='width:50%'>"
    pre_existing_template+='<tr>'
    for header_name in headers:
        pre_existing_template+="<th style='background-color:#3DBBDB;width:85;color:white'>" + header_name + "</th>"
    pre_existing_template+="</tr>"
    for d in data:
        sub_template="<tr style='text-align:center'>"
        sub_template+="<td>" + str(d[0]) + "</td>"
        sub_template+="<td>" + str(d[1]) + "</td>"
        sub_template+="<td>" + str(d[2]) + "</td>"
        sub_template+="<tr/>"
        pre_existing_template+=sub_template
    pre_existing_template+="</table>" + "</body>" + "</html>"
    return(pre_existing_template)

#Se puede refactorizar
def populate_html():
    threading.Timer(PERIOD, populate_html).start()
    changes=[]
    for linea in reversed(list(open(current_path+"/changes.log"))):
        change=linea.split(", ")
        date_time_obj = datetime.strptime(change[0], "%d-%b-%Y (%H:%M:%S)")
        actual_date= datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
        actual_date_obj = datetime.strptime(actual_date, "%d-%b-%Y (%H:%M:%S)")
        diff=actual_date_obj - date_time_obj
        if (diff.seconds<=PERIOD):
            changes.append(change)

    if len(changes)>0:
            name=str(datetime.today().strftime("%d-%b-%Y-%H-%M-%S"))+".html"
            f = open(current_path + "/reports/" + name, "w")
            f.write(create_table_html(["Timestamp","File Name","Last Hash Calculated"], name[:-4], changes))
            file.close()

'''
Este programa es un script de Python que tiene dos funciones principales: create_table_html y populate_html.

La primera función, create_table_html, es una función que toma como entrada una lista de encabezados, 
una cadena de fecha y hora (el "informe"), y una lista de datos. Esta función crea una tabla HTML con los
encabezados, la fecha del informe y los datos proporcionados. Cada fila de datos se representa como una 
fila en la tabla HTML. Esta función se utiliza para crear el HTML que se mostrará en los informes generados
por el script.

La segunda función, populate_html, es una función que se ejecuta periódicamente y se encarga de buscar en el
archivo changes.log los cambios que han ocurrido en los últimos 20 segundos. Si hay cambios que cumplen con
esta condición, se crea un archivo HTML en la carpeta reports que muestra una tabla con los detalles de los
cambios. Esta función utiliza la función create_table_html para crear la tabla HTML para los informes. 
La función populate_html se ejecuta cada 20 segundos utilizando un temporizador de subproceso para 
actualizar continuamente el archivo HTML de informes.
'''