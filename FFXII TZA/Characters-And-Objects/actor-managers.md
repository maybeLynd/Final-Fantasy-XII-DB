---
title: "Actor managers: the five manager slots at 02098E10, their bind, their record pool, their variable homes and their camera entry tables"
kind: "system"
category: "Characters and objects"
addresses: "02098E10, 02099D70, 0026C8C0, 0026CE60, 00358940, 002679F0, 00264640, 0026ABA0, 0026B730, 00265270, 00264D20, 0026ADC0, 00264800, 0026AD10, 002640C0, 002640D0, 002673F0, 00267310, 003DA400, 003DA370, 003DA000, 003DA4D0, 003DA570, 003DA2D0, 003DD230, 003DCF60, 003DD1F0, 0026B790, 0026B800, 0026B870, 003DA500"
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

A manager slot is a `288`<sub>h</sub>-byte block; five of them sit at `02098E10`, so slot `n` is
`02098E10 + n * 288h` and the array ends at `02099AB7`. `02099D70` holds the slot being worked on:
the bind and the pass store it there, `002640C0` returns it and `002640D0` returns that slot's index
`+28`<sub>h</sub>. Three one-byte getters take a slot index: `002673F0` returns `+13`<sub>h</sub>, `00267310` returns
`+201`<sub>h</sub>, and the field pass reads `+10`<sub>h</sub>.

### The bind

`0026C8C0(slot, payload, callback)` binds a loaded definition payload to a slot (its stack frame
holds the slot pointer in `02099D70` for the duration):

1. it zeroes the eight qwords `+244`<sub>h</sub>-`+27C`<sub>h</sub>, clears `+200`<sub>h</sub> bit 2, writes the slot index to
   `+28`<sub>h</sub> and the payload pointer to `+00`<sub>h</sub>;
2. on slot 0 it also runs `00238B00`, zeroes `+204`<sub>h</sub>-`+243`<sub>h</sub> of slots 0-3, runs `002EF350(1)` and
   releases the two kind `D`<sub>h</sub> and `E`<sub>h</sub> registrations at `02099DD0` and `02099DD8` (`00369760`,
   `0036D160`, `003697F0`);
3. still on slot 0: `0025A990` when `00377440(field)` is non-zero and `0025AA30` when
   `00377480(field)` is 0, then `003ACA90(8)`, `00360110`, `002E24B0`, `00408AD0`, `0036E3B0`,
   `0026FFA0(1)`, `002700C0(1)`, `002EC590(1)`, `002EC5A0(1)`, the clears of `02099DE8[0..7]` and
   `0209A2A0[0..7]`, and `0042ED30`;
4. between the slot-0 extras and the pointer block it makes one indirect call through a checked
   function pointer with the slot index as its argument;
5. it fills the pointer block: `+88`<sub>h</sub> = the callback or `00267930` when none was given, `+48`<sub>h</sub> =
   the persistent save payload (`002EF2B0()`), `+50`<sub>h</sub> = payload + payload `+48`<sub>h</sub>, `+58`<sub>h</sub> =
   `02099DF0`, `+60`<sub>h</sub> = `02099FF0`, `+98`<sub>h</sub> = `00264E30`;
6. it sets `+68`<sub>h</sub>, `+70`<sub>h</sub>, `+78`<sub>h</sub> and `+80`<sub>h</sub> = payload + its dwords `+20`<sub>h</sub>, `+24`<sub>h</sub>, `+28`<sub>h</sub> and
   `+2C`<sub>h</sub>, and zeroes `+40`<sub>h</sub>, `+1E0`<sub>h</sub>, `+1F0`<sub>h</sub> and `+1F8`<sub>h</sub>;
7. it sums the `u16` entries of the payload's table at payload `+[14h]` (a count followed by the
   entries, added in pairs with the odd tail) into `+20`<sub>h</sub>, the record count;
8. it resets the flag bytes: `+10`<sub>h</sub> = `82`<sub>h</sub> (bits 1 and 7 only), `+11`<sub>h</sub> = `(old & F8h) | 1` (bit 0
   set, bits 1 and 2 cleared, so a bind un-suspends the slot), `+13`<sub>h</sub> and `+14`<sub>h</sub> = 1, `+15`<sub>h</sub> =
   (slot index is not 3), `+16`<sub>h</sub> = 1, `+17`<sub>h</sub> = `(old & 40h) | 23h` with bit 7 set only on slot 0;
9. it sets `+12`<sub>h</sub> = (the payload's `i16 +50h` is not negative), `+200`<sub>h</sub> bit 0, and bit 1 on slot 0
   (cleared elsewhere), and zeroes `+201`<sub>h</sub>, `+24`<sub>h</sub>, `+30`<sub>h</sub> and `+38`<sub>h</sub>;
10. it zeroes `+A0`<sub>h</sub>-`+B8`<sub>h</sub>, `+C8`<sub>h</sub>-`+F8`<sub>h</sub>, `+100`<sub>h</sub>, `+108`<sub>h</sub>, `+1D0`<sub>h</sub>, `+1E8`<sub>h</sub> and `+1FC`<sub>h</sub>,
   runs `00263660` and `003DDC20(index, 0)`, and on slot 3 `00359200(1)` after a `0026D6F0` on the
   focus actor;
11. `02099DA1` becomes 1 when any slot's `+17`<sub>h</sub> bit 3 is set; on slot 0 the field state is reset
   (`0026DB30`, `002EBDB0(0)`, `002ECB70(0)`, `0209A2C4[1..3]` = 1, `002EDA60`, `002EDA80`, `002EDA50`,
   `002EDA70`, `002EDA40`, `002E83A0`, `002EDA30`, `002EBC30`); `003DD790(index)` ends the bind.

### The record pool

`0026CE60(slot)` runs after the bind for a slot whose `+10`<sub>h</sub> bit 0 is clear and `+13`<sub>h</sub> is set:

1. it allocates the record pool with `002679F0(slot)` and stores it at `+08`<sub>h</sub>
   ([the actor record](actor-record.md)), then runs `00266C50`,
   `002342F0` on slot 0, and `00265A20` ([battle units](battle-units.md));
2. on slot 0 it makes one checked indirect call, clears the sixteen party-slot pointers at
   `0209A210`, zeroes `02099DA6`, runs `002EA870(0)`, `002EA690` and `003DD220(1)`, then runs the
   stamping loops below and `00314010`, `00314DF0(-1)` and `00358BC0`;
3. it clears `+13`<sub>h</sub>, fills `+40`<sub>h</sub> with payload + payload `+38`<sub>h</sub> when still 0, runs
   `0026D3E0(slot, payload)`, sets `+10`<sub>h</sub> bit 0 and runs `00263660` on slot 3;
4. it recomputes `02099DB4` as the sum of slots 0, 1 and 2's `+1E0`<sub>h</sub> counters (each under its own
   `+10`<sub>h</sub> bit 0) and runs `002572E0(slot)` when both `+D8`<sub>h</sub> and `+E0`<sub>h</sub> are set (it fills the
   camera driver block's per-row effect handles from the camera-shot rows' `+20`<sub>h</sub> words through
   `00257AD0`);
5. it runs the resource pass `003DB1F0(slot)` and, on slot 0, ends with `00253A30`, `002EA650` and
   `00233CF0`.

The stamping loops of step 2 walk the slot's records and, through `003587C0(ordinal)`, store into
each record:

- the words `+C8`<sub>h</sub>, `+D6`<sub>h</sub>, `+E4`<sub>h</sub> and `+DC`<sub>h</sub>, read from four lists in the payload, zeroing the
  record's word `+F6`<sub>h</sub> in every loop;
- in the `+DC`<sub>h</sub> loop, `+1C`<sub>h</sub> bit 10 set when the stamp is not negative (a stamp of `FFFF`<sub>h</sub> is
  replaced by the payload word `+16`<sub>h</sub> of a row with more than 10 entries) and cleared otherwise,
  `00268EA0` when `+0B`<sub>h</sub> bit 3 is set, and `+1C`<sub>h</sub> bit 2 cleared;
- in a last loop, `+F6`<sub>h</sub> zeroed once more.

The pool is a count dword followed by the record pointers: `00358940(slot, ordinal)` returns
`[pool + 8 + ordinal * 8]` for an ordinal from 0 to count - 1 and null otherwise.

### The variable homes

The script interpreter receives the slot as its first argument and resolves script variables by
storage class through these pointers ([script variables](../Scripts-And-Script-Commands/script-variables.md)):

| Slot field offset | Points at | Accessors on slot 0 |
|---|---|---|
| `40`<sub>h</sub> | payload + payload `+38`<sub>h</sub> | |
| `48`<sub>h</sub> | the persistent save payload: the `i16[256]` operand bank, then the script globals ([save data fields](../Saving-Loading-And-Settings/save-data-fields.md)) | `00264640(i)` reads and `0026ABA0(i, v)` writes entry `i < 100h`; `00265270()` reads and `0026B730(v)` writes entry 0 |
| `50`<sub>h</sub> | payload + payload `+48`<sub>h</sub> | |
| `58`<sub>h</sub> | `02099DF0`, 64 words | `00264D20(i)` reads and `0026ADC0(i, v)` writes entry `i < 40h` |
| `60`<sub>h</sub> | `02099FF0`, 32 words: the group persistent bank the save carries | `00264800(i)` reads and `0026AD10(i, v)` writes entry `i < 20h` |
| `78`<sub>h</sub> | payload + payload `+28`<sub>h</sub>: the variable descriptor table | |
| `98`<sub>h</sub> | `00264E30`, the resolver | |

Every accessor requires slot 0's `+10`<sub>h</sub> bit 0 and a non-null pointer, and returns 0 or does
nothing otherwise; a rejected write is indistinguishable from a successful one.

### The camera entry tables

`+110`<sub>h</sub> and `+170`<sub>h</sub> are two arrays of four 24-byte entries: side A at `+110`<sub>h</sub> is bound against
the camera-shot table `[slot + D8h]` and side B at `+170`<sub>h</sub> against the camera-shake table
`[slot + F0h]`. Each table is checked for a null pointer and the record index against its count at
`+04`<sub>h</sub>; the entry index must be below 4.

| Operation | Side A | Side B |
|---|---|---|
| bind `(slot, record, clock, entry, lookup)` | `003DA400`: `+0C`<sub>h</sub> = clock, `+0A`<sub>h</sub> = record, `+00`<sub>h</sub> = the table row's `+14`<sub>h</sub> (16-byte rows), `+04`<sub>h</sub> = max(lookup, 0), `+08`<sub>h</sub> = 1, `+10`<sub>h</sub> = 1.0, `+14`<sub>h</sub> = 0, then `00257230(index, value, entry)` and the reverse lookup `+18h[lookup]` = entry | `003DD230`: the same into `+17C`<sub>h</sub>, `+17A`<sub>h</sub>, `+170`<sub>h</sub>, `+174`<sub>h</sub> (a negative lookup is replaced by `005C5230()`, which returns 0), `+178`<sub>h</sub> = 1, `+180`<sub>h</sub> = 1.0, then `0037DCF0(index, value, entry)` and `+1Ch[lookup]` = entry |
| reset all | `003DA000(slot)`: lookups `+18`<sub>h</sub>, `+1A`<sub>h</sub> = -1, each entry's `+08`<sub>h</sub> = 0 and `+0A`<sub>h</sub> = -1; `003DA370` does the same on the current slot and tail-calls `00257830` | `003DCF60(slot)`: lookups `+1C`<sub>h</sub>, `+1E`<sub>h</sub> = -1 and the four entries likewise |
| clear one | `003DA4D0(slot, entry)`: `+08`<sub>h</sub> = 0 | |
| republish | `003DA570(slot, entry)`: `+18h[entry +04h]` = entry | |
| set rate | `003DA2D0(slot, entry, rate)`: writes `+120h + entry * 18h` with no bound or table test | `003DD1F0(slot, entry, rate)`: the same at `+180h + entry * 18h` |

`00257230(index, value, entry)` initialises the camera driver block `02092830 + index * BB0h + entry * 2E0h`
(or `02096520` for a negative entry): its `+178`<sub>h</sub> = the value's row `[02092810[index * 176h] + 18h + value * 40h]`
or 0, and its clocks and scales reset (`+FC`<sub>h</sub> and `+10C`<sub>h</sub> = 1.0). `0037DCF0(index, value, entry)`
writes into the `1E`<sub>h</sub>-byte shake entry `02ADD980 + index * 7Ah + entry * 1Eh`: byte `+03`<sub>h</sub>, dword
`+04`<sub>h</sub>, bytes `+1B`<sub>h</sub>-`+1E`<sub>h</sub> and a dword at `+1F`<sub>h</sub> are zeroed, so the last store runs into the next
entry's first bytes.

The binds are reached from the camera verbs: `camerastart` `7D`<sub>h</sub> (`0034F2F0`) and
`camerashakestart` `1A2`<sub>h</sub> (`003492F0`) pass clock 0, the record index masked to 24 bits, the entry
and a popped lookup; `camerastart` `7E`<sub>h</sub> (`0034F930`) and `camerashakestart` `1A3`<sub>h</sub> (`00349730`)
pass a lookup of -1, which side A clamps to 0 and side B replaces with `005C5230()` = 0. The lookup
subscript is not bounded above by either bind: a lookup of 110, the largest literal a shipped script
passes, stores the entry index at slot `+F4`<sub>h</sub>, inside the pointer `+F0`<sub>h</sub>.

`003DA500` exchanges the two halves of both reverse lookups of every live slot (`+18`<sub>h</sub> with `+1A`<sub>h</sub>,
`+1C`<sub>h</sub> with `+1E`<sub>h</sub>) and then sets `+1A`<sub>h</sub> and `+1E`<sub>h</sub> to -1. It runs from `002F1950`, the callback
the `crossfade` task (`002F1A90`, verb `016F`<sub>h</sub>) stores at task `+08`<sub>h</sub>, only for a crossfade
opened with mode bit 2 (task `+28`<sub>h</sub>).

### The step-point bits

Each slot carries two 512-bit arrays, sixteen dwords each: the status bits at `+204`<sub>h</sub> and the mark
bits at `+244`<sub>h</sub>. Point `n` is clamped to 0-511 and lives in dword `n >> 5`, bit `n & 31`. The verbs
pass the calling actor's manager (record `+15`<sub>h</sub>) as the slot:

| Verb | Id | Handler | Writes |
|---|---|---|---|
| `steppoint(n)` | `04EE`<sub>h</sub> | `00342D80` | mark bit `n` set (`0026B790(slot, n, 1)`), after `005C5230(slot, n)` |
| `setsteppointmarkstatus(n, v)` | `04F3`<sub>h</sub> | `00343570` | mark bit `n` = `v != 0` (`0026B790`) |
| `setsteppointstatus(n, v)` | `04EF`<sub>h</sub> | `003431B0` | status bit `n` = `v != 0` (`0026B800`) |
| `setsteppointstatusall(v)` | `04F0`<sub>h</sub> | `00343980` | all sixteen status dwords to all ones for a non-zero `v`, else 0 (`0026B870`) |

The bind zeroes the mark bits of the slot it binds and, on slot 0, the status bits of slots 0-3.

## Layouts

Struct ActorManagerSlot base=`02098E10` size=`288`<sub>h</sub> count=5:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u8*` | payload | the bound definition payload (`0026C8C0`) |
| `008`<sub>h</sub> | `u8*` | recordPool | count dword then record pointers (`0026CE60`, `00358940`) |
| `010`<sub>h</sub> | `u8` | flags | bit 0 live (`0026CE60` sets), bit 2 field initialised, bits 3-4 the slot-0 request steps, bit 5 hold, bit 7 field busy |
| `011`<sub>h</sub> | `u8` | flags2 | bit 0 copy of flags bit 7, bit 1 trigger, bit 2 suspended, bit 3 blocks the request path |
| `012`<sub>h</sub> | `u8` | drivePending | 1 at bind when the payload's i16 +`50`<sub>h</sub> is not negative |
| `013`<sub>h</sub> | `u8` | requestFlag | 1 at bind, cleared by `0026CE60` (`002673F0`) |
| `014`<sub>h</sub> | `u8` | bindFlag | 1 at bind |
| `015`<sub>h</sub> | `u8` | notSlot3 | 1 unless the slot index is 3 |
| `016`<sub>h</sub> | `u8` | bindFlag2 | 1 at bind |
| `017`<sub>h</sub> | `u8` | flags3 | bit 2, bit 3 (`02099DA1`), bit 4 frozen pass, bit 5 set at bind, bit 7 set at bind on slot 0 |
| `018`<sub>h</sub> | `i16[2]` | lookupA | side A reverse lookup, -1 when unbound |
| `01C`<sub>h</sub> | `i16[2]` | lookupB | side B reverse lookup |
| `020`<sub>h</sub> | `i32` | recordCount | the sum of the payload's u16 table at +[`14`<sub>h</sub>] |
| `024`<sub>h</sub> | `i32` | passCounter | zeroed at bind, incremented by the pass |
| `028`<sub>h</sub> | `i32` | slotIndex |  |
| `030`<sub>h</sub> | `i32` | bindCounter | zeroed at bind |
| `038`<sub>h</sub> | `i32` | passCounter2 | zeroed at bind, incremented by the pass |
| `040`<sub>h</sub> | `u8*` | fileHome | payload + payload +`38`<sub>h</sub> (`0026CE60`) |
| `048`<sub>h</sub> | `u8*` | globalHome | the persistent save payload |
| `050`<sub>h</sub> | `u8*` | localBase | payload + payload +`48`<sub>h</sub> |
| `058`<sub>h</sub> | `u8*` | scratch1 | `02099DF0` |
| `060`<sub>h</sub> | `u8*` | scratch2 | `02099FF0` |
| `068`<sub>h</sub> | `u8*` | section20 | payload + payload +`20`<sub>h</sub> |
| `070`<sub>h</sub> | `u8*` | section24 | payload + payload +`24`<sub>h</sub> |
| `078`<sub>h</sub> | `u8*` | descriptors | payload + payload +`28`<sub>h</sub> |
| `080`<sub>h</sub> | `u8*` | section2C | payload + payload +`2C`<sub>h</sub> |
| `088`<sub>h</sub> | `void*` | callback | the bind's third argument or `00267930` |
| `098`<sub>h</sub> | `void*` | resolver | `00264E30` |
| `0D8`<sub>h</sub> | `u8*` | cameraShotTable | side A's definition table (setter `0026CE00`) |
| `0E0`<sub>h</sub> | `u8*` | cameraSection | set by `0026CE20`; `0026CE60` runs `002572E0` when this and +`D8`<sub>h</sub> are set |
| `0F0`<sub>h</sub> | `u8*` | cameraShakeTable side B's definition table (setter 0026D3A0) |  |
| `100`<sub>h</sub> | `u8*` | section100 | set by `0026CE40` |
| `110`<sub>h</sub> | `u8[96]` | entriesA | four 24-byte camera-shot drivers |
| `170`<sub>h</sub> | `u8[96]` | entriesB | four 24-byte camera-shake drivers |
| `1E0`<sub>h</sub> | `i32` | liveCounter | summed into `02099DB4` |
| `200`<sub>h</sub> | `u8` | rosterFlags | bit 0 set at bind, bit 1 the party roster pending (slot 0), bit 2 cleared at bind |
| `201`<sub>h</sub> | `u8` | stepRequest | the tick's sub-step gate (`00267310`) |
| `204`<sub>h</sub> | `u32[16]` | stepPointStatus | 512 status bits (`0026B800`, `0026B870`); zeroed by a slot-0 bind on slots 0-3 |
| `244`<sub>h</sub> | `u32[16]` | stepPointMarks | 512 mark bits (`0026B790`); zeroed at bind |

Struct ActorManagerSlotEntry size=`18`<sub>h</sub>:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | definitionValue | the table row's +`14`<sub>h</sub> |
| `04`<sub>h</sub> | `i32` | lookupIndex | the reverse-lookup subscript, clamped non-negative on side A |
| `08`<sub>h</sub> | `u16` | bound | 1 at bind, 0 on reset and clear |
| `0A`<sub>h</sub> | `i16` | recordIndex | -1 when unbound |
| `0C`<sub>h</sub> | `f32` | clock |  |
| `10`<sub>h</sub> | `f32` | rate | 1.0 at bind, set by the rate setters |
| `14`<sub>h</sub> | `u8` | clockRunning | cleared by side A's bind only |

## Operations

- The four access tables beside this page (`actor-managers-accesses.tsv`, `actor-managers-rip-accesses.tsv`,
  `actor-managers-slot-accesses.tsv`, `actor-managers-entry-accesses.tsv`) list every reach into a
  slot through the bound-slot pointer, through a literal slot address, through the array route and
  into the entry arrays; every row's instruction was checked against the executable.
- The world tick runs the field pass per slot, reads `+201`<sub>h</sub> to decide which slots get a further
  sub-step, and the pass reads `+10`<sub>h</sub>, `+11`<sub>h</sub>, `+12`<sub>h</sub>, `+13`<sub>h</sub>, `+17`<sub>h</sub>, `+20`<sub>h</sub> and `+200`<sub>h</sub>
  ([field runtime](field-runtime.md)).

## Modding notes

- Script globals live behind slot 0's `+48`<sub>h</sub>, which is the save payload: a value written there is
  saved with the game.
- The two scratch banks at `+58`<sub>h</sub> and `+60`<sub>h</sub> are shared by every slot; only the second one is in
  the save image (payload `+E040`<sub>h</sub> and `+2E250`<sub>h</sub> as the group persistent bank).
- A bind on slot 0 resets the field state and the camera and shake registrations; binding a scene
  payload to slots 1-4 leaves them alone.

## Related

- [Field runtime](field-runtime.md): the pass that drives a slot's records.
- [The actor record](actor-record.md): the pool's records.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the operand bank and the group persistent bank.
- [Script variables and their storage classes](../Scripts-And-Script-Commands/script-variables.md): how the homes are addressed.
