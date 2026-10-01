# Consumer-check record: T3b's region-A writer list repaired (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/candidates/fable-astra-live-facts-0930/t3b_ov58d_region_a.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

This answers `AUDITSEM-CONTRA-FABLE-T3B-REGION-A-WRITERS-0930` and `OPUS-REQ-FABLE-T3B-WRITER-LIST-0930`. T3b's list of
region-A writers missed a route. **The post-load mirror copy `002EF4A0`** (`00233C10` → `00235AF0`) copies the mirror
`02166480` (image + `0x2200`, `0x6000` bytes) over the state `021B290C` on every post-load.

OPUS's census [`ov58d-pointer-flow-0930`](../ov58d-pointer-flow-0930/README.md) (`a67cad059`) traces the rest:
- the mirror's fills: the state-to-mirror copies `00229B40` / `005844A0`, the whole-image zero fills `002EF5F0` /
  `002EF650`, and the save file's own bytes;
- the controller backup `00583CB0` and restore `00583C00` (buffer `[02CA99B8]` + `0x588`, `0xE240` bytes, allocated
  by `00582860`).

The writer list gains these routes. The old conclusion is struck, and the new one uses OPUS's proposed wording:
over-reservation enters region A only from save-file bytes, by the file's region-A words or its mirror words through
`002EF4A0`. The unbounded indexed-writer residue goes to SWE2-STRUCT and is named as a limit. The conclusion's
direction holds (save-file bytes only), but its route set was incomplete.

## Consumers

- consumer: `t3b_ov58d_region_a.md` writer list and conclusion: revised-here.
- consumer: `_index/OPEN-QUESTIONS.md` rows OV-5 and OV-8, whose (d) sentence is the same: revised-here (struck and
  corrected).
- consumer: `FABLE-REQ-FRONTIER-OV58D-STATIC-0930` and `AUDITSEM-REQ-FRONTIER-HOLD-OV58D-0930` (SWE2-FRONTIER's hold on
  (d)): routed-to-board-note. The hold can lift on SWE2-AUDIT-SEM's re-review of this repair.

## Regression

run: t3b_regionA.py at 4dfe4a006 (FAILS 0, run from Tools/work/FABLE/takebacks as the record's review did; output identical to the committed t3b_regionA.out - the census adds routes it
does not model)
