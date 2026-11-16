---
title: "Actor managers: the five manager slots at 0x02098E10, their bind, their record pool, their variable homes and their camera entry tables"
kind: "system"
category: "Characters and objects"
addresses: "0x02098E10, 0x02099D70, 0x0026C8C0, 0x0026CE60, 0x00358940, 0x002679F0, 0x00264640, 0x0026ABA0, 0x0026B730, 0x00265270, 0x00264D20, 0x0026ADC0, 0x00264800, 0x0026AD10, 0x002640C0, 0x002640D0, 0x002673F0, 0x00267310, 0x003DA400, 0x003DA370, 0x003DA000, 0x003DA4D0, 0x003DA570, 0x003DA2D0, 0x003DD230, 0x003DCF60, 0x003DD1F0, 0x003DD320, 0x0026B790, 0x0026B800, 0x0026B870, 0x003DA500"
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
the bind, the pass and `0x0026CE60` store it there (`0x0026CE60` puts the old value back before it returns:
`0x0026CE6D`, `0x0026CE8D`, `0x0026D383`; the bind does the same at `0x0026CDC0`), `0x002640C0` returns it and
`0x002640D0` returns that slot's index
`+0x28`. Three one-byte getters take a slot index: `0x002673F0` returns `+0x13`, `0x00267310` returns
`+0x201`, and the field pass reads `+0x10`.

Slot 0's `flags3` byte `+0x17` is `0x02098E27`. `0x0025D5D0` clears its bit `0x80`; seven functions call it (`0x00342828`,
`0x00343804`, `0x00343C96`, `0x0034442F`, `0x00345BDA`, `0x00346D08`, `0x00347AA2`), among them `0x00342770`, the begin of the verb
`musicplay` ([music](../Sound-And-Music/music.md)). `0x002628B0` (`0x00262E60`), `0x00266D10` (`0x0026701D`), `0x0026A2A0` (`0x0026A2C9`)
and `0x0026C8C0` (`0x0026CCD7`) test its bit `0x8`, the first two then slot 1's at `0x020990AF` (`0x00262E72`, `0x00267036`).

`0x00265680` (`0x002656AE`) and `0x002672B0` (`0x002672B5`) walk the five slots' `+0x17` from `0x02098E27` in steps of `0x288`
until `0x02099ACF`, and answer 1 only when every slot whose `+0x10` has bit `0x1` holds both bits `0x1` and `0x2` there
(`0x002656CB`, `0x002672CF`).

### The bind

`0x0026C8C0(slot, payload, callback)` binds a loaded definition payload to a slot (its stack frame
holds the slot pointer in `0x02099D70` for the duration):

1. it stores the slot pointer in `0x02099D70`, zeroes the eight qwords `+0x244`-`+0x27C`, clears `+0x200` bit
   `0x4`, and writes the slot index to `+0x28` and the payload pointer to `+0x00` (`0x0026C911`-`0x0026C95A`);
2. on slot 0 (`0x0026C95D`-`0x0026C95F`) it also runs `0x00238B00(0)`, zeroes `+0x204`-`+0x243` of slots 0-3 and
   runs `0x002EF350(1, -1)`; then, for each of `0x02099DD0` (kind `0xD`) and `0x02099DD8` (kind `0xE`) that is set,
   it runs `0x00369760(kind)`, `0x0036D160(kind)` and `0x003697F0(pointer)` and stores 0 in the pointer
   (`0x0026C965`-`0x0026CA17`);
3. on slot 0, with `v` the answer of `0x0032F240(0)`: `0x0025A990()` when
   `0x00377440(v)` is non-zero and `0x0025AA30()` when `0x00377480(v)` is 0, then `0x003ACA90(8)`, `0x00360110()`,
   `0x002E24B0()`, `0x00408AD0()` by the thunk `0x003EC850()`, `0x0036E3B0()`, `0x0026FFA0(1)`, `0x002700C0(1)`,
   `0x002EC590(1)`, `0x002EC5A0(1)`, clears `0x02099DE8[0..7]` and `0x0209A2A0[0..7]`, and `0x0042ED30()` by
   the thunk `0x002E8050()` (`0x0026C9B5`-`0x0026C9C3`, `0x0026CA1E`-`0x0026CAC0`);
4. between the slot-0 extras and the pointer block it calls the `ret` stub `0x0016D6A0(index)`
   (`0x0026CACC`), which does nothing;
5. it fills the pointer block: `+0x88` = the callback or `0x00267930` when no callback was given, `+0x98` = 0
   and `+0x40` = 0, and only then `+0x48` = the persistent save payload (`0x002EF2B0()`), `+0x50` = payload +
   its dword `+0x48` zero-extended, `+0x58` = `0x02099DF0`, `+0x60` = `0x02099FF0`, and last `+0x98` = `0x00264E30`
   (`0x0026CAE6`-`0x0026CB76`);
6. it sets `+0x68`, `+0x70`, `+0x78` and `+0x80` = payload + its dwords `+0x20`, `+0x24`, `+0x28` and
   `+0x2C`, each sign-extended (`0x0026CB3C`-`0x0026CB6B`); it zeroes `+0x1F0` and `+0x1F8` before `0x002EF2B0`
   (`0x0026CAD9`-`0x0026CAE0`) and `+0x1E0` after it (`0x0026CB1F`);
7. it sums the `u16` entries of the payload's table at payload + its dword `+0x14`, sign-extended (a count
   followed by the entries, added in pairs with the odd tail) into `+0x20`, the record count
   (`0x0026CB7D`-`0x0026CBD9`);
8. it resets the flag bytes: `+0x10` = `0x82` (bits `0x2` and `0x80` only), `+0x11` = `(old & 0xF8) | 1`
   (bit `0x1` set, bits `0x2` and `0x4` cleared, so a bind un-suspends the slot; `0x0026CAD1`,
   `0x0026CBE0`-`0x0026CBF6`), `+0x13` and `+0x14` = 1 (`0x0026CC6C`), `+0x15` = (slot index is not 3)
   (`0x0026CBF9`-`0x0026CC0D`), `+0x16` = 1 (`0x0026CCD3`), `+0x17` = `0x23`, or `0xA3` on slot 0;
9. it sets `+0x12` = (the payload's `i16 +0x50` is not negative) (`0x0026CD1A`-`0x0026CD28`) and `+0x200` bit
   `0x1` (`0x0026CBC7`), sets `+0x200` bit `0x2` on slot 0 and clears it on the others (`0x0026CD2B`-`0x0026CD38`),
   and zeroes `+0x201`, `+0x30` and `+0x38` (`0x0026CC38`-`0x0026CC42`) and `+0x24` (`0x0026CD59`);
10. it zeroes `+0xA0`-`+0xB8`, `+0xC8`-`+0x100`, `+0x108`, `+0x1E8` and `+0x1FC` (`0x0026CBE6`-`0x0026CC65`) and
   `+0x1D0` (`0x0026CD52`), and runs `0x00263660()` and `0x003DDC20(index, 0)` (`0x0026CC72`-`0x0026CC7C`); on slot 3 it
   then calls `0x0026D6F0(actor, [0x01DFE0BC] × 0.0, 2)` when `0x003588B0(0x003590D0())` finds the focus actor, and
   `0x00359200(1, 3)` in either case (`0x0026CC81`-`0x0026CCBA`);
11. `0x02099DA1` becomes 1 when any slot's `+0x17` bit `0x8` is set and 0 otherwise (`0x0026CCC3`-`0x0026CD1F`);
   on slot 0 (`0x0026CD5C`-`0x0026CD5E`) the field state is reset: `0x0026DB30()`, `0x002EBDB0(0)`, `0x002ECB70(0)`,
   `0x0209A2C4[1..3]` = 1, then `0x002EDA80(0x002EDA60())`, `0x002EDA70(0x002EDA50())`, `0x002E83A0(0x002EDA40())` and
   `0x002EBC30(0x002EDA30())`, each setter taking the float the call before it returned (`0x0026CD60`-`0x0026CDB9`);
12. `0x02099D70` gets its old value back and `0x003DD790(index)` ends the bind (`0x0026CDBE`-`0x0026CDE3`).

Each of the two clear loops of step 3 carries a bounds test that leads to `0x00809728()` for an index of 8 or
more (`0x0026CA87`-`0x0026CA8B`, `0x0026CAA5`-`0x0026CAA9`, `0x0026CDE8`, `0x0026CDEE`); the loops count from 0 to 7, so
it is not taken.

Step 8 gives what the bind leaves. On `+0x17` its own instructions are `| 3` (`0x0026CAD5`), `& 0xE7`
(`0x0026CBD2`), `& 0xFB` and `| 0x20` (`0x0026CCBF`, `0x0026CCC5`), which keep bits `0x40` and `0x80` of the old
byte. `0x003DDC20(index, 0)` of step 10 clears bit `0x40` in the slot's `+0x17` (`0x003DDC2D`) before the bind
reads the byte back (`0x0026CCCF`) and stores it with bit `0x80` set on slot 0 and clear on the others
(`0x0026CD43`-`0x0026CD4F`).

On `+0x10` the stores are: anded with `0xE7` (`0x0026CB0B`), stored with bit `0x1` clear (`0x0026CB67`), stored
again with `0x82` or-ed in (`0x0026CC45`), and anded with `0x9B` (`0x0026CD3F`). The calls of step 10 come
between the last two: `+0x10` is `(old & 0x64) | 0x82` and `+0x17` is `(old & 0xE4) | 3` when `0x00263660` is
entered. Also stored only after those calls: bits `0x4`, `0x20` and `0x80` of `+0x17`, `+0x16`, `0x02099DA1`,
`+0x12`, bit `0x2` of `+0x200`, `+0x1D0` and `+0x24`.

Within `0x002EF2B0`, `0x00263660`, `0x003DDC20`, `0x003DD6C0`, `0x003590D0`, `0x003588B0`, `0x0026D6F0`, `0x00359200` and
`0x003DD790` themselves, the store at `0x003DDC2D` and the one after it (`0x003DDC39`, which ors in nothing for a
second argument of 0) are the only ones to a slot's `+0x10`, `+0x11` or `+0x17`.

### The record pool

`0x0026CE60(slot)` runs after the bind for a slot whose `+0x10` bit `0x1` is clear and `+0x13` is set:

1. it allocates the record pool with `0x002679F0(slot pointer)` and stores it at `+0x08`. The pool's
   records are the subject of [the actor record](actor-record.md). It then runs
   `0x00266C50(slot pointer)`, `0x002342F0()` on slot 0, and
   `0x00265A20(slot pointer)` ([battle units](battle-units.md)) (`0x0026CEA8`-`0x0026CECE`);
2. on slot 0 (`0x0026CED5`-`0x0026CED8`) it calls the `ret` stub `0x0016D6A0()` (`0x0026CEE8`), clears the sixteen
   map-jump group pointers at `0x0209A210`, zeroes `0x02099DA6`, runs `0x002EA870(0)`, `0x002EA690()` and
   `0x003DD220(1)` (`0x0026CEED`-`0x0026CF3E`), then runs the stamping loops below and `0x00314010()`, `0x00314DF0(-1)`
   and `0x00358BC0()` through the thunk `0x00358BB0()` (`0x0026D2C2`-`0x0026D2CF`);
3. if `+0x13` is still set (`0x0026D2D9`-`0x0026D2DD`), it clears it, fills `+0x40` with payload + its dword
   `+0x38`, zero-extended, when still 0, runs `0x0026D3E0(slot pointer, payload)`, sets `+0x10` bit `0x1` and
   runs `0x00263660()` on slot 3 (`0x0026D2E3`-`0x0026D30F`); otherwise it goes straight to the slot-0 ending of
   step 5, past steps 3 and 4 and `0x003DB1F0`;
4. it recomputes `0x02099DB4` as the sum of slots 0, 1 and 2's `+0x1E0` counters (each under its own
   `+0x10` bit `0x1`) and runs `0x002572E0(index)` when both `+0xD8` and `+0xE0` are set (it fills the
   camera driver block's per-row effect handles from the camera-shot rows' `+0x20` words through
   `0x00257AD0`) (`0x0026D314`-`0x0026D35D`);
5. after step 4 it runs the resource pass `0x003DB1F0(index)` (`0x0026D362`-`0x0026D365`); then, on slot 0, it
   ends with `0x00253A30()`, `0x002EA650()` and `0x00233CF0()` (`0x0026D36A`-`0x0026D37E`) on both paths.

The entry test of `+0x10` and `+0x13` is `0x0026CE94`-`0x0026CEA2`. The clear loop of step 2 limits its index
to 0-15 (`0x0026CF00`-`0x0026CF0F`); it counts 0 to 15 (`0x0026CF11`-`0x0026CF1A`), so the limit changes nothing.

The stamping loops of step 2 walk the slot's records: each of the five takes its record from
`0x00358940(slot pointer, i)` for `i` from 0 while `i` is below the slot's `+0x20`, a signed compare made on
every pass, and stores 0 in the answer's word `+0xF6` with no null test (`0x0026CF45`-`0x0026CFD3`, `0x0026CFE0`-`0x0026D07C`,
`0x0026D089`-`0x0026D146`, `0x0026D154`-`0x0026D263`, `0x0026D284`-`0x0026D2C0`).

Each loop's word goes into the record `0x003587C0(s, w)`
returns: `w` is the walked record's word `+0`, passed whole, and `s` the slot's `+0x28`, or `w >> 16`, which
is 0, when `w` has bit `0x4000`. `0x0026CE60` stores through the answer with no null test
(`0x0026CFA4`-`0x0026CFC7`, `0x0026D04D`-`0x0026D070`, `0x0026D117`-`0x0026D13A`, `0x0026D1DA`-`0x0026D1FC`). Every other
store and test below is on the walked record:

- the words `+0xC8`, `+0xD6`, `+0xE4` and `+0xDC`, read from four lists in the payload, zeroing the
  record's word `+0xF6` in every loop; each loop stores its word only when the payload is
  present with word `+0` above 3, its list is not empty, the stamp is not negative and bit
  `0x8000` is clear in the record's word `+0` (`0x0026CF6D`-`0x0026CFC7`, `0x0026D00B`-`0x0026D070`,
  `0x0026D0B1`-`0x0026D13A`, `0x0026D18C`-`0x0026D1FC`);
- in the `+0xDC` loop, `+0x1C` bit `0x400` set unless the record's word `+0xDC` is `0xFFFF` and the
  row has 10 entries or fewer or its word `+0x16` is negative (`0x0026D203`-`0x0026D238`); when the
  bit is set it then runs `0x00268EA0(record)` when `+0x0B` bit `0x8` is set, and clears `+0x1C` bit `0x4`
  (`0x0026D23A`-`0x0026D24F`); otherwise only bit `0x400` is cleared (`0x0026D255`);
- in a last loop, `+0xF6` zeroed once more; it makes the same call, `0x0020E600(that dword)`, for a payload that
  is present and whose word `+0x00` is above 3, and uses nothing of the answer (`0x0026D29A`-`0x0026D2B6`).

Each stamp comes from the walked record's directory: payload + the low 32 bits of `0x0020E600(dword +0x18 of
the record's +0x40 object)`, a run of lists, each a signed count word followed by that many words. The
stamp is the first word of the list reached by stepping over one list for `+0xC8`, two for `+0xD6`, five
for `+0xE4` and three for `+0xDC`, and it is taken only when that list's count is above 0
(`0x0026CF78`-`0x0026CF96`, `0x0026D016`-`0x0026D03F`, `0x0026D0BC`-`0x0026D109`, `0x0026D197`-`0x0026D1CC`).

The `+0xDC` loop's row test decodes the directory again, `0x0020E600(the same dword +0x18)`
(`0x0026D210`-`0x0026D21A`), without
the payload tests the stamps carry.

The pool is a count dword followed by the record pointers: `0x00358940(slot, ordinal)` returns
`[pool + 8 + ordinal * 8]` for an ordinal from 0 to count - 1 and null otherwise.

For manager 0 that pointer, the slot's `+0x08`, is the qword at `0x02098E18`. It holds what `0x002679F0(slot)`
answered, stored by `0x0026CE60` (`0x0026CEB0`-`0x0026CEB8`): the count and the pointer table, not an array of
records.

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

Every accessor requires slot 0's `+0x10` bit `0x1` and a non-null pointer, and returns 0 or does
nothing otherwise; a rejected write is indistinguishable from a successful one.

### The camera entry tables

`+0x110` and `+0x170` are two arrays of four 24-byte entries: side A at `+0x110`, the four shot channels of the [scripted camera](../Graphics/scripted-camera.md), is bound against
the camera-shot table `[slot + 0xD8]` and side B at `+0x170` against the camera-shake table
`[slot + 0xF0]`. Each table is checked for a null pointer and the record index against its count at
`+0x04`; the entry index must be below 4.

| Operation | Side A | Side B |
|---|---|---|
| bind `(slot, record, clock, entry, lookup)` | `0x003DA400`: `+0x0C` = clock, `+0x0A` = record, `+0x00` = the table row's `+0x14` (16-byte rows), `+0x04` = max(lookup, 0), `+0x08` = 1, `+0x10` = 1.0, `+0x14` = 0, then `0x00257230(index, value, entry)` and the reverse lookup `+0x18[lookup]` = entry | `0x003DD230`: the same into `+0x17C`, `+0x17A`, `+0x170`, `+0x174` (a negative lookup is replaced by `0x005C5230()`, which returns 0), `+0x178` = 1, `+0x180` = 1.0, then `0x0037DCF0(index, value, entry)` and `+0x1C[lookup]` = entry |
| reset all | `0x003DA000(slot)`: lookups `+0x18`, `+0x1A` = -1, each entry's `+0x08` = 0 and `+0x0A` = -1; `0x003DA370` does the same on the current slot `0x002640C0()`, with no null test, and tail-calls `0x00257830` with its own first argument, a float in `xmm0`, and its second to fourth arguments unchanged (`0x003DA38F`-`0x003DA3F8`) | `0x003DCF60(slot)`: lookups `+0x1C`, `+0x1E` = -1 and the four entries likewise |
| clear one | `0x003DA4D0(slot, entry)`: word `+0x08` = 0 (`+0x118 + 0x18 x entry`, `0x003DA4E8`), only for an entry of at most 3 and a non-null `+0xD8` (`0x003DA4D0`-`0x003DA4DD`); `camerastop` `0x0053` and `camerastop_54` `0x0054` call it (`0x00350696`, `0x0035030C`) | `0x003DD320(slot, entry)`: word `+0x178 + 0x18 x entry` = 0, only for an entry of at most 3 and a non-null `+0xF0` (`0x003DD320`-`0x003DD338`); `camerashakestop` `0x019D` and `camerashakestop_19e` `0x019E` call it (`0x0034A3A6`, `0x00349EFC`) |
| republish | `0x003DA570(slot, entry)`: `+0x18[entry +0x04]` = entry | |
| set rate | `0x003DA2D0(slot, entry, rate)`: writes `+0x120 + entry * 0x18` with no bound or table test | `0x003DD1F0(slot, entry, rate)`: the same at `+0x180 + entry * 0x18` |

The `camerastop` handler `0x00350660` calls `0x00267F90(context, 0)`, takes the slot from `0x002640C0()`, calls
`0x00267E10(context)` and jumps to `0x003DA4D0(slot, what 0x00267E10 returned)`; the context is its fourth
argument (`0x0035066A`-`0x00350696`).

`0x00257230(index, value, entry)` initialises the camera driver block `0x02092830 + index * 0xBB0 + entry * 0x2E0`
(or `0x02096520` for a negative entry): its `+0x178` = the value's row `[0x02092810[index * 0x176] + 0x18 + value * 0x40]`
or 0, and its clocks and scales reset (`+0xFC` and `+0x10C` = 1.0).

`0x0037DCF0(index, value, entry)` zeroes fields of the `0xF0`-byte shake entry
`0x02ADD990 + index * 0x3D0 + entry * 0xF0` ([camera shake](../EBP-Script-Files/ebp-camera-shake.md)):
the qword `+0x08`, the dword `+0x10`, the 32 bytes `+0xC8`-`+0xE7` and the state dword `+0xE8`
(`0x0037DD10`-`0x0037DD38`). Every store is inside the entry.

The binds are reached from the camera verbs: `camerastart` `0x7D` (`0x0034F2F0`) and
`camerashakestart` `0x1A2` (`0x003492F0`) pass clock 0, the record index masked to 24 bits, the entry
and a popped lookup; `camerastart` `0x7E` (`0x0034F930`) and `camerashakestart` `0x1A3` (`0x00349730`)
pass a lookup of -1, which side A clamps to 0 and side B replaces with `0x005C5230()` = 0. The lookup
subscript is not bounded above by either bind: a lookup of 110, the largest literal a shipped script
passes, stores the entry index at slot `+0xF4`, inside the pointer `+0xF0`.

`0x003DA500` exchanges the two halves of both reverse lookups of every live slot (`+0x18` with `+0x1A`,
`+0x1C` with `+0x1E`) and then sets `+0x1A` and `+0x1E` to -1. It runs from `0x002F1950`, the callback
the `crossfade` task (`0x002F1A90`, verb `0x016F`) stores at task `+0x08`, only for a crossfade
opened with mode bit `0x4` (task `+0x28`).

### The step-point bits

Each slot carries two 512-bit arrays, sixteen dwords each: the status bits at `+0x204` and the mark
bits at `+0x244`. Point `n` is clamped to 0-511 and lives in dword `n >> 5`, under the bit value
`1 << (n & 31)` (`0x0026B7A7`-`0x0026B7D4`, `0x0026B817`-`0x0026B844`). `0x0026B790`, `0x0026B800` and `0x0026B870` take the
slot as `0x02098E10 + slot × 0x288` with no bound or live test (`0x0026B796`-`0x0026B7A4`, `0x0026B806`-`0x0026B814`,
`0x0026B87D`-`0x0026B891`). The verbs
pass the calling actor's manager (record `+0x15`) as the slot:

| Verb | Id | Handler | Writes |
|---|---|---|---|
| `steppoint(n)` | `0x04EE` | `0x00342D80` | point `n`'s mark bit set (`0x0026B790(slot, n, 1)`), after `0x005C5230(slot, n)` |
| `setsteppointmarkstatus(n, v)` | `0x04F3` | `0x00343570` | point `n`'s mark bit = `v != 0` (`0x0026B790`: set for a non-zero `v`, cleared for 0, `0x0026B7D9`-`0x0026B7E9`) |
| `setsteppointstatus(n, v)` | `0x04EF` | `0x003431B0` | point `n`'s status bit = `v != 0` (`0x0026B800`, the same at `+0x204`, `0x0026B849`-`0x0026B859`) |
| `setsteppointstatusall(v)` | `0x04F0` | `0x00343980` | all sixteen status dwords to all ones for a non-zero `v`, else 0 (`0x0026B870`) |

The bind zeroes the mark bits of the slot it binds and, on slot 0, the status bits of slots 0-3.

## Layouts

Struct ActorManagerSlot base=`0x02098E10` size=`0x288` count=5:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8*` | payload | the bound definition payload (`0x0026C8C0`) |
| `+0x008` | `u8*` | recordPool | count dword then record pointers (`0x0026CE60`, `0x00358940`) |
| `+0x010` | `u8` | flags | bit `0x1` live (`0x0026CE60` sets), bit `0x4` field initialised, mask `0x18` the slot-0 request steps, bit `0x20` hold, bit `0x80` field busy |
| `+0x011` | `u8` | flags2 | bit `0x1` copy of flags bit `0x80`, bit `0x2` trigger, bit `0x4` suspended, bit `0x8` blocks the request path |
| `+0x012` | `u8` | drivePending | 1 at bind when the payload's i16 `+0x50` is not negative |
| `+0x013` | `u8` | requestFlag | 1 at bind, cleared by `0x0026CE60` (`0x002673F0`) |
| `+0x014` | `u8` | bindFlag | 1 at bind |
| `+0x015` | `u8` | notSlot3 | 1 unless the slot index is 3 |
| `+0x016` | `u8` | bindFlag2 | 1 at bind |
| `+0x017` | `u8` | flags3 | bit `0x4`, bit `0x8` (`0x02099DA1`), bit `0x10` frozen pass, bit `0x20` set at bind, bit `0x80` set at bind on slot 0 |
| `+0x018` | `i16[2]` | lookupA | side A reverse lookup, -1 when unbound |
| `+0x01C` | `i16[2]` | lookupB | side B reverse lookup |
| `+0x020` | `i32` | recordCount | the sum of the payload's u16 table at +[`0x14`] |
| `+0x024` | `i32` | passCounter | zeroed at bind, incremented by the pass |
| `+0x028` | `i32` | slotIndex |  |
| `+0x030` | `i32` | bindCounter | zeroed at bind |
| `+0x038` | `i32` | passCounter2 | zeroed at bind, incremented by the pass |
| `+0x040` | `u8*` | fileHome | payload + payload `+0x38` (`0x0026CE60`) |
| `+0x048` | `u8*` | globalHome | the persistent save payload |
| `+0x050` | `u8*` | localBase | payload + payload `+0x48` |
| `+0x058` | `u8*` | scratch1 | `0x02099DF0` |
| `+0x060` | `u8*` | scratch2 | `0x02099FF0` |
| `+0x068` | `u8*` | section20 | payload + payload `+0x20` |
| `+0x070` | `u8*` | section24 | payload + payload `+0x24` |
| `+0x078` | `u8*` | descriptors | payload + payload `+0x28` |
| `+0x080` | `u8*` | section2C | payload + payload `+0x2C` |
| `+0x088` | `void*` | callback | the bind's third argument or `0x00267930` |
| `+0x098` | `void*` | resolver | `0x00264E30` |
| `+0x0D8` | `u8*` | cameraShotTable | side A's definition table (setter `0x0026CE00`) |
| `+0x0E0` | `u8*` | cameraSection | set by `0x0026CE20`; `0x0026CE60` runs `0x002572E0` when this and `+0xD8` are set |
| `+0x0F0` | `u8*` | cameraShakeTable | side B's definition table (setter `0x0026D3A0`) |
| `+0x100` | `u8*` | section100 | set by `0x0026CE40` |
| `+0x110` | `u8[96]` | entriesA | four 24-byte camera-shot drivers |
| `+0x170` | `u8[96]` | entriesB | four 24-byte camera-shake drivers |
| `+0x1E0` | `i32` | liveCounter | summed into `0x02099DB4` |
| `+0x200` | `u8` | rosterFlags | bit `0x1` set at bind, bit `0x2` the party roster pending (slot 0), bit `0x4` cleared at bind |
| `+0x201` | `u8` | stepRequest | the tick's sub-step gate (`0x00267310`) |
| `+0x204` | `u32[16]` | stepPointStatus | 512 status bits (`0x0026B800`, `0x0026B870`); zeroed by a slot-0 bind on slots 0-3 |
| `+0x244` | `u32[16]` | stepPointMarks | 512 mark bits (`0x0026B790`); zeroed at bind |

Struct ActorManagerSlotEntry size=`0x18`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | definitionValue | the table row's `+0x14` |
| `+0x04` | `i32` | lookupIndex | the reverse-lookup subscript, clamped non-negative on side A |
| `+0x08` | `u16` | bound | 1 at bind, 0 on reset and clear |
| `+0x0A` | `i16` | recordIndex | -1 when unbound |
| `+0x0C` | `f32` | clock |  |
| `+0x10` | `f32` | rate | 1.0 at bind, set by the rate setters |
| `+0x14` | `u8` | clockRunning | cleared by side A's bind only |

## Operations

- Four access tables beside this page list every reach into a slot, each row with the instruction at its address
  in the executable:
  - [`actor-managers-accesses.tsv`](actor-managers-accesses.tsv): through the bound-slot pointer. A row whose
    `route` is `seed` is in a function that took the slot itself, from `0x002640C0` or by reading `0x02099D70`, or in
    the script interpreter `0x0025E4C0`, which receives the slot as its first argument; a row whose `route` is
    `argN+0xK<F@S` is in a function the slot was passed to;
  - [`actor-managers-rip-accesses.tsv`](actor-managers-rip-accesses.tsv): through a literal slot address;
  - [`actor-managers-slot-accesses.tsv`](actor-managers-slot-accesses.tsv): through the array route;
  - [`actor-managers-entry-accesses.tsv`](actor-managers-entry-accesses.tsv): into the entry arrays.
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
- [`actor-definition-payload-accesses.tsv`](actor-definition-payload-accesses.tsv): the accesses of the bind
  `0x0026C8C0` to the definition payload it receives in `rdx`, one row per instruction (7 rows).

In this access table, `function`, `name` and `site` give the function, its name and the instruction's address,
`disp` the offset in the payload, `kind` a read (`r`) or the address taken (`addr`), `instruction` the instruction
itself, and `route` how the payload reached it: in `rdx` at the entry of `0x0026C8C0`, which keeps it in `r15`
(`0x0026C8F7`) and stores it to the slot's `+0x00` (`0x0026C95A`).

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Gameplay: `0x003590D0` is called by `0x0031ADB0`; those functions are documented on
  [bestiary](../Enemy-Spawning/bestiary.md).
