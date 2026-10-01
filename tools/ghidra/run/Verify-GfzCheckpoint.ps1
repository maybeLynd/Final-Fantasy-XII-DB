<#
.SYNOPSIS
  Reproduce a checkpoint's certified state from a freshly imported project.
.DESCRIPTION
  Runs the four proofs the GFZ contract demands before ANY mutation:
    1. ledger        (ReportV121Coverage)
    2. snapshot SHA  (GFZFunctionAnnotationSnapshotV2 -> FAS2)
    3. embedded EXE  (ExtractEmbeddedOriginal -> authorized SHA)
    4. residual      (unresolved address list -> residual SHA)
  Any mismatch is fatal. Pass -Expect* to verify a post-mutation checkpoint instead
  of the sealed GM160 parent.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$ProjectDir,
  [string]$ProjectName = 'GFZ_PARENT',
  [string]$ProgramName,
  [string]$OutDir,
  [string]$ExpectSnapshot,
  [string]$ExpectResidual,
  [int]$ExpectExplicit   = -1,
  [int]$ExpectUnresolved = -1,
  # Forwarded to Invoke-GfzHeadless: verify a program that is not the current
  # certified parent (the certification path for a NEW checkpoint is exactly
  # that). CT-2's guard stays on unless this is passed knowingly.
  [switch]$AllowNonParentProgram
)
. "$PSScriptRoot\GfzEnv.ps1"
if (-not $ProgramName) {
  $ProgramName = Get-GfzProgramName -ProjectDir $ProjectDir -ProjectName $ProjectName
  Write-Host "[gfz] program: $ProgramName" -ForegroundColor DarkGray
}

# Default the scratch dir PER PROJECT, not to a shared 'verify' folder. Several sessions verify
# concurrently, and a shared dir races on snapshot.fas2 / embedded_exe.bin / residual_addrs.txt —
# where the loser silently reads the winner's artefacts and reports a pass for the wrong project.
# Pass -OutDir explicitly to override. (Race reported by a parallel session, 2026-09-02.)
if (-not $OutDir)         { $OutDir = Join-Path $GfzWork ('verify_' + $ProjectName) }
if (-not $ExpectSnapshot) { $ExpectSnapshot = $GfzParentSnapshot }
if (-not $ExpectResidual) { $ExpectResidual = $GfzResidualSha }
if ($ExpectExplicit   -lt 0) { $ExpectExplicit   = $GfzLedger.explicit }
if ($ExpectUnresolved -lt 0) { $ExpectUnresolved = $GfzLedger.unresolved }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$covTsv  = Join-Path $OutDir 'coverage.tsv'
$fas2    = Join-Path $OutDir 'snapshot.fas2'
$exeBin  = Join-Path $OutDir 'embedded_exe.bin'
$addrs   = Join-Path $OutDir 'residual_addrs.txt'
$failed  = @()

function Invoke-Step { param([string]$Script,[string[]]$A)
  & "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Process -ProjectDir $ProjectDir -ProjectName $ProjectName `
      -ProgramName $ProgramName -Script $Script -ScriptArgs $A `
      -AllowNonParentProgram:$AllowNonParentProgram
}

Write-Host "[gfz] 1/4 ledger" -ForegroundColor Cyan
$covOut = Invoke-Step 'ReportV121Coverage.java' @($covTsv)
$line = ($covOut -split "`n" | Where-Object { $_ -match 'V121_COVERAGE' } | Select-Object -First 1)
if (-not $line) { throw 'ReportV121Coverage produced no V121_COVERAGE line' }
Write-Host "  $($line.Trim())"
$vals = @{}
foreach ($m in [regex]::Matches($line,'(\w+)=([0-9.]+)')) { $vals[$m.Groups[1].Value] = $m.Groups[2].Value }
if ([int]$vals['internal']   -ne $GfzLedger.internal) { $failed += "internal=$($vals['internal']) expected $($GfzLedger.internal)" }
if ([int]$vals['overlap']    -ne 0)                   { $failed += "overlap=$($vals['overlap']) expected 0" }
if ([int]$vals['explicit']   -ne $ExpectExplicit)     { $failed += "explicit=$($vals['explicit']) expected $ExpectExplicit" }
if ([int]$vals['unresolved'] -ne $ExpectUnresolved)   { $failed += "unresolved=$($vals['unresolved']) expected $ExpectUnresolved" }

Write-Host "[gfz] 2/4 deterministic snapshot" -ForegroundColor Cyan
Invoke-Step 'GFZFunctionAnnotationSnapshotV2.java' @($fas2) | Out-Null
$snapSha = Get-GfzSha256 -Path $fas2
Write-Host "  snapshot $snapSha"
if ($snapSha -ne $ExpectSnapshot.ToLowerInvariant()) { $failed += "snapshot $snapSha expected $ExpectSnapshot" }

Write-Host "[gfz] 3/4 embedded authorized EXE" -ForegroundColor Cyan
Invoke-Step 'ExtractEmbeddedOriginal.java' @($exeBin) | Out-Null
$exeSha = Get-GfzSha256 -Path $exeBin
Write-Host "  embedded EXE $exeSha"
if ($exeSha -ne $GfzAuthorizedExeSha) { $failed += "embedded EXE $exeSha expected $GfzAuthorizedExeSha" }

Write-Host "[gfz] 4/4 residual regeneration" -ForegroundColor Cyan
# Residual address list = the --UNRESOLVED-- section of the coverage TSV, entry column only.
$cov = Get-Content -LiteralPath $covTsv
$idx = [Array]::IndexOf($cov, '--UNRESOLVED--')
if ($idx -lt 0) { throw 'coverage TSV has no --UNRESOLVED-- section' }
# When --UNRESOLVED-- is the LAST line the section is empty: ($idx+1)..($cov.Length-1)
# would produce a DESCENDING range that recaptures the header as a fake residual.
$res = @()
if ($idx -lt $cov.Length - 1) {
  $res = $cov[($idx+1)..($cov.Length-1)] | Where-Object { $_ -ne '' -and $_ -match '^[0-9A-Fa-f]{8}\b' } | ForEach-Object { ($_ -split "`t")[0] }
}
# Contract: LF-terminated, sorted ascending, uppercase hex - matches GM160_CURRENT160_ADDRS.txt
$sorted = $res | Sort-Object
$bytes = [System.Text.Encoding]::ASCII.GetBytes((($sorted -join "`n") + "`n"))
[System.IO.File]::WriteAllBytes($addrs, $bytes)
$resSha = Get-GfzSha256 -Path $addrs
Write-Host "  residual count $($sorted.Count)  sha $resSha"
if ($sorted.Count -ne $ExpectUnresolved) { $failed += "residual count $($sorted.Count) expected $ExpectUnresolved" }
if ($resSha -ne $ExpectResidual.ToLowerInvariant()) { $failed += "residual $resSha expected $ExpectResidual" }

Write-Host ""
if ($failed.Count -gt 0) {
  Write-Host "[gfz] CHECKPOINT VERIFY FAILED" -ForegroundColor Red
  $failed | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  throw 'checkpoint verification failed - do not mutate'
}
Write-Host "[gfz] CHECKPOINT VERIFIED - ledger, snapshot, embedded EXE and residual all reproduce" -ForegroundColor Green
[pscustomobject]@{ Coverage=$covTsv; Snapshot=$fas2; SnapshotSha=$snapSha; Residual=$addrs; ResidualSha=$resSha; EmbeddedExeSha=$exeSha }
