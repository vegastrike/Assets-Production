#!/bin/sh
ARG=$1
SETUPARG=${ARG:="nosetup"}
CURPWD=$PWD

VERSION=`head -1 $CURPWD/../Version.txt`
mkdir -p $HOME/$VERSION
cd $HOME/$VERSION
if [ \! -e ~/$VERSION/setup.config ]; then
  cp $CURPWD/../setup.config .
fi
if [ \! -e ~/$VERSION/vegastrike.config ]; then
  cp $CURPWD/../vegastrike.config .
   $CURPWD/setup
fi
if [ $SETUPARG = "setup" ] || [ $SETUPARG = "--setup" ]; then
   $CURPWD/setup
else
  cd $CURPWD
  ./vegastrike
fi
