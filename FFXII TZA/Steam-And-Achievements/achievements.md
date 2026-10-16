---
title: "Achievements: the achievement list, the counters and conditions that award each one, and how an award reaches Steam"
kind: "system"
category: "Steam and achievements"
summary: "The 41 achievement records with their developer tags and Steam titles, the 30 descriptors that give each tracked achievement a counter or a test, the saved counter block and award bits, the menuhandbook.bin targets and lists the tests read, the code that feeds every counter, the periodic sweep and its re-send, the script and scene awards, the path from an award to SetAchievement and StoreStats, and the Sky Pirate's Den statues that show the awards."
addresses: "01DFE410, 00D10460, 00D10550, 00316A50, 00315E90, 003166F0, 00316760, 00316BF0, 003165C0, 00316930, 003162E0, 01EED070, 00316440, 003160C0, 003161A0, 00315420, 00309EC0, 008632B0, 0020CE60, 00352250, 0034C9A0, 0020CB50, 00906290, 003158B0, 022C2550, 00316810, 00572920, 003154B0, 00315390, 020927C0"
---

## What the player sees

The game has 41 Steam achievements. Most come from running totals the game keeps whether or not Steam is
present: attacks, magicks and technicks used, items stolen, foes defeated, steps, gil gained and spent,
loot sold, licence points and clan points. Others test collections (every magick, every technick, every
Bestiary entry, every map visited), ten rare foes, eight story scenes and two Trial Mode stages. The last,
Champion of Ivalice, comes when all the others are held.

The thirty tracked achievements are also kept in the save. The Clan Primer's Sky Pirate's Den shows one
statue for each one earned, and the clan rank counts them, so both work without Steam.

## How it works

### The records

The achievement list is a static array of 41 records of `0x198` bytes at `01DFE410`. Each holds the
developer tag (`ACH_COUNT_KILL`), the English Steam title inline, and the achieved byte at `+0x190`. The
Steam manager (`0020CD30`) uses this array directly as its entry table; an award names an entry by its
index 0-40.

### Descriptors

Thirty achievements are tracked by descriptor index 0-29. The descriptor table `00D10460` (8 bytes each)
gives each a counter width (`kind`), the counter's offset in the save block, a test (`mode`) and a parameter.
The award table `00D10550` (one dword per index) gives the entry index the award goes to; descriptor 13,
for example, awards entry 19.

### Moving a counter: `00316A50(index, amount)`

The updater refuses an index of 30 or more. Then:

1. With `kind` 0 (no stored counter) it compares the amount itself. Mode 0 fires when the amount is at
   least the target, which is `003165C0(index)` or, when that returns 0, the descriptor's parameter (a signed
   compare, `00316AF8`-`00316B01`). Mode 1 fires only when the amount equals the parameter (`00316AA6`). Any
   other mode returns.
2. With `kind` 2 or 4 it reads the counter (`003166F0`). Mode 0 adds the amount, saturating at `0x7FFF`
   (kind 2) or `0x7FFFFFFF` (kind 4) and clamping a negative sum to 0. Mode 3 sets bit `amount - 0xE2`
   (`00316B73`). Mode 8 returns.
3. It calls the evaluator `00315E90(index)` and only then the store `00316BF0` (`00316BC1`, `00316BCC`).
   The evaluator therefore sees the value from before this update.

Firing sets bit `index` of the award bits at block `+0x3844` and calls `008632B0` with the award-table
entry.

### The evaluator: `00315E90(index)`

It refuses an index of 31 or more and returns when the award bit is already set. Otherwise it dispatches on
the mode through the eight-entry table at `00316098`:

| Mode | Test (award when true) |
|---|---|
| 0 | `00316760(index)` is at least `003165C0(index)`, or the parameter when that is 0 |
| 1, 4 | never; they return |
| 2 | the parameter is two `u16` values lo and hi; every encoded id in `[lo, hi)` answers non-zero to `00309EC0(id, 0)`, the owned bit (`002FD970`) |
| 3 | at least `003165C0(index)` of the counter's low 16 bits are set, or 16 when that is 0 |
| 5 | `003160C0()`: every map flagged in `menuhandbook.bin` has a revealed tile |
| 6 | `003161A0()`: every Bestiary entry is unlocked |
| 7 | the parameter (0-9) indexes the handbook's monster list; that monster's defeat count is above 0 |

`00316760` returns the stored counter, or works out the two counter-less values itself: index 5 is the step
total (`00254E80`, `002536D0`, capped at 99,999,999) and index 8 is the mean of level byte `+0xBA` over the
party records whose slot is 0-5 (`00282FA0`), or 0 when fewer than six qualify. Every other counter-less
index reads -1 and never passes.

`00282DD0(i)` returns party record `i`, `[0209AC30] + 0x408 + i × 0xC0`. The mean walks records 0-8 and
also skips a record whose `+0x60` word is negative or whose first byte has bit `0x2` set (`003167A2`);
the re-send's sampler for index 8 reads the records the same way (`00316382`).

### Map and Bestiary tests

`003160C0` reads the map count at blob `+0x0A` and the bitmap at `+0x0C`. For each flagged map n it
requires a non-zero popcount of the 32-byte exploration bitmap at block `+0x224 + 32n` (`00255120`); for
the current map it first tries the live bitmap (`00255060`).

`003161A0` walks Bestiary ids below the section count (384). An id with a type-0 rule passes when the story
counter `00265270` reaches the rule's value; a type-1 rule tests another monster's defeat count; any other id
needs its own defeat count (`00315420`: save byte `+0x3404 + id`, minus 1) above 0.

### The sweep and the re-send

`00316930` runs at the end of each field frame (`0022AEE6`), before the clan rank count (`00316681`) and
from the handbook's arm 7 (`005775B2`). It does four things:

1. It calls `00283270(1)`, which rebuilds the party status records.
2. For each monster in the handbook list with a non-negative short in `01EED130`, it sets the monster's
   defeat count to 1 when it is still 0 and `00315DC0(short)` passes: that quest is cleared (`0046B1A0`)
   or its scenario byte reaches the handbook's value for it.
3. It evaluates descriptors 0-29 (`00316A36`-`00316A43`).
4. It tail-jumps `003162E0`.

`01EED130` holds `0xA7` at position 1 and `0xAA` at position 10; positions 0 and 2-9 are -1 and position 11 is 0.
The list search exits only past position 10 (`10 < index`), so two monsters qualify: `0xFB` (position 1)
with quest `0xA7` (handbook quest row (167, 100)), and `0x103` (position 10) with quest `0xAA` (row
(170, 70)). Nothing writes `01EED130`; its only readers are `00316958` and `00315DB0`.

`003162E0` keeps twelve samplers of 16 bytes at `01EED070` (`{id, -, last sample, step}`; ids 0-8, 11,
14, 17; step 100 for ids 5 and 17, else 1). When a counter has moved by at least its step, and the last
sample already met the target, and the Steam entry reads not achieved (`00863280`), it calls `008632B0`
again. `00316440` does the same for descriptor 13 (entry 19) before every kind-10 action is counted.

### What feeds each counter

| Index | Caller | Amount |
|---|---|---|
| 0, 1, 2 | `00305640`, when the acting unit's `[+0x698]` byte `+5` is 0: row kind `+0x1E` 0, 1 or 2 (`00305744`-`003057A5`) | 1 |
| 13 | the same, row kind 10, after `00316440` | the row index (`0xE2`-`0xF1`) |
| 3 | `003112F0`, for each stolen item as it clears the item's bit (`00311475`) | 1 |
| 4 | `003171C0`, called by `00312280` for a defeated unit whose `[+0x698]` byte `+5` is 1 (`003171E7`) | 1 |
| 6, 7 | the gil setter `00254EE0`: 6 when gil rises, 7 when it falls (`00254EF8`-`00254F02`) | the change |
| 11 | `00312280`, for each member given licence points (`00312496`) | the points given |
| 14 | `0056D370`, a sale while the shop shows loot (`[+0xE4] & 0x3FC0 == 0x1C0`) | the quantity |
| 19 | `0056D370`, every purchase (`0056D4D2`) | the encoded id bought |
| 17 | `00317090` from `00312280` (`003125BC`), and `002E2380` for script verb `addclanpoint` | `(byte +0x1C2 - byte +0x88) x word [[+0xE78]] + word [[+0xE70]]` of the foe; the verb's argument |
| 18 | `0028F0C0`, the chain counter's display update (`0028F0E3`) | the chain count |

Indices 6, 7, 11, 14 and 19 reach `00316A50` directly, from `00254F02`, `00312496` and `0056D4D2`; the
sale of loot loads `cl` = `0xE` and jumps to the purchase's call (`0056D48F`-`0056D498`). The rest go
through the 5-byte jump `00253770`, from six sites: `0028F0E3`, `002E2387`, `003057A5`, `00311475`,
`003170D8` and `003171E7`.

### Script and scene awards

Script verb `0x5AD` (`unkCall_5ad`, handler `00352250`) pops an int and calls `008632B0` with it. Script
verb `0x11B` (`startscene`, handler `0034C9A0`) calls `00863240` → `0020CB50(manager, key1, key2)`: key 2
is the scene number, key 1 the event-script number registered for the calling slot (`0032F240`, filled by
`0032FCA0`). `0020CB50` looks the pair up in the seven 12-byte rows `{key1, key2, entry}` at `00906290` and
awards the entry. Row 6 also awards entries 31-37 (`0020CC11`-`0020CC87`).

### From award to Steam

`008632B0(entry)` returns at once when no Steam manager exists (`[01F83450]` null). Otherwise
`0020CE60` returns when the entry's `+0x190` is set, sets it, clears `+0x194`, and when Steam's stats have
arrived (manager `+0x18`) calls user-stats slot `+0x38` with the tag and tail-jumps slot `+0x50`
(SetAchievement and StoreStats in the Steamworks interface order). Before that, the award is only marked
locally. The Steam stats receipt rewrites `+0x190` of entries 1-40 from Steam and awards entry 0 when the
other forty are achieved.

### Sky Pirate's Den

`00572920` lays out one statue for each descriptor 0-29 whose award bit is set (`00576E10` →
`003154B0(7, i)`), from the 32-byte records of `menuhandbook_order.bin`. A record whose first byte is
`0xFF` is drawn with the statue numbered `003165C0(record index)`; record 31's value 16 places it with
statue 16. The clan rank `00315390` counts the set award bits (`00316670`, which runs the sweep first) and
reads counter 17 as the clan points.

## Layouts

The achievement record, `01DFE410 + entry x 0x198`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u64` | id | descriptor index for entries 1-30; the entry's own index for 31-40; 0 for entry 0 |
| `008` | `char*` | tag | ACH_ tag, the name passed to Steam |
| `010` | `char[128]` | title | English Steam title; replaced by Steam's "name" on stats receipt |
| `090` | `char[256]` | desc | empty in the image; Steam's "desc" on stats receipt |
| `190` | `u8` | achieved set by an award, rewritten from Steam on stats receipt |  |
| `194` | `u32` | - | cleared by an award |

The descriptor, `00D10460 + index x 8`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8` | kind | 0 no counter, 2 signed word, 4 signed dword (`00316A81`, `003166F0`) |
| `01` | `u8` | offset | the counter's byte offset in block +`0x384C` |
| `02` | `u8` | mode | test, see the evaluator |
| `03` | `u8` | - | 0 in all 30 |
| `04` | `i32` | param | target, exact value, u16 range pair or monster-list index |

The saved achievement state, block `[020927C0]` (`002536A0`), which the save carries at payload `+0x8000`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `3844` | `u32` | awarded | bit i = descriptor i awarded; only ever set |
| `384C` | `i16[5]` | counters 0-4 |  |
| `3856` | `i16` | counter 13 (a 16-bit set) |  |
| `3858` | `i16` | counter 14 |  |
| `385A` | `u16` | - | no descriptor points here |
| `385C` | `i32` | counter 11 |  |
| `3860` | `i32` | counter 6 |  |
| `3864` | `i32` | counter 7 |  |
| `3868` | `i32` | counter 17 (clan points) |  |

The `menuhandbook.bin` chain. Each hop adds the `u16` at the current position, starting at blob `+8`:

```
+0x08 (hop 0)  u16 step, u16 mapCount, u8 bitmap[]            maps that mode 5 requires
hop 1          u16 step, u16 bestiaryCount, u16, u16 ruleCount, {u16 id|type<<12, u16 value}[]
hop 2          u16 step, u16 count, {u8 quest, u8 scenario}[]  00315DC0
hop 3          u16 step, u16 count, u16 monster[]              mode 7
hop 4          u16, u16, u32 mask, u32 value[popcount(mask)]   003165C0
```

`003165C0(i)` returns 0 for `i >= 32`, a missing blob or a zero hop, or a clear mask bit; otherwise the value
at the rank of bit `i` among the set bits. `003158B0` loads the file (kind 7, id `0xC8`) into `022C2550`.

The hops are summed in 32 bits: `003165C0` adds each step with `add eax, edx` and reads the next one with
`movzx eax, word ptr [rax]` (`003165DA`-`003165FC`), and `00315E90` mode 7 and `00316930` do the same.
The chain is therefore correct only while the loaded `menuhandbook.bin` (`[022C2550]`) sits below 4 GB.

## Shipped data

| Fact | Value |
|---|---|
| records | 41: `COUNT` 11, `SPECIAL` 11, `EVENT` 8, `MASTER` 4, `COMPLETE` 3, `TRIAL` 2, `CHAMPION` 1, `LEVEL` 1 |
| descriptors | 30: kind 2 ×7, kind 4 ×4, kind 0 ×19 |
| modes | 0: 13 (0-8, 11, 14, 17, 18); 1: index 19 (`0xD07F`); 2: 9, 10, 12; 3: 13; 5: 15; 6: 16; 7: 20-29 (0-9) |
| `menuhandbook.bin` copies | 9; 320 bytes (`ch`, `cn`, `in`, `kr`), 316 (`de`, `es`, `fr`, `it`), 312 (`us`) |
| copy read | `in`, or `ch` for three language settings: the kind-7 entry `0xC8` of every language's path array (`002DF9A0`) |
| targets in the copy read | 0: 300, 1: 200, 2: 100, 3: 50, 4: 500, 5: 50,000, 6: 100,000, 7: 1,000,000, 8: 50, 11: 48,000, 13: 8, 14: 1,000, 17: 500,000, 18: 50, 31: 16 |
| `us`, `de`, `es`, `fr`, `it` copies | the same targets without index 11 |
| monster list | 11 ids: `0xF8`, `0xFB`, `0xFD`, `0xF0`, `0xFA`, `0xE6`, `0x104`, `0x121`, `0x10F`, `0x111`, `0x103`; no descriptor indexes the last, the sweep reaches it |
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
| 15 | `ACH_MASTER_MAGIC` | Runeweaver | 9 | all of `0x3000`-`0x3050` owned |
| 16 | `ACH_MASTER_TECH` | Jack-of-All-Trades | 10 | all of `0x4000`-`0x4017` owned |
| 17 | `ACH_SPECIAL_HORIDASHI` | Collector | 19 | bazaar good `0xD07F` bought |
| 18 | `ACH_COMPLETE_MAP` | Cartographer | 15 | every flagged map visited |
| 19 | `ACH_COMPLETE_YUGOU` | Mist Walker | 13 | 8 different kind-10 rows used |
| 20 | `ACH_SPECIAL_MONSTER06` | Eagle Eye | 25 | monster `0xE6` defeated |
| 21 | `ACH_SPECIAL_MONSTER04` | Wyrmslayer | 23 | monster `0xF0` defeated |
| 22 | `ACH_SPECIAL_MONSTER01` | Sharpshooter | 20 | monster `0xF8` defeated |
| 23 | `ACH_SPECIAL_MONSTER05` | Freshmaker | 24 | monster `0xFA` defeated |
| 24 | `ACH_SPECIAL_MONSTER02` | Master Swordsman | 21 | monster `0xFB` defeated, or quest `0xA7` |
| 25 | `ACH_SPECIAL_MONSTER03` | Lord of the Kings | 22 | monster `0xFD` defeated |
| 26 | `ACH_SPECIAL_MONSTER07` | Hunter Extraordinaire | 26 | monster `0x104` defeated |
| 27 | `ACH_SPECIAL_MONSTER08` | Radiant Savior | 27 | monster `0x121` defeated |
| 28 | `ACH_SPECIAL_MONSTER09` | Fell Angel | 28 | monster `0x10F` defeated |
| 29 | `ACH_SPECIAL_MONSTER10` | Zodiac Knight | 29 | monster `0x111` defeated |
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
| `00316A50(index, amount)` | update a counter or fire a counter-less descriptor |
| `00315E90(index)` | evaluate one descriptor and award it |
| `003166F0(index)` / `00316BF0(index, value)` | read / store a counter at its declared width |
| `00316760(index)` | counter value, with the step total and mean level for 5 and 8 |
| `003165C0(index)` | the handbook target |
| `00316930()` | sweep: rare-monster fix-up, evaluate 0-29, re-send |
| `008632B0(entry)` | award a Steam entry |
| `00316810()` | on load (`00584398`): reseed the samplers and pull a saturated counter one below its cap (`0x7FFE`, `0x7FFFFFFE`) |

## State

| Address | What |
|---|---|
| block `+0x3844`, `+0x384C`-`+0x386B` | award bits and counters, saved ([save fields](../Saving-Loading-And-Settings/save-data-fields.md)) |
| `01DFE410` + `0x190` per entry | the Steam-side achieved bytes, not saved |
| `01EED070` | the twelve samplers, reseeded on load |
| `022C2550` | the loaded `menuhandbook.bin` |

The award bits are only set: the one other writer of `+0x3844`, `00315910` category 7, is reached only from
`00577699` with categories 0-4 (`00D23750`).

## Modding notes

- A counter target is the handbook copy the language reads (`in` or `ch`); editing the `us` copy changes
  nothing. A descriptor whose mask bit is clear falls back to its `param`, which is 0 for every counter.
- A counter award lands on the update after the one that crosses the target, or at the next sweep.
- An award made before Steam's stats arrive is marked locally and then overwritten by the receipt. Counter
  achievements and entry 19 are sent again by the re-send; a scene, script or evaluator award is not, because
  its save bit is already set.
- Raising the descriptor `param` of a mode-7 entry to 10 makes it use the eleventh list monster `0x103`.
- `kind` and `offset` place the counter in the save block; overlapping offsets share bytes.

## Related

- [Steam integration](steam-integration.md): the award call and the stats receipt.
- [Clan Primer](../Menus-And-HUD/clan-primer.md): the Sky Pirate's Den and the Bestiary rules.
- [Handbook files](../Game-Files-And-Data-Tables/handbook-files.md): the other handbook files.
- [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md): `addclanpoint`.
- [Script verb table](../Scripts-And-Script-Commands/verb-table.md): verbs `0x5AD` and `0x11B`.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the block that holds the award bits and counters.
