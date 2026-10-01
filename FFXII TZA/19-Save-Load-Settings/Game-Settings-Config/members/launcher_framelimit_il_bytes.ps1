# launcher_framelimit_il_bytes.ps1 (FABLE, Claude Opus 5.5, 2026-09-25; UQ-268 / DH-6)
# Prints the raw IL bytes of ConfigForm.LoadConfiguration 0x36-0x90 (the FrameLimit read and its branch) so the
# branch structure can be decoded by hand: output launcher-framelimit-il-bytes.txt beside this file.
$path = 'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA_GameSetting.exe'
$asm = [Reflection.Assembly]::LoadFile($path)
$flags = [Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
$t = $asm.GetType('GameSettings.ConfigForm')
foreach ($name in @('LoadConfiguration', 'GetIniString')) {
  foreach ($m in $t.GetMethods($flags) | Where-Object { $_.Name -eq $name }) {
    $il = $m.GetMethodBody().GetILAsByteArray()
    Write-Output ('=== ' + $name + ' len ' + $il.Length + ' params ' + (($m.GetParameters() | ForEach-Object { $_.ParameterType.Name + ' ' + $_.Name }) -join ', '))
    $lo = 0; $hi = $il.Length
    if ($name -eq 'LoadConfiguration') { $lo = 0x36; $hi = 0x90 }
    $line = ''
    for ($i = $lo; $i -lt $hi; $i++) { $line += ('{0:X2} ' -f $il[$i]) }
    Write-Output $line
  }
}
