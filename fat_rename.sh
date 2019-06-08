#!/bin/sh
#A script to rename files and directories in place, automatically replacing 
#illegal characters in FAT with underscores. Note that this does NOT work around
#FAT's case insensitivity. Use with care!
#By Charles Bos

usage() {
  echo "Usage:"
  echo "  fat_copy.sh target"
}

IFS=$'\n'

if [ ! -d "$1" ] && [ ! -f "$1" ]; then
  usage
  exit 1
fi

abs=$(realpath $1)
top=$(dirname $abs)

for x in $(find $abs | sort -r); do
  item="$(echo $(basename $x) | sed 's@[<>:"\|?*]@_@g')"
  location="$(dirname $x)"
  dest="$(realpath $location/$item)"
  if [ ! "$x" == "$dest" ]; then
    echo "Renaming $(basename $x) to $(basename $dest)"
    mv "$x" "$dest"
  fi
done
