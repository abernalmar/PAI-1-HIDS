from datetime import datetime
import threading
import os

current_path = os.path.dirname(os.path.abspath(__file__))
PERIOD = 10  #10 segundos es 1 día


#Crea una tabla HTML con los encabezados, la fecha del informe y los datos proporcionados.
#Cada fila de datos se representa como una fila. Crea el HTML que se mostrará en los informes generados por el script.
def create_table_html(headers,report, data):
    pre_existing_template="""
    <!DOCTYPE html> 
        <html> 
            <head>
                <style>
                    table, th, td {border: 1px solid black;border-collapse: collapse;border-spacing:8px}
                </style>
            </head>
            <body>
    """
    pre_existing_template+= "<strong>" + "REPORT DATE: " + report + "</strong>" 
    pre_existing_template+="""
                <table style='width:50%'>
                    <tr>
    """
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
        
    pre_existing_template+="""
                </table> 
            </body> 
        </html>
    """
    return(pre_existing_template)

#Busca en el archivo changes.log los cambios que han ocurrido en los últimos 20 segundos.
#Si hay cambios, se crea un archivo HTML en la carpeta reports que muestra una tabla con los detalles de los cambios.
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
        file = open(current_path + "/reports/" + name, "w")
        file.write(create_table_html(["Timestamp","File Name","Last Hash Calculated"], name[:-4], changes))
        file.close()