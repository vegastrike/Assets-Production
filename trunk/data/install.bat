echo off
:L_start
SET SH=FALSE
SET SM=FALSE

cls
echo Vega Strike Install Utility
echo You have chosen to install Vega Strike, a program under the GPL.
echo For documentation about Vegastrike's license and source, visit
echo http://vegastrike.sourceforge.net

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
echo Installing Voodoo drivers
copy voodoo.config vegastrike.config







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
