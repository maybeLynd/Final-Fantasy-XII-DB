<#
.SYNOPSIS
  Enrich + apply a CodeDomain batch under the full exact-current fence.
.DESCRIPTION
  Input is a 4-column TSV you author:
        entry <TAB> domain <TAB> unused <TAB> evidence
  (header row required; "unused" is a legacy column, put the batch tag or RECOVERY)

  This wrapper:
    1. snapshots the pre-state (FAS2)
    2. runs EnrichCurrentBodyManifest  -> computes the ADDRESS-SALTED body hash itself
    3. runs ApplyCurrentBodyCodeDomainBatch with an EXACT expected count
    4. snapshots the post-state and runs diff_fas2.py
    5. FAILS if immutable drift != 0, functions added/removed != 0, tag removals != 0,
       or any field other than comment/tags changed

  Never hand-author the 7-column manifest. The prose hashes in the handoff are
  PLAIN-BODY-BYTE hashes; the apply gate wants ADDRESS-SALTED. Step 2 is the only
  correct producer.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$ProjectDir,
  [string]$ProjectName = 'GFZ_PARENT',
  [string]$ProgramName,
  [Parameter(Mandatory)][string]$PreEnrichTsv,
  [Parameter(Mandatory)][string]$BatchId,
  [Parameter(Mandatory)][int]$ExpectedCount,
  [Parameter(Mandatory)][string]$Summary,
  [string]$PreSnapshot,
  [string]$OutDir,
  [switch]$AllowExistingTag
)
. "$PSScriptRoot\GfzEnv.ps1"
if (-not $ProgramName) {
  $ProgramName = Get-GfzProgramName -ProjectDir $ProjectDir -ProjectName $ProjectName
  Write-Host "[gfz] program: $ProgramName" -ForegroundColor DarkGray
}
if (-not $OutDir) { $OutDir = Join-Path $GfzWork ("batch_$BatchId") }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$manifest = Join-Path $OutDir 'manifest.tsv'
$preFas   = if ($PreSnapshot) { $PreSnapshot } else { Join-Path $OutDir 'pre.fas2' }
$postFas  = Join-Path $OutDir 'post.fas2'
$diffJson = Join-Path $OutDir 'diff.json'

function Invoke-Step { param([string]$Script,[string[]]$A)
  & "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Process -ProjectDir $ProjectDir -ProjectName $ProjectName `
      -ProgramName $ProgramName -Script $Script -ScriptArgs $A
}

# --- sanity on the authored pre-enrichment rows ---
$rows = Get-Content -LiteralPath $PreEnrichTsv | Where-Object { $_ -ne '' }
if ($rows.Count - 1 -ne $ExpectedCount) {
  throw "pre-enrich TSV has $($rows.Count - 1) data rows but -ExpectedCount is $ExpectedCount"
}

if (-not $PreSnapshot) {
  Write-Host "[gfz] 1/5 pre-mutation snapshot" -ForegroundColor Cyan
  Invoke-Step 'GFZFunctionAnnotationSnapshotV2.java' @($preFas) | Out-Null
}
Write-Host "  pre  snapshot $(Get-GfzSha256 -Path $preFas)"

Write-Host "[gfz] 2/5 exact-current enrichment" -ForegroundColor Cyan
$eo = Invoke-Step 'EnrichCurrentBodyManifest.java' @($PreEnrichTsv, $manifest)
if ($eo -notmatch 'ENRICH_CURRENT_BODY_MANIFEST_PASS') { throw 'enrichment did not report PASS' }
Write-Host ($eo -split "`n" | Where-Object { $_ -match 'ENRICH_CURRENT_BODY_MANIFEST_PASS' } | Select-Object -First 1)

Write-Host "[gfz] 3/5 apply (exact expected count = $ExpectedCount)" -ForegroundColor Cyan
$applyScript = if ($AllowExistingTag) { 'ApplyCurrentBodyCodeDomainBatchAllowExisting.java' } else { 'ApplyCurrentBodyCodeDomainBatch.java' }
$ao = Invoke-Step $applyScript @($manifest, $BatchId, "$ExpectedCount", $Summary)
# The AllowExisting variant reports ..._ALLOW_EXISTING_MUTATION_PASS; accept either marker.
if ($ao -notmatch 'CURRENT_BODY(_ALLOW_EXISTING)?_MUTATION_PASS') { throw 'apply did not report MUTATION_PASS' }
Write-Host ($ao -split "`n" | Where-Object { $_ -match 'CURRENT_BODY(_ALLOW_EXISTING)?_MUTATION_PASS' } | Select-Object -First 1)

Write-Host "[gfz] 4/5 post-mutation whole-project snapshot" -ForegroundColor Cyan
Invoke-Step 'GFZFunctionAnnotationSnapshotV2.java' @($postFas) | Out-Null
Write-Host "  post snapshot $(Get-GfzSha256 -Path $postFas)"

Write-Host "[gfz] 5/5 whole-project diff" -ForegroundColor Cyan
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) { throw 'python not found - needed for diff_fas2.py' }
& $py.Source (Join-Path $GfzAnalysis 'diff_fas2.py') $preFas $postFas $diffJson | Out-Null
$d = Get-Content -Raw -LiteralPath $diffJson | ConvertFrom-Json

$bad = @()
if ($d.from_functions -ne $d.to_functions)    { $bad += "function count changed $($d.from_functions) -> $($d.to_functions)" }
if ($d.added_functions.Count   -ne 0)         { $bad += "functions added: $($d.added_functions.Count)" }
if ($d.removed_functions.Count -ne 0)         { $bad += "functions removed: $($d.removed_functions.Count)" }
if ($d.immutable_changed_count -ne 0)         { $bad += "IMMUTABLE DRIFT: $($d.immutable_changed_count)" }
if ($d.changed_common_functions -ne $ExpectedCount) { $bad += "changed functions $($d.changed_common_functions) expected $ExpectedCount" }
$removedTags = @($d.tag_removals.PSObject.Properties)
if ($removedTags.Count -ne 0)                 { $bad += "tag removals: $($removedTags.Count)" }
foreach ($f in $d.field_counts.PSObject.Properties) {
  if ($f.Name -notin @('comment','tags')) { $bad += "unexpected field changed: $($f.Name) x$($f.Value)" }
  elseif ([int]$f.Value -ne $ExpectedCount) { $bad += "$($f.Name)=$($f.Value) expected $ExpectedCount" }
}

Write-Host ""
Write-Host "  changed=$($d.changed_common_functions)  immutable_drift=$($d.immutable_changed_count)  added/removed=$($d.added_functions.Count)/$($d.removed_functions.Count)"
Write-Host "  changed_entries_fields_sha256=$($d.changed_entries_fields_sha256)"
if ($bad.Count -gt 0) {
  Write-Host "[gfz] DIFF GATE FAILED" -ForegroundColor Red
  $bad | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  throw 'whole-project diff rejected the mutation'
}
Write-Host "[gfz] DIFF CLEAN - comment/tags only, immutable drift 0" -ForegroundColor Green
Write-Host "[gfz] NOT YET PERSISTED. Close the project, then run Pack-GfzCheckpoint.ps1 in a SEPARATE invocation."
[pscustomobject]@{ Manifest=$manifest; Pre=$preFas; Post=$postFas; Diff=$diffJson; ChangedFieldsSha=$d.changed_entries_fields_sha256 }
