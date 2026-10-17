---
title: "Gambits: how a character's gambit list is checked top to bottom, what runs before it, the three gambit sets and the authored presets"
kind: "system"
category: "Enemy AI and gambits"
addresses: "00305AB0, 00305CC0, 003014C0, 00308EC0, 00327DE0, 00326030, 00327CB0, 0030F760"
---

## What the player sees

When a character is ready to act:

1. **A command the player gave** is carried out first; the gambits are not looked at.
2. **Confuse**, and **Berserk** on a party member, replace the gambit list with their own behaviour.
3. Otherwise the **gambit list** is tried from the top. The first line whose target condition finds a
   target and whose action can be carried out is the one that runs; the lines below it are not tried.
   A party member whose record is not marked for gambits only carries out commands (below).
4. A line that is switched off, or has no condition or no action, is not in the list at all.
5. A "Foe" condition only picks an enemy that already holds enmity toward someone. An enemy that has not
   noticed anyone is not a gambit target until something raises its enmity ([Enmity](enmity.md)).

Each character has three gambit sets. All three start as copies of the character's preset, and the menu
chooses which one is used.

## How it works

### What runs before the gambits

`00305AB0(unit, resume)` picks the next action (`00305AB0`-`00305CB4`). A unit with flag bit 22 first runs
`00308270` (`00305AC1`-`00305AC8`). Then:

1. **A pending command.** When unit flag `0x4000` is set it is cleared (`00305AEB`); the command's action
   `+0xBA0` and target `+0xBB8` are committed with `0030F760`. Ids `0x4000`-`0x4166` (orders) skip the
   availability check `002FFCF0` (`00305AF6`-`00305B09`). A successful commit ends the turn.
2. **Confuse or Berserk.** When the unit has Confuse (status 5), or is an enemy-table unit with Berserk
   (27), the order set at `01EEC320` is walked instead (`00305B66`-`00305B90`).
3. **The unit's own lists.** The set at `+0x6E8` is walked; a party record with Berserk then walks the set
   at `01EEC370` (`00305BBB`-`00305BE5`) and, when that fails, goes on to step 5.
4. **The gambit list.** For a party record, the walk of the gambit set at `+0x6E0` happens only when bit 2
   of its stats record's first dword is set; otherwise a command set at `+0x6F8` is walked if one is
   queued (`00305BE7`-`00305C32`). Enemy records walk `+0x6E0` with their subgroup `+0x6B5`
   ([Enemy AI](enemy-ai.md)). The `+0x6E0` walk first clears `+0x6F8` and `+0x748` (`00305C3C`-`00305C4C`).
5. **The last set** at `+0x6F0` is walked (`00305C61`-`00305C71`).
6. **Nothing matched.** Unless resuming, the unit commits order `0x4021`, a wait, from `01EEC298`
   (`00305C7E`-`00305C9B`, [Battle orders](../Battle-Actions/battle-orders.md)).

With bit 15 of the active field record set, a party record skips steps 2-5 and goes straight to step 6
(`00305B3C`-`00305B57`), and every other unit skips step 2 (`00305B5D`-`00305B64`).

### The walk

`00305CC0(unit, set, subgroup, resume)` walks one subgroup of an order set (`00305CC0`-`00305E64`):

1. The set's first `0x20` bytes count the orders of each subgroup; the subgroup's first order is after
   the counts of all earlier subgroups (`00305D24`-`00305D97`). A subgroup with a count of 0 walks
   nothing.
2. For each order in turn it calls the evaluator `003014C0(unit, order, &action, &target)` and, when that
   matches, the commit `0030F760(unit, order, action, target, 1)` (`00305DC2`-`00305DF9`).
3. The first order that both matches and commits ends the walk with 1. Otherwise it moves 24 bytes on, up
   to the subgroup's count, which it re-reads every time (`00305DFD`-`00305E0A`).

In resume mode, an order with flag `0x80` is skipped, and while the order in flight (`[unit+0x708]`) has
flag `0x4000` only orders with flag `0x40` are tried (`00305D6B`-`00305DC0`). Reaching the order the context points at
returns 1 without trying it (`00305DA4`). A resumed commit also calls
`004697C0([unit+0x698], action, previous action, 4)` (`00305E31`-`00305E5A`).

### One line's test

`003014C0` decides whether one order can run (`003014C0`-`0030180E`):

1. It decodes the action (`00308EC0`, below) into `*action` (`00301500`); `0xFFFF` fails.
2. Bit 5 of the battle flags `02089340`, the battle freeze, fails every order
   ([Boss fights](../Battle-Actions/boss-fights.md); `00301511`).
3. Every order but `0x414D` fails for a unit that cannot act (`0030151A`-`00301580`): its flag byte lacks
   bit 4, it has no stats record, it has KO, Stone or X-Zone and the field's bit 15 does not waive it, or it
   is an enemy-table unit whose spawn record's first byte has a bit of `0x30` or `0x48`. So a KO'd
   character's gambits never run.
4. An order with flag `0x800` fails while it is the unit's previous order `+0x738`; for an action id only
   when the previous command's `+0x730` bit 0 is set (`003015A6`-`003015C9`).
5. For an action outside the order band, the actor and the availability check must pass
   (`003015EA`-`00301606`), and an order with a non-zero chance word `c` at `+0x02` passes only when a shared
   gameplay LCG draw gives `00328370() % 100 < (s16)c` (`00301608`-`00301637`; the draw is `00328370`,
   [Random number generators](../Random-Numbers/random-number-generators.md)).
6. It builds the candidates for an action with `0030F130` (`00301649`). An order id instead must pass
   `00301830` and takes the unit's perception list `+0xBC0` as its candidates (`00301599`, `003015D4`-`003015E1`;
   [Enemy AI](enemy-ai.md)). Then it runs the order's tests, below.

### The target tests

An order holds three 6-byte tests from `+0x06`, each a relation, a sub-selector, an opcode and an operand.
`003014C0` runs them in turn (`00301681`, `0030176D`, `00301771`):

- a test whose relation is 0 is skipped (`00301685`);
- each test runs the selector `00301AD0` over the same candidates, unless bits `0x20 >> i` and
  `0x20 >> (i + 1)` of the order's flags are both set, which makes test i + 1 filter test i's result
  (`003016BE`-`003016E0`);
- a test that keeps no unit fails the order (`003016AD`);
- the target is chosen from what the first test kept, by `003087E0` (`003017BF`).

A gambit line copies its flags from the condition row's `+0x0E`, which is 0 in every shipped row, so a second
test only has to find one unit. Every test, opcode and pick rule of the shipped conditions is on
[Gambit conditions](gambit-conditions.md).

### Which units a condition may pick

`0030BD00(unit, candidate, mode)` admits a candidate by the relation mode (`0030BD27`-`0030BE3E`). It first asks
`0030AB40` whether the two are on the same side (`0030AB40`-`0030AC41`):

- a unit whose actor class nibble is 5, or whose flag byte lacks bit 4, is on neither side
  (`0030AB93`-`0030ABB2`);
- a party record, or an actor of class nibble 3, is on the party side, and every other unit on the other
  side (`0030ABB8`-`0030AC0A`);
- a deciding unit under Confuse sees the two sides swapped (`0030AC14`-`0030AC25`).

| Mode | Admits | Gambit word | Site |
|---:|---|---|---|
| `0` | every unit | - | `0030BD45` |
| `1` | a unit on the other side | Foe | `0030BD6D` |
| `2` | a unit on the same side | Ally | `0030BD5E` |
| `3` | the unit whose id is the deciding unit's `+0x24` | - | `0030BDBC` |
| `4` | the deciding unit itself | Self | `0030BD4F` |
| `5` | a unit with the same team byte `+0x54` | - | `0030BDCB` |
| `6` | a unit on the same side other than itself | - | `0030BDDB` |
| `7` | a unit with the same team byte other than itself | - | `0030BDF1` |
| `8` | a unit with a different team byte | - | `0030BE08` |
| `9` | the deciding unit's current target `+0x710` | - | `0030BE18` |
| `10` | the unit in the deciding unit's `+0x748` | - | `0030BE2A` |

For mode 1, when a party record looks at an enemy-table record, the enemy must also hold enmity above 0
toward one of the 40 combatants (`0030BDA0`, `00321840` → `00321770`). Without it no Foe condition, not even
"Foe: party leader's target", picks that enemy.

### A weighted action

`00308EC0` reads the order's action word (`00308EC0`-`00308FCC`). A word below `0x8000` is the action id
itself. A word from `0x8000` is an index into the weighted table `[02EBF160]`: entries `index` to
`index + 1` of its pointer list bound a run of 4-byte entries (below), and a shared
gameplay LCG roll `r = LCG % 100` picks the first entry whose running weight sum is above `r`
(`00308F61`-`00308F99`). With no such entry the result is `0xFFFF`.

Each weighted entry, 4 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | action | the action id |
| `+0x02` | `u8` | weight | its weight in the roll |
| `+0x03` | `u8` | pad | not read by the pick |

### From the menu to the list

Each party member's twelve gambit lines are stored as a bank of `0x34` bytes in the battle state block
`[02EBF190]`: the bank of member `k` is `+0x5B10 + (k * 3 + selected) * 0x34`, with the selected set at
`+0x7370 + 4 * k` (`00327E27`-`00327E4B`). `00327DE0(stats)` rebuilds the member's order set at
`02089378 + type * 0x170` from it (`00327DE0`-`00327F70`):

- every line whose bit in the mask `+0x30` is set and whose condition and action are both not `0xFFFF`
  becomes one 24-byte order, in line order (`00327E60`-`00327F4B`);
- the order's action word is the line's action, and its flags and condition fields are copied from the
  condition's row of `02EBF0D8` (id `0x6000` + row, `00327EC1`-`00327F33`); the chance word `+0x02` is not
  written;
- the number of orders is stored as the count of subgroup 0 (`00327F60`).

A switched-off line is therefore not in the walked list.

### The three sets and the presets

`00326030(state, k)` resets member `k`'s selected set to 0 and copies the 52-byte gambit block at stats
`+0x88`-`+0xBB` into all three banks (`00326039`-`003260D5`).

That block is filled from an authored preset by `00327CB0(stats, preset)` (`00327CB0`-`00327DD9`). A preset
is a row of `02EBF0E0`, id `0x5000` + row, with twelve condition words from `+0x00` and twelve action words
from `+0x20`. The loader copies the pairs into the twelve 4-byte slots from `+0x88` until either word is
`0xFFFF`, sets a mask bit for each (`+0xB8`) and stores the count (`+0xBA`) (`00327D42`-`00327D84`). The unit
definition passes the party table row's word `+0x14` as the preset (`0023AEEE`).

The fresh stats record `0023AC80` calls `00327CB0`, `00326030` and `00327DE0` in turn (`0023AEF5`-`0023AF1D`,
[Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)). The party-row reset `00328BD0`, run
by the script verb `resetJobs`, makes the same three calls (`00328CAA`-`00328D1E`,
[Party table](../Party/party-table.md), [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)).

## Layouts

The gambit bank, `0x34` bytes, three per party member:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[24]` | lines | twelve (condition, action) pairs; `0xFFFF` = empty (`00327E6B`-`00327E80`) |
| `+0x30` | `u16` | enabled | bit i set: line i is on (`00327E60`-`00327E65`) |
| `+0x32` | `u8` | count | number of line slots the menu shows, 0-12; setgambit_slotmax adds to it (`00327930`) |
| `+0x33` | `u8` | pad33 | copied with the block |

One order of a walked set, 24 bytes from set `+0x20`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | action | action id, or `0x8000` + weighted-table index (`00308ECA`) |
| `+0x02` | `i16` | chance | percent chance the line is tried; 0 = always (`00301608`) |
| `+0x04` | `u16` | flags | `0x40` try while resuming, `0x80` skip on resume (`00305DB2`, `00305DBC`); `0x4000` on the order in flight limits a resume to `0x40` orders (`00305D7F`); `0x20` >> i with `0x20` >> (i + 1) chains test i + 1 to test i (`003016BE`); `0x800` not repeated while it is the previous order (`003015A6`); a gambit line takes the condition row's `+0x0E` (`00327F2F`) |
| `+0x06` | `u16` | relation0 | first test: relation mode, 0 = no test (`00301685`; row `+0x10`, `00327EEA`) |
| `+0x08` | `u8` | sub0 | first test: sub-selector (`00301B1A`; row `+0x08`, `00327EDF`) |
| `+0x09` | `u8` | opcode0 | first test: opcode; even = highest, set or at least, odd = lowest, clear or below (`00301B14`, `00301B44`) |
| `+0x0A` | `i16` | operand0 | first test: operand (`00301B1F`; row `+0x18`, `00327EF2`) |
| `+0x0C` | `u16` | relation1 | second test, from row `+0x11` (`00327F02`) |
| `+0x0E` | `u8` | sub1 | from row `+0x0A` (`00327EFA`) |
| `+0x0F` | `u8` | opcode1 | from row `+0x0B` (`00327EFA`) |
| `+0x10` | `i16` | operand1 | from row `+0x1A` (`00327F0A`) |
| `+0x12` | `u16` | relation2 | third test, from row `+0x12` (`00327F1A`) |
| `+0x14` | `u8` | sub2 | from row `+0x0C` (`00327F12`) |
| `+0x15` | `u8` | opcode2 | from row `+0x0D` (`00327F12`) |
| `+0x16` | `i16` | operand2 | from row `+0x1C` (`00327F22`) |

One gambit condition, a row of `battle_pack.bin` section 7 (`02EBF0D8`, 32 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[3]` | pad00 | 0 in every row |
| `+0x03` | `u8` | b03 | `0xFF` in every row; copied to the menu record `+0x2C` (`0031D0CB`) |
| `+0x04` | `u16` | helpId | 16000 + row: the help line (`0031D0BE`) |
| `+0x06` | `u16` | value06 | 50, 70, 100 or 300; copied to the menu record `+0x28` (`0031D0B7`) |
| `+0x08` | `u8` | sub0 | first test sub-selector (`00327EDF`) |
| `+0x09` | `u8` | opcode0 | first test opcode (`00327EDF`) |
| `+0x0A` | `u8` | sub1 | second test sub-selector (`00327EFA`) |
| `+0x0B` | `u8` | opcode1 | second test opcode (`00327EFA`) |
| `+0x0C` | `u8` | sub2 | third test sub-selector, 0 in every row (`00327F12`) |
| `+0x0D` | `u8` | opcode2 | third test opcode, 0 in every row (`00327F12`) |
| `+0x0E` | `u16` | orderFlags | copied to the order's flags, 0 in every row (`00327F2F`) |
| `+0x10` | `u8` | relation0 | 1 Foe, 2 Ally, 4 Self (`00327EEA`) |
| `+0x11` | `u8` | relation1 | second test relation (`00327F02`) |
| `+0x12` | `u8` | relation2 | third test relation, 0 in every row (`00327F1A`) |
| `+0x13` | `u8` | pad13 | 0 in every row |
| `+0x14` | `u16` | nameWord | section 61 sub-table word >> 11, entry word & `0x7FF` (`0031D034`) |
| `+0x16` | `u8` | menuColumn | gambit menu column; `0xFF` = not listed (`002388F3`) |
| `+0x17` | `u8` | menuRow | gambit menu row (`00238903`) |
| `+0x18` | `i16` | operand0 | first test operand (`00327EF2`) |
| `+0x1A` | `i16` | operand1 | second test operand (`00327F0A`) |
| `+0x1C` | `i16` | operand2 | third test operand, 0 in every row (`00327F22`) |
| `+0x1E` | `u16` | pad1E | 0 in every row |

## Shipped data

The presets are `battle_pack.bin` section 8, 40 rows of 64 bytes. 29 party table rows name one in word
`+0x14`; rows 14 and 16 share `0x500E`, and rows 6 and 17-26 have none (`0xFFFF`). Presets `0x5006` and
`0x5010`-`0x501A` are named by no party row. Party rows 0-5 are Vaan, Ashe, Fran, Balthier, Basch and Penelo,
the characters the "Ally: Vaan" to "Ally: Penelo" conditions test, and rows 27-39 are the Espers.

All 40 rows, with their condition ids and action rows, are in [gambit-preset-list.tsv](gambit-preset-list.tsv),
which `Database/Tools/catalogues/gambit_presets.py` writes from the shipped file (two runs give byte-identical
output). The twelve presets no party row names hold "Foe: nearest visible → Attack": once in `0x5006` and
`0x5010`-`0x5019`, twelve times in `0x501A`.

| Preset | Party rows | Lines, top first |
|---|---|---|
| `0x5000` | 0 | Foe: party leader's target → Attack |
| `0x5001` | 1 | Ally: HP < 50% → Potion; Foe: nearest visible → Attack |
| `0x5002` | 2 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5003` | 3 | Ally: any → First Aid; Foe: nearest visible → Attack |
| `0x5004` | 4 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5005` | 5 | Foe: party leader's target → Attack |
| `0x5007` | 7 | Ally: HP < 50% → Cure; Foe: nearest visible → Attack |
| `0x5008` | 8 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5009` | 9 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x500A` | 10 | Ally: HP < 30% → Cura; Ally: HP < 50% → Cure; Self: HP < 70% → Potion; Foe: targeting self → Attack; Foe: nearest visible → Attack; Ally: any → Poisona; Ally: any → Blindna; Ally: any → Vox |
| `0x500B` | 11 | Foe: flying → Telekinesis; Foe: party leader's target → Attack; Foe: targeting self → Attack; Foe: targeting ally → Attack; Foe: nearest visible → Attack; Foe: any → Attack |
| `0x500C` | 12 | Foe: flying → Telekinesis; Foe: party leader's target → Attack; Foe: targeting self → Attack; Foe: targeting ally → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Phoenix Down |
| `0x500D` | 13 | Ally: HP < 50% → Cura; Self: HP < 70% → Potion; Foe: party leader's target → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Poisona; Ally: any → Blindna; Ally: any → Vox |
| `0x500E` | 14, 16 | Foe: party leader's target → Attack; Foe: targeting ally → Attack; Foe: targeting self → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Arise; Ally: any → Serum; Ally: any → Gold Needle; Ally: any → Echo Herbs; Self: HP < 30% → Domaine Calvados |
| `0x500F` | 15 | Foe: nearest visible → Attack |
| `0x501B` | 27 | `0x60FF` → Hellfire; Foe: fire-vulnerable → Painflare; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501C` | 28 | `0x60FF` → Frostwave; Foe: ice-vulnerable → Flash-Freeze; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501D` | 29 | `0x60FF` → Judgment Bolt; Foe: lightning-vulnerable → Flash Arc; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501E` | 30 | `0x60FF` → Gaia's Wrath; Foe: earth-vulnerable → Roxxor; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x501F` | 31 | `0x60FF` → Blight; Foe: undead → Attack; Foe: nearest visible → Malaise; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5020` | 32 | `0x60FF` → Tsunami; Foe: water-vulnerable → Briny Cannonade; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5021` | 33 | `0x60FF` → Condemnation; Foe: nearest visible → Kill; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x5022` | 34 | `0x60FF` → Soul Purge; Foe: nearest visible → Devour Soul; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5023` | 35 | `0x60FF` → Tornado; Foe: wind-vulnerable → Whirlwind; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5024` | 36 | `0x60FF` → Big Bang; Foe: nearest visible → Gravity Well; Foe: nearest visible → Attack |
| `0x5025` | 37 | `0x60FF` → Meteor; Foe: nearest visible → Comet; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5026` | 38 | `0x60FF` → Eschaton; Foe: holy-vulnerable → Redemption; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5027` | 39 | `0x60FF` → Final Eclipse; Foe: dark-vulnerable → Banish Ray; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |

Every Esper preset starts with condition `0x60FF`, which takes the foe with the highest max HP while the summon
timer is below 20 ([Gambit conditions](gambit-conditions.md)).

## Modding notes

- A character's starting gambits are the preset its party row names in `+0x14`; editing a preset row
  changes every character that uses it.
- Order of lines is priority: the walk never re-sorts them.
- A line's percent chance and weighted action are features of the order format; the gambit rebuild
  writes neither, so a party line's action is the one the menu shows.

## Related

- [Gambit conditions](gambit-conditions.md) - every target condition.
- [Enemy AI](enemy-ai.md) - the same walk for enemies and the subgroups.
- [Enemy order sets](enemy-order-sets.md) - every shipped enemy order, in the 24-byte order layout.
- [Action commit](../Battle-Actions/action-commit.md) - `0030F760`.
- [Battle orders](../Battle-Actions/battle-orders.md) - the order ids, including `0x4021`.
- [Boss fights](../Battle-Actions/boss-fights.md) - the battle freeze.
