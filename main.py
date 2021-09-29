from random import *
from tkinter import *
from pyautogui import *
import time


def left_click():
    print(random_delay(0, 2, 530) + (float(minutes.get()) * 60) +
          (float(seconds.get())) + (float(milliseconds.get()) / 1000))


def random_delay(minutes, seconds, millis):
    min = randint(0, minutes)
    sec = randint(0, seconds)
    ms = randint(0, millis)
    return (min*60 + sec + ms/1000)


if __name__ == '__main__':
    # declare the window
    window = Tk()
    click(position())
    # declare buttons
    button1 = Button(window, text="Start", bg="#301B3F", command=left_click)
    button1.configure(height=2, width=10, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    button1.pack()

    # declare text fields
    milliseconds = Entry(window, bg="#301B3F", fg="#B4A5A5")
    milliseconds.insert(0, "0")
    milliseconds.pack()
    seconds = Entry(window, bg="#301B3F", fg="#B4A5A5")
    seconds.insert(0, "0")
    seconds.pack()
    minutes = Entry(window, bg="#301B3F", fg="#B4A5A5")
    minutes.insert(0, "0")
    minutes.pack()

    # set window title
    window.title("Goles Autoclicker")
    # set window width and height
    window.geometry("500x300")
    window.resizable(False, False)
    # set window background color
    window.configure(bg='#3C415C')
    # move window center
    winWidth = window.winfo_reqwidth()
    winwHeight = window.winfo_reqheight()
    posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
    posDown = int(window.winfo_screenheight() / 2 - winwHeight / 2)
    window.geometry("+{}+{}".format(posRight, posDown))
    window.mainloop()
