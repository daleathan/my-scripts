#!/bin/sh
#For a given set of files or directories, set the user and group ownership to
#$USER and set the permissions to 644 for ordinary files and 755 for
#directories and executables
#By Charles Bos

IFS=$'\n'

if [ ! "$1" ]; then
  echo "Supply at last one file or directory as an argument."
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
  echo "Usage:
  ownit.sh [FILES/DIRS...]"
  exit
fi

for x in "$@"; do
  if [ -f "$x" ] || [ -d "$x" ]; then
    for y in $(find "$x"); do
      chown $USER:$USER "$y"
      if [ -f "$y" ]; then
        if [ $(file -b "$y" | grep executable) ]; then
          chmod 755 "$y"
        else
          chmod 644 "$y"
        fi
      else
        chmod 755 "$y"
      fi
    done
  fi
done
