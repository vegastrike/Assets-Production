#!/bin/bash
# This is a small wrapper that lets VegaStrike - Upon the Coldest Sea
# run from seemingly anywhere
set -e

VEGASTRIKE_LOCAL_SHARE_DIR="/usr/local/share/vegastrike"
VEGASTRIKE_SHARE_DIR="/usr/share/vegastrike"

#Let's keep a log of the console
touch ~/.vegastrike/console.log
mv -vf ~/.vegastrike/console.log ~/.vegastrike/console.bak 

if [ -d "${VEGASTRIKE_LOCAL_SHARE_DIR}" ]; then 
    vegastrike -d"${VEGASTRIKE_LOCAL_SHARE_DIR}" "$1" | tee ~/.vegastrike/console.log
elif [ -d "${VEGASTRIKE_SHARE_DIR}" ]; then
    vegastrike -d"${VEGASTRIKE_SHARE_DIR}" "$1" | tee ~/.vegastrike/console.log
else
    echo "Unknown Game Asset Data Location."
    echo "Do you have the game assets installed?"
    exit 1
fi
