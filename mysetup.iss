; -- Discord Ripper PRO Inno Setup Script --
; Created by GitHub Copilot

#define AppName "Discord Ripper PRO"
#define DirName "Discord Ripper PRO"
#define OutputFolder "output"

#define InputFolder "output\Discord Emoji Ripper PRO.dist"
#define LaunchExe "Discord Emoji Ripper PRO.exe"

[Setup]
AppName={#AppName}
AppVersion=1.0.0
AppPublisher=Gnogle
AppPublisherURL=https://gnogle.com
AppSupportURL=https://gnogle.com/support
AppUpdatesURL=https://gnogle.com/updates
DefaultDirName={commonpf}\{#DirName}
DefaultGroupName={#DirName}
DisableProgramGroupPage=no
OutputDir=.\{#OutputFolder}
OutputBaseFilename={#AppName} Setup
SetupIconFile=.\assets\icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
WizardImageFile=.\assets\logoBig.bmp
WizardSmallImageFile=.\assets\logoSmall.bmp
PrivilegesRequired=none

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#InputFolder}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#LaunchExe}"; WorkingDir: "{app}"
Name: "{userdesktop}\{#AppName}"; Filename: "{app}\{#LaunchExe}"; WorkingDir: "{app}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Dirs]
Name: "{app}\assets"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[CustomMessages]
WelcomeLabel1=Welcome to the {#AppName} Setup Wizard
