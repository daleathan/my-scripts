#!/usr/bin/python
#A script to add icons to an existing Openbox menu file
#This is untested and may not work at all as expected
#By Charles Bos

import sys
import os
import shutil

def usage() :
    print('''Usage:
  obiconadder.py <path to menu file>''')

def getDotDesktop(item, identifier) :
    for x in dotDesktops :
        file = open(x, "r", encoding = "utf-8")
        fileText = file.read()
        file.close()
        idStart = fileText.find(identifier)
        idEnd = fileText.find("\n", idStart)
        if item == fileText[idStart + 5:idEnd].split(" %")[0] : return x
    #As a fallback position, try and match the execute line from the file with
    #the .desktop filename
    if identifier == "Exec=" :
        for x in dotDesktops :
            if item == x.split("/")[-1].split(".desktop")[0] : return x
    return None

def getIcon(dotDesktop) :
    file = open(dotDesktop, encoding = "utf-8")
    fileText = file.read()
    file.close()
    iconStart = fileText.find("Icon=")
    if iconStart != -1 :
        iconEnd = fileText.find("\n", iconStart)
        for x in iconsList :
            if fileText[iconStart + 5:iconEnd] == x.split("/")[-1].split(".")[0] :
                return x
        return None
    else : return None

def getIconTheme() :
    #Try and get the icon theme from ~/.gtkrc-2.0
    homeDir = os.path.expanduser('~')
    try :
        file = open(homeDir + "/.gtkrc-2.0", "r")
        fileText = file.read()
        file.close()
        fileText = fileText.split("\n")
        for x in fileText :
            y = x.split("=")
            if y[0].strip() == "gtk-icon-theme-name" : theme = y[-1].strip().strip('"')
        if os.path.exists("/usr/share/icons/" + theme + "/48x48") : return theme
        else : return None
    except IOError :
        return None
        
#Handle args
args = sys.argv
if (len(args) != 2) or (args[1] == '-h') or (args[1] == '--help') :
    usage()
    os._exit(0)
elif os.path.isfile(args[1]) : menuFile = args[1]
else :
    usage()
    os._exit(0)

#Get locations of icons and .desktops
iconDirs = ["/usr/share/pixmaps", "/usr/share/icons/hicolor/48x48"]
if getIconTheme() != None : iconDirs.append("/usr/share/icons/" + getIconTheme() + "/48x48")
if os.path.exists("/usr/share/icons/gnome/48x48") : iconDirs.append("/usr/share/icons/gnome/48x48")
iconsList = []
for x in iconDirs :
    for root, dirs, files in os.walk(x, topdown=False):
        for name in files:
            iconsList.append(os.path.join(root, name))
dotDesktops = os.listdir("/usr/share/applications")
for x in dotDesktops : dotDesktops[dotDesktops.index(x)] = "/usr/share/applications/" + x

#Start scanning menu file
file = open(menuFile, "r")
fileText = file.read()
file.close()

#Get icons for applications
nameStart = fileText.find('<item label="')
nameEnd = fileText.find('">', nameStart)
while 0 <= nameStart <= len(fileText) :
    dotDesktop = getDotDesktop(fileText[nameStart + 13:nameEnd].split('" icon="')[0], "Name=")
    if dotDesktop != None : icon = getIcon(dotDesktop)
    else :
        #If identification by name fails, try by exec instead 
        execStart = fileText.find("<execute>", nameEnd)
        execEnd = fileText.find("</execute>", execStart)
        dotDesktop = getDotDesktop(fileText[execStart + 9:execEnd], "Exec=")
        if dotDesktop != None : icon = getIcon(dotDesktop)
        else : icon = None
    if icon != None :
        fileText = fileText.replace(fileText[nameStart + 13:nameEnd], fileText[nameStart + 13:nameEnd].split('" icon="')[0] + '" icon="' + icon)
    else :
        fileText = fileText.replace(fileText[nameStart + 13:nameEnd], fileText[nameStart + 13:nameEnd].split('" icon="')[0])
    nameStart = fileText.find('<item label="', nameEnd)
    nameEnd = fileText.find('">', nameStart)

#Get icons for categories
#If user set theme cannot be found or does not contain an
#appropriate number of icons, fall back to gnome-icon-theme
try :
    if getIconTheme() != None :
        if len(os.listdir("/usr/share/icons/" + getIconTheme() + "/48x48/categories")) >= 15 : 
            catTheme = getIconTheme()
    elif os.path.exists("/usr/share/icons/gnome/48x48") : catTheme = "gnome"
    else : catTheme = None
except IOError :
    if os.path.exists("/usr/share/icons/gnome/48x48") : catTheme = "gnome"
    else : catTheme = None

if catTheme != None :
    catStart = fileText.find('<menu id="')
    catEnd = fileText.find('" ', catStart)
    labelStart = fileText.find('label="', catEnd)
    labelEnd = fileText.find('">', labelStart)
    while 0 <= catStart <= len(fileText) :
        if os.path.isfile("/usr/share/icons/" + catTheme + "/48x48/categories/applications-" + fileText[labelStart + 7:labelEnd].lower() + ".png") :
            icon = "/usr/share/icons/" + catTheme + "/48x48/categories/applications-" + fileText[labelStart + 7:labelEnd].lower() + ".png"
        elif os.path.isfile("/usr/share/icons/" + catTheme + "/48x48/categories/package_" + fileText[labelStart + 7:labelEnd].lower() + ".png") :
            icon = "/usr/share/icons/" + catTheme + "/48x48/categories/package_" + fileText[labelStart + 7:labelEnd].lower() + ".png"
        else :
            icon = None
        if icon != None :
            fileText = fileText.replace(fileText[catStart:labelStart - 1], fileText[catStart:catEnd + 1] + ' icon="' + icon + '"')
        catStart = fileText.find('<menu id="', labelEnd)
        catEnd = fileText.find('" ', catStart)
        labelStart = fileText.find('label="', catEnd)
        labelEnd = fileText.find('">', labelStart)

#Backup original file
shutil.copyfile(menuFile, menuFile + ".bak")
#Now add the icons
#This will replace the contents of the old file
file = open(menuFile, "w")
print(fileText.rstrip("\n"), file = file)
file.close()