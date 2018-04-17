#!/bin/sh
#A script to increase, decrease or toggle the pulseaudio volume. Optionally
#volume notifications can be shown as well.

usage() {
  echo "Usage:
  volume-change.sh ACTION

Actions:
  up: increase the volume by 5%
  down: decrease the volume by 5%
  toggle: mute/unmute the volume"
}

send_notify() {
  if [ $1 -eq 0 ]; then
    icon=audio-volume-muted
  elif [ $1 -gt 30 ] && [ $1 -lt 70 ]; then
    icon=audio-volume-medium
  elif [ $1 -gt 65 ]; then
    icon=audio-volume-high
  else
    icon=audio-volume-low
  fi
  notify-send -h int:value:$1 \
    -h string:x-canonical-private-synchronous:anything " " \
    -i $icon
}

#We test specifically for notify-osd because it is the only notifications
#server that supports the synchronous hint which is needed for the progress bar
notify=0
if [ -f "/usr/bin/notify-send" ] && [ $(pgrep notify-osd) ]; then
  notify=1
fi

if [ "$1" == "toggle" ]; then
  pactl set-sink-mute @DEFAULT_SINK@ toggle
  if [ "$notify" == 1 ]; then
    mute=$(amixer | tr -s ' ' | grep "Front Left: Playback" | cut -d " " -f 7)
    if [ "$mute" == "[off]" ]; then
      send_notify 0 
    else
      volume=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | \
        cut -d "%" -f 1)
      send_notify "$volume"
    fi
  fi
elif [ "$1" == "up" ]; then
  volume=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | \
    cut -d "%" -f 1)
  if [ "$volume" -lt 100 ]; then
    pactl set-sink-mute @DEFAULT_SINK@ false
    pactl set-sink-volume @DEFAULT_SINK@ +5%
  fi
  if [ "$notify" == 1 ]; then
    new_vol=$(expr "$volume" + 5)
    send_notify "$new_vol"
  fi
elif [ "$1" == "down" ]; then
  volume=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | \
    cut -d "%" -f 1)
  if [ "$volume" -gt 0 ]; then
    pactl set-sink-mute @DEFAULT_SINK@ false 
    pactl set-sink-volume @DEFAULT_SINK@ -5%
  fi
  if [ "$notify" == 1 ]; then
    new_vol=$(expr "$volume" - 5)
    send_notify "$new_vol"
  fi
else
  usage
fi
