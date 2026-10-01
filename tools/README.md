# GFZ Tools — FFXII TZA engine reconstruction

Everything needed to advance the **GFZ/GZF V121 full-executable reconstruction** and to
build the `Database/FFXII TZA/` documentation database from it.

Set up **2026-09-02**. Verified working on this machine.

---

## Layout

```
Database/Tools/
  README.md                   <- this manifest
  parent/                     <- the certified continuation GZF (82,110,895 bytes)
  ghidra/
    scripts/                  <- the 21 GFZ Java scripts (mutation authority)
    run/                      <- PowerShell wrappers that enforce the GFZ contract
  analysis-kit/
    gfz-scripts/              <- diff_fas2.py (whole-project diff), fas2_export.py (new)
    historical/               <- prior batch-builder scripts (Linux paths; reference only)
    radare2/                  <- radare2 6.2.0 w64 (independent challenge)
  evidence/                   <- GM160 residual evidence + GN read-only trail + seals
  docs/                       <- handoff, build standard, continuation requirements, seals
  work/                       <- scratch: projects, snapshots, residual dumps (gitignore)
```

---

## Tier 1 — mutation authority

Only this layer may write GFZ state.

| Component | Location | Status |
|---|---|---|
| Ghidra | `C:\Users\Kristian\ghidra\ghidra_12.1.2_PUBLIC` | ✅ 12.1.2 PUBLIC — matches the pack log |
| JDK | `C:\Users\Kristian\ghidra\jdk-21.0.11+10` | ✅ Temurin 21.0.11+10 — same build as the pack log |
| GFZ Ghidra scripts | `ghidra/scripts/*.java` | ✅ 21 scripts |
| Continuation GZF | `parent/…GM160_RECOVERY_TRANSFER_99P58_2026-08-31.gzf` | ✅ SHA verified `381d2aea…7461b` |

`java` is **not** on PATH. Every wrapper sets `JAVA_HOME` from `GfzEnv.ps1`.

### Script argument contracts

| Script | Args |
|---|---|
| `ReportV121Coverage` | `[out.tsv]` |
| `DumpUnresolvedStructure` | `out.tsv` |
| `DumpUnresolvedMechanismFeatures` | `out maxInsns` |
| `DumpUnresolvedNeighborhoodDomains` | `out` |
| `DumpUnresolvedIncomingDataRefContexts` | `out` |
| `DumpUnresolvedIncomingOwnerRefs` | `out` |
| `DumpUnresolvedStringReferences` | `out` |
| `ScanUnresolvedExactByteCloneDomains` | `out` |
| `ScanUnresolvedQualifiedSymbols` | `out` |
| `DumpMsvcVtableRtti` | `out vftable…` |
| `DumpPointerTableResolvedTargets` | `out addr…` |
| `DumpFullCoverageGraph` | `functions.tsv edges.tsv [sidecar.json parent.gzf]` — run through `ghidra\run\Export-GfzCensus.ps1`, which passes the certified parent so the export stamps `functions.parent.json`; `check_census_generation.py` refuses a census whose stamp is not `$GfzParentSha` |
| `DecompileAddressFileBounded` | `output address_file seconds` ← **arg order trap** |
| `EnrichCurrentBodyManifest` | `input output` |
| `ApplyCurrentBodyCodeDomainBatch` | `manifest batchId expectedCount summary` |
| `ApplyCurrentBodyCodeDomainBatchAllowExisting` | same, permits an existing tag |
| `GFZFunctionAnnotationSnapshotV2` | `output.fas2` |
| `GFZNonFunctionAnnotationSnapshotV1` | `output.txt` — non-function annotation state (symbols, comments, equates, DTM, applied types, ref overrides); sorted text for cross-parent diffing |
| `ExtractEmbeddedOriginal` | `output.bin` |
| `PackClosedDomainFile` | `domainPath output.gzf` |
| `ListProjectFiles` | `[out]` — added 2026-09-02, see below |
| `ReportFunctionBrief` | *(none)* |

### ⚠ The program inside the project is **not** named `FFXII_TZA.exe`

A `.gzf` imports under the **packed file's own name**, which changes at every checkpoint:

| Checkpoint | Program name inside the project |
|---|---|
| GM160 recovery-transfer parent | `FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GM160_RECOVERY_TRANSFER_99P58_2026-08-31` |
| an older pack (from the pack log) | `gd_parent` |

So `analyzeHeadless -process FFXII_TZA.exe` fails with exit 1 against a GFZ project — the
`-process` filter matches nothing and the script never runs. **Never hardcode the name.**

`ListProjectFiles.java` enumerates the project, and `Get-GfzProgramName` (in `GfzEnv.ps1`)
parses it. The wrappers now discover the name automatically when `-ProgramName` is omitted;
pass it explicitly only if a project ever holds more than one program.

---

## PowerShell pipeline wrappers

Run from `ghidra/run/`. They exist so the contract cannot be run wrong.

```powershell
# 1. verify + fresh-import the sealed parent (auto-analysis OFF, new project)
$p = .\Import-GfzParent.ps1

# 2. reproduce ledger + snapshot + embedded EXE + residual. Fatal on any mismatch.
.\Verify-GfzCheckpoint.ps1 -ProjectDir $p.ProjectDir -ProjectName $p.ProjectName

# 3. regenerate the full evidence set for the CURRENT residual
.\Dump-GfzResidual.ps1 -ProjectDir $p.ProjectDir -ProjectName $p.ProjectName

# 4. enrich + apply a batch, then whole-project diff (fails on any drift)
.\Apply-GfzBatch.ps1 -ProjectDir $p.ProjectDir -PreEnrichTsv .\gn_pre.tsv `
    -BatchId GN -ExpectedCount 2 -Summary "GN: two protected holds closed"

# 5. SEPARATE invocation, target closed. Requires PACK_PASS.
.\Pack-GfzCheckpoint.ps1 -ProjectDir $p.ProjectDir -DomainPath /FFXII_TZA.exe `
    -OutputGzf ..\..\parent\<next>.gzf

# 6. fresh-import the pack into a COMPLETELY NEW project and verify again
.\Import-GfzParent.ps1 -Gzf ..\..\parent\<next>.gzf -ExpectedSha <sha> -ProjectDir <new>
```

`Verify-GfzCheckpoint` and `Apply-GfzBatch` both **throw** rather than warn. A failed gate
means no mutation and no checkpoint claim.

### ⚠ The hash-convention trap

Two different body hashes exist in this toolchain and the handoff prose never says so:

| Convention | Produced by | Value for `00313A00` |
|---|---|---|
| **Address-salted** (range min/max as BE64, then bytes) | `DumpUnresolvedStructure`, `EnrichCurrentBodyManifest`, **`ApplyCurrentBodyCodeDomainBatch`** | `0966b7b4c90df147b52348bf8a0fd392b1d56a544963fa55e5aa6c778fa16071` |
| **Plain body bytes** | `DumpUnresolvedMechanismFeatures` — and every hash quoted in the handoff prose | `c076cfeadbc81442c947e0c749eefbdef7e7c6717297847333a7cbae9289d246` |

The **apply gate compares the address-salted one.** Never copy a prose hash into a manifest.
Author the 4-column pre-enrich TSV and let `EnrichCurrentBodyManifest` compute column 7.
`Apply-GfzBatch.ps1` enforces this ordering.

Also note: `ApplyCurrentBodyCodeDomainBatch.java` hardcodes `DATE=2026-08-28` into every
comment block it writes. Cosmetic, but the stamp will be wrong for later batches.

---

## Tier 2 — independent challenge tooling

May corroborate or **refute** a reading. May never assign ownership on its own.

| Tool | Location | Status |
|---|---|---|
| **ff12-script** (.ebp decompiler/compiler) | `Collaboration/Tools/ffxii/ff12-script-master/x64/Release/ff12-script.exe` | ✅ built v3.00 |
| **ff12-vbf** (VBF archive unpack/repack) | `Collaboration/Tools/ffxii/VBF Browser/ff12-vbf/ff12-vbf.exe` | ✅ v1.0 |
| **radare2** | `analysis-kit/radare2/bin/radare2.exe` | ✅ 6.2.0 w64 — installed 2026-09-02 |
| **LIEF 1.0.0** · **capstone 5.0.9** · **duckdb** | `Collaboration/Tools/analysis/venv` (Py 3.14) | ✅ |
| **angr 9.3.3** | `Collaboration/Tools/analysis/angr-venv` (Py 3.12.13, uv) | ✅ — needs Py ≤3.12 |
| **DynamoRIO 11.91** | `Collaboration/Tools/analysis/DynamoRIO-Windows-11.91.20692/bin64/drrun.exe` | ✅ |
| **Cheat tables** (3 annotated) | `Collaboration/Tools/ffxii/cheat-tables/*.CT` | ✅ static seed |
| **Ghidra REST bridge** | `http://127.0.0.1:8090` | ⚠ start on demand; `rename_function` broken, use headless |
| **ghidra-mcp** | `mcp__ghidra-mcp__*` | ⚠ needs a connected instance |
| **Cheat Engine 7.7** | `mcp__cheat-engine__*` | ⚠ needs the game running |

Python for the analysis kit:
`Collaboration/Tools/analysis/venv/Scripts/python.exe`

### Banned

**The 7z CLI.** Use standard ZIP or system libarchive. This is a hard GFZ rule.

---

## Certified parent invariants

Baked into `GfzEnv.ps1`; every wrapper checks against them.

| Item | Value |
|---|---|
| GZF size | `82,110,895` |
| GZF SHA-256 | `381d2aea82b96d7af781844e191d9b92a37e93bd2d4ff276a33ba56e7307461b` |
| Snapshot (FAS2) SHA-256 | `d2445517c66513976c83a446f87537a3c1d8c21f5bef033779affe98d7e61a20` |
| Authorized embedded EXE SHA-256 | `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` |
| Residual (160 addrs) SHA-256 | `fa6f614a463bf9981f32cbd4582e31ba23b04e6b803cfbb0139b209dffda5a1a` |
| Canonical V120 (final replay target) | `507490534a8bb67e8d3c6deba4d527c23ab9fdd3672494e511db0d9ef0e511a9` |
| Ledger | 38,161 internal · 38,001 explicit · 160 unresolved · 99.58072% · overlap 0 |

Ghidra image base is `0x00120000`; every address in the evidence and the documentation
database is already in that space.

---

## Building the documentation database

`fas2_export.py` turns a snapshot into the source data for `Database/FFXII TZA/`:

```powershell
$py = 'C:\Users\Kristian\source\repos\XIIOnline\Collaboration\Tools\analysis\venv\Scripts\python.exe'
& $py analysis-kit\gfz-scripts\fas2_export.py work\verify\snapshot.fas2 `
     --tsv work\functions.tsv --jsonl work\functions.jsonl `
     --domains work\domains.tsv --owners work\owners.tsv --unresolved work\unresolved.txt
```

`--jsonl` carries the full GFZ comment block per function — that is the raw material every
system document is written from.

## Querying the knowledge base

`analysis-kit/gfz-scripts/knowledge_db.py` builds a **derived SQLite index** over the documents,
`functions.tsv`, `edges.tsv`, `rip_data_refs.tsv`, `_types/*.tsv` and the question ledger — in about
a second, into `work/knowledge/knowledge.sqlite` (gitignored).

```bash
python knowledge_db.py build            # rebuild (staging + mid-build guard); safe to run any time
python knowledge_db.py check            # CURRENT/STALE vs the recorded input fingerprints - the
                                        #  dependency check, not a timestamp or integrity_check
python knowledge_db.py queries          # charter §7's list, and what is NOT answerable
python knowledge_db.py query callers 0017DB90
python knowledge_db.py query writers-of-field "WidgetSingleton02AEE4C0+0008"   # w AND rw kinds
python knowledge_db.py query readers-of-global 02F9736C
python knowledge_db.py sql "SELECT category, COUNT(*) FROM documents GROUP BY category"
```

`query`/`sql`/`info` refuse to answer from a stale index — a stale dependency prints `STALE`
naming the moved inputs rather than returning apparently-fresh rows. `query --refresh`
rebuilds through the staging guard first; `query --snapshot` runs a labelled as-of read with
the build's revision, hashes and stale list attached. Policy: `FFXII TZA/_index/DERIVED-DATA.md`.

**`edges.caller_is_eh` is a column.** Unwind-funclet and catch-handler callers are banned as semantic
evidence and `edges.tsv` offers them by default; `query callers` filters them, and
`query callers-including-banned` shows both so the difference is visible rather than assumed.

The documents remain authoritative — the index asserts nothing of its own. Full description and the
list of what it cannot answer: `Database/FFXII TZA/_index/KNOWLEDGE-SCHEMA.md`.

---

## ⚠ `work/headless/GFZ_HEADLESS` holds **GN158** — do not use it

**Added 2026-09-07 after it silently served a whole session's decompiles.**

That project was imported **2026-09-02 01:08** and never re-imported. It reports
`explicit=38003 unresolved=158 pct=99.58596`, snapshot `46f02e26…`, residual `c5d4b7f7…` — the
**`GN158` lineage entry**, two certified checkpoints behind the current parent.

**Use `work/headless_gn160/GFZ_GN160`**, imported and verified 2026-09-07:

```
explicit=38022  unresolved=139  pct=99.63575
snapshot b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
residual b5008f9d42c7cd6c8f4737528cb9c821cd2b4da419e5523fc7bf67dcdc5e3274
embedded EXE 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
CHECKPOINT VERIFIED
```

### Why this was invisible

`GfzEnv.ps1` was correctly updated to GN160 on 2026-09-03, exactly as the non-negotiable requires.
**The project was not.** Every wrapper auto-discovers the program name from the project, so
`Invoke-GfzHeadless -Mode Process` on the stale project runs happily and prints a plausible name —
`…GM160_RECOVERY_TRANSFER_99P58_2026-08-31` — which *looks* like a parent name and is not the current
one. **Nothing fails. The decompiles succeed. The names are two checkpoints old.**

> **The standing rule "update `GfzEnv.ps1` after every certified checkpoint" has a silent twin:
> update, or re-import, the working project too.** `Verify-GfzCheckpoint` is the only thing that
> catches the gap, and it is only ever run at session start — so a project that goes stale between
> sessions is used unverified until someone runs it again.

**Run `Verify-GfzCheckpoint` against the project you are about to read from, not against the one the
last session happened to leave behind.**
