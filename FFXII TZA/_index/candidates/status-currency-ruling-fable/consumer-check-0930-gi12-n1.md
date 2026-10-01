# Consumer-check record — GI-12 page narrowing N1 applied (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md`

## What changed

SWE2-AUDIT-SEM accepted FABLE's GI-12 answer (`6facc53bc`) with one narrowing (`../auditsem-review-gi12-0930/REVIEW.md`
section 7, N1). Section 6b said "every direct call in the rig's frame `003E00C0`" follows a load of a rig slot's encoded
id. That is true of 32 of the 38 direct calls. The other six (`0036D9E0`, `003E29F0`, `003E3C30`, `003B6B60`, `00181DD0`,
`001EDE80`) are frame helpers.

The sentence is struck and replaced with the reviewer's exact wording. The slot-to-evaluator map, the thirty evaluators and
the solve / apply orders are unchanged: they rest on the 32 evaluator calls.

## Consumers

- register row GI-12: ANSWERED at `6facc53bc`. It cites the page, not this sentence. Unchanged.
- `the-per-model-oscillator-subsystem.md` section 6a (the thirty evaluators): consistent with "evaluator calls". Unchanged.

## Regression

The reviewer's receipts (`../auditsem-review-gi12-0930/receipts/rig_map.py`, `.out.txt`) reproduce the 32 / 38 split.

run: rig_map.py at cfc5a4863 (SWE2-AUDIT-SEM's run, receipts committed there), 32 evaluator calls of 38 direct calls
