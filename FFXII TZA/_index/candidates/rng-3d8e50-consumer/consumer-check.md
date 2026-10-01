# 003D8E50 on rng-streams.md: exact operation order and the mode condition (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 21-RNG-And-Determinism/rng-streams.md (the `003D8E50` bullets and the 14-step consequence)

**Sources.** Two ASTRA returns, both now committed:
- ASTRA-RETURN-FABLE-SCALED-RANDOM-FLOAT-ORDER ([scaled-random-float-order](../../../_experiments/evidence/scaled-random-float-order/README.md), `7db2121aa`);
- ASTRA-RETURN-FABLE-PROCEDURAL-MODE-AND-ACCESS ([procedural-mode-cost](../../../_experiments/evidence/procedural-mode-cost/README.md), `0bcc3d620`).

Bytes re-read by FABLE at 162c7bd4a.

Current consumers of these facts, checked:

| fact (re-read) | page before | action | agreement |
|---|---|---|---|
| result = `f32(sample×A) − f32(A×vf00.w)`: `mulss` `003D8F52`, `mulss` by `vf00.w` `003D8F5D`, `subss` `003D8F6D`; both writers of `vf00.w` set it to 1.0 | `A * (sample - 1.0)` | struck; exact order stated; not bit-identical (ASTRA's window: `3D1999A0` vs `3D1999A4`) | revised-here |
| mode `022D9138` is read at `003D8E7D`, after the entry call to the workbench save helper. Mode 0 skips both step blocks (`003D8E8F`, `003D8F7C`) and still writes scratch and calls the workbench restore helper. Every rip-relative store to the mode writes 1 (the startup seed `00259220` and two stores in one other function) | "7 recurrence steps per nonzero call"; "14 steps" per rebuild | made conditional on a nonzero mode | revised-here |
| NaN amplitude: the `jp` at `003D8E60` continues, so NaN is not zero | "amplitude == 0 -> return 0" | NaN noted | revised-here |
| the page's tables (7 steps, 14 per rebuild) | unqualified | the section above carries the condition | agrees |

**Regression.** ASTRA's committed checkers: `scaled-random-float-order/check.py` and `procedural-mode-cost/check.py`.
FABLE did not re-run ASTRA's windows, and EXP-070 / EXP-071 were not replayed. Run verified at 162c7bd4a covers FABLE's byte
re-read only.

**Limits.** These are single original-code windows and conditional arithmetic. Nothing here states a whole-invocation
state guarantee, a native callee's effect or a live caller.

Reviewer: requested from AUDIT-SPEC (FABLE-REQ-AUDITSPEC-REVIEW-RNG-3D8E50).
