<#
.SYNOPSIS
  Step 1 of the pipeline. Verify the sealed GZF, then fresh-import it into a
  BRAND-NEW writable Ghidra project with auto-analysis disabled.
.DESCRIPTION
  Refuses to reuse an existing project directory unless -Force is given, because
  the GFZ contract requires a fresh import for every checkpoint verification.
#>
[CmdletBinding()]
param(
  [string]$Gzf,
  [string]$ProjectDir,
  [string]$ProjectName = 'GFZ_PARENT',
  [string]$ExpectedSha,
  [switch]$Force
)
. "$PSScriptRoot\GfzEnv.ps1"

if (-not $Gzf)         { $Gzf = Join-Path $GfzParentDir $GfzParentGzf }
if (-not $ExpectedSha) { $ExpectedSha = $GfzParentSha }
if (-not $ProjectDir)  { $ProjectDir = Join-Path $GfzWork ('proj_' + (Get-Date -Format 'yyyyMMdd_HHmmss')) }

if (-not (Test-Path $Gzf)) { throw "GZF not found: $Gzf" }

Write-Host "[gfz] verifying continuation parent" -ForegroundColor Cyan
$size = (Get-Item $Gzf).Length
Write-Host "  size $size bytes"
if ($ExpectedSha -eq $GfzParentSha -and $size -ne $GfzParentSize) {
  throw "GZF size mismatch: expected $GfzParentSize, got $size"
}
Assert-GfzSha -Path $Gzf -Expected $ExpectedSha -Label 'GZF'

if ((Test-Path $ProjectDir) -and -not $Force) {
  $existing = Get-ChildItem -LiteralPath $ProjectDir -ErrorAction SilentlyContinue
  if ($existing) { throw "Project dir not empty: $ProjectDir  (fresh import required; pass -Force to override)" }
}

$log = Join-Path $GfzWork 'import.log'
Write-Host "[gfz] fresh-importing into $ProjectDir\$ProjectName (auto-analysis OFF)" -ForegroundColor Cyan
& "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Import -ProjectDir $ProjectDir -ProjectName $ProjectName `
    -ImportFile $Gzf -Script 'ReportV121Coverage.java' -LogFile $log | Write-Host

Write-Host ""
Write-Host "[gfz] imported. project: $ProjectDir\$ProjectName" -ForegroundColor Green
Write-Host "      next: Verify-GfzCheckpoint.ps1 -ProjectDir '$ProjectDir' -ProjectName '$ProjectName'"
[pscustomobject]@{ ProjectDir = $ProjectDir; ProjectName = $ProjectName; Gzf = $Gzf; Log = $log }
