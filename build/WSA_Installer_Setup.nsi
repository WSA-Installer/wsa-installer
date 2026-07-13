; ============================================================
;  WSA_Installer_Setup.nsi — NSIS Installer Script
;  Modified for MR CYBER with Social Buttons & Branding
; ============================================================

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"
!include "nsDialogs.nsh"
!include "FileFunc.nsh"
!include "StrFunc.nsh"
${StrLoc}

; ── App Info ─────────────────────────────────────────────────
!define APP_NAME        "WSA Installer"
!ifndef APP_VERSION
  !define APP_VERSION   "1.0"
!endif
!define APP_PUBLISHER   "MR CYBER"
!define APP_EXE         "WSA Installer.exe"
!define APP_ICON        "assets\icon.ico"
!define SOURCE_DIR      "dist\WSA Installer"
!define INSTALL_DIR     "$PROGRAMFILES64\WSA Installer"
!define UNINSTALL_KEY   "Software\Microsoft\Windows\CurrentVersion\Uninstall\WSAInstaller"
!define MUTEX_NAME      "WSAInstallerSetupMutex"

; ── Social Links ─────────────────────────────────────────────
!define YT_URL          "https://www.youtube.com/@AT_Tech_Zone"
!define COFFEE_URL      "https://buymeacoffee.com/mrcyberdev"

; ── Output ───────────────────────────────────────────────────
Name          "${APP_NAME}"
OutFile       "dist\WSA_Installer_Setup.exe"
InstallDir    "${INSTALL_DIR}"
InstallDirRegKey HKLM "${UNINSTALL_KEY}" "InstallLocation"
BrandingText "WSA Installer | Developed by AT Tech Zone & MR CYBER"
RequestExecutionLevel admin       ; Must run as admin
SetCompressor /SOLID lzma         ; Best compression
SilentInstall normal              ; Enable /S silent mode for auto-update

; ── MUI Settings ─────────────────────────────────────────────
!define MUI_ICON                   "${APP_ICON}"
!define MUI_UNICON                 "${APP_ICON}"
!define MUI_WELCOMEPAGE_TITLE      "Welcome to ${APP_NAME} Setup"
!define MUI_WELCOMEPAGE_TEXT       "This professional installer will set up Windows Subsystem for Android (WSA) with Google Play Store support on your Windows 11 PC.$\n$\nFeatures:$\n - One-click installation of WSA$\n - Full Google Play Store integration$\n - Optimized for performance and stability$\n - Developed by AT Tech Zone & MR CYBER$\n$\nClick Next to start the installation process."

; --- Branding Images ---
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "assets\header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\sidebar.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "assets\sidebar.bmp"

; --- Light Mode (Default) ---
; White background and standard text colors
!define MUI_BGCOLOR                "FFFFFF"
!define MUI_TEXTCOLOR              "000000"

!define MUI_FINISHPAGE_RUN         "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT    "Launch ${APP_NAME} now"
!define MUI_ABORTWARNING

; ── MUI Pages ────────────────────────────────────────────────
!insertmacro MUI_PAGE_WELCOME

; Maintenance / Repair Gate (Page 2)
Page custom MaintenancePage

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; Custom Socials Page (Page 3) - Moved to after installation
Page custom SocialsPage
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ── Version Info ─────────────────────────────────────────────
VIProductVersion "${APP_VERSION}.0.0"
VIAddVersionKey "ProductName"      "${APP_NAME}"
VIAddVersionKey "ProductVersion"   "${APP_VERSION}"
VIAddVersionKey "CompanyName"      "AT Tech Zone / MR CYBER"
VIAddVersionKey "FileDescription"  "WSA Installer Download Edition - Easy Android on Windows"
VIAddVersionKey "FileVersion"      "${APP_VERSION}"
VIAddVersionKey "LegalCopyright"   "© 2026 AT Tech Zone. All rights reserved."

; ── Maintenance Page ──────────────────────────────────────────
Var ButtonRepair
Var ButtonUninstall
Var MaintenanceDialog
Var RepairMode

Function MaintenancePage
    ; Skip in silent/repair mode (from Windows Settings)
    ${If} $RepairMode == 1
        Return
    ${EndIf}

    ; Check if app is installed
    ReadRegStr $R0 HKLM "${UNINSTALL_KEY}" "UninstallString"
    ${If} $R0 == ""
        Return ; Skip page if not installed
    ${EndIf}

    nsDialogs::Create 1018
    Pop $MaintenanceDialog
    ${If} $MaintenanceDialog == "error"
        Abort
    ${EndIf}

    ${NSD_CreateLabel} 0 0 100% 24u "${APP_NAME} is already installed.$\nSelect an action below to manage your installation:"
    Pop $0

    ${NSD_CreateButton} 25% 45u 50% 25u "Repair / Reinstall"
    Pop $ButtonRepair
    ${NSD_OnClick} $ButtonRepair OnClickRepair

    ${NSD_CreateButton} 25% 75u 50% 25u "Uninstall"
    Pop $ButtonUninstall
    ${NSD_OnClick} $ButtonUninstall OnClickUninstall

    nsDialogs::Show
FunctionEnd

Function OnClickRepair
    ; Pre-fill install directory from existing installation
    ReadRegStr $INSTDIR HKLM "${UNINSTALL_KEY}" "InstallLocation"
    ${If} $INSTDIR == ""
        StrCpy $INSTDIR "${INSTALL_DIR}"
    ${EndIf}
    ; Move to the next page (Directory)
    SendMessage $HWNDPARENT ${WM_COMMAND} 1 0
FunctionEnd

Function OnClickUninstall
    ; Perform silent uninstall and then exit
    ExecWait '"$INSTDIR\Uninstall.exe" /S _?=$INSTDIR'
    Quit
FunctionEnd

; ── Custom Socials Page ──────────────────────────────────────
Var Dialog
Var Label
Var ButtonYT
Var ButtonCoffee

Function SocialsPage
    ; Skip in silent/repair mode (from Windows Settings)
    ${If} $RepairMode == 1
        Return
    ${EndIf}

    nsDialogs::Create 1018
    Pop $Dialog

    ${If} $Dialog == "error"
        Abort
    ${EndIf}

    ${NSD_CreateLabel} 0 0 100% 24u "We hope you find this tool useful! $\nIf you'd like to support future development, consider subscribing or donating."
    Pop $Label

    ${NSD_CreateButton} 25% 45u 50% 25u "Subscribe on YouTube"
    Pop $ButtonYT
    ${NSD_OnClick} $ButtonYT OnClickYT

    ${NSD_CreateButton} 25% 75u 50% 25u "Buy Me a Coffee"
    Pop $ButtonCoffee
    ${NSD_OnClick} $ButtonCoffee OnClickCoffee

    nsDialogs::Show
FunctionEnd

Function OnClickYT
    ExecShell "open" "${YT_URL}"
FunctionEnd

Function OnClickCoffee
    ExecShell "open" "${COFFEE_URL}"
FunctionEnd

; ── Installer Functions ───────────────────────────────────────
Function .onInit
    ; Prevent multiple instances of setup
    System::Call 'kernel32::CreateMutex(p 0, i 1, t "${MUTEX_NAME}") p .r0 ?e'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONEXCLAMATION "Setup is already running."
        Abort
    ${EndIf}

    ${IfNot} ${AtLeastWin10}
        MessageBox MB_OK|MB_ICONSTOP "WSA Installer requires Windows 11 (22H2 or later).$\nSetup will now exit."
        Abort
    ${EndIf}

    ; Detect /repair flag (from Windows Settings "Modify" / "Repair" buttons)
    ${GetParameters} $R0
    ${StrLoc} $R0 $R0 "/repair" ">"
    ${If} $R0 != ""
        StrCpy $RepairMode 1
        SetSilent silent
    ${EndIf}
FunctionEnd

Function .onInstSuccess
    ExecShell "open" "${YT_URL}"
FunctionEnd

; ── Main Install Section ─────────────────────────────────────
Section "WSA Installer (Required)" SecMain
    SectionIn RO

    ; Detect repair vs fresh install
    ${If} $RepairMode == 1
        DetailPrint "Repairing ${APP_NAME} installation..."
    ${Else}
        DetailPrint "Installing ${APP_NAME}..."
    ${EndIf}

    ; ── Kill old server before install ───────────────────────────
    DetailPrint "Stopping old WSA Background Service..."
    ExecWait 'sc stop WSABackgroundService'
    Sleep 2000
    ExecWait 'sc delete WSABackgroundService'
    DetailPrint "Closing any running WSA Installer instance..."
    ExecWait 'taskkill /F /IM "${APP_EXE}" /T'
    Sleep 1000

    SetOutPath "$INSTDIR"
    SetOverwrite on

    ; Copy ALL files from PyInstaller output
    File /r "${SOURCE_DIR}\*.*"

    ; Save running installer inside install folder (for Windows Settings Repair)
    ; NSIS extracts to temp dir, so original EXE is NOT locked — safe to copy
    CreateDirectory "$INSTDIR\out_asset"
    CopyFiles "$EXEPATH" "$INSTDIR\out_asset\WSA_Installer_Setup.exe"

    ; Registry keys
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayName"          "${APP_NAME}"
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayVersion"       "${APP_VERSION}"
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "Publisher"            "${APP_PUBLISHER}"
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "InstallLocation"      "$INSTDIR"
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "UninstallString"      "$INSTDIR\Uninstall.exe"
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayIcon"          "$INSTDIR\${APP_EXE}"
    WriteRegDWORD HKLM "${UNINSTALL_KEY}" "NoModify"             0
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "ModifyPath"           '"$INSTDIR\out_asset\WSA_Installer_Setup.exe" /S /repair'
    WriteRegStr   HKLM "${UNINSTALL_KEY}" "Repair"               '"$INSTDIR\out_asset\WSA_Installer_Setup.exe" /S /repair'
    WriteRegDWORD HKLM "${UNINSTALL_KEY}" "EstimatedSize"        52000

    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Shortcuts
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortCut  "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"   "$INSTDIR\Uninstall.exe"

    ; Install and start Windows service
    DetailPrint "Installing Windows background service..."
    ExecWait 'sc create WSABackgroundService binPath= "$INSTDIR\${APP_EXE} --bg-service" start= auto'
    ExecWait 'sc failure WSABackgroundService reset=86400 actions=restart/10000/restart/15000/restart/30000'
    ExecWait 'sc description WSABackgroundService "Monitors Windows Subsystem for Android and manages Play Store patcher SDK. Auto-restarts on failure."'
    ExecWait 'sc start WSABackgroundService'
    DetailPrint "Service started."
SectionEnd

; ── Uninstaller ───────────────────────────────────────────────
Section "Uninstall"

    ; Stop and delete the Windows service FIRST (prevents SCM auto-restart)
    ExecWait 'sc stop WSABackgroundService'
    Sleep 2000
    ExecWait 'sc delete WSABackgroundService'
    Sleep 500

    ; Ensure the application is not running
    ExecWait 'taskkill /F /IM "${APP_EXE}" /T'
    
    ; Run Python uninstaller to clean WSA and related data
    ; We capture the exit code in $0. 0 = Success, 1 = Cancel/Error
    ExecWait '"$INSTDIR\${APP_EXE}" --uninstall' $0
    
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONINFORMATION "Uninstallation was cancelled or interrupted. The installation directory will not be removed."
        Abort
    ${EndIf}

    ; If we reach here, uninstallation was successful
    DetailPrint "WSA Uninstalled successfully. Removing remaining files..."
    
    ; Safety delay to release file handles
    Sleep 1000
    
    RMDir /r "$INSTDIR"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir  "$SMPROGRAMS\${APP_NAME}"
    DeleteRegKey HKLM "${UNINSTALL_KEY}"
SectionEnd

Function un.onUninstSuccess
    ExecShell "open" "${YT_URL}"
FunctionEnd
