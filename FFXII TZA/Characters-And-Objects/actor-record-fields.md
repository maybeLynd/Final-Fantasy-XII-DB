[Home](../../README.md) / [Characters and objects](README.md) / Actor record fields

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Actor record fields: the record offset by offset, its flag bytes, and the movement and secondary contexts | reference | Characters and objects | Field actors | The access tables of the actor record and its two interior contexts: the accesses reached from every holder of a record, by function, site, offset and instruction; the record's regions and the fields the actor record page names; the movement context at record +0x120 with the position at its head; and the secondary context at record +0x350. | 0x00266530, 0x00266AD0, 0x003DB580, 0x00265020, 0x0026AE90, 0x002E4A10, 0x0025DF00 |

## What it lists

The [actor record](actor-record.md) page lays the record out and names its fields. This page carries
the measurements behind it: [`actor-record-fields.tsv`](actor-record-fields.tsv) lists the accesses to a record
reached from every holder listed below, and five
further tables list the accesses to the record's interiors, which code reaches through the pointers at `+0xA0`, `+0xA8`, `+0xB8`
and `+0xC0` of a record it holds:

| Table | Region | Rows |
|---|---|---|
| [`actor-record-fields.tsv`](actor-record-fields.tsv) | the record itself | 1,961 |
| [`actor-record-fields-movement-context.tsv`](actor-record-fields-movement-context.tsv) | the movement context, record `+0x120`: `0x230` bytes for class 3, `0x80` for class 1, `0x20` for class 2 | 991 |
| [`actor-record-fields-secondary-context.tsv`](actor-record-fields-secondary-context.tsv) | the secondary context, record `+0x350`, `0x188` bytes | 849 |
| [`secondary-context-element-accesses.tsv`](secondary-context-element-accesses.tsv) | the `0x30`-byte elements at the start of the secondary context, each access by its offset in the element; every site is also a row of the secondary-context table, and every secondary-context access below `+0x120` has a row here | 594 |
| [`actor-record-fields-wait-slots.tsv`](actor-record-fields-wait-slots.tsv) | the wait slots behind `+0xA8` | 32 |
| [`actor-record-fields-resource-entries.tsv`](actor-record-fields-resource-entries.tsv) | the request entries behind `+0xA0` | 96 |

Every access whose base register holds a record, followed from the holders below, is a row. The records come from the
handle
resolver `0x003588B0`, the current-actor getter `0x00358940`, the ordinal resolver `0x003587C0`,
the roster getter `0x00263750` and the 9 functions that return their records, from the record the initialiser
`0x00266530` builds, and from the 1,885 script natives, which receive records in `rcx` and `rdx`. Every
record passed in an argument register at a direct call or jump is followed, to a fixed point: 1,079 further functions
receive one.

Two stored record pointers are followed as well: the 32-bit offset `0x0037B4D0` decodes with `0x0020E600` from its
binding block, and the record bound to a presentation entry's render record (render record `+0x108`, stored by
`0x002E28E0`). Records held only in other stored pointers or offsets, or passed only to functions called through a
pointer, are not in the table. Of the 58 functions that reference the manager slots `0x02098E10`, 32 have no row: 29 use only slot fields and the
payload or pass a record on, and `0x00263AC0`, `0x0026C3E0` and `0x0026C5D0` read a record held in a stored pointer.

The interiors were followed from every record so held, through their pointers, through the 47 functions that receive
an interior pointer in an argument register, through the entry resolver `0x003DB550` and through `0x002651A0`,
which returns the current wait slot's integer result `+0x0C` and sets the slot's phase `+0x15` to 2
(`0x002651B0`, `0x002651B5`).

### The regions

| Record offset | Size | Region |
|---|---|---|
| `+0x000` | `0x1C` | identity and flag bytes: index, entry class, class and sequence, the masks and the eleven flag bytes |
| `+0x01C` | 4 | the flag dword seeded by sequence |
| `+0x020` | 8 | the byte `+0x20`, the word `+0x21`, the byte `+0x23` and the channel bit words `+0x24` and `+0x26` |
| `+0x028` | 8 | a qword zeroed at init |
| `+0x030` | 8 | the battle unit |
| `+0x038` | 8 | the frame callback |
| `+0x040` | `0x20` | the script entry and its three section pointers |
| `+0x060` | 4 | the request entry list heads and flags |
| `+0x064` | `0x20` | the script VM's four integer and four float registers |
| `+0x088` | `0x18` | the channel counts and the channel tail and head arrays |
| `+0x0A0` | `0x28` | the four interior pointers, at `+0xA0`, `+0xA8`, `+0xB8` and `+0xC0` |
| `+0x0C8` | `0x24` | the eighteen override words |
| `+0x0F8` | `0x0C` | the name text, its length and the name id |
| `+0x104` | `0x1C` | sentinels and counters the initialiser sets |
| `+0x120` | `0x230` | the movement context (class 1 and above; the position is its first three floats). `0x230` is class 3's extent; it is `0x80` for class 1 and `0x20` for class 2 ([actor record](actor-record.md)) |
| `+0x350` | `0x188` | the secondary context (class 3) |
| after | | the request entry pool and the wait slots, at the offsets the actor record page's table gives per sequence |

## Columns

Each table has one row per access site:

| Column | Meaning |
|---|---|
| `function` | the function containing the instruction |
| `name` | the name the scan carried for the function, `FUN_` when the scan carried no name |
| `site` | the instruction's address |
| `disp` | the offset reached, relative to the record, to the context or, in the element table, to the element |
| `kind` | `r` read, `w` write, `rw` read-modify-write, `addr` the address is formed and passed on |
| `instruction` | the instruction text |
| `route` | how the function reached the object: `the record pool or a static record` when it resolved the record itself, `argN from F at S` when the object came in as argument N (0 = `rcx`, 1 = `rdx`, 2 = `r8`, 3 = `r9`) from the caller F at the call site S (`argN+0xK` when offset by K; where several call sites pass the record, the route names the lowest-address direct call site, and a script native names the verb lifecycle's table call at `0x002621D0`), `actor +0xP, the actor as argN from F at S` or `actor +0xP, the actor in R` when the function loaded the interior from a record it held in that argument or register, `chain from the record: ...` for the slot and entry arrays walked from the record's counts, `a context the function resolved itself`, `a slot the function resolved itself` and `an entry the function resolved itself` in the context, wait-slot and entry tables when the function found the record itself, as for `the record pool or a static record`, and took the object from it, `ctor` for the record constructor, and `embed SecondaryContext+0x0` in the element table: the elements at the start of the secondary context |
| `note` | `idx` when an index register takes part |

## Data

### The movement context

`0x00266AD0` plants `+0xB8` = record `+0x120` for sequences 1 to 7 and null for sequence 0
(`0x00266AFE`). A sequence above 7 (`+0x03` bits `0x1F`, compared at `0x00266ADC`) returns before any
store (`0x00266ADF`), leaving `+0xB8` as it was.

The context's first three floats are the actor's world position: `0x00265020(actor, x, y, z)` copies
`[+0xB8] + 0`, `+4` and `+8`
for a class-1 or class-3 actor and zeros otherwise. The field runtime's wait resolver reads the
steering request through `[[+0xB8] + 0xF0]` (its mode at `+0x29`, its speed at `+0x7C`), and the
manager cleanup `0x0025B070` ends a job it keeps at `+0x74` (class 1) or `+0x220` (class 3). The
context's own layout is the movement category's.

`0x00265FF0(record)` resets the movement context, which it reads from `+0xB8`, by the record's class, `+0x03` shifted
right by 5 (`0x0026601B`-`0x00266037`, `0x00266042`, `0x0026636A`, `0x002663A7`). Its second argument, which the initialiser
passes as `[+0xB8]`, goes unused: `rdx` is written before any use (`0x0026629A`, `0x002663FA`). It first sets the record's
`+0x09` to `(old & 0xE9) | 1` (`0x00266010`-`0x00266018`). Classes 0 and 4 to 7 get nothing more (`0x00266037`), and every
class ends in `0x0026D6F0(record, 0.0, 2)`, the speed scale `[0x01DFE0BC]` times 0.0, through a tail jump
(`0x00266507`-`0x00266526`).

For class 2 it writes `(0, 0, 0, 1.0)` to the context's `+0x00` and `+0x10` (`0x00266371`-`0x00266384`) and clears bit
`0x40` of the record's `+0x09` and `+0x0B` (`0x0026638F`, `0x00266397`).

For class 1 the context's talk half-angle `+0x50` becomes 6.2832 (2 pi), `+0x54`-`+0x5B` and `+0x60` become 0, `+0x70`
becomes 1.0 and the low three bits of `+0x5D` are cleared (`0x002663BA`-`0x002663D1`). The talk pair `+0x40` and the touch
pair `+0x30` are each reset by `0x003DA830` and set by `0x003DA860(pair, 0, 0.01, 0.01, 1.0, 1.0)`
(`0x002663D8`-`0x0026642B`). Then `(0, 0, 0, 1.0)` goes to `+0x00`, `+0x10` and `+0x20`, the height `+0x68` becomes -1.0
with `+0x5C` = 1, `+0x6C` becomes 0.5 and `+0x74` 0, and bit `0x40` of the record's `+0x09` and `+0x0B` is cleared
(`0x00266435`-`0x00266480`).

For class 3 the context gets `(0, 0, 0, 1.0)` at `+0x00` and `+0x40`, 1.0 at `+0x20`, `+0x24`, `+0x28` and the margin
`+0xFC`, `{37, 50, 37}` in `+0x104`-`+0x106`, 0 in `+0x100`, `+0x228` and `+0xDC`, and `+0x107` = `(old & 0xFD) | 1`
(`0x00266049`-`0x002660B7`, `0x002660ED`). It also sets the record's `+0x0F` to 3 (`0x002660B3`). The steering request `+0xF0`
points at the context's own `+0x120` (`0x002660D7`, `0x002660F4`). `0x0026AA60(record, 0.2094)` stores that angle, wrapped
into -pi to pi, at `+0xB0` (`0x002660FB`, `0x0026AAB8`); a later store of the pair `{0.15708, 0}` replaces it
(`0x00266227`).

The blocks at `+0x140` and `+0x1C0` get the same reset: 3.1416 (pi) at their `+0x30`, `+0x34` and `+0x3C`, 0.15708 at
`+0x38` and `+0x4C`, 0 at `+0x00`-`+0x07`, `+0x0C`-`+0x13`, `+0x1C`-`+0x23`, `+0x2C`, `+0x45`, `+0x50`, `+0x54` and
`+0x5C`, and bit `0x80` of `+0x42` cleared; after each, bits `0x1` and `0x2` of the steering request's `+0x6A` are
cleared (`0x00266100`-`0x0026620C`).

Then `+0x10`-`+0x1C` takes a copy of the zeroed position with `+0x1C` = 1.0 (`0x00266210`-`0x00266239`). `+0xA8`-`+0xAF`
and `+0x224` are zeroed, the height `+0xC0` and talk height `+0xC8` become 2.0, `+0xC4` and the talk depth `+0xCC`
0.5, and `+0xDD` 0 (`0x00266232`-`0x00266274`).

The body ellipse `+0x50`, the talk ellipse `+0x70` and the touch ellipse `+0x60` are reset (`0x003DA830`), `+0xDE` and
`+0xDF` become 1, and `0x003DA860(+0x50, +0x80, 0.5, 0.5, 1.0, 1.0)` sets the body radii and the body base `+0x80` to
0.5 and 0.5; `0x003DA890` gives the talk ellipse the body's radii with margin 0.5 and the touch ellipse with margin 0.3
(`0x0026627B`-`0x002662EE`).

It sets the talk half-angle `+0xBC` to 1.5708 (pi / 2) and zeroes `+0xA0`-`+0xA7` and `+0xD8` (`0x002662F3`-`0x00266305`),
sets bit `0x40` of the record's `+0x09` and clears it in `+0x0B` (`0x00266310`, `0x00266318`). Then it sets `+0x98` = 0.5,
`+0x9C` = 0.67, the speed `+0xE0` = 0.1, `+0xE4` = 0.15, and 0 in `+0x220` and `+0x108`-`+0x117`
(`0x0026631F`-`0x00266359`). Every class-3 record also gets 0 in the two blocks' words `+0x08` and bytes `+0x44`, in the
steering request's `+0x24` and speed `+0x7C`, and in `+0xD0`, and `+0xF8` = -1.0 (`0x00266484`-`0x002664FD`).

### The secondary context

`+0xC0` = record `+0x350` for sequences 5-7. The initialiser resets its `+0x138` to 0, `+0x148` to
1.0, `+0x14E` to 1 and `+0x140` and `+0x144` to 0 (each followed by `0x00268380`), and `+0x152` to 0
for a tagged entry; the frozen pass `0x0025E400` runs `0x002E5180` on a record whose `+0xC0` object has a
`+0x138`.

### The flag bytes at init

| Byte offset | Manager 0 | Other managers |
|---|---|---|
| `+0x08` | `(old & 0x9F) \| 0x11`, then bit `0x80` cleared; `0x00265FF0` then applies `(v & 0xF5) \| 4` for classes 1 and 2 and `(v & 0xFB) \| 0xA` for class 3 (`0x0026638B`-`0x0026639B`, `0x0026645B`-`0x0026646B`, `0x0026630C`-`0x0026631C`) | `(old & 0x8F) \| 1`, then bit `0x80` cleared; the same for classes 1 to 3 |
| `+0x0D` | `(old & 0xA2) \| 0x82`, then bit `0x20` cleared | `(old & 0x22) \| 2`, then bit `0x20` cleared |
| `+0x14` | `(old & 0xB0) \| 0x30`; bit `0x80` for sequences 5 and 7 | the same |
| `+0x0C` | 8, or `0x18` for class 3: `(old & 0x70) \| 8`, then bits under mask `0x70` cleared; for class 3 the tail `0x0026D6F0(record, 0.0, 2)` of `0x00265FF0` then sets bit `0x10` (`0x0026D74C`) | the same |
| `+0x0E` | set to `0xF0`, then `0x00265FF0` makes it `0xB4` for class 1 and `0xF5` for class 3; classes 0 and 2 keep `0xF0` | the same |
| `+0x1C` | 0, `0x38`, `0x40`, `0x30004` or `0x34C85` by sequence; bits `0x100` and `0x2000` cleared for class 3 by the initialiser (`0x002666ED`-`0x002666F1`) and again by `0x00265FF0` (`0x002660C2`-`0x002660CC`); for class 3 the initialiser then sets or clears bits `0x4` and `0x400` from the `+0x06` and `+0x16` resource ids (`0x00266A00`-`0x00266AA4`, [actor record](actor-record.md)) | the same |

## Related

- [Actor record](actor-record.md): the pool, the initialiser and the lists.
- [Field runtime](field-runtime.md): the wait slots.
- [Battle units](battle-units.md): the unit at `+0x30`.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 5 calls with 2 other topics</summary>

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

| Function | | Functions |
|---|---|---|
| `0x00263750` | is called by | `0x00226BE0` |
| `0x00358940` | is called by | `0x00226BE0` |

**World, areas and travel** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [game over](../World-Areas-And-Travel/game-over.md), [actor model rebuild](actor-model-rebuild.md))

| Function | | Functions |
|---|---|---|
| `0x002E28E0` | calls | `0x00377C20` |
| `0x0037B4D0` | calls | `0x00377A90`, `0x00377DB0` |

</details>
