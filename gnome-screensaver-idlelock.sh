#!/bin/bash
#Lock screen with GNOME Screensaver after 10 minutes idle time
#Requires xprintidle

#Check if already running and exit immediately if so
RUNNING=$(pgrep -f -c gnome-screensaver-idlelock.sh)
if [ ! "$RUNNING" = "1" ]; then
  echo "gnome-screensaver-idlelock.sh is already running"
  exit 0
fi
 
while true
do
  IDLE=$(xprintidle)
  SCREENSAVER=$(gnome-screensaver-command -q)
  if [ "$IDLE" -ge 600000 ] && [ "$SCREENSAVER" = "The screensaver is inactive" ]; then
    gnome-screensaver-command --lock
  fi
  sleep 1
done
