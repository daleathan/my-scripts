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
tracknums = []
titles = []

for root, dirs, files in os.walk(musicDir, topdown=False):
    for name in files:
        if name.find(".mp3") != -1 : 
            musicFiles.append(os.path.join(root, name))

for x in musicFiles :
    try :
        audio = ID3(x)
        titles.append(str(audio["TIT2"].text[0]))
        tracknums.append(str(audio["TRCK"].text[0]))
    except (ID3NoHeaderError, KeyError) :
        musicFiles.remove(x)

#Add leading 0 if missing
for x in tracknums :
    if len(x) == 1 : tracknums[tracknums.index(x)] = "0" + x

if (len(tracknums) != len(titles)) or (len(tracknums) == len(titles) == 0) :
    print("Music files not found or improperly tagged. Unable to continue.")
    os._exit(0)
else :
    #Start renaming
    def getPath(origSong) :
        return origSong.rfind("/") + 1
 
    counter = 0
    for x in musicFiles :
        path = x[:getPath(x)]
        os.rename(x, path + tracknums[counter] + " " + titles[counter] + ".mp3")
        counter += 1