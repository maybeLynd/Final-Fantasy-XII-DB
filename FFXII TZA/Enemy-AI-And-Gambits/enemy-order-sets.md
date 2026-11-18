[Home](../../README.md) / [Enemy AI and gambits](README.md) / Enemy order sets

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Enemy order sets: every enemy's own order lists by area, each order's action, chance, flags and tests | reference | Enemy AI and gambits | Enemy decisions | Every order set of the shipped area files (.ard directory slot 1) with the enemies that use it, and every order in each set by phase: the action, battle order or weighted pick it carries, its chance or parameter, its flag bits by name, the gambit condition it matches when it matches one, and its three tests in words, with the full vocabulary of tests the selector 0x00301AD0 can run, the registers an order can read and write, and the weighted action table. | 0x02EBF168, 0x02EBF160, 0x00301AD0, 0x003014C0, 0x00305CC0, 0x00308EC0, 0x00301830, 0x00321190, 0x002FE660, 0x0030BD00 |

## What it lists

An enemy's own lists are order sets from its area file's directory slot 1, `[0x02EBF168]`
([Enemy AI](enemy-ai.md), [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)). The
166 shipped area files hold 1,422 sets with 50,050 orders between them; four of the files (`asp_a`, `dor_f`,
`mrm_a` and `slm_a`) have a set count of 0, so the sets come from 162 areas:

- [the order sets](enemy-order-sets.tsv), one row per set: its order count, its phase counts and the enemies
  that use it;
- [the orders](enemy-orders.tsv), one row per order, in the order the walk `0x00305CC0` tries them.

Slot 1 opens with a `u16` count and a `u16` that is 100 in every file, then `count + 1` 32-bit offsets from the
section. Each set fills the bytes up to the next offset exactly: twelve phase counts, 20 zero bytes, then the
24-byte orders ([Gambits](gambits.md) has the order layout).

An enemy definition names its sets by four words: `+0x50` is the list the unit starts with¹, and
`+0x50`, `+0x52`, `+0x54` and `+0x56` are lists 0-3, which orders `0x4112`-`0x4115` switch to². Orders
`0x4116`-`0x4121` switch the phase, the subgroup of the set the walk starts in³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A94D` |
| ² | `0x002FE025` |
| ³ | `0x002FE0B3` |

</details>

### The weighted actions

An action word from `0x8000` is an index into `[0x02EBF160]`, `battle_pack.bin` directory entry `+0x2C`: a `u16`
count (826) and a `u16` 0, then from `+4` `count + 1` 32-bit offsets from the section (`0x00308F2F` reads entry `i`
at `+4 + 4i`), each pair bounding a run of 4-byte entries (`u16` action, `u8` weight, `u8` pad). Every shipped
run's weights sum to 100.

`0x00308EC0` draws `r = LCG % 100` and takes the first entry whose running sum is above `r`¹.
A word whose index is not below the count comes back unchanged², and a run with no such
entry gives `0xFFFF`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308F61`-`0x00308F99` |
| ² | `0x00308EF0`-`0x00308EFA` |
| ³ | `0x00308FA4` |

</details>

The loader adds the section's address to all `count + 1` offsets (`0x00236D39`, `0x00384780`, bound at `0x0038478B`).
[`enemy-weighted-pools.tsv`](enemy-weighted-pools.tsv) lists the 826 pools and
[`enemy-weighted-pool-members.tsv`](enemy-weighted-pool-members.tsv) their 3,587 members, with raw action ids,
weights and pad bytes.

Pools 0-16, 37, 75, 137, 228, 229, 382-385, 388, 389, 525 and 590 are Reserve. None of the 50,050 orders of the 166
area files names one of them, in the `in` or the `ch` folder, and the index test at `0x00308EF0`-`0x00308EFA` accepts
each.

A member of weight 0 is never taken: the running sum does not rise at it and the roll is at least 0¹. Six pools hold 679 such members, each with action word `0x0000`, and 667 of them are in
pool 312, which has 676 members.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308F94`-`0x00308F99` |

</details>

So an order in an area file can point to a weighted list instead of a single action. These lists are kept in
`battle_pack.bin`, each list's weights add up to 100, and the game rolls a number from 0 to 99 and takes the first
action whose running total of weights is above the roll.

### What a test can check

Each test is a relation word, a sub-selector byte `s`, an opcode byte and an `i16` operand `v` (order `+0x06`,
`+0x08`, `+0x09`, `+0x0A` for test 1, then every 6 bytes). `0x00301AD0` runs it over the candidates the relation
filter `0x0030BD00` admits; a relation above 10 admits no candidate¹. The opcode picks the check through the
jump tables `0x00303680`/`0x00303604`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030BD2A` |
| ² | `0x00301EA3`-`0x00301ECA` |

</details>

An even opcode keeps the units that pass and the next odd one the units that fail¹. For a highest or
lowest check the even opcode takes the highest. A distance or angle check passes for the even opcode when the
value is below `v` ("within"), and for the odd one when it is `v` or more.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301B44` |

</details>

The distance of `s` = 7 is `0x0031E6F0`: the horizontal distance between the two units' positions `+0xE0` less
each unit's collision radius, the larger of its two radii (the calls at `0x0031E70D` and `0x0031E718`), and never
below 0¹ ([Navigation](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031E750` |

</details>

| Opcodes | Check | Site |
|---|---|---|
| 0 | any unit, picked at random | `0x00301ECC` |
| 2, 3 | highest / lowest of a value chosen by `s`: 0 attack power `+0x2E`, 1 defense `+0x2F`, 3 magick resist `+0x30`, 4 HP, 5 MP, 6 level `+0x1C2`, 7 distance (`0x0031E6F0`), 8 units committed against it `+0xEA8`, 9 max HP, 10 max MP, 12-15 strength, magick power, vitality, speed (`+0x2A`-`+0x2D`), 17 the deciding unit's enmity toward it, party members only (`0x003215C0`; opcode 2 needs it above 0) | `0x00301EF7`, table `0x003036C8` |
| 6, 7 | status `s` (stats `+0x64` or `+0x3C`) | `0x003021A3` |
| 8, 9 | unit byte `+0x55` is `s` (13 = undead) | `0x003021CC` |
| 10, 11 | unit type byte `+0x56` is `s` (46 = flying) | `0x003021EC` |
| 12, 13 | bit value `1 << s` of unit word `+0x52` | `0x003021F3` |
| 14, 15 | HP (`0x00308C20` with a last argument of 1) at least 90, 80, 70 ... 0 % for `s` = 0-9 (`0x00D102E0`) of the cap of opcodes 46 and 47: max HP `+0x24`, or `2 × +0x24` with status bit `0x10000000`, or with status bit `0x10000` the current HP `+0x48`, at least 1 (`0x00302223`-`0x00302295`); a unit whose cap is 0 is kept by neither opcode (`0x00302251`-`0x00302253`) | `0x00302203` |
| 16, 17 | the cap of opcodes 46 and 47 (`0x0030231C`-`0x0030234A`) at least 500, 1,000, 2,000, 5,000, 10,000, 20,000, 30,000, 50,000, 100, 200 (`0x00D10308`) | `0x003022FC` |
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
| 44, 45 | MP at least 75, 50, 25 or 10 % of max MP (`0x00D10370`); a unit with max MP 0, or with bit `0x80` in stats byte `+0x6C` or `+0x7C`, is kept by neither opcode (`0x00302F3E`-`0x00302F59`) | `0x00302F17` |
| 46, 47 | `s` = 0: HP (`0x00308C20` with a last argument of 1) at least the cap: max HP `+0x24`, or `2 × +0x24` with status bit `0x10000000`, or with status bit `0x10000` the current HP `+0x48`, at least 1 (`0x00302FAF`-`0x00302FE2`). `s` = 1: MP at least max MP `+0x28`, or at least 0, which always holds, when byte `+0x6C` or `+0x7C` of the stats has bit `0x80` (`0x00302F8B`-`0x00302FA7`). Any other `s` keeps no unit (`0x00302F82`-`0x00302F85`) | `0x00302F7E` |
| 48, 49 | the whole field, read at the first candidate: `s` = 0 the environment class (`0x00321490`) is `v`, 1 the MP regime (`0x00320160`) is `v`, 2 the MP regime is at least `v` | `0x00303027` |
| 52, 53 | before any candidate: every active enemy whose spawn record tag `+0x15` is `v` (1-255) and that no unit is committed against (`+0xEA4` = 0) | `0x00301CFB`-`0x00301DAB` |
| 54, 55 | before any candidate, for `s` = 0-2: a register (next tables) equal to `v`, at least `v`, or with bit value `1 << v` set; a pass keeps the deciding unit. `s` = 3 runs the candidates instead and tests bit value `1 << v` of each one's register `+0xB90` | `0x00301C2B`-`0x00301CF6`, `0x00303079` |
| 56, 57 | `s` = 0: on screen (`0x00322360`), nearest for 56 and furthest for 57; 1: the target (`+0x750`) of the deciding unit's linked unit, the unit `0x0031B7E0` gives for its `+0x24`; with no linked unit, or with a linked unit other than the deciding unit whose action word `+0x714` is above `0x21E`, neither opcode keeps a unit (`0x00303141`-`0x00303180`); 2: carrying out a magick (its action word `+0x714` is at most `0x21E` and the action's kind `+0x1E` is 1, `0x003030C3`-`0x00303130`) | `0x003030A7` |
| 58, 59 | at least `v` units that relation mode `s` admits (0 = every unit) in its own perception list `+0xBC4` | `0x003031C4` |
| 60, 61 | team byte `+0x54` is `v` | `0x0030329B` |
| 62, 63 | MP at least `10 * s` % of max MP, through the code of opcodes 44 and 45 from `0x00302F37` (`0x003032AF`-`0x003032BB`), so with the same two kinds of unit kept by neither opcode | `0x003032A7` |
| 64, 65 | the party holds at least `10 * s` of the line's item (`0x003093D0`, `0x00309EC0`, read at the first candidate), or the candidate is an enemy | `0x003032C0` |
| 66, 67 | a unit committed against it (`+0xEA4`) carries: `s` = 0 the same action; 1 an action removing a status it has that this action also removes (`0x0031C500`); 2 an action restoring HP (`+0x2C` bit `0x1000`); 3 one restoring MP (bit `0x8000`) | `0x00303334` |
| 68, 69 | the whole field: the summon timer (battle state `+0x5AD8`) at least 20, 30, 60, 90 or 120 (`0x00D10380`) | `0x00303523` |
| 1, 4, 5, 18, 19, 30, 31, 50, 51 | no unit is kept | `0x00301C08`, `0x00303567` |

`0x00321320(unit, out)` first stores -1 in the output dword, and again at `0x0032134D`. It
answers -1 for a null unit and -2 for a unit with no stats record `+0x698`; otherwise it
calls `0x00321400(word +0x50 of the stats record, out)` and answers 0¹. The branch at `0x00321357`, taken only if the address of that
word were 0, answers -3².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321324`-`0x00321361` |
| ² | `0x00321368` |

</details>

An active enemy of opcodes 52 and 53, and a party slot of check 18 below, counts only while it is in play: a
unit whose status words `+0x3C | +0x64` hold KO, Stone or X-Zone¹ is passed over unless the area's
town flag is set (the calls at `0x00301D4E` and `0x00302738`, [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x80000003` |

</details>

Before the candidates `0x00301AD0` asks `0x003272A0()` and, when the deciding unit's `+0x24`
is not 0, `0x0031B7E0` for that unit¹. A candidate is taken with
`0x0031B760` from the list entry, must pass `0x0030BD00` and must not pass `0x0030B9B0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301BA7`-`0x00301BB9` |
| ² | `0x00301E1E`-`0x00301E68` |

</details>

For opcodes 52 and 53 the walk is over `0x00236820(i)` for `i` below `0x00236850()`, asked
again at every step¹. An enemy is kept when it holds bit `0x10` in
its first byte, has a stats record `+0x698`, passes `0x00377C20()` when that record's dwords
`+0x64` and `+0x3C` hold a bit of `0x80000003`, has byte `+5` of the stats record equal to
1, holds bit `0x10` in the first byte of its record `+0x6A0`, has that record's tag `+0x15`
equal to `v` and has a dword `+0xEA4` of 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301D0E`-`0x00301DA5` |
| ² | `0x00301D30`-`0x00301D84` |

</details>

The qword `+0x10` of a kept enemy is added to the list and the list's count `+4` goes up
by 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301D86`-`0x00301D96` |

</details>

For opcodes 40 and 41 the HP missing is the cap of opcodes 46 and 47 (max HP `+0x24`,
or `2 × +0x24` with status bit `0x10000000`, or the current HP `+0x48`, at least 1, with
status bit `0x10000`) less the answer of `0x00308C20`¹. Opcodes 42 and 43
compare that answer itself².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00302DD4`-`0x00302E23` |
| ² | `0x00302EA0`-`0x00302EBF` |

</details>

For opcodes 48 and 49 an `s` above 2 ends the test with no unit kept¹. For opcodes 58 and 59 an `s` of 0 takes the count `+0xBC4` as it stands²; any other `s` counts the list units `0x0030BD00`
admits in mode `s`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030303A`-`0x0030303D` |
| ² | `0x003031E3`-`0x003031E5`, `0x00303292` |
| ³ | `0x003031EB`-`0x0030322E` |

</details>

For opcodes 64 and 65 the item is `0x003093D0` of the line's action word and the count
`0x00309EC0(item, 0)`, both taken at the first candidate¹; the
answer is kept in the dword `0x022BED94` for the later candidates².
An item of `0xFFFF` passes over the first candidate without writing `0x022BED94`³, and the later candidates are judged by the value it already
held.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003032C4`-`0x003032E4` |
| ² | `0x003032F8`-`0x00303300` |
| ³ | `0x003032D6`-`0x003032D9` |

</details>

For opcodes 66 and 67 a committed unit is `0x00236820(i)` for a set bit `i` of the
candidate's `+0xEA4`, when its qword `+0x780` equals the candidate's `+0x10` and
`0x00322C50(0x14, action, 0)` answers non-zero for its action word `+0x714`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00303380`-`0x003033C8` |

</details>

For `s` = 1 of opcodes 66 and 67 `0x0031C500` is asked twice: for the deciding unit's
stats, the candidate's stats and the line's action¹, and for the
committed unit's stats, the candidate's stats and that unit's action²; the two status masks it answers must share a set bit³. With an `s` above 3 no committed unit passes: opcode 66 keeps no unit and
opcode 67 keeps every candidate⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030333F`-`0x0030335B` |
| ² | `0x003034AD`-`0x003034C4` |
| ³ | `0x003034CB` |
| ⁴ | `0x003033E8`-`0x003033EB`, `0x003034FF`-`0x0030351E` |

</details>

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
| 30, 31 | a status of set A `0x0208D320` other than bit `0x20000000` (30), or of set B `0x0208D324` (31) | `0x00302C35`, `0x00302C59` |
| 32 | holding a bow, crossbow, gun or hand-bomb (equipment class 7, 8, 9 or 17, group 4 of `0x0031E9F0`) | `0x00302C77` |
| 5-7, 14, 15, 22, 23 | no unit is kept | `0x00303567` |

A check that needs a unit which is absent ends the whole test with no unit kept: no
party leader for checks 19 and 21¹, no
linked unit for checks 20 and 24² and no
combatant `v` from `0x0031B770` for check 27³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003028C2`-`0x003028CA`, `0x003029C7`-`0x003029CF` |
| ² | `0x00302945`-`0x0030294A`, `0x00302A76`-`0x00302A7E` |
| ³ | `0x00302AE7`-`0x00302AFA` |

</details>

The same end is taken by opcodes 36 and 37 when `0x00320940` answers below 0¹, by opcodes 38 and 39 when `0x002367A0(s)` gives no unit² and by opcodes 26 and 27 for an `s` above 5³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00302C9D`-`0x00302CA4` |
| ² | `0x00302D25`-`0x00302D34` |
| ³ | `0x00302416`-`0x00302419` |

</details>

Check 27 asks `0x0031B770` for combatant `v` at the first candidate and keeps the answer
in the qword `0x022BED98`¹; opcodes 38 and 39 keep theirs in
`0x022C17A8`². Check 26 passes when `0x0030AB40(deciding unit, target, 0)`
answers a value other than 0 and 2, the target being `0x0031B7E0` of the candidate's dword
`+0x710`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00302AE3`-`0x00302AF0` |
| ² | `0x00302D2A` |
| ³ | `0x00302AB1`-`0x00302AD8` |

</details>

### The registers

A register is named by a kind and an index: kind = relation word `>> 12`, index = its low byte. `0x00321190` reads it¹ and `0x00329E60` writes it: kinds 6 and 7, whose entries in the table at `0x00329F40` lead to
`0x00329F38`, and any kind outside 1-10² write nothing and return -1³;
kind 9 with an index above 15 and kind 10 with a null unit or an index other than 0 write nothing and return 0⁴:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003211A4`-`0x003211B8` |
| ² | `0x00329E64`-`0x00329E69` |
| ³ | `0x00329F38`-`0x00329F3F` |
| ⁴ | `0x00329F03`-`0x00329F37` |

</details>

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

`0x00321190(kind, unit, index, &value)` returns 0 with the value. Kinds 1-3 give their word sign-extended¹ and kind 9 its word zero-extended². Kind 9 with an index above
15, and kind 10 with a null unit or an index other than 0, give 0³. Any other kind gives 0
and returns -1⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003211C2`, `0x003211D7`, `0x003211EC` |
| ² | `0x0032125C` |
| ³ | `0x00321253`-`0x00321290` |
| ⁴ | `0x0032119B`, `0x0032129B`-`0x003212A0` |

</details>

The orders that write a register¹ take it from the order's own test-1 relation word, except
`0x4122` and `0x4123`, which write the `+0xB90` of the unit in the deciding unit's `+0x710`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FE660` |

</details>

| Order | Writes |
|---|---|
| `0x4122`, `0x4156` | sets bit value `1 << (parameter & 31)` (`bts`, `0x002FE732`) |
| `0x4123`, `0x4157` | clears bit value `1 << (parameter & 31)` (`btr`, `0x002FE73D`) |
| `0x4149` | sets the register to `parameter` (`0x002FE71A`) |
| `0x4155` | adds `parameter` (`0x002FE723`) |

`0x002FE660(unit)` acts only while the unit's phase byte `+0x6B4` is 0, and returns 1 at once in a later phase¹. For `0x4122` and `0x4123` the register is kind 10, index 0, of the unit `0x0031B7E0` finds for the
deciding unit's handle `+0x710`². It reads the register with `0x00321190` and returns -1,
writing nothing, when that returns -1³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FE69D` |
| ² | `0x002FE6C4`-`0x002FE6D7` |
| ³ | `0x002FE6EE` |

</details>

It then changes the value as the table above says, with `parameter` the order's `(s16)` word `+0x02`¹,
writes it back with `0x00329E60`, whose answer it does not test, sets the phase to 2 and returns 1². The orders `0x4124`-`0x4154` that are not in the table return -1 after the read³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FE68D` |
| ² | `0x002FE74E`-`0x002FE757` |
| ³ | `0x002FE6F8`, `0x002FE75E` |

</details>

## Columns

[`enemy-order-sets.tsv`](enemy-order-sets.tsv), one row per set:

| Column | Meaning |
|---|---|
| `area_id`, `area` | the area number and its `.ard` name |
| `set` | the set's place in the area's directory |
| `orders` | how many orders it holds |
| `phase_counts` | the orders in phases 0, 1, 2 ..., up to the last phase that has one |
| `used_by` | each enemy definition that names it: its name, its row and, unless it is the starting list, which of lists 1-3 it is; `-` when no definition names it |

[`enemy-orders.tsv`](enemy-orders.tsv), one row per order:

| Column | Meaning |
|---|---|
| `area_id`, `area`, `set` | the set, as above |
| `phase`, `line` | the phase (subgroup 0-11) and the order's place in it |
| `action_id` | the word at `+0x00` |
| `action` | an action's name; a battle order with what it does ([Battle orders](../Battle-Actions/battle-orders.md)); or a weighted pick with each action's weight |
| `value` | the word at `+0x02`, read for the action (next list) |
| `flags` | the word at `+0x04` in hex, then a token per bit (next table) |
| `gambit_condition` | the gambit condition whose row gives exactly these three tests and these flags, when there is one ([Gambit conditions](gambit-conditions.md)) |
| `test1`, `test2`, `test3` | the three tests of the order, one column each, in words: the relation (`Foe`, `Ally`, `Self`, `Any`, `Linked unit` for mode 3, `Same team`, `Other team`, `Own target`, `Issued target`), then the check; empty when the relation word is 0, which skips the test (`0x00301685`) |

The `value` column reads the word `+0x02` by action:

- an action: the percent chance the order is tried, `always` for 0: it is tried when
  `value` is 0 or `0x00328370() % 100 < (s16)value`¹;
- orders `0x4051`-`0x4121` except `0x4091`, and `0x414B`: the same percentage, checked by `0x00301830` with the
  same test, `value` 0 or `0x00328370() % 100 < (s16)value`²; 0 and 100 are `always`;
- the wait `0x4021`: seconds, `never ends` for 0³;
- any other order: its parameter.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00301608`-`0x00301637` |
| ² | `0x0030193B`-`0x00301962` |
| ³ | `0x002FE7D0` |

</details>

Both percentages, and the weighted pick, take a draw of the shared gameplay LCG modulo 100 (the calls at
`0x0030160F`, `0x0030193F` and `0x00308F61`; [Random number generators](../Random-Numbers/random-number-generators.md)).

| Token | Bits | Meaning | Site |
|---|---|---|---|
| `keep` | `0x8000` | the order in flight is not re-planned over, and its time-out is 60 times the time-out factor instead of 30 (10 for an action id above `0x21E`) ([Target selection](../Battle-Actions/target-selection.md)) | `0x0030873B`, `0x0030AF49` |
| `guard` | `0x4000` | while it is in flight, a resumed walk tries only `resume` orders | `0x00305D7F` |
| `sticky` | `0x1000` | when the deciding unit's `+0x744` is this action, the unit in its `+0x740` is taken as the only target | `0x00301B47`-`0x00301B72`, `0x00301E76`-`0x00301E88` |
| `no-repeat` | `0x800` | not tried while it is the unit's previous order `+0x738`; an action id outside the order band only when the previous command's `+0x730` has bit `0x1`, set when its state step finished with result 1 ([Enemy AI](enemy-ai.md), [Gambits](gambits.md)) | `0x003015A6`-`0x003015C9` |
| `spread` | `0x400` | an enemy passes over a candidate three units are committed against (`+0xEA8`) | `0x00301B79`-`0x00301B9C`, `0x00301E8E`-`0x00301E9D` |
| `skip-resume` | `0x80` | skipped by a resumed walk | `0x00305DBC` |
| `resume` | `0x40` | tried by a resumed walk while a `guard` order is in flight | `0x00305DB2` |
| `chain-2`, `chain-3` | `0x20` with `0x10`, `0x10` with `0x08` | test 2 (or 3) keeps only what test 1 (or 2) kept | `0x003016BE`-`0x003016E0` |
| `bit-…` | `0x2000` | the order in flight is never timed out: the cancel check `0x002FFB60` skips the time-out `0x0030AF30` (its reason 7) while the bit is set | `0x002FFCA5`-`0x002FFCB5` |
| `bit-…` | `0x4`, `0x100`, `0x200` | set in shipped orders; the walk `0x00305CC0`, the evaluator `0x003014C0`, the selector `0x00301AD0`, the combat frame `0x00308610`, the cancel check `0x002FFB60` and the time-out `0x0030AF30` do not test them | - |

`bit-…` is a single token for the bits this table does not name, written as their sum in hex: `bit-0x2000`,
`bit-0x2200`.

The ARD editor of The Insurgent's Toolkit, a community modding tool, has its own names for the bits below. They are
given here as aliases, credited to that tool, so that its users can find each bit; what each bit does is read from
the executable, at the sites above:

| Toolkit name | Token | Bits |
|---|---|---|
| `caseLinkType` | `chain-2`, `chain-3` | `0x38` |
| `noInterruptToLowerPriority` | `skip-resume` | `0x80` |
| `noTargetWith3Attackers` | `spread` | `0x400` |
| `noConsecutiveUse` | `no-repeat` | `0x800` |
| `noRetargeting` | `sticky` | `0x1000` |
| `noTimeout` | `bit-0x2000` | `0x2000` |
| `noInterruptByHigherPriority` | `guard` | `0x4000` |
| `noInterruptByAny` | `keep` | `0x8000` |

[`enemy-weighted-pools.tsv`](enemy-weighted-pools.tsv), one row per pool:

| Column | Meaning |
|---|---|
| `pool` | the index a word from `0x8000` carries |
| `action_word` | `0x8000 + pool`, the word an order holds |
| `section_offset` | where the pool's first member starts, from the section |
| `bytes`, `members` | the run's length and how many 4-byte members it holds |
| `weight_sum` | the sum of its weights |
| `zero_weight_members` | how many of its members have weight 0 |
| `orders`, `sets` | how many orders of the 166 area files hold its word, and in how many sets |
| `used_in` | those sets, each as `area:set`; `none` when no order holds the word |

[`enemy-weighted-pool-members.tsv`](enemy-weighted-pool-members.tsv), one row per member:

| Column | Meaning |
|---|---|
| `pool`, `member` | the pool and the member's place in it |
| `section_offset` | the member's offset from the section |
| `action_id` | the `u16` at `+0`, raw |
| `action` | that action's name |
| `weight` | the `u8` at `+2` |
| `pad` | the `u8` at `+3` |

## Data

The order TSVs hold the order sets of the `us` `battle_pack.bin` and of the 166 area files of the kind-21 path list
([Bestiary](../Enemy-Spawning/bestiary.md)). Every file has the slot layout above, and every set has
its zero padding and fills its length exactly. Of the 50,050 orders, 3,336 carry exactly the tests and flags of a
gambit condition, and the TSV's wording for those agrees with the condition's name.

The pool TSVs hold directory entry `+0x2C` of the `us` `battle_pack.bin`: 17,664 bytes at file offset `0x4910`,
sha256 `51da8a9d38aa3837b5c421eba862a813a2d3dabbf07d487a01e7fcc0e4161803`. Four zero bytes follow the last pool.
All nine language files hold the same bytes, at `fr` `0x4900`, `de` `0x4C60`, `es` `0x4BB8`, `it` `0x4980`,
`kr` `0x4920`, `cn` `0x4468`, `ch` `0x4460` and `in` `0x4450`. Every pool's weights sum to 100, every pad byte is
0 and every member's action id is below `0x21F`.

## Related

- [Enemy AI](enemy-ai.md) - how a unit walks its order sets and switches lists and phases.
- [Gambits](gambits.md) - the walk, the evaluator, the order layout and the relation modes.
- [Gambit conditions](gambit-conditions.md) - the party's conditions, which run on the same selector.
- [Battle orders](../Battle-Actions/battle-orders.md) - every order id.
- [Bestiary](../Enemy-Spawning/bestiary.md) - the enemies, with the set numbers of their four lists.
- [Area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md) - the area file.
- [Enmity](enmity.md) - the enmity checks of opcodes 2 and 34.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 12 calls with 5 other topics</summary>

**Damage and battle formulas** (explained on [native limits](../Engine-Core/native-limits.md), [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [action results](../Battle-Actions/action-results.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [traps](../World-Areas-And-Travel/traps.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) | is called by | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log)<br>[`0x0031E800`](enemy-order-sets.md) Battle stats: get owning actor handle |
| [`0x00236850`](enemy-order-sets.md) | is called by | [`0x0031B860`](../Battle-Actions/battle-log.md) Battle stats: find owning battle unit (on battle log)<br>[`0x0031E800`](enemy-order-sets.md) Battle stats: get owning actor handle<br>[`0x00384F40`](../Battle-Actions/action-results.md) (on action results) |
| [`0x00308C20`](enemy-order-sets.md) Ai order: compute bounded selector scalar | calls | [`0x00308B90`](../Battle-Actions/action-results.md) (on action results) |
| [`0x0030B9B0`](enemy-order-sets.md) | is called by | [`0x00300530`](../Characters-And-Objects/battle-unit-fields.md) Battle stats: modify hp and process lethal state (on battle unit fields)<br>[`0x003112F0`](../Rewards-EXP-Gil-And-Loot/gil.md) Battle formula: apply target result (on gil) |
| [`0x00322C50`](../Engine-Core/item-and-ability-ids.md) Battle encoded id: is valid for class (on item and ability ids) | is called by | [`0x002FEF30`](../Enemy-Spawning/bestiary.md) Battle stats: rebuild effective stats and affinity state (on bestiary) |
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00300530`](../Characters-And-Objects/battle-unit-fields.md) Battle stats: modify hp and process lethal state (on battle unit fields) |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00313A00`](../Battle-Actions/action-phases.md) (on action phases) |

**Rewards: EXP, LP, gil and loot** (explained on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) | is called by | [`0x00312280`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle unit: process defeat rewards and loot (on strong and weak mode) |

</details>
