#!/usr/bin/python
#A simple script to check for AUR package updates
#By Charles Bos

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import requests
import os

aurPkgs = Popen(["pacman", "-Qm"], stdout = PIPE).communicate()
aurPkgs = (str(aurPkgs).replace("\\n", " ").replace("b\'", "").replace("\', None", "").strip("()").rstrip(" ")).split(" ")

counter = 0
while counter < len(aurPkgs) - 1 :
    aurPkgs[counter] = (aurPkgs[counter], aurPkgs[counter + 1])
    del aurPkgs[counter + 1]
    counter += 1
    
updates = []
splitPkgs = []
mismatches = []
failures = []
devel = ["-git", "-bzr", "-svn", "-hg"]

for x in aurPkgs:
    try :
        response = requests.get("https://aur.archlinux.org/packages/" + x[0])
    except requests.ConnectionError :
        print("Error. Connection to network failed.")
        os._exit(0)
    page = str(BeautifulSoup(response.content, "html.parser"))
    start = page.find("<h2>Package Details: ")
    if start == -1 : failures.append(x[0])
    else :
        end = page.find("</h2>", start)
        version = page[start + 21:end].split(" ")[1]
        if x[1] < version : 
            updates.append(str(x[0] + " " +x[1] + " --> " + version))
            pkgBaseStart = page.find('''<a href="https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=''')
            pkgBaseEnd = page.find('''">View PKGBUILD</a> /''')
            pkgBase = page[pkgBaseStart + 64:pkgBaseEnd]
            if x[0] != pkgBase : splitPkgs.append(str(x[0] + " " +x[1] + " --> " + version))
        elif x[1] > version : 
            if not any(y in x[0] for y in devel) : mismatches.append(str(x[0] + " " +x[1] + " --> " + version))  

if updates == mismatches == failures == [] : print("Everything is up to date.")
else :
    if failures != [] :
        print("The following packages were not found in the AUR:\n-----")
        for x in failures : print(x)
        if mismatches != [] : print()
    if mismatches != [] :
        print("The following local packages are more recent than their AUR versions:\n-----")
        for x in mismatches : print(x)
        if updates != [] : print()
    if updates != [] :
        print("The following packages have updates available:\n-----")
        for x in updates : print(x)
        fetch = input("\nFetch updated tarballs? [y/n] ")
        if fetch == "y" :
            homeDir = os.path.expanduser('~')
            if os.path.exists(homeDir + "/Downloads") : downloadsDir = homeDir + "/Downloads"
            else : downloadsDir = homeDir
            for x in updates :
                if x in splitPkgs : continue
                newPkg = x.split(' ')[0]
                pkgUrl = "https://aur.archlinux.org/cgit/aur.git/snapshot/" + newPkg + ".tar.gz"
                Popen(["wget", "-q", pkgUrl, "-P", downloadsDir]).wait()
                if os.path.exists(downloadsDir + "/" + newPkg + ".tar.gz") : completion = "SUCCESS"
                else : completion = "FAILURE"
                print("Fetch: " + newPkg + ".tar.gz - " + completion)
            print("\nDownloads completed. Check: " + downloadsDir)
