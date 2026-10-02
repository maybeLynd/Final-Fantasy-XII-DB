# Consumer check: 17-Render contradictions (part B) from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-17-VALUES-1002, part B. Cloud wave 5 mapped `17-Presentation-Rendering/` from a text
snapshot (session `session_01Bf11Bg4ubT2fxuBZvpWtqD`; report `cloud-reports/re-readiness/17-render.md` in
maybeLynd/Final-Fantasy-XII-DB; rated NOT YET). Its value items were page-text only. A local read-only pass took the
106 items in report lines 2800-3212 (GP.CV-10 .. CM.CV-23) and decided most of them at the shipping image. Some are
naming questions or were not read. OPUS re-checked a sample (`render_b_check.py`). Report sections 3.2 (counts) and 3.3
(stale and banner items) are not in this pass; the task stays open for them.

Corrected at the bytes, on OPUS's lines:
- the texture page budget subtracts both runtime totals before the page mask (`00467AA0+0x17`, `+0x23`), so 176 pages
  holds only with zero totals;
- the published maximum is the whole mip chain's footprint (`002F7380+0xBB`);
- `002F2D60+0x44` clears bits 1 and 2 only;
- the floor-probe gate is mask 4, bit 2 (`002F3750+0x2A`);
- draw-list entry `+8` is the sort key (`003A3A50+0x103`);
- step 7's lens is the constant 35.0 at `008F312C` (`00193DA0+0x150`), not `cfg+0x2C`;
- the screen-fade descriptor fields, the issued marker bits and the `0x4B7FFBFF` value.

The pass drafted 126 strike edits (`apply_17render_b.py`). OPUS applies the 33 on its own lines across eleven pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 22 on six OPUS-led pages that carry OPUS's own uncommitted work wait until that work publishes
  (`apply_by_owner.py OPUS-HELD`). Four pages have F-interior sections (fcp, fte-fct, mh, ppfx-function-identification).
  Two have part-A readiness edits (fef, bone trails).
- 44 go to SWE2-EC7.
- 12 go to FABLE.
- 10 go to SWE2-FRONTIER, on FRONTIER's lines.
- 5 go to SWE2-DATA.

- **Affected:** 17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md, 17-Presentation-Rendering/Effect-File-Formats/the-element-types-80-97.md, 17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md, 17-Presentation-Rendering/Model-And-Motion-Formats/README.md, 17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md, 17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md, 17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md, 17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md, 17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md, 17-Presentation-Rendering/Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md, 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the eleven OPUS-led 17 pages (OPUS lines) | revised-here |
  | fcp, fte-fct, mh, ppfx-function-identification, fef and the bone-trail page | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 22 edits) |
  | EC7's dispatch, registry, GI, pose, command-list and camera pages, and its screen-fade lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 44 edits) |
  | the VIF1/VU1, 00-0A, post-processing contract and ten-channel pages, and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 12 edits) |
  | FRONTIER's element-type and oscillator lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 10 edits) |
  | the fdm/for page and DATA's ftr-node-table line | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 5 edits) |
  | RE repo `docs/readiness/17-render.md` | routed-to-OPUS (filed after this publish, with the part-A and part-B byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-render-b-readiness-fixes-1002/render_b_check.py, verified at 813b1f063: 8 instructions decode as cited and `008F312C` holds 35.0, FAILS 0 ([`render_b_check.out`](render_b_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (33), FAILS 0.
