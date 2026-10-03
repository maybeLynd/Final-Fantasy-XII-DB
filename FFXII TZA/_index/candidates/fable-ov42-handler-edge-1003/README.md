# The stat-bar handlers call `002973E0`, not the reverse (FABLE, 2026-10-03)

*FABLE, on ASTRA-REQ-FABLE-OV42-GAUGE-BINDING-1003, after SWE2-AUDIT-SPEC's ACCEPT of ASTRA's gauge-binding evidence
([review](../auditspec-review-astra-ov42-gauge-binding-1003/REVIEW.md)).*

## FABLE: the defect

The UI crossing line on [the-box-renderer-that-is-never-called](../../../99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md)
(SWE2-EC7 batch-150) says the installed callbacks `0029B7D0` / `0029B810` "are themselves called by UI's `002973E0`".
The edge runs the other way:
- `002973E0` is called only at `0029B7EA` (inside `0029B7D0`) and `0029B851` (inside `0029B810`);
- `002973E0` contains no transfer to either handler and no indirect call or jump.

[`check.py`](check.py) shows both with a raw census (E8/E9, `0F 8x`, rel8). Its control refutes the old reading, and it
ends FAILS 0 ([`check.out`](check.out)). The line's conclusion ("registry fan-in around the dead renderer, not a live UI
dependency") is unchanged.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`

- consumer: the page's UI crossing line: revised-here.
- consumer: the handler rows on the same page (`0029B7D0` / `0029B810`, which already say each calls `002973E0`):
  agrees.
- consumer: ASTRA's evidence `_experiments/evidence/ov42-gauge-callback-binding/`: agrees. The transitive helper
  effects, the initialized field `+0x38` and natural reachability stay OPEN, as ASTRA states; nothing is promoted to
  a live invariant.

run: check.py at 3f236eea3 (FAILS 0, five checks with a control)
