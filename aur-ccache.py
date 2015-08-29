#!/usr/bin/python
#Remove all cached AUR packages other than the ones installed
#By Charles Bos

from subprocess import Popen, PIPE
import os
import sys

def usage() :
    print('''Usage:
  aur-ccache.py <path to cache> <options>
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
instOutput = (str(instOutput).replace("\\n", " ").replace("b\'", "").replace("\', None", "").strip("()").rstrip(" ")).split(" ")
instOutput = [x for x in instOutput if (x != "") and (x != ":")]

name = []
version = []
arch = []
instPkgs = []

counter = 0
while counter < len(instOutput) :
    if instOutput[counter] == "Name" : name.append(instOutput[counter + 1])
    elif instOutput[counter] == "Version" : version.append(instOutput[counter + 1])
    elif instOutput[counter] == "Architecture" : arch.append(instOutput[counter + 1])
    counter += 1

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
