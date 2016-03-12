#!/bin/sh
#A script to increase, decrease or toggle the pulseaudio volume.

if [ "$1" == "toggle" ]; then
  pactl set-sink-mute $(pactl list sinks short | cut -f 1) toggle
elif [ "$1" == "up" ]; then
  CURRENT_VOLUME=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | cut -d "%" -f 1)
  if [ "$CURRENT_VOLUME" -lt 100 ]; then
    sh -c 'pactl set-sink-mute $(pactl list sinks short | cut -f 1) false; pactl set-sink-volume $(pactl list sinks short | cut -f 1) +5%'
  fi
elif [ "$1" == "down" ]; then
  CURRENT_VOLUME=$(amixer | grep "Front Left: Playback" | cut -d "[" -f 2 | cut -d "%" -f 1)
  if [ "$CURRENT_VOLUME" -gt 0 ]; then
    sh -c 'pactl set-sink-mute $(pactl list sinks short | cut -f 1) false; pactl set-sink-volume $(pactl list sinks short | cut -f 1) -5%'
  fi
fi
