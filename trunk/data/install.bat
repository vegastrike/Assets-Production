@echo off
:L_start
SET SH=FALSE
SET SM=FALSE

cls
echo Vega Strike Install Utility
echo You have chosen to install Vega Strike, a program under the GPL.
echo For documentation about Vegastrike's license and source, visit
echo http://vegastrike.sourceforge.net
echo Information about key bindings and gameplay is contained in README
choice Would you like to read the readme now
if errorlevel==2 goto FICTION
more README
:FICTION
choice Would you like to view the game fiction?
if errorlevel==2 goto GF3
more FICTION

:GF3
choice Do you have a GeForce 3 
if errorlevel==2 goto GeForce2
copy geforce3.config vegastrike.config
goto end

:GeForce2
choice Do you have a GeForce or ATI Radeon
if errorlevel==2 goto TNT
copy geforce2.config vegastrike.config
goto end

:TNT
choice Do you have a TNT or other not 3dfx card without T&L
if errorlevel==2 goto voodoo
copy tnt.config vegastrike.config
goto end



:voodoo
choice Do you have a 3dfx card
if errorlevel==2 goto software
echo Installing Voodoo drivers
copy voodoo.config vegastrike.config

:software
echo Installing software drivers
copy software.config vegastrike.config





:end
echo Determining system type
choice Do you have a 800 MHZ machine or better? 
if errorlevel==2 goto PIII
copy vs1000 vegastrike.exe
goto eend

:PIII
choice Do you have a 450 MHz machine or better
if errorlevel==2 goto PII
copy vs550 vegastrike.exe
goto eend




:PII
echo Installing Pentium II/Celeron Drivers
copy vs200 vegastrike.exe
:eend
echo Thank you for installing Vega Strike!
echo You may begin playing by running vegastrike.exe 
echo You can run the provided VegastrikeMissionX.bat files to run missions
echo Edit them if you wish to change missions.
echo vegastrike.exe test2.mission > VegastrikeMission2.bat
echo vegastrike.exe test3.mission > VegastrikeMission3.bat
echo vegastrike.exe test4.mission > VegastrikeMission4.bat
echo vegastrike.exe test5.mission > VegastrikeMission5.bat
echo Install successful!
echo E-mail comments to vegastrike-users@lists.sourceforge.net
