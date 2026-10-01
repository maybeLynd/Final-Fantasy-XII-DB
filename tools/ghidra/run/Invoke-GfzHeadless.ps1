<#
.SYNOPSIS
  Low-level analyzeHeadless driver. Every other wrapper goes through this.
.PARAMETER Mode
  Import  - import a .gzf into a NEW project (auto-analysis always disabled)
  Process - run scripts against an existing program in an existing project
  Project - run scripts with NO program context (used by PackClosedDomainFile)
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][ValidateSet('Import','Process','Project')][string]$Mode,
  [Parameter(Mandatory)][string]$ProjectDir,
  [Parameter(Mandatory)][string]$ProjectName,
  [string]$ImportFile,
  [string]$ProgramName,
  [Parameter(Mandatory)][string]$Script,
  [string[]]$ScriptArgs = @(),
  [string]$LogFile,
  # CT-2 escape hatch: Process refuses a program that is not the certified
  # parent. Certifying a NEW checkpoint is the legitimate exception - pass this
  # knowingly, never to silence an unexplained mismatch.
  [switch]$AllowNonParentProgram
)
. "$PSScriptRoot\GfzEnv.ps1"

if (-not (Test-Path $ProjectDir)) { New-Item -ItemType Directory -Force -Path $ProjectDir | Out-Null }

$cmd = @($ProjectDir, $ProjectName)
switch ($Mode) {
  'Import'  {
    if (-not $ImportFile) { throw 'Import mode requires -ImportFile' }
    $cmd += @('-import', $ImportFile, '-noanalysis')
  }
  'Process' {
    if (-not $ProgramName) { throw 'Process mode requires -ProgramName' }
    # CT-2 (2026-09-27): the program must be the CURRENT certified parent. The
    # five-day stale-parent gap survived because Verify-GfzCheckpoint runs only
    # at session start while the project drifts between sessions; the program
    # name derives from the GZF it was imported from and the current parent's
    # name is $GfzParentGzf, so the check is one string compare per run.
    if (-not $AllowNonParentProgram) {
      $expected = [IO.Path]::GetFileNameWithoutExtension($GfzParentGzf)
      if ($ProgramName -ne $expected) {
        throw ("Process refused: program '$ProgramName' is not the certified " +
               "parent '$expected'.`n  The project went stale between " +
               "sessions - re-import the current parent, or pass " +
               "-AllowNonParentProgram when this run is deliberately against " +
               "another image (e.g. certifying a new checkpoint).")
      }
    }
    $cmd += @('-process', $ProgramName, '-noanalysis')
  }
  'Project' { }
}
$cmd += @('-scriptPath', $GfzScripts, '-postScript', $Script)
if ($ScriptArgs.Count -gt 0) { $cmd += $ScriptArgs }

Write-Host "[gfz] analyzeHeadless $($cmd -join ' ')" -ForegroundColor DarkGray
$out = & $GfzHeadless @cmd 2>&1
$code = $LASTEXITCODE
$text = $out | Out-String
if ($LogFile) { $text | Out-File -FilePath $LogFile -Encoding utf8 }
Write-Output $text
if ($code -ne 0) { throw "analyzeHeadless exited $code (script: $Script)" }
