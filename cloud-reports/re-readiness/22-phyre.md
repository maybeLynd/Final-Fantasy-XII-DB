# Reconstruction readiness — `FFXII TZA/22-Middleware-PhyreEngine/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-22-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`86b70c69`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** _filled in when the report is complete (see the end of the commit history)._

Citation form: `path:line`, where `path` is relative to `FFXII TZA/22-Middleware-PhyreEngine/`. To keep the tables
readable, the long page paths are abbreviated as follows (the abbreviation is always followed by `:line`):

| abbrev. | page | lines |
|---|---|---:|
| `README` | `README.md` | 82 |
| `CAM` | `the-camera-state-snapshot.md` | 228 |
| `MAP` | `Subsystem-Map/phyre-subsystem-map.md` | 425 |
| `MOD` | `Subsystem-Map/the-fifteen-modules-registered-before-main.md` | 598 |
| `APP` | `Application-Framework-Boundary/the-game-is-a-phyre-application.md` | 1,070 |
| `PAC` | `Phyre-Asset-Container/README.md` | 48 |
| `HDR` | `Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md` | 749 |
| `C-HDR` | `Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md` | 955 |
| `NS` | `Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` | 644 |
| `C-NS` | `Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md` | 506 |
| `CDMS` | `Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` | 1,978 |
| `C-CD` | `Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` | 917 |
| `MR` | `Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md` | 2,402 |
| `AR` | `Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md` | 445 |
| `IS` | `Reflection-And-Class-Metadata/phyre-class-instance-sizes-and-alignments.md` | 220 |
| `FS` | `Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md` | 495 |
| `LUA` | `Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md` | 1,259 |
| `ACC` | `Script-Object-Accessors/phyre-script-object-accessors.md` | 953 |
| `PPF` | `Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md` | 1,715 |
| `PFX` | `Post-Process-Chain/the-phyre-post-effect-class-family.md` | 884 |
| `CTX` | `Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md` | 985 |
| `FRM` | `The-Frame/what-happens-between-two-frames.md` | 1,547 |
| `ANI` | `Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md` | 1,122 |

"Not stated" means none of the 23 pages says it. Where another category's page is the only place a point is made,
the pointer is given as a path from `FFXII TZA/`, but that page was not audited for this report.

## Pages read

All 23 `.md` files were read in full (20,227 lines). Member `.tsv` files were opened only to confirm layouts and row
counts; no item below rests on a `.tsv` alone, and where a `.tsv` disagrees with its page that is reported as a
contradiction, not resolved.

| page | front matter as the page states it | in-body / index banner that differs |
|---|---|---|
| `README` | none; "Functions \| 6,768" (`README:8`) | indexes 8 of the 22 pages only (`README:13-63`) |
| `CAM` | `status: DOCUMENTED — its one register row, SD-60, is ANSWERED …` (`CAM:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-03` (`:19`) | body dated to 2026-09-30 (`CAM:104`, `:186`) |
| `MAP` | `status: DOCUMENTED — how the 6,769 Phyre functions map onto the classes (AQ-2) is SUPERSEDED 2026-09-26 …` (`MAP:4`); `evidence_tier: 4` (`:6`); `last_reviewed: 2026-09-02` (`:19`) | "**PARTIAL, and tier 4 by construction.**" (`MAP:41`) |
| `MOD` | `status: AUDITED` (`MOD:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-08` (`:19`) | not indexed in `README` |
| `APP` | `status: AUDITED` (`APP:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | `README:25` "**DOCUMENTED, tier 1, one falsification pass.**" |
| `PAC` | none | "corrected 2026-09-03" heading (`PAC:27`) |
| `HDR` | `status: AUDITED` (`HDR:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:20`); `corpus_validated: "169 / 169 extracted .phyre files — 0.47 % of the 35,984 shipped"` (`:19`) | body covers all 35,984 files from 2026-09-12 (`HDR:227-234`) |
| `C-HDR` | `readiness: CONTRACT READY` (`C-HDR:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:18`) | "This is the first contract in `22-Middleware-PhyreEngine`" (`C-HDR:32`) |
| `NS` | `status: AUDITED` (`NS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:20`) | body dated to 2026-09-30 (`NS:275`) |
| `C-NS` | `readiness: CONTRACT READY` (`C-NS:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:17`) | — |
| `CDMS` | `status: AUDITED` (`CDMS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-13` (`:18`) | `README:21` "**DOCUMENTED, tier 1.**" |
| `C-CD` | `readiness: CONTRACT READY` (`C-CD:6`); `confidence: PROVEN` (`:7`); `last_reviewed: 2026-09-12` (`:17`) | "Status `FAIL_INCOMPLETE`" mutation campaign (`C-CD:329-330`) |
| `MR` | `status: AUDITED` (`MR:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | `README:33` "**DOCUMENTED, tier 1, one falsification pass.**"; body dated to 2026-09-28 |
| `AR` | `status: AUDITED — SD-61, SD-62, SD-63 and UQ-281 are ANSWERED and every box on the page is closed …` (`AR:4`); `readiness: SIGNATURE RESOLVED` (`:8`); `confidence: PROVEN` (`:9`); `last_reviewed: 2026-09-08` (`:17`) | an un-boxed open bullet remains (`AR:181`) |
| `IS` | `status: DOCUMENTED` (`IS:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-19` (`:18`) | — |
| `FS` | `status: AUDITED - was REOPENED; …` (`FS:4`); `evidence_tier: 3` (`:6`); `last_reviewed: 2026-09-05` (`:20`) | "**Evidence tier 9, deliberately.**" (`FS:39`); "**REOPENED 2026-09-07.**" (`FS:122`) |
| `LUA` | `status: DOCUMENTED` (`LUA:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`) | body dated to 2026-09-25 (`LUA:937`) |
| `ACC` | `status: AUDITED` (`ACC:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-13` (`:18`) | `README:46` "**DOCUMENTED, tier 2.**" |
| `PPF` | `status: AUDITED` (`PPF:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-13` (`:12`) | not indexed in `README` |
| `PFX` | `status: DOCUMENTED` (`PFX:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-29` (`:15`) | `README:59` "tier 2 for the names and tier 1 for everything else" |
| `CTX` | `status: DOCUMENTED` (`CTX:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-30` (`:15`) | — |
| `FRM` | `status: AUDITED` (`FRM:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-07` (`:18`) | `README:14` "**DOCUMENTED, tier 1, crossref-clean.**" |
| `ANI` | `status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) …` (`ANI:4`); `evidence_tier: 2` (`:6`); `last_reviewed: 2026-09-30` (`:18`) | not indexed in `README` |

Member `.tsv` files checked for layout and count only (results are used in §3 where they disagree with a page):
`Subsystem-Map/members/phyre-function-class-map.tsv` (6,769 rows), `members/phyre-*.tsv` (17 module files),
`Phyre-Asset-Container/members/user-fixup-census.tsv` (239 rows, files sum 35,984),
`Reflection-And-Class-Metadata/phyre-field-schema.tsv` (686 data rows, 246 `class`, 182 `class_leaf`),
`Reflection-And-Class-Metadata/members/phyre-class-instance-sizes.tsv` (177 rows), the 23 family `.tsv` files in
`Reflection-And-Class-Metadata/members/`, the 24 in `Script-Object-Accessors/members/`, and the four in
`Post-Process-Chain/members/`.

---
