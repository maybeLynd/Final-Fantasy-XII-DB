$ErrorActionPreference = 'Stop'
$tokens=$null; $errors=$null
$source = Join-Path $PSScriptRoot 'capture.ps1'
$tree=[Management.Automation.Language.Parser]::ParseFile($source,[ref]$tokens,[ref]$errors)
if ($errors.Count) { throw 'Capture source parse failed' }
$defs=@($tree.FindAll({param($a) $a -is [Management.Automation.Language.FunctionDefinitionAst] -and $a.Name -in @('Hash-Text','Select-Profile')},$true))
if ($defs.Count -ne 2) { throw 'Expected exactly the two pure profile functions' }
foreach ($d in $defs) { . ([scriptblock]::Create($d.Extent.Text)) }
$fixture=@'
"users"
{
 "76561197960265729"
 {
  "AccountName" "controluser"
  "AutoLogin" "1"
 }
}
'@
$digest=Hash-Text 'controluser'
$p=Select-Profile $fixture 1 $digest
if ($p.record_count -ne 1 -or $p.selected.steam_id64 -cne '76561197960265729') { throw 'Modern profile without MostRecent rejected' }
$cases=[ordered]@{missing_MostRecent_supported=$true}
foreach ($case in @(
    @{name='empty_population';text='"users" {}';low=1;hash=$digest},
    @{name='wrong_active_id';text=$fixture;low=2;hash=$digest},
    @{name='wrong_account_name';text=$fixture;low=1;hash=(Hash-Text 'otheruser')},
    @{name='ambiguous_duplicate';text=($fixture+"`n"+$fixture);low=1;hash=$digest}
)) {
    $rejected=$false
    try { $null=Select-Profile $case.text $case.low $case.hash } catch { $rejected=$true }
    if (-not $rejected) { throw ('Invalid profile control accepted: '+$case.name) }
    $cases[$case.name+'_rejected']=$true
}
[ordered]@{status='CONTROLS_PASS';cases=$cases;capture_sha256=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant();control_sha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()} | ConvertTo-Json -Depth 5
