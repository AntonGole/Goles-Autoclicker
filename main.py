from tkinter.ttk import Frame, Button, Entry, Style
from random import *
from tkinter import *
from tkinter import ttk
import pickle
import os

from PIL import ImageTk
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
    root.focus_set()

    global staticDelay
    staticDelay = int(tfList[0].get() or 0) * 60000 + (int(tfList[1].get() or 0) * 1000) + (int(tfList[2].get() or 0))
    if staticDelay == 0:
        return

    start.configure(bg="#5e5e5e", cursor="arrow")
    disable_widgets()
    stop.configure(bg="#2d7c9d", cursor="hand2")

    global clicking
    for tf in tfList:
        if tf.get() == '':
            tf.insert(0, "0")

    global double_click_delay
    double_click_delay = randint(128, 315) / 1000

    if myCombo.get() == "Left click":
        print("Clicking started")
        clicking = True
        calculate_new_delay()
        left_click_start()
        start_timer(int(tfList[6].get()))

    elif myCombo.get() == "Double click":
        print("Double clicking started")
        clicking = True
        calculate_new_delay()
        double_click_start()
        start_timer(int(tfList[6].get()))


# Start clicking with delay calculated by the calculate_new_delay function
def left_click_start():
    print("left_click_start()")
    if clicking:
        timer = threading.Timer(delay, left_click_start)
        timer.daemon = True
        timer.start()
        click()
        calculate_new_delay()


# Start double clicking with delay calculated by the calculate_new_delay function
def double_click_start():
    print("double_click_start()")
    print("New delay: {}, Double click delay: {}".format(delay, double_click_delay))
    if clicking:
        timer = threading.Timer(delay, double_click_start)
        timer.daemon = True
        timer.start()
        double_click()
        calculate_new_delay()


# Stop clicking
def stop_clicking():
    print("Stop clicking pressed")
    start.configure(bg="#2d7c9d", cursor="hand2")
    enable_widgets()
    stop.configure(bg="#5e5e5e", cursor="arrow")
    root.focus_set()
    global clicking
    clicking = False
    global current_mode
    current_mode = 0
    print("Clicking stopped")


# Double click (delay between clicks from 128ms to 315ms)
def double_click():
    print("double_click()")
    if clicking:
        timer = threading.Timer(double_click_delay, click)
        timer.daemon = True
        timer.start()
        click()
        calculate_new_double_click()


def start_timer(seconds):
    if not seconds == 0:
        timer = threading.Timer(seconds, stop_clicking)
        timer.daemon = True
        timer.start()


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
        elif len(new) > 6:
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
    for i in range(7):
        tf = Entry(tFrame, bg="#2d7c9d", validatecommand=(is_valid_command, '%P', '%s'), validate='key',
                   disabledbackground="#5e5e5e", disabledforeground="#404040")
        tf.configure(width=12)
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
        tf.bind('<Enter>', highlight)
        tf.bind('<Leave>', unhighlight)


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
            if all(k in current for k in SHIFT_F1) and start["state"] == NORMAL:
                start_clicking()
        elif key in SHIFT_F2:
            current.add(key)
            if all(k in current for k in SHIFT_F2) and stop["state"] == NORMAL:
                stop_clicking()

    def on_release(key):
        try:
            current.remove(key)
        except KeyError:
            pass

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()


def exit_function():
    save_data()
    global clicking
    clicking = False
    root.destroy()


def save_data():
    numbers = []
    for number in tfList:
        numbers.append(int(number.get()))
    numbers.append(myCombo.get())
    pickle.dump(numbers, open("data.dat", "wb"))


def load_data():
    numbers = pickle.load(open("data.dat", "rb"))
    for x in range(7):
        tfList[x].delete(0, END)
        tfList[x].insert(0, numbers[x])
    myCombo.current(options.index(numbers[7]))


def disable_widgets():
    start["state"] = DISABLED
    start["text"] = "Clicking"
    start["cursor"] = "arrow"
    stop["state"] = NORMAL
    stop["cursor"] = "hand2"
    disable_combobox()
    for x in tfList:
        x["state"] = DISABLED
        x["cursor"] = "arrow"


def enable_widgets():
    start["state"] = NORMAL
    start["text"] = "Start (SHIFT+F1)"
    start["cursor"] = "hand2"
    stop["state"] = DISABLED
    stop["cursor"] = "arrow"
    enable_combobox()
    for x in tfList:
        x["state"] = NORMAL
        x["cursor"] = "xterm"


def disable_combobox():
    myCombo["state"] = "disabled"
    combostyle_disabled.theme_use('combostyle_disabled')


def enable_combobox():
    myCombo["state"] = "readonly"
    combostyle_enabled.theme_use('combostyle_enabled')


def highlight(event):
    if event.widget["state"] == NORMAL:
        event.widget["bg"] = "#61afd1"


def unhighlight(event):
    if event.widget["state"] == NORMAL:
        event.widget["bg"] = "#2d7c9d"


# Remove focus from entries etc. when clicking outside the widget
def click_event(event):
    x, y = root.winfo_pointerxy()
    widget = root.winfo_containing(x, y)
    if widget == root or widget == tFrame or widget != root.focus_get():
        root.focus()


if __name__ == '__main__':
    # Set global variables
    staticDelay = 0
    delay = 0
    clicking = False
    double_click_delay = 0
    current_mode = 0

    # declare the window
    root = Tk()
    is_valid_command = root.register(is_valid_input)
    tfList = []

    # Creating thread for listening to keys
    thread = threading.Thread(target=input_thread, args=(), daemon=True)
    thread.start()

    # declare combobox
    options = [
        "Left click",
        "Double click"
    ]

    combostyle_enabled = ttk.Style()
    combostyle_enabled.theme_create('combostyle_enabled', parent='alt', settings={'TCombobox': {'configure':
                                                                                                    {
                                                                                                        'selectbackground': '#2d7c9d',
                                                                                                        'selectforeground': 'black',
                                                                                                        'fieldbackground': '#2d7c9d',
                                                                                                        'background': '#2d7c9d',
                                                                                                        'foreground': 'black'}}})

    combostyle_disabled = ttk.Style()
    combostyle_disabled.theme_create('combostyle_disabled', parent='alt', settings={'TCombobox': {'configure':
                                                                                                      {
                                                                                                          'fieldbackground': 'grey',
                                                                                                          'background': 'grey',
                                                                                                          'foreground': '#404040'}}})
    combostyle_enabled.theme_use('combostyle_enabled')
    myCombo = ttk.Combobox(root, width=15, value=options, state="readonly")
    myCombo.master.option_add('*TCombobox*Listbox.background', '#2d7c9d')
    myCombo.master.option_add('*TCombobox*Listbox.selectBackground', '#61afd1')
    myCombo.master.option_add('*TCombobox*Listbox.selectForeground', 'black')
    myCombo.current(0)
    myCombo.grid(row=0, column=4, padx=10, pady=20, columnspan=2)

    # declare buttons
    start = Button(root, text="Start (SHIFT+F1)", bg="#2d7c9d", disabledforeground="#404040",
                   command=start_clicking)
    start.configure(height=2, width=18, activebackground="#61afd1", activeforeground="#404040", cursor="hand2", )
    start.grid(row=0, column=0, padx=(10, 0), pady=20, columnspan=1)
    start.bind('<Enter>', highlight)
    start.bind('<Leave>', unhighlight)

    stop = Button(root, text="Stop (SHIFT+F2)", bg="#5e5e5e", disabledforeground="#404040",
                  command=stop_clicking)
    stop.configure(height=2, width=18, activebackground="#61afd1", activeforeground="#404040", cursor="arrow")
    stop.bind('<Enter>', highlight)
    stop.bind('<Leave>', unhighlight)
    stop.grid(row=0, column=1, padx=(0, 0), pady=20, columnspan=1, sticky=W)
    stop["state"] = DISABLED

    # declare frame for textfields
    tFrame = Frame(root)
    tFrame.grid(row=1, column=0, columnspan=5)
    tFrame.configure(bg='#161d20')

    # declare text fields
    create_textfields()
    tfList[0].grid(row=2, column=1, pady=10)
    tfList[1].grid(row=3, column=1, pady=10)
    tfList[2].grid(row=4, column=1, pady=10)
    tfList[3].grid(row=2, column=2, pady=10)
    tfList[4].grid(row=3, column=2, pady=10)
    tfList[5].grid(row=4, column=2, pady=10)
    tfList[6].grid(row=2, column=3, pady=10, padx=(110, 0))

    # declare labels
    static_label = Label(tFrame, text="Time delay", bg="#2d7c9d", width=12)
    static_label.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), columnspan=1)
    random_label = Label(tFrame, text="Random delay", bg="#2d7c9d", width=12)
    random_label.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), columnspan=1)
    duration_label = Label(tFrame, text="Clicking duration (seconds)", bg="#2d7c9d", width=22)
    duration_label.grid(row=1, column=3, padx=(110, 10), pady=(10, 10), columnspan=2)
    info_label_one = Label(tFrame, text="0 = infinite", bg="#2d7c9d", width=9)
    info_label_one.grid(row=2, column=4, padx=(10, 10), pady=(10, 10), columnspan=1)

    min_label = Label(tFrame, text="Minutes", bg="#2d7c9d", width=9)
    min_label.grid(row=2, column=0, padx=(10, 10), pady=10, sticky=W)
    sec_label = Label(tFrame, text="Seconds", bg="#2d7c9d", width=9)
    sec_label.grid(row=3, column=0, padx=(10, 10), pady=10, sticky=W)
    ms_label = Label(tFrame, text="Milliseconds", bg="#2d7c9d", width=9)
    ms_label.grid(row=4, column=0, padx=(10, 10), pady=10, sticky=W)

    # set window title
    root.title('Goles Autoclicker')
    # set window width and height
    root.geometry("800x330")
    root.resizable(False, False)
    # set window background color
    root.configure(bg='#161d20')
    # move window center
    winWidth = root.winfo_reqwidth()
    winwHeight = root.winfo_reqheight()
    posRight = int(root.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(root.winfo_screenheight() / 2 - winwHeight / 2)
    root.protocol('WM_DELETE_WINDOW', exit_function)
    root.geometry("+{}+{}".format(posRight, posDown))
    root.bind("<Button-1>", click_event)

    # load previous settings
    if os.path.isfile("data.dat"):
        load_data()
    root.mainloop()
