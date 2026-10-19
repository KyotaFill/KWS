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
AppId={{187F2EBD-B8E7-4317-B4C5-443BE58ECB5B}
AppName=KWS MySQL Local
AppVersion=0.1.0
AppVerName=KWS MySQL Local {#ReleaseId}
DefaultDirName={localappdata}\Programs\KWSLocal\{#ReleaseId}
UsePreviousAppDir=no
DisableDirPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
MinVersion=10.0
AppMutex=Local\KWSDesktopRunning,Local\KWSLocalRunning
CloseApplications=no
RestartApplications=no
DisableProgramGroupPage=yes
OutputDir={#OutputDir}
OutputBaseFilename=KWS-MySQL-Setup-{#ReleaseId}-x64
Compression=lzma2
SolidCompression=yes
UninstallDisplayIcon={app}\server\KWSLocal.exe
WizardStyle=modern
SetupIconFile=..\..\apps\desktop\assets\kws-app-icon.ico
#ifdef WmsSignedBuild
SignTool=WmsSign
SignedUninstaller=yes
#endif
[Files]
Source: "{#BundleDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{userprograms}\KWS MySQL Local"; Filename: "{app}\server\KWSLocal.exe"; WorkingDir: "{app}\server"
Name: "{userdesktop}\KWS MySQL Local"; Filename: "{app}\server\KWSLocal.exe"; WorkingDir: "{app}\server"
[Run]
Filename: "{app}\server\KWSLocal.exe"; Description: "Mở KWS và kiểm tra MySQL"; Flags: postinstall nowait skipifsilent
; Server data and existing LAN client configuration are outside {app}; never removed.
