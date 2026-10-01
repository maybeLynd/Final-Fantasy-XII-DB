# Consumer check: falsification pass 1 on fef-and-motion-entries (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md (the @FEF external-name section, the residue, the frontmatter note: CON-195)
corrects: 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md (the 0041E3A0 arms table: CON-196)
corrects: 02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md (the OV-39 box: CON-195, added 2026-09-29)

## What was corrected

- **CON-195.** The name table `02B64380` is seeded at start-up: `0041E3A0` -> `00409F80` -> `0040A230`, all direct calls on the
  chain from `0017D000` through the boot fixups `0022A0B0`. All 144 seeded `obj_finish` paths are entries of the installed
  archive. "Dead-stripped, NULL, would fault, vestigial" no longer follows. Whether a shipped session reaches the arm is not
  observed.
- **CON-196.** The populator stores `.rdata` path strings, not `.text` function pointers.

## Current consumers

- consumer: `_index/OPEN-QUESTIONS.md` row `UQ-218` repeats "dead-stripped ... NULL ... vestigial". That row is FABLE /
  SWE2-DATA's (PARTIAL, under active work); routed to them, **PENDING PROPAGATION** for that row.
- consumer: `_index/AUDIT-LOG.md` (SWE2-DATA, UQ-218 pass 13) is history; the correction is recorded here and in the row.
- consumer: `_index/candidates/ov39-fef-producers-fable/README.md` ~~names the table as a configuration table indexed by the
  name; it agrees.~~ **Corrected 2026-09-29 (OPUS): it does not agree - its row "optional configuration" says the table is
  never populated and `0040A230` dead-stripped. The record is history; the claim it carried is corrected where it was
  repeated:**
  - consumer: `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md` (the OV-39
    box): revised-here at the nonempty-PRF falsification pass (`falsify_nonempty_prf.py` R6).
  - consumer: `_index/OPEN-QUESTIONS.md` row `OV-39` repeats "never populated"; FABLE's row, routed as
    OPUS-NOTICE-FABLE-OV39-ROW-CON195-0929, **PENDING PROPAGATION** for that row.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-195`, `CON-196`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_fef_entries.py` F3 (fails unless each link of the start-up
chain is a direct `rel32` call and `00409F84` calls `0040A230`), F4 (144 obj_finish paths, all in the installed archive),
F5 (every stored value in `.rdata`).

run: verified at 5c7b4baeb (BROKEN 0, exit 0), against the certified image `73461d08…` and the installed archive header `c9e1f530…`.

run (R6, the OV-39 consumer): verified at 3754d9b4d (falsify_nonempty_prf.py BROKEN 0, exit 0).
