#!/usr/bin/python
#A simple interface for configuring some Metacity settings
#By Charles Bos

from tkinter import *
from subprocess import Popen, PIPE
import os
import time

def getTheme() :
    theme = Popen(["gsettings", "get", "org.gnome.metacity", "theme"], stdout = PIPE).communicate()
    theme = str(theme[0]).lstrip('''b"\'''').rstrip(''''\\n"''')
    return theme

def findThemes() :
    sysThemes = os.listdir("/usr/share/themes")
    if os.path.exists("/usr/local/share/themes") : locThemes = os.listdir("/usr/local/share/themes")
    else : locThemes = []

    #Eliminate non Metacity themes from final list
    themes = []
    
    for x in sysThemes :
        dirFiles = []
        for root, dirs, files in os.walk("/usr/share/themes/" + x, topdown=False):
            for name in files:
                dirFiles.append(name)
        if (("metacity-theme-1.xml" not in dirFiles) and ("metacity-theme-2.xml" not in dirFiles) and ("metacity-theme-3.xml" not in dirFiles)) : pass
        else : themes.append(x)

    if locThemes != [] :
        for x in locThemes :
            dirFiles = []
            for root, dirs, files in os.walk("/usr/local/share/themes/" + x, topdown=False):
                for name in files:
                    dirFiles.append(name)
            if (("metacity-theme-1.xml" not in dirFiles) and ("metacity-theme-2.xml" not in dirFiles) and ("metacity-theme-3.xml" not in dirFiles)) : pass
            else : themes.append(x)

    return sorted(themes)

def setTheme(self) :
    newTheme = varOp.get()
    Popen(["gsettings", "set", "org.gnome.metacity", "theme", newTheme])

def getSysFont() :
    status = Popen(["gsettings", "get", "org.gnome.desktop.wm.preferences", "titlebar-uses-system-font"], stdout = PIPE).communicate()
    status = str(status[0]).lstrip('''b"\'''').rstrip(''''\\n"''')
    return status

def setSysFont() :
    if getSysFont() == 'true' :
        Popen(["gsettings", "set", "org.gnome.desktop.wm.preferences", "titlebar-uses-system-font", 'false'])
        b1["text"] = "Toggle (Now off)"
    else :
        Popen(["gsettings", "set", "org.gnome.desktop.wm.preferences", "titlebar-uses-system-font", 'true'])
        b1["text"] = "Toggle (Now on)"

def getTitleFont() :
    font = Popen(["gsettings", "get", "org.gnome.desktop.wm.preferences", "titlebar-font"], stdout = PIPE).communicate()
    font = str(font[0]).lstrip('''b"\'''').rstrip(''''\\n"''')
    return font

def setTitleFont() :
    font = e1.get()
    if (font[0] != "'") and (font[-1] != "'") : font = "'" + font + "'"
    Popen(["gsettings", "set", "org.gnome.desktop.wm.preferences", "titlebar-font", font])

def getButtonLayout() :
    layout = Popen(["gsettings", "get", "org.gnome.desktop.wm.preferences", "button-layout"], stdout = PIPE).communicate()
    layout = str(layout[0]).lstrip('''b"\'''').rstrip(''''\\n"''')
    return layout

def setButtonLayout() :
    layout = e2.get()
    Popen(["gsettings", "set", "org.gnome.desktop.wm.preferences", "button-layout", layout])

def reset() :
    #Reset settings
    Popen(["gsettings", "reset", "org.gnome.metacity", "theme"])
    Popen(["gsettings", "reset", "org.gnome.desktop.wm.preferences", "titlebar-uses-system-font"])
    Popen(["gsettings", "reset", "org.gnome.desktop.wm.preferences", "titlebar-font"])
    Popen(["gsettings", "reset", "org.gnome.desktop.wm.preferences", "button-layout"])
    
    #Update ui
    time.sleep(0.5)
    varOp.set("Current: " + getTheme())
    b1["text"] = "Toggle (Now on)"
    e1.delete(first = 0, last = len(e1.get()) + 1)
    e2.delete(first = 0, last = len(e2.get()) + 1)
    e1.insert(0, getTitleFont())
    e2.insert(0, getButtonLayout())
        
class UI() :
    def __init__(self, parent) :
        l1 = Label(parent, text = "Configure the Metacity theme, titlebar font and button order.", pady = 5, padx = 5, relief = RAISED)
        l1.grid(row = 1, column = 1, columnspan = 3)

        #Theme ui
        l2 = Label(parent, text = "Choose theme:", pady = 7, padx = 5).grid(row = 2, column = 1)
        global varOp
        varOp = StringVar(parent)
        varOp.set("Current: " + getTheme())
        themes = findThemes()
        m1 = OptionMenu(parent, varOp, *themes, command = setTheme).grid(row = 2, column = 2)

        #Font ui
        ##Use Sysfont?
        l3 = Label(parent, text = "Use system font?", pady = 7, padx = 5).grid(row = 3, column = 1)
        if getSysFont() == 'true' : b1Text = "Toggle (Now on)"
        else : b1Text = "Toggle (Now off)"
        global b1
        b1 = Button(parent, text = b1Text, command = setSysFont)
        b1.grid(row = 3, column = 2)

        ##Titlebar font
        l4 = Label(parent, text = "Set font:", pady = 7, padx = 5).grid(row = 4, column = 1)
        global e1
        e1 = Entry(parent)
        e1.grid(row = 4, column = 2)
        e1.insert(0, getTitleFont())
        b2 = Button(parent, text = "Update", command = setTitleFont).grid(row = 4, column = 3)

        #Button layout ui
        l4 = Label(parent, text = "Set button layout:", pady = 7, padx = 5).grid(row = 5, column = 1)
        global e2
        e2 = Entry(parent)
        e2.grid(row = 5, column = 2)
        e2.insert(0, getButtonLayout())
        b3 = Button(parent, text = "Update", command = setButtonLayout).grid(row = 5, column = 3)

        #Reset all
        b4 = Button(parent, text = "Reset all", command = reset).grid(row = 6, column = 3)
        
top = Tk()
top.title("Settings for Metacity")
ui = UI(top)
top.mainloop()
