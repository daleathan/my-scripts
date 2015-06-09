#!/usr/bin/python
#A simple script to check for AUR package updates
#By Charles Bos

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import requests
import os
import sys

args = sys.argv
if ('-h' in args) or ('--help' in args) : print('''Usage:
  -h, --help: Print this help message
  -aur4: Check the new git based AUR instead of the current AUR 3
  --strict: AUR 4 option. Assume that untransitioned packages are not in AUR 4''')
else :
    print("Checking...")
    
    if '-aur4' in args : aurVer = 4
    else : aurVer = 3

    aurPkgs = Popen(["pacman", "-Qm"], stdout = PIPE).communicate()
    aurPkgs = (str(aurPkgs).replace("\\n", " ").replace("b\'", "").replace("\', None", "").strip("()").rstrip(" ")).split(" ")

    counter = 0
    while counter < len(aurPkgs) - 1 :
        aurPkgs[counter] = (aurPkgs[counter], aurPkgs[counter + 1])
        del aurPkgs[counter + 1]
        counter += 1
        
    try :
        updates = []
        mismatches = []
        failures = []
        if aurVer == 4 : aurUrl = "https://aur4.archlinux.org/packages/"
        else : aurUrl = "https://aur.archlinux.org/packages/"
        
        for x in aurPkgs:
            if (aurVer == 4) and ('--strict' in args) :
                response = requests.get("https://aur4.archlinux.org/cgit/aur.git/log/?h=" + x[0])
                existCheck = str(BeautifulSoup(response.content))
                if existCheck.find("Invalid branch: " + x[0]) != -1 : failures.append("Check for " + x[0] + " failed. Is it in the AUR?")
            else :    
                response = requests.get(aurUrl + x[0])
                page = str(BeautifulSoup(response.content))
                start = page.find("<h2>Package Details: ") + 21
                if start == 20 : failures.append("Check for " + x[0] + " failed. Is it in the AUR?")
                else :
                    end = page.find("</h2>", start)
                    version = page[start:end].split(" ")[1]
                    if x[1] < version : updates.append((x[0], str("Update for " + x[0] + " is available: " + x[1] + " --> " + version)))
                    elif x[1] > version : mismatches.append(str("Local " + x[0] + " looks newer than AUR version: " + x[1] + " --> " + version))

        if updates == mismatches == failures == [] : print("\nEverything is up to date.")
        else :
            if failures != [] :
                print("\nSearch failures:\n----------------")
                for x in failures : print(x)
            if mismatches != [] :
                print("\nLocal remote mismatches:\n------------------------")
                for x in mismatches : print(x)
            if updates != [] :
                print("\nAvailable updates:\n------------------")
                for x in updates : print(x[1])
                fetch = input("\nFetch updated tarballs? [y/n] ")
                if fetch == "y" :
                    if os.path.exists(os.path.expanduser('~') + "/Downloads") : downloadsDir = os.path.expanduser('~') + "/Downloads"
                    else : downloadsDir = os.path.expanduser('~')
                    for x in updates :
                        print("Fetching: " + x[0] + ".tar.gz")
                        if aurVer == 4 : pkgUrl = "https://aur4.archlinux.org/cgit/aur.git/snapshot/" + x[0] + ".tar.gz"
                        else : pkgUrl = "https://aur.archlinux.org/packages/" + x[0][:2] + "/" + x[0] + "/" + x[0] + ".tar.gz"
                        Popen(["wget", "-q", pkgUrl, "-P", downloadsDir])
                    print("\nTarballs have been downloaded. Check: " + downloadsDir)    
    except requests.ConnectionError :
        print("Error. Connection to network failed.")
