# Consumer check: falsification pass 1 on the-phyre-post-effect-class-family (OPUS, 2026-09-29)

corrects: 22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md (CON-197 slot 1, CON-198 code construction, CON-199 GF-3 overrides, CON-200 0018D0E0, CON-201 state column)
corrects: 22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md (CON-198: the non-SMAA arm of 00191DA0, and PFXAA instantiation)
corrects: 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md (CON-198: the +0x378 subobject)
corrects: _types/types.tsv row PFXAA and _types/fields.tsv row PostProcessParamContext +0x378 (CON-198)

## What was corrected

- **CON-198.** One `PFXAA` is built and run by the game. `0018CD90` (the `PostProcessParamContext` constructor) calls `00645DB0`
  on `context + 0x378`, which stamps the `PFXAA` vtable `00D625D0`. `00191DA0` (on its `+0x4A3 == 0` arm) and `0018FD70` call
  `0065A630` -> `0065A640`, `PFXAA`'s worker, on that member. The other 35 classes and GF-6's asset census are untouched.
  Player terms: with post-AA on and SMAA not chosen, each frame runs PhyreEngine's own FXAA effect, not "a plain copy".
- **CON-197.** Slot 1's 1280 x 720 fallback is unreachable: the context getter returns a static, and `0x520` is added before the
  null test.
- **CON-199.** `PAtmospherics` and `PCelShading` override `0 1 2 6`, not `0 1 2 3 6`.
- **CON-200.** `0018D0E0` has 52 direct call sites; the one-selector conclusion stands on the `_purecall` slot.
- **CON-201.** Section 4b's state column, re-measured under its own definition.

## Current consumers

- consumer: `_index/OPEN-QUESTIONS.md` rows `GF-1` (1280 x 720 fallback), `GF-2` ("nothing in the executable constructs a
  post-effect"), `GF-3` (the leaves override `0 1 2 3 6`), `GF-4` (its withdrawal cites GF-2's "nothing constructs one"; the
  two classes it asks about are still constructed by nothing), `GF-6` ("the executable constructs none of the 37"), `W-4` and
  `EA-7` (the non-SMAA arm as "a plain copy"). These rows are FABLE's; routed to FABLE, **PENDING PROPAGATION** for those rows.
- consumer: `22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md`: revised-here.
- consumer: `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md`: revised-here.
  The W-5 consumer record at `_index/candidates/w5-inverted-passes/consumer-check.md` quoted the old "not claimed" line and
  agreed with it; it is history.
- consumer: `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`: revised-here (the second qword
  at `+0x380` is the class descriptor `02D35FA0`, not a vtable).
- consumer: `_types/types.tsv` (`PFXAA`: instance, allocation, ctor, route) and `_types/fields.tsv` (`PostProcessParamContext`
  `+0x378` now typed `PFXAA`): revised-here.
- consumer: `_index/candidates/gf4-no-instance/consumer-check.md`, `_index/_inbox/FABLE.md` and the retained copy under
  `_experiments/evidence/gf4-caller-preflight/retained/` are history.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-197` to `CON-201`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_posteffect_family.py` P2 (the slot map, and fails if
`PAtmospherics`/`PCelShading` override slot 3), P4 (fails unless `005FD050` returns one static and the add precedes the test),
P7 (fails unless the upward closure of every vtable-stamping body leaves the band at exactly the three `PFXAA` sites), P8
(fails unless both callers of `0065A630` pass `context + 0x378`), P10 (the state column), P12 (52 call sites to `0018D0E0`).

run: verified at 05b858cfa (BROKEN 0, exit 0), against the certified image `73461d08…`.
