# Affected-consumer check: FABLE's 2026-09-13 layout-key join corrected, 222 → 226 keys (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md (§2 "Which code reads each key", §3, §7 Y-1 and Y-6, §8), 16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md (§2.1), 16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md (UQ-383's answer, the "timing constants" clause), 16-UI/Text-And-Number-Rendering/the-text-control-code-language.md (§2.6, the skipped-codes row)

regenerated with it: the members tables and scripts `layout_key_slots.py`, `layout-key-slots.tsv`, `layout_key_readers.py`, `layout-key-readers.tsv` (16-UI/Layout-Parameter-System/members/)

run: y1_key_uses.py at bbd3af82a (worktree = that HEAD plus this package), 5 checks, FAILS 0. K5 is the check that
measures the correction; K1 and K4 measure its consequences (335 key/reader pairs; 13 unread keys, 213 read).

**The change.** My 2026-09-13 join of `001CA600` (the `uisize.json` loader) with `001AF470` (the slot installer) had
two defects:

1. capstone prints a small displacement in decimal. `mov rcx, qword ptr [rbx + 8]` (`001CA673`) did not match the
   hex-only pattern, so `mCommandTitleFontHeight` (→ `01E0C374`) was dropped.
2. At `001CC572`, `rbx` is reloaded with `001B5FB0()`'s object (the singleton at `01F81200`) for the three
   `Variant_ReadFloat` keys. `001B44A0` fills that object's slots (`001B4551`–`001B4574`; reached by the tail jump at
   `0017FA07`, with `rcx = 001B5FB0()`).
   - The script keyed slots by offset alone. `FontItalicVal`'s `[rbx + 0x2f8]` therefore replaced
     `MessageWinMaskBottom` (int slot `+0x2F8`, `001CB2CD`).
   - The two other float keys are loaded through `rax` and were never matched.

Corrected, the join binds all 226 distinct keys:

| key | 09-13 join | corrected |
|---|---|---|
| `MessageWinMaskBottom` | absent | `01E0CDA8` |
| `FontItalicVal` | `01E0CDA8` | `01E0CF90` |
| `FontItalicScale` | absent | `01E0CF94` |
| `FontShadowAlphaMuti` | absent | `01DF6DE0` |
| `mCommandTitleFontHeight` | absent | `01E0C374` |

Readers now cover 213 keys in 125 functions; 13 keys have no reader, including `FontShadowAlphaMuti`.

| consumer | what it says | state |
|---|---|---|
| layout page §2, the join sentence and the count table | 222 keys, 210 with readers, 124 functions | revised-here (struck; dated correction paragraph) |
| layout page §2, "No rip-relative reader: 12 keys" | 12 | revised-here (13; `FontShadowAlphaMuti` added) |
| layout page §2 family table, `FontItalic…` and `MessageWin…` rows | `002A6190`/`002A6C40`/`002A70B0` read `FontItalicVal` | revised-here (struck; the three read `MessageWinMaskBottom`; the `FontItalic…` readers replaced; a `CommandTitle…` row added) |
| layout page §3, `001AF470` row | "installs the 222 slot pointers" | revised-here (227: 223 keyed plus 4 unkeyed; `001B44A0` row added) |
| layout page §8 evidence row | 222 / 210 / 124 | revised-here |
| layout page Y-6 ⚠ paragraph (OPUS's) | "the remaining difference is unexplained" | revised-here (a dated resolution sentence appended; OPUS's text kept) |
| layout page Y-1 box, the 09-13 narrowing | "210 of the 222 keys" | revised-here by the Y-1 answer |
| map-screens page §2.1 | "binds 222 … all 222 keys" | revised-here (my 09-13 text; struck, 226) |
| `members/layout_key_slots.py`, `layout-key-slots.tsv` | the defective join | revised-here (object tracking, decimal displacements, a fourth column naming the installer) |
| `members/layout_key_readers.py`, `layout-key-readers.tsv` | readers keyed on the old join | revised-here (regenerated; `001B44A0` excluded as an installer, like `001AF470`) |
| `16-UI/Message-Windows/the-message-window-layout-readers.md` rows `002A6C40`, `002A70B0` and site `002A6E43` | `FontItalicVal` at `01E0CDA8`, "the italic skew field" | routed-to-FRONTIER (the page's author, from `FABLE-REQ-SWE2-FRONTIER-LAYOUT-KEY-READERS`): the key is `MessageWinMaskBottom`, the gap between the window's bottom and the screen's bottom |
| layout page, FRONTIER's 09-14 section (`002A70B0` "NobuMsg/FontBase/MessageLine/FontItalic") and SWE2-EC7-26 (`0024ABC0` "the `FontItalic` builders") | `002A70B0` reads a `FontItalic` key | routed-to-FRONTIER in the same request (it reads `MessageWinMaskBottom`) |
| battle-hud readers page rows `00273E30`, `00298250`; the license-board reader `005569F0`; the confirm-window reader `0057C480`; the widget-protocol page's `003EED60` | no `FontItalicScale` / `FontItalicVal` listed | routed-to-FRONTIER as additions (the Y-1 rows give each site) |
| `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md` §`001B44A0` | `001B44A0` seeds `+0x2F8`/`+0x300`/`+0x308` from `01E0CF90`/`01E0CF94`/`01DF6DE0` | agrees (the same stores K5 reads) |
| `19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md` | `+0x9E = 01E0C374` in the command-window builder | agrees (`0027E02A`; the Y-1 row names the key) |
| `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md` crossings paragraph | `001CA600` reads `mScrollListHeight` and `mCommandTitleFontHeight` | agrees |
| register Y-6 row | reports the 222 / 226 mismatch as the owner's to correct | agrees as history. The Y-1 row states the resolution, and Y-6's own answer, read of the body, is unchanged. |
| numeric-formatting page, UQ-383's answer (FABLE, 09-18) | `01E0CDAC`/`…B0`/`…B4`/`…BC`/`…C0` are "timing constants" of `002A4430` | revised-here (struck; they are the layout keys `MessageLineWordCount`, `MsgWinLogCursorOffsetX`/`Y`, `MsgWinSelectCursorOffsetY`, `FontBaseWidth`, per the Y-1 rows for `002A4430`) |
| control-code page §2.6 (FABLE, 09-14), the skipped-codes row | `<` is skipped | revised-here (struck; `002AE1C5` reads the payload into `+0xAB`, which the glyph path adds to each glyph's Y at `002B0AED`–`002B0B2D`) |
| `_index/candidates/y1-layout-key-uses/y1-layout-key-uses.tsv` | three rows keyed `FontItalicVal` at `01E0CDA8` | revised-here (re-keyed `MessageWinMaskBottom`; nine rows added for the four keys the join had lost or misbound) |

Grep of `FontItalicVal`, `FontItalicScale`, `FontShadowAlphaMuti`, `MessageWinMaskBottom`, `mCommandTitleFontHeight`,
`01E0CDA8`, `01E0CF90`, `01E0CF94`, `01DF6DE0`, `01E0C374`, "222 keys", "222 slot", "210 keys", "124 functions" across the
database's pages, tables and scripts, 2026-09-27. Inbox, audit-log and handoff mentions are receipts and are not edited.
