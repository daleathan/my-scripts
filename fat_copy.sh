#!/bin/sh
#A script to copy files and directories, automatically replacing illegal
#characters in FAT with underscores. Note that this does NOT work around
#FAT's case insensitivity. Use with care!
#By Charles Bos

usage() {
  echo "Usage:"
  echo "  fat_copy.sh src dest"
}

IFS=$'\n'

if [ ! $1 ] || [ ! $2 ] || ([ ! -d $1 ] && [ ! -f $1 ]) || [ ! -d $2 ]; then
  usage
  exit
fi

abs=$(realpath $1)
top=$(dirname $abs)

for x in $(find $abs); do
  if [ -f $x ]; then
    path=$(dirname $x)
  else
    path=$x
  fi
  dest=`realpath $(echo $2/${path/$top/} | sed 's@[<>:"\|?*]@_@g')`
  if [ ! -d $dest ]; then
    mkdir -p $dest
  fi
  if [ -f $x ]; then
    filename=$(basename $x | sed 's@[<>:"/\|?*]@_@g')
    cp $x $dest/$filename
  fi
done
