#!/usr/bin/python3
#A Python script to set the theme for GTK+ 2 and GTK+ 3 applications in minimal environments
#This shouldn't overwrite existing ~/.gtkrc-2.0 or ~/.config/gtk-3.0/settings.ini files - instead
#it will try to update them in place.
#By Charles Bos

from tkinter import *
from tkinter import messagebox
import os

def findThemes(themeType) :
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
        if themeType == "gtk2" :
            if "gtk-2.0" in (dirs) :
                gDir = os.listdir(x + "/gtk-2.0")
                if "gtkrc" in gDir : final.append(y[-1])
        else :
            if "gtk-3.0" in (dirs) :
                gDir = os.listdir(x + "/gtk-3.0")
                if "gtk.css" in gDir : final.append(y[-1])
    #Add default themes to list    
    if "Adwaita" not in final : final.append("Adwaita")
    if "Raleigh" not in final : final.append("Raleigh")

    return sorted(final)

def findIcons(themeType) :
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
        #Dir needs to contain index.theme and might well contain cursors dir. Therefore, the
        #number of items within dir needs to be greater than 2 for it to contain a viable icon
        #theme. For cursor theme, we only need the cursor dir.
        if "index.theme" in dirs :
            if themeType == "cursors" :
                if "cursors" in dirs : final.append(y[-1])
            else :
                if len(dirs) > 2 : final.append(y[-1])
    #Remove hicolor and default
    if "hicolor" in final : final.remove("hicolor")
    if "default" in final : final.remove("default")

    return sorted(final)

def getResource(sFile, resource) :
    if resource == "gtk-button-images" or resource == "gtk-menu-images" : default = 0
    else : default = "None set"
    homeDir = os.path.expanduser('~')
    try :
        if sFile == "gtk2" : file = open(homeDir + "/.gtkrc-2.0", "r")
        elif sFile == "gtk3" : file = open(homeDir + "/.config/gtk-3.0/settings.ini", "r")
        elif sFile == "xdg_cursor" : file = open(homeDir + "/.icons/default/index.theme", "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        for x in contents :
            y = x.split("=")
            if y[0].strip() == resource : return y[-1].strip().strip('"')
        return default
    except IOError :
        return default

def setResource(sFile, resource, var) :
    homeDir = os.path.expanduser('~')
    if sFile == "gtk2" : path = homeDir + "/.gtkrc-2.0"
    elif sFile == "gtk3" : path = homeDir + "/.config/gtk-3.0/settings.ini"
    elif sFile == "xdg_cursor" : path = homeDir + "/.icons/default/index.theme"
    if os.path.exists(path) :
        #If file exists, read it and try to get find resource name line
        #If found, update it
        found = False
        file = open(path, "r")
        contents = file.read()
        file.close()
        contents = contents.split("\n")
        contents = [x for x in contents if x != ""]
        for x in contents :
            y = x.split("=")
            if y[0].strip() == resource :
                if y[0][-1] == " " :
                    if sFile == "gtk2": z = str(resource + " = " + '"' + var.get() + '"')
                    else : z = str(resource + " = " + var.get())
                else :
                    if sFile == "gtk2" : z = str(resource + "=" + '"' + var.get() + '"')
                    else : z = str(resource + "=" + var.get())
                contents[contents.index(x)] = z
                found = True
                break

        if found :
            #If file exists and resource is present, update it
            file = open(path, "w")
            for x in contents :
                if contents.index(x) == len(contents) -1 : file.write(x)
                else : file.write(x + "\n")
        elif not found and contents != [] :
            #If file exists and is full but resource is not present, append it
            file = open(path, "w")
            for x in contents :
                if contents.index(x) == len(contents) -1 : file.write(x)
                else : file.write(x + "\n")
            if sFile == "gtk2" : file.write("\n" + resource + " = " + '"' + var.get() + '"')
            elif sFile == "gtk3" : file.write("\n" + resource + " = " + var.get())
            elif sFile == "xdg_cursor" : file.write("\n" + resource + "=" + var.get())
        else :
            #If file exists but is empty, overwrite it
            file = open(path, "w")
            if sFile == "gtk2" : file.write(resource + " = " + '"' + var.get() + '"')
            elif sFile == "gtk3" : file.write("[Settings]\n" + resource + " = " + var.get())
            elif sFile == "xdg_cursor" : file.write("[Icon Theme]\n" + resource + "=" + var.get())
        file.close()
    else :
        #If file does not exist, create it
        if sFile == "gtk3" :
            try : os.makedirs(homeDir + "/.config/gtk-3.0/")
            except FileExistsError : pass
        elif sFile == "xdg_cursor" :
            try : os.makedirs(homeDir + "/.icons/default/")
            except FileExistsError : pass
        file = open(path, "w")
        if sFile == "gtk2" : file.write(resource + " = " + '"' + var.get() + '"')
        elif sFile == "gtk3" : file.write("[Settings]\n" + resource + " = " + var.get())
        elif sFile == "xdg_cursor" : file.write("[Icon Theme]\n" + resource + "=" + var.get())
        file.close()

def endOnNewline(filePath) :
    if os.path.exists(filePath) :
        file = open(filePath, "r")
        contents = file.read()
        file.close()
        if len(contents) > 0 :
            if contents[-1] != '\n' :
                file = open(filePath, "a")
                file.write('\n')
                file.close()

def update(rVars) :
    changes = False

    #Update GTK+ 2 theme
    if (rVars[0].get() != getResource("gtk2", "gtk-theme-name")) and (rVars[0].get() != "None set") :
        setResource("gtk2", "gtk-theme-name", rVars[0])
        changes = True

    #Update GTK+ 3 theme
    if (rVars[1].get() != getResource("gtk3", "gtk-theme-name")) and (rVars[1].get() != "None set") :
        setResource("gtk3", "gtk-theme-name", rVars[1])
        changes = True

    #Update GTK+ 2 and GTK+ 3 font
    if (rVars[2].get() != getResource("gtk2", "gtk-font-name")) and (rVars[2].get() != "None set") :
        setResource("gtk2", "gtk-font-name", rVars[2])
        setResource("gtk3", "gtk-font-name", rVars[2])
        changes = True

    #Update GTK+ 2 and GTK+ 3 icons
    if (rVars[3].get() != getResource("gtk2", "gtk-icon-theme-name")) and (rVars[3].get() != "None set") :
        setResource("gtk2", "gtk-icon-theme-name", rVars[3])
        setResource("gtk3", "gtk-icon-theme-name", rVars[3])
        changes = True

    #Update GTK+ 2, GTK+ 3 and XDG cursor theme
    if (rVars[4].get() != getResource("xdg_cursor", "Inherits")) and (rVars[4].get() != "None set") :
        setResource("xdg_cursor", "Inherits", rVars[4])
        setResource("gtk2", "gtk-cursor-theme-name", rVars[4])
        setResource("gtk3", "gtk-cursor-theme-name", rVars[4])
        changes = True

    #Update images in GTK+ menus and buttons
    if  rVars[5].get() != bool(int(getResource("gtk2", "gtk-button-images"))) :
        temp = StringVar()
        temp.set(str(int(rVars[5].get())))
        setResource("gtk2", "gtk-button-images", temp)
        setResource("gtk3", "gtk-button-images", temp)
        changes = True
    if  rVars[6].get() != bool(int(getResource("gtk2", "gtk-menu-images"))) :
        temp = StringVar()
        temp.set(str(int(rVars[6].get())))
        setResource("gtk2", "gtk-menu-images", temp)
        setResource("gtk3", "gtk-menu-images", temp)
        changes = True

    #Ensure that the last char in all files is a newline
    homeDir = os.path.expanduser('~')
    endOnNewline(homeDir + "/.gtkrc-2.0")
    endOnNewline(homeDir + "/.config/gtk-3.0/settings.ini")
    endOnNewline(homeDir + "/.icons/default/index.theme")

    #Show completion message
    if changes : messagebox.showinfo(title = "Complete!", message = "Restart your applications for the settings to take effect.")
    else : messagebox.showinfo(title = "Complete!", message = "Settings files were already up to date. No Changes were made.")

class UI() :
    def __init__(self, parent) :
        parent.title("Set GTK+ theme")
        l1 = Label(parent, text = "Set the theme for GTK+ 2 and 3 applications", pady = 5, padx = 5, relief = RAISED)
        l1.grid(row = 1, column = 1, columnspan = 2)

        #List of resource vars. Positions format is as follows:
        #0 = GTK+ 2 theme, 1 = GTK+ 3 theme, 2 = Font, 3 = Icons, 4 = Cursors, 5 = Button images, 6 = Menu images
        rVars = []

        #GTK+ 2 section
        l2 = Label(parent, text = "GTK+ 2 app theme:", pady = 7, padx = 5).grid(row = 2, column = 1, sticky = W)
        varOpG2 = StringVar(parent)
        rVars.append(varOpG2)
        varOpG2.set(getResource("gtk2", "gtk-theme-name"))
        themesG2 = findThemes("gtk2")
        m1 = OptionMenu(parent, varOpG2, *themesG2).grid(row = 2, column = 2, sticky = W)

        #GTK+ 3 section
        l3 = Label(parent, text = "GTK+ 3 app theme:", pady = 7, padx = 5).grid(row = 3, column = 1, sticky = W)
        varOpG3 = StringVar(parent)
        rVars.append(varOpG3)
        varOpG3.set(getResource("gtk3", "gtk-theme-name"))
        themesG3 = findThemes("gtk3")
        m2 = OptionMenu(parent, varOpG3, *themesG3).grid(row = 3, column = 2, sticky = W)

        #Hereafter, we're not supporting seperate settings for GTK+ 2 and GTK+ 3.
        #For displaying the current setting, we only check the GTK+ 2 settings file.
        
        #Font section
        l4 = Label(parent, text = "GTK+ font:", pady = 7, padx = 5).grid(row = 4, column = 1, sticky = W)
        fontField = Entry(parent)
        rVars.append(fontField)
        fontField.grid(row = 4, column = 2, sticky = W)
        fontField.insert(0, getResource("gtk2", "gtk-font-name"))

        #Icons section
        l5 = Label(parent, text = "GTK+ icons:", pady = 7, padx = 5).grid(row = 5, column = 1, sticky = W)
        varOpIcons = StringVar(parent)
        rVars.append(varOpIcons)
        varOpIcons.set(getResource("gtk2", "gtk-icon-theme-name"))
        icons = findIcons("icons")
        m3 = OptionMenu(parent, varOpIcons, *icons).grid(row = 5, column = 2, sticky = W)

        #Cursors section
        l6 = Label(parent, text = "GTK+ cursors:", pady = 7, padx = 5).grid(row = 6, column = 1, sticky = W)
        varOpCursors = StringVar(parent)
        rVars.append(varOpCursors)
        varOpCursors.set(getResource("xdg_cursor", "Inherits"))
        cursors = findIcons("cursors")
        m4 = OptionMenu(parent, varOpCursors, *cursors).grid(row = 6, column = 2, sticky = W)

        #Button and menu images section
        varOpButtonImages = BooleanVar(parent)
        varOpMenuImages = BooleanVar(parent)
        rVars.append(varOpButtonImages)
        rVars.append(varOpMenuImages)
        varOpButtonImages.set(getResource("gtk2", "gtk-button-images"))
        varOpMenuImages.set(getResource("gtk2", "gtk-menu-images"))
        imgMenuButton = Checkbutton(parent, variable = varOpButtonImages, text = "Images in buttons").grid(row = 7, column = 1, sticky = W)
        imgMenuButton = Checkbutton(parent, variable = varOpMenuImages, text = "Images in menus").grid(row = 7, column = 2, sticky = W)

        #Buttons
        b1 = Button(parent, text = "Close", padx = 5, pady = 5, bd = 3, command = parent.destroy).grid(row = 8, column = 1)
        b2 = Button(parent, text = "Update", padx = 5, pady = 5, bd = 3, command = lambda : update(rVars)).grid(row = 8, column = 2)
        
top = Tk()  
ui = UI(top)
top.mainloop()
