# Reconstruction readiness — `FFXII TZA/24-Compiler-And-CRT-Runtime/`

| | |
|---|---|
| Stream | R (reconstruction readiness), per [`docs/cloud-briefs/re-readiness.md`](../../docs/cloud-briefs/re-readiness.md) |
| Board task | `OPUS-CLOUD-R-READINESS-24-1002` |
| Date | 2026-10-02 |
| Snapshot | this repo's text snapshot only (`34861cfd`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item is a quotation or a paraphrase of a page, with its location. Several pages in this folder are being edited by other lanes; every quotation is of the snapshot text. |

**Counts:** COUNTS-PLACEHOLDER

Citation form: `ABBREV:line`, where the abbreviation stands for a page path relative to
`FFXII TZA/24-Compiler-And-CRT-Runtime/`. Line numbers are those of the snapshot file.

| abbrev. | page | lines |
|---|---|---:|
| `README` | `README.md` | 64 |
| `SI` | `Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md` | 950 |
| `LZ` | `Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md` | 808 |
| `ST` | `Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md` | 298 |
| `EH` | `Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md` | 1,063 |
| `OBJ` | `Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md` | 1,126 |
| `OC` | `Cxx-Runtime-Families/the-ordered-container-runtime.md` | 594 |
| `MS` | `Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md` | 393 |
| `GEN` | `Generated-Families/generated-function-families.md` | 315 |
| `RV` | `Generated-Adapters/the-return-value-adapter-family.md` | 498 |
| `MEM` | `Memory-And-Allocation/where-the-games-memory-comes-from.md` | 1,982 |
| `TH` | `Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md` | 824 |
| `RS` | `Runtime-Service-Surface/what-the-game-asks-windows-for.md` | 577 |
| `HARD` | `Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md` | 888 |
| `MATH` | `Maths-Library/the-maths-the-game-runs-on.md` | 897 |

"Not stated" means none of the 15 pages says it. Where a point is made only on a page outside this category
(for example the register `_index/OPEN-QUESTIONS.md`), it is given as a path from `FFXII TZA/` and marked as
outside the audited set.

## Pages read

All 15 `.md` files were read in full (11,277 lines). Member `.tsv` files (and the one `.txt`) were opened only
to confirm layouts and row counts. No item below rests on a `.tsv` alone. Where a `.tsv` disagrees with its
page, that is reported as a contradiction and not resolved.

The category `README` indexes only 5 of the 14 system pages (`README:13-47`): `HARD`, `SI`, `LZ`, `OBJ`, `EH`.
`ST`, `OC`, `MS`, `GEN`, `RV`, `MEM`, `TH`, `RS` and `MATH` are not linked from it.

| page | front matter as the page states it | README / in-body banner that differs |
|---|---|---|
| `SI` | `status: AUDITED` (`SI:4`); `evidence_tier: 1` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 5`, `reopened_count: 1` (`:20`, `:24`) | `README:19` "**DOCUMENTED, tier 1.**"; heading `## 12. REOPENED and corrected 2026-09-02 (fourth pass)` (`SI:807`); body dated to 2026-09-29 (`SI:926`) |
| `LZ` | `status: AUDITED` (`LZ:4`); `evidence_tier: 1`; `last_reviewed: 2026-09-02` (`:18`); `passes: 1` (`:20`) | `README:25` "**DOCUMENTED, tier 1, one falsification pass.**"; body dated to 2026-09-29 (`LZ:783`) |
| `ST` | `status: DOCUMENTED — … (UQ-329), the +0x20 flag (UQ-330) and the atexit-ordering question (UQ-331 …) answered 2026-09-17; the owners of the 224 list heads (UQ-329) and the +0x20 flag (UQ-330) answered 2026-09-17` (`ST:4`; the UQ-329/330 clause is written twice); `last_reviewed: 2026-09-13` (`:11`); `crossref_clean: false` (`:20`) | family rows edited to 2026-10-01 (`ST:46`) |
| `EH` | `status: AUDITED` (`EH:4`); `evidence_tier: 1 (one group of 128 relies on tier 8 for its *identity*, see §8)` (`:6`); `last_reviewed: 2026-09-02` (`:18`); `passes: 1` (`:20`) | `README:43` "**DOCUMENTED, tier 1, one falsification pass.**"; sections dated to 2026-09-29 (`EH:1045`); one update section dated "2026-05-15" (`EH:1019`) |
| `OBJ` | `status: AUDITED` (`OBJ:4`); `last_reviewed: 2026-09-02` (`:19`); `passes: 2` (`:21`); `origin: … 915 functions` (`:26`) | `README:34` "**DOCUMENTED, tier 1, one falsification pass.**"; in-body "`DOCUMENTED`, one falsification pass." (`OBJ:558`) and "`DOCUMENTED`, two falsification passes." (`OBJ:617`); body dated to 2026-09-29 (`OBJ:1092`) |
| `OC` | `status: AUDITED — every register row is closed …` (`OC:4`); `last_reviewed: 2026-09-30` (`:12`); `promoted: 2026-10-01 DOCUMENTED -> AUDITED` (`:20`) | `OC:21` "measured A on this DOCUMENTED page" (2026-09-30); section banner "*Tier 2:" (`OC:593`) vs `evidence_tier: 1` (`OC:6`) |
| `MS` | `status: AUDITED — every register row is closed …` (`MS:4`); `readiness: BEHAVIORALLY UNDERSTOOD (2026-09-30, OPUS)` (`:5`); `last_reviewed: 2026-09-30` (`:20`); `promoted: 2026-10-01` (`:28`) | `MS:9` "Was, 2026-09-15: SEMANTICALLY IDENTIFIED … superseded by SD-80"; "*Tier 2:" (`MS:393`) |
| `GEN` | `status: DOCUMENTED — the fifty-five families are catalogued and every register row is closed …` (`GEN:4`); `last_reviewed: 2026-09-29` (`:11`); `last_pass: 2026-09-13` (`:14`); `crossref_clean: false` (`:20`) | rows edited 2026-09-30 / 2026-10-01 (e.g. `GEN:24`, `:31`) |
| `RV` | `status: AUDITED` (`RV:4`); `last_reviewed: 2026-09-08` (`:19`); `last_pass: 2026-09-13` (`:22`) | no `promoted:` line, unlike `OC:20`/`MS:28`; body dated to 2026-10-02 (`RV:212`) |
| `MEM` | `status: REOPENED` (`MEM:4`); `last_reviewed: 2026-09-12` (`:18`); `passes: 1`, `reopened_count: 0` (`:20`, `:24`); `crossref_clean: false` (`:23`); `external_production: … date: 2026-09-23 … status: "locally validated; formal independent acceptance pending"` (`:25-29`) | "Historical audit receipts above do not certify this new production." (`MEM:1901`); body dated to 2026-10-02 (`MEM:1509`) |
| `TH` | `status: AUDITED — BU-1 closed 2026-09-18 as NO ADMISSIBLE SOURCE …` (`TH:4`); `last_reviewed: 2026-09-13` (`:19`); `passes: 3`, `last_pass: 2026-09-03` (`:21-22`) | TH-ROW-PLACEHOLDER |
| `RS` | `status: AUDITED` (`RS:4`); `last_reviewed: 2026-09-07` (`:19`); `passes: 1`, `last_pass: 2026-09-07`, `last_pass_kind: attack` (`:21-24`) | RS-ROW-PLACEHOLDER |
| `HARD` | `status: AUDITED` (`HARD:4`); `last_reviewed: 2026-09-07` (`:19`); `passes: 2`, `reopened_count: 1` (`:21`, `:25`); `last_pass_state: b57264ba…` (`:23`), which is `MATH`'s snapshot hash (`MATH:16`), not `HARD`'s own `46f02e26…` (`HARD:9`) | `README:14` "**DOCUMENTED, tier 1.**"; body dated to 2026-09-29 (`HARD:870`); family row edited 2026-09-30 (`HARD:27`) |
| `MATH` | `status: AUDITED` (`MATH:4`); `last_reviewed: 2026-09-12` (`:18`); `last_pass: 2026-09-07` (`:21`) | "`status` unchanged at **DOCUMENTED**" (`MATH:778`); body dated to 2026-09-29 (`MATH:862`) |
| `README` | "Functions \| ~5,150" (`README:8`) | indexes 5 of 14 pages (`README:13-47`) |

