from random import *
from tkinter import *
from pyautogui import *
import time
from threading import Timer
from pynput.keyboard import Listener

staticDelay = 0
delay = 0
clicking = False


def start_clicking():
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
    if staticDelay == 0:
        return
    else:
        print("test")
        calculate_new_delay()
        left_click()


def stop_clicking():
    global clicking
    clicking = False


def left_click():
    if clicking:
        timer = Timer(delay, left_click)
        timer.start()
        click()
        calculate_new_delay()


def random_delay(minutes, seconds, millis):
    totalMs = minutes * 60000 + seconds * 1000 + millis
    return randint(0, totalMs)


def calculate_new_delay():
    global delay
    delay = ((staticDelay + random_delay(int(tfList[3].get()), int(tfList[4].get()), int(tfList[5].get())) - 11) / 1000)


def is_valid_input(new, old):
    try:
        int(new)
        if new[-1] == "0" and old != "":
            return False
        else:
            return True
    except ValueError:
        if new == '':
            return True
        else:
            return False


def create_textfields():
    for i in range(6):
        tf = Entry(window, bg="#301B3F", fg="#B4A5A5", validatecommand=(is_valid_command, '%P', '%s'), validate='key')
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


if __name__ == '__main__':
    # declare the window
    window = Tk()
    is_valid_command = window.register(is_valid_input)
    tfList = []


    def keyinputs(event):
        if event.keysym == "F1":
            start_clicking()
        if event.keysym == "F2":
            stop_clicking()


    # declare buttons
    start = Button(window, text="Start", bg="#301B3F", command=start_clicking)
    start.configure(height=2, width=10, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    start.pack()

    stop = Button(window, text="Stop", bg="#301B3F", command=stop_clicking)
    stop.configure(height=2, width=10, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    stop.pack()

    # declare text fields
    create_textfields()
    for i in range(6):
        tfList[i].pack()

    # set window title
    window.title("Goles Autoclicker")
    # set window width and height
    window.geometry("1000x600")
    window.resizable(False, False)
    # set window background color
    window.configure(bg='#3C415C')
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    window.bind('<KeyPress>', keyinputs)
    window.mainloop()


    # Detecting key inputs
    def on_press(key):
        print("Key Pressed")


    def on_release(key):
        print("Key released")


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
