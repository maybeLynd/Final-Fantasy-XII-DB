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
interior contexts, which code reaches only through the pointers at `+B8`<sub>h</sub> and `+C0`<sub>h</sub>:

| Table | Region | Rows |
|---|---|---|
| `actor-record-fields.tsv` | the record itself | 1,130 |
| `actor-record-fields-movement-context.tsv` | the movement context, record `+120`<sub>h</sub>, `230`<sub>h</sub> bytes | 708 |
| `actor-record-fields-secondary-context.tsv` | the secondary context, record `+350`<sub>h</sub>, `188`<sub>h</sub> bytes | 309 |
| `actor-record-fields-wait-slots.tsv` | the wait slots behind `+A8`<sub>h</sub> | 14 |
| `actor-record-fields-resource-entries.tsv` | the resource entries behind `+A0`<sub>h</sub> | 82 |

Every instruction in all five tables was disassembled from the executable and matched.

### The regions

| Record offset | Size | Region |
|---|---|---|
| `+000`<sub>h</sub> | `20`<sub>h</sub> | identity and flag bytes: index, entry class, class and sequence, the masks and the eleven flag bytes |
| `+01C`<sub>h</sub> | 4 | the flag dword seeded by sequence |
| `+028`<sub>h</sub> | 8 | a qword zeroed at init |
| `+030`<sub>h</sub> | 8 | the battle unit |
| `+038`<sub>h</sub> | 8 | the frame callback |
| `+040`<sub>h</sub> | `20`<sub>h</sub> | the script entry and its three section pointers |
| `+060`<sub>h</sub> | 4 | the resource entry list heads and flags |
| `+064`<sub>h</sub> | `20`<sub>h</sub> | the script VM's four integer and four float registers |
| `+088`<sub>h</sub> | `18`<sub>h</sub> | the channel counts and the channel tail and head arrays |
| `+0A0`<sub>h</sub> | `20`<sub>h</sub> | the four interior pointers |
| `+0C8`<sub>h</sub> | `24`<sub>h</sub> | the eighteen override words |
| `+0F8`<sub>h</sub> | `0C`<sub>h</sub> | the name text, its length and the name id |
| `+104`<sub>h</sub> | `1C`<sub>h</sub> | sentinels and counters the initialiser sets |
| `+120`<sub>h</sub> | `230`<sub>h</sub> | the movement context (class 1 and above; the position is its first three floats) |
| `+350`<sub>h</sub> | `188`<sub>h</sub> | the secondary context (class 3) |
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

`00266AD0` plants `+B8`<sub>h</sub> = record `+120`<sub>h</sub> for every sequence but 0. The context's first three
floats are the actor's world position: `00265020(actor, x, y, z)` copies `[+B8h] + 0`, `+4` and `+8`
for a class-1 or class-3 actor and zeros otherwise. The field runtime's wait resolver reads the
steering request through `[[+B8h] + F0h]` (its mode at `+29`<sub>h</sub>, its speed at `+7C`<sub>h</sub>), and the
manager cleanup `0025B070` ends a job it keeps at `+74`<sub>h</sub> (class 1) or `+220`<sub>h</sub> (class 3). The
context's own layout is the movement category's.

### The secondary context

`+C0`<sub>h</sub> = record `+350`<sub>h</sub> for sequences 5-7. The initialiser resets its `+138`<sub>h</sub> to 0, `+148`<sub>h</sub> to
1.0, `+14E`<sub>h</sub> to 1 and `+140`<sub>h</sub> and `+144`<sub>h</sub> to 0 (each followed by `00268380`), and `+152`<sub>h</sub> to 0
for a tagged entry; the frozen pass `0025E400` runs `002E5180` on a record whose `+C0`<sub>h</sub> object has a
`+138`<sub>h</sub>.

### The flag bytes at init

| Byte offset | Manager 0 | Other managers |
|---|---|---|
| `08`<sub>h</sub> | `(old & 9Fh) \| 11h`, then bit 7 cleared | `(old & 8Fh) \| 1`, then bit 7 cleared |
| `0D`<sub>h</sub> | `(old & A2h) \| 82h`, then bit 5 cleared | `(old & 22h) \| 2`, then bit 5 cleared |
| `14`<sub>h</sub> | `(old & B0h) \| 30h`; bit 7 for sequences 5 and 7 | the same |
| `0C`<sub>h</sub> | `(old & 71h) \| 8`, then bits 4-6 cleared | the same |
| `0E`<sub>h</sub> | set to `F0`<sub>h</sub>, then `00265FF0` writes the low nibble: 4 for class 1, 5 for class 3 | the same |
| `1C`<sub>h</sub> | 0, `38`<sub>h</sub>, `40`<sub>h</sub>, `30004`<sub>h</sub> or `34C85`<sub>h</sub> by sequence; bits 8 and 13 cleared for class 3 | the same |

## Related

- [Actor record](actor-record.md): the pool, the initialiser and the lists.
- [Field runtime](field-runtime.md): the wait slots.
- [Battle units](battle-units.md): the unit at `+30`<sub>h</sub>.
