# GfzEnv.ps1 — common paths/environment for the GFZ headless pipeline.
# Dot-source this from every wrapper:  . "$PSScriptRoot\GfzEnv.ps1"

$ErrorActionPreference = 'Stop'

$GfzGhidraHome = 'C:\Users\Kristian\ghidra\ghidra_12.1.2_PUBLIC'
$GfzJavaHome   = 'C:\Users\Kristian\ghidra\jdk-21.0.11+10'
$GfzHeadless   = Join-Path $GfzGhidraHome 'support\analyzeHeadless.bat'

$GfzToolsRoot  = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # ...\Database\Tools
$GfzScripts    = Join-Path $GfzToolsRoot 'ghidra\scripts'
$GfzAnalysis   = Join-Path $GfzToolsRoot 'analysis-kit\gfz-scripts'
$GfzParentDir  = Join-Path $GfzToolsRoot 'parent'
$GfzEvidence   = Join-Path $GfzToolsRoot 'evidence'
$GfzWork       = Join-Path $GfzToolsRoot 'work'

# --- CURRENT certified parent -------------------------------------------------
# GN162 checkpoint, 2026-09-16. Supersedes GN161.
# UPDATE THIS BLOCK after every certified checkpoint, or every later run works from a
# stale parent and silently re-does closed work.
#
# GN162 is GN161 plus batch R30: the last 30 residual rows of residual-30-GN161.tsv,
# evidence-validated by OPUS (residual-30-GN161-stage1.tsv, fb75d534) and ruled
# ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM (REVIEW-residual30-stage1-proposals.md) --
# 30/30 domains stand as written; one evidence-cite correction folded in
# (0024B580: the-unresolved-158.md 1164-1240 -> 1280-1347, same file).
# Every figure moves by exactly thirty and nothing else moves at all.
# **Residual count 30 -> 0: the V121 full-executable ledger is closed at 100.00000%.**
#
# Applied under the full fence: diff CLEAN (comment/tags only on exactly 30),
# immutable_drift 0, added/removed 0/0, tag_removals 0; AllowExisting variant;
# packed PACK_PASS; certified by fresh import into work\gn162_certify with the
# embedded EXE re-extracting to the authorized hash below and the imported
# snapshot matching the post-mutation snapshot byte-for-byte. The certification
# surfaced and fixed a Verify-GfzCheckpoint edge case: an EMPTY --UNRESOLVED--
# tail section had the slice recapture the header as a fake residual -- first
# time the pipeline ever saw unresolved=0.
$GfzParentGzf        = 'FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GN162_100P000_2026-09-16.gzf'
$GfzParentSize       = 82201392
$GfzParentSha        = '59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92'
$GfzParentSnapshot   = '16a2a832d8856ba3d5c78d531ef0fd2295ef7dce956ca5cd545cf54f065bd192'
$GfzAuthorizedExeSha = '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8'
$GfzResidualSha      = '01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b'
$GfzCanonicalV120Sha = '507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9'

$GfzLedger = @{
  internal    = 38161
  owner       = 9409
  finalNo     = 585
  codeDomain  = 28167
  explicit    = 38161
  unresolved  = 0
  overlap     = 0
  pct         = '100.00000'
}

# --- Superseded lineage (provenance only; never a continuation parent) ---------
$GfzLineage = @(
  @{ tag='GN161'; gzf='...GN161_99P921_2026-09-14.gzf'
     sha='11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500'
     snapshot='c16409ec2c3b9070ea6ce3b6a16f5b4f2d9827380fe5cb626af173cc63739e4c'
     residual='955da8c990265c87878d7b6c5e30e0fdfdb395825745cadc3813ec3b40a93353'
     explicit=38131; unresolved=30 }
  @{ tag='GN160'; gzf='...GN160_99P636_2026-09-03.gzf'
     sha='fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708'
     snapshot='b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34'
     residual='b5008f9d42c7cd6c8f4737528cb9c821cd2b4da419e5523fc7bf67dcdc5e3274'
     explicit=38022; unresolved=139 }
  @{ tag='GN159'; gzf='...GN159_99P596_2026-09-03.gzf'
     sha='fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7'
     snapshot='a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd'
     residual='3188016e863484acdd899c889acb8d860360ef9e5b7fcba6be7ecf928a464726'
     explicit=38007; unresolved=154 }
  @{ tag='GN158'; gzf='...GN158_99P586_2026-09-02.gzf'
     sha='2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9'
     snapshot='46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2'
     residual='c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff'
     explicit=38003; unresolved=158 }
  @{ tag='GM160'; gzf='…GM160_RECOVERY_TRANSFER_99P58_2026-08-31.gzf'
     sha='381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b'
     snapshot='d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20'
     residual='fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a'
     explicit=38001; unresolved=160 }
)

if (-not (Test-Path $GfzHeadless)) { throw "analyzeHeadless not found: $GfzHeadless" }
if (-not (Test-Path $GfzJavaHome)) { throw "JDK 21 not found: $GfzJavaHome" }
$env:JAVA_HOME = $GfzJavaHome
if (-not (Test-Path $GfzWork)) { New-Item -ItemType Directory -Force -Path $GfzWork | Out-Null }

function Get-GfzSha256 {
  param([Parameter(Mandatory)][string]$Path)
  (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Assert-GfzSha {
  param([string]$Path, [string]$Expected, [string]$Label)
  $actual = Get-GfzSha256 -Path $Path
  if ($actual -ne $Expected.ToLowerInvariant()) {
    throw "$Label SHA MISMATCH`n  expected $Expected`n  actual   $actual"
  }
  Write-Host "  [OK] $Label $actual"
}

function Assert-GfzProjectUnlocked {
  <#
    A Ghidra project can only be opened by one process at a time. If the GUI has it open,
    every headless invocation fails - and Ghidra's own message is unhelpful. Fail early
    and say what is actually wrong.

    Recommended pattern: keep GUI browsing and headless pipeline work in SEPARATE project
    copies imported from the same sealed GZF. They are equivalent and independently
    verifiable, so nothing is lost by having two.
  #>
  param(
    [Parameter(Mandatory)][string]$ProjectDir,
    [Parameter(Mandatory)][string]$ProjectName
  )
  $lock = Join-Path $ProjectDir ($ProjectName + '.lock')
  if (Test-Path $lock) {
    $holders = @(Get-Process javaw, java -ErrorAction SilentlyContinue |
                 Select-Object -ExpandProperty Id)
    throw ("project is LOCKED: $lock`n" +
           "  Held by a Ghidra GUI or another headless run (java/javaw PIDs: $($holders -join ', ')).`n" +
           "  Close it, or run headless against a separate project copy - see Tools/README.md.")
  }
}

function Get-GfzProgramName {
  <#
    Discover the program (DomainFile) name inside a project.

    The name is derived from the packed GZF filename and therefore CHANGES at every
    checkpoint - e.g. the GM160 parent imports as
    'FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GM160_RECOVERY_TRANSFER_99P58_2026-08-31',
    while an older pack used '/gd_parent'. Never hardcode it.
  #>
  param(
    [Parameter(Mandatory)][string]$ProjectDir,
    [Parameter(Mandatory)][string]$ProjectName
  )
  Assert-GfzProjectUnlocked -ProjectDir $ProjectDir -ProjectName $ProjectName
  $out = & $GfzHeadless $ProjectDir $ProjectName `
           -scriptPath $GfzScripts -postScript 'ListProjectFiles.java' 2>&1 | Out-String
  $names = @()
  foreach ($m in [regex]::Matches($out, 'PROJECT_FILE (\S+) content=(\S+)')) {
    if ($m.Groups[2].Value -eq 'Program') { $names += $m.Groups[1].Value.TrimStart('/') }
  }
  if ($names.Count -eq 0) {
    if ($out -match 'lock|Unable to open project|already open') {
      throw ("project appears LOCKED: $ProjectDir\$ProjectName`n" +
             "  A Ghidra GUI or another headless run holds it. Close that instance, or use a " +
             "separate project for headless work (recommended - see Tools/README.md).")
    }
    throw "no Program DomainFile found in $ProjectDir\$ProjectName"
  }
  if ($names.Count -gt 1) {
    throw ("project holds $($names.Count) programs; pass -ProgramName explicitly:`n  " +
           ($names -join "`n  "))
  }
  $names[0]
}
