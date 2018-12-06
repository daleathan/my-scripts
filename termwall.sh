#!/bin/bash
#Start a number of equally sized terminals that cover the screen in a grid
#Note that the window manager needsto be using a MinOverlapPlacement algorithm
#For the terminal windows to be laid out in a grid. Also note that we use the
#screen dimensions of the primary display.
#By Charles Bos

usage() {
  echo "Usage:
  termwall.sh [ROWS] [COLUMNS] [OPTIONS]

  where ROWS and COLUMNS are the number of terminals per ROW and COLUMN
  respectively. If these are not supplied, they both default to 2.

Options:
  --help:        show this dialogue

  --term:        executable of the terminal to use. Use the format --term=term.

  --one-less:    assume that one terminal is already running and start one less
                 terminal accordingly, i.e. for a grid of 4, start 3 terms.

  --char-height: set height divisor to convert pixel dimensions into character 
                 dimensions used by terminals. Use format --char-height=x. 
                 Defaults to 16.

  --char-width:  set width divisor to convert pixel dimensions into character 
                 dimensions used by terminals. Use format --char-width=x. 
                 Defaults to 8.

  --offset:      number of char columns and rows to subtract from the terminal
                 height and width in order to ensure the terminals do not
                 overlap. Use format --offset=x. Defaults to 1.
                 
  --screen-res:  screen resolution of the display to start the terminals on.
                 Use format --screen-res=1366x768 for instance. If this is not
                 supplied we use xrandr to the get dimensions of the primary
                 display."
}

get_dimensions() {
  echo $(xrandr | grep '*\|primary' | grep -A1 primary | tail -n 1 | \
    tr -s ' ' | cut -d ' ' -f 2)
}

get_height() {
  local DIMS="$1"
  echo "$DIMS" | cut -d "x" -f 2
}

get_width() {
  local DIMS="$1"
  echo "$DIMS" | cut -d "x" -f 1
}

get_term_dimension() {
  local DIMENSION="$1"
  local NTERMS="$2"
  local CHARSIZE="$3"
  local OFFSET="$4"
  #We get the terminal height/width by diving the screen height/width by the
  #number of terminals in a row/col to get the pixel dimension. Then we divide
  #that by the character size to get the character dimension. Finally, we
  #subtract one from the result to ensure the terms fit with no overlaps
  echo $(expr $(expr $(expr $DIMENSION / $NTERMS) / $CHARSIZE) - $OFFSET)
}

run() {
  #Handle args
  local ROWSIZE="$1"
  if [ ! "$ROWSIZE" ] || [[ ! "$ROWSIZE" =~ ^[0-9]+$ ]]; then
    ROWSIZE=2
  fi
  local COLSIZE="$2"
  if [ ! "$COLSIZE" ] || [[ ! "$COLSIZE" =~ ^[0-9]+$ ]]; then
    COLSIZE=2
  fi
  local BIN="urxvt"
  local LIMIT=$(expr $ROWSIZE \* $COLSIZE)
  local CHARHEIGHT=16
  local CHARWIDTH=8
  local OFFSET=1

  for x in $@; do
    if [ "$x" == "-h" ] || [ "$x" == "--help" ]; then
      usage
      exit 0
    fi
    if [ "${x%=*}" == "--term" ]; then
      which "${x#*=}" > /dev/null 2>&1
      if [ $? == 0 ]; then
        BIN="${x#*=}"
      else
        echo "Terminal "${x#*=}" was not found!!! Exiting."
        exit 1
      fi
    fi
    if [ "$x" == "--one-less" ]; then
      LIMIT=$(expr $LIMIT - 1)
    fi
    if [ "${x%=*}" == "--char-height" ] && [[ "${x#*=}" =~ ^[0-9]+$ ]]; then
      CHARHEIGHT="${x#*=}"
    fi
    if [ "${x%=*}" == "--char-width" ] && [[ "${x#*=}" =~ ^[0-9]+$ ]]; then
      CHARWIDTH="${x#*=}"
    fi
    if [ "${x%=*}" == "--offset" ] && [[ "${x#*=}" =~ ^[0-9]+$ ]]; then
      OFFSET="${x#*=}"
    fi
    if [ "${x%=*}" == "--screen-res" ]; then
      if [ "${x#*=}" ]; then
        local DIMS="${x#*=}"
        local HEIGHT=$(get_height "$DIMS")
        local WIDTH=$(get_width "$DIMS")
        if [[ ! "$HEIGHT" =~ ^[0-9]+$ ]] || [[ ! "$WIDTH" =~ ^[0-9]+$ ]]; then
          echo "Invalid screen resolution!!!"
          exit 1
        fi
      fi
    fi
  done

  if [ ! "$DIMS" ]; then
    which xrandr > /dev/null 2>&1
    if [ ! $? == 0 ]; then
      echo "xrandr was not found!!! Exiting."
      exit 1
    fi
    local DIMS=$(get_dimensions)
    local WIDTH=$(get_width "$DIMS")
    local HEIGHT=$(get_height "$DIMS")
  fi

  #Get the height and width of each terminal
  local TWIDTH=$(get_term_dimension $WIDTH $ROWSIZE $CHARWIDTH $OFFSET)
  local THEIGHT=$(get_term_dimension $HEIGHT $COLSIZE $CHARHEIGHT $OFFSET)

  #Start terminals
  for x in $(seq 1 "$LIMIT"); do
    "$BIN" -geometry ${TWIDTH}x${THEIGHT} &
  done
}

run $@
