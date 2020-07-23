#!/bin/bash
# This is a small wrapper that lets VegaStrike - Upon the Coldest Sea
# run from seemingly anywhere
set -e

VEGASTRIKE_LOCAL_SHARE_DIR="/usr/local/share/vegastrike"
VEGASTRIKE_SHARE_DIR="/usr/share/vegastrike"

#Let's keep a log of the console
if [ -f  ~/.vegastrike/console.log ]; then 
  mv -f ~/.vegastrike/console.log ~/.vegastrike/console.bak
fi
if [ -f ~/.vegastrike/console_err.log ]; then 
  mv -f ~/.vegastrike/console_err.log ~/.vegastrike/console_err.bak
fi

echo "Starting Vega Strike, console output will be saved in ~/.vegastrike/console.log, errors in ~/.vegastrike/console_err.log"
echo ""

if [ -d "${VEGASTRIKE_LOCAL_SHARE_DIR}" ]; then 
    vegastrike -d"${VEGASTRIKE_LOCAL_SHARE_DIR}" "$1" --debug=3 >~/.vegastrike/console.log 2>~/.vegastrike/console_err.log
elif [ -d "${VEGASTRIKE_SHARE_DIR}" ]; then
    vegastrike -d"${VEGASTRIKE_SHARE_DIR}" "$1" --debug=3 >~/.vegastrike/console.log 2>~/.vegastrike/console_err.log
else
    echo "Unknown Game Asset Data Location."
    echo "Do you have the game assets installed?"
    exit 1
fi
