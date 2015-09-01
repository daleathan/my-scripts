#!/bin/sh
#Toggle the xautolock setting and Xfpm presentation mode

QUERY="xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode"
PRES_MODE=$(eval $QUERY)
if [ $PRES_MODE = "false" ]; then
  xautolock -disable
  eval "$QUERY -s true"
else
  xautolock -enable
  eval "$QUERY -s false"
fi