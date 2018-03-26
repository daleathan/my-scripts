#!/usr/bin/python3
#Remove all cached AUR packages other than the ones installed
#By Charles Bos

from subprocess import Popen, PIPE
import os
import sys

def usage() :
    print('''Usage:
  aur-ccache.py <path to cache>
  Note: without the path to cache argument, the path is taken to be ~/.aurcache''')

# Get cache directory
args = sys.argv
if len(args) > 1 :
    if (args[1] == '-h') or (args[1] == '--help') :
        usage()
        os._exit(0)
    elif os.path.exists(args[1]) : cacheDir = args[1]
    else :
        usage()
        os._exit(0)
elif os.path.exists(os.path.expanduser('~') + "/.aurcache") : cacheDir = os.path.expanduser('~') + "/.aurcache"
else :
    usage()
    os._exit(0)

#Get package list in cache
cachePkgs = os.listdir(cacheDir)

#Get installed AUR package list
instOutput = Popen(["pacman", "-Qmi"], stdout = PIPE).communicate()
instOutput = (str(instOutput).replace("b\'", "").replace("\', None", "").replace(" ", "").strip("()").lstrip('''"b''')).split("\\n")
instOutput = [x for x in instOutput if (x != "") and (x != ":")]

name = []
version = []
arch = []
instPkgs = []

for x in instOutput :
    if x[:5] == "Name:" : name.append(x[5:])
    elif x[:8] == "Version:" : version.append(x[8:])
    elif x[:13] == "Architecture:" : arch.append(x[13:])

#Exit if package info extraction failed
if not (len(name) == len(version) == len(arch)) :
    print("Error getting names of installed packages.")
    os._exit(0)

counter = 0
while counter < len(name) :
    pkgName = name[counter] + "-" + version[counter] + "-" + arch[counter] + ".pkg.tar.xz"
    instPkgs.append(pkgName)
    counter += 1

#Check cache packages against installed ones
oldPkgs = []
for x in cachePkgs :
    if x not in instPkgs : 
        if x.find(".pkg.tar.xz") != -1 : oldPkgs.append(x)
oldPkgs = sorted(oldPkgs)

#Show packages to be removed and remove them if specified
if len(oldPkgs) > 0 :
    print("Packages to be removed:\n-----")
    for x in oldPkgs : print(x)
    remove = input("\nWould you like to remove these packages? [y/n] ")
    if remove == "y" :
        for x in oldPkgs : os.remove(cacheDir + "/" + x)
        print("All old packages removed.")
else : 
    print("No packages to be removed.")
