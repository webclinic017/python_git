import threading
import time

def hello():
    global Flag
    global Flag2

    t = threading.Thread(target=stop)
    t.start()
    print("hello")
    time.sleep(10)
    Flag = False
    Flag2 = False

def stop():
    global Flag
    global Flag2

    while(Flag):
        print("stop")
        time.sleep(1)

Flag = True
Flag2 = True

def go():
    while (Flag2):
        hello()

t1 = threading.Thread(target=go)
t1.start()