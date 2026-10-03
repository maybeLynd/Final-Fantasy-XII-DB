# Reconstruction readiness, pass 2: `FFXII TZA/26-PKFL-Package-Container/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Lane | FABLE, session r2-27 |
| Date | 2026-10-03 |
| Snapshot | this repo at `b23bdddd` (text synced from XIIOnline `f9d9053b9`); no executable, archive, Ghidra or live game was used |
| Pass 1 | [`cloud-reports/re-readiness/26-pkfl.md`](../re-readiness/26-pkfl.md) (2026-10-02, snapshot `f26c5667`) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes a page with its location. |

Citation form: `ABBREV:line`. Line numbers are those of this snapshot. Pass 1 read only the two pages in the
folder; this pass also reads the pages and register rows that now answer pass-1 gaps, and cites them.

| abbrev. | page (relative to `FFXII TZA/`) |
|---|---|
| `PK` | `26-PKFL-Package-Container/Container/pkfl-package-container.md` (520 lines; 504 in pass 1) |
| `RM` | `26-PKFL-Package-Container/README.md` (178 lines, unchanged length) |
| `OQ` | `_index/OPEN-QUESTIONS.md` (the register) |
| `VP` | `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md` |
| `QP` | `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` |
| `IS` | `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` |
| `AN` | `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md` |
| `AL` | `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md` |
| `WT` | `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` |
| `SP` | `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` |
| `SV` | `01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md` |
| `SW` | `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` |
| `GA` | `00-Engine-Core-Runtime/Application-Root/game-application.md` |
| `EB` | `25-EBP-Script-Container/README.md` |

## 1. Summary

**What changed since pass 1.** On 2026-10-02 OPUS put in-place corrections ("*corrected 2026-10-02, OPUS: …
re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages*") through `PK` §§2, 3, 5,
6, 6b and 7 and `RM`. These corrections settle most of pass 1's four-byte-era contradictions and restate the
corpus invariants under the pair reading. `PK` also gained two new sections, an interior-citation table (`PK:506-512`)
and a homed-body table (`PK:514-520`). Several structural gaps pass 1 listed as missing from the folder are answered
on neighbouring pages (`VP` §2.1-§2.5, `QP` §2.2, `AN` §3, `IS` §3) and in register rows (`FZ-12`, `FZ-19`, `FZ-20`,
`GA-5`, `CC-9`, `FRP-2`, `OV-35`). Most of those answers are older than pass 1, which read only the folder.

**Pass-1 items judged: 66.** These are pass 1's §2 gaps (S-1…S-8, G-1…G-18, U-1…U-5) and its §3 contradictions
(X-1…X-15, B-1…B-20). The contradictions are included because the brief counts "two pages that disagree" as a gap.

| verdict | S (self-stated) | G (structural) | U (unexplained) | X (value-changing) | B (stale / banner) | **total** |
|---|---:|---:|---:|---:|---:|---:|
| CLOSED | 1 | 5 | 1 | 9 | 7 | **23** |
| NARROWED | 2 | 10 | 3 | 6 | 1 | **22** |
| OPEN | 5 | 0 | 0 | 0 | 12 | **17** |
| WRONG-IN-PASS-1 | 0 | 3 | 1 | 0 | 0 | **4** |
| **total** | 8 | 18 | 5 | 15 | 20 | **66** |

Classes of the 39 still-open pass-1 items (NARROWED + OPEN): **DOC 23 · STATIC 10 · DATA 6 · RUNTIME 0**. No pass-1 item and no new gap needs
the live game. 14 of the 23 DOC items are stale text or front matter on `PK` / `RM` themselves.

**New gaps: 8.** DOC 6 · STATIC 1 · DATA 1 · RUNTIME 0 (§3).

**Rating: MOSTLY, unchanged from pass 1** (pass 1: MOSTLY overall, with three parts NOT YET). The three parts pass 1
rated NOT YET (writing a package, `(ns, index)` addressing, the sub-file request) are now **MOSTLY**: what they
lack is pointers and two narrow static reads, not structure (§4).
