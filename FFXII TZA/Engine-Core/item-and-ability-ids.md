---
title: "Item and ability ids: the sixteen-bit id space, the fifteen inventory classes, the thirty-two-class validator and the query record"
kind: "system"
category: "Engine core"
addresses: "00309440, 01EEBCC0, 0030B6A0, 00322C50, 00323054, 00309EC0, 0030AE30, 0030ADC0, 00309F30, 003008A0, 002FD150, 002FD8D0, 002FD420, 002FD970, 002FD530, 002FD640, 002FD780, 002FD880, 00325F40, 00252E60, 002535D0, 0031C5D0, 0031E598, 0035D330, 0035D380, 0035E070, 00236C30, 003845F0, 0020E600, 00254EE0, 00253690, 0046A630, 00512CD0, 02EBF190"
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
`id & 0xFFF` are the index inside it. `00309440(id)` returns the class: nibble `0xF` gives -1,
otherwise the `+0x38` field of the descriptor at `01EEBCC0 + nibble × 0x58`, which holds 5 for
nibble 0 up to 19 for nibble `0xE`. So the class is the nibble plus five, and the descriptor
table at `01EEBCC0` has fifteen records of `0x58` bytes:

| Offset | Field |
|---|---|
| `+0x00` / `+0x08` | region A: offset into the battle state block `[02EBF190]`, and the pointer the rebaser derives from it |
| `+0x10` | region A length in 16-bit words |
| `+0x18` / `+0x20`, `+0x28` / `+0x30` | regions B and C the same way (0 = none) |
| `+0x38` | class, 5 to 19 |
| `+0x3C` | id count; an index at or past it is invalid |
| `+0x40` | cumulative id base, the running sum of the earlier counts (written at run time) |
| `+0x48` | mutate handler `(id, delta, absolute, channel, flags)` or 0 |
| `+0x50` | query handler `(id, mode)` or 0 |

The rebaser `0030B6A0(state)` adds the state block's address to every non-zero offset, writes
the cumulative bases, zeroes `0x200` bytes at state `+0x57C8` and masks `0x80` bytes at `+0x59C8`
with `0xF8`. It runs from `00233C10` and from `00238A80`, which first points `02EBF190` at
`002EF640() + 0x4E68C` in the save runtime buffer and is called only by the payload reset
`002EF650` ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)). The fifteen
records, read from the image:

| Nibble | Class | Count | Region A (words) | B | C | Handlers | What it holds |
|---|---|---|---|---|---|---|---|
| 0 | 5 | 64 | `+0x4748` (64) | | `+0x57C0` | packed count | items |
| 1 | 6 | 420 | `+0x47C8` (420) | | | packed count | equipment |
| 2 | 7 | 512 | `+0x4B10` (512) | `+0x57C8` | | packed count | loot |
| 3 | 8 | 81 | `+0x4F10` (6) | | | bitset | magicks |
| 4 | 9 | 24 | `+0x4F1C` (2) | | | bitset | technicks |
| 5 | 10 | 0 | | | | none | unused |
| 6 | 11 | 256 | `+0x4F20` (16) | | | bitset | gambit conditions |
| 7 | 12 | 0 | | | | none | unused |
| 8 | 13 | 512 | `+0x4F40` (32) | | | bitset | key items |
| 9 | 14 | 512 | | | | mutate only `002FD530` | reward packages |
| A | 15 | 256 | | | | mutate only `002FD640` | package selectors |
| B | 16 | 0 | | | | none | unused |
| C | 17 | 32 | `+0x4F80` (2) | | | bitset | quickenings |
| D | 18 | 128 | | | | mutate only `002FD780` | bazaar goods |
| E | 19 | 4,095 | | | | mutate only `002FD880` | gil amounts |

The regions abut: each region A ends where the next begins, which is what makes `+0x10` a word
count. The counts sum to 6,892.

### Owning things: the two handler pairs

`003008A0(id, delta, absolute, channel, flags)` is the one entry that changes what the party
owns. It refuses `0xFFFF`, `0x1000` (the Unarmed row) and nibbles above `0xE`, returns -1 for an
index at or past the class's count, reads the channel's value through `00309F30(id, channel)`,
calls the descriptor's mutate handler with the same five arguments, and returns the value after.

When the channel is 1 and the value went from nothing to something it also sets bits of the
state block's flag dword `[02EBF190] + 4`: bit 0 for a magick, plus a school bit found in two
hops (byte `+2` of the magick's row in `02EBF0F0`, `id - 0x3000`, is an action index; word
`+0x2C & 7` of that row in `02EBF138` is k, and `01EECF98[k]` is ORed in when k < 5); `0x40` for a
technick; `0x80` for a quickening `0xC000` to `0xC011` and `0x100` for `0xC012` to `0xC01E`.

The packed-count classes (items, equipment, loot) keep one 16-bit word per id in region A: bits
0 to 9 the owned total, capped at 99, bits 10 to 15 the reserved copies. The query handler
`002FD8D0(id, mode)` returns total minus reserved for mode 0 (which can go negative), the total
for mode 1, the reserved count for mode 2 and the region-B byte for mode 3. The mutate handler
`002FD150` by channel:

- channel 1 sets or adds the total, clamped between the reserved count and 99; when the total
  rose it sets the id's bit in region C (items' ever-owned bitset at `+0x57C0`, byte `index >> 3`,
  bit `index & 7`); then the derived-index hook `00325F40(id, old total, new total)` and, for a
  relative change with flag bit 0, the "You obtain" line `0046A630(id, delta)`;
- channel 0 subtracts `delta` from the reserved count (absolute: reserved = total - `delta`),
  clamped to 0 to total, and returns total minus reserved; channel 2 adds `delta` to it
  (absolute: reserved = `delta`), clamped the same way, and returns the reserved count;
- channel 3 sets or adds the region-B byte, clamped to 0 to 99 (loot's bazaar-sold tally at
  `+0x57C8`).

The bitset classes (magicks, technicks, gambit conditions, key items, quickenings) keep one bit
per id in region A: word `index >> 4`, bit `index & 0xF`. `002FD970(id, mode)` returns that bit
for modes 0 and 1, 0 for mode 2, and the byte-addressed bit of region B or C for modes 3 and 4.
`002FD420` ignores the channel: the new value is `delta` (absolute) or the bit plus `delta`, a
negative clears it and anything above 1 saturates to 1; the hook and the obtain line follow.

The four handler-only classes act on other classes, only for `absolute` 0 and channel 1:

- class 14 (`002FD530`): row `{u32 gil, u16 item, u16 count, u16 item, u16 count}` of the table at
  `02EBF070`; gil through `00254EE0(00253690() + gil × delta)` clamped at 0, with the gil
  "obtain" line `00469E80(gained)` when flag bit 0 is set, then each item that is not `0xFFFF`
  through `003008A0(item, count × delta, 0, 1, flags)`;
- class 15 (`002FD640`): six `u16` ids in the row of `02EBF068`, the first triple, or the second
  when flag bit 1 is set, each granted with `delta`; the first triple tests each id for `0xFFFF`
  on its own, the second grants its sixth id whenever its fifth is not `0xFFFF`;
- class 18 (`002FD780`): three `(u16 item, u8 count)` pairs at `+4`, `+8` and `+0xC` of the row of
  `02EBF058`, each with a non-zero count granted as `count × delta`;
- class 19 (`002FD880`): gil through `00254EE0(00253690() + (id & 0xFFF) × delta)`, clamped at 0:
  the id is the amount.

`00325F40(id, old, new)` runs on a 0 to non-zero or non-zero to 0 transition: it validates the
id with the class-1 arm, returns for a nibble above 10 (the eleven `{map, count}` pairs at
`01EED1B0` cover nibbles 0 to 10, and 9 and 10 are null), maps the nibble (and for equipment the
row's category byte `+9` of `02EBF0F8`, when that table is bound) through the signed-byte maps to
a category list, and appends (`00252E60`) or removes (`002535D0`) the id in that list; those
lists are what the menus page through.

### The thirty-two-class validator

`00322C50(class, id)` answers whether an id is valid for a class. Classes 1 to 32 dispatch
through the 32-entry table at `00323054`, and every arm ends in the shared test `lo ≤ id ≤ hi -
1`, so a bound is a count and the valid set is `[lo, lo + count)`. The count comes from the
`+4` word of an authored table (`st2e`: `+4` rows, `+8` stride, rows from `+0x20`, bound at area
load by `00236C30` through `003845F0`), except for four arms:

- class 1 derives the class from the id with `00309440` and re-enters the switch;
- class 19 uses `0xE000` to `0xEFFF` compiled in, so the last valid id is `0xEFFE`;
- class 22 uses a literal 4 and class 23 a literal 9 (ids 0 to 3 and 0 to 8).

| Class | Base | Table | Class | Base | Table |
|---|---|---|---|---|---|
| 2 | 0 | `02EBF130` party definitions | 18 | `0xD000` | `02EBF058` bazaar goods |
| 3 | 0 | `02EBF120` | 20 | 0 | `02EBF138` actions |
| 4 | 0 | `02EBF150` | 21 | 0 | `02EBF128` battle commands |
| 5 | 0 | `02EBF100` items | 24 | 0 | `02EBF110` magick schools |
| 6 | `0x1000` | `02EBF0F8` equipment | 25, 32 | 0 | `02EBF038` licence nodes |
| 7 | `0x2000` | `02EBF098` loot | 26 | 0 | `02EBF118` statuses |
| 8 | `0x3000` | `02EBF0F0` magicks | 27 | 0 | `02EBF050` elements |
| 9 | `0x4000` | `02EBF0E8` technicks | 28 | 0 | `02EBF0B0` equipment categories |
| 10 | `0x5000` | `02EBF0E0` gambit presets | 29 | 0 | `02EBF040` augments |
| 11 | `0x6000` | `02EBF0D8` gambit conditions | 13 | `0x8000` | `02EBF090` + `02EBF088` + `02EBF080` + `02EBF078`, the four key-item sub-tables summed |
| 12 | `0x7000` | `02EBF0D0` | 14 | `0x9000` | `02EBF070` reward packages |
| 15, 30, 31 | `0xA000` | `02EBF068` package selectors | 16 | `0xB000` | `02EBF060` |
| 17 | `0xC000` | `02EBF0C8` quickenings | | | |

The table has 29 distinct arms for 32 classes: 15, 30 and 31 share one, 25 and 32 another. For
the fifteen inventory classes the arm's base equals `(class - 5) << 12`, the same structure the
descriptors carry. A missing table counts as zero rows, so a null-guarded arm accepts nothing.

### The query record

`0031C5D0(record)` fills a `0x98`-byte record whose `+0` is the class and whose `+4` is the row
(classes 2 to 4 and 19 to 29, 32) or whose `+6` is the id (classes 1, 5 to 11, 13 to 18, 30, 31).
It clears the name pointer at `+0x18` and dispatches through the 32-entry table at `0031E598` by
`class - 1`. Each arm validates with `00322C50` and writes its own fields:

- the name pointer `+0x18`, the description `+0x10`, and an auxiliary text `+0x08` for actions,
  commands and schools;
- the two inventory channels `+0x20` and `+0x24` (`00309EC0(id)` and `0030AE30(id)`, the
  descriptor's query handler with modes 0 and 1);
- class-specific scalars from `+0x28` on.

Every arm's failed validation returns -2 (`0031C650`). Class 1 derives the class from the id,
stores it at `+0` and re-dispatches; class 12 returns -2 at once; class 19 and any class above
32 validate the row and return -1 on a valid one (`0031C63B`); classes 4, 22 and 23 validate and
return 0 with no other output. A successful fill leaves fields it did not write as they were, so
the record is partial, not a fresh value.

Two static records serve most callers: `0035D330(class, row)` writes the row form into
`022CA520` and `0035D380(class, id)` the id form into `022CA480`; both zero all `0x98` bytes
when the fill returns negative and return the record's address either way. The row form has
159 call sites in 75 functions and the id form 15; `0035E070` fills the row record itself for
class 1 with the id in the high word of `+4`, and eleven other functions hand `0031C5D0` their
own record at fourteen sites.

The menus are those callers: the gambit screen's row and page builders (`00567B60`, `0056B100`,
`0056AE80`), the licence screens (`00558CE0`, `005618E0`) and the battle menu's title
`0027D480` use the row form ([gambit screen](../Menus-And-HUD/gambit-screen.md),
[menu screens](../Menus-And-HUD/menu-screens.md)).

The name at `+0x18` is the field half of the callers read and nothing else; the equipment block
`+0x3C` to `+0x60` is read by the equip menus, the licence bytes `+0x21` to `+0x25` by the
licence board. String pointers point into the loaded text banks; the record never allocates or
copies them.

### The empty id

`0xFFFF` is the empty id. The dispatchers refuse it before the nibble test, `003008A0` refuses it,
the bundle rows use it for "no item", a derived-index list blanks a removed entry with it and
compacts past it, an equipment slot holds it when empty and a unit's reserved item at `+0xDC8`
when none is reserved.

One-byte fields use `0xFF` the same way: the relation pool at `02CA81F0` links its 16-byte
records through byte indices at `+0xD` and `+0xE`, and `00512CD0` unlinks a record by writing
`0xFF` into its neighbours' links (then clears the low nibble of its `+0xF` and decrements the
owner's count byte `+0xE` and the pool count `02EBA481`), because index 0 is a real record and
the only free value is the largest the byte can hold.

## Layouts

```python
encoded id (u16): nibble = id >> 12 (0..0xE), index = id & 0xFFF; class = nibble + 5; 0xFFFF = none
01EEBCC0  descriptor[15], 0x58 each (layout above); 01EEBCF8 = record 0's class
[02EBF190] + 0x4748  u16[64]  items          +0x47C8  u16[420] equipment     +0x4B10  u16[512] loot
[02EBF190] + 0x4F10  u16[6]   magicks bits   +0x4F1C  u16[2]   technicks     +0x4F20  u16[16]  gambit conditions
[02EBF190] + 0x4F40  u16[32]  key items      +0x4F80  u16[2]   quickenings   +0x57C0  items ever-owned bits
[02EBF190] + 0x57C8  u8[512]  loot sold tally   +0x59C8  u8[128] masked with 0xF8 by the rebaser
[02EBF190] + 0x04    u32  discovery bits: 0 magick, 2..0x20 school, 0x40 technick, 0x80 / 0x100 quickenings
packed word: bits 0-9 total (0..99), bits 10-15 reserved
00323054  u32[32]  validator arm RVAs by class - 1 (29 distinct)
0031E598  u32[32]  query filler arm RVAs by class - 1 (28 distinct)
EncodedIdQueryRecord (0x98): +0 u32 class; +4 u32 row | +6 u16 id; +8 ptr aux text; +0x10 ptr description; +0x18 ptr name;
  +0x20 s32 channel 0; +0x24 s32 channel 1; +0x28.. class-specific; 022CA520 the row-form copy, 022CA480 the id-form copy
reward package row (12): u32 gil, u16 item, u16 count, u16 item, u16 count
package selector row (12): u16 id[3], u16 id[3]
bazaar good row (36): u16 name, u16 desc, (u16 item, u8 count, u8)[3], u32 price, u16, (u16 loot, u16 count)[3], u16
01EED1B0  {ptr map, u32 count}[11] by nibble: the derived-index category maps
```

## Shipped data

| Fact | Value |
|---|---|
| inventory classes | 15 (nibbles 0 to `0xE`), 11 with handlers, 3 empty |
| id counts | items 64, equipment 420, loot 512, magicks 81, technicks 24, gambit conditions 256, key items 512 (64 + 32 + 416 + 0), quickenings 32, reward packages 512, selectors 256, bazaar goods 128, gil 4,095; sum 6,892 |
| validator classes | 32, 29 arms; four without a table (1, 19, 22, 23) |
| query classes | 32, 28 arms |
| owned-count cap | 99; reserved field 6 bits |
| refused ids | `0xFFFF`, `0x1000` (Unarmed) in the modify path |

## Operations

Per grant or loss: `003008A0` once, the handler once, the derived-index hook on a presence
transition, the obtain line when asked. Per menu row: one query record fill, through a static
copy or the caller's own record. Per area load: `00236C30` binds the authored tables, the rebaser
runs on the state block.

## State

The descriptor table's run-time fields (pointers and cumulative bases), the inventory regions of
the battle state block, the discovery dword, the derived-index lists, the two static query
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
- Classes 10, 12 and 16 are holes in the nibble space: a count of 0 and no handler, so any id with
  top nibble 5, 7 or `0xB` is refused everywhere.

## Related

- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the setter the gil and package classes call.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): where the state block's
  inventory regions sit in the save image.
