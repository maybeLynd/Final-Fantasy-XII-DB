---
title: "Actor record fields: the record offset by offset, its flag bytes, and the movement and secondary contexts"
kind: "reference"
category: "Characters and objects"
addresses: "00266530, 00266AD0, 003DB580, 00265020, 0026AE90, 002E4A10, 0025DF00"
---

## What it lists

The [actor record](actor-record.md) page lays the record out and names its fields. This page carries
the measurements behind it: `actor-record-fields.tsv` lists every access to a record the typed scan
reached through a proven record register, and two further tables list the accesses to the record's
interior contexts, which code reaches only through the pointers at `+0xB8` and `+0xC0`:

| Table | Region | Rows |
|---|---|---|
| `actor-record-fields.tsv` | the record itself | 1,130 |
| `actor-record-fields-movement-context.tsv` | the movement context, record `+0x120`, `0x230` bytes | 708 |
| `actor-record-fields-secondary-context.tsv` | the secondary context, record `+0x350`, `0x188` bytes | 309 |
| `actor-record-fields-wait-slots.tsv` | the wait slots behind `+0xA8` | 14 |
| `actor-record-fields-resource-entries.tsv` | the resource entries behind `+0xA0` | 82 |

Every instruction in all five tables was disassembled from the executable and matched.

### The regions

| Record offset | Size | Region |
|---|---|---|
| `000` | 32 | identity and flag bytes: index, entry class, class and sequence, the masks and the eleven flag bytes |
| `01C` | 4 | the flag dword seeded by sequence |
| `028` | 8 | a qword zeroed at init |
| `030` | 8 | the battle unit |
| `038` | 8 | the frame callback |
| `040` | 32 | the script entry and its three section pointers |
| `060` | 4 | the resource entry list heads and flags |
| `064` | 32 | the script VM's four integer and four float registers |
| `088` | 24 | the channel counts and the channel tail and head arrays |
| `0A0` | 32 | the four interior pointers |
| `0C8` | 36 | the eighteen override words |
| `0F8` | 12 | the name text, its length and the name id |
| `104` | 28 | sentinels and counters the initialiser sets |
| `120` | 560 | the movement context (class 1 and above; the position is its first three floats) |
| `350` | 392 | the secondary context (class 3) |
| after | | the resource entry pool and the wait slots, at the offsets the actor record page's table gives per sequence |

## Columns

Each table has one row per access site:

| Column | Meaning |
|---|---|
| `function` | the function containing the instruction |
| `name` | the name the scan carried for the function, `FUN_` when none |
| `site` | the instruction's address |
| `disp` | the offset reached, relative to the record or to the context |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed and passed on |
| `instruction` | the instruction text, checked against the executable |
| `route` | how the scan knew the register held the object: a seed accessor's return, or an argument passed by a named caller at a named site |
| `note` | `idx` when an index register takes part |

## Data

### The movement context

`00266AD0` plants `+0xB8` = record `+0x120` for every sequence but 0. The context's first three
floats are the actor's world position: `00265020(actor, x, y, z)` copies `[+0xB8] + 0`, `+4` and `+8`
for a class-1 or class-3 actor and zeros otherwise. The field runtime's wait resolver reads the
steering request through `[[+0xB8] + 0xF0]` (its mode at `+0x29`, its speed at `+0x7C`), and the
manager cleanup `0025B070` ends a job it keeps at `+0x74` (class 1) or `+0x220` (class 3). The
context's own layout is the movement category's.

### The secondary context

`+0xC0` = record `+0x350` for sequences 5-7. The initialiser resets its `+0x138` to 0, `+0x148` to
1.0, `+0x14E` to 1 and `+0x140` and `+0x144` to 0 (each followed by `00268380`), and `+0x152` to 0
for a tagged entry; the frozen pass `0025E400` runs `002E5180` on a record whose `+0xC0` object has a
`+0x138`.

### The flag bytes at init

| Byte | Manager 0 | Other managers |
|---|---|---|
| `08` | `(old & 0x9F) \| 0x11`, then bit 7 cleared | `(old & 0x8F) \| 1`, then bit 7 cleared |
| `0D` | `(old & 0xA2) \| 0x82`, then bit 5 cleared | `(old & 0x22) \| 2`, then bit 5 cleared |
| `14` | `(old & 0xB0) \| 0x30`; bit 7 for sequences 5 and 7 | the same |
| `0C` | `(old & 0x71) \| 8`, then bits 4-6 cleared | the same |
| `0E` | set to `0xF0`, then `00265FF0` writes the low nibble: 4 for class 1, 5 for class 3 | the same |
| `1C` | 0, `0x38`, `0x40`, `0x30004` or `0x34C85` by sequence; bits 8 and 13 cleared for class 3 | the same |

## Related

- [Actor record](actor-record.md): the pool, the initialiser and the lists.
- [Field runtime](field-runtime.md): the wait slots.
- [Battle units](battle-units.md): the unit at `+0x30`.
