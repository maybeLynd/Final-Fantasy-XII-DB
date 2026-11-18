[Home](../../README.md) / [Game files and data tables](README.md) / Authored data tables

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Authored data tables: the 64-slot registry that holds the battle_pack.bin tables, the area .ard tables and the license boards, how each is bound, and how rows are found | system | Game files and data tables | Data tables and configs | The registry of 64 pointer slots at 0x02EBF008 through which the game reaches its authored data: which battle_pack.bin entry, area .ard section or license board each slot holds, the boot and area-change loads that fill them, the binders that turn stored offsets into addresses, the shared table header, the inline row formula and its 32-bit arithmetic, the encoded battle id classes and the table each one is checked against, the lookup grids built at bind time, how the twelve license boards load, and the runtime blocks and dead cells that share the array. | 0x02EBF008, 0x02EBF200, 0x0208E680, 0x002368D0, 0x003843F0, 0x00384420, 0x00238850, 0x00236C30, 0x003845F0, 0x003846F0, 0x00237FC0, 0x00238160, 0x00238660, 0x00238880, 0x003847B0, 0x00384510, 0x0023A160, 0x003EA710, 0x003EA820, 0x00238260, 0x00233E00, 0x00238390, 0x0055BFF0, 0x0055B3F0, 0x003236B0, 0x00233C10, 0x00238A80, 0x00324510, 0x0020E600, 0x0020E620, 0x003876D0, 0x00322C50, 0x00309440, 0x01EEBCF8, 0x0032A230, 0x0208D300, 0x0208D308, 0x0208D310, 0x0208D318 |

## What the player sees

Every number the battle system looks up, from an item's price and a spell's power to a character's
starting stats, a gambit's target and an enemy's level, comes from a table the game loads once at
start-up or each time the party enters a new area. When a table is missing, the game does not fall
back to a default: most lookups read from address 0 and the game crashes, and the few that first
check an id against the table's count refuse the id instead.

An id such as an item or a spell number also says which table it belongs to: each range of ids belongs to one table,
and the id less the start of its range is the row. The id is valid only while that row is below the table's row count.

## How it works

The game reaches its authored tables through one array of 64 qword slots, `0x02EBF008` to `0x02EBF200`,
eight bytes apart. Each slot holds a pointer to a loaded table. Most hold a table from
`battle_pack.bin`; five are rebound from the current area's `.ard`; twelve hold license boards; a few
hold runtime blocks or are never used. All start null.

### The battle pack load

At start-up `0x002368D0` calls `0x003843F0(0x13, 0x00238850, "STATIC")`, which files a kind-2 request for
file 0x13, `battle_pack.bin` (`0x00384420`: size from `0x0032E400(2, id)`, no request when it is
negative, allocation with `0x0036A190`, then `0x0032E620`). On delivery `0x00238850` rebases the pack's
directory with `0x003846F0(&0x0208E680, pack, 0)` and calls `0x00236C30(1)`.

`0x00384420(id, callback, name, arena, tag, flags)` returns 0 with no request when the size is negative¹. Otherwise it pushes the arena (`0x0036C1D0(arena, flags)`, `0x00384466`) and the tag
(`0x0036C1A0(tag)`, `0x00384472`), allocates the size top-down², labels a non-null block with
the name and the id³ and pops both⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00384457`-`0x0038445B` |
| ² | `0x0036A190`, `0x00384479` |
| ³ | `0x0036C660`, `0x00384481`-`0x0038448F` |
| ⁴ | `0x0036C110`, `0x0036C140` |

</details>

It then files `0x0032E620(2, id, block, size, descriptor)`¹ and returns the block. The stack
descriptor holds 0 at `+0x00`, the block's low 32 bits at `+0x08`, the callback at `+0x10` and 0 at `+0x18`². The null test at `0x00384481` skips only the label, so a null block is requested with
destination 0. `0x003843F0` gives arena 4, tag 6 and flags 4³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003844C9` |
| ² | `0x0038449E`-`0x003844BF` |
| ³ | `0x003843F4`-`0x00384402` |

</details>

The pack starts with a `u16` entry count (71), two zero bytes and 72 offsets: one for each entry and,
last, the end offset. The directory rebase (`0x00384727` reads the count; the loop to `0x0038478E` runs
count + 1 times) turns them into addresses. `0x00236C30(1)` then sends 42 of the entries to slots:

- 33 through `0x003845F0(&slot, entry)`;
- `+0x2C` to `0x02EBF160` with `0x003846F0(…, 0)` and `+0xF8` to `0x02EBF170` with `0x003846F0(…, 1)`;
- five through bespoke binders: `+0x20` `0x00238880`, `+0x38` `0x00238160`, `+0x3C` `0x00237FC0`,
  `+0x40` `0x003847B0` and `+0xA0` `0x00238660`;
- two stored with no internal fixup: `+0x04` to `0x02EBF180` and `+0x11C` to `0x02EBF200`.

`0x00236C30(0)` frees the pack, nulls `0x0208E680` and files the request again.

### Area tables

`0x003EA820(area)` loads the area's `.ard` (kind `0x15`, file `area × 2`). It first unbinds the five
area-table slots and calls `0x0023A160(category, 0)` for each, so an area without a `.ard` leaves them null. This
first unbind runs only when a file is loaded (root `0x02B5E0C0` non-null, `0x003EA883`, `0x003EA98D`), which it frees;
a size of 1 or more unbinds the five, again after a freed file, before the read is filed¹.
With no file
loaded and a size of 0 or less it unbinds nothing.
On delivery `0x003EA710` binds the sections through `0x0023A160(category, address)`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EA8DA`-`0x003EA90D` |

</details>

| Category | `.ard` header field | Slot | Binder |
|---|---|---|---|
| 0 | `+0x10` | `0x02EBF150` | `0x003845F0` |
| 1 | `+0x14` | `0x02EBF168` | `0x003846F0`, depth 0 |
| 2 | `+0x18` | `0x02EBF120` | `0x003845F0` |
| 3 | `+0x24` (0 = no section) | `0x02EBF148` | `0x003845F0` |
| 4 | `+0x28` (0 = no section) | `0x02EBF140` | `0x003845F0` |

Categories 0–2 are bound from their offsets unconditionally; 3 and 4 are null when the field is 0.
These five are the only slots that change when the area changes. `0x0023A160` jumps to the binder of its category¹ and returns without a store for a category outside 0 to 4².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A178`-`0x0023A1C1` |
| ² | `0x0023A1C6` |

</details>

### Binding a table

`0x003845F0(slot, table)` stores the table in the slot first, so a null entry leaves the slot null. It
then adds the table's own low 32 bits to each of the header fields `+0x0C`, `+0x10`, `+0x18` and
`+0x1C` that is non-zero. A non-zero `+0x14` is rebased, encoded with `0x0020E620` and walked as a
sub-directory `{u16 count; u32 entry[count + 1]}`: the first `count` entries go through `0x003846F0`
at depth 0 and the last, an end offset, is rebased in place.

`0x003846F0(slot, base, depth)` stores `0x0020E620(base)` and reads the `u16` count `n` at `+0`. A null `base`
stores 0 and returns¹. For each of
the `n + 1` dwords after it, from `+0x04`, it adds `base` when the depth is 0 or the dword is the last; otherwise it
recurses into that entry with `depth − 1`, passing the entry plus `base`, so the call's own store rebases the
dword too². The result is a nest of offset tables `depth + 1` deep.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0038470E` |
| ² | `0x00384759`-`0x0038476B` |

</details>

Nothing marks a table as bound: binding the same table twice adds its base twice.

### The bespoke binders

- **`0x00237FC0`, action_data¹.** After binding, it takes the largest row bytes `+0x38` and
  `+0x39` (ignoring `0xFF`), stores the two extents at `0x0208D300`/`0x0208D301`, allocates an
  `extent38 × extent39` grid of `u16` named `gmbtAct`² at `0x0208D308` filled with `0xFF`,
  and writes each row's index at `[+0x38][+0x39]`.
- Each extent is the largest byte plus one, stored as a byte. `0x00237FC0` first stores 0 at `0x0208D308`
 ³; when either extent is 0 (no row with a byte other than `0xFF` there, a null slot or no rows) it
  allocates no grid and the pointer stays 0⁴.
- Otherwise the grid is `2 × extent38 × extent39` bytes, every byte set to `0xFF`⁵. A row whose
  `+0x38` or `+0x39` is `0xFF` is left out⁶; row `r` is stored at element
  `+0x38 × extent39 + +0x39`⁷.
- `0x00384510(size, name, 0)` pushes arena 4 (`0x0036C1D0(4, 4)`, `0x0038452E`) and tag 6 (`0x0036C1A0(6)`,
  `0x00384538`), allocates the size top-down⁸, labels a non-null block with the name
 ⁹, pops both¹⁰ and returns the block.
- The fills `0x002380AB` and `0x0023896B` do not test that block, so when arena 4 has no room the fill writes at
  address 0 and faults.
- **`0x00238880`, targetchip_data¹¹.** The same with row bytes `+0x16`/`+0x17`, extents
  at `0x0208D310`/`0x0208D311` and grid `gmbtTgt` at `0x0208D318`, storing `0x6000 + row`.
- `0x00238880` likewise stores 0 at `0x0208D318` first¹², allocates nothing when either extent is 0
 ¹³, sets every byte to `0xFF`¹⁴, leaves out a row with a `0xFF` byte and
  stores at element `+0x16 × extent17 + +0x17`¹⁵.
- **`0x00238160`, eitm_data¹⁶.** After binding, it adds the table's `+0x18` (an area after
  the rows) to each row's encoded `+0x28`.
- **`0x00238660`, shop_data¹⁷.** A three-level table with its own header (`+4` `u16` stride,
  `+6` `u16` count, `+8` rows). It adds the base to the slot, to the header's `+8`, to each row's `+4`
  (a sub-table) and that sub-table's `+8`, and to each sub-row's `+4` and its `+8`.
- The slot gets its low 32 bits plus the entry, zero-extended¹⁸, which is the entry while
  the slot is empty, and the header's `+8` is read at once with no null test¹⁹. Rows run to the
  header's `+6` and sub-rows to the sub-table's `+6`²⁰.
- The header's `+8`, each sub-table's `+8` and the `+8` of the table each sub-row's `+4` points to are rebased
  only when not 0²¹. Each row's and sub-row's `+4` is rebased even when 0
 ²².
- **`0x003847B0`, status_data²³.** A tail jump to `0x003845F0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EBF138` |
| ² | `0x00384510` |
| ³ | `0x00238059` |
| ⁴ | `0x00238073`-`0x0023807D` |
| ⁵ | `0x002380AB` |
| ⁶ | `0x00238107`, `0x00238110` |
| ⁷ | `0x00238116`-`0x00238132` |
| ⁸ | `0x0036A190`, `0x0038453F` |
| ⁹ | `0x0036C660`, `0x00384547`-`0x00384555` |
| ¹⁰ | `0x0036C110`, `0x0036C140` |
| ¹¹ | `0x02EBF0D8` |
| ¹² | `0x00238919` |
| ¹³ | `0x00238933`-`0x0023893D` |
| ¹⁴ | `0x0023896B` |
| ¹⁵ | `0x002389C7`-`0x002389F9` |
| ¹⁶ | `0x02EBF0F8` |
| ¹⁷ | `0x02EBF158` |
| ¹⁸ | `0x00238678`-`0x00238686` |
| ¹⁹ | `0x0023868D` |
| ²⁰ | `0x002386CC`, `0x00238778` |
| ²¹ | `0x00238698`, `0x00238739`, `0x002387F8` |
| ²² | `0x00238726`, `0x002387E5` |
| ²³ | `0x02EBF118` |

</details>

### License boards

The twelve slots `0x02EBF1A0`–`0x02EBF1F8` hold `board_1.bin` to `board_12.bin` (kind 2, files
`0x47`–`0x52`). At start-up `0x002368D0` zeroes them and calls `0x00238260(k)` for each:

- `0x00238260(k)` requests board `k` (`0x00384420`, name `BOARD`) when its slot is empty and
  `0x00233E00(k)` allows it; `0x00233E00` says yes when the board is already resident or fewer than six
  of the twelve are.
- `0x00238260(k)` returns 0 for `k` above 11, an unsigned byte compare¹, the board when slot `k`
  holds one², 0 when `0x00233E00` says no³, and otherwise what `0x00384420` returns for
  id `0x47 + k`, the setter `k`, name `BOARD`, arena 3, tag 8 and flags 4⁴.
- `0x00233E00` also says no for `k` above 11⁵, and counts the twelve slots six at a time
 ⁶.
- A slot fills only when its read completes, through the setters `0x00238390` + `0x30·k`, which free
  any old board⁷ and store the new one; `0x002383C0` is board 2's, slot `0x02EBF1A8`. Each setter
  stores its 32-bit argument sign-extended (`movsxd`, `0x00238396`, `0x002383C6`).
- The boot loop is the only caller of `0x00238260` and files the twelve requests back to back, so the
  six-board test passes for every board unless six reads finish while it is still filing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00238304` |
| ² | `0x00238324` |
| ³ | `0x00238332` |
| ⁴ | `0x00238355`-`0x0023837D` |
| ⁵ | `0x00233E03` |
| ⁶ | `0x00233E40`-`0x00233E8B` |
| ⁷ | `0x003844F0` |

</details>

Each board has its own slot and setter, `0x30` bytes apart. Every slot is a `ptr`, 0 until its read completes:

| Board | File | Slot | Setter | Store |
|---|---|---|---|---|
| 1 | `board_1.bin` | `0x02EBF1A0` | `0x00238390` | `0x002383AA` |
| 2 | `board_2.bin` | `0x02EBF1A8` | `0x002383C0` | `0x002383DA` |
| 3 | `board_3.bin` | `0x02EBF1B0` | `0x002383F0` | `0x0023840A` |
| 4 | `board_4.bin` | `0x02EBF1B8` | `0x00238420` | `0x0023843A` |
| 5 | `board_5.bin` | `0x02EBF1C0` | `0x00238450` | `0x0023846A` |
| 6 | `board_6.bin` | `0x02EBF1C8` | `0x00238480` | `0x0023849A` |
| 7 | `board_7.bin` | `0x02EBF1D0` | `0x002384B0` | `0x002384CA` |
| 8 | `board_8.bin` | `0x02EBF1D8` | `0x002384E0` | `0x002384FA` |
| 9 | `board_9.bin` | `0x02EBF1E0` | `0x00238510` | `0x0023852A` |
| 10 | `board_10.bin` | `0x02EBF1E8` | `0x00238540` | `0x0023855A` |
| 11 | `board_11.bin` | `0x02EBF1F0` | `0x00238570` | `0x0023858A` |
| 12 | `board_12.bin` | `0x02EBF1F8` | `0x002385A0` | `0x002385BA` |

Each setter reads its slot first and frees the board there through `0x003844F0` (for board 3, `0x002383F9`-`0x00238405`).
`0x00238260` takes the setters' addresses¹ for the requests it files. The boot's battle work
init `0x002368D0` zeroes all twelve slots with one `rep stosq`² before `0x00238260` files the
reads. Readers reach a slot by
board number from the array's start `0x02EBF1A0`, which `0x00233E00`, `0x00237630`, `0x00238260`, `0x00328990`, `0x003FC900`,
`0x0055B3F0`, `0x0055E2C0`, `0x0055E600`, `0x0055F830`, `0x00560070` and `0x00560610` form.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023827D`-`0x002382F9` |
| ² | `0x002369E5`-`0x00236A01` |

</details>

The license screen reads a board through `0x0055BFF0`, indexing the slots by the signed byte
`[obj + 0x558]` and reading the `licd` header (`+4` width, `+6` height, `u16` cells from `+8`).
`0x0055B3F0` fills `[obj + 0x558]` from `0x003236B0(member)`, which returns the member's battle record byte
`+0x1C5` when the record exists, its byte `+5` is 0 and its byte `+4` is below 7, and `0xFF`
otherwise. For `0xFF` it sets the board size `+0x559` to 0, so slot −1 is never read.

`0x003236B0` gives `0xFF` for a member above 39¹ and takes the record
`[0x02EBF190] + 8 + member × 0x1C8`. Its record test checks that sum for 0², so with `0x02EBF190` null
it reads byte `+5` below `0x10000` and faults.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003236B0`-`0x003236B3` |
| ² | `0x003236CD` |

</details>

`0x0055B3F0` makes the call only while `[obj + 0x128]` is 0 and bit `0x400` of `[obj + 0x570]` is clear¹. Its store for `0xFF` is a 16-bit zero over `+0x559` and `+0x55A`². For
any other board it reads the slot with no null test³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0055B429`, `0x0055B436` |
| ² | `0x0055B45C` |
| ³ | `0x0055B481`-`0x0055B484` |

</details>

### Finding a row

There is no shared accessor. Every reader computes, inline,

```python
row = 0x0020E600([table + 0x0C]) + u16[table + 0x08] × index
```

in 32-bit arithmetic (`0x003876D0`: `imul ecx, ebx; add ecx, eax`), so tables must lie below 4 GB.
A null slot or a zero row reference gives a base of 0 and the read still happens: `0x003876D0`, the
status timer reader, reads byte `+9` of address 0. Most readers do not bound the index; the ones
that do compare it with `+0x04`.

`0x0020E600` adds the 64-bit base at `0x01F83530` to a zero-extended dword and `0x0020E620` subtracts its low
dword; those two instructions are the base's only references (see the arena page).

### Battle id classes

`0x00322C50(class, id)` checks an encoded battle id against the table its class names: the id is valid
when it lies in `[start, start + count)`, with the count read from the table's `+4` (0 for a null slot).
A class of 0 or above 32 is never valid. Class 1 is first remapped through `0x00309440`: the class in the `0x58`-byte record at `0x01EEBCF8` for
the id's top nibble (5–19), −1 for nibble 15.

| Class | Start | Table |
|---|---|---|
| 2 | 0 | `0x02EBF130` chr_data |
| 3 | 0 | `0x02EBF120` `.ard` category 2 |
| 4 | 0 | `0x02EBF150` `.ard` category 0 |
| 5 | 0 | `0x02EBF100` dougu_data |
| 6 | `0x1000` | `0x02EBF0F8` eitm_data |
| 7 | `0x2000` | `0x02EBF098` eventitem_data |
| 8 | `0x3000` | `0x02EBF0F0` maho_data |
| 9 | `0x4000` | `0x02EBF0E8` waza_data |
| 10 | `0x5000` | `0x02EBF0E0` gambit_data |
| 11 | `0x6000` | `0x02EBF0D8` targetchip_data |
| 12 | `0x7000` | `0x02EBF0D0`, never written, so no id is valid |
| 13 | `0x8000` | the counts of `0x02EBF090`, `0x02EBF088`, `0x02EBF080` and `0x02EBF078` added together |
| 14 | `0x9000` | `0x02EBF070` eis_data |
| 15, 30, 31 | `0xA000` | `0x02EBF068` questreward_data |
| 16 | `0xB000` | `0x02EBF060` price_data |
| 17 | `0xC000` | `0x02EBF0C8` menkyo_data |
| 18 | `0xD000` | `0x02EBF058` horidashi |
| 19 | `0xE000` | no table: `0xE000`–`0xEFFE` |
| 20 | 0 | `0x02EBF138` action_data |
| 21 | 0 | `0x02EBF128` comac_data |
| 22 | 0 | no table: 0–3 |
| 23 | 0 | no table: 0–8 |
| 24 | 0 | `0x02EBF110` mgccategory_data |
| 25, 32 | 0 | `0x02EBF038` license_data |
| 26 | 0 | `0x02EBF118` status_data |
| 27 | 0 | `0x02EBF050` attribute_data |
| 28 | 0 | `0x02EBF0B0` sobicategory_data |
| 29 | 0 | `0x02EBF040` ability_data |

### Grouped and nested tables

- **tutorial_data¹.** Its `+0x1C` points to a group index: a count, then the end row of
  each group. `0x0032A230(group, key, &row)` scans the rows from the previous group's end to this one's
  for a row whose leading `u16` equals the key.
- **commandpack² and `.ard` category 1³.** Bound by `0x003846F0` at depth 0: a
  `u16` count and `count + 1` addresses, read in pairs as ranges.
- **word⁴.** Bound at depth 1: up to 32 banks, each a counted list of text addresses.
- **WepJob_Matrix⁵.** `u16` stride (1), `u16` count (23), then one byte per row.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EBF020` |
| ² | `0x02EBF160` |
| ³ | `0x02EBF168` |
| ⁴ | `0x02EBF170` |
| ⁵ | `0x02EBF180` |

</details>

### Runtime blocks and dead cells

- `0x02EBF190` is not a table. It always holds `0x002EF640() + 0x4E68C`, the party block (magic
  `0x05071901` at `+0`; 40 member stats records of `0x1C8` bytes from `+8`), written by `0x00233C10` when
  null and by `0x00238A80`.
- `0x02EBF178` is written only by `0x00324510`, a builder for 301 kind-`0x1A` files that never runs: its
  state `0x022C27A0` is touched only inside it, and nothing stores the state 1 that starts it.
- `0x00324510` is called from `0x0022AE6F`, `0x0022BAEF` and `0x0022BD3F`, and with its state at 0 it returns at once
 ¹. It stores the buffer `[0x022C27B0]` in `0x02EBF178` once all 301 entries are filed and the in-flight
  count `0x022C27A8` is 0 (`0x0032468F`-`0x0032469A`, then state 3), and 0 in state 3 when the dword `0x022C27A4` is not 0
 ².
- The rip-relative references to `0x022C27A4` are that test at `0x0032452F` and the qword store of 0 at `0x00324551`
  on the same path, which covers it.
- `0x02EBF188` has 93 writes and no read.
- `0x02EBF0D0` is read once (class 12) and never written. `0x02EBF198` has no reference at all.
- `0x02EBF200` (`license_board.bin`) is stored once and never read.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00324529` |
| ² | `0x0032452F`-`0x00324558` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

Table header (all offsets from the header until bound):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | magic | 'st2e' (or u16 count on `0x003846F0` tables) |
| `+0x04` | `u32` |  | row count |
| `+0x08` | `u16` |  | row stride |
| `+0x0A` | `u16` | word0A | 0 |
| `+0x0C` | `...` |  | row array |
| `+0x10` | `...` | reference |  |
| `+0x14` | `...` |  | encoded sub-directory |
| `+0x18` | `...` | reference |  |
| `+0x1C` | `...` | reference |  |

Battle_pack (the file ends with u8[4] 0):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16` | count | 71 |
| `+0x002` | `u8[2]` | bytes002 | 0 |
| `+0x004` | `...` | entry offsets | `+0x04` + 4k: offset of entry k (k < 71) |
| `+0x120` | `...` | end offset | file size - 4 |
| `+0x124` | `u8[4]` | bytes124 | 0 |

Licd board:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `...` | magic | 'licd' |
| `+0x04` | `u16` | width |  |
| `+0x06` | `u16` | height |  |
| `+0x08` | `...` | cells | u16 cells[width*height] |

.ard header, section offsets (categories 0-4):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x10` | `...` | section offset | category 0 |
| `+0x14` | `...` | section offset | category 1 |
| `+0x18` | `...` | section offset | category 2 |
| `+0x24` | `...` | section offset | category 3 |
| `+0x28` | `...` | section offset | category 4 |
| `+0x2C` | `...` | section | section for `0x003DCF00` |

The header fields are listed access by access in
[`authored-data-tables-header-accesses.tsv`](authored-data-tables-header-accesses.tsv), and the slot
references in [`authored-data-tables-slot-accesses.tsv`](authored-data-tables-slot-accesses.tsv). In the
header table, `route` names the registry slot whose pointer the function loads before the access, one slot
on each of the 1,800 rows, and `note` names the function that loads it, on every row the accessing function.

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

The `us` `battle_pack.bin` (281,128 bytes), by directory offset; shapes are rows × row bytes.

| Slot | Entry | File | Shape |
|---|---|---|---|
| `0x02EBF008` | `+0x118` | movie | 49 × 8 |
| `0x02EBF010` | `+0x114` | move_support | 120 × 8 |
| `0x02EBF018` | `+0x0C` | battle_message | 102 × 8 |
| `0x02EBF020` | `+0x70` | tutorial_data | 6 × 20 |
| `0x02EBF028` | `+0xF0` | savemember_data | 226 × 44 |
| `0x02EBF030` | `+0xF4` | saveparty_data | 50 × 208 |
| `0x02EBF038` | `+0x34` | license_data | 361 × 24 |
| `0x02EBF040` | `+0xEC` | ability_data | 129 × 8 |
| `0x02EBF048` | `+0xAC` | shoki_data | 32 × 4 |
| `0x02EBF050` | `+0xA8` | attribute_data | 8 × 2 |
| `0x02EBF058` | `+0xE8` | horidashi | 128 × 36 |
| `0x02EBF060` | `+0x74` | price_data | 128 × 4 |
| `0x02EBF068` | `+0x9C` | questreward_data | 256 × 12 |
| `0x02EBF070` | `+0x98` | eis_data | 512 × 12 |
| `0x02EBF078` | `+0x94` | s_daiji_data | 0 × 10 |
| `0x02EBF080` | `+0x90` | q_daiji_data | 416 × 10 |
| `0x02EBF088` | `+0x8C` | g_daiji_data | 32 × 10 |
| `0x02EBF090` | `+0x88` | m_daiji_data | 64 × 10 |
| `0x02EBF098` | `+0x84` | eventitem_data | 512 × 10 |
| `0x02EBF0A0` | `+0x80` | yugoyaku_data | 16 × 13 |
| `0x02EBF0A8` | `+0x14` | jochumodel_data | 0 × 4 |
| `0x02EBF0B0` | `+0x18` | sobicategory_data | 32 × 4 |
| `0x02EBF0B8` | `+0x10` | damagemp_data | 25 × 8 |
| `0x02EBF0C0` | `+0x1C` | drop | 4 × 37 |
| `0x02EBF0C8` | `+0x6C` | menkyo_data | 32 × 8 |
| `0x02EBF0D8` | `+0x20` | targetchip_data | 256 × 32 |
| `0x02EBF0E0` | `+0x24` | gambit_data | 40 × 64 |
| `0x02EBF0E8` | `+0x7C` | waza_data | 24 × 8 |
| `0x02EBF0F0` | `+0x78` | maho_data | 81 × 8 |
| `0x02EBF0F8` | `+0x38` | eitm_data | 557 × 52 |
| `0x02EBF100` | `+0x4C` | dougu_data | 64 × 12 |
| `0x02EBF108` | `+0x28` | hpmpbase_data | 99 × 2 |
| `0x02EBF110` | `+0x30` | mgccategory_data | 5 × 4 |
| `0x02EBF118` | `+0x40` | status_data | 32 × 40 |
| `0x02EBF128` | `+0x48` | comac_data | 21 × 4 |
| `0x02EBF130` | `+0x44` | chr_data | 40 × 128 |
| `0x02EBF138` | `+0x3C` | action_data | 543 × 60 |
| `0x02EBF158` | `+0xA0` | shop_data | own header |
| `0x02EBF160` | `+0x2C` | commandpack | offset list |
| `0x02EBF170` | `+0xF8` | word | 15 banks |
| `0x02EBF180` | `+0x04` | WepJob_Matrix | 23 × 1 |
| `0x02EBF200` | `+0x11C` | license_board | 24 × 24 `licd` |

The other 29 entries are empty in every language's pack, each starting where the next one starts: id 19, the
pack itself, the 27 text-group ids (1, 20-25, 43-56, 62-67), whose menu, help and list-help texts and quest
titles the game loads as files of their own, and id 40, which no path array names. All 48 shipped
`board_N.bin` files are 1,160-byte 24 × 24 `licd` boards.

</details>

## State

<details>
<summary>Show the state it keeps</summary>

The 64 slots, the pack pointer `0x0208E680`, the two lookup grids and their extents¹, and the party block behind `0x02EBF190`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0208D300`-`0x0208D318` |

</details>

</details>

## Modding notes

- Keep every table's header offsets relative to the table: the binder adds the table's address once
  at load.
- The id classes take their ranges from each table's row count at `+0x04`; an id is `start + row`.
- Row bytes `+0x38`/`+0x39` of action_data and `+0x16`/`+0x17` of targetchip_data place the row in
  the menu grids; use `0xFF` to leave a row out.
- Categories 0–2 of an `.ard` are bound even when their offset is 0, which binds the file header as
  a table and corrupts it; every `.ard` needs all three.
- Never leave a table out of the pack or an area's `.ard` that a reader needs: a missing table is read
  at address 0.

## Related

- [Resource arenas and relocation](resource-arena-and-relocation.md): the 32-bit address encoding.
- [File size tables](file-size-tables-fst.md): the file kinds the pack, `.ard` and boards are loaded by.
- [Resource ownership and disposal](resource-ownership-and-disposal.md): how other loaded data is owned.
