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

for x in $(find $1 -type f); do
  path=$(dirname $x)
  dest=$(echo $2/$top/${path/*$top//} | sed 's@[<>:"\|?*]@_@g')
  if [ ! -d $dest ]; then
    mkdir -p $dest
  fi
  filename=$(basename $x | sed 's@[<>:"/\|?*]@_@g')
  cp $x $dest/$filename
done

IFS=$IFS_ORIG
