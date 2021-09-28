from tkinter import *
import tkinter as tk
import time
root=Tk()

Flag = True
variable=StringVar()

def stop():
    global after_id
    global Flag
    Flag = False
    
def update_label():
    global Flag
    i=0
    while (Flag):
        i=i+1
        variable.set(str(i))
        root.update()

your_label=Label(root,textvariable=variable)
your_label.pack()
start_button=Button(root,text="start",command=update_label)
start_button.pack()

stop_frame = tk.Frame(root)
stop_frame.pack(side=tk.TOP)
stop_button = tk.Button(stop_frame, text='Stop', command = stop)
stop_button.pack(side=tk.LEFT)

root.mainloop()