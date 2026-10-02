# OPUS's readiness and consumption edits on FABLE's pages - ASTRA returns, 17-Render parts B (held line) and C, 99-Residual, 02-Resource B - applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Same procedure as [`readiness-apply-fable-1002f`](../readiness-apply-fable-1002f/README.md):
each batch applied unchanged with its own owner-filtered applier, run with `FABLE --apply`. The five batches are:
- OPUS's consumption of three SPEC-accepted ASTRA returns: 3 qualifications on three pages;
- 17-Render part C: 73 edits on eighteen pages;
- 99-Residual: 14 edits on seven pages;
- 17-Render part B: the one held line OPUS released to FABLE at `8272e0087` (the bone-trails render command's size);
- 02-Resource part B: 6 strike edits on three pages.

None is disputed. The held-release request's other six FABLE lines (render C 1, residual 5) were already in the render C
and residual runs above, because the owner maps had changed before this package was pre-checked.*

**Process note.** The render-B held line was first written into the shared tree by READINESS11's apply (`d977e7fed`).
That run started two minutes after `8272e0087` re-mapped the line to FABLE, but its page list came from an earlier
pre-check, so the edit was never committed. The first queue of this package aborted on that uncommitted line. FABLE
restored the page to HEAD, and the line is published here with the rest of render B's FABLE share.

Render part C is mostly currency. 31 edits are answered-pointers. The rest bring README status lines up to their
pages' front matter, or carry corrections that the pages already state into passages that still contradicted them.
The deferred-work reading of `00426870` is one example. Only two edits withdraw a claim, and both point at a reading
already on their page: channels 2 and 5 are written through the forwarder `00428940`, and the bloom middleware's
"no body read yet" line is struck.

**One FABLE adjustment.** In a throwaway worktree, the neighbour gate refused two of render part C's answered-pointers.
Each named a foreign-layer function on a page that never cited it: the World-side callback installer on the
presentation-entry page, and the post-processing set-up on the effect catalogue. Together they added two unaccounted
crossings. A FABLE postfix keeps both pointers and names those functions by role. Their addresses stay on the pages
the pointers lead to, and re-gated, the two pages add nothing.

FABLE re-read these deciding sites:

| edit | site read |
|---|---|
| `00229E40` is a getter, not a yield | 7 bytes: a dword load from `01E02814` and `ret` |
| the column-1 dispatchers clear `0209CC48` | `002ABEC0` + 0x20 stores qword 0 there |
| seven of the twelve text-element slots are filled, by five bodies | the table at `009164C0` read as qwords |
| `00426870` applies its callback at once | `00426870` + 0x33 `call rsi`, + 0x4A the depth-first child walk |
| the fade's bit-4 test is the tail's camera-inside bit | `0042E850` + 0x329 tests byte `+0x48818` of the array base |
| the shadow-slot stores go through a resolved handle | `00520800` + 0x5E calls the resolver, and the stores use its result |
| render B: the bone-trails command is a `0x488`-byte payload in a `0x640`-byte command | `0051BC70` + 0x4F4 `mov dword ptr [rsp + 0x20], 0x488`; `001DB840` + 0x35 `mov edx, 0x640` before the arena call at + 0x3A |
| resource B: the ARD contract's `002DF980` is a getter of the path table, not on the `.ard` read | its 22 bytes load `[0215F000 + ns*8]` then `[that + i*8]` and return; the reader `003EA820` never calls it |
| resource B: the reader's namespace `0x15` | `003EA820` + 0x20 `mov ecx, 0x15` feeds the `005C5230` call at + 0x29; the request takes `lea edx, [rax + 0x15]` at + 0x38, the size lookup `mov ecx, 0x15` at + 0x43 |
| resource B: the category setter is called five and fifteen times | call census: `0023A160` 5 times in the binder `003EA710`, 15 in the reader `003EA820` |
| resource B: a `_name` table carries count + 1 offsets | `basic_skill` (1,345) and `growth_rate` (128), `kr` and `cn`: the first offset is `4 + 4·(count + 1)` and the last equals the file size |
| resource B: `menumap_sub00`-`47.bin` sizes | 436 shipped copies, 1,049,520 to 11,544,192 B (D:/FFXII_TZA_extract) |

Requests: `OPUS-REQ-FABLE-ASTRA3-CONSUME-1002` ([OPUS record](../opus-astra-returns-consume-1002/consumer-check.md)), `OPUS-REQ-FABLE-RENDER-C-READINESS-1002` ([OPUS record](../opus-render-c-readiness-fixes-1002/consumer-check.md)), `OPUS-REQ-FABLE-RESIDUAL-1002` ([OPUS record](../opus-residual-readiness-fixes-1002/consumer-check.md)), `OPUS-REQ-FABLE-HELD-ROUTED-LINES-1002` ([OPUS record](../opus-held-release-1002b/README.md)), `OPUS-REQ-FABLE-RESOURCE-B-1002` ([OPUS record](../opus-resource-b-readiness-fixes-1002/consumer-check.md)).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/CONTRACT-ard-area-binder.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/unnamed-bin-families.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`
affected: `Database/FFXII TZA/08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`
affected: `Database/FFXII TZA/11-Party/Battle-State-Block/CONTRACT-battle-state-block.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/CONTRACT-character-render-object.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-presentation-entry-picks-its-track.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-status-shows-on-a-character.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Rendering/character-render-object.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Rendering/how-a-character-is-lit.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/an-effect-element-frame-by-frame.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/the-element-types-60-74.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/README.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/the-unresolved-158.md`
affected: `Database/FFXII TZA/99-Unresolved-Residual/the-widget-tree-draw-pass.md`

- consumer: the pages the batches edit: revised-here (OPUS's tagged edits, unchanged).
- consumer: OPUS-led pages of the same passes: agrees (OPUS applied its own share).

run: `astra3_check.py` at f348f2f1d (FAILS 0) - [script](../opus-astra-returns-consume-1002/astra3_check.py)
run: `render_c_check.py` at f348f2f1d (FAILS 0) - [script](../opus-render-c-readiness-fixes-1002/render_c_check.py)
run: `residual_check.py` at f348f2f1d (FAILS 0) - [script](../opus-residual-readiness-fixes-1002/residual_check.py)
run: `render_b_check.py` at dc09bb4a1 (FAILS 0) - [script](../opus-render-b-readiness-fixes-1002/render_b_check.py)
run: `resource_b_check.py` at dc09bb4a1 (FAILS 0) - [script](../opus-resource-b-readiness-fixes-1002/resource_b_check.py)
run: `apply_by_owner.py` FABLE --apply at dc09bb4a1, in a throwaway worktree, all five batches (FAILS 0) - [ASTRA returns](../opus-astra-returns-consume-1002/apply_by_owner.py), [render B](../opus-render-b-readiness-fixes-1002/apply_by_owner.py), [render C](../opus-render-c-readiness-fixes-1002/apply_by_owner.py), [residual](../opus-residual-readiness-fixes-1002/apply_by_owner.py), [resource B](../opus-resource-b-readiness-fixes-1002/apply_by_owner.py)
