#!/bin/sh
#For those of us who made our swap partitions a little bit too small ;)

fs=$(vmstat -s | grep 'free swap' | tr -s ' ' | cut -d ' ' -f 2)
um=$(vmstat -s | grep 'used memory' | tr -s ' ' | cut -d ' ' -f 2)

if [ $um -lt $fs ]; then
  echo 1
else
  echo 0
fi
