#!/usr/bin/python
#Silly Python script to analyse music collection by year of release

import os
import math

homeDir = os.path.expanduser('~')
rboxDir = homeDir + '/.local/share/rhythmbox/rhythmdb.xml'

file = open(rboxDir, 'r')
contents = file.read()
file.close()

years = []
yearStart = contents.find('<date>')
yearEnd = contents.find('</date>', yearStart)

while 0 <= yearStart <= len(contents) :
    yearExtract = int(contents[yearStart + 6:yearEnd])
    year = math.floor((yearExtract / 365.05) + 0.5)
    years += [year]
    yearStart = contents.find('<date>', yearEnd)
    yearEnd = contents.find('</date>', yearStart)
years = [x for x in years if len(str(x)) == 4]
    
# Begin reporting results
print("Your results:\n")

# Report mean
total = 0
for x in years : total += x
print("Mean year of release for your music: " + str(math.floor((total / len(years)) + 0.5)))

# Report median
years = sorted(years)
if len(years) % 2 != 0 : print("Median year of release for your music: " + str(years[(len(years) / 2) + 0.5]))
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
print("Mode year of release for your music: " + str(modeList[0][0]) + " (" + str(len(modeList[0])) + " tracks)")

# Top and bottom 10 years for tracks
print("\nTop 10 years for tracks")
counter = 0
while counter < 10 :
    print(str(counter + 1) + ": " + str(modeList[counter][0]) + " (" + str(len(modeList[counter])) + " tracks)")
    counter += 1

print("\nBottom 10 years for tracks")
counter = -1
while counter > -11 :
    print(str(abs(counter)) + ": " + str(modeList[counter][0]) + " (" + str(len(modeList[counter])) + " tracks)")
    counter -= 1

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
decades.sort(key=len, reverse=True)

print("\nNumber of tracks per decade")
counter = 0
while counter < len(decades) :
    print(str(counter + 1) + ": " + str(decades[counter][0]) + "s (" + str(len(decades[counter])) + " tracks)")
    counter += 1
    

        
    
    
    
    
