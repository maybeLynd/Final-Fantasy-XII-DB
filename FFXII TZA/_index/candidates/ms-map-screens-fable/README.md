# MS-1 and MS-2: the map containers' state bits and the picture origin (FABLE, Claude Opus 5.5, 2026-09-29)

[`ms_states.py`](ms_states.py) runs C, C2, 9, 10, 11 and O: FAILS 0 ([output](ms_states.out)). Static.

## MS-1: what container `+0x179D2` bits 9, 10 and 11 mean as states

**C (the census).**
- **Coverage.** It collects all 47 writes to the word. Each one's register source is traced to its immediate, and no
  register source is left unresolved.
- **The whole-word stores and xor merges add no bit 9–11 (C2).** Two toggle bit 2; one ORs bits 0–1 into the word it
  read; the xor merges are masked to `0x40` / `0x30`.
- **Limit.** The census reads displacements `0x179D2` / `0x179D3` (none of the latter exist) and `0x179D0`, which is
  word-wide everywhere, so nothing overlaps.

**The three bits:**

| bit | set by | cleared by | meaning |
|---|---|---|---|
| 9 | only the location page's link path (`002BB8BD`) | each page's per-frame step (`002B784E` track, `002BABE7` location), once both page slots are empty and it has called `003C21B0` | the reopen request after a link |
| 10 | only the two mode-5 openers: `002B6220` (track; creates the container with `0x500`) and the leaf `002BA000`, whose only caller is the fullscreen procedure's location opener `0028E660` | nothing | "opened in mode 5": the location setup copies the field-time container's map data instead of rebuilding it |
| 11 | only `002BAA79` (`r14d` = `0x800` at `002BA927`), at the end of the location map's confirm | nothing | the confirm latch: after one confirm, every later close and confirm is refused. The track map tests it but never sets it |

## MS-2: what the two floats `+0x10` / `+0x14` of the block `02B457F0` mean

**O.** Their only writer is the setter `003C6360`. Its only caller is the `NPS2` consumer `00379870`, the sub-location
id → world-to-image transform of the `sloc` container page. The consumer passes the record's originX / originZ (`+0x10` /
`+0x14`), or 0 for a null slot.

So the floats are **the current sub-location picture's world origin**. The track arm negates them before its transform
call, which translates world positions into the picture's frame (4 pixels per unit, per the `sloc` page).

**Holders.** The block is also reached by pointer, through `003C8060` (nine call sites) and a `lea` at `003C4237`. None
of the ten stores to `+0x10` / `+0x14` within 40 instructions of receiving it.

affected: `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` (the two "not established / not read" sentences
struck and answered; the status line keeps MS-3 open)

consumer: the `sloc` container page §4 lists `003C6360` / `003C6380` as "the origin and extent consumers … not read here".
This record reads them, and the page agrees.

run: ms_states.py at 42a617a9a, FAILS 0.

**Still open.** MS-3, which ancestors of a container can be released.
