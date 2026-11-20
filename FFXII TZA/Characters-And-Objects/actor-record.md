[Home](../../README.md) / [Characters and objects](README.md) / Actor record

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Actor record: the record every field actor is driven through, its pool, its classes, its sub-objects and its lifetime | system | Characters and objects | Field actors | The record behind every actor a manager owns: how the pool is sized and carved from the loaded script payload's per-sequence counts and the eight-entry descriptor table, the class and sequence byte, what the initialiser writes into a fresh record, the interior sub-objects (movement context, secondary context, request entry pool, wait slots) and where each class puts them, the request entry lists and the channel masks, the handle fields, and the two-phase release that frees the pool. | 0x002679F0, 0x00266530, 0x00266AD0, 0x00266BD0, 0x003DB580, 0x003DB550, 0x003DBF60, 0x003DB2A0, 0x003DB640, 0x00358940, 0x0025B070, 0x002628B0, 0x003697F0, 0x00265020, 0x00263C20, 0x003589B0, 0x002659D0, 0x00269FC0, 0x0026BED0, 0x0026B480, 0x0026AD90, 0x0026AB50, 0x0026A140, 0x0026AD40, 0x00269EE0, 0x00269F60, 0x00265060, 0x002638F0, 0x002E9BE0, 0x002638C0, 0x00269DD0, 0x003EC5F0, 0x003EC690, 0x003DC710, 0x003605A0, 0x003E9970, 0x003B6C20, 0x003DEE10, 0x003DEC90, 0x0036DE70, 0x0036E080, 0x002A7A40, 0x002E2300, 0x00368AA0, 0x003EBD70, 0x003604D0, 0x0025A280, 0x002E63D0, 0x003EA200, 0x003E9100, 0x002E1630, 0x0036A280, 0x002E06F0, 0x0035AB50, 0x002ECBE0, 0x002EBDE0, 0x002697A0, 0x0033F650, 0x0025BAD0, 0x0025BE50, 0x0025C230, 0x0025C830, 0x0025B7E0, 0x002675C0 |

## What the player sees

Every townsperson, door, trigger line, party member and monster in a field is one record owned by
one of the five actor managers. When a field or a scene loads, the manager's script payload says
how many actors of each kind it brings, the records are carved out of one block, and each is set up
with its script entry, its position and steering state and its slots for resource requests and
waits. The record stays alive until the manager unloads, when the block is freed.

A handle kept to a record then fails while its slot is unbound. A rebuilt pool starts every discriminator at 1
again, so a handle kept from the old pool names whichever new record has that index.

## How it works

### The pool

`0x002679F0(slot)` builds a manager's record pool from its bound payload (`[slot + 0x00]`) and the
record count at `+0x20` ([actor managers](actor-managers.md)):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | the payload's table at payload `+[0x14]` holds a `u16` count of sequences followed by a `u16` per sequence; the pool's payload size is the sum over sequences of the descriptor's size, rounded up to 16, times that count; |   |
| 2 | the header is `(count * 8 + 0x17) & ~0xF` bytes and is allocated twice over: the block is `2 * header + payload` bytes from the allocator at `[slot + 0x88]`, zeroed, with the count at `+0x00`; `[slot + 0x1F0]` keeps `block + header`; | `0x00267A79`<br>`0x00267A8B` |
| 3 | records are carved from `block + 2 * header` in sequence order; the pointer table at `block + 8` receives each, and each record's byte `+0x03` becomes `(class << 5) \| sequence`; the slot's per-class counts at `+0x1D0` (four `u16`) are added up, and `0x00267B3A`-`0x00267B61` write their running offsets: `+0x1D8` = 0, `+0x1DA` = the class-0 count, `+0x1DC` = classes 0-1, `+0x1DE` = classes 0-2; |   |
| 4 | `0x00266530(slot, block, i)` initialises every record, for `i` from 0 to the count `+0x20` less one (`0x00267B63`-`0x00267B82`, the call at `0x00267B79`), and the block is returned. The per-class counts are added to the words already at `+0x1D0`, and the byte `+0x03` keeps the sequence's low five bits. | `0x00267B89`<br>`0x00267AD4`<br>`0x00267AE8`-`0x00267B13` |

`0x0046BA50(m)` returns `[slot + 0x1F0]` of manager `m`¹ when the slot's `+0x10` bit `0x1` is set, and
otherwise an empty table at `0x02CA6050`, whose first dword it zeroes; `0x0046BA90(m)` returns the count `[slot + 0x1F8]`,
or 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263FF0` |
| ² | `0x0046BA9F`, `0x0046BAAA` |

</details>

The table holds dword handles, not records: four sites call `0x0046BA90` and then `0x0046BA50` (`0x0031F5F9`/`0x0031F607`,
`0x0035E63A`/`0x0035E644`, `0x00465339`/`0x00465344`, `0x00465A79`/`0x00465A84`), and the walker at `0x0031F607` reads each entry as
a dword¹ and resolves it through `0x003588B0`² when its pointer `[rsp + 0xC0]` is
set and `0x02089340` bit `0x10` is set (`0x0031F618`-`0x0031F63E`, up to 512 entries).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031F640`, `0x0031F6DD` |
| ² | `0x0031F642` |

</details>

Five builders fill the table and write its count `+0x1F8`¹
for a slot whose `+0x10` bit `0x1` is set, and 0 for another, each walking the class-3 ordinals from `+0x1DE` for the
count `+0x1D6` through `0x00358940`. A listed record's handle is
`((word +0x16 & 0x7FF) << 4 | manager) << 16 | ordinal`, the fields `0x003588B0` takes apart for a non-zero handle². What each builder leaves out first:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046B7D7`, `0x0046B9B7`, `0x0046BCA5`, `0x0046BE5E`, `0x0046BF3D` |
| ² | `0x003588B6`, `0x003588CB`-`0x003588DC` |

</details>

- `0x0046B690` and `0x0046B870`: a record `0x002647B0` answers 1 for (`+0x12` from 0 to 3; `0x0046B74B`, `0x0046B92B`) or whose
  `+0x18` is 1, then the others [target selection](../Battle-Actions/target-selection.md#actor-manager-lists) lists;
- `0x0046BAC0(m, mode)`: with mode 1 it first lists the class-1 ordinals from `+0x1DA` for `+0x1D2` whose `+0x1C` bit
  `0x4`, `+0x0E` bits `0x40` and `0x80` and `+0x0C` bit `0x2` are set¹; on the class-3 range it
  skips as `0x0046B690` does², then chooses between `0x00322480` and `0x00322490` by mode
 ³;
- `0x0046BD60(m)`: a record whose `+0x18` is 1, whose class nibble is 6 or whose `+0x0E` bit `0x20` is clear, then the
  others [map screens](../Menus-And-HUD/map-screens.md#minimap-markers) lists⁴;
- `0x0046BE80(m)`: a record whose `+0x18` is 1, whose `+0xC0`⁵ is null or starts with -1, or whose `+0x09`
  bit `0x2` is set⁶; its handle takes the manager from `+0x15` and the ordinal from the word
  `+0x00`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046BB12`-`0x0046BB76` |
| ² | `0x0046BBB4`-`0x0046BBC5` |
| ³ | `0x0046BC4D`-`0x0046BD08` |
| ⁴ | `0x0046BDC3`-`0x0046BE17` |
| ⁵ | `0x002E97B0` |
| ⁶ | `0x0046BEDD`-`0x0046BEF9` |
| ⁷ | `0x0046BEFB`-`0x0046BF17` |

</details>

`0x00358940(slot, ordinal)` returns `[block + 8 + ordinal * 8]`, the block being `[slot + 0x08]`, for an ordinal from 0
to below the count `[block + 0]`, and null for any other ordinal or a slot with no block¹. The
builders use its answer with no null test in their loops: `+0x09` &= `0xFD` at `0x0046B6DC` and `0x0046B8BC`, `+0x0A` = 0
at `0x0046B740` and `0x0046BBB0`, and reads of `+0x18` at `0x0046BDC3` and `0x0046BEDD`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00358940`-`0x0035895D` |

</details>

So the table count, the slot's `+0x20` and the class word `+0x1D6` must agree. The class-3 arming `0x00269800` passes
each answer to `0x00269860`, which returns for a null record ([field
runtime](field-runtime.md#the-all-records-loop-and-the-trigger-bit)).

The descriptor table at `0x01E0C328` has eight entries of `{u8 class, u8 sub, u16 size}`:

| Sequence | Class | Sub | Size | Movement context | Secondary context | Request entries | Wait slots |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | `0x328` | no context | no context | `+288`, 10 | `+0x1E8`, 8 |
| 1 | 1 | 0 | `0x3A8` | `+0x120` | no context | `+416`, 10 | `+0x268`, 8 |
| 2 | 1 | 1 | `0x330` | `+0x120` | no context | `+416`, 8 | `+0x240`, 6 |
| 3 | 2 | 0 | `0x348` | `+0x120` | no context | `+320`, 10 | `+0x208`, 8 |
| 4 | 2 | 1 | `0x2D0` | `+0x120` | no context | `+320`, 8 | `+0x1E0`, 6 |
| 5 | 3 | 0 | `0x6E0` | `+0x120` | `+0x350` | `+1240`, 10 | `+0x5A0`, 8 |
| 6 | 3 | 0 | `0x6E0` | `+0x120` | `+0x350` | `+1240`, 10 | `+0x5A0`, 8 |
| 7 | 3 | 1 | `0x668` | `+0x120` | `+0x350` | `+1240`, 8 | `+0x578`, 6 |

`0x00266AD0(record)` plants the pointers from the sequence in `+0x03 & 0x1F`: `+0xB8` = the movement
context, `+0xC0` = the secondary context, `+0xA0` = the request entry pool, `+0xA8` = `+0xA0` plus
`0xC8`, or `0xA0` when the descriptor's `sub` is 1. The request entries are 20 bytes each and the
wait slots 40, so the wait slots end exactly at the record's size on every row. A "no context" cell
is a stored null¹. A sequence above 7 returns before
any store², leaving all four pointers as they were.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00266AFE`, `0x00266B05`, `0x00266B1F`, `0x00266B40` |
| ² | `0x00266ADC`-`0x00266ADF` |

</details>

### The class byte

The bits under mask `0xE0` of `+0x03` are the class and bits `0x1F` the sequence. The movement code accepts class 3
(`+0x03 & 0xE0 == 0x60`); the position read `0x00265020` accepts classes 1 and 3; the `setline` verb
writes class 2 ([battle units](battle-units.md)).

`0x00266BD0` seeds the flag dword `+0x1C` by
sequence: 0 for sequence 0, `0x38` for 1 and 2, `0x40` for 3 and 4, `0x30004` for 5 and 6, `0x34C85`
for 7, and sets `+0x14` bit `0x80` (battle-unit eligible) for sequences 5 and 7; a sequence above 7 writes
neither¹. A separate nibble, bits
`0xF` of `+0x0E`, is what `0x00263C20` returns as the actor class nibble.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00266BDE` |

</details>

### The initialiser

`0x00266530(slot, block, i)` fills record `i` on a zeroed block:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | it clears `+0x14` bit `0x80`, zeroes `+0xEC` and sets `+0xF5` to `0xFF`, picks the counts (8 wait slots and 10 request entries, or 6 and 8 for a `sub` of 1), plants the pointers and seeds `+0x1C` and `+0x14` bit `0x80`; | `0x00266AD0`<br>`0x00266BD0` |
| 2 | it writes `+0x00` = `i`, `+0x10` = 0, `+0x12` = `0xFF`, `+0x15` = the slot index, `+0x16` = 1, `+0x118` = `0x3C0000`, `+0x102` = `0xFFFF`, `+0x04` = `0xFF00`, `+0x20` = `0xFF`, and `+0xF8` = the empty string at `0x02F8F2A0`, whose first four bytes it writes 0; | `0x0026669B` |
| 3 | it writes `+0x100` = 0, `+0x18` = `0xFFFF0000`, `+0x104` = `0xFFFF`, `+0x106` = 0, `+0x0F` = 0, `+0x21` = 0, `+0x0A` = 0, the entry-group word `+0xF6` = 0, and zeroes `+0x28`, `+0x30`, `+0x38`, `+0x10C` and `+0x114`; |   |
| 4 | it sets the flag bytes: `+0x14` = `(old & 0xB0) \| 0x30`, `+0x0D` = `(old & 0xA2) \| 0x82` and `+0x08` = `(old & 0x9F) \| 0x11` on manager 0 (`(old & 0x22) \| 2` and `(old & 0x8F) \| 1` elsewhere);<br>• then `+0x0D` bit `0x20` and `+0x08` bit `0x80` cleared, `+0x0B` &= `0xC0`, `+0x0C` = 8, `+0x09` bits `0x20` and `0x80` cleared, `+0x13` &= `0x3C`, `+0x0E` \|= `0xF0` then `&= 0xF0`, and for class 3 `+0x1C` bits `0x100` and `0x2000` cleared; | `0x0026661B`-`0x002666AC` |
| 5 | it binds the script entry: `+0x02` = 1, or 2 while `i` is below the payload's count word at `+[0x14] + 2` (only compared, `0x00266705`); `+0x40` = the entry at payload `+[0x18] + 4 + i * 0x20` (`0x30` when the payload's word `+0` is 8 or more), with no bound on `i`; `+0x48` and `+0x50` = payload + the resolved dwords at entry `+0x10` and `+0x14`, `+0x58` = payload + entry `+0x08`; | `0x0026656A`, `0x00266710`-`0x00266734` |
| 6 | a tagged entry (byte `+0x06` negative and not `0xFF`) registers the record in the pointer table at `0x0209A1F0` by its low 7 bits (`[0x120000 + rax * 8 + 0x1F7A1F0]`, `0x00266758`-`0x0026677C`): tags 0-3 are the party roster entries the field runtime walks ([field runtime](field-runtime.md)), and tags 4 and above the sixteen pointers from `0x0209A210` that `0x0026CE60` clears on slot 0; |   |
| 7 | the new record gets `+0x12` = the tag and `+0x0F` = 2 for tags 0-3, 3 above. The eviction at `0x00266754`-`0x00266771` tests this record's own `+0x12`, which step 2 set to `0xFF`, so it does not run, and the record the table held keeps its `+0x12` and `+0x0F`; | `0x00266612` |
| 8 | it builds the request entry free list and clears bytes `+0x00`-`+0x16` of the first `+0x88` (channel count) wait slots, which covers every slot only because the two counts are both 8 or both 6; | `0x003DB580` |
| 9 | it runs the movement defaults `0x00265FF0(record, [+0xB8])` and `0x00265B60`. `0x00265FF0` resets the context for the record's class and writes the class nibble: `+0x0E` = `(old & 0xB4) \| 4` for class 1, `(old & 0xF5) \| 5` and `+0x0F` = 3 for class 3, ending with `0x0026D6F0(record, 0.0, 2)`; |   |
| 10 | it resets the secondary context (`+0x138` = 0, `+0x148` = 1.0, `+0x14E` = 1, `+0x140` and `+0x144` = 0 with `0x00268380`), fills the eighteen words `+0xC8`-`+0xEB` with `0xFFFF`, and for a tagged entry with a secondary context sets its `+0x152` = 0 and runs `0x002681E0`; |   |
| 11 | it issues the initial resource requests through `0x003DBB60(record, channel, id, 2, 0)`, counting each request on the last channel in `+0x10`. On channel `channels - 1` it issues the `+0x20` id (only when the payload word `+0` is 10 or more; from `+0xE6`, else the entry row's word `+0x20` when the row's count is 16 or more), then id 0, then the `+0x14` id (`+0xDA`, else row `+0x14` when the count is over 9); |   |
| 12 | on channel 0 it issues the `+0x04` id (`+0xCA`, else row `+0x04` when the count is over 1), not counted. A negative row word (sign-extended, then tested for its sign: `0x00266921`-`0x00266924`, `0x00266994`-`0x00266997`, `0x002669E3`-`0x002669E6`) or an absent row word issues nothing; an override word other than `0xFFFF` is zero-extended and always issues; |   |
| 13 | for a class-3 actor it sets `+0x1C` bit `0x4` from the `+0x06` id (`+0xCC`, else row `+0x06` when the count is over 2), running `0x00268EA0` when `+0x0B` bit `0x8` is set, else clears bit `0x4`; then bit `0x400` from the `+0x16` id (`+0xDC`, else row `+0x16` when the count is over 10) with the same call, and setting bit `0x400` clears bit `0x4` again; else clears bit `0x400`. It ends with `0x003DB280(record)`. |   |

Over the 769 field scripts (`plan_map`), read as `0x00266530` binds them, sequence 7 holds 4,054 entries, 2,202 of them
named `monster_` and none of those tagged; its 724 tagged entries are the party controllers `PC00`-`PC03` (tags 0-3,
181 each), and the other sequences hold 2,224 tagged entries.

### The request entry lists

The pool at `+0xA0` holds the record's 20-byte
[request entries](../Scripts-And-Script-Commands/script-requests.md#the-entry-pool), linked by index: `0x003DB580`
chains them (`+0x00` next, `+0x01` previous, `+0x04` = `0x80000000`, `+0x10` = 0), sets the counts `+0x88`
(channels) and `+0x89` (entries), the free-list head `+0x60` = 0 and the detached head `+0x61` =
`0xFF`, the channel heads `+0x94` and tails `+0x8C` to `0xFF`, and clears the masks `+0x06`,
`+0x24` and `+0x26` (one dword store at `+0x24`, `0x003DB59B`) and the flags byte `+0x63`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB626` |

</details>

The `+0x10` store is a word, clearing the mode and the run state¹. `0x003DB550(record, index)` returns
`[+0xA0] + index * 0x14`, null for `0xFF` and for a null record²; the index is
taken as a signed 32-bit value³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB5C7` |
| ² | `0x003DB550`-`0x003DB55B` |
| ³ | `0x003DB55D` |

</details>

- `0x003DBF60(record, id, class)` walks every channel whose bit in `+0x06` is set, from channel 0 upward
 ¹ and on each from its head, returning the first entry whose `+0x04` word equals `id` or whose
  `+0x12 >> 1` equals `class` (a negative filter is skipped, `0x003DBFDA`, `0x003DBFE8`), bounded by the entry count;
  `0xFF` when no entry matches or the channel count is 0².
- `0x003DB640(record, channel)` tests bit `channel` of `+0x06`.
- `0x003DB2A0(record, index)` removes an entry. An entry in mode 4 (`+0x10`) or with a negative
  channel byte `+0x02` is on the detached list at `+0x61`, otherwise on its channel's list at
  `+0x94[channel]`. It returns bit `0x1` of the entry's flags `+0x12`³; an index of `0xFF` returns
  1 at once⁴, and a null record reads the flags byte at address `0x12`⁵, which faults.
- It removes only that list's head: an empty list (`0xFF`, `0x003DB320`) removes nothing, and a non-head index is
  left in place when it is the tail and otherwise never leaves the loop at `0x003DB326`-`0x003DB33F`. The remover:
  1. unlinks it⁶;
  2. on the detached list, only moves `+0x61` to the entry's next⁷; on a channel list, notifies the
     end of a mode-3 request whose `+0x06` is not `0x8000`
    ⁸, notifies by class⁹ when `+0x12` is 2 or more, fixes the head and tail,
     and clears bit `channel` of `+0x06`, `+0x24` and `+0x26` when the channel empties;
  3. pushes the entry on the free list¹⁰, sets `+0x63` bit `0x2` and makes it the head.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DC016` |
| ² | `0x003DBF77` |
| ³ | `0x003DB2EF` |
| ⁴ | `0x003DB2B0` |
| ⁵ | `0x003DB2EA` |
| ⁶ | `0x003DC1B0` |
| ⁷ | `0x003DB35E` |
| ⁸ | `0x003DC0D0` |
| ⁹ | `0x00263050` |
| ¹⁰ | `0x003DB650` |

</details>

`0x003DB650(record, head, index)` links entry `index` in front of entry `head` in the 20-byte entries at record
`+0xA0`, whose byte `+0x00` is the next index and byte `+0x01` the previous. The entry's next becomes `head`¹ and, for a `head` other than `0xFF`, `head`'s previous becomes `index`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB6D1` |
| ² | `0x003DB6C8`-`0x003DB6CD` |

</details>

The entry's
previous becomes `0xFF` when `head` is `0xFF` or has no previous¹; otherwise it takes the
previous byte of the entry before `head`, and that entry's next becomes `index`². The
function does not test its own entry pointer, which is null for an `index` of `0xFF` or a null record³; with a null record the store at `0x003DB6C3` is made through that null pointer, to
address 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DB678`-`0x003DB6C3` |
| ² | `0x003DB6B5`-`0x003DB6BE` |
| ³ | `0x003DB656`-`0x003DB675` |

</details>

`0x002697A0(record)` re-issues a record's standing requests. It removes the first entry with a
non-zero byte `+0x11` from channel 1 and then from channel 0 (`0x003DB420(record, channel, 3)`, which
walks only that channel and only when its bit in `+0x06` is set), then runs `0x00269640`.

While
`0x02099DE1` is set, `0x00269640` issues on channel 1 the `+0xC8` id (the payload row's word `+0x02`
when `+0xC8` is `0xFFFF` and the row's count is positive) when `+0x1C` bit `0x1` is set, and on channel
0 the `+0xDE` id (row word `+0x18` when the count exceeds 11) when `+0x1C` bit `0x800` is set, both
through `0x003DBB60(record, channel, id, 0, 0)`. A record whose `+0x18` is 1 issues neither.

### The handle

A record is named outside its manager by the handle `0x003589B0` encodes from `+0x00` (the index),
`+0x15` (the manager) and `+0x16` (the discriminator, seeded 1 by the initialiser and advanced by
`0x002659D0` through 1-2047 on a definition change); the resolver `0x003588B0` checks all three against the live record ([battle
units](battle-units.md)).

### The verb accessors

Script verbs reach a record's own bytes, its secondary context `[+0xC0]` and a few globals through
small accessors. Each takes the calling actor unless the row says otherwise:

| Verb | Id | Accessor | What it does |
|---|---|---|---|
| `settargetliststatus(v)` | `0x053A` | `0x00269FC0` | `+0x0E` bit `0x40` = `v != 0` |
| `setnochecktouchheightflag(v)` | `0x020F` | `0x0026BED0` | `+0x08` bit `0x80` = `v != 0` |
| `fieldsign` | `0x0176` | `0x0026B480` | class 1 only: `+0x0D` bit `0x8` = bit `0x1` of the value the verb passes |
| `setmapjumpgroup(i)` | `0x011E` | `0x0026AD90` | stores the actor in `0x0209A210[i]`, an `i` above 15 taken as 15 and a negative `i` as 0 |
| `set_force_char_nearfade(v)` | `0x0552` | `0x0026AB50(1, v)` | the globals `0x02099DA4` = 1 and `0x02099DA5` = `v` |
| `attachinfo(i, ref)` | `0x01C8` | `0x0026A140` | secondary `+0x120 + i * 8` = the address `0x002650B0` resolves `ref` to through the current slot's homes, and secondary `+0x14F` bit `0x4` set |
| `setambient(r, g, b)`, `resetambient` | `0x0116`, `0x0117` | `0x0026AD40` | secondary `+0x151` bit `0x10` set, the colour handed to `0x0026A420`; `resetambient` passes the colour `0x00379900` returns and clears the bit again |
| `fetchambient`, `fetchambient_4e1(x, y, z)` | `0x04E0`, `0x04E1` | `0x0026AD40` | the same bit set, then `0x002E49B0(actor, 0)` or `0x002E49B0(actor, {x, y, z, 1.0})` |
| `set_ignore_hitgroup(v)` | `0x0503` | `0x00269EE0` | byte `+0x119` of the movement body at secondary `+0x138` = `v` |
| `unkCall_5d0(v)` | `0x05D0` | `0x00269F60` | through the render record the secondary context's `+0x00` names (`0x003EC200`), dword `+0x738` = `v`, with the debug print `set root bone physical` |
| `enable_by_chocobo(v)` | `0x040A` | `0x0033F650` | `+0x0B` bit `0x1` = `v != 0` (`0x0033F661`-`0x0033F66A`); the bit is read only while the leader rides (below) |

`0x00269FC0` writes nothing for a null actor (`0x00269FC3`; its two stores to `+0x0E` are `0x00269FC5` and `0x00269FD1`).
`0x00269EE0` writes nothing when the actor's `+0xC0` or
the body at its `+0x138` is null (`0x00269EEA`, `0x00269EF6`; the store of `+0x119` is `0x00269EF8`). `0x00269F60` takes
the secondary context from `0x002E97B0(actor)`
and does nothing when that is null or its dword `+0x00` is -1; otherwise it ends in a jump to `0x003EC200` with
that context's word `+0x00` and `v`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00269F68`-`0x00269F81` |

</details>

The distance verbs `distance3d`, `distance`, `distance_290`, `distance3d_291` (`0x028E`-`0x0291`) and
`isrange`, `isrange_296` (`0x0295`, `0x0296`) read positions through `0x00265060(actor)`, which
returns the movement context of a class-1 or class-3 actor and the static block `0x02099DC0` for any
other actor or a null one. `0x002638F0` returns secondary `+0x140` (0 without a context), and
`0x002E9BE0` the signed secondary byte `+0x13` (-1 without an actor or a context).

While the leader rides a chocobo, the field leaves out every actor whose script has not called
`enable_by_chocobo(1)`: the rider cannot talk to it, touch it or set off its trigger. Six tests read `+0x0B` bit `0x1`,
each only when the chocobo-mode predicate `0x0037C860` (a jump to `0x00303EC0`, control-mode level 2,
[party control modes](../Engine-Core/party-control-modes.md)) answers non-zero, and each treats an actor
without the bit as no candidate:

- the talk tests `0x0025BAD0` (class 3, `0x0025BB69`-`0x0025BB77`, which skips the talk-box test to the function's tail at
  `0x0025BDF3`) and `0x0025BE50` (class 1, `0x0025BE80`-`0x0025BE8F`) ([script requests](../Scripts-And-Script-Commands/script-requests.md));
- the touch test `0x0025C230` (class 3, `0x0025C35E`-`0x0025C36A`) and the trigger-record test `0x0025C830` (class 1,
  `0x0025C8CE`-`0x0025C8DB`);
- `0x0025B7E0` (from `0x003DF6F0`, `0x0025B7F2`-`0x0025B803`) and `0x002675C0` (from `0x002739B0`, `0x002C6F70` and `0x0046BD60`,
  `0x002675F6`-`0x00267603`).

The initialiser's `+0x0B &= 0xC0` clears the bit, so every load starts with it clear.

`0x0025BE50(entry, actor, other, bit, angle)`, the class-1 talk test, works on the context `c` at the actor's
`+0xB8`, which it loads at `0x0025BE63` and uses without a null test.
After the chocobo test above it goes on only when bits `0x1` and `0x4` of `c`'s byte `+0x5D` are both
set, bit `0x1` of the actor's byte `+0x08` is set and bit `0x2` of its byte `+0x0C` is set¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025BE92`-`0x0025BEC1` |

</details>

While `c`'s byte `+0x5C` is 0 it tests the height: the float `+0x04` of `other`, its Y, must be at or above
`c.Y - c[+0x6C] - other[+0xC0] × other[+0x24]` and at or below `c.Y + c[+0x68]`, with `c.Y` the float `+0x04`
of `c`. Outside that band it clears bit `0x2` of the actor's byte `+0x0C` and returns¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025BEC7`-`0x0025BF04` |

</details>

Bit number `bit` of `c`'s dword `+0x60` must be set¹, the float `d` that
`0x003A1960(other, c)` returns must be below the float `0x0209A2B0`², and
`0x003A1BB0(angle, c[+0x50], other[+0x00], other[+0x08], c[+0x10], c[+0x18])` must answer non-zero³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025BF09`-`0x0025BF10` |
| ² | `0x0025BF12`-`0x0025BF30` |
| ³ | `0x0025BF32`-`0x0025BF67` |

</details>

It then stores the entry's dword `+0x28` at `0x0209A2B4`, the actor's word `+0x00` as a dword at `0x0209A2B8`, `d` at
`0x0209A2B0` and 1 in the byte `0x0209A2AA`¹, so `0x0209A2B0` falls with every candidate
accepted.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0025BF69`-`0x0025BF84` |

</details>

`0x002637D0(actor, default)` returns bit `0x2` of the secondary byte `+0x29` when the context exists¹, its
dword `+0x00` is not -1 and that byte's bit `0x1` is set, and `default` otherwise. `0x002ED530(actor)` returns
`0x0030BEB0()` while `0x00265760()` answers non-zero and `0x002637D0(actor, 0)` otherwise; the character draw `0x004256E0`
asks it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E97B0` |
| ² | `0x00425B7D`, `0x00425CD1` |

</details>

The common effect verbs keep one effect job per actor in the movement context: `0x002638C0` reads it
and `0x00269DD0` writes it, at `+0x74` for class 1 and `+0x220` for class 3 (other classes read 0 and
write nothing):

- `charcommoneffectplay(v)` (`0x0465`, `0x00342A80`) ends a running job¹ and zeroes it,
  pushes -1, `v` and 5, runs the nested verb `0x00357620`, and stores the integer result of the
  current wait slot (`0x002651A0`, which also sets that slot's command phase to 2) as the new job;
  - `v` indexes the 14-entry common effect table `0x01EF9400` (effect numbers `0x72`-`0x76`, `0x88`, `0x87`, `0x89`,
    `0x8A`, `0x8C`, `0x8D`, `0x95`, `0x8B`, `0x96`), which `0x0036E750` reads with no bound²
    and hands to `0x003B02A0`, so a `v` of 14 or more reads past the table and a negative `v` reads before it;
- `charcommoneffecttrigger(v)` (`0x0466`, `0x00343080`) passes `v` to the job³;
- `charcommoneffectstop` (`0x0467`, `0x003433A0`) ends the job and zeroes it, as the release below does.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0024CFF0` |
| ² | `0x0036E764`-`0x0036E76B` |
| ³ | `0x0024FE30` |

</details>

### Release

A manager's teardown `0x002628B0` runs in two phases.

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x0025B070(slot)` is the semantic cleanup, run for every bound slot but 4: its only call, `0x00262D34`, is skipped when the slot's `+0x10` bit `0x1` is clear or the slot is 4. For the class-1 and class-3 records (the ranges `+0x1DA`/`+0x1D2` and `+0x1DE`/`+0x1D6`) it ends the movement context's `+0x74` or `+0x220` job and zeroes it. | `0x00262930`<br>`0x00262D2C`-`0x00262D2F`<br>`0x0024CFF0` |
| 2 | The job is `+0x74` of the context `[record + 0xB8]` for a record whose byte `+0x03` says class 1 and `+0x220` for class 3; a job of 0 is skipped and a null record passed over. | `0x0025B0A5`-`0x0025B114`, `0x0025B136`-`0x0025B1A6` |
| 3 | For the class-3 range it also runs `0x002693D0(record, 1)`, the per-`+0x04` teardown (`0x002E3AF0`, `0x003DE5F0` or `0x002E3D00` for 1, 2 or 3) and sets the `+0x04` word to `0xFF00`, whatever that word held. | `0x0025B1A9`-`0x0025B1E5` |
| 4 | Then for every record, ordinals 0 to the count `+0x20` less one, it releases the unit with `0x00234200([slot + 0x28], record)` when `+0x14` bit `0x80` is set and a unit is at `+0x30`, and runs `0x002EB780(record)` for every record, with or without a unit. | `0x0025B200`-`0x0025B237` |
| 5 | The owning release: the block at `[slot + 0x08]` is freed with `0x003697F0`, the pointer nulled, the slot's `+0x10` bit `0x1` and `+0x200` bit `0x4` cleared and `+0x13` zeroed. | `0x00262D96`-`0x00262DB3` |
| 6 | The slot's `+0x00`, `+0x30`, `+0xE8`, `+0x1E0`, `+0x1FC` and `+0x284` are zeroed and `+0x17` bit `0x8` is cleared; the live-slot totals `0x02099DB4`/`0x02099DB8` are recomputed over slots 0-2 and the flag `0x02099DA1` over all five slots; the slot's `+0x108` callback is called once with the slot and then nulled. |   |

Every record address and interior pointer is valid only until that release.

### What else the teardown resets

Besides the record pool, `0x002628B0(slot)` resets state that other systems keep per manager slot,
and on slot 0 state that belongs to the field. Among its calls, in order (rows after `0x003DC710` run only while the slot is bound, `0x00262930`):

| Call | Runs for | What it clears |
|---|---|---|
| `0x003EC5F0` | slot 0 | calls `0x003EB6C0(i)` for `i` = 0-15, each only while `0x00377C20()` is 0 |
| `0x003EC690` | slot 0 | releases the trap marker resource `0x02B5EC94` (`0x002EBD60(id, 0)`, `0x002E3DC0`) and zeroes it ([traps](../World-Areas-And-Travel/traps.md)) |
| `0x003DC710` | slots 0 and 3 | each of the 16 entries of `0x14` bytes at `0x02B57F74` with state byte `+0x02` = 3, byte `+0x03` = 0 and word `+0x00` = 0 gets `+0x10` added to its dword `+0x04` (`byte +0x0F \| 0x10` when bits `0xFFFF0` come out 0), state 4, and `0x02B58170` = 1 |
| `0x003605A0(slot)` | a bound slot | the slot's eight skip entries at `0x022CB730 + slot * 0x80` (byte `+0` = index, `+1` = slot, `+2` and qword `+8` = 0) and its armed and executed masks `0x022CB9C0` and `0x022CB9D8` ([cutscenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `0x003E9970(slot)` | a bound slot | stops (`0x003E98B0(i)`) each of the 64 voice slots at `0x02B5D0B0` whose byte `+0x05` is the slot ([voices](../Sound-And-Music/voices.md)); before the test every voice slot takes its table for the language into `+0x30` (`+0x20` or `+0x28` by `0x002DEBB0`, `0x003E9990`-`0x003E999D`) |
| `0x003B6C20` | a bound slot | the summon group's requested count `0x02EBCC60`, its 32 handles at `0x02EBCBE0`, the unique count `0x02EBCBC0`, the leader handle `0x02EBCC70`, the 32 bytes at `0x02EBCA80` and `0x02EBCA90` (two 16-byte zero stores, `0x003B6C58` and `0x003B6C60`; `0x003B6ED0` clears them too, `0x003B6F12` and `0x003B6F24`) and the dword `0x02EBCAA0` |
| `0x003DEE10(slot)` | a bound slot, twice | the slot's eight event-sound entries at `0x02B59360 + (slot * 8 + i) * 0x38`, below |
| `0x0036DE70(slot)` | a bound slot | each of the 32 script effect slots at `0x022D94B0` whose byte `+0x08` is the slot and whose word `+0x04` has a bit other than bit `0x4` gets word `+0x04` = 4 and, when `0x003B24C0` returns 0 for its handle `+0x00`, `0x003B18E0(handle)` ([native commands](../Scripts-And-Script-Commands/native-commands.md)) |
| `0x0036E080(slot)` | a bound slot | zeroes every dword of the three 64-dword tables `0x022D97B0`, `0x022D98B0` and `0x022D99B0` whose bits `0xF0000` are the slot |
| `0x003E91D0` | a bound slot | when slot `+0xB8` is set: `0x002A7A40(slot +0xC0)` clears bit `0x1` of `0x0209C510 + i * 0x20` and runs `0x0024A680(qword 0x0209C518 + i * 0x20, 0)`; then `+0xB8` = 0 |
| `0x002E2300(0)` | a bound slot | jumps to the `ret` stub `0x0016D6A0` |
| `0x00368AA0(3, 1)` | slot 0 | clears bit `0x8` of `0x02EC0B39` (`0x00368AA0(bit, on)` clears the bit for a non-zero `on` and sets it otherwise; the movie verbs and `setflickerfreemode` also call it) |
| direct stores | slot 0 | `0x02099DA4` and `0x02099DA5`, the pair `set_force_char_nearfade` writes, = 0 |
| `0x003EBD70` | slot 0 | `0x02B5EC60` = 0, frees the block `0x02B5EC68` and zeroes `0x02B5EC70`-`0x02B5EC8F`; the free (`0x003697F0`) and the null store to `0x02B5EC68` run only when that pointer is set (`0x003EBD86`-`0x003EBD90`) |
| `0x003604D0` | slot 0, when `0x003603C0()` is non-zero | every slot's skip entries and masks, as `0x003605A0` does for one, and `0x022CB9BC` = 0 |
| `0x0025A280(2, 0)` | slot 0 | dword `0x020973F0 + 2 * 0x110 + 4` = 0 and, when it was not 0, dword `0x02098570 + 4` = 0 |
| `0x002E63D0` | slot 0 | the keep bit `0x10` of `+0x19` in all 128 binding entries ([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)) |
| `0x003EA200` | slot 0 | with the expanded voice memory `0x02B5E0B0` held: stops each voice slot whose byte `+0x07` is 12 and whose state byte `+0x04` is 2, 3 or 4 (`0x0032E520(0)` first for 2 and 4), runs `0x0036D160(0xC)` and frees the block; every voice slot first takes its table for the language into `+0x30` (`0x003EA225`-`0x003EA235`), the pointer `0x02B5E0B0` is zeroed after the free (`0x003EA287`), and with it null nothing runs (`0x003EA20C`) |
| `0x003E9100` | slot 0 | `0x00408200` when `0x02B5D090` is set, then `0x02B5D090` = 0 |
| `0x002E1630` | slot 0 | returns -1 when `0x00290180()` is 0, 1 when it is 2 and 0 otherwise; a non-zero value runs only a call to the `ret` stub `0x0016D6A0` (`0x00262C4A`) |
| `0x0036A280` | slot 0 | writes 0-14 into the 15 bytes at `0x022D89A8` |
| `0x002E06F0` | slot 0 | the 8 records of `0x68` bytes at `0x0215F200`: a live one (qword `+0x00` set) runs `0x002A2720` with that qword, gets dword `+0x08` = 6, and `0x002F1C50` with the byte at `0x0215F1B6` when its byte `+0x40` is -1 (`0x002E072D`-`0x002E0746`); every byte `+0x40` becomes `0xFE` (`0x002E074D`) |
| `0x0035AB50(0)` | slots 1-3 | slot 0's model list, below |

Each event-sound entry is handled by its state byte `+0x10`: 1 frees its two blocks `+0x08` and
`+0x18`; 5 also releases the block's ids¹ and words² first; 2, 3 and 4 are
waited out (`0x00379E30`, `0x002DEE90`, `0x0032E520(0)`, `0x003DEB30`, `0x0035EA30`) and re-tested. A released
entry gets state 0 and its bit cleared in `0x02B59C20[slot]`. `0x003DEC90(slot, i)`, the release the
`eventsounddispose` verb (`0x0154`) runs, does the same for one entry, except that it hands an
entry in state 1 to `0x003DEFC0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002DF050` |
| ² | `0x002DEB40` |

</details>

Every wait runs `0x0032E520(0)` and `0x0035EA30(0)`; state 2 first pumps the entry's handle `+0x04`¹ and state 4 first calls `0x002DEE90(-1)`, and both of them also run `0x003DEB30`². State 5 releases the dword ids the block `+0x08` counts at `+0x04`, from `+0x20`,
and the words it counts at `+0x10`, from `+0x12`³. A block is freed with `0x003697F0`
and nulled only when it is set, and the bit is `1 << i`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00379E30` |
| ² | `0x003DEE9C`-`0x003DEED1` |
| ³ | `0x003DEEDC`-`0x003DEF24` |
| ⁴ | `0x003DEF79`-`0x003DEF82` |

</details>

An entry in any other state, 0 included, keeps its state and its bit¹. `0x003DEC90` returns at
once for an index above 7², and leaves an entry in state 1 to `0x003DEFC0(entry, slot, i)` without
freeing or clearing anything itself³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003DEED6` |
| ² | `0x003DEC9E` |
| ³ | `0x003DEDE8`-`0x003DEDF0` |

</details>

`0x0035AB50(slot)`, with that slot made current, walks the list of `{name, mask}` pairs the payload's
dword `+0x80` names: for each name that resolves to a binding entry it clears the entry's `+0x19`
bit `0x1` and, for each bit `i` from 1 to 31 set in the mask, releases the hold on lane `i` and then on
lane 0 (`0x002ECAB0(id, i, 0)`, `0x002ECAB0(id, 0, 0)`).

It makes the slot current with `0x0026A480(0x00263FF0(slot))`¹ and ends by making the
slot `0x002640C0()` gave on entry current again (`0x0035AB5A`, tail jump `0x0026A480` at `0x0035AC5A`). The list sits at
the payload `[slot + 0]` plus the low 32 bits of `0x0020E600([payload + 0x80])`: a count dword, then the pairs²; a null payload, a null answer or a count of 0 or less walks nothing³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035AB64`-`0x0035AB6F` |
| ² | `0x0035AB80`-`0x0035AB9F` |
| ³ | `0x0035AB7A`, `0x0035AB8E`, `0x0035ABA7` |

</details>

The id is `0x002E9A60(name)`; an id of 0, or one with no binding entry `0x002E99C0(0x002EB7A0(id))`, is passed
over¹, and the lane releases run only for an id above 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035ABD4`, `0x0035ABE7` |
| ² | `0x0035AC08` |

</details>

The teardown always passes slot 0 to `0x0035AB50`, after the
keep and hold clears the [area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)
page describes. Slot 0's own unload `0x0025AFC0` runs the same tail and then `0x002ECBE0(0)` and
`0x002EBDE0(0)`, which call `0x0036C5D0(handle, 0)` on the 32 handles at `+0x60` of every node of the
list `0x0215FD68` and on the handle `+0x10` of every node of the list `0x0215FD58`, passing over a handle of 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECC22`, `0x002EBDFB` |

</details>

Both follow each node's next pointer `+0x08`¹ and pass their own argument on as the
second one².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECC37`, `0x002EBE06` |
| ² | `0x002ECC26`, `0x002EBDFF` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

Struct ActorRecord size=by sequence (`0x2D0` to `0x6E0`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16` | index | the record's ordinal in its manager |
| `+0x002` | `u8` | entryClass | 1 or 2 from the initialiser |
| `+0x003` | `u8` | classAndSequence | bits under mask `0xE0` class, mask `0x1F` sequence |
| `+0x004` | `u16` | definitionState | `0xFF00` at init and at release |
| `+0x006` | `u16` | channelActiveMask |  |
| `+0x008` | `u8` | flags08 | bit `0x40` set by the field runtime's roster and record loops |
| `+0x00A` | `u8` | field0A | 0 at init |
| `+0x009` | `u8` | flags09 |  |
| `+0x00B` | `u8` | flags0B | bit `0x1` usable while riding (enable_by_chocobo, `0x0033F650`) |
| `+0x00C` | `u8` | flags0C | bit `0x1` the wait resolver's id match |
| `+0x00D` | `u8` | flags0D | bit `0x40` set while the `+0x38` callback runs |
| `+0x00E` | `u8` | flags0E | bits `0xF` the class nibble (`0x00263C20`): 4 class 1, 5 class 3 (`0x00265FF0`) |
| `+0x010` | `u8` | pendingRequests | resource requests the initialiser issued; 0 = idle for the field runtime |
| `+0x011` | `i8` | currentWaitSlot |  |
| `+0x012` | `u8` | slotTag | `0xFF`, or the entry's tag |
| `+0x013` | `u8` | flags13 |  |
| `+0x014` | `u8` | flags14 | bit `0x10` drive the battle unit, bit `0x40` settled, bit `0x80` battle-unit eligible |
| `+0x015` | `u8` | managerIndex |  |
| `+0x016` | `u16` | discriminator | 1 at init |
| `+0x01C` | `u32` | flags1C | seeded by sequence (`0x00266BD0`) |
| `+0x024` | `u16` | channelMask24 |  |
| `+0x026` | `u16` | channelMask26 |  |
| `+0x030` | `u8*` | battleUnit | `0x002134A0` |
| `+0x038` | `void*` | frameCallback | `0x00233F70` for a unit-bound record |
| `+0x040` | `u8*` | scriptEntry | the payload's entry for this actor |
| `+0x048` | `u8*` | functionTable | payload + entry `+0x10` |
| `+0x050` | `u8*` | jumpTable | payload + entry `+0x14` |
| `+0x058` | `u8*` | bytecodeBase | payload + entry `+0x08` |
| `+0x060` | `u8` | entryFreeListHead |  |
| `+0x061` | `u8` | detachedEntryListHead |  |
| `+0x062` | `u8` | selectedEntryIndex |  |
| `+0x063` | `u8` | entryListFlags |  |
| `+0x064` | `i32[4]` | vmRegI | the script VM's integer registers |
| `+0x074` | `f32[4]` | vmRegF | the script VM's float registers |
| `+0x088` | `u8` | channelCount | 8 or 6 |
| `+0x089` | `u8` | entryCount | 10 or 8 |
| `+0x08C` | `u8[8]` | channelTail |  |
| `+0x094` | `u8[8]` | channelHead |  |
| `+0x0A0` | `u8*` | resourceEntries | 20-byte entries |
| `+0x0A8` | `u8*` | waitSlots | 40-byte slots (field runtime page) |
| `+0x0B8` | `u8*` | movementContext | at `+0x120`: `0x80` bytes for sequences 1-2 (class 1), `0x20` for 3-4 (class 2), `0x230` for 5-7 (class 3), null for sequence 0 |
| `+0x0C0` | `u8*` | secondaryContext | `0x188` bytes at `+0x350`, class 3 only |
| `+0x0C8` | `u16[18]` | overrides | `0xFFFF` at init |
| `+0x0F6` | `u16` | entryGroup | 0 at init; stamped by `0x0026CE60` |
| `+0x0F8` | `u8*` | nameText | the literal name (npc-names page) |
| `+0x100` | `u16` | nameLength |  |
| `+0x102` | `i16` | nameId |  |
| `+0x118` | `u32` | field118 | `0x3C0000` at init |

Struct ActorResourceEntry size=`0x14`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | next |  |
| `+0x01` | `u8` | prev |  |
| `+0x02` | `i8` | channel | negative: on the detached list |
| `+0x04` | `u16` | resourceId |  |
| `+0x06` | `u16` | field06 | `0x8000` when unset |
| `+0x10` | `u8` | state | 3 a request in flight, 4 detached |
| `+0x12` | `u8` | classAndFlag | the class in the bits under mask `0xFE` |

</details>

## Operations

- The pool is one allocation per manager; the record count, the per-class counts and the carve
  order all come from the payload's sequence table, and the class is stamped before any record is
  initialised.
- Interior pointers (`+0xA0`, `+0xA8`, `+0xB8`, `+0xC0`) point into the record itself and are valid
  for the life of the block.

## Modding notes

- A script's actor counts set the pool: adding an actor to a scene means adding it to the payload's
  sequence table, which sizes the block.
- Only class-3 records carry a secondary context and can be steered; a class-1 record has a
  position but no steering, a class-2 record is a trigger line.
- A record pointer is dead once the block is freed at unload. A handle resolves to nothing until the slot is bound
  again; after that it names whichever new record has its index, because every discriminator restarts at 1.

## Related

- [Actor record fields](actor-record-fields.md): every reached offset and the two contexts' access tables.
- [Actor managers](actor-managers.md): the slot the pool belongs to.
- [Field runtime](field-runtime.md): the wait slots and the drive loops.
- [Battle units](battle-units.md): the unit bound at `+0x30` and the handle.
- [NPC names](npc-names.md): `+0xF8` and `+0x102`.
- [`actor-sequence-descriptor-accesses.tsv`](actor-sequence-descriptor-accesses.tsv): the reads of the
  descriptor table at `0x01E0C328`, each by its offset in the four-byte entry the sequence selects (6 rows).
- [`actor-storage-record-flags1c-initial-values.tsv`](actor-storage-record-flags1c-initial-values.tsv): the value
  `0x00266BD0` gives the flag dword `+0x1C` for each sequence: `dispatch` the arm its jump table selects, `flags1c`
  the value, `bits_set` its bits as values, and `side_effects` what else the arm does (8 rows). A sequence above 7
  (`byte +0x03 & 0x1F`) leaves `+0x1C` unwritten¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00266BDE` |

</details>

In the descriptor table's rows, `function`, `name` and `site` give the function, its name and the instruction's
address, `disp` the offset in the entry, `kind` `r` (a read), `instruction` the instruction itself, and `route`
`array 0x01E0C328 reg`: an entry of the table at `0x01E0C328` that a register selects.

---

[Actor managers →](actor-managers.md)
