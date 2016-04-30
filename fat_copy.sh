#!/bin/sh
#A script to copy directories and their contents, automatically replacing
#FAT illegal characters with underscores

usage() {
  echo "Usage:"
  echo "  fat_copy.sh src_dir dest_dir"
  IFS=$IFS_ORIG
}

IFS_ORIG=$IFS
IFS=$'\n'

if [ ! $1 ] || [ ! $2 ] || [ ! -d $1 ] || [ ! -d $2 ]; then
  usage
  exit
fi

cd $1
abs=$(dirname $PWD)
length=$(expr ${#abs} + 1)
top=${1:$length}

for x in $(find . -type f); do
  dest=$(echo $2/$top/$(dirname $x) | sed 's@[<>:"\|?*]@_@g')
  if [ ! -d $dest ]; then
    mkdir -p $dest
  fi
  filename=$(basename $x | sed 's@[<>:"/\|?*]@_@g')
  cp $x $dest/$filename
done

IFS=$IFS_ORIG
