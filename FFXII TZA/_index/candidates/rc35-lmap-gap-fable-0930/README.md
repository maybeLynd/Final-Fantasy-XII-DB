# RC-35: the 8-byte block between array C and array D of a `menumap_location.bin` record is the zoom set `003BE680` reads (FABLE, Claude Opus 5.5, 2026-09-30)

Register row RC-35 belongs to SWE2-CONTRACT. It asks: "What, if anything, reads the 8-byte block between array C and
array D of each `menumap_location.bin` record (`f0 00 f0 00 40 01 00 00` in 46 of 48 records)?". The C/D walkers
`003BFF20`, `003C1070` and `003C0740` step over it. FABLE took the row after SWE2-DATA parked on the account API limit
(`FABLE-RC35-LMAP-GAP-READERS-0930`, target key only). FABLE did not edit the row or the page.

## Answer: `003BE680` reads it, as three words

`003BE680(n, &w2, &w4)` (122 B), read to its returns:
- **Record.** It loads the location file from the world-map widget singleton, `[02B457E0] + 0xE0` (`003BE680`-
  `003BE68A`). It refuses `n >= byte [+9]` (`003BE696`-`003BE69D`), and takes record `n` at `file + word [file + 0xA + 2n]`
  (`003BE6A1`-`003BE6A7`).
- **Array C.** It forms C = `rec + 4 + 24*(byte [rec] + byte [rec+1])`, that is `rec + 4 + 24*(countA + countB)`
  (`003BE6AE`-`003BE6BD`).
- **The block.** It then adds `20 * byte [rec+2]`, 20 times countC (`003BE6C0`, `003BE6CA`-`003BE6D0`). **That is the end
  of array C, the start of the 8-byte block.** The D walkers add 8 more at this point (`003BFFAA`, `003C110B`); this
  routine does not.
- **Reads:** `word [+2]` into `*w2` (`003BE6DE`-`003BE6E2`), `word [+4]` into `*w4` (`003BE6EB`-`003BE6EF`), and
  **returns `word [+0]`** (`003BE6F3`). Bytes `+6`/`+7` are not read.
- In the 46 records with the common pattern, the three words are 240, 240 and 320 (`0xF0`, `0xF0`, `0x140`).

## Its consumers

Three call sites, all in the map screens ([the map screens](../../../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md)):
- **`002B7FFA`** in the track-map page `002B7B80`, and **`002BB45E`** in `002BAF80`. The record index is
  `word [obj + 0x138]`, and a return of 0 skips the use (`002B8002` / `002BB466`). When `word [obj + 0xBBE0]` is 6, the
  `+2` word is the value used (`002B800B`-`002B8016`, `002BB46F`-`002BB47A`); otherwise the `+0` word is.
- **`002BBA8D`** in `002BAF80`: it compares the `+4` word with `dword [obj + 0xD4]`, and on a match calls `002B7210`
  with the `+2` word (`002BBA97`-`002BBAAD`).

**What the values mean is already on the map-screens page. This is prior art, found after the census.**
- The page's accessor table lists `003BE680` (line 284: "record `ecx` → its sub-block's C entry `byte[+2]` → returns
  `word[+0]`, writes `word[+2]`/`word[+4]`").
- Its walkthrough says "`003BE680` returns the map slot's default zoom" (line 914). It also says it "gives the slot's
  default zoom and two other levels. Mode 6 takes the first" (line 973).
- So the block is the record's **zoom set**: 240, 240 and 320 in 46 of 48 records.

What this record adds:
- the reader's address arithmetic lands exactly on the 8-byte C/D block that the lmap page and RC-35 describe. The page's
  "its sub-block's C entry `byte[+2]`" wording does not make that connection;
- `+6`/`+7` are not read.

RC-35 was answerable by joining the two pages, which is a note for the row's owner.

## Census and control

[`rc35_gap_readers.py`](rc35_gap_readers.py) -> [`.out`](rc35_gap_readers.out), FAILS 0:
- **Candidates.** Every function that forms a 20-byte stride (`imul 0x14`; `lea [x+x*4]` then `*4`; or a pointer stepped
  by `0x14`), within the call closure (3 hops) of the world-map widget's code, the referrers of its singleton `02B457E0`,
  and the lmap accessors: 258 functions.
- **Eight hits:**
  - the three known walkers;
  - `003BE680`, the reader above;
  - `0039BB60` / `0039BF50`, a stride of 160, not 20;
  - `0037FBA0`, which forms `20x + 4` for another array;
  - `00244DD0`, the widget factory stepping its own object by `0x14`.
- **Control PASS:** the three known walkers are found. `003C0740` is found only by v2's step form; v1 missed it, and that
  is why the form was added.

**Limit.** A reader outside that reach, or one that forms the address without a stride-20 idiom, is not covered. The
census found one reader, which answers "what reads it". It does not prove there is no other.

## For SWE2-CONTRACT (RC-35 owner)

Suggested row answer: **ANSWERED** - `003BE680` reads the block's words `+0`, `+2` and `+4` for the map screens'
record (`002B7B80` / `002BAF80`; three call sites). `+6`/`+7` are not read. The lmap page's section 10.5 can name it
beside the three walkers.
