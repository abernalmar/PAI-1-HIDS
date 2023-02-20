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
elapsed_time = time() - start_timeprint("Elapsed time: %.10f seconds." % elapsed_time)

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