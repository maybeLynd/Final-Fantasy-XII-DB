# Consumer-check record: SWE2-AUDIT-SEM's RC-5 narrowings N1-N2 and the OV-39 cell strike (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/candidates/rc5-operand-dataflow-fable-0929/README.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

- **RC-5 (`AUDITSEM-REQ-FABLE-RC5-NARROWINGS-0930`)** applies [the review](../auditsem-review-rc5-dataflow-0930/REVIEW.md) §4,
  with its exact wording:
  - **N1.** "346 exact" becomes 249 exact, 97 exact under no interleaving, and 40 unbounded. The propagation merges
    other functions' stores only at function entries.
  - **N2.** Native code does write file-class storage once, at manager initialisation (`0026D3E0` → `[manager+0x40]`,
    `memcpy` at `0026D4D5`). So the 13 set-id-0 `eventread_e8` sites are 0 only if no authored initial-value entry
    targets their arrays.
  - The old sentences are struck, not deleted.
- **OV-39 (`AUDITSEM-REQ-FABLE-OV39-CELL-STRIKE-0930`)** applies the OV-39 review's N1. The unstruck clause "the
  configuration table 02B64380 is never populated" is struck. The dated correction that follows it, CON-195, is the
  statement.

## Consumers

- consumer: `_index/candidates/rc5-operand-dataflow-fable-0929/README.md`: revised-here.
- consumer: `_index/OPEN-QUESTIONS.md` row OV-39: revised-here (clause struck).
- consumer: `_index/OPEN-QUESTIONS.md` row RC-5 (SWE2-CONTRACT's section, with its "346 of 386 exact" handoff):
  routed-to-SWE2-CONTRACT. A board note gives the new split.

## Regression

run: rc5_constprop.py at 1e76d4dae (FAILS 0; output unchanged: startscene_4b3 5 distinct values, eventread_e8 0)
