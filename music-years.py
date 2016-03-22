#!/usr/bin/python
#Silly Python script to analyse music collection by year of release

import os
import math
import sys
from mutagen.id3 import ID3, ID3NoHeaderError

def usage() :
    print('''Usage:
  music-years.py <path to music>
  Note: without the path to music argument, the path is taken to be ~/Music''')

# Get music directory
args = sys.argv
if len(args) > 1 :
    if (args[1] == '-h') or (args[1] == '--help') :
        usage()
        os._exit(0)
    elif os.path.exists(args[1]) : musicDir = args[1]
    else :
        usage()
        os._exit(0)
elif os.path.exists(os.path.expanduser('~') + "/Music") : musicDir = os.path.expanduser('~') + "/Music"
else :
    usage()
    os._exit(0)

# Get dates for music files
musicFiles = []
years = []

for root, dirs, files in os.walk(musicDir, topdown=False):
    for name in files:
        musicFiles.append(os.path.join(root, name))

for x in musicFiles :
    try :
        audio = ID3(x)
        years.append(int(str(audio["TDRC"].text[0])))
    except (ID3NoHeaderError, KeyError) :
        pass

if years == [] :
    print("No valid music files found. Nothing to do. Exiting...")
    os._exit(0)
else :
    # Begin reporting results
    print("Number of files found: " + str(len(musicFiles)))
    print("Number of tagged tracks found: " + str(len(years)) + "\n")

    # Report mean
    total = 0
    for x in years : total += x
    print("Mean year of release for your music: " + str(math.floor((total / len(years)) + 0.5)))

    # Report median
    years = sorted(years)
    if len(years) % 2 != 0 : print("Median year of release for your music: " + str(years[int((len(years) / 2) + 0.5)]))
    else :
        year1 = years[int(len(years) / 2)]
        year2 = years[int((len(years) / 2) + 1)]
        medianYear = math.floor(((year1 + year2) / 2) + 0.5)
        print("Median year of release for your music: " + str(medianYear))

    # Report mode
    modeList = []
    counter = 0
    for x in years :
        if x != years[counter - 1] :
            temp = [y for y in years if y == x]
            modeList += [temp]
        counter += 1
    modeList.sort(key=len, reverse=True)
    if modeList != [] : print("Mode year of release for your music: " + str(modeList[0][0]) + " (" + str(len(modeList[0])) + " tracks)")
    else : print("Mode year of release for your music: " + str(years[0]) + " (" + str(len(years)) + " tracks)")

    # Top years for tracks
    print("\nTop years for tracks (max 10)")
    counter = 0
    if modeList != [] :
        while (counter < 10) and (counter < len(modeList)) :
            print(str(counter + 1) + ": " + str(modeList[counter][0]) + " (" + str(len(modeList[counter])) + " tracks)")
            counter += 1
    else : print("1: " + str(years[0]) + " (" + str(len(years)) + " tracks)")

    # Report tracks per decade
    def getDecade(x) :
        return int(str(x)[:-1]) * 10

    decades = []

    trackDecs = years[:]
    counter = 0
    while counter < len(trackDecs) :
        trackDecs[counter] = getDecade(trackDecs[counter])
        counter += 1

    counter = 0
    for x in trackDecs :
        if x != trackDecs[counter -1] :
            temp = [y for y in trackDecs if y == x]
            decades += [temp]
        counter += 1
    if decades == [] : decades += [trackDecs]
    decades.sort(key=len, reverse=True)

    print("\nNumber of tracks per decade")
    counter = 0
    while counter < len(decades) :
        print(str(counter + 1) + ": " + str(decades[counter][0]) + "s (" + str(len(decades[counter])) + " tracks) (" + str(round(len(decades[counter]) / len(years) * 100, 2)) + "%)")
        counter += 1
    print("\n* percentages are rounded")
