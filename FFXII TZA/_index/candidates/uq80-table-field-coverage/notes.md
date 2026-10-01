# UQ-80 - row meaning of the authored tables behind the class slots (research notes, 2026-09-27)

Read-only pass. Nothing under the repository was edited. Every number below is copied from
`coverage_run.txt` (the output of `uq80_coverage.py`) or from the named script's output.

## What was measured

23 `st2e` sections of the `us` `battle_pack.bin`: the 20 sections the registry's UQ-80 box lists
(18 lines, the key-item line is three sections) plus the three class slots with their own binders
(`eitm_data` +0x38, `status_data` +0x40, `action_data` +0x3C). The box's four non-pack class slots
(`02EBF150`, `02EBF120`, `02EBF0D8`, `02EBF0D0`) are not `battle_pack.bin` entries and are named, not
measured.

## Method

1. **Headers** (`pack.py`): each section located by its directory dword, magic `st2e`, header `+0xC` = 0x20,
   rows fit before the next section. All 23 shapes reproduce the registry box / encoded-id page 2.5 (control C1).
2. **Tallies** (`tally.py`): every byte, aligned u16 and u32 of every row: distinct count, min, max, top values.
3. **Reader sweep** (`trace.py`, output `trace_all.txt`): for each slot, every function that loads it
   rip-relative (from the instruction cache `y1p_all.txt`), minus the registrar `00236C30`; then a flow-aware
   ("may", union at joins) register-tag dataflow per function: T = [slot], O = [T+0xC], W = [T+8],
   R = `0020E600`(O), P = W x id, X+n = row pointer plus a known offset, X*n = a strided walk from n.
   Every memory operand based on a row pointer is printed with its access width and row offset. Functions
   returning a row pointer (accessors) seed rax at every call site in pass 2, including callers that never load
   the slot. 739 row reads, 91 call sites passing a row pointer on (not followed). Image-base-relative forms:
   the only `[reg + 0x2D9Fxxx]` operands in the image are `0x2d9f1a0` and `0x2d9f278` (02EBF1A0 / 02EBF278),
   outside the slot band 02EBF008..02EBF180, so the rip census is complete for these slots.
4. **Coverage by page**: grep of every table name / slot, plus an exact-token index of every 8-hex address on
   every page (`citecov.py` -> `reader_citations.tsv`) to find which reader instructions pages already cite; then
   the cited passages were read to decide whether a page states the field's *meaning in row terms*. Pages that
   state a meaning only for a query-record field were not counted as row coverage (licence +2 / +4 / +6 are
   composed through the filler and marked `pass`).
5. **Meaning** only where a reader's use or the data supports it; the query filler `0031C5D0` was read arm by
   arm to see which query-record slot each row field lands in, and the consumers of those slots were read
   (sort comparators `002D01A0` / `002CFFE0` / `002D0070` / `002CFDA0` on query +0x30, the shop list filler
   `0057DED0` on query +0x28 as the unit price).
6. **Census** (`uq80_coverage.py` + `uq80_manifest.tsv`): the manifest has one row per field / pad span per table;
   the script re-reads the pack and the exe, checks every row (offsets, overlaps, pad constancy over every
   shipped row, and that each of the 278 cited reader instructions decodes to a memory operand of the stated
   displacement and width, and that each cited page exists), then prints the coverage and the exact residue.
   Deterministic (two runs identical); exits 1 on any FAIL. `fields_emit.py` writes the per-table
   `<table>-fields.tsv` from the manifest, the tallies and the sweep.

## Controls (all PASS in `coverage_run.txt`)

| id | what | known answer | result |
|---|---|---|---|
| C1 | 23 section shapes read from the pack | registry box + encoded-id 2.5 count x size | 23/23 |
| C2 | file names through the pointer table at `01E4D830` (a .data read; a .text-only offset corrupts it) | manifest slot k = pack entry k | 23/23 names match |
| C3 | price_data rows equal to 1 | "45 rows hold 1" (encoded-id 2.8) | measured 45 |
| C4 | questreward rows with a first id | rows 128-172 (encoded-id 2.8) | exactly 128..172 (45) |
| C5 | action_data +0x15..+0x17 zero; +0x26 on the summon rows | "0 on all 543"; 13 rows 27-39 (action page) | both reproduced |
| C6a-c | reader instrument re-derives three published row layouts from the bodies | `002FD530` {u32 +0, u16 +4,+6,+8,+0xA}; `002FD780` three (u16, u8) pairs from +4; `002FD640` six u16 | exact sets |
| C6d | negative: the same instrument on a slot the function does not load | empty | empty |
| C7 | reader-check sensitivity | `002FD5A9` accepted as dword [row+0]; wrong width and wrong disp rejected | as expected |
| C8 | pad-check sensitivity | dougu +0 varies (52 values), dougu +1 constant | as expected |
| C9 | joins behind three `pass` meanings | dougu +7 64/64, maho +2 81/81, waza +2 24/24 | as expected |
| C10 | the sort-key comparator reads query +0x30 | `002D01CE`, `002D01D8` | as expected |

Sweep (`trace.py`) known answers, checked by hand against pages: it finds the class-5 arm reads the
encoded-id contract cites (`0031C723`..`0031C75F`, header reads `0031C733`..`0031C75A`), the licence LP deduction
the licence-check page cites (`003239C3`), the gambit preset loader's reads (`00327D45`, `00327D4F`, cited
`00327D42`..`00327D82`), and the bundle handlers' rows (C6).

**Two defects the controls caught in my own instrument, fixed before the numbers above:** the first linear
version missed the four class-5 row reads after a join (`0031C81A`..`0031C845`); the second attributed the
walk `00316FF0 movzx ecx, word [rsi]` (rsi = row + 0x58) to row offset 0. The shipped `trace.py` tracks
offsets through `lea` / `add imm` and widens loop walks.

## Result

- **Fully covered by existing pages (every byte, page meaning or page-declared pad): 4 of 23** -
  `gambit_data`, `eis_data`, `questreward_data`, `attribute_data`. `horidashi` has a page meaning for every
  field; its six remaining bytes are alignment pads the page does not list (zero on all 128 rows).
- **Mapped in this pass: 19 tables needed a map; after the pass 15 of 23 have no residue.**
- **Residue: 8 tables, 63 unmapped bytes** (exact list, from the script):
  `chr_data 0x07,0x08,0x09,0x2d,0x32,0x74,0x76,0x78,0x7a,0x7b,0x7c; m_daiji 0x00,0x01; g_daiji 0x00,0x01;
  q_daiji 0x00,0x01; menkyo_data 0x04; eitm_data 0x06,0x10,0x1b,0x1c,0x1d,0x1e,0x20,0x21,0x22,0x23,0x24,0x25,0x27,0x2c,0x2d,0x30,0x31,0x32,0x33;
  status_data 0x11,0x12,0x14,0x15,0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f;
  action_data 0x04,0x0a,0x0b,0x1c,0x1d,0x1f,0x20,0x21,0x28,0x30,0x31,0x3a`.

## Per-table summary (page / pass / pad / residue bytes)

- **chr_data** 40 x 128 (45 / 51 / 21 / 11). New: +0x04..+0x06 the special-sequence candidate ids (party rows
  0-5 = their three Quickening action rows 208-225); +0x18 / +0x19 HP scale (`002F8E50`: stats+8 x (b18+1) x b19 / 100)
  and +0x1D MP percent (`002F9180`); +0x2B the perception range (unit +0x68, composing the unit-definition page
  with the battle-unit field map); +0x34 ten counts, +0x58 ten item ids, +0x3E gil - granted on activation by
  `00316DF0`, and +0x58 is also the only item list an item action may use (`003062C0`..`003062D2`, reason 0xF);
  +0x48 innate status mask (-> status word 2) and +0x4C refused-status mask (-> status word 3, 0x8801FFFE on
  the 13 espers); +0x70 the definition (model) key `0031C2F0` returns for party ids. Residue: +0x07 (read by
  `0031B8E0`, meaning open), +0x32 (read by `002FA0E0` for the summon presentation, meaning open), and eight
  bytes with no reader (+0x08, +0x09, +0x2D, +0x74, +0x76, +0x78, +0x7A..+0x7C).
- **dougu_data** 64 x 12: +0 sort key, +4 icon, +7 action row, +8 name, +0xA price (Potion 60, Hi-Potion 180). Complete.
- **eventitem_data** 512 x 10: +0 price, +2 description id, +4 icon, +6 name, +8 sort key. Complete.
- **maho_data / waza_data** 81 / 24 x 8: +0 price, +2 action row, +3 icon, +4 name, +6 sort key. Complete.
- **gambit_data** 40 x 64: page-complete (two u16[12] arrays and two zero spans, re-verified).
- **m/g/q_daiji** 64 / 32 / 416 x 10: +2 sort key, +4 icon, +6 description id, +8 name. Residue +0x00 u16
  (m: equal to the row index on 48 rows; g: 64-91; q: 96 and up) - no reader in the slot-loading functions.
- **eis_data / questreward_data** 512 / 256 x 12: page-complete (encoded-id 2.8).
- **price_data** 128 x 4: the u32 lands in the class-16 query's +0x28, the slot the shop list filler reads as
  the unit price; no other reader. Not shown: that a class-16 id ever reaches a shop list.
- **menkyo_data** 32 x 8: +0 name, +2 the action id `00306340` hands to the usable test `003064F0`
  (rows hold 265-296). Residue +0x04 (a permutation of 0-31, row index on 25 rows, no reader).
- **horidashi** 128 x 36: page-complete plus six pads.
- **comac_data / mgccategory_data** 21 / 5 x 4: +0 a text id -> query +0x08, +2 name. Complete.
- **license_data** 361 x 24: rows +0, +5, +7, +8..+0x17 stated on pages in row terms; +2 description, +4 LP cost
  and +6 square kind composed here from the licence-board view's query-record reading through the filler.
- **attribute_data** 8 x 2: page-complete (name). **sobicategory_data** 32 x 4: +0 description id (0 on all rows), +2 name.
- **ability_data** 129 x 8: +0 description id, +2 name, +4 amount (+5 is its high byte: 1 on the six rows with
  amount >= 256), +6 the timer slot 0-7 into stats +0x17C (0xFF none). Complete.
- **eitm_data** 557 x 52 (15 / 5 / 13 / 19): new +8 sort key, +0xE description id (0 on all rows), +0x12 price.
  Residue 19 bytes: all but +0x24 have readers in the sweep (listed in `eitm_data-fields.tsv`); the
  subtype union +0x18..+0x23 (selected by `0031E9A0`) was not decoded beyond the page-stated bytes.
- **status_data** 32 x 40: `_types` covers 26 bytes. Residue +0x11, +0x12, +0x14..+0x1F: values are 0xFF or
  25-31 (the shape of the list-order keys), no reader.
- **action_data** 543 x 60: page covers 39 bytes with meaning; seven unlisted bytes are zero on all rows
  (+0x27, +0x29..+0x2B, +0x32, +0x33, +0x37). New: +0x38 / +0x39 are a (family, tier) key - the binder
  `00237FC0` builds the grid at `0208D308` (dims `0208D300` / `0208D301`) holding the action row at
  [b38 x dim + b39] (`00238103`..`00238132`); the page says "reader not found". Residue = the page's own
  shape-only fields (+0x04, +0x0A..+0x0B, +0x1C, +0x1D, +0x1F..+0x21, +0x28, +0x30..+0x31, +0x3A).

## Contradictions and leads found (not routed; for the caller)

1. **Encoded-id page 2.8, price_data range.** "45 rows hold 1, the rest values from 30 to 11,160": 45 is right,
   the range is not - the other 83 rows run 15 .. 999,999 (row 25 = 15, row 77 = 999999; rows 118-127 hold
   1118-1127). The same paragraph's "nothing consumes it" holds for gameplay code, but the filler does copy it
   into query +0x28, the price slot.
2. **CONTRACT-periodic-tick section 8** attributes "`+6` effect-timer slot index, `0xFF` meaning none" to
   `status_data.bin`. status_data +6 is the class word and holds no 0xFF in 32 rows (0 x13, 32 x10, 223 x3 ...);
   the reads with that shape (`0030EA9D`, `00385619`, `0039001D`: bound 7, 0xFF = none, index into stats +0x17C)
   all load `[02EBF040]`, ability_data. Appears to be a misattribution; worth a second reader before correcting.
3. **Action page +0x38**: "reader not found" - `00237FC0` reads +0x38 / +0x39 four times (above).
4. **Action page +0x28**: "the 26 Esper attacks (Red Spiral 120, White Whorl 121 ...)" - the 26 non-zero rows are
   208-233; rows 208-225 are the 18 Quickenings (+0x22 = 0xC000..0xC011), so "Esper attacks" is a mislabel.
5. **`_types` LicenseNodeRecord** says the whole 24-byte record is "HONESTLY EMPTY"; pages map +0, +5, +7, +8 in row
   terms, and the filler composes +2 / +4 / +6.
6. **Unit-definition page 2.3** still says "the registry page records its 456-byte rows"; the registry corrected
   that on 2026-09-13 (those were runtime stats records), and the us stride is 128.

## Limits

- The reader sweep starts from functions that load the slot rip-relative, plus callers of accessors. A row pointer
  handed to another function (91 sites, listed as `arg` lines in `trace_all.txt`) is not followed, so every
  "no reader" in the residue is bounded to that population, not image-wide.
- `trace.py` depends on the scratch instruction cache `y1p_all.txt`; `uq80_coverage.py` does not (it decodes the
  cited instructions and the three control bodies from the exe directly).
- Only the `us` pack was tallied; the other eight language packs were not.
- "Sort key" rests on the four comparators passed to the sort helper `00249CE0`; that every list sorts through them
  is not shown. "Price" for loot / magick / technick / equipment rests on the class arm writing query +0x28 and
  `0057DED0` reading +0x28 as the unit price.
- `pad` means constant on every shipped `us` row and no reader in the sweep population.

## Files

`pack.py`, `tally.py`, `trace.py` (+ `trace_v1.py`, the linear first version kept for the record), `summ.py`,
`citecov.py`, `joins.py`, `fields_emit.py`, `uq80_coverage.py`, `uq80_manifest.tsv`; outputs `coverage.tsv`,
`coverage_run.txt`, `trace_all.txt`, `readers_compact.txt`, `reader_citations.tsv`, `f0031C5D0.txt` (the filler),
and 23 `<table>-fields.tsv`.
