#!/usr/bin/python3
#Script to split an album contained in one m4a file into its constituent
#tracks, preserving the thumbnail in the original file. Takes as an argument
#the path to the m4a file and the path to a timestamps file which contains lines
#of the form: 05:17|Song Title. Requires FFmpeg and AtomicParsley.

import os
import sys
import datetime

def usage() :
    print("split-chapters.py <path to media file> <path to timestamps file>")
    
args = sys.argv
if len(args) != 3 or not os.path.isfile(args[1]) or not os.path.isfile(args[2]) :
    usage()
    os._exit(1)
    
media = args[1]
timestamps = args[2]
ext = os.path.splitext(media)[1]

cmd = "ffmpeg -i \"" + media + "\" -map 0:1 thumbnail.png"
status = os.system(cmd)
if status != 0 :
    raise ValueError("Error extracting thumbnail. Command was: " + cmd)
    
parts = []

file = open(timestamps, "r", encoding="utf8")
counter = 1
for line in file :
    line = line.strip("\r").strip("\n").split("|")
    if len(line) != 2 :
        raise ValueError("Line should only contain: start_ts|title")
    start_ts = line[0]
    if len(start_ts.split(":")) != 2 and len(start_ts.split(":")) != 3 :
        raise ValueError("Invalid start timestamp: " + start_ts)
    title = line[1]
    parts.append([start_ts, title, ""])
file.close()

for x in range(len(parts) - 1) :
    start_ts = parts[x][0].split(":")
    end_ts = parts[x + 1][0].split(":")
    if len(start_ts) == 2 :
        start_hours = 0
        start_mins = int(start_ts[0])
        start_secs = int(start_ts[1])
    else :
        start_hours = int(start_ts[0])
        start_mins = int(start_ts[1])
        start_secs = int(start_ts[2])
    if len(end_ts) == 2 :   
        end_hours = 0
        end_mins = int(end_ts[0])
        end_secs = int(end_ts[1])
    else :
        end_hours = int(end_ts[0])
        end_mins = int(end_ts[1])
        end_secs = int(end_ts[2])
    start_td = datetime.timedelta(hours = start_hours, minutes = start_mins, seconds = start_secs)
    end_td = datetime.timedelta(hours = end_hours, minutes = end_mins, seconds = end_secs)
    parts[x][2] = str((end_td - start_td).total_seconds())
    
for part in parts :
    start_ts = part[0]
    title = part[1]
    duration = part[2]
    outfile = str(counter).rjust(2, '0') + " " + title + ext
    if duration != "" :
        cmd = "ffmpeg -i \"" + media + "\" -ss " + start_ts + " -t " + duration + " -map 0:0 -c copy \"" + outfile + "\""
    else :
        cmd = "ffmpeg -i \"" + media + "\" -ss " + start_ts + " -map 0:0 -c copy \"" + outfile + "\""
    print(cmd)
    status = os.system(cmd)
    if status != 0 :
        raise ValueError("Error extracting track. Command was: " + cmd)
    cmd = "AtomicParsley \"" + outfile + "\" --artwork thumbnail.png --output \"" + outfile + ".1\""
    status = os.system(cmd)
    if status != 0 :
        raise ValueError("Error setting thumbnail. Command was: " + cmd)
    os.replace(outfile + ".1", outfile)
    counter += 1    