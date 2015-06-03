#!/bin/bash
# Lock screen with GNOME Screensaver when the monitor is switched off
# Note: works only if monitor is switched off, not if monitor is blanked
 
while true
do
  if [ "$(pidof gnome-screensaver)" ]; then
    MONITOR=$(xset -q | grep Monitor)
    SCREENSAVER=$(gnome-screensaver-command -q)
    if [ "$MONITOR" = "  Monitor is Off" ] && [ "$SCREENSAVER" = "The screensaver is inactive" ]; then
      gnome-screensaver-command --lock
    fi
    sleep 1
  else
    exit 0
  fi
done
