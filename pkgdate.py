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
instOutput = instOutput[0].decode("utf-8").split("\n")

name = []
date = []

for x in instOutput :
    x = x.partition(":")
    if x[0].rstrip() == "Name" : name.append(x[2].lstrip())
    if x[0].rstrip() == "Install Date" :
        dateElems = x[2].lstrip().split(" ")[1:-1]
        for x in range(len(dateElems)) : 
            if x != len(dateElems) - 1 :
                dateElems[x] = dateElems[x] + " "
        date.append(''.join(dateElems))

instPkgs = [list(x) for x in zip(name, date)]
instPkgs = sorted(instPkgs, key=lambda x: datetime.datetime.strptime(x[1], '%d %b %Y %H:%M:%S'))
if "-n" in args : 
    for x in instPkgs : print (x[0])
else :
    for x in instPkgs : print(x[1] + ", " + x[0])
