#!/bin/sh
#For those of us who made our swap partitions a little bit too small ;)

usage() {
  echo "Run 'systemctl hibernate' only if the amount of memory in usage does not exceed the amount of available swap space.

Usage:
  safehibernate.sh [OPTIONS]
  -h: show this dialog
  -c: only check if hibernation is possible. Return 1 if so or else return 0"
}

if [ "$1" = "-h" ]; then
  usage
  exit 0
fi

fs=$(vmstat -s | grep 'free swap' | tr -s ' ' | cut -d ' ' -f 2)
um=$(vmstat -s | grep 'used memory' | tr -s ' ' | cut -d ' ' -f 2)
check_only=$(for x in "$@"; do if [ "$x" = "-c" ]; then echo 1; fi; done)

if [ $um -lt $fs ]; then
  if [ "$check_only" = 1 ]; then 
    echo 1
  else 
    systemctl hibernate
  fi
else
  if [ "$check_only" = 1 ]; then 
    echo 0
  else
    xmessage -center 'Cannot hibernate. Too much memory is in use.'
  fi
fi
