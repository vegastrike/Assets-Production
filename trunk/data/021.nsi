; Kinnear's NSIS SuperPiMP VS Install Script

  Name "VegaStrike 0.2.9 Beta"	; caption in titlebar
  OutFile "vs_021_win32.exe"	; installer file to create
  Icon "vs.ico"		
  BrandingText " "		; removes default 'nullsoft' branding at
				; bottom of window
  CRCCheck on			; YAY!

;default install dir, and registry entry
  AutoCloseWindow true
  InstallDir "C:\Program Files\VegaStrike\0.2.9\"
  InstallDirRegKey HKLM SOFTWARE\Vegastrike\0.2.9\ "Install_Dir"

  ComponentText "This will install Vega Strike 0.2.9 Beta onto your PC."
  DirText "Choose a directory to install in to:"
  EnabledBitmap "yes.bmp"
  DisabledBitmap "no.bmp"
  ShowInstDetails show

;first option section - install the program and write uninstall registry
;entries
  Section "Vega Strike files (Required)"
  SetOutPath $INSTDIR
  File /r "C:\temp\data\newdir\*.*"
  WriteRegStr HKLM SOFTWARE\VegaStrike\0.2.9\ "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VegaStrike\0.2.9\" "DisplayName" "VegaStrike 0.2.9"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VegaStrike\0.2.9\" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteUninstaller "uninstall.exe"
  SectionEnd

;second install option - adds the shortcuts to the start menu. optional.
  Section "Start Menu Shortcuts"
    CreateDirectory "$SMPROGRAMS\Vega Strike\0.2.9"
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Launcher.lnk" "$INSTDIR\Launcher.exe" "" "$INSTDIR\Launcher.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Setup.lnk" "$INSTDIR\setup.exe" "" "$INSTDIR\setup.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Auto Updater.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\AutoUpdate.bat" 0
  SectionEnd

;Other Functions - this one is what to do once install is completed
Function .onInstSuccess
	ExecWait $INSTDIR/OpenALwEAX.exe
      ExecWait $INSTDIR/SETUP.EXE 
      MessageBox MB_YESNO "Installation Successful. View readme?" IDNO NoReadme
         ExecShell "open" $INSTDIR\README
         NoReadme:
      MessageBox MB_YESNO "Would you like to veiw the story behind VegaStrike 0.2.9?" IDNO NoStory
         ExecShell "open" $INSTDIR\CelesteStory.txt
         NoStory:
  FunctionEnd

 Function .onInstFailed
        MessageBox MB_OK "Installation Cancelled or Data corrupt."  
 FunctionEnd

;uninstaller stuff
UninstallText "This will uninstall Vega Strike 0.2.9 and remove all saved games. Hit next to continue."

Section "Uninstall"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\vegastrike\0.2.9\"
  DeleteRegKey HKLM SOFTWARE\VegaStrike\0.2.9\
  Delete "$SMPROGRAMS\Vega Strike\0.2.9\*.*"
  RMDir "$SMPROGRAMS\Vega Strike\0.2.9\"
  RMDir /r "$INSTDIR"
SectionEnd

; note - i haven't made the uninstaller remove VegaStrike folder. This is
; because we don't want it to delete EVERY copy of VS.. just the one
; they're uninstalling. :)

; eof

