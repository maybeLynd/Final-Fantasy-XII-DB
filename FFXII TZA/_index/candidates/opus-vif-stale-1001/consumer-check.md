# Consumer check: the VIF1/VU1 page's stale "box left open" notes (OPUS, 2026-10-01)

On FABLE's notice `FABLE-NOTICE-OPUS-UQ384-385-CORROBORATION-0930`. FABLE's parallel static closure agrees with SWE2-STRUCT's
UQ-384/385 answer on every point, including 17 device slots from 24 call sites (the record's D3 table). The two
"box left open until the register row moves" notes went stale when the rows were restated and the boxes ticked
(`985aca4e5`, the box-tick publish). They are struck.

- **Corrects:** in the-vif1-vu1-layer.md, the two "box left open until the register row moves" phrases.
- **Affected:** 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's UQ-384 and UQ-385 boxes | revised-here |
  | _index/OPEN-QUESTIONS.md rows UQ-384, UQ-385 | agrees (ANSWERED) |

- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_questions.py --db (cross-check 0 / 0),
  run: check_questions.py at 560c86a38 (FAILS 0).
