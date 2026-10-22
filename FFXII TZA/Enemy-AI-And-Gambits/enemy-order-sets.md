---
title: "Enemy order sets: every enemy's own order lists by area, each order's action, chance, flags and tests"
kind: "reference"
category: "Enemy AI and gambits"
addresses: "0x02EBF168, 0x02EBF160, 0x00301AD0, 0x003014C0, 0x00305CC0, 0x00308EC0, 0x00301830, 0x00321190, 0x002FE660, 0x0030BD00"
---

## What it lists

An enemy's own lists are order sets from its area file's directory slot 1, `[0x02EBF168]`
([Enemy AI](enemy-ai.md), [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)). The
166 shipped area files hold 1,422 sets with 50,050 orders between them:

- [the order sets](enemy-order-sets.tsv), one row per set: its order count, its phase counts and the enemies
  that use it;
- [the orders](enemy-orders.tsv), one row per order, in the order the walk `0x00305CC0` tries them.

Slot 1 opens with a `u16` count and a `u16` that is 100 in every file, then `count + 1` 32-bit offsets from the
section. Each set fills the bytes up to the next offset exactly: twelve phase counts, 20 zero bytes, then the
24-byte orders ([Gambits](gambits.md) has the order layout).

An enemy definition names its sets by four words: `+0x50` is the list the unit starts with (`0x0023A94D`), and
`+0x50`, `+0x52`, `+0x54` and `+0x56` are lists 0-3, which orders `0x4112`-`0x4115` switch to (`0x002FE025`). Orders
`0x4116`-`0x4121` switch the phase, the subgroup of the set the walk starts in (`0x002FE0B3`).

### The weighted actions

An action word from `0x8000` is an index into `[0x02EBF160]`, `battle_pack.bin` directory entry `+0x2C`: a `u16`
count (826), then `count + 1` offsets from the section, each pair bounding a run of 4-byte entries (`u16` action,
`u8` weight, `u8` pad). Every shipped run's weights sum to 100. `0x00308EC0` draws `r = LCG % 100` and takes the
first entry whose running sum is above `r` (`0x00308F61`-`0x00308F99`).

### What a test can check

Each test is a relation word, a sub-selector byte `s`, an opcode byte and an `i16` operand `v` (order `+0x06`,
`+0x08`, `+0x09`, `+0x0A` for test 1, then every 6 bytes). `0x00301AD0` runs it over the candidates the relation
filter `0x0030BD00` admits; a relation above 10 admits none (`0x0030BD2A`). The opcode picks the check through the
jump tables `0x00303680`/`0x00303604` (`0x00301EA3`-`0x00301ECA`).

An even opcode keeps the units that pass and the next odd one the units that fail (`0x00301B44`). For a highest or
lowest check the even opcode takes the highest. A distance or angle check passes for the even opcode when the
value is below `v` ("within"), and for the odd one when it is `v` or more.

The distance of `s` = 7 is `0x0031E6F0`: the horizontal distance between the two units' positions `+0xE0` less
each unit's collision radius, the larger of its two radii (the calls at `0x0031E70D` and `0x0031E718`), and never
below 0 (`0x0031E750`) ([Navigation](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)).

| Opcodes | Check | Site |
|---|---|---|
| 0 | any unit, picked at random | `0x00301ECC` |
| 2, 3 | highest / lowest of a value chosen by `s`: 0 attack power `+0x2E`, 1 defense `+0x2F`, 3 magick resist `+0x30`, 4 HP, 5 MP, 6 level `+0x1C2`, 7 distance (`0x0031E6F0`), 8 units committed against it `+0xEA8`, 9 max HP, 10 max MP, 12-15 strength, magick power, vitality, speed (`+0x2A`-`+0x2D`), 17 the deciding unit's enmity toward it, party members only (`0x003215C0`; opcode 2 needs it above 0) | `0x00301EF7`, table `0x003036C8` |
| 6, 7 | status `s` (stats `+0x64` or `+0x3C`) | `0x003021A3` |
| 8, 9 | unit byte `+0x55` is `s` (13 = undead) | `0x003021CC` |
| 10, 11 | unit type byte `+0x56` is `s` (46 = flying) | `0x003021EC` |
| 12, 13 | bit `s` of unit word `+0x52` | `0x003021F3` |
| 14, 15 | HP at least 90, 80, 70 ... 0 % of max HP for `s` = 0-9 (`0x00D102E0`) | `0x00302203` |
| 16, 17 | max HP at least 500, 1,000, 2,000, 5,000, 10,000, 20,000, 30,000, 50,000, 100, 200 (`0x00D10308`) | `0x003022FC` |
| 20, 21 | weak to element `s` (stats `+0x40`) | `0x003023A5` |
| 22, 23 | absorbs element `s` (stats `+0x41`) | `0x003023C9` |
| 24, 25 | party type `s` (stats word `+0x04`; 255 stands for `0xFFFF`) | `0x003023ED` |
| 26, 27 | equipment slot `s` (0-5) holds an item: stats word `+0x50 + 2s` is neither `0xFFFF` nor `0x1000` | `0x00302416` |
| 28, 29 | the weapon's motion class is `s` (byte `+0x26` of its equipment row, through `0x00321320`) | `0x00302451` |
| 32, 33 | augment `s` in the augment layer stats `+0x68` or `+0x78`, named by its term on [Augment list](../Damage-And-Battle-Formulas/augment-list.md) ([Augments](../Damage-And-Battle-Formulas/augments.md)) | `0x00302478` |
| 34, 35 | one of 23 checks chosen by `s` (next table) | `0x003024B0`, table `0x00303710` |
| 36, 37 | within `v` of field point `s + 1` (`0x00320940`) | `0x00302C8F` |
| 38, 39 | within `v` of the unit of definition selector `s` (`0x002367A0`) | `0x00302D1F` |
| 40, 41 | HP missing at least 100, 200, 300, 500, 700, 1,000, 2,000, 3,000, 4,000, 5,000 (`0x00D10328`) | `0x00302DB4` |
| 42, 43 | HP at least 100,000, 50,000, 10,000, 5,000, 3,000, 2,000, 1,000, 500, 75, 50 (`0x00D10350`) | `0x00302E80` |
| 44, 45 | MP at least 75, 50, 25 or 10 % of max MP (`0x00D10370`); a unit with max MP 0 fails | `0x00302F17` |
| 46, 47 | `s` = 0: HP full; `s` = 1: MP full | `0x00302F7E` |
| 48, 49 | the whole field, read at the first candidate: `s` = 0 the environment class (`0x00321490`) is `v`, 1 the MP regime (`0x00320160`) is `v`, 2 the MP regime is at least `v` | `0x00303027` |
| 52, 53 | before any candidate: every active enemy whose spawn record tag `+0x15` is `v` (1-255) and that no unit is committed against (`+0xEA4` = 0) | `0x00301CFB`-`0x00301DAB` |
| 54, 55 | before any candidate, for `s` = 0-2: a register (next tables) equal to `v`, at least `v`, or with bit `v` set; a pass keeps the deciding unit. `s` = 3 runs the candidates instead and tests bit `v` of each one's register `+0xB90` | `0x00301C2B`-`0x00301CF6`, `0x00303079` |
| 56, 57 | `s` = 0: on screen (`0x00322360`), nearest for 56 and furthest for 57; 1: the party leader's target (`+0x750`); 2: carrying out a magick (its action's kind `+0x1E` is 1) | `0x003030A7` |
| 58, 59 | at least `v` units that relation mode `s` admits (0 = every unit) in its own perception list `+0xBC4` | `0x003031C4` |
| 60, 61 | team byte `+0x54` is `v` | `0x0030329B` |
| 62, 63 | MP at least `10 * s` % of max MP | `0x003032A7` |
| 64, 65 | the deciding unit holds at least `10 * s` of the line's item (`0x003093D0`, `0x00309EC0`, read at the first candidate), or the candidate is an enemy | `0x003032C0` |
| 66, 67 | a unit committed against it (`+0xEA4`) carries: `s` = 0 the same action; 1 an action removing a status it has that this action also removes (`0x0031C500`); 2 an action restoring HP (`+0x2C` bit 12); 3 one restoring MP (bit 15) | `0x00303334` |
| 68, 69 | the whole field: the summon timer (battle state `+0x5AD8`) at least 20, 30, 60, 90 or 120 (`0x00D10380`) | `0x00303523` |
| 1, 4, 5, 18, 19, 30, 31, 50, 51 | no unit is kept | `0x00301C08`, `0x00303567` |

An active enemy of opcodes 52 and 53, and a party slot of check 18 below, counts only while it is in play: a
unit whose status words `+0x3C | +0x64` hold KO, Stone or X-Zone (`0x80000003`) is passed over unless the area's
town flag is set (the calls at `0x00301D4E` and `0x00302738`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

The checks of opcodes 34 and 35:

| `s` | Check | Site |
|---|---|---|
| 0 | linked to a unit: `+0x24` is not 0 | `0x003024C8` |
| 1 | the party leader (`0x003273B0`) | `0x003024DA` |
| 2 | its own linked unit (`+0x08` = `+0x24`) | `0x003024F0` |
| 3 | a guest: a party record of type 7-25 | `0x003024FD` |
| 4 | a party record of type 27-39 | `0x00302537` |
| 8 | its highest enmity toward an active party member is at least `v` (`0x00321630`) | `0x0030255D` |
| 9-12 | a unit in its own perception list whose team byte `+0x54` is `v` (9), with status `v` (10), whose byte `+0x55` is `v` (11), or whose byte `+0x56` is `v` (12) | `0x003025B6` |
| 13 | an enemy whose definition row byte `+0x03` has bit `0x10` | `0x0030266C` |
| 16 | level `+0x1C2` at least `v` | `0x00302696` |
| 17 | within `v` of the point at `+0x50` of the deciding enemy's spawn record (the deciding unit must be an enemy) | `0x0030282B` |
| 18 | 34: within `v` of the nearest of party slots 0-3; 35: `v` or more from the furthest | `0x003026EC` |
| 19, 20 | within `v` of the party leader (19) or of the deciding unit's linked unit (20) | `0x003028C2`, `0x00302945` |
| 21 | the party leader within `v` degrees of its facing | `0x003029C7` |
| 24, 25, 26 | targeting (`+0x710`) the deciding unit's linked unit, the deciding unit, or one of the deciding unit's allies | `0x00302A76`, `0x00302A98`, `0x00302AB1` |
| 27 | targeting combatant `v` | `0x00302AE3` |
| 28, 29 | within `v` degrees of the deciding unit's facing (28) or within `v` of the deciding unit (29) | `0x00302B18`, `0x00302BC0` |
| 30, 31 | a status of set A `0x0208D320` other than bit 29 (30), or of set B `0x0208D324` (31) | `0x00302C35`, `0x00302C59` |
| 32 | holding a bow, crossbow, gun or hand-bomb (equipment class 7, 8, 9 or 17, group 4 of `0x0031E9F0`) | `0x00302C77` |
| 5-7, 14, 15, 22, 23 | no unit is kept | `0x00303567` |

### The registers

A register is named by a kind and an index: kind = relation word `>> 12`, index = its low byte. `0x00321190` reads
it (`0x003211A4`-`0x003211B8`) and `0x00329E60` writes it:

| Kind | Register | Reader |
|---|---|---|
| 1 | word `i` of the 64-word field table `[0x02098E68]` (word 3 is the group-defeated signal, [Boss fights](../Battle-Actions/boss-fights.md)) | `0x00264D20` |
| 2 | word `i` of the 32-word table `[0x02098E70]` | `0x00264800` |
| 3 | story word `i` of `[0x02098E58]`, 256 words ([Story progress](../Story-Events-And-Hunts/story-progress.md)) | `0x00264640` |
| 4, 5 | quest `i` ordered, quest `i` cleared ([Quests](../Story-Events-And-Hunts/quests.md)) | `0x0046B240`, `0x0046B1A0` |
| 6 | quest `i`'s progress byte, save `+0x1064` | `0x0046B180` |
| 7 | quest `i`'s contract word, save `+0x1164` | `0x0046B0D0` |
| 8 | story flag `i` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) | `0x0032A920` → `0x0032A8A0` |
| 9 | battle word `i` of the sixteen at `0x0208D334`, zeroed when an area starts | `0x00321253` |
| 10 | the unit's own register `+0xB90` (index 0) | `0x0032126F` |

The orders that write a register (`0x002FE660`) take it from the order's own test-1 relation word, except
`0x4122` and `0x4123`, which write the `+0xB90` of the unit in the deciding unit's `+0x710`:

| Order | Writes |
|---|---|
| `0x4122`, `0x4156` | sets bit `parameter` |
| `0x4123`, `0x4157` | clears bit `parameter` |
| `0x4149` | sets the register to `parameter` |
| `0x4155` | adds `parameter` |

## Columns

`enemy-order-sets.tsv`, one row per set:

| Column | Meaning |
|---|---|
| `area_id`, `area` | the area number and its `.ard` name |
| `set` | the set's place in the area's directory |
| `orders` | how many orders it holds |
| `phase_counts` | the orders in phases 0, 1, 2 ..., up to the last phase that has one |
| `used_by` | each enemy definition that names it: its name, its row and, unless it is the starting list, which of lists 1-3 it is; `-` for none |

`enemy-orders.tsv`, one row per order:

| Column | Meaning |
|---|---|
| `area_id`, `area`, `set` | the set, as above |
| `phase`, `line` | the phase (subgroup 0-11) and the order's place in it |
| `action_id` | the word at `+0x00` |
| `action` | an action's name; a battle order with what it does ([Battle orders](../Battle-Actions/battle-orders.md)); or a weighted pick with each action's weight |
| `value` | the word at `+0x02`, read for the action (next list) |
| `flags` | the word at `+0x04` in hex, then a token per bit (next table) |
| `gambit_condition` | the gambit condition whose row gives exactly these three tests and these flags, when there is one ([Gambit conditions](gambit-conditions.md)) |
| `test1`-`test3` | each test in words: the relation (`Foe`, `Ally`, `Self`, `Any`, `Linked unit` for mode 3, `Same team`, `Other team`, `Own target`, `Issued target`), then the check; empty when the relation word is 0, which skips the test (`0x00301685`) |

The `value` column reads the word `+0x02` by action:

- an action: the percent chance the order is tried, `always` for 0: it is tried when
  `value` is 0 or `0x00328370() % 100 < (s16)value` (`0x00301608`-`0x00301637`);
- orders `0x4051`-`0x4121` except `0x4091`, and `0x414B`: the same percentage, checked by `0x00301830` with the
  same test, `value` 0 or `0x00328370() % 100 < (s16)value` (`0x0030193B`-`0x00301962`); 0 and 100 are `always`;
- the wait `0x4021`: seconds, `never ends` for 0 (`0x002FE7D0`);
- any other order: its parameter.

Both percentages, and the weighted pick, take a draw of the shared gameplay LCG modulo 100 (the calls at
`0x0030160F`, `0x0030193F` and `0x00308F61`; [Random number generators](../Random-Numbers/random-number-generators.md)).

| Token | Bits | Meaning | Site |
|---|---|---|---|
| `keep` | `0x8000` | the order in flight is not re-planned over | `0x0030873B` |
| `guard` | `0x4000` | while it is in flight, a resumed walk tries only `resume` orders | `0x00305D7F` |
| `sticky` | `0x1000` | when the deciding unit's `+0x744` is this action, the unit in its `+0x740` is taken as the only target | `0x00301B47`-`0x00301B72`, `0x00301E76`-`0x00301E88` |
| `no-repeat` | `0x800` | not tried while it is the unit's previous order | `0x003015A6` |
| `spread` | `0x400` | an enemy passes over a candidate three units are committed against (`+0xEA8`) | `0x00301B79`-`0x00301B9C`, `0x00301E8E`-`0x00301E9D` |
| `skip-resume` | `0x80` | skipped by a resumed walk | `0x00305DBC` |
| `resume` | `0x40` | tried by a resumed walk while a `guard` order is in flight | `0x00305DB2` |
| `chain-2`, `chain-3` | `0x20` with `0x10`, `0x10` with `0x08` | test 2 (or 3) keeps only what test 1 (or 2) kept | `0x003016BE`-`0x003016E0` |
| `bit-…` | `0x4`, `0x100`, `0x200`, `0x2000` | set in shipped orders; the walk `0x00305CC0`, the evaluator `0x003014C0`, the selector `0x00301AD0` and the combat frame `0x00308610` do not test them | - |

## Data

The two TSVs are written by `Database/Tools/catalogues/opus_enemy_orders.py` from the us `battle_pack.bin` and
the 166 area files of the kind-21 path list ([Bestiary](../Enemy-Spawning/bestiary.md)). It asserts
the slot layout of every file, the zero padding and exact length of every set, the sum of every weighted run and
the register kind of every opcode-54/55 test. Of the 50,050 orders, 3,336 carry exactly the tests and flags of a
gambit condition, and the tool's wording for those agrees with the condition's name.

## Related

- [Enemy AI](enemy-ai.md) - how a unit walks its order sets and switches lists and phases.
- [Gambits](gambits.md) - the walk, the evaluator, the order layout and the relation modes.
- [Gambit conditions](gambit-conditions.md) - the party's conditions, which run on the same selector.
- [Battle orders](../Battle-Actions/battle-orders.md) - every order id.
- [Bestiary](../Enemy-Spawning/bestiary.md) - the enemies, with the set numbers of their four lists.
- [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md) - the area file.
- [Enmity](enmity.md) - the enmity checks of opcodes 2 and 34.
