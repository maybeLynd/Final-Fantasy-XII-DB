# Y-1 — what every `uisize.json` layout key positions

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Table: `y1-layout-key-uses.tsv` (335 rows). Control: `y1_key_uses.py` (5 checks, FAILS 0).
Correction record: [`consumer-check.md`](consumer-check.md).

**The question.** Y-1 asks for the remaining parameter names and what each positions. The loader `001CA600` binds 226
keys, and every key lands in a fixed global. So "what a key positions" means what each function that reads the
key's global does with the value at each read.

**The population.** The key → global join is
[`members/layout-key-slots.tsv`](../../../16-UI/Layout-Parameter-System/members/layout-key-slots.tsv), and the global →
reader table is [`members/layout-key-readers.tsv`](../../../16-UI/Layout-Parameter-System/members/layout-key-readers.tsv).
- Both were corrected in this package. My 2026-09-13 join had bound 222 keys and misbound one; the consumer check
  gives the two defects.
- Corrected, 213 keys have a rip-relative reader, in 125 functions. That is 335 (key, reader) pairs, and each gets one
  row with these columns:
  - the key, its global and the reader;
  - `sites`: every instruction in the reader that reads the global by rip;
  - `use`: what the value is added to, compared with or stored into, with the instruction addresses;
  - `positions`: one plain phrase for what the key places or sizes on screen;
  - a confidence and a note.

All 335 rows are `read`. Where a row's note names something it did not follow, the named step is beyond the key's
use, for example a downstream consumer of the field the key sets. What the key does is stated in the row.

**How the rows were made, and what checks them.**
- **Drafting.** Two subagent passes (Claude Opus 5.5, under FABLE) drafted the rows, one half each. A third pass
  resolved the 27 rows the first two left partial.
- **FABLE's own reads.**
  - I read the nine rows the corrected join added: `FontItalicScale` ×5, `FontItalicVal` ×3 and
    `mCommandTitleFontHeight`.
  - I read the three rows re-keyed from `FontItalicVal` to `MessageWinMaskBottom`.
  - I checked the contradictions below against the bytes before recording them.
- **The control** re-derives everything in a row that the bytes decide:
  - **K1:** the rows are exactly the 335 pairs.
  - **K2:** each site list equals the reader's rip reads of the global. A `mov` whose destination is the global is a
    write and is excluded.
  - **K3:** every cited address is a function entry, a real instruction start, or a global the image references. Its
    control is that `00562C54` passes and `00562C55`, one byte into that instruction, fails.
  - **K4:** the 13 unread keys have no reader by any route (below).
  - **K5:** the join correction holds in the bytes.

**The 13 keys with no reader.** They are:
- the ten `mCursor{Up,Down,Left,Right,Open}{X,Y}`;
- `BattleLogBlackBandH` and `LicenseBlackBandH`;
- `FontShadowAlphaMuti`, a float key whose global `01DF6DE0` is referenced only by its slot installer `001B44A0`.

K4 rules out every route:
- no rip operand outside the installer;
- no image-base-relative operand (`[reg + global − 0x120000]`);
- no qword load of the key's slot pointer outside the installer. For the int keys that slot is at settings
  `+0x3B00 + slot`. For `FontShadowAlphaMuti` it is `001B5FB0()`'s object `+0x308`, looked for in every function that
  calls `001B5FB0` or loads its singleton `01F81200`.

Its positive control is that all 213 read keys are found with a rip reader. These 13 values are loaded from the file
and stored, and nothing reads them.

**What the rows correct, all checked in the bytes.**

| where | what it says | what the bytes say |
|---|---|---|
| layout page §2 and `members/` (FABLE, 09-13) | 222 keys; `FontItalicVal` → `01E0CDA8` | 226 keys. `01E0CDA8` is `MessageWinMaskBottom`, and `FontItalicVal` is `01E0CF90`. Corrected here. |
| message-window readers page, `002A6C40` / `002A70B0` / `002A6E43` | `FontItalicVal`, "the italic skew field" | `MessageWinMaskBottom`: 448 − window height − key is the window's Y, the gap to the screen's bottom. Routed to FRONTIER. |
| battle-hud readers page, `002C4720` | the three `ActionListMist…Offset` keys are X offsets | each is added to the anchor widget's Y + height (`+0x9A` + `+0x9E`) and stored as a Y (`002C530B`, `002C532E`, `002C5350`). Routed. |
| battle-hud readers page, `0028B140` | the `*NumOffset*` values are stored into the `0209BA60`–`0209BA78` effect globals | right, and it has a consequence the page does not draw. One of those stores (`0028B24A`, `ExpNumOffsetX` or `LpNumOffsetX` by `0028B1F0` / `0028B236`) lands on `EXPLPNumOffsetX`'s own global before its read at `0028B5F1`, so the authored `EXPLPNumOffsetX` never reaches the digits. Routed as an addition. |
| shared-dialogs page, `00292390` | `ListItemIconW` is "an icon width arg"; `ListItemIconH` is an icon-height guard | the column and row counts of the clear and copy loops that write a W × H block into the icon texture, and the atlas steps `01E0C478` / `01E0C47C`. Routed. |
| shared-dialogs page, `002CEB40` | `ScrollMarkOffsetY`, "the per-row mark Y" | no read. The two sites are `lea` end bounds of the 0x10-stride array at `0209E638` that precedes the key's global. The key's one read is in `002D1750`. Routed. |
| layout page, SWE2-EC7-26 (`0024ABC0`) | multiplies by `float[008C5B30]` "0x3C000000 = 1/128" | the bytes at `008C5B30` are `00 00 00 3B`, `0x3B000000` = 1/512. 1/128 is `008C5B34`. Routed. |
| numeric-formatting page, UQ-383's answer (FABLE, 09-18) | `01E0CDAC` / `…B0` / `…B4` / `…BC` / `…C0` are "timing constants" | they are the layout keys `MessageLineWordCount`, `MsgWinLogCursorOffsetX/Y`, `MsgWinSelectCursorOffsetY` and `FontBaseWidth`, which place the message-log cursor and the select pointer. Corrected here (my text). |
| control-code page §2.6 (FABLE, 09-14) | `'<'` is skipped | `002B0280` decodes it into text-context byte `+0xAB` (`002B19BE`) and adds it to each glyph's Y, so `NAOverHeadTextOffsetY` is a baseline shift. `002AC5F0` does the same at `002AE1C5`. Corrected here (FABLE's 09-14 text). |

**Findings worth knowing without opening the table.**
- **`FontItalicVal` is a real italic slant.** It is stored at text-descriptor `+0x40`. The glyph drawer `002B0280` reads
  it at `002B0AE3`, where advance × value + pen X is the x of each glyph quad's top edge. The bottom edge stays at pen X
  (`002B0BEA`, `002B0BEF`).
- **`FontItalicScale` (0.88) is the size at which italic text is measured and drawn.** It scales both measured words in
  `0029CD00`, for the battle-command widths, and is descriptor `+0x34` elsewhere.
- **`mCommandTitleFontHeight` is the battle command window's title row.** The list starts that far down and the window
  grows by it. A title-only window (mode `0x11`, or flag bit 15) is exactly that tall (`0027E02A`).
- **`mHelpMessageFontCount` and `mTriangleHelpMessageFontCount` are widths, not counts.** Each is compared with the
  measured text width (`002BFC34`), and wider text sets the child's overflow bit.
- **`PartyBlackBandTime` is a duration.** It sets the widget's animation-duration override bits at `+0x7C`.
