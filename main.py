from tkinter import *
from PIL import ImageGrab
from pyautogui import *
import time


def left_click():
    print("Hello")
    #px = ImageGrab.grab().load()
    #color = px[1758, 641]
    #print(color)



if __name__ == '__main__':
    # declare the window
    window = Tk()
    click(position())
    # declare buttons
    button1 = Button(window, text="Start", bg="#301B3F", command=left_click)
    button1.configure(height=2, width=10, fg="#B4A5A5", activebackground="#7a49a5", activeforeground="#B4A5A5")
    button1.pack()

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
