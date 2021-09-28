from pynput import keyboard
import tkinter as tk
import threading

# The event listener will be running in this block
Flag = True

def monitor():
    global Flag
    global var_status
    while(Flag):
        with keyboard.Events() as events:
            event = events.get(1)
            # for event in events:
            if event is None:
                print("None")
                # var_status.set("None")
                # window.update()

            else:
                if event.key == keyboard.Key.esc:
                    break
                else:
                    print('Received event {}'.format(event))
                    # var_status.set(str(event))
                    # window.update()
    print("endddddddddddddddddddddddddd")                
    # window.after(3000, monitor)     

def stop():
    global after_id
    global Flag
    Flag = False

window = tk.Tk()
window.title('Monitor')
window.geometry('800x600')                   

start_frame = tk.Frame(window)
start_frame.pack(side=tk.TOP)
start_button = tk.Button(start_frame, text='start', command = monitor)
start_button.pack(side=tk.LEFT)

stop_frame = tk.Frame(window)
stop_frame.pack(side=tk.TOP)
stop_button = tk.Button(stop_frame, text='Stop', command = stop)
stop_button.pack(side=tk.LEFT)

var_status = tk.StringVar()
var_status.set("test")
status_frame = tk.Frame(window)
status_frame.pack(side=tk.TOP)
status_frame_label_left = tk.Label(status_frame, text='status')
status_frame_label_left.pack(side=tk.LEFT)
status_frame_label_right = tk.Label(status_frame, textvariable=var_status, bg='white', fg='red', font=('Arial', 8), width=100, height=1)
status_frame_label_right.pack(side=tk.RIGHT)

t1 = threading.Thread(target = monitor)
t1.start()
window.mainloop()