#!/usr/bin/python
#Copy compiled packages to AUR cache and remove the original tarballs and build dirs
#By Charles Bos

import os
import sys
import shutil

def usage() :
    print('''Usage:
  aur-cache.py <path to cache> <path to pkg location>
  Note: 
    * without the path to cache argument, the path is taken to be ~/.aurcache
    * without the path to pkg location argument, the path is taken to be ~/Downloads''')

#Get cache and pkg location dirs
args = sys.argv
homeDir = os.path.expanduser('~')
if len(args) == 1 :
    if (os.path.exists(homeDir + "/.aurcache")) and (os.path.exists(homeDir + "/Downloads")) :
        cacheDir = homeDir + "/.aurcache"
        pkgDir = homeDir + "/Downloads"
    else :
        usage()
        os._exit(0)
elif len(args) == 2 :
    if (os.path.exists(args[1])) and (os.path.exists(homeDir + "/Downloads")) :
        cacheDir = args[1]
        pkgDir = homeDir + "/Downloads"
    else :
        usage()
        os._exit(0)
elif len(args) == 3 :
    if (os.path.exists(args[1])) and (os.path.exists(args[2])) :
        cacheDir = args[1]
        pkgDir = args[2]
    else :
        usage()
        os._exit(0)
else :
    usage()
    os._exit(0)

#Check for pkg files in each dir
dirs = os.listdir(pkgDir)
counter = 0
while counter < len(dirs) :
    dirs[counter] = pkgDir + "/" + dirs[counter]
    counter += 1
for x in dirs :
    try :
        contents = os.listdir(x)
        counter = 0
        while counter < len(contents) :
            contents[counter] = x + "/" + contents[counter]
            counter += 1
    except (NotADirectoryError, FileNotFoundError) :
        continue
    #Copy found package files
    contains = False
    for y in contents :
        if y.find(".pkg.tar.xz") != -1 :
            shutil.copyfile(y, cacheDir + "/" + y.split("/")[-1])
            contains = True
    #For dirs containing pkg files, remove them and also remove the
    #original tar.gz file
    if contains :
        shutil.rmtree(x)
        try : 
            os.remove(x + ".tar.gz")
        except FileNotFoundError : 
            pass

print("Done")
