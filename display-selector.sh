#!/bin/sh
#A simple zenity GUI for selecting the output screen
#We use xrandr to select turn on/off the screens
#By Charles Bos

OPTION=$(zenity --title "Display Selector" \
  --list --text "Select the output display(s)." --radiolist \
  --column "Select" \
  --column "Display(s)" \
  TRUE "Laptop only" \
  FALSE "Television only" \
  FALSE "Laptop and television")

if [ "$OPTION" = "Television only" ]; then 
  xrandr --output HDMI1 --auto --output LVDS1 --off
elif [ "$OPTION" = "Laptop and television" ]; then
  xrandr --output HDMI1 --auto --output LVDS1 --auto
else
  xrandr --output HDMI1 --off --output LVDS1 --auto
fi

unset OPTION
