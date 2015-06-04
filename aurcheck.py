#!/usr/bin/python
#A simple script to check for AUR package updates
#By Charles Bos

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import requests
import os

print("Checking...")

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
    for x in aurPkgs:
        response = requests.get("https://aur.archlinux.org/packages/" + x[0])
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
                    link = "https://aur.archlinux.org/packages/" + x[0][:2] + "/" + x[0] + "/" + x[0] + ".tar.gz"
                    Popen(["wget", "-q", link, "-P", downloadsDir])
                print("\nTarballs have been downloaded. Check: " + downloadsDir)    
except requests.ConnectionError :
    print("Error. Connection to network failed.")
