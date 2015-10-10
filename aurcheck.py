#!/usr/bin/python
#A simple script to check for AUR package updates
#By Charles Bos

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import requests
import os

def versionCheck(localVer, aurVer) :
    #Compare versions by splitting version string at "." and comparing each number in turn -
    #letters will be converted into their ascii codes. If lengths are not equal after
    #splitting, this cannot be done properly so fall back to simple string comparison.
    #Return 0 immediately if vers are equal. Return 1 for updates and return -1 for mismatches -
    #(where local ver is newer than aur ver).
    if localVer == aurVer : return 0
    versions = [localVer, aurVer]
    for x in versions :
        y = list(x.replace("-", "."))
        for z in range(0, len(y) - 1) :
            if y[z] != "." :
                try :
                    int(y[z])
                except ValueError :
                    y[z] = str(ord(y[z]))
        y = ''.join(y)
        y = y.split(".")
        versions[versions.index(x)] = y
    if len(versions[0]) == len(versions[1]) :
        counter = 0
        while counter < len(versions[0]) :
            if int(versions[1][counter]) > int(versions[0][counter]) : return 1
            elif int(versions[1][counter]) < int(versions[0][counter]) : return -1
            counter += 1
    else :
        if aurVer > localVer : return 1
        elif aurVer < localVer : return -1
        
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
        comparison = versionCheck(x[1], version)
        if comparison == 1 : 
            updates.append(str(x[0] + " " +x[1] + " --> " + version))
            pkgBaseStart = page.find('''<a href="https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=''')
            pkgBaseEnd = page.find('''">View PKGBUILD</a> /''')
            pkgBase = page[pkgBaseStart + 64:pkgBaseEnd]
            if x[0] != pkgBase : splitPkgs.append(str(x[0] + " " +x[1] + " --> " + version))
        elif comparison == -1 : mismatches.append(str(x[0] + " - (local) " +x[1] + " (AUR) " + version))

if updates == mismatches == failures == [] : print("Everything is up to date.")
else :
    if failures != [] :
        print("The following packages were not found in the AUR:\n-----")
        for x in failures : print(x)
        if (mismatches != []) or (updates != []) : print()
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
