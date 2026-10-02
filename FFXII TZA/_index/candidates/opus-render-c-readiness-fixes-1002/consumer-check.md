# Consumer check: 17-Render counts and stale items (part C) from a cloud reconstruction-readiness map, settled at the bytes (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-17-VALUES-1002, part C (report sections 3.2 and 3.3; parts A and B are published). A local read-only pass recounted every count at the image or in the cited TSV and checked each stale item, and OPUS re-checked a sample (`render_c_check.py`). Among the corrections: the status push has 44 non-empty arms (bit 31 is tested, `003E7650`+0x318, +0x580); 36 enqueue builders and four command-object sizes; 42 concrete classes plus the abstract base; 11 factories; 25 untouched device slots; arena sizes 8 to 0x640. Where two figures measure different scopes, the scope is named instead. Regenerate requests: `character-render-record-accesses.tsv` (SWE2-STRUCT) and `members/vif1-gif-tags.tsv` (FABLE).

The pass drafted 279 edits (`apply_17render_c.py`). OPUS applies the 69 on its own lines (`apply_by_owner.py OPUS`).

- 72 go to FABLE (`apply_by_owner.py FABLE`).
- 3 go to SWE2-FRONTIER (`apply_by_owner.py FRONTIER`).
- 12 held (`apply_by_owner.py OPUS-HELD`): another lane's uncommitted work sits on the page; applied after it publishes.
- 22 go to SWE2-DATA (`apply_by_owner.py SWE2-DATA`).
- 101 go to SWE2-EC7 (`apply_by_owner.py SWE2-EC7`).

- **Affected:** 17-Presentation-Rendering/CONTRACT-character-transform-publish.md, 17-Presentation-Rendering/CONTRACT-coast-down-latch.md, 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md, 17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md, 17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md, 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md, 17-Presentation-Rendering/Effect-File-Formats/README.md, 17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md, 17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md, 17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md, 17-Presentation-Rendering/Position-To-Scalar/how-a-position-becomes-a-single-number.md, 17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md, 17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md, 17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md, 17-Presentation-Rendering/Screen-Fade/the-screen-fade-layers-and-the-movie-fade-schedule.md, 17-Presentation-Rendering/Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md, 17-Presentation-Rendering/Visual-Tuning-Parameters/README.md, 17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the OPUS-led pages listed above (OPUS lines) | revised-here |
  | CONTRACT-character-render-object.md, CONTRACT-post-processing-subsystem.md, README.md, add-motion-skeleton-and-high-model-tables.md, an-effect-element-frame-by-frame.md, frp-object-container.md, how-a-character-fades-the-ten-channels.md, how-a-character-is-lit.md, how-a-presentation-entry-picks-its- | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 72 edits) |
  | README.md, the-per-model-oscillator-subsystem.md, the-screen-fade-layers-and-the-movie-fade-schedule.md | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER`, 3 edits) |
  | character-render-object.md | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 12 edits) |
  | README.md, effect-mesh-records-kind-54.md, fcp-character-parameter-block.md, fdm-and-for-entries.md, fef-and-motion-entries.md, fte-fct-texture-colour-tables.md, the-character-render-record-array.md | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 22 edits) |
  | CONTRACT-authored-command-ramp-channels.md, CONTRACT-render-record-pool-lifecycle.md, adm-add-motion-tables.md, effect-element-type-dispatch.md, gi-render-command-family.md, how-a-camera-reaches-the-renderer.md, mh-movie-seek-index.md, the-menu-effect-registry.md, the-ordered-render-command-list.md, | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 101 edits) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-render-c-readiness-fixes-1002/render_c_check.py, verified at f4da4b816: 9 instructions decode as cited, FAILS 0 ([`render_c_check.out`](render_c_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (69), FAILS 0.

**Pass-22 neighbours.** Other layers' functions in NEW text are named by role or ledger name; `check_page_neighbours.py` shows no new hit on any edited page.
