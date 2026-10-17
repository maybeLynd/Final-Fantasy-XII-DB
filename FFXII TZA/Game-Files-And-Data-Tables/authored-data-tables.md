---
title: "Authored data tables: the 64-slot registry that holds the battle_pack.bin tables, the area .ard tables and the license boards, how each is bound, and how rows are found"
kind: "system"
category: "Game files and data tables"
addresses: "02EBF008, 02EBF200, 0208E680, 002368D0, 003843F0, 00384420, 00238850, 00236C30, 003845F0, 003846F0, 00237FC0, 00238160, 00238660, 00238880, 003847B0, 00384510, 0023A160, 003EA710, 003EA820, 00238260, 00233E00, 00238390, 0055BFF0, 0055B3F0, 003236B0, 00233C10, 00238A80, 00324510, 0020E600, 0020E620, 003876D0, 00322C50, 00309440, 01EEBCF8, 0032A230, 0208D300, 0208D308, 0208D310, 0208D318"
---

## What the player sees

Every number the battle system looks up, from an item's price and a spell's power to a character's
starting stats, a gambit's target and an enemy's level, comes from a table the game loads once at
start-up or each time the party enters a new area. When a table is missing, the game does not fall
back to a default: the lookup reads address 0 and the game crashes.

## How it works

The game reaches its authored tables through one array of 64 qword slots, `02EBF008` to `02EBF200`,
eight bytes apart. Each slot holds a pointer to a loaded table. Most hold a table from
`battle_pack.bin`; five are rebound from the current area's `.ard`; twelve hold license boards; a few
hold runtime blocks or are never used. All start null.

### The battle pack load

At start-up `002368D0` calls `003843F0(13h, 00238850, "STATIC")`, which files a kind-2 request for
file `13`<sub>h</sub>, `battle_pack.bin` (`00384420`: size from `0032E400(2, id)`, no request when it is
negative, allocation with `0036A190`, then `0032E620`). On delivery `00238850` rebases the pack's
directory with `003846F0(&0208E680, pack, 0)` and calls `00236C30(1)`.

The pack starts with a `u32` entry count (71) followed by 71 offsets, which the directory rebase
turns into addresses. `00236C30(1)` then sends 42 of the entries to slots:

- 33 through `003845F0(&slot, entry)`;
- `+2C`<sub>h</sub> to `02EBF160` with `003846F0(…, 0)` and `+F8`<sub>h</sub> to `02EBF170` with `003846F0(…, 1)`;
- five through bespoke binders: `+20`<sub>h</sub> `00238880`, `+38`<sub>h</sub> `00238160`, `+3C`<sub>h</sub> `00237FC0`,
  `+40`<sub>h</sub> `003847B0` and `+A0`<sub>h</sub> `00238660`;
- two stored with no internal fixup: `+04`<sub>h</sub> to `02EBF180` and `+11C`<sub>h</sub> to `02EBF200`.

`00236C30(0)` frees the pack, nulls `0208E680` and files the request again.

### Area tables

`003EA820(area)` loads the area's `.ard` (kind `15`<sub>h</sub>, file `area × 2`). It first unbinds the five
area slots and calls `0023A160(category, 0)` for each, so an area without a `.ard` leaves them null.
On delivery `003EA710` binds the sections through `0023A160(category, address)`:

| Category | `.ard` header field | Slot | Binder |
|---|---|---|---|
| 0 | `+10`<sub>h</sub> | `02EBF150` | `003845F0` |
| 1 | `+14`<sub>h</sub> | `02EBF168` | `003846F0`, depth 0 |
| 2 | `+18`<sub>h</sub> | `02EBF120` | `003845F0` |
| 3 | `+24`<sub>h</sub> (0 = none) | `02EBF148` | `003845F0` |
| 4 | `+28`<sub>h</sub> (0 = none) | `02EBF140` | `003845F0` |

Categories 0–2 are bound from their offsets unconditionally; 3 and 4 are null when the field is 0.
These five are the only slots that change when the area changes.

### Binding a table

`003845F0(slot, table)` stores the table in the slot first, so a null entry leaves the slot null. It
then adds the table's own low 32 bits to each of the header fields `+0C`<sub>h</sub>, `+10`<sub>h</sub>, `+18`<sub>h</sub> and
`+1C`<sub>h</sub> that is non-zero. A non-zero `+14`<sub>h</sub> is rebased, encoded with `0020E620` and walked as a
sub-directory `{u16 count; u32 entry[count + 1]}`: the first `count` entries go through `003846F0`
at depth 0 and the last, an end offset, is rebased in place.

`003846F0(slot, base, depth)` stores `0020E620(base)` and reads the `u16` count `n` at `+0`. For each of
the `n + 1` dwords after it, it adds `base` when the depth is 0 or the dword is the last; otherwise it
recurses into that entry with `depth − 1`. The result is a nest of offset tables `depth + 1` deep.

Nothing marks a table as bound: binding the same table twice adds its base twice.

### The bespoke binders

- **`00237FC0`, action_data (`02EBF138`).** After binding, it takes the largest row bytes `+38`<sub>h</sub> and
  `+39`<sub>h</sub> (ignoring `FF`<sub>h</sub>), stores the two extents at `0208D300`/`0208D301`, allocates an
  `extent38 × extent39` grid of `u16` named `gmbtAct` (`00384510`) at `0208D308` filled with `FF`<sub>h</sub>,
  and writes each row's index at `[+38h][+39h]`.
- **`00238880`, targetchip_data (`02EBF0D8`).** The same with row bytes `+16`<sub>h</sub>/`+17`<sub>h</sub>, extents
  at `0208D310`/`0208D311` and grid `gmbtTgt` at `0208D318`, storing `6000h + row`.
- **`00238160`, eitm_data (`02EBF0F8`).** After binding, it adds the table's `+18`<sub>h</sub> (an area after
  the rows) to each row's encoded `+28`<sub>h</sub>.
- **`00238660`, shop_data (`02EBF158`).** A three-level table with its own header (`+4` `u16` stride,
  `+6` `u16` count, `+8` rows). It adds the base to the slot, to the header's `+8`, to each row's `+4`
  (a sub-table) and that sub-table's `+8`, and to each sub-row's `+4` and its `+8`.
- **`003847B0`, status_data (`02EBF118`).** A tail jump to `003845F0`.

### License boards

The twelve slots `02EBF1A0`–`02EBF1F8` hold `board_1.bin` to `board_12.bin` (kind 2, files
`47`<sub>h</sub>–`52`<sub>h</sub>). At start-up `002368D0` zeroes them and calls `00238260(k)` for each:

- `00238260(k)` requests board `k` (`00384420`, name `BOARD`) when its slot is empty and
  `00233E00(k)` allows it; `00233E00` says yes when the board is already resident or fewer than six
  of the twelve are.
- A slot fills only when its read completes, through the setters `00238390` + `30h·k`, which free
  any old board (`003844F0`) and store the new one; `002383C0` is board 2's, slot `02EBF1A8`. Each setter
  stores its 32-bit argument sign-extended (`movsxd`, `00238396`, `002383C6`).
- The boot loop is the only caller of `00238260` and files the twelve requests back to back, so the
  six-board test passes for every board unless six reads finish while it is still filing.

The license screen reads a board through `0055BFF0`, indexing the slots by the signed byte
`[obj + 558h]` and reading the `licd` header (`+4` width, `+6` height, `u16` cells from `+8`).
`0055B3F0` fills `[obj + 558h]` from `003236B0(member)`, which returns the member's battle record byte
`+1C5`<sub>h</sub> when the record exists, its byte `+5` is 0 and its byte `+4` is below 7, and `FF`<sub>h</sub>
otherwise. For `FF`<sub>h</sub> it sets the board size `+559`<sub>h</sub> to 0, so slot −1 is never read.

### Finding a row

There is no shared accessor. Every reader computes, inline,

```python
row = 0020E600([table + 0x0C]) + u16[table + 0x08] × index
```

in 32-bit arithmetic (`003876D0`: `imul ecx, ebx; add ecx, eax`), so tables must lie below 4 GB.
A null slot or a zero row reference gives a base of 0 and the read still happens: `003876D0`, the
status timer reader, reads byte `+9` of address 0. Most readers do not bound the index; the ones
that do compare it with `+04`<sub>h</sub>.

`0020E600` adds the 64-bit base at `01F83530` to a zero-extended dword and `0020E620` subtracts its low
dword; those two instructions are the base's only references (see the arena page).

### Battle id classes

`00322C50(class, id)` checks an encoded battle id against the table its class names: the id is valid
when it lies in `[start, start + count)`, with the count read from the table's `+4` (0 for a null slot).
A class of 0 or above 32 is never valid. Class 1 is first remapped through `00309440`: the class in the `58`<sub>h</sub>-byte record at `01EEBCF8` for
the id's top nibble (5–19), −1 for nibble 15.

| Class | Start | Table |
|---|---|---|
| 2 | 0 | `02EBF130` chr_data |
| 3 | 0 | `02EBF120` `.ard` category 2 |
| 4 | 0 | `02EBF150` `.ard` category 0 |
| 5 | 0 | `02EBF100` dougu_data |
| 6 | `1000`<sub>h</sub> | `02EBF0F8` eitm_data |
| 7 | `2000`<sub>h</sub> | `02EBF098` eventitem_data |
| 8 | `3000`<sub>h</sub> | `02EBF0F0` maho_data |
| 9 | `4000`<sub>h</sub> | `02EBF0E8` waza_data |
| 10 | `5000`<sub>h</sub> | `02EBF0E0` gambit_data |
| 11 | `6000`<sub>h</sub> | `02EBF0D8` targetchip_data |
| 12 | `7000`<sub>h</sub> | `02EBF0D0`, never written, so no id is valid |
| 13 | `8000`<sub>h</sub> | the counts of `02EBF090`, `02EBF088`, `02EBF080` and `02EBF078` added together |
| 14 | `9000`<sub>h</sub> | `02EBF070` eis_data |
| 15, 30, 31 | `A000`<sub>h</sub> | `02EBF068` questreward_data |
| 16 | `B000`<sub>h</sub> | `02EBF060` price_data |
| 17 | `C000`<sub>h</sub> | `02EBF0C8` menkyo_data |
| 18 | `D000`<sub>h</sub> | `02EBF058` horidashi |
| 19 | `E000`<sub>h</sub> | none: `E000`<sub>h</sub>–`EFFE`<sub>h</sub> |
| 20 | 0 | `02EBF138` action_data |
| 21 | 0 | `02EBF128` comac_data |
| 22 | 0 | none: 0–3 |
| 23 | 0 | none: 0–8 |
| 24 | 0 | `02EBF110` mgccategory_data |
| 25, 32 | 0 | `02EBF038` license_data |
| 26 | 0 | `02EBF118` status_data |
| 27 | 0 | `02EBF050` attribute_data |
| 28 | 0 | `02EBF0B0` sobicategory_data |
| 29 | 0 | `02EBF040` ability_data |

### Grouped and nested tables

- **tutorial_data (`02EBF020`).** Its `+1C`<sub>h</sub> points to a group index: a count, then the end row of
  each group. `0032A230(group, key, &row)` scans the rows from the previous group's end to this one's
  for a row whose leading `u16` equals the key.
- **commandpack (`02EBF160`) and `.ard` category 1 (`02EBF168`).** Bound by `003846F0` at depth 0: a
  `u16` count and `count + 1` addresses, read in pairs as ranges.
- **word (`02EBF170`).** Bound at depth 1: up to 32 banks, each a counted list of text addresses.
- **WepJob_Matrix (`02EBF180`).** `u16` stride (1), `u16` count (23), then one byte per row.

### Runtime blocks and dead cells

- `02EBF190` is not a table. It always holds `002EF640() + 4E68Ch`, the battle state block (magic
  `05071901`<sub>h</sub> at `+0`; 40 party battle records of `1C8`<sub>h</sub> bytes from `+8`), written by `00233C10` when
  null and by `00238A80`.
- `02EBF178` is written only by `00324510`, a builder for 301 kind-`1A`<sub>h</sub> files that never runs: its
  state `022C27A0` is touched only inside it, and nothing stores the state 1 that starts it.
- `02EBF188` has 93 writes and no read.
- `02EBF0D0` is read once (class 12) and never written. `02EBF198` has no reference at all.
- `02EBF200` (`license_board.bin`) is stored once and never read.

## Layouts

```python
table header   +0x00 'st2e' (or u16 count on 003846F0 tables), +0x04 u32 row count, +0x08 u16 row stride,
               +0x0A u16 0, +0x0C row array, +0x10 reference, +0x14 encoded sub-directory,
               +0x18 reference, +0x1C reference (all offsets from the header until bound)
battle_pack    +0x00 u32 count (71), +0x04 + 4k: offset of entry k
licd board     +0x00 'licd', +0x04 u16 width, +0x06 u16 height, +0x08 u16 cells[width*height]
.ard header    +0x10 / +0x14 / +0x18 / +0x24 / +0x28 section offsets (categories 0-4), +0x2C section for 003DCF00
```

The header fields are listed access by access in
[`authored-data-tables-header-accesses.tsv`](authored-data-tables-header-accesses.tsv), and the slot
references in [`authored-data-tables-slot-accesses.tsv`](authored-data-tables-slot-accesses.tsv).

## Shipped data

The `us` `battle_pack.bin` (281,128 bytes), by directory offset; shapes are rows × row bytes.

| Slot | Entry | File | Shape |
|---|---|---|---|
| `02EBF008` | `+118`<sub>h</sub> | movie | 49 × 8 |
| `02EBF010` | `+114`<sub>h</sub> | move_support | 120 × 8 |
| `02EBF018` | `+0C`<sub>h</sub> | battle_message | 102 × 8 |
| `02EBF020` | `+70`<sub>h</sub> | tutorial_data | 6 × 20 |
| `02EBF028` | `+F0`<sub>h</sub> | savemember_data | 226 × 44 |
| `02EBF030` | `+F4`<sub>h</sub> | saveparty_data | 50 × 208 |
| `02EBF038` | `+34`<sub>h</sub> | license_data | 361 × 24 |
| `02EBF040` | `+EC`<sub>h</sub> | ability_data | 129 × 8 |
| `02EBF048` | `+AC`<sub>h</sub> | shoki_data | 32 × 4 |
| `02EBF050` | `+A8`<sub>h</sub> | attribute_data | 8 × 2 |
| `02EBF058` | `+E8`<sub>h</sub> | horidashi | 128 × 36 |
| `02EBF060` | `+74`<sub>h</sub> | price_data | 128 × 4 |
| `02EBF068` | `+9C`<sub>h</sub> | questreward_data | 256 × 12 |
| `02EBF070` | `+98`<sub>h</sub> | eis_data | 512 × 12 |
| `02EBF078` | `+94`<sub>h</sub> | s_daiji_data | 0 × 10 |
| `02EBF080` | `+90`<sub>h</sub> | q_daiji_data | 416 × 10 |
| `02EBF088` | `+8C`<sub>h</sub> | g_daiji_data | 32 × 10 |
| `02EBF090` | `+88`<sub>h</sub> | m_daiji_data | 64 × 10 |
| `02EBF098` | `+84`<sub>h</sub> | eventitem_data | 512 × 10 |
| `02EBF0A0` | `+80`<sub>h</sub> | yugoyaku_data | 16 × 13 |
| `02EBF0A8` | `+14`<sub>h</sub> | jochumodel_data | 0 × 4 |
| `02EBF0B0` | `+18`<sub>h</sub> | sobicategory_data | 32 × 4 |
| `02EBF0B8` | `+10`<sub>h</sub> | damagemp_data | 25 × 8 |
| `02EBF0C0` | `+1C`<sub>h</sub> | drop | 4 × 37 |
| `02EBF0C8` | `+6C`<sub>h</sub> | menkyo_data | 32 × 8 |
| `02EBF0D8` | `+20`<sub>h</sub> | targetchip_data | 256 × 32 |
| `02EBF0E0` | `+24`<sub>h</sub> | gambit_data | 40 × 64 |
| `02EBF0E8` | `+7C`<sub>h</sub> | waza_data | 24 × 8 |
| `02EBF0F0` | `+78`<sub>h</sub> | maho_data | 81 × 8 |
| `02EBF0F8` | `+38`<sub>h</sub> | eitm_data | 557 × 52 |
| `02EBF100` | `+4C`<sub>h</sub> | dougu_data | 64 × 12 |
| `02EBF108` | `+28`<sub>h</sub> | hpmpbase_data | 99 × 2 |
| `02EBF110` | `+30`<sub>h</sub> | mgccategory_data | 5 × 4 |
| `02EBF118` | `+40`<sub>h</sub> | status_data | 32 × 40 |
| `02EBF128` | `+48`<sub>h</sub> | comac_data | 21 × 4 |
| `02EBF130` | `+44`<sub>h</sub> | chr_data | 40 × 128 |
| `02EBF138` | `+3C`<sub>h</sub> | action_data | 543 × 60 |
| `02EBF158` | `+A0`<sub>h</sub> | shop_data | own header |
| `02EBF160` | `+2C`<sub>h</sub> | commandpack | offset list |
| `02EBF170` | `+F8`<sub>h</sub> | word | 15 banks |
| `02EBF180` | `+04`<sub>h</sub> | WepJob_Matrix | 23 × 1 |
| `02EBF200` | `+11C`<sub>h</sub> | license_board | 24 × 24 `licd` |

The other 29 entries (menus, help and list-help text, quest titles and others) are not registry
slots. All 48 shipped `board_N.bin` files are 1,160-byte 24 × 24 `licd` boards.

## State

The 64 slots, the pack pointer `0208E680`, the two lookup grids and their extents
(`0208D300`–`0208D318`), and the battle state block behind `02EBF190`.

## Modding notes

- Keep every table's header offsets relative to the table: the binder adds the table's address once
  at load.
- The id classes take their ranges from each table's row count at `+04`<sub>h</sub>; an id is `start + row`.
- Row bytes `+38`<sub>h</sub>/`+39`<sub>h</sub> of action_data and `+16`<sub>h</sub>/`+17`<sub>h</sub> of targetchip_data place the row in
  the menu grids; use `FF`<sub>h</sub> to leave a row out.
- Categories 0–2 of an `.ard` are bound even when their offset is 0, which binds the file header as
  a table and corrupts it; every `.ard` needs all three.
- Never leave a table out of the pack or an area's `.ard` that a reader needs: a missing table is read
  at address 0.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): the 32-bit address encoding.
- [File size tables](file-size-tables-fst.md): the file kinds the pack, `.ard` and boards are loaded by.
- [Resource ownership and disposal](resource-ownership-and-disposal.md): how other loaded data is owned.
