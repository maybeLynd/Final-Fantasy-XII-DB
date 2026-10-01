<#
.SYNOPSIS
  Regenerate the complete evidence set for the CURRENT unresolved residual.
.DESCRIPTION
  Runs every read-only scan script. Must be re-run after every mutation and every
  fresh reopen - the GFZ contract forbids reusing a stale residual/evidence set.

  NOTE ON HASHES (this is the trap that aborts mutations):
    STRUCTURE.tsv  body_sha256 = ADDRESS-SALTED  (range min/max BE64, then bytes)
                                 -> this is what the APPLY GATE compares
    MECHANISM_FEATURES.tsv sha256 = PLAIN BODY BYTES
                                 -> this is what the handoff prose quotes
  Never copy a prose hash into a manifest. Let Apply-GfzBatch build it.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$ProjectDir,
  [string]$ProjectName = 'GFZ_PARENT',
  [string]$ProgramName,
  [string]$OutDir,
  [int]$MaxInsns = 4000
)
. "$PSScriptRoot\GfzEnv.ps1"
if (-not $ProgramName) {
  $ProgramName = Get-GfzProgramName -ProjectDir $ProjectDir -ProjectName $ProjectName
  Write-Host "[gfz] program: $ProgramName" -ForegroundColor DarkGray
}
if (-not $OutDir) { $OutDir = Join-Path $GfzWork ('residual_' + (Get-Date -Format 'yyyyMMdd_HHmmss')) }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Invoke-Step { param([string]$Script,[string[]]$A)
  & "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Process -ProjectDir $ProjectDir -ProjectName $ProjectName `
      -ProgramName $ProgramName -Script $Script -ScriptArgs $A
}

$steps = @(
  @{ n='structure';       s='DumpUnresolvedStructure.java';              a=@((Join-Path $OutDir 'STRUCTURE.tsv')) }
  @{ n='mechanism';       s='DumpUnresolvedMechanismFeatures.java';      a=@((Join-Path $OutDir 'MECHANISM_FEATURES.tsv'), "$MaxInsns") }
  @{ n='neighborhoods';   s='DumpUnresolvedNeighborhoodDomains.java';    a=@((Join-Path $OutDir 'NEIGHBORHOODS.tsv')) }
  @{ n='dataref contexts';s='DumpUnresolvedIncomingDataRefContexts.java';a=@((Join-Path $OutDir 'DATAREF_CONTEXTS.tsv')) }
  @{ n='owner refs';      s='DumpUnresolvedIncomingOwnerRefs.java';      a=@((Join-Path $OutDir 'OWNER_REFS.tsv')) }
  @{ n='string refs';     s='DumpUnresolvedStringReferences.java';       a=@((Join-Path $OutDir 'STRING_REFS.tsv')) }
  @{ n='byte clones';     s='ScanUnresolvedExactByteCloneDomains.java';  a=@((Join-Path $OutDir 'EXACT_BYTE_CLONES.tsv')) }
  @{ n='qualified syms';  s='ScanUnresolvedQualifiedSymbols.java';       a=@((Join-Path $OutDir 'QUALIFIED_SYMBOLS.tsv')) }
)
foreach ($st in $steps) {
  Write-Host "[gfz] scan: $($st.n)" -ForegroundColor Cyan
  Invoke-Step $st.s $st.a | Out-Null
}

Write-Host ""
Write-Host "[gfz] residual evidence written to $OutDir" -ForegroundColor Green
Write-Host "[gfz] EH-contamination census (these are NOT usable as semantic evidence):"
$dr = Import-Csv -LiteralPath (Join-Path $OutDir 'DATAREF_CONTEXTS.tsv') -Delimiter "`t"
$dr | Group-Object data_type | Sort-Object Count -Descending |
      ForEach-Object { Write-Host ("    {0,5}  {1}" -f $_.Count, $(if ($_.Name) { $_.Name } else { '<real code reference>' })) }
$OutDir
