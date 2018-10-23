#!/usr/bin/python3
#A little python script that displays a countdown to a supplied date and time
#By Charles Bos

import sys
import os
import time
import datetime

def usage() :
    print('''Usage:
    countdown.py "%Y-%m-%d %H:%M:%S"''')

try :
    end = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
except (ValueError, IndexError) :
    usage()
    os._exit(1)
now = datetime.datetime.today()

print("Beginning countdown to " + str(end) + " !!!")

while now <= end :
    sys.stdout.write("\r" + str(end - now).split(".")[0])
    sys.stdout.flush()
    time.sleep(1)
    now = datetime.datetime.today()
sys.stdout.write("\n")

print("Countdown finished !!!")
