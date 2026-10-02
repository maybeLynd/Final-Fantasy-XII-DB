# Consumer check: 16-UI contradictions from a cloud reconstruction-readiness map, settled at the bytes, OPUS's share applied (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-16-VALUES-1002. Cloud wave 4 mapped `16-UI/` from a text snapshot (session
`session_016dMPD3qWpTj3TJxBrhZe2s`; report `cloud-reports/re-readiness/16-ui.md` in maybeLynd/Final-Fantasy-XII-DB,
ce22721b; rated NOT YET). Its 112 value items were page-text only. A local read-only pass checked them at the shipping
image:
- 74 decided against one side;
- 16 both partly or needing no edit;
- 5 undecidable statically;
- 17 left for longer multi-body reads.

The 24 count items are left out. OPUS re-checked the deciding instructions (`ui_check.py`), and every address in the
correction text is a function entry or entry+offset.

The pass drafted 129 strike edits (`apply_16ui.py`). OPUS applies the 59 on its own lines across 16 pages
(`apply_by_owner.py OPUS`). The rest go to their owners as requests:
- 44 to SWE2-EC7, on its seven pages and two of its lines;
- 15 to FABLE, on the router contract and 13 of its lines;
- 8 to FRONTIER and 1 to SWE2-FRONTIER, all their lines;
- 2 to SWE2-DATA, its lines.

- **Affected:** 16-UI/Battle-Hud/the-battle-hud-layout-readers.md, 16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md, 16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md, 16-UI/Handbook/the-handbook-screen.md, 16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md, 16-UI/README.md, 16-UI/Request-Router/ui-request-router.md, 16-UI/Shared-Dialogs/the-shared-dialog-widgets.md, 16-UI/Shop-Screens/the-shop-screens.md, 16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md, 16-UI/Text-And-Number-Rendering/the-text-control-code-language.md, 16-UI/Widget-Object-Model/CONTRACT-widget-object.md, 16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md, 16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md, 16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md, 16-UI/the-selection-the-menu-publishes.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the sixteen OPUS-led and shared 16 pages (OPUS lines) | revised-here |
  | EC7's message-protocol, layout, Config, licence-grid, message-window, quest-list and monster-viewer pages and lines | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 44 edits) |
  | the router contract and FABLE's lines | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 15 edits) |
  | FRONTIER's lines | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py FRONTIER` and `SWE2-FRONTIER`, 9 edits) |
  | DATA's lines | routed-to-SWE2-DATA (request with `apply_by_owner.py SWE2-DATA`, 2 edits) |
  | the 17 undecided value items and the 24 count items | routed-to-OPUS (later reads) |
  | RE repo `docs/readiness/16-ui.md` | routed-to-OPUS (filed from this commit, with the byte verdicts) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ui-readiness-fixes-1002/ui_check.py, verified at fd96f1634: 7 instructions decode as cited, FAILS 0 ([`ui_check.out`](ui_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (59), FAILS 0.
