#!/usr/bin/python
#List packages by date of installation
#By Charles Bos

from subprocess import Popen, PIPE
import datetime

instOutput = Popen(["pacman", "-Qi"], stdout = PIPE).communicate()
instOutput = (str(instOutput).replace("\\n", " ").replace("b\'", "").replace("\', None", "").strip("()").rstrip(" ")).split(" ")
instOutput = [x for x in instOutput if (x != "") and (x != ":")]

name = []
date = []
instPkgs = []

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

counter = 0
while counter < len(name) :
    instPkgs.append((name[counter], date[counter]))
    counter += 1

instPkgs = sorted(instPkgs, key=lambda x: datetime.datetime.strptime(x[1], '%d %b %Y %H:%M:%S'))

for x in instPkgs : print(x[0] + ", " + x[1])
