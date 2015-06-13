#!/bin/bash
#Lock screen with GNOME Screensaver when the monitor is switched off
#Note: works only if monitor is switched off, not if monitor is blanked

#Check if already running and exit immediately if so
RUNNING=$(ps aux | grep gnome-screensaver-idlelock.sh | grep -v grep | wc -l)
if [ "$RUNNING" -gt "2" ]; then
  echo "gnome-screeensaver-idlelock.sh is already running"
  exit 0
fi
 
while true
do
  MONITOR=$(xset -q | grep Monitor)
  SCREENSAVER=$(gnome-screensaver-command -q)
  if [ "$MONITOR" = "  Monitor is Off" ] && [ "$SCREENSAVER" = "The screensaver is inactive" ]; then
    gnome-screensaver-command --lock
  fi
  sleep 1
done
