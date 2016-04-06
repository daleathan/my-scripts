#!/usr/bin/python3
#A Python script to set the theme for GTK+ 2 and GTK+ 3 applications in minimal environments
#This shouldn't overwrite existing ~/.gtkrc-2.0 or ~/.config/gtk-3.0/settings.ini files - instead
#it will try to update them in place.
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

def findIcons() :
    homeDir = os.path.expanduser('~')
    a = os.listdir("/usr/share/icons")
    for x in a : a[a.index(x)] = "/usr/share/icons/" + x
    if os.path.exists("/usr/local/share/icons") :
        b = os.listdir("/usr/local/share/icons")
        for x in b : b[b.index(x)] = "/usr/local/share/icons/" + x
    else : b = []
    if os.path.exists(homeDir + "/.icons") :
        c = os.listdir(homeDir + "/.icons")
        for x in c : c[c.index(x)] = homeDir + "/.icons/" + x
    else : c = []
    allIcons = a + b + c
    final = []
    
    for x in allIcons :
        dirs = os.listdir(x)
        y = x.split("/")
        if dirs != [] and "index.theme" in dirs and len(dirs) > 2 : final.append(y[-1])
    #Remove hicolor and default
    if "hicolor" in final : final.remove("hicolor")
    if "default" in final : final.remove("default")

    return sorted(final)

def getResource(ver, resource) :
    homeDir = os.path.expanduser('~')
    try :
        if ver == 2 : file = open(homeDir + "/.gtkrc-2.0", "r")
        else : file = open(homeDir + "/.config/gtk-3.0/settings.ini", "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        for x in contents :
            y = x.split("=")
            if y[0].strip() == resource : return y[-1].strip().strip('"')
        return "None set"
    except IOError :
        return "None set"

def setResource(ver, resource, var) :
    homeDir = os.path.expanduser('~')
    if ver == 2 : path = homeDir + "/.gtkrc-2.0"
    else : path = homeDir + "/.config/gtk-3.0/settings.ini"
    if os.path.exists(path) :
        #If file exists, read it and try to get find resource name line
        #If found, update it
        found = False
        file = open(path, "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        for x in contents :
            y = x.split("=")
            if y[0].strip() == resource :
                if y[0][-1] == " " :
                    if ver == 2: z = str(resource + " = " + '"' + var.get() + '"')
                    else : z = str(resource + " = " + var.get())
                else :
                    if ver == 2 : z = str(resource + "=" + '"' + var.get() + '"')
                    else : z = str(resource + "=" + varOpG3.get())
                contents[contents.index(x)] = z
                found = True
                break

        if not found and contents != [''] :
            #If file exists and is full but resource is not present, append it
            file = open(path, "a")
            if ver == 2 : file.write("\n" + resource + " = " + '"' + var.get() + '"')
            else : file.write("\n" + resource + " = " + var.get())
        elif found :
            #If file exists and resource is present, update it
            file = open(path, "w")
            for x in contents :
                if contents.index(x) == len(contents) -1 : file.write(x)
                else : file.write(x + "\n")
        else :
            #If file exists but is empty, overwrite it
            file = open(path, "w")
            if ver == 2 : file.write(resource + " = " + '"' + var.get() + '"')
            else : file.write("[Settings]\n" + resource + " = " + var.get())
        file.close()
    else :
        #If file does not exist, create it
        if ver == 3 :
            try :
                os.makedirs(homeDir + "/.config/gtk-3.0/")
            except FileExistsError :
                pass
        file = open(path, "w")
        if ver == 2 : file.write(resource + " = " + '"' + var.get() + '"')
        else : file.write("[Settings]\n" + resource + " = " + var.get())
        file.close()

def endOnNewline() :
    homeDir = os.path.expanduser('~')
    if os.path.exists(homeDir + "/.gtkrc-2.0") :
        path = homeDir + "/.gtkrc-2.0"
        file = open(path, "r")
        contents = file.read()
        file.close()
        if contents[-1] != '\n' :
            file = open(path, "a")
            file.write('\n')
            file.close()
    if os.path.exists(homeDir + "/.config/gtk-3.0/settings.ini") :
        path = homeDir + "/.config/gtk-3.0/settings.ini"
        file = open(path, "r")
        contents = file.read()
        file.close()
        if contents[-1] != '\n' :
            file = open(path, "a")
            file.write('\n')
            file.close()

def update() :
    #Update GTK+ 2 theme
    if (varOpG2 != getResource(2, "gtk-theme-name")) and (varOpG2.get() != "None set") : setResource(2, "gtk-theme-name", varOpG2)

    #Update GTK+ 3 theme
    if (varOpG3 != getResource(3, "gtk-theme-name")) and (varOpG3.get() != "None set") : setResource(3, "gtk-theme-name", varOpG3)

    #Update GTK+ 2 and GTK+ 3 font
    if (fontField.get() != getResource(2, "gtk-font-name")) and (fontField.get() != "None set") :
        setResource(2, "gtk-font-name", fontField)
        setResource(3, "gtk-font-name", fontField)

    #Update GTK+ 2 and GTK+ 3 icons
    if (varOpIcons.get() != getResource(2, "gtk-icon-theme-name")) and (varOpIcons.get() != "None set") :
        setResource(2, "gtk-icon-theme-name", varOpIcons)
        setResource(3, "gtk-icon-theme-name", varOpIcons)

    #Ensure that the last char in both files is a newline
    endOnNewline()

class UI() :
    def __init__(self, parent) :
        l1 = Label(parent, text = "Set the theme and font for GTK+ applications", pady = 5, padx = 5, relief = RAISED)
        l1.grid(row = 1, column = 1, columnspan = 2)

        #GTK+ 2 section
        l2 = Label(parent, text = "GTK+ 2 app theme:", pady = 7, padx = 5).grid(row = 2, column = 1, sticky = W)
        global varOpG2
        varOpG2 = StringVar(parent)
        varOpG2.set(getResource(2, "gtk-theme-name"))
        themesG2 = findThemes(2)
        m1 = OptionMenu(parent, varOpG2, *themesG2).grid(row = 2, column = 2, sticky = W)

        #GTK+ 3 section
        l3 = Label(parent, text = "GTK+ 3 app theme:", pady = 7, padx = 5).grid(row = 3, column = 1, sticky = W)
        global varOpG3
        varOpG3 = StringVar(parent)
        varOpG3.set(getResource(3, "gtk-theme-name"))
        themesG3 = findThemes(3)
        m2 = OptionMenu(parent, varOpG3, *themesG3).grid(row = 3, column = 2, sticky = W)

        #Hereafter, we're not supporting seperate settings for GTK+ 2 and GTK+ 3.
        #For displaying the current setting, we only check the GTK+ 2 settings file.
        
        #Font section
        l4 = Label(parent, text = "GTK+ font:", pady = 7, padx = 5).grid(row = 4, column = 1, sticky = W)
        global fontField
        fontField = Entry(parent)
        fontField.grid(row = 4, column = 2, sticky = W)
        fontField.insert(0, getResource(2, "gtk-font-name"))

        #Icons section
        l5 = Label(parent, text = "GTK+ icons:", pady = 7, padx = 5).grid(row = 5, column = 1, sticky = W)
        global varOpIcons
        varOpIcons = StringVar(parent)
        varOpIcons.set(getResource(2, "gtk-icon-theme-name"))
        icons = findIcons()
        m3 = OptionMenu(parent, varOpIcons, *icons).grid(row = 5, column = 2, sticky = W)

        #Buttons
        b1 = Button(parent, text = "Close", padx = 5, pady = 5, bd = 3, command = parent.destroy).grid(row = 6, column = 1)
        b2 = Button(parent, text = "Update", padx = 5, pady = 5, bd = 3, command = update).grid(row = 6, column = 2)
        
top = Tk()  
top.title("Set GTK+ theme")
ui = UI(top)
top.mainloop()
