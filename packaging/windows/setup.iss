#ifndef BundleDir
  #error BundleDir is required
#endif
#ifndef ReleaseId
  #error ReleaseId is required
#endif
#ifndef OutputDir
  #error OutputDir is required
#endif
[Setup]
AppId={{319D23EB-2BC0-46DF-8673-02317278062E}
AppName=KWS Desktop
AppVersion=0.1.0
AppVerName=KWS Desktop {#ReleaseId}
VersionInfoVersion=0.1.0.0
DefaultDirName={localappdata}\Programs\KWS\{#ReleaseId}
UsePreviousAppDir=no
DisableDirPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
MinVersion=10.0
AppMutex=Local\KWSDesktopRunning
SetupMutex=Local\KWSDesktopSetup
CloseApplications=no
RestartApplications=no
DisableProgramGroupPage=yes
OutputDir={#OutputDir}
OutputBaseFilename=KWS-Setup-{#ReleaseId}-x64
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\KWS.exe
WizardStyle=modern
#ifdef WmsSignedBuild
SignTool=WmsSign
SignedUninstaller=yes
#endif

[Files]
Source: "{#BundleDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userprograms}\KWS Desktop"; Filename: "{app}\KWS.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\KWS Desktop"; Filename: "{app}\KWS.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\KWS.exe"; Description: "Mở KWS Desktop"; Flags: postinstall nowait skipifsilent

; No UninstallDelete, cache reset, config overwrite, startup task or forced process kill.
; Old app versions and %LOCALAPPDATA%\kws-lan are intentionally preserved.
