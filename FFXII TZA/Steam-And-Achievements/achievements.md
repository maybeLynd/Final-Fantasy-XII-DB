---
title: "Achievements: the achievement list, the counters and conditions that award each one, and how an award reaches Steam"
kind: "system"
category: "Steam and achievements"
addresses: "0x01DFE410, 0x00D10460, 0x00D10550, 0x00316A50, 0x00315E90, 0x003166F0, 0x00316760, 0x00316BF0, 0x003165C0, 0x00316930, 0x003162E0, 0x01EED070, 0x00316440, 0x003160C0, 0x003161A0, 0x00315420, 0x00309EC0, 0x008632B0, 0x0020CE60, 0x00352250, 0x0034C9A0, 0x0020CB50, 0x00906290, 0x003158B0, 0x022C2550, 0x00316810, 0x00572920, 0x003154B0, 0x00315390, 0x020927C0"
---

## What the player sees

The game has 41 Steam achievements. Most come from running totals the game keeps whether or not Steam is
present: attacks, magicks and technicks used, items stolen, foes defeated, steps, gil gained and spent,
loot sold, licence points and clan points. Others test collections (every magick, every technick, every
Bestiary entry, every map visited), ten rare foes, eight story scenes and two Trial Mode stages. The last,
Champion of Ivalice, comes when all the others are held.

Thirty of the achievements, all but the eight story scenes, the two Trial Mode stages and Champion of
Ivalice, are also kept in the save. The Clan Primer's Sky Pirate's Den shows one statue for each of those
thirty earned, and the clan rank counts them, so both work without Steam.

Most of the running totals are kept in the save, and each target (50 items stolen, 500 foes defeated and so on) comes
from the language's copy of `menuhandbook.bin`. Once a total has reached its target, the game sets that achievement's
bit in the save and passes the award to Steam; an award made before Steam has sent its stats is only marked in the
game.

## How it works

### The records

The achievement list is a static array of 41 records of `0x198` bytes at `0x01DFE410`. Each holds the
developer tag (`ACH_COUNT_KILL`), the English Steam title inline, and the achieved byte at `+0x190`. The
Steam manager (`0x0020CD30`) uses this array directly as its entry table; an award names an entry by its
index 0-40.

### Descriptors

Thirty achievements are tracked by descriptor index 0-29. The descriptor table `0x00D10460` (8 bytes each)
gives each a counter width (`kind`), the counter's offset in the save block, a test (`mode`) and a parameter.
The award table `0x00D10550` (one dword per index) gives the entry index the award goes to; descriptor 13,
for example, awards entry 19.

### Moving a counter: `0x00316A50(index, amount)`

The updater refuses an index of 30 or more. Then:

1. With `kind` 0 (no stored counter) it compares the amount itself. Mode 0 fires when the amount is at
   least the target, which is `0x003165C0(index)` or, when that returns 0, the descriptor's parameter (a signed
   compare, `0x00316AF8`-`0x00316B01`). Mode 1 fires only when the amount equals the parameter (`0x00316AA6`). Any
   other mode returns.
2. With `kind` 2 or 4, the only non-zero kinds in the table, it reads the counter (`0x003166F0`). Mode 0 adds the
   amount, `v + a`, saturating at `0x7FFF` (kind 2) or `0x7FFFFFFF` (kind 4) and clamping a negative sum to 0; any
   other non-zero kind would add with no bound (`0x00316BBB`). Mode 3 sets bit `amount - 0xE2` (`0x00316B73`). Mode 8
   returns. Any other mode keeps the value read and goes on to step 3 (`0x00316B71`).
   - For the counter `v` and the amount `a`, kind 2 gives `a >= 0x7FFF - v ? 0x7FFF : v + a < 0 ? 0 : v + a`
     (`0x00316B87`-`0x00316BA1`), and kind 4 the same with `0x7FFFFFFF` (`0x00316BA5`-`0x00316BB4`).
3. It calls the evaluator `0x00315E90(index)` and only then the store `0x00316BF0` (`0x00316BC1`, `0x00316BCC`).
   The evaluator therefore sees the value from before this update.

Firing sets bit `index` of the award bits at block `+0x3844` and calls `0x008632B0` with the award-table
entry. Kind 0 fires without testing that bit first, so every qualifying call sets the bit and calls
`0x008632B0` again (`0x00316ABD`-`0x00316AEA`, `0x00316B11`-`0x00316B47`).

### The evaluator: `0x00315E90(index)`

It refuses an index of 31 or more (`0x00315E93`) and returns when the award bit is already set (`0x00315EDF`).
Index 30 has no award bit to test or set (`0x00315EB0`, `0x00316045`); both callers give 0-29 (`0x00316A39`,
`0x00316BC1`), so it is never evaluated. A mode above 7 returns (`0x00315F06`). Otherwise it dispatches on
the mode through the eight-entry table at `0x00316098`:

| Mode | Test (award when true) |
|---|---|
| 0 | `0x00316760(index)` is at least `0x003165C0(index)`, or the parameter when that is 0 |
| 1, 4 | never; they return |
| 2 | the parameter is two `u16` values lo and hi; every encoded id in `[lo, hi)` answers non-zero to `0x00309EC0(id, 0)`, the owned bit (`0x002FD970`) |
| 3 | at least `0x003165C0(index)` of the counter's low 16 bits are set, or 16 when that is 0 |
| 5 | `0x003160C0()`: every map flagged in `menuhandbook.bin` has a revealed tile |
| 6 | `0x003161A0()`: every Bestiary entry is unlocked |
| 7 | the parameter (0-9) indexes the handbook's monster list; that monster's defeat count is above 0 |

A passing test sets bit `index` of block `+0x3844` (`0x00316061`-`0x00316069`) and calls `0x008632B0` with
award-table dword `index` (`0x00316078`); a failing test returns with nothing stored. Mode 0 compares signed
(`0x00315F3B`).

Mode 2 takes lo from the low 16 bits of the parameter and hi from the high 16 bits (`0x00315F46`-`0x00315F56`);
with `lo >= hi` it passes at once (`0x00315F5B`), and otherwise it stops at the first id that answers 0
(`0x00315F6D`). Mode 3 counts the set bits of `0x003166F0(index)` (`0x00315FA5`-`0x00315FCB`). Mode 7 returns when
the blob or a hop is missing (`0x0031600C`-`0x0031602D`) or when the signed parameter is not below the list
count at hop 3 `+2` (`0x00316035`); the monster is the `u16` at hop 3 `+4 + param × 2` (`0x00316037`).

`0x00316760` returns the stored counter, or works out the two counter-less values itself: index 5 is the step
total (`0x00254E80`, `0x002536D0`, capped at 99,999,999) and index 8 is the mean of level byte `+0xBA` over the
party records whose slot is 0-5 (`0x00282FA0`), or 0 when fewer than six qualify. Every other counter-less
index reads -1 and never passes.

`0x00282DD0(i)` returns party record `i`, `[0x0209AC30] + 0x408 + i × 0xC0`. The mean walks records 0-8 and
also skips a record whose `+0x60` word is negative or whose first byte has bit `0x2` set (`0x003167A2`);
the re-send's sampler for index 8 reads the records the same way (`0x00316382`).

### Map and Bestiary tests

`0x003160C0` reads the map count at blob `+0x0A` and the bitmap at `+0x0C`. For each flagged map n it
requires a non-zero popcount of the 32-byte exploration bitmap at block `+0x224 + 32n` (`0x00255120`); for
the current map it first tries the live bitmap (`0x00255060`).

It returns 0 without the blob (`0x003160D0`) and at the first flagged map that fails (`0x0031617A`), and 1 when
every flagged map passes (`0x0031616A`). The current map is `0x003779F0(m)`, with `m` from `0x00264790()`, or from
`0x003148F0()` when that returns 0 or less (`0x003160EA`-`0x003160FA`). The live test is
`0x00255060([0x003C4AD0()], 0x20)`; when it returns 0 or less, the saved bitmap still decides
(`0x0031613A`-`0x00316150`).

`0x003161A0` walks Bestiary ids below the section count (384). An id with a type-0 rule passes when the story
counter `0x00265270` reaches the rule's value; a type-1 rule tests another monster's defeat count; any other id
needs its own defeat count (`0x00315420`: save byte `+0x3404 + id`, minus 1) above 0.

It returns 0 without the blob or with a zero hop (`0x003161B0`-`0x003161CA`) and at the first id that fails
(`0x003162AE`), and 1 when every id passes, a section count of 0 included (`0x003162C5`). An id's rule is the
first of the `ruleCount` rules whose low 12 bits equal the id (`0x00316230`-`0x0031623B`), and its type is the
top 4 bits (`0x00316287`).

A rule of type 2 or more falls back to the id's own defeat count, as an id with no rule does (`0x00316291`).
The type-0 test is signed, `(i16)0x00265270() >= value` (`0x0031629E`-`0x003162A9`), and the type-1 test is
`0x00315420(value) > 0` (`0x00316293`). An id of `0x200` or more fails (`0x003161F0`).

### The sweep and the re-send

`0x00316930` runs at the end of each field frame (`0x0022AEE6`), before the clan rank count (`0x00316681`) and
from the handbook's arm 7 (`0x005775B2`). It does four things:

1. It calls `0x00283270(1)`, which rebuilds the party status records.
2. For each monster id below `0x200` (`0x00316A16`) in the handbook list with a short other than -1 in `0x01EED130`
   (`0x003169D4`), it sets the monster's
   defeat count to 1 when it is at most 0 (state byte `+0x3404 + id` 0 or 1, `0x003169E0`-`0x003169FA`; the byte is
   set to 2) and `0x00315DC0(short)` passes: that quest is cleared (`0x0046B1A0`)
   or its scenario byte reaches the handbook's value for it.
3. It evaluates descriptors 0-29 (`0x00316A36`-`0x00316A43`).
4. It tail-jumps `0x003162E0`.

`0x01EED130` holds `0xA7` at position 1 and `0xAA` at position 10; positions 0 and 2-9 are -1 and position 11 is 0.
The list search exits only past position 10 (`10 < index`), so two monsters qualify: `0xFB` (position 1)
with quest `0xA7` (handbook quest row (167, 100)), and `0x103` (position 10) with quest `0xAA` (row
(170, 70)). Nothing writes `0x01EED130`; its only readers are `0x00316958` and `0x00315DB0`.

`0x003162E0` keeps twelve samplers of 16 bytes at `0x01EED070` (`{id, -, last sample, step}`; ids 0-8, 11,
14, 17; step 100 for ids 5 and 17, else 1). When a counter has moved by at least its step (`value - last >= step`,
`0x003163D7`), and the last sample already met the target, and the Steam entry reads not achieved (`0x00863280`), it
calls `0x008632B0` again.

Each sampler's value is its stored counter, read at the descriptor's width (`0x0031634B`, `0x00316357`). A kind-0
id, or a counter that reads -1, takes the step total for id 5 (`0x003163C4`) and the mean level for id 8, or 0
when fewer than six records qualify (`0x00316378`-`0x003163BB`); any other id stays -1 (`0x00316369`). The target
is `0x003165C0(id)` with no parameter fallback (`0x003163E1`), so a zero target needs only `last >= 0`. The entry
is award-table dword `id` (`0x003163EA`). The value replaces the last sample only on the moved path (`0x00316408`).

`0x00316440` does the same for descriptor 13 (entry 19) before every kind-10 action is counted. It tests the
saved award bit of descriptor 13 (block `+0x3845` bit `0x20`) instead of a sample: when that bit is set and
`0x00863280(19)` returns 0, it tail-jumps `0x008632B0(19)` (`0x00316449`-`0x0031646D`); otherwise it returns.

### What feeds each counter

| Index | Caller | Amount |
|---|---|---|
| 0, 1, 2 | `0x00305640`, when the acting unit's `[+0x698]` byte `+5` is 0: row kind `+0x1E` 0, 1 or 2 (`0x00305744`-`0x003057A5`) | 1 |
| 13 | the same, row kind 10, after `0x00316440` | the row index (`0xE2`-`0xF1`) |
| 3 | `0x003112F0`, for each stolen item as it clears the item's bit (`0x00311475`) | 1 |
| 4 | `0x003171C0`, called by `0x00312280` for a defeated unit whose `[+0x698]` byte `+5` is 1 (`0x003171E7`) | 1 |
| 6, 7 | the gil setter `0x00254EE0`: 6 when gil rises, 7 when it falls (`0x00254EF8`-`0x00254F02`) | the change |
| 11 | `0x00312280`, for each member given licence points (`0x00312496`) | the points given |
| 14 | `0x0056D370`, a sale while the shop shows loot (`[+0xE4] & 0x3FC0 == 0x1C0`) | the quantity |
| 19 | `0x0056D370`, every purchase (`0x0056D4D2`) | the encoded id bought |
| 17 | `0x00317090` from `0x00312280` (`0x003125BC`), and `0x002E2380` for script verb `addclanpoint` | `(byte +0x1C2 - byte +0x88) x word [[+0xE78]] + word [[+0xE70]]` of the foe; the verb's argument |
| 18 | `0x0028F0C0`, the chain counter's display update (`0x0028F0E3`) | the chain count |

Indices 6, 7, 11, 14 and 19 reach `0x00316A50` directly, from `0x00254F02`, `0x00312496` and `0x0056D4D2`; the
sale of loot loads `cl` = `0xE` and jumps to the purchase's call (`0x0056D48F`-`0x0056D498`). The rest go
through the 5-byte jump `0x00253770`, from six sites: `0x0028F0E3`, `0x002E2387`, `0x003057A5`, `0x00311475`,
`0x003170D8` and `0x003171E7`.

### Script and scene awards

Script verb `0x5AD` (`unkCall_5ad`, handler `0x00352250`) pops an int and calls `0x008632B0` with it. Script
verb `0x11B` (`startscene`, handler `0x0034C9A0`) calls `0x00863240` → `0x0020CB50(manager, key1, key2)`: key 2
is the scene number, key 1 the event-script number registered for the calling slot (`0x0032F240`, filled by
`0x0032FCA0`). `0x0020CB50` looks the pair up in the seven 12-byte rows `{key1, key2, entry}` at `0x00906290` and
awards the entry. Row 6 also awards entries 31-37 (`0x0020CC11`-`0x0020CC87`).

The calling slot is the issuer's manager `[0x02099D70] + 0x28` (`0x0034C9B5`); `0x0032F240` gives -1 when that manager's
byte `0x022C6D18` is 0 (`0x0032F24A`, `0x0032F25C`), and -1 matches no row. `0x00863240` returns at once when no Steam
manager exists (`[0x01F83450]` null, `0x00863256`). The handler then tail-jumps to `0x0026B750(n)` (`0x0034C9CD`), the
scene start ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)).

`0x0020CB50` takes the first row whose `key1` and `key2` both match (`0x0020CB74`-`0x0020CB7C`); a pair that
matches no row returns with nothing done (`0x0020CB89`). It awards inline with the steps of `0x0020CE60` below:
an entry whose `+0x190` is set is skipped; otherwise `+0x190` becomes 1, `+0x194` is cleared, and slots
`+0x38` (with the tag at `+0x08`) and `+0x50` are called only when manager `+0x18` is set
(`0x0020CBBB`-`0x0020CC09`). Row 6's loop over entries 31-37 runs whether or not row 6's own entry was already
achieved (`0x0020CC0C`), and skips each achieved one (`0x0020CC2C`).

### From award to Steam

`0x008632B0(entry)` returns at once when no Steam manager exists (`[0x01F83450]` null). Otherwise
`0x0020CE60` returns when the entry's `+0x190` is set, sets it, clears `+0x194`, and when Steam's stats have
arrived (manager `+0x18`) calls user-stats slot `+0x38` with the tag and tail-jumps slot `+0x50`
(SetAchievement and StoreStats in the Steamworks interface order). Before that, the award is only marked
locally. The Steam stats receipt rewrites `+0x190` of entries 1-40 from Steam and awards entry 0 when the
other forty are achieved.

`0x0020CE60` returns 1 for an entry already achieved (`0x0020CEE2`), 0 when the stats have not arrived
(`0x0020CED6`), and otherwise the result of slot `+0x50` through its tail jump (`0x0020CED2`); the result of
slot `+0x38` is not used.

### Sky Pirate's Den

`0x00572920` lays out one statue for each descriptor 0-29 whose award bit is set (`0x00576E10` →
`0x003154B0(7, i)`), from the 32-byte records of `menuhandbook_order.bin`. A record whose first byte is
`0xFF` is drawn with the statue numbered `0x003165C0(record index)`; record 31's value 16 places it with
statue 16. The clan rank `0x00315390` counts the set award bits (`0x00316670`, which runs the sweep first) and
reads counter 17 as the clan points.

## Layouts

The achievement record, `0x01DFE410 + entry x 0x198`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u64` | id | descriptor index for entries 1-30; the entry's own index for 31-40; 0 for entry 0 |
| `+0x008` | `char*` | tag | ACH_ tag, the name passed to Steam |
| `+0x010` | `char[128]` | title | English Steam title; replaced by Steam's "name" on stats receipt |
| `+0x090` | `char[256]` | desc | empty in the image; Steam's "desc" on stats receipt |
| `+0x190` | `u8` |  | achieved set by an award, rewritten from Steam on stats receipt |
| `+0x194` | `u32` | - | cleared by an award |

The descriptor, `0x00D10460 + index x 8`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | kind | 0 no counter, 2 signed word, 4 signed dword (`0x00316A81`, `0x003166F0`) |
| `+0x01` | `u8` | offset | the counter's byte offset in block `+0x384C` |
| `+0x02` | `u8` | mode | test, see the evaluator |
| `+0x03` | `u8` | - | 0 in all 30 |
| `+0x04` | `i32` | param | target, exact value, u16 range pair or monster-list index |

The saved achievement state, block `[0x020927C0]` (`0x002536A0`), which the save carries at payload `+0x8000`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x3844` | `u32` | awarded | bit i = descriptor i awarded; only ever set |
| `+0x384C` | `i16[5]` |  | counters 0-4 |
| `+0x3856` | `i16` |  | counter 13 (a 16-bit set) |
| `+0x3858` | `i16` |  | counter 14 |
| `+0x385A` | `u16` | - | no descriptor points here |
| `+0x385C` | `i32` |  | counter 11 |
| `+0x3860` | `i32` |  | counter 6 |
| `+0x3864` | `i32` |  | counter 7 |
| `+0x3868` | `i32` |  | counter 17 (clan points) |

The `menuhandbook.bin` chain. Each hop adds the `u16` at the current position, starting at blob `+8`:

```python
+0x08 (hop 0)  u16 step, u16 mapCount, u8 bitmap[]            maps that mode 5 requires
hop 1          u16 step, u16 bestiaryCount, u16, u16 ruleCount, {u16 id|type<<12, u16 value}[]
hop 2          u16 step, u16 count, {u8 quest, u8 scenario}[]  # 0x00315DC0
hop 3          u16 step, u16 count, u16 monster[]              mode 7
hop 4          u16, u16, u32 mask, u32 value[popcount(mask)]  # 0x003165C0
```

`0x003165C0(i)` returns 0 for `i >= 32`, a missing blob or a zero hop, or a clear mask bit; otherwise the value
at the rank of bit `i` among the set bits. `0x003158B0` loads the file (kind 7, id `0xC8`) into `0x022C2550`.
`0x003158B0`, called from `0x00253937`, first frees a copy already loaded with `0x003697F0` and clears the pointer
(`0x003158C5`, `0x003158CA`), then stores the result of `0x00249180(arg, 7, 0xC8, 3, 0, 0)` there unchecked
(`0x003158F8`, `0x003158FD`).

The hops are summed in 32 bits: `0x003165C0` adds each step with `add eax, edx` and reads the next one with
`movzx eax, word ptr [rax]` (`0x003165DA`-`0x003165FC`), and `0x00315E90` mode 7, `0x00316930`, the Bestiary test
`0x003161A0` (`0x003161C6`, `0x0031620A`), the quest test `0x00315DC0` (`0x00315E03`, `0x00315E0C`) and the list lookup
`0x00315D50` that reads `0x01EED130` (`0x00315D68`-`0x00315D7A`) do the same.
The chain is therefore correct only while the loaded `menuhandbook.bin` (`[0x022C2550]`) sits below 4 GB.

## Shipped data

| Fact | Value |
|---|---|
| records | 41: `COUNT` 11, `SPECIAL` 11, `EVENT` 8, `MASTER` 4, `COMPLETE` 3, `TRIAL` 2, `CHAMPION` 1, `LEVEL` 1 |
| descriptors | 30: kind 2 ×7, kind 4 ×4, kind 0 ×19 |
| modes | 0: 13 (0-8, 11, 14, 17, 18); 1: index 19 (`0xD07F`); 2: 9, 10, 12; 3: 13; 5: 15; 6: 16; 7: 20-29 (0-9) |
| `menuhandbook.bin` copies | 9; 320 bytes (`ch`, `cn`, `in`, `kr`), 316 (`de`, `es`, `fr`, `it`), 312 (`us`) |
| copy read | `in`, or `ch` for three language settings: the kind-7 entry `0xC8` of every language's path array (`0x002DF9A0`) |
| targets in the copy read | 0: 300, 1: 200, 2: 100, 3: 50, 4: 500, 5: 50,000, 6: 100,000, 7: 1,000,000, 8: 50, 11: 48,000, 13: 8, 14: 1,000, 17: 500,000, 18: 50, 31: 16 |
| `us`, `de`, `es`, `fr`, `it` copies | the same targets without index 11 |
| monster list | 11 Bestiary entries: `0xF8` Trickster, `0xFB` Gilgamesh, `0xFD` Behemoth King, `0xF0` Fafnir, `0xFA` Carrot, `0xE6` Deathgaze, `0x104` Yiazmat, `0x121` Hell Wyrm, `0x10F` Ultima, the High Seraph, `0x111` Zodiark, Keeper of Precepts, `0x103` Shadowseer; no descriptor indexes the last, the sweep reaches it |
| maps | 369, of which 359 are flagged |
| Bestiary section | 384 ids, 15 rules in the copy read |
| action rows by kind (`battle_pack.bin`, all languages) | kind 0: row `0x96`; kind 1: 81; kind 2: 24 (`0x9E`-`0xB5`); kind 10: 16 (`0xE2`-`0xF1`) |
| verb `0x5AD` calls | per language: 39 and 40 once each in the 100 Trial Mode stage scripts `tri_*`; 33 once in `slm_a01` |

The full list, with what awards each entry:

| Entry | Tag | Title | Descriptor | Awarded when |
|---:|---|---|---:|---|
| 0 | `ACH_CHAMPION_IVALICE` | Champion of Ivalice | - | entries 1-40 achieved (Steam receipt) |
| 1 | `ACH_COUNT_FIGHT` | Assault Striker | 0 | 300 uses of row `0x96` |
| 2 | `ACH_COUNT_MAGIC` | Spellslinger | 1 | 200 kind-1 actions |
| 3 | `ACH_COUNT_TECH` | Premier Prestidigitator | 2 | 100 kind-2 actions |
| 4 | `ACH_COUNT_STEAL` | Master Thief | 3 | 50 items stolen |
| 5 | `ACH_COUNT_KILL` | Blood Dancer | 4 | 500 foes defeated |
| 6 | `ACH_COUNT_CHAIN` | The Unrelenting | 18 | a chain count of 50 |
| 7 | `ACH_COUNT_STEP` | Wayfarer | 5 | 50,000 steps |
| 8 | `ACH_COUNT_GET_GIL` | Plunderer | 6 | 100,000 gil gained |
| 9 | `ACH_COUNT_SCORE` | Record Breaker | 17 | 500,000 clan points |
| 10 | `ACH_COUNT_USE_GIL` | Spendthrift | 7 | 1,000,000 gil spent |
| 11 | `ACH_COUNT_SELL_EVITEM` | Privateer | 14 | 1,000 loot sold |
| 12 | `ACH_LEVEL_AVERAGE` | Exemplar | 8 | mean level 50 over six members |
| 13 | `ACH_MASTER_LICENSE` | Conqueror | 11 | 48,000 licence points given |
| 14 | `ACH_COMPLETE_MONSTER` | Scrivener | 16 | every Bestiary entry unlocked |
| 15 | `ACH_MASTER_MAGIC` | Runeweaver | 9 | all 81 magicks, `0x3000`-`0x3050`, owned (the descriptor's range `0x3000` to `0x3051`) |
| 16 | `ACH_MASTER_TECH` | Jack-of-All-Trades | 10 | all 24 technicks, `0x4000`-`0x4017`, owned (the descriptor's range `0x4000` to `0x4018`) |
| 17 | `ACH_SPECIAL_HORIDASHI` | Collector | 19 | bazaar good `0xD07F`, the Morbid Urn, bought |
| 18 | `ACH_COMPLETE_MAP` | Cartographer | 15 | every flagged map visited |
| 19 | `ACH_COMPLETE_YUGOU` | Mist Walker | 13 | 8 different kind-10 rows used |
| 20 | `ACH_SPECIAL_MONSTER06` | Eagle Eye | 25 | Deathgaze (Bestiary entry `0xE6`) defeated |
| 21 | `ACH_SPECIAL_MONSTER04` | Wyrmslayer | 23 | Fafnir (`0xF0`) defeated |
| 22 | `ACH_SPECIAL_MONSTER01` | Sharpshooter | 20 | Trickster (`0xF8`) defeated |
| 23 | `ACH_SPECIAL_MONSTER05` | Freshmaker | 24 | Carrot (`0xFA`) defeated |
| 24 | `ACH_SPECIAL_MONSTER02` | Master Swordsman | 21 | Gilgamesh (`0xFB`) defeated, or quest `0xA7` |
| 25 | `ACH_SPECIAL_MONSTER03` | Lord of the Kings | 22 | Behemoth King (`0xFD`) defeated |
| 26 | `ACH_SPECIAL_MONSTER07` | Hunter Extraordinaire | 26 | Yiazmat (`0x104`) defeated |
| 27 | `ACH_SPECIAL_MONSTER08` | Radiant Savior | 27 | Hell Wyrm (`0x121`) defeated |
| 28 | `ACH_SPECIAL_MONSTER09` | Fell Angel | 28 | Ultima, the High Seraph (`0x10F`) defeated |
| 29 | `ACH_SPECIAL_MONSTER10` | Zodiac Knight | 29 | Zodiark, Keeper of Precepts (`0x111`) defeated |
| 30 | `ACH_MASTER_SUMMON` | High Summoner | 12 | all of `0xC012`-`0xC01E` owned |
| 31 | `ACH_EVENT_FINISH_REX` | For the Homeland | - | scene 18 of event script 244 (`naf_b0401`) |
| 32 | `ACH_EVENT_FIRST_HUNT` | Galbana Bloom | - | scene 4 of event 724 (`dst_a0181`) |
| 33 | `ACH_EVENT_RETURN_RABANASTRE` | A Traitor Redeemed | - | verb `0x5AD` in `slm_a01` |
| 34 | `ACH_EVENT_SAVE_ASHE` | Fated Meeting | - | scene 5 of event 284 (`rsn_y0100`) |
| 35 | `ACH_EVENT_DEFEAT_VOSSLER` | The Mist Seethes | - | scene 0 of event 302 (`alc_z0200`) |
| 36 | `ACH_EVENT_DEFEAT_JUDGE_BERGAN` | Visions of the Dreamer | - | scene 1 of event 196 (`bul_a0201`) |
| 37 | `ACH_EVENT_DEFEAT_CID` | Reins of History | - | scene 1 of event 177 (`dor_b0101`) |
| 38 | `ACH_EVENT_DEFEAT_VAYNE` | Wings of My Own | - | scene 1 of event 151 (`bhm_d0101`), which also awards 31-37 |
| 39 | `ACH_TRIAL_MODE_50` | Judge Magister | - | verb `0x5AD` in the Trial Mode stage scripts |
| 40 | `ACH_TRIAL_MODE_100` | Imperator | - | verb `0x5AD` in the Trial Mode stage scripts |

The event-script names are the kind-8 path entries `key1 x 4`; each of the seven scripts contains a
`startscene` call with its row's scene number.

## Operations

| Function | Role |
|---|---|
| `0x00316A50(index, amount)` | update a counter or fire a counter-less descriptor |
| `0x00315E90(index)` | evaluate one descriptor and award it |
| `0x003166F0(index)` / `0x00316BF0(index, value)` | read / store a counter at its declared width: a sign-extended `i16` for kind 2 and an `i32` for kind 4 at `block + 0x384C + offset` (`0x0031673B`, `0x00316750`, `0x00316C30`, `0x00316C45`); for an index of 30 or more or any other kind the read gives -1 (`0x00316753`) and the store writes nothing (`0x00316C48`) |
| `0x00316760(index)` | counter value, with the step total and mean level for 5 and 8 |
| `0x003165C0(index)` | the handbook target |
| `0x00316930()` | sweep: rare-monster fix-up, evaluate 0-29, re-send |
| `0x008632B0(entry)` | award a Steam entry |
| `0x00316810()` | on load (`0x00584398`): reseed the samplers and pull a saturated counter one below its cap (`0x7FFE`, `0x7FFFFFFE`); each sampler's `+4` and last sample get `0x00316760(id)` (`0x00316850`, `0x00316853`), and a kind-2 value of `0x7FFF` or more or a kind-4 value of `0x7FFFFFFF` is stored back as `0x7FFE` or `0x7FFFFFFE`, with the last sample set to the same (`0x003168FC`, `0x003168FF`, `0x0031689D`, `0x003168A3`); `0x003162E0` never reads `+4` |

## State

| Address | What |
|---|---|
| block `+0x3844`, `+0x384C`-`+0x386B` | award bits and counters, saved ([save fields](../Saving-Loading-And-Settings/save-data-fields.md)) |
| `0x01DFE410` + `0x190` per entry | the Steam-side achieved bytes, not saved |
| `0x01EED070` | the twelve samplers, reseeded on load |
| `0x022C2550` | the loaded `menuhandbook.bin` |

The award bits are only set: the one other writer of `+0x3844`, `0x00315910` category 7, is reached only from
`0x00577699` with categories 0-4 (`0x00D23750`).

## Modding notes

- A counter target is the handbook copy the language reads (`in` or `ch`); editing the `us` copy changes
  nothing. A descriptor whose mask bit is clear falls back to its `param`, which is 0 for every counter.
- A counter award lands on the update after the one that crosses the target, or at the next sweep.
- An award made before Steam's stats arrive is marked locally and then overwritten by the receipt. The re-send
  sends entry 19 and the counter achievements of descriptors 0-8, 11, 14 and 17 again. Entry 6 (descriptor 18,
  chain count) has no sampler; as a kind-0 descriptor it fires again at the next chain count of 50 or more, and
  entry 17 at the next purchase of the urn.
- An evaluator award is not sent again: no sampler covers it, and the evaluator returns once its save bit is
  set. A scene or script award has no save bit and no sampler; it is sent again only if its scene or verb runs
  again, since `0x0020CB50` and `0x0020CE60` test only `+0x190`.
- Raising the descriptor `param` of a mode-7 entry to 10 makes it use the eleventh list monster `0x103`.
- `kind` and `offset` place the counter in the save block; overlapping offsets share bytes.

## Related

- [Steam integration](steam-integration.md): the award call and the stats receipt.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): the Sky Pirate's Den and the Bestiary rules.
- [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md): the other handbook files.
- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md): `addclanpoint`.
- [Script verb table](../Scripts-And-Script-Commands/verb-table.md): verbs `0x5AD` and `0x11B`.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the block that holds the award bits and counters.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Spawn encounter lifecycle: `0x003148F0` is called by `0x00233780`; those functions are documented on
  [enemy respawning](../Enemy-Spawning/enemy-respawning.md).
