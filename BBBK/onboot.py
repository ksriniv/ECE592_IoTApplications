import threading
from subprocess import call
from main import LampSaver
from user_data_server import main as live_data_server
#from MYOlib.gesture import main as gesture_main

call(["gcc", "navigation.c", "-o", "nav", "-lm"])
#call(["bash", "./init.sh"])
#call(["bash", "./als_init"])

#p3 = threading.Thread(target=gesture_main)
#p3.start()

ls = LampSaver(debug=True)
p1 = threading.Thread(target=ls.main)
p1.start()

#p2 = threading.Thread(target=live_data_server)
#p2.start()

try:
    call(["python2", "./MYOlib/gesture.py"])
except Exception as e:
    print(e)

