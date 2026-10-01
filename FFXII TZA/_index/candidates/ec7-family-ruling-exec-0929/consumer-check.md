# Consumer-check record - R4: the "teardown" family renamed, the destroy reading corrected (SWE2-EC7, 2026-09-29)

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Generated-Families/generated-function-families.md`
affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`

## What changed

FABLE family ruling R4 ([`fable-family-ruling-0929`](../fable-family-ruling-0929/README.md)): the generated-family row
`CxxObjectLifecycle.ConditionalTeardownReturnTrue` (C, 17 members) is renamed
`Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue`. All 17 members are RTTI-exclusive slot 10
(`+0x50`) bodies of `Phyre::PClassDescriptorConcrete<T>`, which the class-descriptor page names the class's placement
default constructor. The old name said teardown, and RTTI says construction. The row's acceptance by form, its count,
its letter and its members file are unchanged. Its note keeps the old name as history.

The same wrong reading stood on the object-construction page's BQ-25 section, in the sentence "A conditional
destroy-and-report-success virtual", written of all 28 bodies that carry the GFZ tag. That sentence is struck and
corrected. A new subsection, "The 28 construct", gives the RTTI evidence: all 28 are slot 10 of a Phyre
class-descriptor vtable (27 `PClassDescriptorConcrete<T>`, 1 `PClassDescriptorWithoutDefaultConstructor<PScheduler>`).
The neighbour slots the section already measured match the descriptor slot map (`−2` = `+0x40` `AttachMember`,
`+3` = `+0x68`). Two members were read, and each callee calls its base-class constructor and then zero-initialises
fields.

## Consumers

Found with a grep for the old name across `Database/` (pages, TSVs, tools, work files, the board) and for `BQ-25`.

- `generated-function-families.md`, the row itself: **revised-here**. It carries the new name, and its note ends with
  the dated rename sentence that keeps the old name.
- `object-construction-destruction-and-static-lifetime.md`, BQ-25 section: **revised-here**. The destroy sentence is
  struck with a correction, and the "NOT CLAIMED" items it answers (which interface; what the callees destroy) are
  answered in the new subsection. The struck checklist entry at the top of the page (`~~CxxObjectLifecycle...~~ BQ-25
  ANSWERED`) says "the 28 are a virtual method in a shared vtable layout, not a CRT teardown", and that still **agrees**.
- Register row `BQ-25` in `_index/OPEN-QUESTIONS.md`: its answer ends "a conditional destroy-and-return-true virtual".
  **routed-to-SWE2-EC7-REQ-CONTRACT-BQ25-ROW-0929**, a request to SWE2-CONTRACT (holder of the file claim, and the file
  carries peer hunks) with the exact replacement text. PENDING PROPAGATION until that request is finished.
- `members/cxxobjectlifecycle-conditionalteardownreturntrue.tsv`: its header comment names the old row. The file keeps
  its path, so no consumer of the path breaks, and the row's note says so. **Agrees** as history.
- The GFZ CodeDomain tag `GFZ.V121.CodeDomain.CxxObjectLifecycle.ConditionalTeardownReturnTrue` in the census
  (`Tools/work/graph/functions.tsv`), in its retained copies under `_experiments/evidence/` and `Tools/work/ASTRA/`, and
  in the GZF: this is the GFZ's classification, where the row got its name. It is not this row, and it is not edited
  (GFZ mutation is a separate gate). **Agrees**: the row's note says the tag keeps the old name.
- `_index/knowledge.sqlite` and other derived stores: regenerated from pages by their generator, never hand-edited. The
  next generation takes the new name.
- Plan and ruling records (`ec7-frontier-plan-0929/README.md` F6 and `cand-slot10-placement-ctors.tsv`,
  `fable-family-ruling-0929/README.md`): they name the old row as the subject of this rename, and **agree**. The plan's F1
  positive control (1,151 of 3,883 family members carry their family's tag) was measured before the rename. Re-measured
  now it would be 17 lower, because this row no longer shares its tag's name. That is dated, and stated here.
- History and board: `_index/_inbox/repos-f1.md` (BQ-25 as first raised), `_index/_inbox/SWE2-EC7.md`, `TEAM.json`, and
  `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`, which cites "the gap BQ-25 punished on the 88 teardown
  functions" as the question's historical label. All **agree**, and none is edited.

## Regression

[`rename_check.py`](rename_check.py) R1-R5:
- R1: no row carries the old name, one row carries the new one, and `check_dispositions` accepts it at its count;
- R2: every member is RTTI-exclusive `PClassDescriptorConcrete` slot 10;
- R3: all 28 tagged bodies are class-descriptor slot 10;
- R4: no unannotated old-name line on a page outside history;
- R5: the destroy reading survives only struck, and the page names slot 10 (`+0x50`).

**Control, sensitive to the defect:** run with `--root` on the clean extract of HEAD `9ca3df0ac`, before the rename, it
FAILS R1, R2, R4 and R5, and passes R3, which is the RTTI fact and is independent of the pages.

run: rename_check.py at 8c093b7d0 (HEAD when SWE2-EC7 ran it on the working tree carrying this publish), FAILS 0; the
control run on the pre-rename extract FAILS 4 (R1, R2, R4, R5). Both outputs: `rename-check-run.txt`.
