#!/bin/sh
#cvs -z9 -d:pserver:anonymous@cvs.vegastrike.sourceforge.net:/cvsroot/vegastrike checkout -rvegastrike_0_2_9 vegastrike
#cvs -z9 -d:pserver:anonymous@cvs.vegastrike.sourceforge.net:/cvsroot/vegastrike checkout -rvegastrike_0_2_9 data
cd vegastrike
autoconf
automake
./configure 
gmake 
cd saveinterface
sh build.sh
cd ../../data
mkdir ~/.vegastrike
echo "default" > ~/.vegastrike/save.txt
mv ../vegastrike/src/vegastrike . 
mv ../vegastrike/saveinterface/launcher .
echo "install complete.  type ./launcher to run (if build of launcher failed check vegastrike/saveinterface/build.sh  it may not be correct)"
