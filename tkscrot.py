#!/usr/bin/python3
#Simple Tk frontend to scrot with a similar feel to GNOME Screenshot
#By Charles Bos

from tkinter import *
from subprocess import Popen
import time

def run() :
    cmd = ["scrot"]
    if ui.shotType.get() == 1 : cmd.append("-u")
    if ui.shotType.get() == 2 : cmd.append("-s")
    if int(ui.delay.get()) > 0 : cmd.append("-d " + ui.delay.get())
    if int(ui.quality.get()) != 75 : cmd.append("-q " + ui.quality.get())
    if ui.shotType.get() == 1 and ui.incBorder.get() == 1 : cmd.append("-b")
    cmd.append("-e xdg-open $f")
    top.destroy()
    time.sleep(0.1)
    Popen(cmd).wait()

class UI() :
    def __init__(self, parent) :
        parent.title("Take Screenshot")

        #Screenshot
        l1 = Label(parent, text = "Screenshot", pady = 5, padx = 5).grid(row = 1, column = 1, sticky = W)
        self.shotType = IntVar()
        r1 = Radiobutton(parent, text = "Grab the whole screen", variable = self.shotType, value = 0, pady = 5, padx = 5).grid(row = 1, column = 2, sticky = W)
        r2 = Radiobutton(parent, text = "Grab the current window", variable = self.shotType, value = 1, pady = 5, padx = 5).grid(row = 2, column = 2, sticky = W)
        r3 = Radiobutton(parent, text = "Select area to grab", variable = self.shotType, value = 2, pady = 5, padx = 5).grid(row = 3, column = 2, sticky = W)

        #Delay
        l2 = Label(parent, text = "Set delay", pady = 5, padx = 5).grid(row = 4, column = 1, sticky = W)
        self.delay = Spinbox(parent, from_ = 0, to = 60, width = 15)
        self.delay.grid(row = 4, column = 2)

        #Quality
        l3 = Label(parent, text = "Set quality", pady = 5, padx = 5).grid(row = 5, column = 1, sticky = W)
        self.quality = Spinbox(parent, from_ = 1, to = 100, width = 15)
        self.quality.grid(row = 5, column = 2)
        self.quality.delete(0, 1)
        self.quality.insert(0, "100")

        #Window border
        self.incBorder = IntVar()
        self.incBorder.set(1)
        cb1 = Checkbutton(parent, text = "Include window border", variable = self.incBorder, padx = 5, pady = 5).grid(row = 6, column = 2, sticky = W)

        #Buttons
        b1 = Button(parent, text = "Close", padx = 5, pady = 5, bd = 3, command = parent.destroy).grid(row = 7, column = 1, sticky = W)
        b2 = Button(parent, text = "Take Screenshot", padx = 5, pady = 5, bd = 3, command = run).grid(row = 7, column = 2, sticky = E)
        
top = Tk()  
ui = UI(top)
top.mainloop()
