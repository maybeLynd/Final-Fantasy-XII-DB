# An independent reading of RC-35 (corroborating FABLE), and a withdrawn RC-36 reading (OPUS, 2026-09-30)

Register rows RC-35 and RC-36 (registered by SWE2-CONTRACT from `swe2contract-ddres-b5-0930/`). The page is
[`lmap-menumap-location-graph.md`](../../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/lmap-menumap-location-graph.md),
sections 3 and 10.5. The code evidence is static, on the certified image. The data checks read all nine shipped
`menumap_location.bin` copies. There is no original-code execution and no live run.

## RC-35: independent corroboration of FABLE's answer (OPUS)

FABLE answered RC-35 first (`9aac223bf`, `_index/candidates/rc35-lmap-gap-fable-0930/`; the three words are the map
screens' zoom set, per the map-screens page). This section was derived separately, before OPUS saw that commit. It
reaches the same reader, callers and values by a different census (a scan for ×5 multiplies in every function that
references the map object), so it corroborates FABLE's answer. It is OPUS's reading, not a review of FABLE's record;
that review is SWE2-AUDIT-SEM's.

**Answer.** `003BE680(n, &w2, &w4)` is the block's reader (`rc35_block_reader.py`, FAILS 0):
- It takes record `n` of `[[02B457E0] + 0xE0]`.
- It forms C = rec + 4 + 24·(countA + countB), and **block = C + 20·countC**. That is the C end itself; the C/D
  walkers `003BFF20` / `003C1070` add 8 more to reach D.
- It returns word `+0`, and stores word `+2` and word `+4` through its two out pointers (B1). Word `+6` is never read.

Its callers are the map-screen bodies `002B7B80` (`002B7FFA`) and `002BAF80` (`002BB45E`, `002BBA8D`). Each passes the
current record (`word [obj+0x138]`). Each picks one of the three words:
- mode `word [obj+0xBBE0] == 6` takes `+2`;
- otherwise it keeps the stored current value if one of the three equals it, else `+0`.

Each then divides `0xC80` (3,200) by the pick (`002B8052`/`002B8059`, `002BB4BA`, `002BBAEA`) (B2). The data: 46 of 48
records hold 240, 240, 320 (`f0 00 f0 00 40 01 00 00`); one holds 235 ×3 and one 210 ×3; word `+6` is 0 in all.

**Reading.** The three words are the per-location values the location map divides 3,200 by. That reads as scale steps.
The page should call them that only as a candidate; the code shows a divisor, not a unit.

**Completeness (B3).** Every function that references the map object `02B457E0` was scanned for a ×5 multiply
(`lea r, [r + r*4]`, the only way the code forms 20·countC). Only four have one:
- `003BE680`;
- the two walkers;
- `003BD1B0`, whose multiply scales its own 40-byte array (`003BD2B1`), not the table.

## RC-36: this reading is WITHDRAWN - FABLE found the reader it missed (OPUS)

**Withdrawn 2026-09-30, before publication.** FABLE's RC-36 (`9a4cd5784`, `rc36-lmap-label-fable-0930`) shows the location map DOES read a marker's `+0x0C`. OPUS re-read the site: `003C25BD mov ecx, dword ptr [r15 + 0xc]` is in `003C2320`'s marker arm, after the `003BDDE0` call at `003C258B`, and FABLE traces the value through `002F9920` into the draw row.

**Why this census missed it.** ~~`003C2320` receives its point pointer from its caller `003BE3A0` (`003BE554`), not from a call to the accessor `003BF430`.~~ *(Corrected 2026-09-30 on SWE2-AUDIT-SPEC's review `auditspec-review-lmap-rc35-36-0930`:)* The census followed only points returned by direct calls to `003BF430`, forward through registers, the stack and callees. It did not follow a point out through a return value, or reach functions fed from `003BE3A0`'s own array. It therefore missed both marker `+0x0C` readers FABLE found: `003C25BD` in `003C2320`, and `003BEB06` in `003BE950`, whose only caller is `003C2320` (`003C269A`). It also missed `003C25A4`, the `+0x0C` read of the point `003BDDE0` returns in `003C2320`, which is an array-A point in shipped data. The census below followed only `003BF430` results. Its completeness step scanned `+0x0C` operands only in functions that load the table at `+0xE0`, and `003C2320` does neither. SWE2-CONTRACT's P4 was likewise bounded to `003C248F`..`003BDDE0`.

**What still stands.** The kind tests listed below hold for the functions they name. The data check (`lmap_links.py`: every marker's `+0x14` indexes array A) still holds. Neither shows that no code reads a marker's `+0x0C`. The original text is kept, struck through, as the record of the error.

~~**Answer.** Every read of a location point's `+0x0C` is on a kind-0 (array A) point. None is on a marker (array B).
So nothing in the shipped code reads the 60,201–60,244 label id a marker carries. What the location map shows for a
marker's label does not come from that field.~~

~~**Census.** `lmap_field_reads.py` follows the point every one of the 25 calls to the accessor `003BF430` returns
(10 caller functions), through registers, the stack and callees, and logs every read of it. The `+0x0C` reads are in
nine functions (43 read sites). Each is gated to kind 0:
- `003BF920` (`003BF967`), `003C0380` (`003C040F`), `003BED70` (`003BEEDE`, `003BF14E`), `003C12B0` (`003C1480`),
  `003C1A20` (`003C1BDA`): the kind out-slot is tested, and a non-zero kind branches away before the read.
- `003BCDE0` (`003BCE73`, `003BCF43`, `003BCFB4`) and its callee `003C1180`: the same test before each read and call.
- `003C18A0` is called only for kind 0 (`003BF947`, `003BCE47`). Non-zero kinds go to `003C0F70`, which reads the
  marker's `+0x16`, `+0x14` and `+0x12`, never `+0x0C`.
- `003BCBA0` reads `+0x0C` of whatever it is given. Four of its callers pass kind-0 points by the tests above. The
  fifth, `003C0F70`, passes the point `003BDDE0` returns for the marker's link byte `+0x14`, with no kind test. That
  point is kind 0 because:
  - `003BDDE0` fetches point number `+0x14` of the same record;
  - **in all nine copies every marker's `+0x14` is 0xFF (`003C0F70` then skips the lookup) or an array-A index**:
    954 A, 45 FF, 0 B, 0 out of range (`lmap_links.py`);
  - `003BDDE0`'s fallbacks return array-A points only: `003BE1E0` returns point `003BDFF0(n)`, and `003BDFF0`
    considers kind-0 points only (`003BE03E`).
- The table loaders that reach points without the accessor were checked for a `+0x0C` operand. `003C1680`'s is the
  kind-0-only read SWE2-CONTRACT's P5 established. `003BC4E0`'s (`003BC92B`) is on the menu object's init-parameter
  block, not a point.~~

~~**Scope.** The `003BCBA0` path is kind-0 by the shipped data, not by a code test. A file whose marker `+0x14` indexed
array B would route that marker's label id into `003BCBA0` as a field id. Controls: the census finds `003BCDE0`'s known
`+0x0C` comparison (SWE2-CONTRACT C2), and `003C0740` is among the callers.~~

## Files (OPUS)

`rc35_block_reader.py` / `.out` · `lmap_field_reads.py` / `.out` · `lmap_links.py` / `.out`.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). Register and page incorporation: SWE2-CONTRACT.
