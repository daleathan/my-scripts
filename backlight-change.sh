#!/bin/sh
#A script to brighten or dim the backlight under X.org. Optionally 
#notifications can be shown as well.

usage() {
  echo "Usage:
  backlight-change.sh ACTION

Actions:
  up: increase backlight brightness by 10%
  down: decrease backlight brightness by 10%"
}

send_notify() {
  notify-send -h int:value:$1 \
    -h string:x-canonical-private-synchronous:anything " " \
    -i dialog-information
}

#We test specifically for notify-osd because it is the only notifications
#server that supports the synchronous hint which is needed for the progress bar
notify=0
if [ -f "/usr/bin/notify-send" ] && [ "$(pgrep notify-osd)" ]; then
  notify=1
fi

if [ "$1" == "up" ]; then
  xbacklight -inc 10
  if [ "$notify" == 1 ]; then
    level=$(xbacklight -get)
    send_notify $(echo "(${level}+0.5)/1" | bc)
  fi
elif [ "$1" == "down" ]; then
  xbacklight -dec 10
  if [ "$notify" == 1 ]; then
    level=$(xbacklight -get)
    send_notify $(echo "(${level}+0.5)/1" | bc)
  fi
else
  usage
fi
