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

abs=$(realpath $1)
path_to_top=$(dirname $abs)
length=$(expr ${#path_to_top} + 1)
top=${abs:$length}

for x in $(find $1); do
  if [ -f $x ]; then
    path=$(dirname $x)
  else
    path=$x
  fi
  dest=$(echo $2/$top/${path/*$top//} | sed 's@[<>:"\|?*]@_@g')
  if [ ! -d $dest ]; then
    mkdir -p $dest
  fi
  if [ -f $x ]; then
    filename=$(basename $x | sed 's@[<>:"/\|?*]@_@g')
    cp $x $dest/$filename
  fi
done

IFS=$IFS_ORIG
