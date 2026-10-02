# Consumer check: 99-Residual contradictions from a cloud reconstruction-readiness map, settled at the bytes (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-99-VALUES-1002. The cloud map `cloud-reports/re-readiness/99-residual.md` was written without the executable. A local read-only pass decided its 67 value items and 58 stale items at the shipping image and the shipped archive, and OPUS re-checked a sample (`residual_check.py`); OPUS corrected one deciding offset itself (the `"sum_"` load is `0020AC30`+0xFA, not +0xF3). Among the corrections: the nine-patch flag index is inverted; `0020E600` and `00229E40` are a resolver and a getter, not yields; `002B2150` measures and does not draw; several caller counts; the sidecar corpus is 337 files, not 674. Regenerate request (OPUS's own generator): `Unlisted-Code/referenced-unlisted-blocks.tsv` header 129 -> 121.

The pass drafted 178 edits (`apply_99residual.py`). OPUS applies the 110 on its own lines (`apply_by_owner.py OPUS`).

- 9 go to FABLE (`apply_by_owner.py FABLE`).
- 1 go to SWE2-FRONTIER (`apply_by_owner.py FRONTIER`).
- 24 held (`apply_by_owner.py OPUS-HELD`): another lane's uncommitted work sits on the page; applied after it publishes.
- 1 go to SWE2-DATA (`apply_by_owner.py SWE2-DATA`).
- 28 go to SWE2-EC7 (`apply_by_owner.py SWE2-EC7`).
- 5 go to SWE2-FRONTIER (`apply_by_owner.py SWE2-FRONTIER`).

- **Affected:** 99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md, 99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md, 99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md, 99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md, 99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md, 99-Unresolved-Residual/Glyph-Run-Rendering/the-font-painters-public-api.md, 99-Unresolved-Residual/README.md, 99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md, 99-Unresolved-Residual/Unlisted-Code/the-bodies-the-list-cuts-short.md, 99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md, 99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md, 99-Unresolved-Residual/drawing-one-coloured-rectangle.md, 99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md, 99-Unresolved-Residual/the-second-icon-drawer-and-what-it-adds.md, 99-Unresolved-Residual/the-unresolved-158.md, 99-Unresolved-Residual/the-widget-background-and-its-atlas-sets.md, 99-Unresolved-Residual/the-widget-tree-draw-pass.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the OPUS-led pages listed above (OPUS lines) | revised-here |
  | cutscene-name-slots-and-the-depth-of-field-sidecar.md, how-a-line-of-text-becomes-glyph-quads.md, the-shared-drawing-context.md, the-unresolved-158.md, the-widget-tree-draw-pass.md | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 9 edits) |
  | the-code-the-function-list-does-not-contain.md | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 1 edits) |
  | the-largest-unclassified-functions.md, the-text-element-dispatch-table.md | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 24 edits) |
  | measuring-text-by-drawing-it-with-the-output-off.md | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 1 edits) |
  | cutscene-name-slots-and-the-depth-of-field-sidecar.md, drawing-a-line-character-by-character.md, the-blinking-icon-and-its-atlas.md, the-box-renderer-that-is-never-called.md, the-code-the-function-list-does-not-contain.md, the-font-painters-public-api.md, the-nine-patch-window-frame.md, why-the-unow | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 28 edits) |
  | how-a-line-of-text-becomes-glyph-quads.md, painting-a-line-of-text-into-a-render-target.md | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 5 edits) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-residual-readiness-fixes-1002/residual_check.py, verified at f4da4b816: 12 instructions decode as cited, FAILS 0 ([`residual_check.out`](residual_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (110), FAILS 0.

**Pass-22 neighbours.** Other layers' functions in NEW text are named by role or ledger name; `check_page_neighbours.py` shows no new hit on any edited page.
