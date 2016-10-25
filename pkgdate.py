#!/usr/bin/python3
#List packages by date of installation
#By Charles Bos

from subprocess import Popen, PIPE
import datetime
import sys
import os

def usage() :
    print('''Usage:
  pkgdate.py <options>

Options:
  -h: Display this dialog
  -e: List explicitly installed packages only
  -m: List local packages only
  -n: List package names only''')

args = sys.argv

if "-h" in args :
    usage()
    os._exit(0)

pacOpts = "-Qi"
if "-e" in args : pacOpts += "e"
if "-m" in args : pacOpts += "m"

instOutput = Popen(["pacman", pacOpts], stdout = PIPE).communicate()
instOutput = (str(instOutput).replace("\\n", " ").replace("b\'", "").replace("\', None", "").strip("()").rstrip(" ")).split(" ")
instOutput = [x for x in instOutput if (x != "") and (x != ":")]
instOutput[0] = instOutput[0].lstrip('''b"''')

name = []
date = []

counter = 0
while counter < len(instOutput) :
    if instOutput[counter] == "Name" : name.append(instOutput[counter + 1])
    elif (instOutput[counter] == "Install") and (instOutput[counter + 1] == "Date") :
        counter2 = 3
        temp = str()
        while counter2 < 7 :
            temp += instOutput[counter + counter2] + " "
            counter2 += 1
        date.append(temp.rstrip(" "))
    counter += 1

instPkgs = [list(x) for x in zip(name, date)]
instPkgs = sorted(instPkgs, key=lambda x: datetime.datetime.strptime(x[1], '%d %b %Y %H:%M:%S'))
if "-n" in args : 
    for x in instPkgs : print (x[0])
else :
    for x in instPkgs : print(x[0] + ", " + x[1])
