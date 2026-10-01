# Consumer check: falsification pass 1 on an-effect-element-frame-by-frame (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md (sections 1, 3 and 4: CON-179)
corrects: 17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md (UQ-206 item 4 and the completion clause: CON-179)

## What was corrected

- **Type `0x00` spawns children with no cull.** The update dispatcher `002F3910` sends it to the base `002F2530` alone.
  The type byte is the definition's `+0x44` (`002F30F2`). With it zero, the base runs `002F3890` and `003A8950(2)` at
  `002F2C76`, and the base never calls `005002E0`. The page's "only for elements that passed the cull" now holds only
  for the nine types with a tail.
- **Two ends, not one.** Trigger 3 plus the release also runs from floor arm 2's height exit (`002F2A5F` to
  `002F2D37`..`002F2D52`), not only from the lifetime arm.
- **`0044B960` advances the render-local stream five steps, not four.** Five recurrence blocks precede its single store at
  `0044BA00`.
- **Counts.** Section 4 has six tails, not seven. The method's ten are nine tails plus the shared helper `0044B960`, which
  has 48 direct call sites.
- **The dispatch page's two release labels.** `002F3890` is the history shift and colour copy, and it releases nothing.
  The 394-byte body is the spawn-slot routine `003A8950`. The release is `002F31C0`.
- **What survives.**
  - All nineteen sizes.
  - The fork in all nine tails, and the `+0x49` percent test absent only in `0x05`.
  - The cull test's record choice, its two distance modes and the screen window.
  - The release's list surgery.
  - The eight spawn slots and their tag rules.
  - The motion-aligned builder.
  - Mode 3 and mode 6, and the round-ups.
  - The delayed colour time and the degree-tenths factor.
  - The 32-entry trail history.
  - The half-rate test.

## Current consumers

- consumer: `17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md`: revised-here (item 4 and
  the completion clause of the UQ-206 answer).
- consumer: `_index/OPEN-QUESTIONS.md` UQ-206 repeats "released (`002F3890`) and completed with kind 2";
  routed-to-SWE2-DATA, which holds that file's claim (`SWE2-DATA-UQ218-MOTION-RESIDUE`). The row needs the same
  replacement as the dispatch page.
- consumer: `17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md` calls `0044B960` step-only and
  gives no step count; it agrees.
- consumer: `21-RNG-And-Determinism/rng-streams.md` states the recurrence and counts other helpers' steps, not this one's;
  it agrees.
- consumer: `04-Actor-Entity/the-field-runtime-pass.md` (the SWE2-EC7-47 note) says "repeated" chains without a count;
  it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-179`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_effect_element.py`, rows E10 to E15. Each row fails unless:
- E14: the dispatcher sends type `0x00` to `002F2530` alone;
- E11: the base's trigger-2 site at `002F2C76` sits behind the zero-type test, with no `005002E0` call in the base;
- E12: both trigger-3 + release pairs are present;
- E10: `0044B960` holds five recurrence blocks before its one store;
- E15: `002F3890` calls only the two transform helpers and the cookie check, and touches no list field.

run: verified at ae0885d2e (BROKEN 0, exit 0), against the certified image `73461d08…`.
