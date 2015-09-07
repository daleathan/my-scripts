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
trackNums = []
titles = []

for root, dirs, files in os.walk(musicDir, topdown=False):
    for name in files:
        if name.find(".mp3") != -1 : 
            musicFiles.append((root, os.path.join(root, name)))

for x in musicFiles :
    try :
        audio = ID3(x[1])
        titles.append(str(audio["TIT2"].text[0]))
        trackNums.append(str(audio["TRCK"].text[0]))
    except (ID3NoHeaderError, KeyError) :
        musicFiles.remove(x)

#Add leading 0 if missing
#Remove number of tracks per album if it exists
for x in trackNums :
    if len(x.split("/")[0]) == 1 : trackNums[trackNums.index(x)] = "0" + x
    trackNums[trackNums.index(x)] = x.split("/")[0]

if (len(trackNums) != len(titles)) or (len(trackNums) == len(titles) == 0) :
    print("Music files not found or improperly tagged. Unable to continue.")
    os._exit(0)
else :
    #Start renaming
    counter = 0
    for x in musicFiles :
        os.rename(x[1], os.path.join(x[0], trackNums[counter] + " " + titles[counter] + ".mp3"))
        counter += 1