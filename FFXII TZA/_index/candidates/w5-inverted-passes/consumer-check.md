# Affected-consumer check: W-5's 2026-09-17 selector clause corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md (the W-5 box, section 7)

run: w5_inverted.py at 63e642d15 (worktree = that HEAD plus this record), 6 checks, FAILS 0. V2 is the check that
measures the correction.

**The change.** The narrowing said the FXAA and motion-blur selectors (`0065A640`, `00659C20`) "branch on a byte
argument and a call result instead" of the descriptor bit. That is wrong: both test bit 1 of the bound target
descriptor's `+0xC` dword, at `0065A888` and `00659DE4`, exactly as the atmosphere, cel and material selectors do. The
clause is struck in place with a dated correction note. The rest of the narrowing stands.

| consumer | what it says | state |
|---|---|---|
| the W-5 box on the reflected-render-parameters page | the struck clause | revised-here (struck, dated correction note) |
| the W-5 register row's status | the same clause, inside the 2026-09-17 status | revised-here: the new status states the correction first; the old status is kept as history, unedited |
| `22-Middleware-PhyreEngine/Post-Process-Chain/the-phyre-post-effect-class-family.md` | "*Not claimed:* ... what the `*Inverted` / `*Tiled` variants ... are for" | agrees (states no selector mechanism; the W-5 record now answers the `*Inverted` half) |
| `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md` | lists `RenderFXAAInverted`, `RenderCameraMotionBlurInverted` and the others as registered names; "whether `PFXAA` is ever instantiated at runtime" not claimed | agrees (names only; the W-5 record's construction path is static and does not contradict the runtime disclaimer) |
| `members/render-pass-registry-60.tsv`, `members/runtime-render-pass-registry.tsv` | the name objects and their initializers | agrees (V1 re-reads the same objects and initializers) |

No other page states how the FXAA or motion-blur selector chooses its variant (grep of `0065A640`, `00659C20` and
"call result" across the database, 2026-09-27).
