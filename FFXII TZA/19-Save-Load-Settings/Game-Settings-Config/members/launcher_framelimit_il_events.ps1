# launcher_framelimit_il_events.ps1 (FABLE, Claude Opus 5.5, 2026-09-25; UQ-268 / DH-6)
# Loads the shipped settings launcher FFXII_TZA_GameSetting.exe by reflection (no code runs) and prints, for every
# method whose IL names FrameLimit, its ldstr / ldfld / stfld / call / callvirt / ldc.i4 operands in IL order.
# Output: launcher-framelimit-il-events.txt beside this file.
$path = 'D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA_GameSetting.exe'
$asm = [Reflection.Assembly]::LoadFile($path)
$flags = [Reflection.BindingFlags]'Public,NonPublic,Instance,Static,DeclaredOnly'
try { $types = $asm.GetTypes() } catch [Reflection.ReflectionTypeLoadException] { $types = $_.Exception.Types | Where-Object { $_ } }
# one-byte opcodes that carry a 4-byte token or int32 operand we want, plus a crude length table for skipping
foreach ($t in $types) {
  $members = @()
  try { $members += $t.GetMethods($flags) } catch {}
  try { $members += $t.GetConstructors($flags) } catch {}
  foreach ($m in $members) {
    $body = $null
    try { $body = $m.GetMethodBody() } catch {}
    if (-not $body) { continue }
    $il = $body.GetILAsByteArray()
    $events = New-Object System.Collections.ArrayList
    $touch = $false
    for ($i = 0; $i -lt $il.Length - 4; $i++) {
      $op = $il[$i]
      if ($op -eq 0x72 -or $op -eq 0x7D -or $op -eq 0x7B -or $op -eq 0x28 -or $op -eq 0x6F -or $op -eq 0x20) {
        $tok = [BitConverter]::ToInt32($il, $i + 1)
        $txt = $null
        try {
          switch ($op) {
            0x72 { $txt = 'ldstr "' + $m.Module.ResolveString($tok) + '"' }
            0x7D { $txt = 'stfld ' + $m.Module.ResolveField($tok).Name }
            0x7B { $txt = 'ldfld ' + $m.Module.ResolveField($tok).Name }
            0x28 { $txt = 'call ' + $m.Module.ResolveMethod($tok).Name }
            0x6F { $txt = 'callvirt ' + $m.Module.ResolveMethod($tok).Name }
            0x20 { $txt = 'ldc.i4 ' + $tok }
          }
        } catch {}
        if ($txt) {
          [void]$events.Add(('{0:X4} {1}' -f $i, $txt))
          if ($txt -match 'FrameLimit') { $touch = $true }
        }
      }
    }
    if ($touch) {
      Write-Output ('=== ' + $t.FullName + '::' + $m.Name)
      $events | ForEach-Object { Write-Output ('   ' + $_) }
    }
  }
}
