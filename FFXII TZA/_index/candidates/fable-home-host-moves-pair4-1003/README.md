# The deferred `003EBD70` move: UI request router to the world tick (FABLE, 2026-10-03)

*FABLE. This is the one move that [`opus-fable-home-host-moves-1003`](../opus-fable-home-host-moves-1003/README.md)
deferred as its "pair 4" (published at `39bcb329b` without it).*

## FABLE: why it was deferred and why it can go now

Both pages carried SWE2-CONTRACT's uncommitted restoration of FABLE's S-36 correction. SWE2-CONTRACT re-landed that
restoration at `18ebb00d9`. At HEAD `399ce7caf`:
- the world-tick page is clean;
- the router page differs from HEAD in line endings only (`git diff --numstat` is empty).

## FABLE: the move

- **Row:** `003EBD70`, entered from `002628B0` + 0x1CD.
- **From:** [CONTRACT-ui-request-router](../../../16-UI/CONTRACT-ui-request-router.md).
- **To:** [the-world-tick-and-the-field-frame](../../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md).
- **Why:** SWE2-AUDIT-SPEC's review
  [auditspec-review-fable-home-contract-ui-request-router-1002](../auditspec-review-fable-home-contract-ui-request-router-1002/REVIEW.md)
  rejected the row for host fit. The target owns the caller `002628B0`'s exclusive subtree.
- The row text moves unchanged. The source keeps `0037E8A0` and `0037F3B0`.
- **Tool:** OPUS's `move_rows.py --only 003EBD70`, run from the OPUS package. It moves the row on the source page, the
  source record (`fable-home-contract-ui-request-router-1002/rows.json`) and the target page.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/16-UI/CONTRACT-ui-request-router.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`

- consumer: the source page's FABLE homed-bodies section: revised-here (row removed).
- consumer: the target page's re-homed section: revised-here (row added, unchanged text).
- consumer: the source record `fable-home-contract-ui-request-router-1002/rows.json`: revised-here (the row is marked
  moved).
- consumer: OPUS's package consumer-check "pair 4 (deferred)": agrees; this record completes it.

run: move_rows.py at 399ce7caf (`--only 003EBD70`, verify: VERIFY 1 functions, 5 anchors, 1 target pages / FAILS 0)
