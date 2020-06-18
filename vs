#!/bin/bash
set -e

VEGASTRIKE_LOCAL_SHARE_DIR="/usr/local/share/vegastrike"
VEGASTRIKE_SHARE_DIR="/usr/share/vegastrike"

# This is a small wrapper that lets VegaStrike - Upon the Coldest Sea
# run from seemingly anywhere
if [ -d "${VEGASTRIKE_LOCAL_SHARE_DIR}" ]; then 
    vegastrike -d"${VEGASTRIKE_LOCAL_SHARE_DIR}"
elif [ -d "${VEGASTRIKE_SHARE_DIR}" ]; then
    vegastrike -d"${VEGASTRIKE_SHARE_DIR}"
else
    echo "Unknown Game Asset Data Location."
    echo "Do you have the game assets installed?"
    exit 1
fi
