---
title: "Enemy order sets: every enemy's own order lists by area, each order's action, chance, flags and tests"
kind: "reference"
category: "Enemy AI and gambits"
addresses: "02EBF168, 02EBF160, 00301AD0, 003014C0, 00305CC0, 00308EC0, 00301830, 00321190, 002FE660, 0030BD00"
---

## What it lists

An enemy's own lists are order sets from its area file's directory slot 1, `[02EBF168]`
([Enemy AI](enemy-ai.md), [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)). The
166 shipped area files hold 1,422 sets with 50,050 orders between them:

- [the order sets](enemy-order-sets.tsv), one row per set: its order count, its phase counts and the enemies
  that use it;
- [the orders](enemy-orders.tsv), one row per order, in the order the walk `00305CC0` tries them.

Slot 1 opens with a `u16` count and a `u16` that is 100 in every file, then `count + 1` 32-bit offsets from the
section. Each set fills the bytes up to the next offset exactly: twelve phase counts, 20 zero bytes, then the
24-byte orders ([Gambits](gambits.md) has the order layout).

An enemy definition names its sets by four words: `+50`<sub>h</sub> is the list the unit starts with (`0023A94D`), and
`+50`<sub>h</sub>, `+52`<sub>h</sub>, `+54`<sub>h</sub> and `+56`<sub>h</sub> are lists 0-3, which orders `4112`<sub>h</sub>-`4115`<sub>h</sub> switch to (`002FE025`). Orders
`4116`<sub>h</sub>-`4121`<sub>h</sub> switch the phase, the subgroup of the set the walk starts in (`002FE0B3`).

### The weighted actions

An action word from `8000`<sub>h</sub> is an index into `[02EBF160]`, `battle_pack.bin` directory entry `+2C`<sub>h</sub>: a `u16`
count (826), then `count + 1` offsets from the section, each pair bounding a run of 4-byte entries (`u16` action,
`u8` weight, `u8` pad). Every shipped run's weights sum to 100. `00308EC0` draws `r = LCG % 100` and takes the
first entry whose running sum is above `r` (`00308F61`-`00308F99`).

### What a test can check

Each test is a relation word, a sub-selector byte `s`, an opcode byte and an `i16` operand `v` (order `+06`<sub>h</sub>,
`+08`<sub>h</sub>, `+09`<sub>h</sub>, `+0A`<sub>h</sub> for test 1, then every 6 bytes). `00301AD0` runs it over the candidates the relation
filter `0030BD00` admits; a relation above 10 admits none (`0030BD2A`). The opcode picks the check through the
jump tables `00303680`/`00303604` (`00301EA3`-`00301ECA`).

An even opcode keeps the units that pass and the next odd one the units that fail (`00301B44`). For a highest or
lowest check the even opcode takes the highest. A distance or angle check passes for the even opcode when the
value is below `v` ("within"), and for the odd one when it is `v` or more.

The distance of `s` = 7 is `0031E6F0`: the horizontal distance between the two units' positions `+E0`<sub>h</sub> less
each unit's collision radius, the larger of its two radii (the calls at `0031E70D` and `0031E718`), and never
below 0 (`0031E750`) ([Navigation](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)).

| Opcodes | Check | Site |
|---|---|---|
| 0 | any unit, picked at random | `00301ECC` |
| 2, 3 | highest / lowest of a value chosen by `s`: 0 attack power `+2E`<sub>h</sub>, 1 defense `+2F`<sub>h</sub>, 3 magick resist `+30`<sub>h</sub>, 4 HP, 5 MP, 6 level `+1C2`<sub>h</sub>, 7 distance (`0031E6F0`), 8 units committed against it `+EA8`<sub>h</sub>, 9 max HP, 10 max MP, 12-15 strength, magick power, vitality, speed (`+2A`<sub>h</sub>-`+2D`<sub>h</sub>), 17 the deciding unit's enmity toward it, party members only (`003215C0`; opcode 2 needs it above 0) | `00301EF7`, table `003036C8` |
| 6, 7 | status `s` (stats `+64`<sub>h</sub> or `+3C`<sub>h</sub>) | `003021A3` |
| 8, 9 | unit byte `+55`<sub>h</sub> is `s` (13 = undead) | `003021CC` |
| 10, 11 | unit type byte `+56`<sub>h</sub> is `s` (46 = flying) | `003021EC` |
| 12, 13 | bit `s` of unit word `+52`<sub>h</sub> | `003021F3` |
| 14, 15 | HP at least 90, 80, 70 ... 0 % of max HP for `s` = 0-9 (`00D102E0`) | `00302203` |
| 16, 17 | max HP at least 500, 1,000, 2,000, 5,000, 10,000, 20,000, 30,000, 50,000, 100, 200 (`00D10308`) | `003022FC` |
| 20, 21 | weak to element `s` (stats `+40`<sub>h</sub>) | `003023A5` |
| 22, 23 | absorbs element `s` (stats `+41`<sub>h</sub>) | `003023C9` |
| 24, 25 | party type `s` (stats word `+04`<sub>h</sub>; 255 stands for `FFFF`<sub>h</sub>) | `003023ED` |
| 26, 27 | equipment slot `s` (0-5) holds an item: stats word `+50h + 2s` is neither `FFFF`<sub>h</sub> nor `1000`<sub>h</sub> | `00302416` |
| 28, 29 | the weapon's motion class is `s` (byte `+26`<sub>h</sub> of its equipment row, through `00321320`) | `00302451` |
| 32, 33 | effect bit `s` at stats `+68`<sub>h</sub> or `+78`<sub>h</sub> ([Augments](../Damage-And-Battle-Formulas/augments.md)) | `00302478` |
| 34, 35 | one of 23 checks chosen by `s` (next table) | `003024B0`, table `00303710` |
| 36, 37 | within `v` of field point `s + 1` (`00320940`) | `00302C8F` |
| 38, 39 | within `v` of the unit of definition selector `s` (`002367A0`) | `00302D1F` |
| 40, 41 | HP missing at least 100, 200, 300, 500, 700, 1,000, 2,000, 3,000, 4,000, 5,000 (`00D10328`) | `00302DB4` |
| 42, 43 | HP at least 100,000, 50,000, 10,000, 5,000, 3,000, 2,000, 1,000, 500, 75, 50 (`00D10350`) | `00302E80` |
| 44, 45 | MP at least 75, 50, 25 or 10 % of max MP (`00D10370`); a unit with max MP 0 fails | `00302F17` |
| 46, 47 | `s` = 0: HP full; `s` = 1: MP full | `00302F7E` |
| 48, 49 | the whole field, read at the first candidate: `s` = 0 the environment class (`00321490`) is `v`, 1 the MP regime (`00320160`) is `v`, 2 the MP regime is at least `v` | `00303027` |
| 52, 53 | before any candidate: every active enemy whose spawn record tag `+15`<sub>h</sub> is `v` (1-255) and that no unit is committed against (`+EA4`<sub>h</sub> = 0) | `00301CFB`-`00301DAB` |
| 54, 55 | before any candidate, for `s` = 0-2: a register (next tables) equal to `v`, at least `v`, or with bit `v` set; a pass keeps the deciding unit. `s` = 3 runs the candidates instead and tests bit `v` of each one's register `+B90`<sub>h</sub> | `00301C2B`-`00301CF6`, `00303079` |
| 56, 57 | `s` = 0: on screen (`00322360`), nearest for 56 and furthest for 57; 1: the party leader's target (`+750`<sub>h</sub>); 2: carrying out a magick (its action's kind `+1E`<sub>h</sub> is 1) | `003030A7` |
| 58, 59 | at least `v` units that relation mode `s` admits (0 = every unit) in its own perception list `+BC4`<sub>h</sub> | `003031C4` |
| 60, 61 | team byte `+54`<sub>h</sub> is `v` | `0030329B` |
| 62, 63 | MP at least `10 * s` % of max MP | `003032A7` |
| 64, 65 | the deciding unit holds at least `10 * s` of the line's item (`003093D0`, `00309EC0`, read at the first candidate), or the candidate is an enemy | `003032C0` |
| 66, 67 | a unit committed against it (`+EA4`<sub>h</sub>) carries: `s` = 0 the same action; 1 an action removing a status it has that this action also removes (`0031C500`); 2 an action restoring HP (`+2C`<sub>h</sub> bit 12); 3 one restoring MP (bit 15) | `00303334` |
| 68, 69 | the whole field: the summon timer (battle state `+5AD8`<sub>h</sub>) at least 20, 30, 60, 90 or 120 (`00D10380`) | `00303523` |
| 1, 4, 5, 18, 19, 30, 31, 50, 51 | no unit is kept | `00301C08`, `00303567` |

An active enemy of opcodes 52 and 53, and a party slot of check 18 below, counts only while it is in play: a
unit whose status words `+3Ch | +64h` hold KO, Stone or X-Zone (`80000003`<sub>h</sub>) is passed over unless the area's
town flag is set (the calls at `00301D4E` and `00302738`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

The checks of opcodes 34 and 35:

| `s` | Check | Site |
|---|---|---|
| 0 | linked to a unit: `+24`<sub>h</sub> is not 0 | `003024C8` |
| 1 | the party leader (`003273B0`) | `003024DA` |
| 2 | its own linked unit (`+08`<sub>h</sub> = `+24`<sub>h</sub>) | `003024F0` |
| 3 | a guest: a party record of type 7-25 | `003024FD` |
| 4 | a party record of type 27-39 | `00302537` |
| 8 | its highest enmity toward an active party member is at least `v` (`00321630`) | `0030255D` |
| 9-12 | a unit in its own perception list whose team byte `+54`<sub>h</sub> is `v` (9), with status `v` (10), whose byte `+55`<sub>h</sub> is `v` (11), or whose byte `+56`<sub>h</sub> is `v` (12) | `003025B6` |
| 13 | an enemy whose definition row byte `+03`<sub>h</sub> has bit `10`<sub>h</sub> | `0030266C` |
| 16 | level `+1C2`<sub>h</sub> at least `v` | `00302696` |
| 17 | within `v` of the point at `+50`<sub>h</sub> of the deciding enemy's spawn record (the deciding unit must be an enemy) | `0030282B` |
| 18 | 34: within `v` of the nearest of party slots 0-3; 35: `v` or more from the furthest | `003026EC` |
| 19, 20 | within `v` of the party leader (19) or of the deciding unit's linked unit (20) | `003028C2`, `00302945` |
| 21 | the party leader within `v` degrees of its facing | `003029C7` |
| 24, 25, 26 | targeting (`+710`<sub>h</sub>) the deciding unit's linked unit, the deciding unit, or one of the deciding unit's allies | `00302A76`, `00302A98`, `00302AB1` |
| 27 | targeting combatant `v` | `00302AE3` |
| 28, 29 | within `v` degrees of the deciding unit's facing (28) or within `v` of the deciding unit (29) | `00302B18`, `00302BC0` |
| 30, 31 | a status of set A `0208D320` other than bit 29 (30), or of set B `0208D324` (31) | `00302C35`, `00302C59` |
| 32 | holding a bow, crossbow, gun or hand-bomb (equipment class 7, 8, 9 or 17, group 4 of `0031E9F0`) | `00302C77` |
| 5-7, 14, 15, 22, 23 | no unit is kept | `00303567` |

### The registers

A register is named by a kind and an index: kind = relation word `>> 12`, index = its low byte. `00321190` reads
it (`003211A4`-`003211B8`) and `00329E60` writes it:

| Kind | Register | Reader |
|---|---|---|
| 1 | word `i` of the 64-word field table `[02098E68]` (word 3 is the group-defeated signal, [Boss fights](../Battle-Actions/boss-fights.md)) | `00264D20` |
| 2 | word `i` of the 32-word table `[02098E70]` | `00264800` |
| 3 | story word `i` of `[02098E58]`, 256 words ([Story progress](../Story-Events-And-Hunts/story-progress.md)) | `00264640` |
| 4, 5 | quest `i` ordered, quest `i` cleared ([Quests](../Story-Events-And-Hunts/quests.md)) | `0046B240`, `0046B1A0` |
| 6 | quest `i`'s progress byte, save `+1064`<sub>h</sub> | `0046B180` |
| 7 | quest `i`'s contract word, save `+1164`<sub>h</sub> | `0046B0D0` |
| 8 | story flag `i` ([Story flags](../Story-Events-And-Hunts/story-flags.md)) | `0032A920` → `0032A8A0` |
| 9 | battle word `i` of the sixteen at `0208D334`, zeroed when an area starts | `00321253` |
| 10 | the unit's own register `+B90`<sub>h</sub> (index 0) | `0032126F` |

The orders that write a register (`002FE660`) take it from the order's own test-1 relation word, except
`4122`<sub>h</sub> and `4123`<sub>h</sub>, which write the `+B90`<sub>h</sub> of the unit in the deciding unit's `+710`<sub>h</sub>:

| Order | Writes |
|---|---|
| `4122`<sub>h</sub>, `4156`<sub>h</sub> | sets bit `parameter` |
| `4123`<sub>h</sub>, `4157`<sub>h</sub> | clears bit `parameter` |
| `4149`<sub>h</sub> | sets the register to `parameter` |
| `4155`<sub>h</sub> | adds `parameter` |

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
| `action_id` | the word at `+00`<sub>h</sub> |
| `action` | an action's name; a battle order with what it does ([Battle orders](../Battle-Actions/battle-orders.md)); or a weighted pick with each action's weight |
| `value` | the word at `+02`<sub>h</sub>, read for the action (next list) |
| `flags` | the word at `+04`<sub>h</sub> in hex, then a token per bit (next table) |
| `gambit_condition` | the gambit condition whose row gives exactly these three tests and these flags, when there is one ([Gambit conditions](gambit-conditions.md)) |
| `test1`-`test3` | each test in words: the relation (`Foe`, `Ally`, `Self`, `Any`, `Linked unit` for mode 3, `Same team`, `Other team`, `Own target`, `Issued target`), then the check; empty when the relation word is 0, which skips the test (`00301685`) |

The `value` column reads the word `+02`<sub>h</sub> by action:

- an action: the percent chance the order is tried, `always` for 0: it is tried when
  `value` is 0 or `00328370() % 100 < (s16)value` (`00301608`-`00301637`);
- orders `4051`<sub>h</sub>-`4121`<sub>h</sub> except `4091`<sub>h</sub>, and `414B`<sub>h</sub>: the same percentage, checked by `00301830` with the
  same test, `value` 0 or `00328370() % 100 < (s16)value` (`0030193B`-`00301962`); 0 and 100 are `always`;
- the wait `4021`<sub>h</sub>: seconds, `never ends` for 0 (`002FE7D0`);
- any other order: its parameter.

Both percentages, and the weighted pick, take a draw of the shared gameplay LCG modulo 100 (the calls at
`0030160F`, `0030193F` and `00308F61`; [Random number generators](../Random-Numbers/random-number-generators.md)).

| Token | Bits | Meaning | Site |
|---|---|---|---|
| `keep` | `8000`<sub>h</sub> | the order in flight is not re-planned over | `0030873B` |
| `guard` | `4000`<sub>h</sub> | while it is in flight, a resumed walk tries only `resume` orders | `00305D7F` |
| `sticky` | `1000`<sub>h</sub> | when the deciding unit's `+744`<sub>h</sub> is this action, the unit in its `+740`<sub>h</sub> is taken as the only target | `00301B47`-`00301B72`, `00301E76`-`00301E88` |
| `no-repeat` | `800`<sub>h</sub> | not tried while it is the unit's previous order | `003015A6` |
| `spread` | `400`<sub>h</sub> | an enemy passes over a candidate three units are committed against (`+EA8`<sub>h</sub>) | `00301B79`-`00301B9C`, `00301E8E`-`00301E9D` |
| `skip-resume` | `80`<sub>h</sub> | skipped by a resumed walk | `00305DBC` |
| `resume` | `40`<sub>h</sub> | tried by a resumed walk while a `guard` order is in flight | `00305DB2` |
| `chain-2`, `chain-3` | `20`<sub>h</sub> with `10`<sub>h</sub>, `10`<sub>h</sub> with `08`<sub>h</sub> | test 2 (or 3) keeps only what test 1 (or 2) kept | `003016BE`-`003016E0` |
| `bit-…` | `4`<sub>h</sub>, `100`<sub>h</sub>, `200`<sub>h</sub>, `2000`<sub>h</sub> | set in shipped orders; the walk `00305CC0`, the evaluator `003014C0`, the selector `00301AD0` and the combat frame `00308610` do not test them | - |

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
