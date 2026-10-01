# DD owner read, batch 3: five residual text-drawing pages and two UI pages (SWE2-DATA, 2026-09-30)

affected: 99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md, 99-Unresolved-Residual/the-widget-tree-draw-pass.md, 99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md, 99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md, 99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md, 16-UI/the-selection-the-menu-publishes.md, 16-UI/Battle-Hud/the-battle-hud-layout-readers.md, _index/OPEN-QUESTIONS.md (new rows SD-100..SD-107, SD-120..SD-128)

run: at aac0f6798: measure_checks.py, widget_draw_checks.py, shared_context_checks.py, dispatch_checks.py,
ui_bi17_dispatch.py and ui_2fe0_sites.py, each FAILS 0 (the .out files beside them). All are static reads of the
shipping image through `../rc22-34-resource-readers-0930/pe.py`.

Task `SWE2-DATA-DD-OWNER-READ-3-0930` (target key only). The pages are the next unowned, clean rows of
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv). The method is the one used for
[`dd-data-0930`](../dd-data-0930/README.md) and [`dd-data-2-0930`](../dd-data-2-0930/README.md). No status word was
raised.

| page | what changed | residue |
|---|---|---|
| measuring text | `002AF340` returns the count of characters laid out up to the stop string, or -1 (the decompiler dropped the return). `002ABB20`'s stop string `00916548` is `0F 23`, the `#` page-wait escape. The "30 frames" period is now a rate. §5 fields corrected per UQ-173 and the "7 of 13 unread" line per UQ-383. Sections added (`measure_checks.py`) | SD-100 |
| widget-tree draw pass | "not read" reconciled: the three bodies are read on the widget-background page. `0208F564` is the draw-bracket pass index. Message gates are anchored (`widget_draw_checks.py`) | SD-101, SD-102 |
| shared drawing context | GJ-1/2/4/5/6 brought up to date. Struck and corrected: "indexed accesses: zero" (seven exist, all at scale 8), the `+0x10FC` width line, the `0209CC48` "cleared" row. The `0x7D00` initialisers are named (`shared_context_checks.py`) | SD-103..SD-105 |
| text-element dispatch table | reconciled to GJ-7, the §6b withdrawal and GJ-11. `002DD680` calls `002B0280`. The kind-2 stamp at `002B3470` is unconditional (`dispatch_checks.py`) | SD-106, SD-107 |
| largest unclassified functions | the UNKNOWN-ID tokens (BI-17..BI-19, never registered) are reworded. The second dispatcher `003CD2C0` maps opcodes 1-8 to `003CCF20`'s eight operations, and the tail's condition is read (`ui_bi17_dispatch.py`). §5 call chain added | SD-120..SD-123 |
| the selection the menu publishes | its two status-line questions are answered: one object type (the `0x3010`-byte command-menu widget; `002778C0` reaches it through `[widget+0xD0]`), and `0209BE80` is the per-frame singleton's pointer slot. The fourteen `+0x2FE0` sites are anchored (`ui_2fe0_sites.py`; that census covers the three named functions only). Sections added | SD-124, SD-125 |
| battle-HUD layout readers | the split table is re-joined, and the status line is reconciled (`00276D30`'s arms are decoded on the selection page). Sections added | SD-126..SD-128 |

## Consumer check

| consumer | disposition |
|---|---|
| the seven pages above | revised-here |
| OPEN-QUESTIONS UQ-173 row, 2026-09-18 narrowing ("the stepper decrements `+0x88` in mode 5") | routed-to-FABLE: the jump table at `002AC1B4` sends modes 3 (`002ABF9F`) and 7 (`002AC18B`) to the `+0x88` decrement; the mode-5 arm (`002ABFFC`) never touches `+0x88` (`measure_checks.py`) |
| `16-UI/Request-Router/ui-request-router` line ~696 ("not established": the return of `002AF340`) | routed-to-FABLE: the page carries another lane's uncommitted edits, so it is not edited here; `measure_checks.py` answers the return and the `00916548` stop string |
| the glyph-quads page `how-a-line-of-text-becomes-glyph-quads` (same folder as the dispatch table) line ~827 (the inside of `002AF340` not established) | routed-to-FABLE: the return value and stop set are now read; the rest of the body is not |
| OPEN-QUESTIONS UQ-383, GJ-1..GJ-7, GJ-11 | agrees (the pages now follow them) |

## Rule before and after (`documented_rule.py`)

Before: READY 6, UNKNOWN-ID 1. After: PARTIAL 7, each on its newly registered SD rows. Before this read, that prose
residue carried no register id.
