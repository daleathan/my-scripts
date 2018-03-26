#!/bin/sh
#A script to increase, decrease or toggle the pulseaudio volume.

usage() {
  echo "Usage:
  volume-change.sh [OPTIONS]

Options:
  up: increase the volume by 5%
  down: decrease the volume by 5%
  toggle: mute/unmute the volume"
}


if [ "$1" == "toggle" ]; then
  pactl set-sink-mute @DEFAULT_SINK@ toggle
elif [ "$1" == "up" ]; then
  volume=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | \
    cut -d "%" -f 1)
  if [ "$volume" -lt 100 ]; then
    pactl set-sink-mute @DEFAULT_SINK@ false
    pactl set-sink-volume @DEFAULT_SINK@ +5%
  fi
  unset volume
elif [ "$1" == "down" ]; then
  volume=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | \
    cut -d "%" -f 1)
  if [ "$volume" -gt 0 ]; then
    pactl set-sink-mute @DEFAULT_SINK@ false 
    pactl set-sink-volume @DEFAULT_SINK@ -5%
  fi
  unset volume
else
  usage
fi
