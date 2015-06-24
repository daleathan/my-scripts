#!/bin/bash
#A wrapper script for batch compression of mp3 files to a lower bitrate

usage() {
  echo '''Usage:
  mp3compress.sh <dir> <bitrate> <encoding>
  Example: mp3compress.sh ~/Music 256 --abr
  Note: Consult the lame man page for more information

Options:
  -h, --help: Show this dialog
  * Bitrate: If this is not supplied, 192 kbps is assumed.
  * Encoding: Should be --cbr, --abr, --vbr-new, --vbr-old. If not supplied, cbr is assumed.'''
}

if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ ! -d "$1" ]; then
  usage
  exit 0
fi

if [[ "$2" =~ ^[0-9]+$ ]]; then
  BITRATE="$2"
else
  BITRATE=192
fi

if [ "$3" == "--abr" ] || [ "$3" == "--vbr-new" ] || [ "$3" == "--vbr-old" ]; then
  ENCODING="$3"
else
  ENCODING="--cbr"
fi

#Modify IFS to cope with spaces in filenames
IFS_ORIG="$IFS"
IFS=$'\n'

#Do conversion
if [ "$ENCODING" == "--abr" ]; then
  for x in $(find "$1" -type f -name "*.mp3"); do
    lame "$x" "$ENCODING" "$BITRATE"
    rm "$x"
    mv "${x}.mp3" "$x"
  done
else
  for x in $(find "$1" -type f -name "*.mp3"); do
    lame "$x" -b "$BITRATE" "$ENCODING"
    rm "$x"
    mv "${x}.mp3" "$x"
  done
fi

#Reset IFS
IFS="$IFS_ORIG"

echo $'\nComplete!'
