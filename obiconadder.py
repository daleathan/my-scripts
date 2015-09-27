#!/usr/bin/python
#A script to add icons to an existing Openbox menu file
#This is untested and may not work at all as expected
#By Charles Bos

import sys
import os

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
        if item == fileText[idStart + 5:idEnd] : return x
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
            if fileText[iconStart + 5:iconEnd] == x.split("/")[-1].split(".")[0].split(" %")[0] :
                return x
        return None
    else : return None
        
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
newFile = fileText[:]

nameStart = fileText.find('<item label="')
nameEnd = fileText.find('">', nameStart)

while 0 <= nameStart <= len(fileText) :
    dotDesktop = getDotDesktop(fileText[nameStart + 13:nameEnd], "Name=")
    if dotDesktop != None : icon = getIcon(dotDesktop)
    else :
        #If identification by name fails, try by exec instead 
        execStart = fileText.find("<execute>", nameEnd)
        execEnd = fileText.find("</execute>", execStart)
        dotDesktop = getDotDesktop(fileText[execStart + 9:execEnd], "Exec=")
        if dotDesktop != None : icon = getIcon(dotDesktop)
        else : icon = None
    if icon != None :
        newFile = newFile.replace(fileText[nameStart + 13:nameEnd], fileText[nameStart + 13:nameEnd] + '" icon="' + icon)
    nameStart = fileText.find('<item label="', nameEnd)
    nameEnd = fileText.find('">', nameStart)

#Now add the icons
#This will replace the contents of the old file
file = open(menuFile, "w")
print(newFile, file = file)
file.close()