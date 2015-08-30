#!/bin/bash
#Lock screen with Cinnamon Screensaver after 10 minutes idle time
#Requires xprintidle

#Check if already running and exit immediately if so
RUNNING=$(pgrep -f -c cinnamon-screensaver-idlelock.sh)
if [ ! "$RUNNING" = "1" ]; then
  echo "cinnamon-screensaver-idlelock.sh is already running"
  exit 0
fi
 
while true
do
  IDLE=$(xprintidle)
  SCREENSAVER=$(cinnamon-screensaver-command -q)
  if [ "$IDLE" -ge 600000 ] && [ "$SCREENSAVER" = "The screensaver is inactive" ]; then
    if [ $(pgrep -f xfce4-power-manager) ]; then
      PRESENTATION_MODE=$(xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode)
      if [ "$PRESENTATION_MODE" = "false" ]; then
        cinnamon-screensaver-command --lock
      fi
    else
      cinnamon-screensaver-command --lock
    fi
  fi
  sleep 1
done
