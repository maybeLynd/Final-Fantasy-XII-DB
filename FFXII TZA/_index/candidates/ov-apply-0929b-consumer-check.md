# Consumer-check record: the OV apply batch of 2026-09-29 (SWE2-FRONTIER)

EVIDENCE-POLICY 4a record for the publish that ticks/annotates checklist boxes on the
SECTION-overlay pages and the `+0x17C` timer rename on the applier page.

## Affected

Affected rows: OV-10, OV-14, OV-17, OV-19, OV-26, OV-34, OV-35, OV-36, OV-42 in
`_index/OPEN-QUESTIONS.md`, and the boxes on `the-script-from-bytecode-through-wait-and-resume.md`
(OV-14, OV-17), `the-indexed-source-request-from-arm-to-terminal-pump.md` (OV-34, OV-35, OV-36)
and `applying-a-result-to-a-target.md` (the Q2 `+0x17C` rename staged as
`_index/candidates/pkg-gp-status-poison/applier-q2.patch`). Every struck span quotes the line's own
removed text verbatim; each annotation names its FABLE record.

## Consumers and agreement

The consumer of each box is the register row, and the register agrees row-for-row: each closing
annotation names the FABLE candidate record that carries the evidence (`ov10-request-bounds-fable`,
`ov14-wait-kinds-fable`, `ov17-constant-bounds-fable`, `ov26-frp-bounds-fable`,
`ov34-state1-owner-fable`, `ov35-source-metadata-fable`, `ov36-callback-delivery-fable`,
`ov42-submit-recovery-fable`, `pkg-gp-status-poison/timers.md`). FABLE authored and staged every
record — the producer agrees; the register table and the page checklists are the consumers and are
updated in the same commit. The OV-42 scope is applied as corrected by
FABLE-NOTICE-FRONTIER-OV42-SCOPE: answered at the owner-protocol level only, with the higher-level
arena residue and the runtime question kept open. Rows left OPEN (OV-10 residue, OV-19 residue,
OV-26 residue, OV-42 residues) keep unticked boxes by design.

## Regression

`Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db "Database/FFXII TZA"`: run
after the apply — 0 unticked-boxes-called-ANSWERED, 0 ticked-boxes-called-OPEN, 0 cell-count
mismatches, table and checklists agree. Q2 rename verified: `applier-q2.patch` applied cleanly
against HEAD at apply time (verified by `git apply --check`, rc 0).
