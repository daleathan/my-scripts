#!/bin/sh
#Script to check how many mp3 files' year tags lie within a given range

usage() {
  echo "Usage:"
  echo "  mp3-range.sh lower-year upper-year directory"
}

IFS=$'\n'

if [ ! $1 ] || [ ! $2 ] || [ ! $3 ] || [ ! -d $3 ]; then
  usage
  exit 1
fi

if [[ ! $1 =~ ^[0-9]+$ ]] || [[ ! $2 =~ ^[0-9]+$ ]]; then
  usage
  exit 1
fi

if [ $1 -ge $2 ]; then
  usage
  exit 1
fi

count=0
rCount=0

for x in $(find $3 -type f -name "*.mp3"); do
  ((count+=1))
  year=$(id3info $x | grep TYER | cut -d " " -f 4)
  if [ $year -ge $1 ] && [ $year -le $2 ]; then
    ((rCount+=1))
  fi
done

echo "$rCount out of $count tracks are tagged in the range $1 - $2"
