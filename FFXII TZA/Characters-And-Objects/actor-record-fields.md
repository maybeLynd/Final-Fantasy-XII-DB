---
title: "Actor record fields: the record offset by offset, its flag bytes, and the movement and secondary contexts"
kind: "reference"
category: "Characters and objects"
addresses: "0x00266530, 0x00266AD0, 0x003DB580, 0x00265020, 0x0026AE90, 0x002E4A10, 0x0025DF00"
---

## What it lists

The [actor record](actor-record.md) page lays the record out and names its fields. This page carries
the measurements behind it: `actor-record-fields.tsv` lists the accesses to a record found from every holder the census followed, and four
further tables list the accesses to the record's interiors, which code reaches through the pointers at `+0xA0`, `+0xA8`, `+0xB8`
and `+0xC0` of a record it holds:

| Table | Region | Rows |
|---|---|---|
| `actor-record-fields.tsv` | the record itself | 1,223 |
| [`actor-record-fields-movement-context.tsv`](actor-record-fields-movement-context.tsv) | the movement context, record `+0x120`, `0x230` bytes | 759 |
| [`actor-record-fields-secondary-context.tsv`](actor-record-fields-secondary-context.tsv) | the secondary context, record `+0x350`, `0x188` bytes | 392 |
| [`actor-record-fields-wait-slots.tsv`](actor-record-fields-wait-slots.tsv) | the wait slots behind `+0xA8` | 26 |
| [`actor-record-fields-resource-entries.tsv`](actor-record-fields-resource-entries.tsv) | the resource entries behind `+0xA0` | 88 |

Every way to a record was followed: the manager pools and the static records the table's own rows resolve, the
handle resolver `0x003588B0` and the current-actor getter `0x00358940`, the 251 functions proven to take a record in an
argument register, and the pointers all of these pass on; the 35 other functions that reference the manager slots
`0x02098E10` touch slot fields, not records. The interiors were followed from every record so held, through their
pointers and through the entry resolvers `0x003DB550` and `0x002651A0`.

### The regions

| Record offset | Size | Region |
|---|---|---|
| `+0x000` | `0x20` | identity and flag bytes: index, entry class, class and sequence, the masks and the eleven flag bytes |
| `+0x01C` | 4 | the flag dword seeded by sequence |
| `+0x028` | 8 | a qword zeroed at init |
| `+0x030` | 8 | the battle unit |
| `+0x038` | 8 | the frame callback |
| `+0x040` | `0x20` | the script entry and its three section pointers |
| `+0x060` | 4 | the resource entry list heads and flags |
| `+0x064` | `0x20` | the script VM's four integer and four float registers |
| `+0x088` | `0x18` | the channel counts and the channel tail and head arrays |
| `+0x0A0` | `0x20` | the four interior pointers |
| `+0x0C8` | `0x24` | the eighteen override words |
| `+0x0F8` | `0x0C` | the name text, its length and the name id |
| `+0x104` | `0x1C` | sentinels and counters the initialiser sets |
| `+0x120` | `0x230` | the movement context (class 1 and above; the position is its first three floats) |
| `+0x350` | `0x188` | the secondary context (class 3) |
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
| `instruction` | the instruction text |
| `route` | how the function reached the object: `the record pool or a static record` when it resolved the record itself, `argN from F at S` when the object came in as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`, 3 = `r9`) from the caller F at the call site S (`argN+0xK` when offset by K), `actor +0xP, the actor as argN from F at S` or `actor +0xP, the actor in R` when the function loaded the interior from a record it held in that argument or register, `chain from the record: ...` for the slot and entry arrays walked from the record's counts, and `ctor` for the record constructor |
| `note` | `idx` when an index register takes part |

## Data

### The movement context

`0x00266AD0` plants `+0xB8` = record `+0x120` for every sequence but 0. The context's first three
floats are the actor's world position: `0x00265020(actor, x, y, z)` copies `[+0xB8] + 0`, `+4` and `+8`
for a class-1 or class-3 actor and zeros otherwise. The field runtime's wait resolver reads the
steering request through `[[+0xB8] + 0xF0]` (its mode at `+0x29`, its speed at `+0x7C`), and the
manager cleanup `0x0025B070` ends a job it keeps at `+0x74` (class 1) or `+0x220` (class 3). The
context's own layout is the movement category's.

### The secondary context

`+0xC0` = record `+0x350` for sequences 5-7. The initialiser resets its `+0x138` to 0, `+0x148` to
1.0, `+0x14E` to 1 and `+0x140` and `+0x144` to 0 (each followed by `0x00268380`), and `+0x152` to 0
for a tagged entry; the frozen pass `0x0025E400` runs `0x002E5180` on a record whose `+0xC0` object has a
`+0x138`.

### The flag bytes at init

| Byte offset | Manager 0 | Other managers |
|---|---|---|
| `+0x08` | `(old & 0x9F) \| 0x11`, then bit `0x80` cleared | `(old & 0x8F) \| 1`, then bit `0x80` cleared |
| `+0x0D` | `(old & 0xA2) \| 0x82`, then bit `0x20` cleared | `(old & 0x22) \| 2`, then bit `0x20` cleared |
| `+0x14` | `(old & 0xB0) \| 0x30`; bit `0x80` for sequences 5 and 7 | the same |
| `+0x0C` | `(old & 0x71) \| 8`, then bits 4-6 cleared | the same |
| `+0x0E` | set to `0xF0`, then `0x00265FF0` writes the low nibble: 4 for class 1, 5 for class 3 | the same |
| `+0x1C` | 0, `0x38`, `0x40`, `0x30004` or `0x34C85` by sequence; bits `0x100` and `0x2000` cleared for class 3 | the same |

## Related

- [Actor record](actor-record.md): the pool, the initialiser and the lists.
- [Field runtime](field-runtime.md): the wait slots.
- [Battle units](battle-units.md): the unit at `+0x30`.
