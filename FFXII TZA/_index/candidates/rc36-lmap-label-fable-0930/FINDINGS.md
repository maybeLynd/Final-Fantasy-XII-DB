# RC-36 findings: who reads a marker's `+0x0C` label id (FABLE, 2026-09-30)

Static, tier 1 (bodies read to their returns). Receipts: `classify.py` → `classify.out`, exit 0, `FAILS 0`, run at
HEAD `63f4b8f89` on 2026-09-30. Shipping image `73461D08…`. Nothing outside this directory was edited.

## Answer

Array B's `+0x0C` is read, as a **dword**, by two functions. Both are in the location map's point-list chain, and both
pass it to the high-pool text resolver `002F9920` (bank = id ÷ 10,000, so 60,2xx lands in bank 6, the 285-entry
`st2e` bank that EXP-002 lists).

1. **`003C25BD`, in `003C2320`'s kind-1 (marker) arm. This is the label that gets drawn.**
   - `mov ecx, dword ptr [r15 + 0xc]` → `003C2629 call 002F9920` → `003C262E mov [row + 0x10], rax`.
   - The row then goes through the page's list build: `00402C30` copies the 0x30 row and measures its `+0x10` string
     through `0029CD00`.
   - The label pass `004044D0` draws it. For each record with byte `+2 == 1` (row `+2` = the point kind, `003C23BE`),
     it draws `[rec + 0x10]` through `002D8670` (`004046AB`) at `+0x18` / `+0x1A`. Those are the marker's own `+0x8` /
     `+0xA` (`003C23A6`–`003C23B2`), scaled by the zoom and offset by the origin.
   - **So the location map draws the marker's "To X" destination string from `menu_mapname.bin` at the marker's
     `+8` / `+0xA` position.**
   - The text is grey (`0x80404040`) unless row `+0x1C` bit 0 is set (`0040463F`–`00404645`). That bit is the marker's
     `+0x12` flag gate (`003C24F0`, `003C250D`).
2. **`003BEB06`, in `003BE950`, the directional next-target search.** It is not a draw.
   - `003BE950` takes the arm where a triple's kind is not 0. There, `mov ecx, dword ptr [rbx + 0xc]` →
     `002F9920` → `0029CD00` measures the string. The measured size, halved, is added to B `+8` / `+0xA`
     (`003BEB2C`–`003BEB5E`) before the distance test `003BD6F0`.
   - So a marker's cursor target is the centre of its label box. The result is the row's direction byte
     `+8..+B` (`003C269F`).

**When the label is replaced**, all in `003C2320`:
- **Locked marker.** If the `+0x12` gate is closed and bit 14 of `00377A40` is clear for the zone that `+0x14`
  names, the row gets the low-pool text `0x3EC` instead (`003C25B1`–`003C25B6`). The label pass drops that string
  unless `00254A10` answers (`00404676`–`00404695`). What text `0x3EC` says was not resolved.
- **No label id.** If `+0x0C` is `0xFFFFFFFF`, the row gets the name of the destination sub-location instead: the
  `menumap_common` entry at byte `+0x11`, its `+4` name id (`003C25C6`–`003C2613`). **No shipped marker takes this
  arm.** Section D counts 0 of 111 in all 9 copies.

**SWE2-CONTRACT's P4 needs a correction.** Its pin window stops at `003C253F`, the arm's first `003BDDE0` call
(`lmap_readers.py` line 102). The arm runs on to `003C2632`, and `003C25BD` is inside it. So the sentence "That arm
does not read `+0xC`" in lmap §10.5 is wrong, and so is the register row's "(P4)" clause. The pin itself is true of
its window. This is routed as a finding. Nothing was edited.

## Per-load table

Arrays: **A** = zones, **B** = markers, **C** = zone routes. "wmap" = `menumap_world.bin` at widget `+0xD8`.

| load | base traced to | array | evidence |
|---|---|---|---|
| `003BCB05` | `[[02B457E0]+0xD8]`: the wmap file header | wmap, not lmap | `003BCAF5`, `003BCAFE` |
| `003C000F` | the same wmap header | wmap | `003BFFFA`, `003C0008` |
| `003C00DF` | the same wmap header | wmap | `003C00CA`, `003C00D8` |
| `003C019F` | the same wmap header | wmap | `003C018A`, `003C0198` |
| `003BD116` | a wmap `word[+0xA]` table entry (stride 0x1C) | wmap | `003BD057`, `003BD05E`, `003BD09C` |
| `003BCEEC` | the `r8` argument, a C entry (from `003C0740`'s walk, `mov r8, rdi` at its one call `003C083F`) | C | `003BCDEB`, `003BCDFA` |
| `003BCBAF`, `003BCBF7` | the `rcx` argument. All 8 callers pass an A point (section K). Two of them rest on data or on a stale out-slot (see Uncertain) | A | `003BCBB3`; K rows |
| `003BF9CA` | `rcx`; its only caller passes `003C2320`'s kind-0 point | A | `003C23C5`, `003C2477`, `003C2482` |
| `003C11A6`, `003C11CA`, `003C11DC`, `003C11FE` | `rdx`; both callers pass the kind-0 point `rbx` | A | `003C118D`, `003BCE6B`, `003BCE73`, `003BCED7`, `003BCEFA` |
| `003C17A2` | an inline point with `r8d = 0` (index below countA) | A | `003C1765`, `003C178A`, `003C179D`, `003C17A0` |
| `003C1936` | `rdx`; all 8 callers are behind a kind-0 `jne` (the other arm goes to `003C0F70`) | A | `003C18B7`; K rows |
| `003BEAAC` | a triple point whose triple kind is 0 | A | `003BEA7E`, `003BEA83`, `003BEA86` |
| `003BF27E`, `003BF30A`, `003BF363` | `003BED70`'s local triples, stored only when kind is 0 (a `003BE1E0` result is A, X3) | A | `003BEEDE`/`003BEEE0`, `003BF14E`/`003BF150`, `003BF263`, `003BF300` |
| `003C23CB`, `003C23F3` | `003C2320`'s point in the kind-0 arm | A | `003C2354`, `003C23C2`, `003C23C5` |
| `003C25A4` | `003BDDE0`(current record, B `+0x14`). In the data it resolves to the linked zone, which goes to `00377A40` | A (data) | `003C2567`, `003C258B`, `003C2590`, `003C25A8` |
| **`003C25BD`** | **`003C2320`'s point in the kind-1 arm (the triple kind from `003BF430`'s out-slot)** | **B** | `003C2354`, `003C23C5`, `003C248A`, `003C2565`, `003C25AF`, `003C2629`, `003C262E` |
| **`003BEB06`** | **a triple point whose triple kind is not 0. The triple array is `003BE3A0`'s, passed through `003C2320` argument 5** | **B** | `003C263D`, `003C2690`, `003BEA7E`, `003BEA83`, `003BEA86`, `003BEB0C` |
| `003C27B0` | `003C26C0`: widget `+0x120 + k·0xA8`, a `menumap_subNN` cache slot's file | not lmap | `003C26DA`, `003C26F7`, `003C271C` |
| `003C0416` (CONTROL) | `003BF430` with kind 0 (`003C040F` `cmp [rsp+0x58],0`, then `jne`) | A: PASS | `003C040A` |
| `0024A33D` | the image member callback's slot `+0x20` | not lmap | `0024A330` |
| `002543FB` | the header of the table at `[020927D0]` | not lmap | `002543F4` |
| `002F99BD` | an `st2e` bank record (inside the resolver itself) | not lmap | `002F9926` |
| `00369B49` | `rcx − 0x40`, the resource block header. **This does receive the lmap buffer, as a release** (`003BC5E0` → `003BC5EC`), but it reads the block header, not a point | not a point | `003698C1`, `003698BC` |
| `0036AE1C`, `0036B235`, `0036BD6C` | resource-pool slot descriptors | not lmap | `0036AE24`, `0036B238` |
| `0039BC4A`, `0039BFFB` | `0039BB60`'s slot table. The widget passes `+0x108`, not `+0xE0` | not lmap | `003BC630`, `003BC63C` |
| `003BC92B` | the widget procedure's message payload | not lmap | `003BC919` |
| `003DFB6C`, `003DFBD2` | a cached record's word table | not lmap | `003DFB63`, `003DFBB5` |

## Uncertain / edge loads

- **`003BE810` → `003BCBA0` (`003BE8DA`). A B point can reach a field-id reader here, in principle.**
  - `003BE810` feeds `003BDDE0` a direction selector byte. 214 of 1,701 selector bytes index a B point (section D).
  - When that B point is not enabled, `003BDDE0` takes its `003BDF06` path. That path returns a same-`+0x11` enabled
    B point and leaves the kind out-slot `[rsp+0x34]` unwritten (X4).
  - If the stale value is 0, `003BCBA0` reads that B's `+0x0C` as a field id (`003C0380`, `MapRef_GetPersistenceGroupId`).
  - Whether this happens depends on the runtime gate state and the stack's contents. It would be a type confusion, not
    a label use.
- **`003C0F70` → `003BCBA0` (`003C0FEE`) and `003C25A4` have no kind test.** They read A only because B `+0x14` never
  indexes a B point: 106 index an A point, 5 are `0xFF`, and 0 index a B point, in all 9 copies. The code does not
  enforce that.
- Every other A verdict follows from a pinned kind test or from X2/X3.

## Reach limit (what "only these two" covers)

- **The census.** The census is every word or dword `+0xC` load (`movzx`/`movsx`/`mov`/`cmp`) in the 258-function
  closure: 3 E8/E9 hops from the widget code and the `02B457E0` referrers. That is `rc36_label_readers.py` Part 2 plus
  Part 1.
- **Where B pointers come from.** Only the 14 functions that load `[[02B457E0]+0xE0]` form lmap addresses (section R:
  158 rip references in 77 functions, and 0 image-base-relative references).
  - The functions that return a point are `003BF430`, `003BDDE0` and `003BE1E0`.
  - Every consumer of a returned point, and the triple chain (20 functions), sits inside the closure. None is outside.
- **Callers of the parameter-taking functions.** These were checked through E8/E9 (rawcalls.json), a `0F 8x` jcc
  sweep, rip-relative references and DIR64 relocations, with each site checked against the instruction boundary. That
  found 0 jcc sites and 0 real references. Three raw candidates were mid-instruction bytes.
- **Folded displacements.** In the root functions, every memory operand with a displacement of 0x0C–0x13 is listed.
  None is a folded B `+0xC` read.
- **What is not covered.**
  - A B point copied wholesale (`movups` or `memcpy`) somewhere and read at a different displacement. No such copy
    was seen in the bodies read. `003BCDE0`'s copy loop moves C entries.
  - A byte-width read of `+0x0C`.
  - Code outside the closure that receives a point through a structure field, not an argument.

## Side readings (static, for the owner)

- **B `+0x11` is the destination sub-location index.**
  - `003C2320` passes it as the record number to `003BDDE0` (`003C253F`), with `+0x15` as the point in that record.
  - The `0xFF` fallback names `menumap_common[+0x11]`.
  - The `0xD` → `0x2F` remap is sub-location 13 → 47: Giza Plains dry season → rainy season, when the flag `0x107` /
    widget `+0xD0` bit 14 answers.
  - All 111 values are below 48.
  - B `+0x14` is a zone of the current record (it feeds `00377A40`, gating the label).
- **RC-35 lead: the map-screens page already names a reader of the 8-byte block.**
  - `003BE680` forms `rec + 4 + 24·(A+B) + 20·C` and returns block `+0`, writing `+2` / `+4`
    (`003BE6B7`–`003BE6EF`).
  - The map-screens page reads it as the slot's default zoom and two other levels
    (`the-map-screens-and-their-shared-map-data.md` lines 914 and 973).
  - Its row at line 284 calls the address "the sub-block's C entry `byte[+2]`". That is loose: `byte[+2]` is countC.
  - The block values `f0 00 f0 00 40 01` are 240 / 240 / 320.
