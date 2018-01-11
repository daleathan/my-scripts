#!/usr/bin/python3
#A script to parse the GTK recently used file and output the top 10 results
#in FVWM menu format

import os
import operator
import sys
import html
import urllib.parse

def usage() :
    print('''Usage:
    fvwm-recent-files.py [OPTIONS]

Options:
    -h: show this dialogue
    -i: use icons''')

def getExec(desktop) :
    file = open(desktop, "r")
    contents = file.read()
    file.close()
    contents = contents.split("\n")
    for x in contents :
        if x[:5] == "Exec=" : 
            if x.find("%") != -1 : return x[x.find("=") + 1:x.find(" %")]
            else : return x[x.find("=") + 1:]
    return None

def getDesktopPath(desktop) :
    desktopDirs = [homedir + "/.local/share/applications",
        "/usr/local/share/applications",
        "/usr/share/applications"]
    for x in desktopDirs :
        try :
            contents = os.listdir(x)
        except (NotADirectoryError, FileNotFoundError) :
            continue
        if desktop in contents : return x + "/" + desktop
    return None

def getProgram(fileinfo) :
    if len(fileinfo) < 3 : return "xdg-open"
    try : desktop = mimeapps[fileinfo[2]]
    except KeyError : return "xdg-open"
    path = getDesktopPath(desktop)
    if path == None : return "xdg-open"
    prog = getExec(path)
    if prog == None : return "xdg-open"
    else : return prog

def getIconTheme() :
    try :
        file = open(homedir + "/.gtkrc-2.0", "r")
        for line in file :
            line = line.split("=")
            if line[0].strip() == "gtk-icon-theme-name" : 
                file.close()
                return line[1].strip().replace('"', "")
        return "gnome"
    except IOError :
        return "gnome"

def getIcon(mimetype, icons) :
    mimetype = mimetype.replace("/", "-")
    for x in icons :
        icondef = os.path.splitext(x[1])[0]
        if mimetype.find(icondef) != -1 or \
                icondef.find(mimetype) != -1 :
            iconpath = os.path.join(x[0], x[1])
            return iconpath

args = sys.argv
homedir = os.path.expanduser("~")
icons = False

if "-h" in args :
    usage()
    os._exit(0)
if "-i" in args :
    icons = True

mimefiles = ["/usr/share/applications/mimeinfo.cache",
    "/usr/share/applications/mimeapps.list",
    "/usr/local/share/applications/mimeinfo.cache",
    "/usr/local/share/applications/mimeapps.list",
    homedir + "/.local/share/mimeinfo.cache",
    homedir + "/.local/share/mimeapps.list",
    homedir + "/.config/mimeapps.list"]
mimeapps = {}

for x in mimefiles :
    try :
        file = open(x, "r")
    except FileNotFoundError :
        continue
    contents = file.read()
    file.close()
    if contents == "" : continue
    contents = contents.split("\n")
    for y in contents :
        if y.find("=") == -1 : continue
        mime = y[:y.find("=")]
        if y.find(";") != -1 : desktop = y[y.find("=") + 1:y.find(";")]
        else : desktop = y[y.find("=") + 1:]
        mimeapps[mime] = desktop

recentFile = homedir + "/.local/share/recently-used.xbel"
recentFileText = ""
if os.path.exists(recentFile) :
    file = open(recentFile, "r")
    recentFileText = file.read()
    file.close()
recentFileLines = recentFileText.split("\n")
files = []

for x in recentFileLines :
    if x.find("href") != -1 :
        added = ""
        modified = ""
        visited = ""
        if x.find("added") != -1 :
            added = \
            x[x.find("added") + 6:x.find(" ", x.find("added"))].strip('"')
        if x.find("modified") != -1 : 
            modified = \
                x[x.find("modified") + 9:x.find(" ", x.find("modified"))].strip('"')
        if x.find("visited") != -1 : 
            visited = \
                x[x.find("visited") + 8:x.find(" ", x.find("visited"))].strip('"')
        tStamps = [added, modified, visited]
        tStamps = sorted(tStamps, reverse = True)
        filename = x.partition("file://")[2].split(" ")[0]
        filename = html.unescape(filename)
        filename = urllib.parse.unquote(filename)
        filename = filename.strip('"')
        files.append([tStamps[0], filename])
    if x.find("<mime:mime-type type=") != -1 :
        mime = x[x.find("<mime:mime-type type=") + 21:x.find("/>")]
        mime = urllib.parse.unquote(mime)
        mime = html.unescape(mime)
        mime = mime.strip('"').strip("'")
        files[-1].append(mime)
files = sorted(files, key = operator.itemgetter(0), reverse = True)

if icons :
    icontheme = getIconTheme()
    icondirs = ["/usr/share/icons/" + icontheme + "/16x16/mimetypes",
                "/usr/share/icons/" + icontheme + "/16x16/places"]
    icons = []
    for x in icondirs :
        for root, dirs, ifiles in os.walk(x, topdown=False):
            for name in ifiles:
                icons.append((root, name))

counter = 0
print("DestroyMenu recreate RecentFiles")
print("AddToMenu RecentFiles \"Recent Files\" Title")
if len(files) > 0 :
    for x in files :
        if counter < 10 :
            if os.path.exists(x[1]) :
                filename = os.path.basename(x[1])
                if len(filename) > 25 : filename = filename[:22] + "..."
                filename = filename.replace("&", "&&")
                prog = getProgram(x)
                iconpath = None
                if icons : iconpath = getIcon(x[2], icons)
                if icons and iconpath != None :
                    print("+ \"" + filename + " %" + iconpath + "%\" Exec " + \
                        prog + " \"" + x[1] + "\"")
                else :
                    print("+ \"" + filename + "\" Exec " + \
                        prog + " \"" + x[1] + "\"")
                counter += 1
        else : break
    print('+ "" Nop')
    if icons : clearicon = \
            "/usr/share/icons/" + icontheme + "/16x16/actions/edit-clear.png"
    if icons and os.path.exists(clearicon) :
        print("+ \"Clear List %" + clearicon + "%\" Exec rm " + recentFile)
    else :
        print("+ \"Clear List\" Exec rm " + recentFile)
