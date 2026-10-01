# Consumer check: wave A of SWE2-AUDIT-SPEC's narrowings (SWE2-CONTRACT for OPUS, 2026-10-01)

Wave A of `SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS` (this folder's README) applied the quoted correction wording
of 13 ACCEPT-WITH-NARROWING reviews to their OPUS-lane records and to the two pages the wording names. Every
replaced statement is kept struck, with a dated note naming the review. No status word or register cell was moved.

- **Corrects:** SD-1's "a kind-1-only branch at `00305BA5`" and "The flag has two readers"; the text-gap record's
  "Four addresses are interior to real `.pdata` extents"; GR-1's S4 "Every read has a covering write in its
  command's begin handler or earlier in the same handler"; GR-7's list of the other `+0xB90` accesses; GR-4/5's
  "722 qword loads ... in 129 functions" and "`00328360` to `002FCBF0`"; GR-14's "They call the target's own
  procedure" (and the B6 check text); GR-17's "135 of the 383"; the DD-CRT record's "`0071E340` constructs two empty
  MSVC strings"; the animation page's "The shipped data uses it four times ... animated this way"; the widget page's
  "203 functions at 240 sites" (§4a); SD-100's mode 0/1/4, mode 3 and mode 5 rows, its "variable" writer row and
  its "variable store" limit; SD-105's V2 writer, V4 sub-bullets and "Authored overrides" limit; SD-106's headline
  sentence, its `0057C58B` / `0057C5DB` row, "centred on screen", and the M5 comment.
- **Affected:** _index/candidates/sd1-force-fight-enemy-consumers-0930/README.md; _index/candidates/text-gap-append-0930/README.md; _index/candidates/gr1-wait-slot-settled-0930/README.md; _index/candidates/gr7-kind10-reader-0930/README.md; _index/candidates/gr4-gr5-action-row-readers-0930/README.md; _index/candidates/gr13-15-shop-list-widget-0930/README.md; _index/candidates/gr13-15-shop-list-widget-0930/gr13_15_shop_list_check.py; _index/candidates/gr13-15-shop-list-widget-0930/gr13_15_shop_list_check.out; _index/candidates/gr17-reward-table-lifetime-0930/README.md; _index/candidates/opus-dd-crt-0930/README.md; _index/candidates/opus-dd-crt-0930/batch2-animation.md; _index/candidates/sd100-reveal-modes-0930/README.md; _index/candidates/sd105-reveal-inputs-0930/README.md; _index/candidates/sd106-measure-sites-0930/README.md; _index/candidates/sd106-measure-sites-0930/sd106_sites.py; 22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md; 16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 13 records and two pages listed above (each corrected statement, struck and noted) | revised-here |
  | 15-Input/Modal-Toggles/r2-force-fight-toggle.md §7, the `FLEEING`-label box ("The force-fight flag `01E0C2B8` has only two readers, both under the battle frame") | disagrees in scope; routed-to-OPUS (page owner). Replacement: "has only two consumer readers, both under the battle frame (UQ-152 below); its writer `00252C80` also reads the old value at `00252C94`" |
  | 15-Input/Modal-Toggles/r2-force-fight-toggle.md §1 SD-1 summary (enemy AI order checks, spawned unit engagement, combos, movement) | agrees (it states the routes, which the review keeps) |
  | _index/candidates/sd1-force-fight-enemy-consumers-0930/sd1_consumers.py docstring ("The flag 01E0C2B8 has two readers") | routed-to-OPUS (a comment; same replacement as the record) |
  | _index/candidates/false-positive-dispositions.tsv row 76 (text-gap record, evidence `940533025da6baf4`) | lapsed by the reword, as the review predicted (now `dd112027c34e0da2`); routed-to-SWE2-AUDIT-SPEC for a re-sign |
  | _index/candidates/text-gap-citations-250.tsv rows `00121E11`, `0036F22E`, and their reasons in textgap_rule13.py | routed-to-OPUS; proposed cells in the README |
  | 04-Actor-Entity/the-field-runtime-pass.md §8 GR-1 answer note ("the next native command that uses the byte overwrites it before any read") | agrees |
  | _index/OPEN-QUESTIONS.md row GR-1 (Limits sentence) | routed-to-OPUS (register owner); proposed cell in the README |
  | 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md `+0xB90` rows; 07-Combat-Action/Action-Definition-Row/the-action-definition-row.md §2.2 `+0x3A` and §7 GR-4 / GR-7 answers | agree (none restates the narrowed lists, counts or chains) |
  | 12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md (GR-14 answer) | agrees (it states that the shop lists never receive message 26, which the review keeps) |
  | 13-Rewards-Progression-Economy/experience-and-license-point-award.md (GR-17 answer) | agrees (it does not restate the 383 count) |
  | _types/types.tsv `MsvcTreeNodeHeader` ctor cell ("constructs two empty MSVC strings at +0x20 and +0x40") | disagrees; blocked (SWE2-STRUCT holds the file in SWE2STRUCT-AWN-WAVE-B-1001); proposed cell in the README |
  | _index/candidates/opus-dd-crt-0930/dd_crt_check.py comment (line 42, the same wording) | routed-to-OPUS (a comment) |
  | 24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md (`0071E340` as a `_Buynode` body) | agrees (it does not say what the strings hold) |
  | 99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md, Glyph-Run-Rendering/the-shared-drawing-context.md, Glyph-Run-Rendering/the-text-element-dispatch-table.md (SD-100 / SD-105 / SD-106 answer pointers) | agree (each carries a pointer to its record and none restates a narrowed sentence) |
  | _index/OPEN-QUESTIONS.md rows SD-1, SD-100, SD-105, SD-106, GR-4, GR-5, GR-7, GR-13 to GR-15, GR-17 | agree (the answers they state stand) |
  | _index/knowledge.sqlite | derived; routed to OPUS for the next regeneration, never hand-edited |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-awn-wave-a-1001/awn_a_checks.py (A: wording present,
  original struck, one unstruck copy fewer than HEAD, note beside it; X: each original present at HEAD; K: checker
  texts; T: table widths; L: note links; B1: the blocked cell untouched).
  run: awn_a_checks.py at 560c86a38 (FAILS 0)
