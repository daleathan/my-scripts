#!/usr/bin/python3
#A Python script to set the theme for GTK+ 2 and GTK+ 3 applications in minimal environments
#By Charles Bos

from tkinter import *
import os

def findThemes(ver) :
    homeDir = os.path.expanduser('~')
    a = os.listdir("/usr/share/themes")
    for x in a : a[a.index(x)] = "/usr/share/themes/" + x
    if os.path.exists("/usr/local/share/themes") :
        b = os.listdir("/usr/local/share/themes")
        for x in b : b[b.index(x)] = "/usr/local/share/themes/" + x
    else : b = []
    if os.path.exists(homeDir + "/.themes") :
        c = os.listdir(homeDir + "/.themes")
        for x in c : c[c.index(x)] = homeDir + "/.themes/" + x
    else : c = []
    allThemes = a + b + c
    final = []
    
    for x in allThemes :
        dirs = os.listdir(x)
        y = x.split("/")
        if ver == 2 :
            if "gtk-2.0" in (dirs) :
                gDir = os.listdir(x + "/gtk-2.0")
                if "gtkrc" in gDir : final.append(y[-1])
        else :
            if "gtk-3.0" in (dirs) :
                gDir = os.listdir(x + "/gtk-3.0")
                if "gtk.css" in gDir : final.append(y[-1])
    #Add default theme to list    
    if ver == 3 : final.append("Raleigh")

    return sorted(final)

def getTheme(ver) :
    homeDir = os.path.expanduser('~')
    try :
        if ver == 2 : file = open(homeDir + "/.gtkrc-2.0", "r")
        else : file = open(homeDir + "/.config/gtk-3.0/settings.ini", "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        for x in contents :
            y = x.split("=")
            if y[0].strip() == "gtk-theme-name" : return y[-1].strip().strip('"')
        return "None set"
    except IOError :
        return "None set"

def setTheme(ver) :
    homeDir = os.path.expanduser('~')
    if ver == 2 : path = homeDir + "/.gtkrc-2.0"
    else : path = homeDir + "/.config/gtk-3.0/settings.ini"
    if os.path.exists(path) :
        #If file exists, read it and try to get find theme name line
        #If found, update it
        found = False
        file = open(path, "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        for x in contents :
            y = x.split("=")
            if y[0].strip() == "gtk-theme-name" :
                if y[0][-1] == " " :
                    if ver == 2: z = str("gtk-theme-name = " + '"' + varOpG2.get() + '"')
                    else : z = str("gtk-theme-name = " + varOpG3.get())
                else :
                    if ver == 2 : z = str("gtk-theme-name=" + '"' + varOpG2.get() + '"')
                    else : z = str("gtk-theme-name=" + varOpG3.get())
                contents[contents.index(x)] = z
                found = True
                break

        if not found and contents != [''] :
            #If file exists and is full but gtk-theme-name is not present, append it
            file = open(path, "a")
            if ver == 2 : file.write("\ngtk-theme-name = " + '"' + varOpG2.get() + '"')
            else : file.write("\ngtk-theme-name = " + varOpG3.get())
        elif found :
            #If file exists and gtk-theme-name is present, update it
            file = open(path, "w")
            for x in contents :
                if contents.index(x) == len(contents) -1 : file.write(x)
                else : file.write(x + "\n")
        else :
            #If file exists but is empty, overwrite it
            file = open(path, "w")
            if ver == 2 : file.write("gtk-theme-name = " + '"' + varOpG2.get() + '"')
            else : file.write("[Settings]\ngtk-theme-name = " + varOpG3.get())
        file.close()
    else :
        #If file does not exist, create it
        if ver == 3 :
            try :
                os.makedirs(homeDir + "/.config/gtk-3.0/")
            except FileExistsError :
                pass
        file = open(path, "w")
        if ver == 2 : file.write("gtk-theme-name = " + '"' + varOpG2.get() + '"')
        else : file.write("[Settings]\ngtk-theme-name = " + varOpG3.get())
        file.close()

def update() :
    if (varOpG2 != getTheme(2)) and (varOpG2.get() != "None set") : setTheme(2)
    if (varOpG3 != getTheme(3)) and (varOpG3.get() != "None set") : setTheme(3)

class UI() :
    def __init__(self, parent) :
        l1 = Label(parent, text = "Set the theme for GTK+ applications", pady = 5, padx = 5, relief = RAISED)
        l1.grid(row = 1, column = 1, columnspan = 2)

        #GTK+ 2 section
        l2 = Label(parent, text = "GTK+ 2 app theme:", pady = 7, padx = 5).grid(row = 2, column = 1, sticky = W)
        global varOpG2
        varOpG2 = StringVar(parent)
        varOpG2.set(getTheme(2))
        themesG2 = findThemes(2)
        m1 = OptionMenu(parent, varOpG2, *themesG2).grid(row = 2, column = 2, sticky = W)

        #GTK+ 3 section
        l3 = Label(parent, text = "GTK+ 3 app theme:", pady = 7, padx = 5).grid(row = 3, column = 1, sticky = W)
        global varOpG3
        varOpG3 = StringVar(parent)
        varOpG3.set(getTheme(3))
        themesG3 = findThemes(3)
        m2 = OptionMenu(parent, varOpG3, *themesG3).grid(row = 3, column = 2, sticky = W)

        #Buttons
        b1 = Button(parent, text = "Close", padx = 5, pady = 5, bd = 3, command = parent.destroy).grid(row = 4, column = 1)
        b2 = Button(parent, text = "Update", padx = 5, pady = 5, bd = 3, command = update).grid(row = 4, column = 2)
        
top = Tk()
top.title("Set GTK+ theme")
ui = UI(top)
top.mainloop()
