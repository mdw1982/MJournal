$TargetFile = "$env:UserProfile\MJournal_Win64\MJournal.exe"
$ShortcutFile = "$env:UserProfile\Desktop\MJournal.lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutFile)
$Shortcut.TargetPath = $TargetFile
$Shortcut.WorkingDirectory = "$env:UserProfile\MJournal_Win64"
$shortcut.IconLocation = "$env:UserProfile\MJournal_Win64\images\MjournalIcon_80x80.ico"
$Shortcut.Save()

