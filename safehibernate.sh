#!/bin/sh
#For those of us who made our swap partitions a little bit too small ;)

fs=$(vmstat -s | grep 'free swap' | tr -s ' ' | cut -d ' ' -f 2)
um=$(vmstat -s | grep 'used memory' | tr -s ' ' | cut -d ' ' -f 2)
deps_missing=0

if [ ! -f "/usr/bin/systemctl" ]; then
  echo Could not find /usr/bin/systemctl
  deps_missing=1
fi

if [ ! -f "/usr/bin/xmessage" ]; then
  echo Could not find /usr/bin/xmessage
  deps_missing=1
fi

if [ $deps_missing -eq 1 ]; then
  unset fs um deps_missing
  exit 1
fi

if [ $um -lt $fs ]; then
  unset fs um deps_missing
  /usr/bin/systemctl hibernate
else
  unset fs um deps_missing
  /usr/bin/xmessage -center 'Cannot hibernate. Too much memory is in use.' \
    -title Warning
fi
