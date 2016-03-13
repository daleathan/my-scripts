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
  pactl set-sink-mute $(pactl list sinks short | cut -f 1) toggle
elif [ "$1" == "up" ]; then
  if [ $(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | cut -d "%" -f 1) -lt 100 ]; then
    pactl set-sink-mute $(pactl list sinks short | cut -f 1) false
    pactl set-sink-volume $(pactl list sinks short | cut -f 1) +5%
  fi
elif [ "$1" == "down" ]; then
  if [ $(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | cut -d "%" -f 1) -gt 0 ]; then
    pactl set-sink-mute $(pactl list sinks short | cut -f 1) false 
    pactl set-sink-volume $(pactl list sinks short | cut -f 1) -5%
  fi
else
  usage
fi
