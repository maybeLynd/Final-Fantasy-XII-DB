<#
.SYNOPSIS
  Export the full-coverage graph census (functions.tsv + edges.tsv) WITH a
  provenance sidecar naming the parent GZF the export was taken from.

  The census has no manifest - functions.tsv carries only an mtime, so a
  wrong-generation export is indistinguishable from a current one. This
  wrapper is the export step that fixes that: it passes the certified
  parent's path to DumpFullCoverageGraph, which hashes the GZF itself and
  writes functions.parent.json beside the census. check_census_generation.py
  is the gate that refuses when the stamped sha is not GfzEnv's
  $GfzParentSha.

  The program name inside a GFZ project changes at every checkpoint - pass
  it explicitly (ListProjectFiles finds it); it is never derived here.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$ProjectDir,
  [Parameter(Mandatory)][string]$ProjectName,
  [Parameter(Mandatory)][string]$ProgramName,
  [string]$OutDir
)
. "$PSScriptRoot\GfzEnv.ps1"

if (-not $OutDir) { $OutDir = Join-Path $GfzWork 'graph' }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$gzf = Join-Path $GfzParentDir $GfzParentGzf
if (-not (Test-Path $gzf)) { throw "certified parent not on disk: $gzf" }

$funcs = Join-Path $OutDir 'functions.tsv'
$edges = Join-Path $OutDir 'edges.tsv'
$side  = Join-Path $OutDir 'functions.parent.json'

& "$PSScriptRoot\Invoke-GfzHeadless.ps1" -Mode Process -ProjectDir $ProjectDir `
  -ProjectName $ProjectName -ProgramName $ProgramName -Script 'DumpFullCoverageGraph.java' `
  -ScriptArgs @($funcs, $edges, $side, $gzf) | Write-Output

# The gate runs immediately: an export that stamps the wrong parent must not
# survive the step that produced it.
& python (Join-Path $GfzAnalysis 'check_census_generation.py') --graph $OutDir
if ($LASTEXITCODE -ne 0) { throw "check_census_generation refused the export - see above" }
