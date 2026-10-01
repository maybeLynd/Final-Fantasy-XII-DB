# Consumer-check record — GI-12 answer and the display-deny correction (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (row GI-12)

## The correction

The rig page, section 5, said the status-error display-deny gate at `003E0680` skips "the last two applies -
Immobilize and Confuse". The frame skips the last **three**: Immobilize, Confuse and the Float bob's apply
`004717E0` (controller 6, behind the bob's running byte `+3`). The apply list on that page also stopped at
controller 3 and gains controller 6. The old words are struck on the page, with the correction beside them.

## Consumers (grep of `003E0680`, `02B59D68` and "display-deny" over the database)

- the rig page, section 5: corrected in this publish;
- the oscillator page: section 6b states the three-apply reading, and its data table names `02B59D68` as the latch;
- register row GI-12: states the correction;
- `how-a-position-becomes-a-single-number.md` section 12 and `how-a-status-shows-on-a-character.md` name the latch and
  its writer only; neither states how many applies it skips. They agree and are unchanged;
- the rig page's falsification row R4 tests only that `02B59D68` is read at `003E0680`. It agrees and is unchanged.

Other GI-12 statements are additions (the map wind, the evaluator slots, `02B59D60` never written, the `0x72`
callers, the reset read whole); the data-table cells that gained a meaning keep their old wording.

## Regression

`oscillator_gi12.py` (this folder; its output `oscillator_gi12.out`) check C1 lists the applies
behind the gate and fails unless they are controllers 7, 3 and 6; the old two-apply reading fails it. C2 to C5 carry
the additions, each with a positive control. Result at `dcdd159f0`: C1 to C5 pass, FAILS 0.

run: oscillator_gi12.py at dcdd159f0 (HEAD when it ran), C1 to C5 pass, FAILS 0 (output: oscillator_gi12.out)
