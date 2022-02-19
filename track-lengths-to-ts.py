#!/usr/bin/python

import os
import sys
import datetime

def usage() :
    print('''track-lengths-to-ts.py - convert a list of track lengths to timestamps
    
Usage:
    ./track-lengths-to-ts.py <path_to_track_lengths_file>
    
    where the track lengths file contains lines of the following form:
        4:04
        4:31''')
        
os.environ['TZ'] = 'UTC'

args = sys.argv

if not len(args) == 2 or not os.path.isfile(args[1]) :
    usage()
    os._exit(1)

current = datetime.datetime.fromtimestamp(0)
timestamps = [current]
file = open(args[1], "r")

for line in file :
    line = line.strip("\r").strip("\n")
    if line.find(":") == -1 :
        raise ValueError("Invalid track length: " + line)
    line = line.split(":")
    if len(line) == 3 :
        hours = int(line[0])
        mins = int(line[1])
        secs = float(line[2])
    else :
        hours = 0
        mins = int(line[0])
        secs = float(line[1])
    delta = datetime.timedelta(hours = hours, minutes = mins, seconds = secs)
    current += delta
    timestamps.append(current)
    
file.close()

for ts in timestamps :
    if ts.hour > 0 :
        print(ts.strftime("%H:%M:%S"))
    else :
        print(ts.strftime("%M:%S"))
    

