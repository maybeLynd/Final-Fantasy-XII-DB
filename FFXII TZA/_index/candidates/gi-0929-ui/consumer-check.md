# Consumer-check record — GI-1, GI-3, GI-5, GI-6 answers and their UI-page corrections (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `Database/FFXII TZA/16-UI/Gambit-Screens/the-gambit-screens.md`
affected: `Database/FFXII TZA/16-UI/License-Board-View/the-license-board-screen-widgets.md`
affected: `Database/FFXII TZA/16-UI/Shop-Screens/the-shop-screens.md`
affected: `Database/FFXII TZA/16-UI/Unlabelled-Panes/the-unlabelled-procedures.md`
affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md` (rows GI-1, GI-3, GI-5, GI-6)

Each correction below is struck on its page with the corrected statement beside it (`**Corrected 2026-09-29 (FABLE, GI-n):**`).
Consumers come from a grep of the address, the offset and the wording over the database (`_experiments/evidence` excluded
as retained history). States: **revised-here** (edited by this publish), **agrees** (a current consumer that already says the
right thing or makes no claim the correction touches; unchanged), **routed-to-<owner>** (text for the owner, quoted).

## GI-1 — the gambit screens

1. **`0056AE80` / `0056B100` sides were swapped.** The page called `0056AE80` the condition-side row emitter and `0056B100`
   the action side; `0056AE80` builds the action picker's tabs (menu kind `0x22`, action grid `0208D300`) and `0056B100` the
   condition picker's (kind `0x23`, target grid `0208D310`).
   Consumers: the gambit page member table — revised-here. No other page cites either body's side.
2. **The `0056B350` list-move row had both keys negated.** `GambitTargetListMoveX` is used unchanged for mode 1 and only
   `GambitActionListMoveX` is negated. Consumers: the gambit page layout-key table — revised-here;
   `16-UI/Layout-Parameter-System/members/layout-key-readers.tsv` rows 103/106 and
   `_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv` rows 103/106 — agrees (already bind Target and Action
   the right way, Action negated).
3. **`00566C10` is not a gambit-type icon.** It is a tab-strip marker (two pulsing page arrows plus an optional sliding
   pointer) shared with the shop; its id 3 computes a sine alpha rather than loading an icon, and create-record `+0x14`
   bit 0 means "has a sliding pointer" (1 gambit strip, 0 shop strip). Consumers: the gambit page procedure table, member
   row, the `00566C10` section and the residue bullet — revised-here; `_index/PROGRAM-STATE.md` (names it "GambitIcon", a
   label only) — agrees; `16-UI/Menu-Screen-Atlas/the-menu-screen-atlas.md` "Screens read so far" ("the `00566C10` icon
   widget") — routed-to-atlas-owner, text in C-1 below.
4. **The list/editor tree was inverted.** The editor `005691E0` creates the pick list `0056B4D0` (through `00567D80` and
   the installer `0056B350`), and the list's `+0xC8` is that editor. Consumers: the gambit page "The tree" and procedure
   table — revised-here; the atlas's "`0056B4D0` (list, parent) → `005691E0` (editor, child on `+0xC8` …)" —
   routed-to-atlas-owner (C-1); `16-UI/Widget-Object-Model/the-widget-message-protocol.md` message-289 row (lists
   `0056B4D0` as a sender only) — agrees.
5. **`0056C170` is the pick list's tab-strip container**, not a per-gambit-row container. Consumers: the gambit page
   `0056C170` section and member row — revised-here; `16-UI/Unlabelled-Panes/the-unlabelled-procedures.md` row
   `0056C060` ("child of the `0056C170` leaf slot") — agrees.
6. **The 2026-09-18 note's closing sentence** ("the icon set does follow a per-slot record field …") — revised-here on the
   gambit page; the merge addresses it cites stay.

## GI-3 — the license board screen widgets

7. **Message 285 is not "node-select, confirm, LP spend".** It is the reply the shared message box and Yes/No box post to
   their opener (dialog code, answer). Consumers: license page section 4 — revised-here; `_index/PROGRAM-STATE.md`
   lines 5772–5773 ("its vocabulary stays UNRESOLVED") — routed-to-PROGRAM-STATE-owner (C-2);
   `16-UI/Widget-Object-Model/the-widget-message-protocol.md` 285 row and "The disposition" ("one screen talking to
   itself") — routed-to-widget-object-model-owner (C-3).
8. **The chooser widget is not an id-10-only cursor handler.** It is the licence-board chooser (the twelve-board wheel)
   and answers 285 for its own dialogs. Consumers: license page summary and section 5 — revised-here; the atlas
   ("the … cursor handler") — routed-to-atlas-owner (C-1); `_index/PROGRAM-STATE.md` line 5771 — routed-to-PROGRAM-STATE-owner (C-2).
9. **The four draw children belong to the chooser**, not to the board view. Consumers: license page section 2 (dated note
   after the tree block) — revised-here; `16-UI/Menu-Screen-Atlas/members/ui_atlas.tsv` installer column — agrees.
10. **The draw children's arms.** The `002472A0` call is the id-25 arm, not arm 4; the backdrop child's `+0xDA` is the
    wheel centre, not a scroll word. Consumers: license page section 7 — revised-here.
11. **`LicenseBoardBallFaceSecondOffsetY` is the second row of member faces**, multiplied by index/3, not a "per-second
    hand". Consumers: license page section 9 — revised-here; `_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv`
    row 148 ("imul by face index/3") — agrees.

## GI-5 — the shop screens

12. **`+0xE4 & 0x3FC0` is the goods kind, not buy/sell.** `0x1C0` is kind 7 (loot) and `0x2C0` kind 11 (bazaar); buy versus
    sell is bit 0. Consumers: shop page, three statements (the trade panel's id-12 bullet, the quantity paragraph, "What
    this screen does") — revised-here. No other page states the field's values.

## GI-6 — the unlabelled procedures

13. **The content pages' kind compares.** The page said both pages compare against 2 and 5; the first compares only
    against 5. Consumers: unlabelled page — revised-here.
14. **The kind-6 host serves the Hunts category**, not item/equip. Consumers: unlabelled page host row — revised-here, and a
    dated note under the `005789D0` / `00579420` heading (that pair's own interior reading is not re-derived);
    the atlas ("item/equip `005789D0`/`00579420`") — routed-to-atlas-owner (C-1); `_index/COVERAGE.md` line 152
    ("item-equip pages") — agrees for now (names a page section; left to the unlabelled page's owner);
    `_index/OPEN-QUESTIONS.md` UQ-160 (answered row, history) — agrees.
15. **The shared table framing.** The page called the records `{paneKind, flag, u16, u16}`; they are
    `{u16 title, u16 help, u8 value, u8 flag}` from `00D23688` (four menu rows, then eight kind rows). Consumers: unlabelled
    page — revised-here; `16-UI/Shared-Dialogs/the-shared-dialog-widgets.md` (the four menu records) and
    `16-UI/Handbook/the-handbook-screen.md` (the kind table) — routed-to-dialogs-batch (GI-2 / GI-4, publishing separately),
    exact text C-5 and C-6 in `consumers_ui.md` of FABLE's ui draft; the sibling batch found the same framing.

## Routed text

**C-1 (atlas, "Screens read so far"):** "*Corrected 2026-09-29 (FABLE, GI-1 / GI-3 / GI-6):* the gambit tree runs the other
way — the editor `005691E0` creates `0056B4D0`, the condition/action pick list, through `00567D80` → `0056B350`, and
`0056B4D0`'s `+0xC8` is that editor; `00566C10` is a tab-strip marker (page arrows + sliding pointer) shared with the shop,
not an icon widget. `00557DB0` is the licence-board chooser (the twelve-board wheel), not only a cursor handler; its four
draw children are its own. `00579AF0` hosts the handbook's Hunts category (pane kind 6); whether `005789D0`/`00579420` are
item/equip is not re-derived."

**C-2 (`_index/PROGRAM-STATE.md` 5771–5773):** replace "the directional-input cursor handler" by "the board chooser
(twelve-board wheel)" and "The board's id-285 sub-command table (18 arms) is mapped but its vocabulary stays UNRESOLVED" by
"id 285 is the shared dialogs' reply (code, answer); all 18 slots mapped to the board's dialog codes 2026-09-29 (GI-3)".

**C-3 (widget-message-protocol page, after the 285/287/289 table):** "*Corrected 2026-09-29 (FABLE, GI-3):* 285 is not one
screen talking to itself. It is the reply the shared message box `002CE370` and Yes/No box `002CDF20` (and `002C2320`) post
to whichever widget opened them — (0x11D, dialog code, answer), Yes = 1 — so its receivers (`0055CD40`, `00557DB0`,
`003FF360`) are the openers and the sub-command is the dialog code the opener passed. The license board's 18 slots are
decoded on the license board page section 8a."

## Regression

Four controls in this folder, each printing its checks and exiting non-zero on any failure, each with a positive control:

- `gi1_tabstrip_marker.py` (output `gi1_tabstrip_marker.out`) — the two installers and their `+0x14` values, every `+0xE8`
  bit-0 reader, the `+0x588` branch, the tab-frame constants, the list-move keys, the tree direction; its REJECTS lines fail
  on the swapped-sides and bit-0-is-art readings.
- `gi3_dialog_reply_and_wheel_layers.py` (output `.out` beside it) — the 18 slots, the only `0x11D` senders, every opener
  code and its shipped text (text-id control: group 12 → `listhelp_status.bin`), the four installers' single callers,
  the art sources, the ring/face loops; its REJECTS lines fail on the node-select vocabulary and the per-second-hand readings.
- `gi5_shop_panel_e4.py` — the whole-image `+0xE4` write sweep (control: the trade panel's own four writes), the 17 panel
  writes, the kind tables and the Buy / Sell / Bazaar sets; its REJECTS line fails on the buy-`0x1C0` / sell-`0x2C0` reading.
- `gi6_handbook_category.py` — the record framing read by every reader, the titles in the shipped text, kind 5 = Bestiary
  as the control (the other framing would title kind 5 "Hunts"), the only kind setters, the page chain.

run: at 6facc53bc (HEAD when they ran) - gi1_tabstrip_marker.py, gi3_dialog_reply_and_wheel_layers.py, gi5_shop_panel_e4.py and gi6_handbook_category.py, every check passes, FAILS 0 in all four (outputs: the .out files beside them)
