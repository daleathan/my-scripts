#!/usr/bin/python3
#A simple Tk GUI for selecting the output screen
#We use xrandr to select turn on/off the screens
#By Charles Bos

from tkinter import *
from subprocess import Popen

def run() :
    if ui.display.get() == 0 :
        cmd = ["xrandr", "--output", "HDMI1", "--off", "--output", "LVDS1", "--auto"]
        Popen(cmd).wait()
    elif ui.display.get() == 1 :
        cmd = ["xrandr", "--output", "HDMI1", "--auto", "--output", "LVDS1", "--off"]
        Popen(cmd).wait()
    else :
        cmd = ["xrandr", "--output", "HDMI1", "--auto", "--output", "LVDS1", "--auto"]
        Popen(cmd).wait()
    top.destroy()

class UI() :
    def __init__(self, parent) :
        parent.title("Display Selector")

        #Screenshot
        l1 = Label(parent, text = "Select the output display(s).", pady = 5, padx = 5).grid(row = 1, column = 1, sticky = W)
        self.display = IntVar()
        r1 = Radiobutton(parent, text = "Laptop only", variable = self.display, value = 0, pady = 5, padx = 5).grid(row = 2, column = 1, sticky = W)
        r2 = Radiobutton(parent, text = "Television only", variable = self.display, value = 1, pady = 5, padx = 5).grid(row = 3, column = 1, sticky = W)
        r3 = Radiobutton(parent, text = "Laptop and television", variable = self.display, value = 2, pady = 5, padx = 5).grid(row = 4, column = 1, sticky = W)

        #Buttons
        b1 = Button(parent, text = "Cancel", padx = 10, pady = 5, bd = 3, command = parent.destroy).grid(row = 5, column = 1, sticky = W)
        b2 = Button(parent, text = "OK", padx = 5, pady = 5, bd = 3, command = run).grid(row = 5, column = 1, sticky = E)
        
top = Tk()  
ui = UI(top)
top.mainloop()
