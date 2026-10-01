# Consumer check: falsification pass 1 on how-a-camera-reaches-the-renderer (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md (section 4a's script side; the note on 00229D20: CON-184)

## What was corrected

- **A third start form.** `camerashakestart_1a2` (`01A2`) has its own handler `003492F0`, which pops the draw from the
  script. `003DD230` maps only a negative draw. So "script shakes always apply to draw 0" is a property of the `1a3` /
  `019C` forms and of the shipped scripts, which never call `1a2`. It is not a property of the mechanism.
- **`00229D20` is the aspect ratio**, as section 3 says: 4/3, or the device's own value through `00182EE0`. It is
  passed to the projections as their aspect. The appended note's "speed-mode factor" and "authored answer" are
  replaced.
- **What survives.**
  - All 38 sizes, and the caller sets with their priorities `0x14` / `0x14` / `0x64`.
  - The eight-slot submit, and the strictly-greater, earliest-wins arbitration.
  - The constants 0.7854, 1.7778, 1.1547 and 1000.
  - The shake gate order.
  - The MT thunk's nine sites, all in the sampler.
  - The five-slot loop.
  - The loader's rejections and per-draw word.
  - The `1a3` / `019C` forms.

## Current consumers

- consumer: `21-RNG-And-Determinism/CONTRACT-gameplay-generators.md` counts the shake sampler's draws and says nothing
  about which draw a shake applies to; it needs no change.
- consumer: `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv` already lists `01A2` with handler
  `003492F0` and three pops; it agrees.
- consumer: `17-Presentation-Rendering/Scripted-Camera/members/camerashake_census.py` counts every `camerashake*` verb and
  finds no `1a2` call; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-184`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_camera_renderer.py` W11 and W12. W11 fails unless
`003492F0` pops the draw without pushing -1, and `003DD230` holds no compare on a non-negative draw. W12 fails unless
`00229D20`'s other path tail-calls `00182EE0` into the device object.

run: verified at f85ed4623 (BROKEN 0, exit 0), against the certified image `73461d08…`.
