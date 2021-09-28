import tkinter as tk
import time

after_id = None
Flag = True

def Refresher():
    global status_frame_label_right
    status_frame_label_right.configure(text="end")
    print("end")
    # window.after(3000, Refresher) # every second...

def hello():
    global after_id

    print("hello")
    if(Flag):
        window.after(1000, hello)
    # after_id = window.after(1000, hello)
    print(after_id)
    # while(flag):
    #     time.sleep(1)
    #     print("hello")
# def stop_monitor():
def stop():
    global after_id
    global Flag
    Flag = False
    # if after_id:
    #     window.after_cancel(after_id)
    #     after_id = None

flag = True    
window = tk.Tk()
window.title('Monitor')
window.geometry('800x600')

var_status = tk.StringVar()
var_status.set("test")
status_frame = tk.Frame(window)
status_frame.pack(side=tk.TOP)
status_frame_label_left = tk.Label(status_frame, text='status')
status_frame_label_left.pack(side=tk.LEFT)
status_frame_label_right = tk.Label(status_frame, text="start", bg='white', fg='red', font=('Arial', 8), width=100, height=1)
status_frame_label_right.pack(side=tk.RIGHT)

stop_frame = tk.Frame(window)
stop_frame.pack(side=tk.TOP)
stop_button = tk.Button(stop_frame, text='Stop', command = stop)
stop_button.pack(side=tk.LEFT)

start_frame = tk.Frame(window)
start_frame.pack(side=tk.TOP)
start_button = tk.Button(start_frame, text='start', command = hello)
start_button.pack(side=tk.LEFT)

window.after(3000, Refresher)
window.mainloop()
# hello()
# Refresher()

# message()

# def Draw():
#     global text

#     frame=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
#     frame.place(x=10,y=10)
#     text=tk.Label(frame,text='HELLO')
#     print("hello")
#     text.pack()

# def Refresher():
#     global text
#     text.configure(text=time.asctime())
#     root.after(1000, Refresher) # every second...

# root=tk.Tk()
# Draw()
# Refresher()
# root.mainloop()