#define MyAppName "XTRAVON ONE"
#define MyAppVersion "1.0.2"
#define MyAppPublisher "QORA SYSTEMS - Alianza con MSL Marine Surveyors and Logistics Group"
#define MyAppExeName "XTRAVON ONE.exe"
#define MySourceDir "..\dist\XTRAVON ONE"

[Setup]
AppId={{6E678D84-4C3C-4D6E-8A64-7A8C0D1E0001}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName}
UninstallDisplayName={#MyAppName}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://qora-systems.com
AppSupportURL=https://qora-systems.com
AppUpdatesURL=https://qora-systems.com
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=XTRAVON_ONE_Setup_{#MyAppVersion}
SetupIconFile=xtravon_one.ico
LicenseFile=EULA_ES.txt
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
SetupLogging=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
CloseApplications=yes
CloseApplicationsFilter={#MyAppExeName}
RestartApplications=no
SetupMutex=XTRAVON_ONE_INSTALLER_MUTEX
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=XTRAVON ONE Grain Control
VersionInfoProductName={#MyAppName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"
Type: files; Name: "{app}\{#MyAppExeName}"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName}"; WorkingDir: "{app}"; Flags: nowait skipifdoesntexist
