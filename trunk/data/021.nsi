; Kinnear's NSIS SuperPiMP VS Install Script

  Name "VegaStrike 0.2.9.2 Beta"	; caption in titlebar
  OutFile "vs_021_win32.exe"	; installer file to create
  Icon "vs.ico"		
  BrandingText " "		; removes default 'nullsoft' branding at
				; bottom of window
  CRCCheck on			; YAY!

;default install dir, and registry entry
  AutoCloseWindow true
  InstallDir "C:\Program Files\Vegastrike"
  InstallDirRegKey HKLM SOFTWARE\Vegastrike\0.2.9\ "Install_Dir"

  ComponentText "This will install Vega Strike 0.2.9.2 Beta onto your PC."
  DirText "Choose a directory to install in to:"
  EnabledBitmap "yes.bmp"
  DisabledBitmap "no.bmp"
  ShowInstDetails show

;first option section - install the program and write uninstall registry
;entries
  Section "Vega Strike files (Required)"
  SetOutPath $INSTDIR\Vegastrike-0.2.9
  File /r "C:\TEMP\ananyomous\data\*.*"
  WriteRegStr HKLM SOFTWARE\VegaStrike\0.2.9\ "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VegaStrike\0.2.9\" "DisplayName" "VegaStrike 0.2.9"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VegaStrike\0.2.9\" "UninstallString" '"$INSTDIR\Vegastrike-0.2.9\uninstall.exe"'
  WriteUninstaller "Vegastrike-0.2.9\uninstall.exe"
  SectionEnd

;second install option - adds the shortcuts to the start menu. optional.
  Section "Start Menu Shortcuts"
    CreateDirectory "$SMPROGRAMS\Vega Strike\0.2.9"
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Launcher.lnk" "$INSTDIR\Vegastrike-0.2.9\Launcher.exe" "" "$INSTDIR\Vegastrike-0.2.9\Launcher.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Manual.lnk" "$INSTDIR\Vegastrike-0.2.9\readme.url" "" "$INSTDIR\Vegastrike-0.2.9\readme.url" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Setup.lnk" "$INSTDIR\Vegastrike-0.2.9\setup.exe" "" "$INSTDIR\Vegastrike-0.2.9\setup.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Uninstall.lnk" "$INSTDIR\Vegastrike-0.2.9\uninstall.exe" "" "$INSTDIR\Vegastrike-0.2.9\uninstall.exe" 0
    CreateShortCut "$SMPROGRAMS\Vega Strike\0.2.9\Vega Strike Updater.lnk" "$INSTDIR\Vegastrike-0.2.9\AutoUpdate.bat" "" "$INSTDIR\Vegastrike-0.2.9\AutoUpdate.bat" 0
  SectionEnd

;Other Functions - this one is what to do once install is completed
Function .onInstSuccess
	ExecWait $INSTDIR/Vegastrike-0.2.9/OpenALwEAX.exe
      ExecWait $INSTDIR/Vegastrike-0.2.9/SETUP.EXE 
      MessageBox MB_YESNO "Installation Successful. View readme?" IDNO NoReadme
         ExecShell "open" $INSTDIR\Vegastrike-0.2.9\readme.txt
         NoReadme:
      MessageBox MB_YESNO "Would you like to veiw the story behind VegaStrike 0.2.9.2?" IDNO NoStory
         ExecShell "open" $INSTDIR\Vegastrike-0.2.9\CelesteStory.txt
         NoStory:
  FunctionEnd

 Function .onInstFailed
        MessageBox MB_OK "Installation Cancelled or Data corrupt."  
 FunctionEnd

;uninstaller stuff
UninstallText "This will delete the following directory and remove ALL of its contents, including your saved games. Hit the uninstall button to continue."

Section "Uninstall"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\vegastrike\0.2.9\"
  DeleteRegKey HKLM SOFTWARE\VegaStrike\0.2.9\
  Delete "$SMPROGRAMS\Vega Strike\0.2.9\*.*"
  RMDir /r "$SMPROGRAMS\Vega Strike\0.2.9\"
  RMDir /r "$INSTDIR"
SectionEnd

; note - i haven't made the uninstaller remove VegaStrike folder. This is
; because we don't want it to delete EVERY copy of VS.. just the one
; they're uninstalling. :)

; eof

