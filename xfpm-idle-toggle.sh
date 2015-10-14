#!/bin/sh
#Toggle Xfpm presentation mode

QUERY="xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode"
PRES_MODE=$(eval $QUERY)
if [ $PRES_MODE = "false" ]; then
  eval "$QUERY -s true"
  notify-send "Presentation mode: ON" -i xfpm-ac-adapter
else
  eval "$QUERY -s false"
  notify-send "Presentation mode: OFF" -i xfpm-ac-adapter
fi