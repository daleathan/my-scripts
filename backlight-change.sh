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
    -i notification-display-brightness
}

get_xrandr_brightness() {
  xrandr --verbose | grep " connected" -A 50 | grep "Brightness" -m 1 | cut -d " " -f 2
}

#We test specifically for notify-osd because it is the only notifications
#server that supports the synchronous hint which is needed for the progress bar
notify=0
if [ -f "/usr/bin/notify-send" ] && [ "$(pgrep notify-osd)" ]; then
  notify=1
fi

#Also test that xbacklight actually works and use xrandr (changing brightness
#in software) as a fallback it it doesn't
xb_mode=1
xb_out=$(xbacklight 2>&1)
monitor="undefined"
if [ ! $? -eq 0 ] || [ ! "$xb_out" ]; then
  xb_mode=0
  monitor=$(xrandr | grep " connected" | cut -d " " -f 1)
fi

if [ "$1" == "up" ]; then
  if [ $xb_mode -eq 1 ]; then
    xbacklight -inc 10
    if [ "$notify" == 1 ]; then
      level=$(xbacklight -get)
      send_notify $(echo "(${level}+0.5)/1" | bc)
    fi
  else
    level=$(get_xrandr_brightness)
    newlevel=$(bc <<< "scale=2; $level + 0.1;")
    if [ $(bc <<< "scale=2; $newlevel <= 1.0;") -eq 1 ]; then
      xrandr --output "$monitor" --brightness $newlevel
      send_notify $(bc <<< "scale=2; $newlevel * 100")
    fi
  fi
elif [ "$1" == "down" ]; then
  if [ $xb_mode -eq 1 ]; then
    xbacklight -dec 10
    if [ "$notify" == 1 ]; then
      level=$(xbacklight -get)
      send_notify $(echo "(${level}+0.5)/1" | bc)
    fi
  else
    level=$(get_xrandr_brightness)
    newlevel=$(bc <<< "scale=2; $level - 0.1;")
    if [ $(bc <<< "scale=2; $newlevel >= 0.0;") -eq 1 ]; then
      xrandr --output "$monitor" --brightness $newlevel
      send_notify $(bc <<< "scale=2; $newlevel * 100")
    fi
  fi
else
  usage
fi
