#!/usr/bin/python
#A quick and dirty interface to end a session - assumes systemd
#By Charles Bos

from tkinter import *
import os
import sys

def getLogoutArg() :
    #If using startx, run with 1 argument, the name of the last x client
    #specified in xinitrc, will usually be the window manager.
    #Else run with no args and the logout command will be pkill -u $USER
    args = sys.argv
    if len(args) == 1 : return "-u $USER"
    else : return args[1]

def runAction() :
    if option.get() == 1 : os.system("pkill " + getLogoutArg())
    elif option.get() == 2 : os.system("systemctl suspend")
    elif option.get() == 3 : os.system("systemctl hibernate")
    elif option.get() == 4 : os.system("systemctl reboot")
    elif option.get() == 5 : os.system("systemctl poweroff")
        
class UI() :
    def __init__(self, parent) :
        global option
        option = IntVar()
        r1 = Radiobutton(parent, text = "Logout", variable = option, value = 1).grid(row = 2, column = 1)
        r2 = Radiobutton(parent, text = "Suspend", variable = option, value = 2).grid(row = 2, column = 2)
        r3 = Radiobutton(parent, text = "Hibernate", variable = option, value = 3).grid(row = 2, column = 3)
        r4 = Radiobutton(parent, text = "Reboot", variable = option, value = 4).grid(row = 2, column = 4)
        r5 = Radiobutton(parent, text = "Poweroff", variable = option, value = 5).grid(row = 2, column = 5)
        b1 = Button(parent, text = "Ok", command = runAction).grid(row = 3, column = 1, columnspan = 5)
        
top = Tk()
top.title("End session")
ui = UI(top)
top.mainloop()
