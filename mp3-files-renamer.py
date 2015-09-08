#!/usr/bin/python
#Python script to rename mp3 files according to the format
#"Track-number Track-name.mp3", for example: 02 Self Control.mp3
#Note: Tracks must have valid ID3 data for this to work - python-mutagen is required.
#By Charles Bos

import os
import sys
from mutagen.id3 import ID3, ID3NoHeaderError

def usage() :
    print('''Usage:
  mp3-file-renamer.py <path to music>''')

#Get music directory
args = sys.argv
if (len(args) != 2) or (args[1] == '-h') or (args[1] == '--help') :
    usage()
    os._exit(0)
else :
    if os.path.exists(args[1]) : musicDir = args[1]
    else :
        usage()
        os._exit(0)

#Get titles and track numbers for songs
musicFiles = []
convList = []
ignore = []

for root, dirs, files in os.walk(musicDir, topdown=False):
    for name in files:
        if name.find(".mp3") != -1 : 
            musicFiles.append((root, os.path.join(root, name)))

for x in musicFiles :
    try :
        audio = ID3(x[1])
        title = str(audio["TIT2"].text[0])
        trackNum = str(audio["TRCK"].text[0])
        convList.append([trackNum, title])
    except (ID3NoHeaderError, KeyError, PermissionError) :
        ignore.append(x)

#Remove problem files from list
for x in ignore : musicFiles.remove(x)

#Add leading 0 if missing
#Remove number of tracks per album if it exists
for x in convList :
    if len(x[0].split("/")[0]) == 1 : convList[convList.index(x)][0] = "0" + x[0]
    convList[convList.index(x)][0] = x[0].split("/")[0]

#If no files to convert, report problem files and exit
if len(convList) == 0 :
    if len(convList) == 0 and len(ignore) == 0:
        print("No music files were found.")
    elif len(convList) == 0 and len(ignore) != 0 :
        print("Some music files were found but none were renamable.\n\nCheck the tags and permissions on the following files:\n-----")
        for x in ignore : print(x[1])
    os._exit(0)
else :
    #Start renaming
    counter = 0
    for x in musicFiles :
        os.rename(x[1], os.path.join(x[0], convList[counter][0] + " " + convList[counter][1] + ".mp3"))
        counter += 1
    print(str(len(convList)) + " files were successfully renamed.")
    if len(ignore) > 0 :
        print("\nSome files could not be renamed.\nCheck the tags and permissions on the following files:\n-----")
        for x in ignore : print(x[1])