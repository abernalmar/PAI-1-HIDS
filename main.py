from save_files import *
import os
import threading
from report import *

global dicc
dicc = save_files()

FILES = os.listdir('./resources')


def timer():
    threading.Timer(2, timer).start()
    for file in FILES:
        check_data = check_digest(file, dicc)
        if len(check_data) > 0:
            write_log(check_data)

remove_log_content()
timer()
populate_html()