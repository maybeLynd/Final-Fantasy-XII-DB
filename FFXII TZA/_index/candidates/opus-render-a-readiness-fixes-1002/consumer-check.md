# Consumer check: 17-Render contradictions (part A) from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-17-VALUES-1002, part A. Cloud wave 5 mapped `17-Presentation-Rendering/` from a text
snapshot (session `session_01Bf11Bg4ubT2fxuBZvpWtqD`; report `cloud-reports/re-readiness/17-render.md` in
maybeLynd/Final-Fantasy-XII-DB; rated NOT YET). Its value items were page-text only. A local read-only pass took the 85
items in report lines 2383-2800 and decided most of them at the shipping image; ten are naming questions or were not
read. OPUS re-checked a sample (`render_a_check.py`).

Corrected at the bytes:
- the trailer store (`00426480+0x13`);
- the walked list `02B3F508`;
- the coerced multiplier: -1 stays -1 (`00417A80+0x38`);
- `base += delta` (`003E4370+0x2D`);
- the constructor `00184F20`;
- the render-record base `022C6F28` (other quoted bases have no references);
- the constant 2^-12, not 2^-13.

The pass drafted 101 strike edits (`apply_17render_a.py`). OPUS applies the 19 on its own lines across six pages
(`apply_by_owner.py OPUS`). The rest are held or routed:
- 12 on the transform-publish contract and the render-command-list contract are held until their F-interior sections
  publish (`apply_by_owner.py OPUS-HELD`).
- 47 go to SWE2-EC7.
- 13 go to FABLE.
- 8 go to SWE2-STRUCT, on its field-tier lines.
- 2 go to SWE2-DATA.

- **Affected:** 17-Presentation-Rendering/CONTRACT-coast-down-latch.md, 17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md, 17-Presentation-Rendering/Character-Render-Records/the-bone-trails.md, 17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md, 17-Presentation-Rendering/Character-Rendering/character-render-object.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the six OPUS-led 17 pages (OPUS lines) | revised-here |
  | the transform-publish and render-command-list contracts | routed-to-OPUS (held; `apply_by_owner.py OPUS-HELD`, 12 edits) |
  | EC7's ramp, pool, lighting, GI, look and status pages and lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 47 edits) |
  | the handlers page, the lighting, fade and README pages, and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 13 edits) |
  | STRUCT's field-tier lines on the record-array page | routed-to-SWE2-STRUCT (request with `apply_by_owner.py SWE2-STRUCT`, 8 edits) |
  | DATA's fef lines | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 2 edits) |
  | RE repo `docs/readiness/17-render.md` | routed-to-OPUS (filed after part B, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-render-a-readiness-fixes-1002/render_a_check.py, verified at 76c2055a3: 4 instructions decode as cited, FAILS 0 ([`render_a_check.out`](render_a_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (19), FAILS 0.
