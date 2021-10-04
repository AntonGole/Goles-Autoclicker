from tkinter.ttk import Frame, Button, Entry, Style
from random import *
from tkinter import *
from pyautogui import *
import time
import threading
from pynput.keyboard import Key, Listener

staticDelay = 0
delay = 0
clicking = False
double_click_delay = 0


def start_clicking():
    print("Start button pressed")
    start.focus_set()
    global clicking
    if clicking:
        return
    clicking = True
    for tf in tfList:
        if tf.get() == '':
            tf.insert(0, "0")

    global staticDelay
    staticDelay = int(tfList[0].get()) * 60000 + (int(tfList[1].get()) * 1000) + (int(tfList[2].get())) / 1000
    global double_click_delay
    double_click_delay = randint(128, 315)
    if staticDelay == 0:
        return
    else:
        print("Clicking started")
        calculate_new_delay()
        left_click()


# Start clicking with delay calculated by the calculate_new_delay function
def left_click():
    if clicking:
        timer = threading.Timer(delay, left_click)
        timer.start()
        click()
        calculate_new_delay()


# Stop clicking
def stop_clicking():
    print("Stop clicking pressed")
    global clicking
    clicking = False
    print("Clicking stopped")
    # double_click()


# Double click (delay between clicks from 128ms to 315ms)
def double_click():
    timer = threading.Timer(double_click_delay, click)
    timer.start()
    click()
    calculate_new_double_click()


def test():
    timer1 = threading.Timer(5, double_click)
    timer1.start()


# Calculate a random delay from minutes, seconds and milliseconds
def random_delay(minutes, seconds, millis):
    totalMs = minutes * 60000 + seconds * 1000 + millis
    return randint(0, totalMs)


# Calculate the next delay using the random_delay function and the staticDelay variable
def calculate_new_delay():
    global delay
    delay = ((staticDelay + random_delay(int(tfList[3].get()), int(tfList[4].get()), int(tfList[5].get())) - 11) / 1000)


def calculate_new_double_click():
    global double_click_delay
    double_click_delay = randint(128, 315) / 1000


# Check if character typed is an integer and that only one "0" is typed in the beginning of the number
def is_valid_input(new, old):
    try:
        int(new)
        if new[-1] == "0" and old == "0":
            return False
        else:
            return True
    except ValueError:
        if new == '':
            return True
        else:
            return False


# Create necessary text fields and bind them to functions remove_all, add_zero and remove_zero
def create_textfields():
    for i in range(6):
        tf = Entry(root, bg="#301B3F", fg="#B4A5A5", validatecommand=(is_valid_command, '%P', '%s'), validate='key')
        tfList.append(tf)

        def remove_all(event, self=tf):
            self.delete(0, END)

        def add_zero(event, self=tf):
            if self.get() == "":
                self.insert(0, "0")

        def remove_zero(event, self=tf):
            if self.get() == "0":
                self.delete(0, END)

        tf.insert(0, "0")
        tf.bind('<FocusIn>', remove_all)
        tf.bind('<FocusOut>', add_zero)
        tf.bind('<KeyPress>', remove_zero)


# Function for listening to keypresses, will be running on a different thread
def input_thread():
    # The key combinations to check
    SHIFT_F1 = {Key.f1, Key.shift}
    SHIFT_F2 = {Key.f2, Key.shift}

    # The currently active modifiers
    current = set()

    # Handling on keypress and on keyrelease event
    def on_press(key):
        if key in SHIFT_F1:
            current.add(key)
            print(current)
            if all(k in current for k in SHIFT_F1):
                print("test")
                start_clicking()
        elif key in SHIFT_F2:
            current.add(key)
            if all(k in current for k in SHIFT_F2):
                stop_clicking()

    def on_release(key):
        try:
            current.remove(key)
        except KeyError:
            pass

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()


if __name__ == '__main__':
    # declare the window
    root = Tk()
    is_valid_command = root.register(is_valid_input)
    tfList = []

    # Creating thread for listening to keys
    thread = threading.Thread(target=input_thread, args=(), daemon=True)
    thread.start()

    # declare buttons
    start = Button(root, text="Start (SHIFT+F1)", bg="#301B3F", command=start_clicking)
    start.configure(height=2, width=14, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    start.grid(row=0, column=0, padx=10, pady=20)

    stop = Button(root, text="Stop (SHIFT+F2)", bg="#301B3F", command=stop_clicking)
    stop.configure(height=2, width=14, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    stop.grid(row=0, column=1, padx=10, pady=20)

    # declare text fields
    create_textfields()
    for i in range(6):
        if i < 3:
            tfList[i].grid(row=2, column=i % 3, pady=(0, 20))
        else:
            tfList[i].grid(row=4, column=i % 3)

    # declare labels
    labelMin = Label(root, text="Minutes", bg="#301B3F", fg="#B4A5A5", height=1, width=14)
    labelMin.grid(row=1, column=0)
    labelSec = Label(root, text="Seconds", bg="#301B3F", fg="#B4A5A5")
    labelSec.grid(row=1, column=1)
    labelMs = Label(root, text="Milliseconds", bg="#301B3F", fg="#B4A5A5")
    labelMs.grid(row=1, column=2)

    labelRMin = Label(root, text="Random Minutes", bg="#301B3F", fg="#B4A5A5", height=1, width=14)
    labelRMin.grid(row=3, column=0)
    labelRSec = Label(root, text="Random Seconds", bg="#301B3F", fg="#B4A5A5")
    labelRSec.grid(row=3, column=1)
    labelRMs = Label(root, text="Random Milliseconds", bg="#301B3F", fg="#B4A5A5")
    labelRMs.grid(row=3, column=2)

    # set window title
    root.title("Goles Autoclicker")
    # set window width and height
    root.geometry("1000x600")
    root.resizable(False, False)
    # set window background color
    root.configure(bg='#3C415C')
    # move window center
    winWidth = root.winfo_reqwidth()
    winwHeight = root.winfo_reqheight()
    posRight = int(root.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(root.winfo_screenheight() / 2 - winwHeight / 2)
    root.geometry("+{}+{}".format(posRight, posDown))
    root.mainloop()
