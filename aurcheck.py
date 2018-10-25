#!/usr/bin/python3
#A simple script to check for AUR package updates
#By Charles Bos

from subprocess import Popen, PIPE
from bs4 import BeautifulSoup
import requests
import os

def versionCheck(localVer, aurVer) :
    if localVer == aurVer : return 0
    if (aurVer.find(":") != -1) and (localVer.find(":") == -1) : return 1
    if (aurVer.find(":") == -1) and (localVer.find(":") != -1) : return -1
    versions = [localVer, aurVer]
    for x in versions :
        y = list(x.replace("-", "."))
        for z in range(0, len(y)) :
            if y[z] != "." :
                try :
                    int(y[z])
                except ValueError :
                    y[z] = str(ord(y[z]))
        y = ''.join(y)
        y = y.split(".")
        versions[versions.index(x)] = y
    for x in range(0, min(len(versions[0]), len(versions[1]))) :
        if int(versions[1][x]) > int(versions[0][x]) : return 1
        elif int(versions[1][x]) < int(versions[0][x]) : return -1
    if len(versions[0]) != len(versions[1]) :
        if len(versions[1]) > len(versions[0]) : return 1
        else : return -1
    else : return 0

aurPkgs = Popen(["pacman", "-Qm"], stdout = PIPE).communicate()
aurPkgs = aurPkgs[0].decode("utf-8").replace("\n", " ").rstrip(" ").split(" ")

counter = 0
while counter < len(aurPkgs) - 1 :
    aurPkgs[counter] = (aurPkgs[counter], aurPkgs[counter + 1])
    del aurPkgs[counter + 1]
    counter += 1
    
updates = []
mismatches = []
failures = []

splitPkgs = {}

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
            if x[0] != pkgBase : splitPkgs[str(x[0] + " " +x[1] + " --> " + version)] = pkgBase
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
        if "wget" in os.listdir("/usr/bin") :
            fetch = input("\nFetch updated tarballs? [y/n] ")
            if fetch == "y" :
                homeDir = os.path.expanduser('~')
                if os.path.exists(homeDir + "/Downloads") : downloadsDir = homeDir + "/Downloads"
                else : downloadsDir = homeDir
                print("Downloading to " + downloadsDir + "\n")
                downloaded = []
                for x in updates :
                    if x in splitPkgs : 
                        newPkg = splitPkgs[x]
                    else :
                        newPkg = x.split(' ')[0]
                    if newPkg in downloaded : continue
                    pkgUrl = "https://aur.archlinux.org/cgit/aur.git/snapshot/" + newPkg + ".tar.gz"
                    Popen(["wget", "-q", pkgUrl, "-O", downloadsDir + "/" + newPkg + ".tar.gz"]).wait()
                    if os.path.exists(downloadsDir + "/" + newPkg + ".tar.gz") : completion = "SUCCESS"
                    else : completion = "FAILURE"
                    print("Fetch: " + newPkg + ".tar.gz - " + completion)
                    downloaded.append(newPkg)
