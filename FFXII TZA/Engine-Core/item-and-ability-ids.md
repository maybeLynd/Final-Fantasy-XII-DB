---
title: "Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record"
kind: "system"
category: "Engine core"
addresses: "0x00309440, 0x01EEBCC0, 0x0030B6A0, 0x00322C50, 0x00323054, 0x00309EC0, 0x0030AE30, 0x0030ADC0, 0x00309F30, 0x003008A0, 0x002FD150, 0x002FD8D0, 0x002FD420, 0x002FD970, 0x002FD530, 0x002FD640, 0x002FD780, 0x002FD880, 0x00325F40, 0x00252E60, 0x002535D0, 0x0031C5D0, 0x0031E598, 0x0035D330, 0x0035D380, 0x0035E070, 0x00236C30, 0x003845F0, 0x0020E600, 0x00254EE0, 0x00253690, 0x0046A630, 0x00512CD0, 0x02EBF190"
---

## What the player sees

Every list the menus draw, the Items tab with its quantities, the Loot tab, the Magicks and
Technicks lists, the gambit condition picker, the Key Items tab, the bazaar's goods and the
licence board's node names, is built by asking one question of one function: here is an id, tell
me its name, its description and how many the party has.

A treasure that gives gil and two
items, a bazaar good that grants three things, and a script line that adds an exact amount of gil
are all ids of the same kind too, and the same function hands them out. The empty slot in every
one of those lists is the number with all its bits set.

## How it works

### The id space

An encoded id is sixteen bits: the top nibble `id >> 12` picks a class and the low twelve bits
`id & 0xFFF` are the index inside it. `0x00309440(id)` returns the class: nibble `0xF` gives -1,
otherwise the `+0x38` field of the descriptor at `0x01EEBCC0 + nibble × 0x58`, which holds 5 for
nibble 0 up to 19 for nibble `0xE`. So the class is the nibble plus five, and the descriptor
table at `0x01EEBCC0` has fifteen records of `0x58` bytes:

| Offset | Field |
|---|---|
| `+0x00` / `+0x08` | region A: offset into the party block `[0x02EBF190]`, and the pointer the rebaser derives from it |
| `+0x10` | region A length in 16-bit words |
| `+0x18` / `+0x20`, `+0x28` / `+0x30` | regions B and C the same way (0 when the class has no such region) |
| `+0x38` | class, 5 to 19 |
| `+0x3C` | id count; an index at or past it is invalid |
| `+0x40` | cumulative id base, the running sum of the earlier counts (written at run time) |
| `+0x48` | mutate handler `(id, delta, absolute, channel, flags)` or 0 |
| `+0x50` | query handler `(id, mode)` or 0 |

The rebaser `0x0030B6A0(state)` adds the state block's address to every non-zero offset, writes
the cumulative bases, zeroes `0x200` bytes at state `+0x57C8` and masks `0x80` bytes at `+0x59C8`
with `0xF8`. It runs from `0x00233C10` and from `0x00238A80`, which first points `0x02EBF190` at
`0x002EF640() + 0x4E68C` in the save runtime buffer and is called only by the payload reset
`0x002EF650` ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)). The fifteen
records, read from the image:

| Nibble | Class | Count | Region A (words) | B | C | Handlers | What it holds |
|---|---|---|---|---|---|---|---|
| 0 | 5 | 64 | `+0x4748` (64) | | `+0x57C0` | packed count | items |
| 1 | 6 | 420 | `+0x47C8` (420) | | | packed count | equipment |
| 2 | 7 | 512 | `+0x4B10` (512) | `+0x57C8` | | packed count | loot |
| 3 | 8 | 81 | `+0x4F10` (6) | | | bitset | magicks |
| 4 | 9 | 24 | `+0x4F1C` (2) | | | bitset | technicks |
| 5 | 10 | 0 | | | | no handler | unused |
| 6 | 11 | 256 | `+0x4F20` (16) | | | bitset | gambit conditions |
| 7 | 12 | 0 | | | | no handler | unused |
| 8 | 13 | 512 | `+0x4F40` (32) | | | bitset | key items |
| 9 | 14 | 512 | | | | mutate only `0x002FD530` | reward packages |
| A | 15 | 256 | | | | mutate only `0x002FD640` | package selectors |
| B | 16 | 0 | | | | no handler | unused |
| C | 17 | 32 | `+0x4F80` (2) | | | bitset | quickenings |
| D | 18 | 128 | | | | mutate only `0x002FD780` | bazaar goods |
| E | 19 | 4,095 | | | | mutate only `0x002FD880` | gil amounts |

The regions abut: each region A ends where the next begins, which is what makes `+0x10` a word
count. The counts sum to 6,892.

### Owning things: the two handler pairs

`0x003008A0(id, delta, absolute, channel, flags)` is the one entry that changes what the party
owns. It refuses `0xFFFF`, `0x1000` (the Unarmed row) and nibbles above `0xE`, returns -1 for an
index at or past the class's count, reads the channel's value through `0x00309F30(id, channel)`,
calls the descriptor's mutate handler with the same five arguments, and returns the value after.

When the channel is 1 and the value went from nothing to something it also sets bits of the
state block's flag dword `[0x02EBF190] + 4`: bit `0x1` for a magick, plus a school bit found in two
hops (byte `+2` of the magick's row in `0x02EBF0F0`, `id - 0x3000`, is an action index; word
`+0x2C & 7` of that row in `0x02EBF138` is k, and `0x01EECF98[k]` is ORed in when k < 5); `0x40` for a
technick; `0x80` for a quickening `0xC000` to `0xC011` and `0x100` for `0xC012` to `0xC01E`.

The packed-count classes (items, equipment, loot) keep one 16-bit word per id in region A: mask
`0x3FF` the owned total, capped at 99, mask `0xFC00` the reserved copies. The query handler
`0x002FD8D0(id, mode)` returns total minus reserved for mode 0 (which can go negative), the total
for mode 1, the reserved count for mode 2 and the region-B byte for mode 3. The mutate handler
`0x002FD150` by channel:

- channel 1 sets or adds the total, clamped between the reserved count and 99; when the total
  rose it sets the id's bit in region C (items' ever-owned bitset at `+0x57C0`, byte `index >> 3`,
  bit `index & 7`); then the derived-index hook `0x00325F40(id, old total, new total)` and, for a
  relative change with flag bit `0x1`, the "You obtain" line `0x0046A630(id, delta)`;
- channel 0 subtracts `delta` from the reserved count (absolute: reserved = total - `delta`),
  clamped to 0 to total, and returns total minus reserved; channel 2 adds `delta` to it
  (absolute: reserved = `delta`), clamped the same way, and returns the reserved count;
- channel 3 sets or adds the region-B byte, clamped to 0 to 99 (loot's bazaar-sold tally at
  `+0x57C8`).

The bitset classes (magicks, technicks, gambit conditions, key items, quickenings) keep one bit
per id in region A: word `index >> 4`, bit `index & 0xF`. `0x002FD970(id, mode)` returns that bit
for modes 0 and 1, 0 for mode 2, and the byte-addressed bit of region B or C for modes 3 and 4.
`0x002FD420` ignores the channel: the new value is `delta` (absolute) or the bit plus `delta`, a
negative clears it and anything above 1 saturates to 1; the hook and the obtain line follow.

The four handler-only classes act on other classes, only for `absolute` 0 and channel 1:

- class 14 (`0x002FD530`): row `{u32 gil, u16 item, u16 count, u16 item, u16 count}` of the table at
  `0x02EBF070`; gil through `0x00254EE0(0x00253690() + gil × delta)` clamped at 0, with the gil
  "obtain" line `0x00469E80(gained)` when flag bit `0x1` is set, then each item that is not `0xFFFF`
  through `0x003008A0(item, count × delta, 0, 1, flags)`;
- class 15 (`0x002FD640`): six `u16` ids in the row of `0x02EBF068`, the first triple, or the second
  when flag bit `0x2` is set, each granted with `delta`; the first triple tests each id for `0xFFFF`
  on its own, the second grants its sixth id whenever its fifth is not `0xFFFF`;
- class 18 (`0x002FD780`): three `(u16 item, u8 count)` pairs at `+4`, `+8` and `+0xC` of the row of
  `0x02EBF058`, each with a non-zero count granted as `count × delta`;
- class 19 (`0x002FD880`): gil through `0x00254EE0(0x00253690() + (id & 0xFFF) × delta)`, clamped at 0:
  the id is the amount.

`0x00325F40(id, old, new)` runs on a 0 to non-zero or non-zero to 0 transition: it validates the
id with the class-1 arm, returns for a nibble above 10 (the eleven `{map, count}` pairs at
`0x01EED1B0` cover nibbles 0 to 10, and 9 and 10 are null), maps the nibble (and for equipment the
row's category byte `+9` of `0x02EBF0F8`, when that table is bound) through the signed-byte maps to
a category list, and appends (`0x00252E60`) or removes (`0x002535D0`) the id in that list; those
lists are what the menus page through.

### The thirty-two-class validator

`0x00322C50(class, id)` answers whether an id is valid for a class. Classes 1 to 32 dispatch
through the 32-entry table at `0x00323054`, and every arm ends in the shared test `lo ≤ id ≤ hi -
1`, so a bound is a count and the valid set is `[lo, lo + count)`. The count comes from the
`+4` word of an authored table (`st2e`: `+4` rows, `+8` stride, `+0x0C` the row array, `0x20` in the
shipped tables that have rows; bound at the pack or area load through `0x003845F0`), except for four arms:

- class 1 derives the class from the id with `0x00309440` and re-enters the switch;
- class 19 uses `0xE000` to `0xEFFF` compiled in, so the last valid id is `0xEFFE`;
- class 22 uses a literal 4 and class 23 a literal 9 (ids 0 to 3 and 0 to 8).

| Class | Base | Table | Class | Base | Table |
|---|---|---|---|---|---|
| 2 | 0 | `0x02EBF130` party definitions | 18 | `0xD000` | `0x02EBF058` bazaar goods |
| 3 | 0 | `0x02EBF120` | 20 | 0 | `0x02EBF138` actions |
| 4 | 0 | `0x02EBF150` | 21 | 0 | `0x02EBF128` battle commands |
| 5 | 0 | `0x02EBF100` items | 24 | 0 | `0x02EBF110` magick schools |
| 6 | `0x1000` | `0x02EBF0F8` equipment | 25, 32 | 0 | `0x02EBF038` licence nodes |
| 7 | `0x2000` | `0x02EBF098` loot | 26 | 0 | `0x02EBF118` statuses |
| 8 | `0x3000` | `0x02EBF0F0` magicks | 27 | 0 | `0x02EBF050` elements |
| 9 | `0x4000` | `0x02EBF0E8` technicks | 28 | 0 | `0x02EBF0B0` equipment categories |
| 10 | `0x5000` | `0x02EBF0E0` gambit presets | 29 | 0 | `0x02EBF040` augments |
| 11 | `0x6000` | `0x02EBF0D8` gambit conditions | 13 | `0x8000` | `0x02EBF090` + `0x02EBF088` + `0x02EBF080` + `0x02EBF078`, the four key-item sub-tables summed |
| 12 | `0x7000` | `0x02EBF0D0` | 14 | `0x9000` | `0x02EBF070` reward packages |
| 15, 30, 31 | `0xA000` | `0x02EBF068` package selectors | 16 | `0xB000` | `0x02EBF060` |
| 17 | `0xC000` | `0x02EBF0C8` quickenings | | | |

The table has 29 distinct arms for 32 classes: 15, 30 and 31 share one, 25 and 32 another. For
the fifteen inventory classes the arm's base equals `(class - 5) << 12`, the same structure the
descriptors carry. A missing table counts as zero rows, so a null-guarded arm accepts nothing.

Class 13's validator range is the four key-item sub-table counts summed from `0x8000`, but the code that reads
the ids fixes the three sub-ranges in immediates of its own:

| Ids | Sub-table | Query filler test | List kind |
|---|---|---|---|
| `0x8000`-`0x803F` | m_daiji_data `0x02EBF090` | `id - 0x8000` at most `0x3F` as an unsigned 16-bit value (`0x0031D10E`-`0x0031D115`) | 21 |
| `0x8040`-`0x805F` | g_daiji_data `0x02EBF088` | `id - 0x8040` at most `0x1F` as an unsigned 16-bit value (`0x0031D2B4`-`0x0031D2BF`) | 22 |
| `0x8060`-`0x81FF` | q_daiji_data `0x02EBF080` | `id - 0x8060` at most `0x19F` as an unsigned 16-bit value (`0x0031D472`-`0x0031D482`) | 20 |

- The query filler's class-13 arm (`0x0031D0EF`) reads the row's name word `+8`, description word `+6`, byte `+4`
  (record `+0x2C`) and word `+2` (record `+0x30`) from the sub-table the test picks. A validated id past `0x81FF`
  skips all four (`0x0031D482` to `0x0031D638`): the record gets only the two channels and `+0x28` = -1, the name
  stays null and the fill returns 0.
- The description line `0x00292B70` returns nothing for a kind-10 entry outside `0x8060`-`0x81FF`
  (`0x00292C3A`-`0x00292C4A`, [text codes](../Menus-And-HUD/text-codes.md)).
- The Key Items list builders `0x0057CF20` and `0x0057D620` hand `0x0057DAD0` a `{u32 end, u32 start}` pair for list
  kinds 20, 21 and 22 (`0x0057D432`-`0x0057D45E`, `0x0057D9D1`-`0x0057D9FD`), and `0x0057DAD0` keeps an id only when
  `start <= id < end` (`0x0057DB2C`-`0x0057DB3B`).
- The class-13 descriptor holds 512 ids and a 32-word bitset, so the owned bits end at `0x81FF` too.

s_daiji_data (`0x02EBF078`) ships with no rows, so the summed count is 64 + 32 + 416 = 512 and every one of these
bounds ends at the same id. A row added to any sub-table moves the validator's end and none of the others.

### From a content id to its row

One rule takes an encoded id to the authored row it names. Its parts are above and on
[authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md); this section only joins them,
reading the validator `0x00322C50` and the query filler `0x0031C5D0` as the two routines that apply it.

1. **Class.** `0x00309440(id)` gives `(id >> 12) + 5`, the descriptor's `+0x38`, or −1 for nibble `0xF`. A
   caller that already holds a class (classes 2-4 and 20-32 have no nibble) passes it directly; the
   class-1 arms of both routines derive it this way and re-enter (`0x00322C7E`-`0x00322C8B`, `0x0031C61F`-`0x0031C639`).
2. **Base and slot.** The class's arm pairs a base with a registry slot (the table in The thirty-two-class
   validator): base `(class − 5) << 12` for the inventory classes 5-19, `0xA000` for 30 and 31, which share
   class 15's arm (`0x00322EC2`, `0x0031D745`), and 0 for 2-4, 20-29 and 32 (`0x00322C9A`-`0x00323028`).
3. **Table.** The slot holds the table its loader bound.
   - For every class with a bound slot except 3 and 4 that is the pack load `0x00236C30(1)`, which passes the
     sign-extended dword `[[0x0208E680] + entry]` of one battle_pack directory entry to `0x003845F0(&slot, table)`
     (33 sites, `0x00236C86`-`0x0023701E`), to a bespoke binder (the same dword in `ecx`, `0x00236D73`) or to
     `0x003846F0`.
   - Class 12's slot `0x02EBF0D0` is bound by no loader (its one reference is the read at `0x00322DFE`), and
     classes 1, 19, 22 and 23 have no slot.
   - Which entry each slot takes is the Shipped data table on
     [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md#shipped-data).
   - Classes 3 and 4 use the area-table slots `0x02EBF120` and `0x02EBF150`, bound from the `.ard` by `0x003EA710`
     through `0x0023A160` (categories 2 and 0) and unbound by `0x003EA820` at each area load (`0x0023A160(category, 0)`,
     `0x003EA8E1`-`0x003EA90D`), so they change with the area.
4. **Row.** `row = id − base`, valid when `0 ≤ row < [table + 0x04]`: the validator's shared tail refuses
   `id < base` and `id > base + count − 1` (`0x0032302E`-`0x0032303B`), with count 0 for a null slot.
5. **Address.** `address = 0x0020E600([table + 0x0C]) + u16[table + 0x08] × row`, in 32-bit arithmetic
   ([finding a row](../Game-Files-And-Data-Tables/authored-data-tables.md#finding-a-row)).
   - `+0x0C` is the row array's offset until `0x003845F0` adds the table's low 32 bits to it, when it is non-zero
     (`0x00384600`-`0x0038460E`); it is `0x20`, the header size, in all 64 battle_pack `st2e` tables that have rows
     and in every `.ard` category-0 and category-2 table that has rows.

The filler's class-6 arm applies the rule: `eax = 0x0020E600([[0x02EBF0F8] + 0xC])` (`0x0031C886`-`0x0031C890`), then
`movzx ebp, word ptr [rbx + 6]`, `sub ebp, 0x1000`, `movzx ecx, word ptr [r8 + 8]`, `imul ebp, ecx`, `add ebp, eax`
(`0x0031C89C`-`0x0031C8AE`).

The same shape with its own base is at
`0x0031CB08` (7), `0x0031CC72` (8), `0x0031CE1E`-`0x0031CE2A` (9, `0x4000` in `r14d`), `0x0031CFC3` (11), `0x0031D6B6` (14),
`0x0031D745` (15), `0x0031D7E3` (16), `0x0031D860` (17) and `0x0031D93B` (18); a base-0 class multiplies the id or row
as it is (class 5 at `0x0031C756`-`0x0031C75F`, class 2 at `0x0031C6A7`-`0x0031C6AF`).

Worked: id `0x1005` has nibble 1, class 6, base `0x1000`, slot `0x02EBF0F8`, bound from directory entry `+0x38`
(eitm_data, 557 rows of 52 bytes), so row 5 at `table + 0x20 + 5 × 52`. Id `0x8045` has class 13 and falls
in the second key-item sub-range, so it is row 5 of g_daiji_data (`0x02EBF088`, entry `+0x8C`).

The exceptions, each read at its bytes:

- **Class 13, key items.** The validator sums the four sub-tables' counts from `0x8000` (`0x00322E28`-`0x00322E8C`),
  but a row is `id − 0x8000` in m_daiji_data (`0x0031D164`), `id − 0x8040` in g_daiji_data (`0x0031D30E`) or
  `id − 0x8060` in q_daiji_data (`0x0031D4D1`), chosen by the sub-range tests in the table above; s_daiji_data
  ships no rows and is reached by no reader.
- **Class 19, gil.** No table: the arm is compiled in as `0xE000`-`0xEFFF` (`0x00322F63`-`0x00322F68`), so the last
  valid id is `0xEFFE`; the gil handler `0x002FD880` takes the amount as `id & 0xFFF` (`0x002FD8A2`) and the
  filler only validates and returns −1 (`0x0031C63B`-`0x0031C64A`).
- **Classes 22 and 23.** No table: literal counts 4 and 9 (`0x00322FA6`, `0x00322FAF`), ids 0-3 and 0-8; the filler
  returns 0 without a row.
- **Class 12.** Slot `0x02EBF0D0` is never written, so its count is 0 and every id is refused.
- **Class 10.** The filler's arm reads no row (`0x0031CF28`-`0x0031CF75`); gambit_data is read by `0x00327CB0`, which
  fills a new stats record's gambit block from a preset, and by `0x00235AF0` ([gambits](../Enemy-AI-And-Gambits/gambits.md)).
- **Base-0 classes** (2-5, 20, 21, 24-29 and 32). The id is the row. The query record takes it at `+4` for 2-4,
  20, 21, 24-29 and 32 (and the bare id for 22 and 23, which have no row) and at `+6` for 5 (The query record
  below). For class 19, `+4` holds the gil id itself, validated
  against `0xE000`-`0xEFFE`; for 30 and 31, `+6` holds an id based at `0xA000`.
- **Shared tables.** Classes 15, 30 and 31 use questreward_data and 25 and 32 license_data, with one base.
- **Zero-row tables.** jochumodel_data (entry `+0x14`), s_daiji_data (entry `+0x94`) and the category-0 and
  category-2 tables of asp_a, dor_f, mrm_a and slm_a in the `ch` and `in` area sets ship with 0 rows and
  `+0x0C` = 0, which the binder leaves at 0; their counts refuse every id, so the rule never reads them.
- **A null slot or a zero `+0x0C`.** The validator refuses. A reader that null-tests the slot without refusing
  (`0x003876D0`, which then uses 0 as the row address, `0x00387712`) or decodes a zero `+0x0C` (`0x0020E600(0)`, 0
  because the base cell `0x01F83530` is never written) reads near address 0
  ([finding a row](../Game-Files-And-Data-Tables/authored-data-tables.md#finding-a-row)).

### The query record

`0x0031C5D0(record)` fills a `0x98`-byte record whose `+0` is the class and whose `+4` is the row
(classes 2 to 4 and 19 to 29, 32) or whose `+6` is the id (classes 1, 5 to 11, 13 to 18, 30, 31).
It clears the name pointer at `+0x18` and dispatches through the 32-entry table at `0x0031E598` by
`class - 1`. Each arm validates with `0x00322C50` and writes its own fields:

- the name pointer `+0x18`, the description `+0x10`, and an auxiliary text `+0x08` for actions,
  commands and schools;
- the two inventory channels `+0x20` and `+0x24` (`0x00309EC0(id)` and `0x0030AE30(id)`, the
  descriptor's query handler with modes 0 and 1);
- class-specific scalars from `+0x28` on.

Every arm's failed validation returns -2 (`0x0031C650`). Class 1 derives the class from the id,
stores it at `+0` and re-dispatches; class 12 returns -2 at once; class 19 and any class above
32 validate the row and return -1 on a valid one (`0x0031C63B`); classes 4, 22 and 23 validate and
return 0 with no other output. A successful fill leaves fields it did not write as they were, so
the record is partial, not a fresh value.

Two static records serve most callers: `0x0035D330(class, row)` writes the row form into
`0x022CA520` and `0x0035D380(class, id)` the id form into `0x022CA480`; both zero all `0x98` bytes
when the fill returns negative and return the record's address either way. The row form has
159 call sites in 75 functions and the id form 15; `0x0035E070` fills the row record itself for
class 1 with the id in the high word of `+4`, and eleven other functions hand `0x0031C5D0` their
own record at fourteen sites.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CA524` | `i32` | 0 (zero-filled tail) | `+4` of the row-form record `0x022CA520`: the row, or for `0x0035E070` the class-1 id in the high word | `0x0035D330`, the row argument (`0x0035D346`); `0x0035E070`, the id shifted left 16 (`0x0035E2B6`) | `0x0031C5D0`, through the record's address from both (`0x0035D34C`, `0x0035E2C6`), in its class arms (`0x0031C61F`-`0x0031CF28`) |

No other instruction reaches `0x022CA524`: no other RIP-relative, image-base-relative or 32-bit offset reference names
it.

The id-form record's id word:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x022CA486` | `u16` | 0 (zero-filled tail) | `+6` of the id-form record `0x022CA480`: the id the caller asks about | `0x0035D380`, the id argument (`0x0035D396`), from its 15 call sites (the first `0x0027BADE`, the last `0x0057DF35`); the `0x98`-byte clear (`0x0035D3BB`) when the fill returns negative | `0x0031C5D0`, through the record's address (`0x0035D38C`), in its class arms: 73 word reads of `+6`, from `0x0031C61F` to `0x0031D9EF` |

The menus are those callers: the gambit screen's row and page builders (`0x00567B60`, `0x0056B100`,
`0x0056AE80`), the licence screens (`0x00558CE0`, `0x005618E0`) and the battle menu's title
`0x0027D480` use the row form ([gambit screen](../Menus-And-HUD/gambit-screen.md),
[menu screens](../Menus-And-HUD/menu-screens.md)).

Half of the callers read the name at `+0x18` and no other field; the equipment block
`+0x3C` to `+0x60` is read by the equip menus, the licence bytes `+0x21` to `+0x25` by the
licence board. String pointers point into the loaded text banks; the record never allocates or
copies them.

`0x003933B0(category)` turns a shop category (`0x002FABD0`, [Shops](../Items-Equipment-Shops-And-Licenses/shops.md))
into the class for a query through the twelve-byte map at `0x00D113B8`: categories 0-3 give class 6 (equipment), 4
gives 5 (items), 5 gives 9 (technicks), 6 gives 8 (magicks), 7 gives 7 (loot), 8 gives 10 (gambit presets), 9
gives 11 (gambit conditions), 10 gives 12 and 11 gives 18 (bazaar goods); a category of 12 or more gives -1. The
shop rows (`0x0056E410`, `0x0056E49D`) and the hunt pane (`0x003F41C0`, `0x003F4210`) take that class to `0x0035D380`.

### The empty id

`0xFFFF` is the empty id. The dispatchers refuse it before the nibble test, `0x003008A0` refuses it,
the bundle rows use it for "no item", a derived-index list blanks a removed entry with it and
compacts past it, an equipment slot holds it when empty and a unit's reserved item at `+0xDC8`
when none is reserved.

One-byte fields use `0xFF` the same way: the relation pool at `0x02CA81F0` links its 16-byte
records through byte indices at `+0xD` and `+0xE`, and `0x00512CD0` unlinks a record by writing
`0xFF` into its neighbours' links (then clears the low nibble of its `+0xF` and decrements the
owner's count byte `+0xE` and the pool count `0x02EBA481`), because index 0 is a real record and
the only free value is the largest the byte can hold.

## Layouts

```
encoded id (u16): nibble = id >> 12 (0..0xE), index = id & 0xFFF; class = nibble + 5; 0xFFFF = the empty id
```

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01EEBCC0` | `ItemClassDescriptor[15]` | descriptors | `0x58` each (layout above); `0x01EEBCF8` = record 0's class |
| `0x00323054` | `u32[32]` | validator arm RVAs | by class - 1 (29 distinct) |
| `0x0031E598` | `u32[32]` | query filler arm RVAs | by class - 1 (28 distinct) |
| `0x01EED1B0` | `...` | category maps | the derived-index category maps, by nibble: {ptr map, u32 count}[11] |

Party block [`0x02EBF190`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0004` | `u32` | discovery bits | `0x1` magick, `0x2`..0x20 school, `0x40` technick, `0x80` / `0x100` quickenings |
| `+0x4748` | `u16[64]` | items |  |
| `+0x47C8` | `u16[420]` | equipment |  |
| `+0x4B10` | `u16[512]` | loot |  |
| `+0x4F10` | `u16[6]` |  | magicks bits |
| `+0x4F1C` | `u16[2]` | technicks |  |
| `+0x4F20` | `u16[16]` |  | gambit conditions |
| `+0x4F40` | `u16[32]` |  | key items |
| `+0x4F80` | `u16[2]` | quickenings |  |
| `+0x57C0` | `...` |  | items ever-owned bits |
| `+0x57C8` | `u8[512]` |  | loot sold tally |
| `+0x59C8` | `u8[128]` | inventoryPackedFlags | masked with `0xF8` by the rebaser |

```
packed word: mask 0x3FF total (0..99), mask 0xFC00 reserved
```

EncodedIdQueryRecord (`0x98`); `0x022CA520` the row-form copy, `0x022CA480` the id-form copy:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | class |  |
| `+0x04` | `u32` | row | row form; the id form has `+0x06` u16 id instead |
| `+0x06` | `u16` | id | id form |
| `+0x08` | `void*` |  | aux text |
| `+0x10` | `void*` | description |  |
| `+0x18` | `void*` | name |  |
| `+0x20` | `i32` |  | channel 0 |
| `+0x24` | `i32` |  | channel 1 |
| `+0x28` | `...` | class-specific | from `+0x28` on |

Reward package row (12):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | gil |  |
| `+0x04` | `u16` | item |  |
| `+0x06` | `u16` | count |  |
| `+0x08` | `u16` | item |  |
| `+0x0A` | `u16` | count |  |

Package selector row (12):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[3]` | id |  |
| `+0x06` | `u16[3]` | id |  |

Bazaar good row (36):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | name |  |
| `+0x02` | `u16` | desc |  |
| `+0x04-0x0F` | `u8[12]` | items | (u16 item, u8 count, u8)[3] |
| `+0x10` | `u32` | price |  |
| `+0x14` | `u16` | word14 |  |
| `+0x16-0x21` | `u8[12]` | loot | (u16 loot, u16 count)[3] |
| `+0x22` | `u16` | word22 |  |

## Shipped data

| Fact | Value |
|---|---|
| inventory classes | 15 (nibbles 0 to `0xE`), 12 with handlers, 3 empty |
| id counts | items 64, equipment 420, loot 512, magicks 81, technicks 24, gambit conditions 256, key items 512 (64 + 32 + 416 + 0), quickenings 32, reward packages 512, selectors 256, bazaar goods 128, gil 4,095; sum 6,892 |
| validator classes | 32, 29 arms; four without a table (1, 19, 22, 23) |
| query classes | 32, 28 arms |
| owned-count cap | 99; reserved field 6 bits |
| refused ids | `0xFFFF`, `0x1000` (Unarmed) in the modify path |

## Operations

Per grant or loss: `0x003008A0` once, the handler once, the derived-index hook on a presence
transition, the obtain line when asked. Per menu row: one query record fill, through a static
copy or the caller's own record. Per area load: `0x00236C30` binds the authored tables, the rebaser
runs on the state block.

## State

The descriptor table's run-time fields (pointers and cumulative bases), the inventory regions of
the party block, the discovery dword, the derived-index lists, the two static query
records.

## Modding notes

- A new id needs three things to agree: a descriptor count that covers its index, an authored
  table with that many rows for the validator and the filler, and a region wide enough in the
  state block for the handler.
- Totals above 99 cannot be stored: the packed word gives the total ten bits and the mutate
  handler clamps at 99 whatever the delta.
- Granting a reward package or a bazaar good is a grant of its parts: the package's own id never
  appears in an inventory region, so a save shows only the items it gave.
- Gil ids `0xE000` to `0xEFFE` carry their amount in the low twelve bits; an amount above 4,094
  needs the gil setter, not an id.
- Classes 10, 12 and 16 are holes in the inventory: their descriptors have a count of 0 and no handler, so
  `0x003008A0` refuses any id with top nibble 5, 7 or `0xB` and the party can never own one. The validator and the
  query filler still accept class-10 ids from `0x5000` while gambit_data has rows (40) and class-16 ids from
  `0xB000` while price_data has rows (128); every class-12 id is refused, because its slot is never bound.
- An encoded id's index is its low twelve bits (`0x00309EC0` at `0x00309F02`, `0x0030AE30` at `0x0030AE72`:
  `and ecx, 0xFFF`), so each of the fifteen classes an id names (5 to 19) reaches at most 4,096 rows, indices 0 to
  `0xFFF`: its table, or for class 13 its four key-item sub-tables together. Rows past that cannot be named by an id.

## Related

- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil and package classes call.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the state block's
  inventory regions sit in the save image.
- [Authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md): the `st2e` header, the
  pack load that binds each slot, and the row arithmetic the readers inline.
- [`item-and-ability-ids-query-record-accesses.tsv`](item-and-ability-ids-query-record-accesses.tsv): every censused
  access to the query record (`EncodedIdQueryRecord`, `0x98` bytes): its row-form copy `0x022CA520` and its id-form
  copy `0x022CA480`, one row per instruction (326 rows).
