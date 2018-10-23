#!/usr/bin/python3
#A little python script that displays a countdown to a supplied date and time
#By Charles Bos

import sys
import os
import time
import datetime

def usage() :
    print('''Usage:
    countdown.py "%Y-%m-%d %H:%M:%S"
    countdown.py -t "%H:%M"

Options:
    -t, --time: specify just a time instead of a full date''')

args = sys.argv
now = datetime.datetime.today()

try :
    if "-t" in args or "--time" in args :
        dstring = now.strftime("%Y-%m-%d") + " " + args[2] + ":00"
    else :
        dstring = args[1]
    end = datetime.datetime.strptime(dstring, "%Y-%m-%d %H:%M:%S")
except (ValueError, IndexError) :
    usage()
    os._exit(1)

print("Beginning countdown to " + str(end) + " !!!")

while now <= end :
    sys.stdout.write("\r" + str(end - now).split(".")[0])
    sys.stdout.flush()
    time.sleep(1)
    now = datetime.datetime.today()
sys.stdout.write("\n")

print("Countdown finished !!!")
