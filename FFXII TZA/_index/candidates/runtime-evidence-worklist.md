# Runtime evidence the verdicts have not judged: a worklist (OPUS, 2026-09-25)

**Instrument:** `Tools/analysis-kit/gfz-scripts/runtime_evidence_worklist.py`. **Output:**
`runtime-evidence-worklist.tsv`. **It scores nothing.** Runtime cells are the scorer's.

**Why.** The goal gate's first NOT-MET row is S-02, and its only gap is `runtime`. The verdict text
said *"the exercised body is one function of three pages"* while EXP-191 had already executed the
other two (`s02-runtime-rejudged-against-exp191.md`). This tool asks the same question of every row.

**Method.** A system's contracts come from `_index/important-subsystems.tsv` (`contracts`), plus the
verdict row's contract cell. Its experiments are:

- the EXP ids cited in those contracts;
- the EXP records whose header names one of them.

An experiment is **judged** when its id appears in the verdict row or in any L2-VERDICTS section headed
by that system id. Otherwise it is **unjudged**. No dates are used, because a row's blame date moves
whenever any cell changes.

**Control:** S-02 lists EXP-191 as unjudged, which is the case found by hand.

**Result (at the time of writing):**

- 49 runtime cells are not MET;
- **37 of them have executed records their verdict never mentions — 120 records in all.**

Largest:

| system | runtime cell | unjudged records |
|---|---|---|
| S-14 battle-unit construction | PARTIAL | 17: EXP-047, 150–161, 192–195 |
| S-38 character rendering | NOT MET | 13: EXP-108–128 range |
| S-20 command commit | NOT MET | 7 |
| S-48 authored ramp channels | NOT MET | 7 |
| S-09, S-24, S-32 | LIVE / NOT MET / NOT MET | 6 each |

The TSV has every row.

**Markers, not classes.** `live` means the record says `live_game: true`. `no-stub` means the record
text does not mention stubs, scripted or intercepted boundaries. That is a hint for the table's
no-stub qualifier (S-10 MET vs S-01 MIXED), not a classification. The scorer reads the record.

**Bounds.**

- A contract can cite an experiment for a side point, so "linked" means "worth reading", not
  "covers this system".
- Experiments that name neither a registry contract nor a contract of the row are invisible here.
