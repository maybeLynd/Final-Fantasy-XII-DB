<#
.SYNOPSIS
  Pack a CLOSED DomainFile into a durable .gzf. Separate invocation by contract.
.DESCRIPTION
  A modified working project is NOT a checkpoint. This must run as its own
  headless invocation, after the mutating invocation has fully exited, with the
  target reporting open=false busy=false changed=false. Requires PACK_PASS in the
  output and a plausible file size; a large-but-truncated file is not a pack.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$ProjectDir,
  [string]$ProjectName = 'GFZ_PARENT',
  [Parameter(Mandatory)][string]$DomainPath,
  [Parameter(Mandatory)][string]$OutputGzf,
  [long]$MinBytes = 80000000
)
. "$PSScriptRoot\GfzEnv.ps1"

$log = Join-Path $GfzWork 'pack.log'
Write-Host "[gfz] packing $DomainPath -> $OutputGzf" -ForegroundColor Cyan
$out = & "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Project -ProjectDir $ProjectDir -ProjectName $ProjectName `
         -Script 'PackClosedDomainFile.java' -ScriptArgs @($DomainPath, $OutputGzf) -LogFile $log
$out | Write-Host

$target = ($out -split "`n" | Where-Object { $_ -match 'PACK_TARGET' } | Select-Object -First 1)
if ($target) { Write-Host "  $($target.Trim())" }
if ($out -notmatch 'PACK_PASS') { throw 'PACK_PASS not reported - pack is INVALID' }
if (-not (Test-Path $OutputGzf)) { throw "pack output missing: $OutputGzf" }
$size = (Get-Item $OutputGzf).Length
if ($size -lt $MinBytes) { throw "pack output implausibly small ($size bytes) - treat as truncated/invalid" }
$sha = Get-GfzSha256 -Path $OutputGzf

Write-Host ""
Write-Host "[gfz] PACK_PASS  size=$size" -ForegroundColor Green
Write-Host "[gfz] sha256=$sha"
Write-Host "[gfz] NOT YET CERTIFIED - now fresh-import this pack into a COMPLETELY NEW project"
Write-Host "      Import-GfzParent.ps1 -Gzf '$OutputGzf' -ExpectedSha $sha -ProjectDir <new>"
[pscustomobject]@{ Gzf=$OutputGzf; Size=$size; Sha256=$sha; Log=$log }
