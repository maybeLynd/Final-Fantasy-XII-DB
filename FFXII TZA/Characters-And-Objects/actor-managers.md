---
title: "Actor managers: the five manager slots at 0x02098E10, their bind, their record pool, their variable homes and their camera entry tables"
kind: "system"
category: "Characters and objects"
addresses: "0x02098E10, 0x02099D70, 0x0026C8C0, 0x0026CE60, 0x00358940, 0x002679F0, 0x00264640, 0x0026ABA0, 0x0026B730, 0x00265270, 0x00264D20, 0x0026ADC0, 0x00264800, 0x0026AD10, 0x002640C0, 0x002640D0, 0x002673F0, 0x00267310, 0x003DA400, 0x003DA370, 0x003DA000, 0x003DA4D0, 0x003DA570, 0x003DA2D0, 0x003DD230, 0x003DCF60, 0x003DD1F0, 0x0026B790, 0x0026B800, 0x0026B870, 0x003DA500"
---

## What the player sees

Everything that moves or talks in a field belongs to one of five managers. The first one owns the
field itself: its townspeople, doors, pots and triggers, the party and the music. The others hold
the actors a cutscene or an event brings in, so that a scene can load its own cast without
touching the field's. Loading a field or a scene binds a script file to a manager, carves out the
records for its actors, and from then on the per-frame pass drives those actors through that
manager ([field runtime](field-runtime.md)).

## How it works

### The slot array

A manager slot is a `0x288`-byte block; five of them sit at `0x02098E10`, so slot `n` is
`0x02098E10 + n * 0x288` and the array ends at `0x02099AB7`. `0x02099D70` holds the slot being worked on:
the bind and the pass store it there, `0x002640C0` returns it and `0x002640D0` returns that slot's index
`+0x28`. Three one-byte getters take a slot index: `0x002673F0` returns `+0x13`, `0x00267310` returns
`+0x201`, and the field pass reads `+0x10`.

### The bind

`0x0026C8C0(slot, payload, callback)` binds a loaded definition payload to a slot (its stack frame
holds the slot pointer in `0x02099D70` for the duration):

1. it zeroes the eight qwords `+0x244`-`+0x27C`, clears `+0x200` bit 2, writes the slot index to
   `+0x28` and the payload pointer to `+0x00`;
2. on slot 0 it also runs `0x00238B00`, zeroes `+0x204`-`+0x243` of slots 0-3, runs `0x002EF350(1)` and
   releases the two kind `0xD` and `0xE` registrations at `0x02099DD0` and `0x02099DD8` (`0x00369760`,
   `0x0036D160`, `0x003697F0`);
3. still on slot 0: `0x0025A990` when `0x00377440(field)` is non-zero and `0x0025AA30` when
   `0x00377480(field)` is 0, then `0x003ACA90(8)`, `0x00360110`, `0x002E24B0`, `0x00408AD0`, `0x0036E3B0`,
   `0x0026FFA0(1)`, `0x002700C0(1)`, `0x002EC590(1)`, `0x002EC5A0(1)`, the clears of `0x02099DE8[0..7]` and
   `0x0209A2A0[0..7]`, and `0x0042ED30`;
4. between the slot-0 extras and the pointer block it makes one indirect call through a checked
   function pointer with the slot index as its argument;
5. it fills the pointer block: `+0x88` = the callback or `0x00267930` when none was given, `+0x48` =
   the persistent save payload (`0x002EF2B0()`), `+0x50` = payload + payload `+0x48`, `+0x58` =
   `0x02099DF0`, `+0x60` = `0x02099FF0`, `+0x98` = `0x00264E30`;
6. it sets `+0x68`, `+0x70`, `+0x78` and `+0x80` = payload + its dwords `+0x20`, `+0x24`, `+0x28` and
   `+0x2C`, and zeroes `+0x40`, `+0x1E0`, `+0x1F0` and `+0x1F8`;
7. it sums the `u16` entries of the payload's table at payload `+[0x14]` (a count followed by the
   entries, added in pairs with the odd tail) into `+0x20`, the record count;
8. it resets the flag bytes: `+0x10` = `0x82` (bits 1 and 7 only), `+0x11` = `(old & 0xF8) | 1` (bit 0
   set, bits 1 and 2 cleared, so a bind un-suspends the slot), `+0x13` and `+0x14` = 1, `+0x15` =
   (slot index is not 3), `+0x16` = 1, `+0x17` = `(old & 0x40) | 0x23` with bit 7 set only on slot 0;
9. it sets `+0x12` = (the payload's `i16 +0x50` is not negative), `+0x200` bit 0, and bit 1 on slot 0
   (cleared elsewhere), and zeroes `+0x201`, `+0x24`, `+0x30` and `+0x38`;
10. it zeroes `+0xA0`-`+0xB8`, `+0xC8`-`+0xF8`, `+0x100`, `+0x108`, `+0x1D0`, `+0x1E8` and `+0x1FC`,
   runs `0x00263660` and `0x003DDC20(index, 0)`, and on slot 3 `0x00359200(1)` after a `0x0026D6F0` on the
   focus actor;
11. `0x02099DA1` becomes 1 when any slot's `+0x17` bit 3 is set; on slot 0 the field state is reset
   (`0x0026DB30`, `0x002EBDB0(0)`, `0x002ECB70(0)`, `0x0209A2C4[1..3]` = 1, `0x002EDA60`, `0x002EDA80`, `0x002EDA50`,
   `0x002EDA70`, `0x002EDA40`, `0x002E83A0`, `0x002EDA30`, `0x002EBC30`); `0x003DD790(index)` ends the bind.

### The record pool

`0x0026CE60(slot)` runs after the bind for a slot whose `+0x10` bit 0 is clear and `+0x13` is set:

1. it allocates the record pool with `0x002679F0(slot)` and stores it at `+0x08`
   ([the actor record](actor-record.md)), then runs `0x00266C50`,
   `0x002342F0` on slot 0, and `0x00265A20` ([battle units](battle-units.md));
2. on slot 0 it makes one checked indirect call, clears the sixteen party-slot pointers at
   `0x0209A210`, zeroes `0x02099DA6`, runs `0x002EA870(0)`, `0x002EA690` and `0x003DD220(1)`, then runs the
   stamping loops below and `0x00314010`, `0x00314DF0(-1)` and `0x00358BC0`;
3. it clears `+0x13`, fills `+0x40` with payload + payload `+0x38` when still 0, runs
   `0x0026D3E0(slot, payload)`, sets `+0x10` bit 0 and runs `0x00263660` on slot 3;
4. it recomputes `0x02099DB4` as the sum of slots 0, 1 and 2's `+0x1E0` counters (each under its own
   `+0x10` bit 0) and runs `0x002572E0(slot)` when both `+0xD8` and `+0xE0` are set (it fills the
   camera driver block's per-row effect handles from the camera-shot rows' `+0x20` words through
   `0x00257AD0`);
5. it runs the resource pass `0x003DB1F0(slot)` and, on slot 0, ends with `0x00253A30`, `0x002EA650` and
   `0x00233CF0`.

The stamping loops of step 2 walk the slot's records and, through `0x003587C0(ordinal)`, store into
each record:

- the words `+0xC8`, `+0xD6`, `+0xE4` and `+0xDC`, read from four lists in the payload, zeroing the
  record's word `+0xF6` in every loop;
- in the `+0xDC` loop, `+0x1C` bit 10 set when the stamp is not negative (a stamp of `0xFFFF` is
  replaced by the payload word `+0x16` of a row with more than 10 entries) and cleared otherwise,
  `0x00268EA0` when `+0x0B` bit 3 is set, and `+0x1C` bit 2 cleared;
- in a last loop, `+0xF6` zeroed once more.

The pool is a count dword followed by the record pointers: `0x00358940(slot, ordinal)` returns
`[pool + 8 + ordinal * 8]` for an ordinal from 0 to count - 1 and null otherwise.

### The variable homes

The script interpreter receives the slot as its first argument and resolves script variables by
storage class through these pointers ([script variables](../Scripts-And-Script-Commands/script-variables.md)):

| Slot field offset | Points at | Accessors on slot 0 |
|---|---|---|
| `+0x40` | payload + payload `+0x38` | |
| `+0x48` | the persistent save payload: the `i16[256]` operand bank, then the script globals ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)) | `0x00264640(i)` reads and `0x0026ABA0(i, v)` writes entry `i < 0x100`; `0x00265270()` reads and `0x0026B730(v)` writes entry 0 |
| `+0x50` | payload + payload `+0x48` | |
| `+0x58` | `0x02099DF0`, 64 words | `0x00264D20(i)` reads and `0x0026ADC0(i, v)` writes entry `i < 0x40` |
| `+0x60` | `0x02099FF0`, 32 words: the group persistent bank the save carries | `0x00264800(i)` reads and `0x0026AD10(i, v)` writes entry `i < 0x20` |
| `+0x78` | payload + payload `+0x28`: the variable descriptor table | |
| `+0x98` | `0x00264E30`, the resolver | |

Every accessor requires slot 0's `+0x10` bit 0 and a non-null pointer, and returns 0 or does
nothing otherwise; a rejected write is indistinguishable from a successful one.

### The camera entry tables

`+0x110` and `+0x170` are two arrays of four 24-byte entries: side A at `+0x110` is bound against
the camera-shot table `[slot + 0xD8]` and side B at `+0x170` against the camera-shake table
`[slot + 0xF0]`. Each table is checked for a null pointer and the record index against its count at
`+0x04`; the entry index must be below 4.

| Operation | Side A | Side B |
|---|---|---|
| bind `(slot, record, clock, entry, lookup)` | `0x003DA400`: `+0x0C` = clock, `+0x0A` = record, `+0x00` = the table row's `+0x14` (16-byte rows), `+0x04` = max(lookup, 0), `+0x08` = 1, `+0x10` = 1.0, `+0x14` = 0, then `0x00257230(index, value, entry)` and the reverse lookup `+0x18[lookup]` = entry | `0x003DD230`: the same into `+0x17C`, `+0x17A`, `+0x170`, `+0x174` (a negative lookup is replaced by `0x005C5230()`, which returns 0), `+0x178` = 1, `+0x180` = 1.0, then `0x0037DCF0(index, value, entry)` and `+0x1C[lookup]` = entry |
| reset all | `0x003DA000(slot)`: lookups `+0x18`, `+0x1A` = -1, each entry's `+0x08` = 0 and `+0x0A` = -1; `0x003DA370` does the same on the current slot and tail-calls `0x00257830` | `0x003DCF60(slot)`: lookups `+0x1C`, `+0x1E` = -1 and the four entries likewise |
| clear one | `0x003DA4D0(slot, entry)`: `+0x08` = 0 | |
| republish | `0x003DA570(slot, entry)`: `+0x18[entry +0x04]` = entry | |
| set rate | `0x003DA2D0(slot, entry, rate)`: writes `+0x120 + entry * 0x18` with no bound or table test | `0x003DD1F0(slot, entry, rate)`: the same at `+0x180 + entry * 0x18` |

`0x00257230(index, value, entry)` initialises the camera driver block `0x02092830 + index * 0xBB0 + entry * 0x2E0`
(or `0x02096520` for a negative entry): its `+0x178` = the value's row `[0x02092810[index * 0x176] + 0x18 + value * 0x40]`
or 0, and its clocks and scales reset (`+0xFC` and `+0x10C` = 1.0). `0x0037DCF0(index, value, entry)`
writes into the `0x1E`-byte shake entry `0x02ADD980 + index * 0x7A + entry * 0x1E`: byte `+0x03`, dword
`+0x04`, bytes `+0x1B`-`+0x1E` and a dword at `+0x1F` are zeroed, so the last store runs into the next
entry's first bytes.

The binds are reached from the camera verbs: `camerastart` `0x7D` (`0x0034F2F0`) and
`camerashakestart` `0x1A2` (`0x003492F0`) pass clock 0, the record index masked to 24 bits, the entry
and a popped lookup; `camerastart` `0x7E` (`0x0034F930`) and `camerashakestart` `0x1A3` (`0x00349730`)
pass a lookup of -1, which side A clamps to 0 and side B replaces with `0x005C5230()` = 0. The lookup
subscript is not bounded above by either bind: a lookup of 110, the largest literal a shipped script
passes, stores the entry index at slot `+0xF4`, inside the pointer `+0xF0`.

`0x003DA500` exchanges the two halves of both reverse lookups of every live slot (`+0x18` with `+0x1A`,
`+0x1C` with `+0x1E`) and then sets `+0x1A` and `+0x1E` to -1. It runs from `0x002F1950`, the callback
the `crossfade` task (`0x002F1A90`, verb `0x016F`) stores at task `+0x08`, only for a crossfade
opened with mode bit 2 (task `+0x28`).

### The step-point bits

Each slot carries two 512-bit arrays, sixteen dwords each: the status bits at `+0x204` and the mark
bits at `+0x244`. Point `n` is clamped to 0-511 and lives in dword `n >> 5`, bit `n & 31`. The verbs
pass the calling actor's manager (record `+0x15`) as the slot:

| Verb | Id | Handler | Writes |
|---|---|---|---|
| `steppoint(n)` | `0x04EE` | `0x00342D80` | mark bit `n` set (`0x0026B790(slot, n, 1)`), after `0x005C5230(slot, n)` |
| `setsteppointmarkstatus(n, v)` | `0x04F3` | `0x00343570` | mark bit `n` = `v != 0` (`0x0026B790`) |
| `setsteppointstatus(n, v)` | `0x04EF` | `0x003431B0` | status bit `n` = `v != 0` (`0x0026B800`) |
| `setsteppointstatusall(v)` | `0x04F0` | `0x00343980` | all sixteen status dwords to all ones for a non-zero `v`, else 0 (`0x0026B870`) |

The bind zeroes the mark bits of the slot it binds and, on slot 0, the status bits of slots 0-3.

## Layouts

Struct ActorManagerSlot base=`0x02098E10` size=`0x288` count=5:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8*` | payload | the bound definition payload (`0x0026C8C0`) |
| `+0x008` | `u8*` | recordPool | count dword then record pointers (`0x0026CE60`, `0x00358940`) |
| `+0x010` | `u8` | flags | bit 0 live (`0x0026CE60` sets), bit 2 field initialised, bits 3-4 the slot-0 request steps, bit 5 hold, bit 7 field busy |
| `+0x011` | `u8` | flags2 | bit 0 copy of flags bit 7, bit 1 trigger, bit 2 suspended, bit 3 blocks the request path |
| `+0x012` | `u8` | drivePending | 1 at bind when the payload's i16 +`0x50` is not negative |
| `+0x013` | `u8` | requestFlag | 1 at bind, cleared by `0x0026CE60` (`0x002673F0`) |
| `+0x014` | `u8` | bindFlag | 1 at bind |
| `+0x015` | `u8` | notSlot3 | 1 unless the slot index is 3 |
| `+0x016` | `u8` | bindFlag2 | 1 at bind |
| `+0x017` | `u8` | flags3 | bit 2, bit 3 (`0x02099DA1`), bit 4 frozen pass, bit 5 set at bind, bit 7 set at bind on slot 0 |
| `+0x018` | `i16[2]` | lookupA | side A reverse lookup, -1 when unbound |
| `+0x01C` | `i16[2]` | lookupB | side B reverse lookup |
| `+0x020` | `i32` | recordCount | the sum of the payload's u16 table at +[`0x14`] |
| `+0x024` | `i32` | passCounter | zeroed at bind, incremented by the pass |
| `+0x028` | `i32` | slotIndex |  |
| `+0x030` | `i32` | bindCounter | zeroed at bind |
| `+0x038` | `i32` | passCounter2 | zeroed at bind, incremented by the pass |
| `+0x040` | `u8*` | fileHome | payload + payload +`0x38` (`0x0026CE60`) |
| `+0x048` | `u8*` | globalHome | the persistent save payload |
| `+0x050` | `u8*` | localBase | payload + payload +`0x48` |
| `+0x058` | `u8*` | scratch1 | `0x02099DF0` |
| `+0x060` | `u8*` | scratch2 | `0x02099FF0` |
| `+0x068` | `u8*` | section20 | payload + payload +`0x20` |
| `+0x070` | `u8*` | section24 | payload + payload +`0x24` |
| `+0x078` | `u8*` | descriptors | payload + payload +`0x28` |
| `+0x080` | `u8*` | section2C | payload + payload +`0x2C` |
| `+0x088` | `void*` | callback | the bind's third argument or `0x00267930` |
| `+0x098` | `void*` | resolver | `0x00264E30` |
| `+0x0D8` | `u8*` | cameraShotTable | side A's definition table (setter `0x0026CE00`) |
| `+0x0E0` | `u8*` | cameraSection | set by `0x0026CE20`; `0x0026CE60` runs `0x002572E0` when this and +`0xD8` are set |
| `+0x0F0` | `u8*` | cameraShakeTable side B's definition table (setter 0x0026D3A0) |  |
| `+0x100` | `u8*` | section100 | set by `0x0026CE40` |
| `+0x110` | `u8[96]` | entriesA | four 24-byte camera-shot drivers |
| `+0x170` | `u8[96]` | entriesB | four 24-byte camera-shake drivers |
| `+0x1E0` | `i32` | liveCounter | summed into `0x02099DB4` |
| `+0x200` | `u8` | rosterFlags | bit 0 set at bind, bit 1 the party roster pending (slot 0), bit 2 cleared at bind |
| `+0x201` | `u8` | stepRequest | the tick's sub-step gate (`0x00267310`) |
| `+0x204` | `u32[16]` | stepPointStatus | 512 status bits (`0x0026B800`, `0x0026B870`); zeroed by a slot-0 bind on slots 0-3 |
| `+0x244` | `u32[16]` | stepPointMarks | 512 mark bits (`0x0026B790`); zeroed at bind |

Struct ActorManagerSlotEntry size=`0x18`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | definitionValue | the table row's +`0x14` |
| `+0x04` | `i32` | lookupIndex | the reverse-lookup subscript, clamped non-negative on side A |
| `+0x08` | `u16` | bound | 1 at bind, 0 on reset and clear |
| `+0x0A` | `i16` | recordIndex | -1 when unbound |
| `+0x0C` | `f32` | clock |  |
| `+0x10` | `f32` | rate | 1.0 at bind, set by the rate setters |
| `+0x14` | `u8` | clockRunning | cleared by side A's bind only |

## Operations

- The four access tables beside this page (`actor-managers-accesses.tsv`, `actor-managers-rip-accesses.tsv`,
  `actor-managers-slot-accesses.tsv`, `actor-managers-entry-accesses.tsv`) list every reach into a
  slot through the bound-slot pointer, through a literal slot address, through the array route and
  into the entry arrays; every row's instruction was checked against the executable.
- The world tick runs the field pass per slot, reads `+0x201` to decide which slots get a further
  sub-step, and the pass reads `+0x10`, `+0x11`, `+0x12`, `+0x13`, `+0x17`, `+0x20` and `+0x200`
  ([field runtime](field-runtime.md)).

## Modding notes

- Script globals live behind slot 0's `+0x48`, which is the save payload: a value written there is
  saved with the game.
- The two scratch banks at `+0x58` and `+0x60` are shared by every slot; only the second one is in
  the save image (payload `+0xE040` and `+0x2E250` as the group persistent bank).
- A bind on slot 0 resets the field state and the camera and shake registrations; binding a scene
  payload to slots 1-4 leaves them alone.

## Related

- [Field runtime](field-runtime.md): the pass that drives a slot's records.
- [The actor record](actor-record.md): the pool's records.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the operand bank and the group persistent bank.
- [Script variables and their storage classes](../Scripts-And-Script-Commands/script-variables.md): how the homes are addressed.
