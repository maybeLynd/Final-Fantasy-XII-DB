[Home](../../README.md) / [Characters and objects](README.md) / Battle unit construction

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Battle unit construction: the party and enemy definition tables, the stats record a unit gets, the kind byte and the type partition | system | Characters and objects | Battle units | How a battle unit becomes a party member or an enemy from a definition id: the installer's split on the id's high byte, the enemy path through the area's enemy table and the spawn record, the party path through the party table and the party block, the common stores, the fresh stats record with its level, equipment, licences, gambits and starting MP, the level grower and the experience curve, the handle re-key on a definition change, the kind byte at stats +5, and the partition of the type byte that the reward, availability and script code test. | 0x0023A570, 0x0023AC80, 0x0030C470, 0x0030C650, 0x002F8F20, 0x00236100, 0x002B58B0, 0x00322050, 0x003220E0, 0x00322C50, 0x00323790, 0x0031A630, 0x00323910, 0x00327CB0, 0x00326030, 0x00327DE0, 0x002F8E90, 0x002F90C0, 0x002F8BB0, 0x0050FF20, 0x00309230, 0x00254A40 |

## What the player sees

A battle unit becomes something when a definition is applied to it: Vaan with his level, equipment,
licences and gambits, or a Wolf with its stats, its one weapon and its loot flags. Party members
come from one authored table and enemies from the area's enemy table, and every piece of combat
code can tell the two apart by one byte in the unit's stats record. A narrower split of the party
side, by the type number, decides who earns experience and licence points and who is only a guest
or a summoned creature.

An enemy whose definition names a row past the end of one of the area's battle tables is not installed and does
not appear. An area without its battle-logic table installs no enemy at all; one without its enemy or class
table makes the installer read from address 0, and the game crashes.

## How it works

### The installer and the definition id

`0x0023A570(unit, id)` applies definition `id` to a unit. The id's high byte is the kind (0 party, 1
enemy, anything else installs nothing, clears unit flag bit `0x4000000` and returns 0) and its low byte the
row index¹. Before anything else the installer:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A580`-`0x0023A594`, `0x0023A626`-`0x0023A63C` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | remembers the unit's previous id, the stats record's word `+0x04`, when unit flag bit `0x4` is set (`0xFFFF` otherwise, and for a null unit pointer), and resets the unit with `0x00236A60(unit)` (`0x0023A597`-`0x0023A5B0`; [battle unit fields](battle-unit-fields.md)). The null test covers only that read: `0x00236A60` reads the unit's flags at `0x00236A6F` with no test; |   |
| 2 | returns 0 when the battle system is down (`0x02089300` = 0; `0x0023A5B5`-`0x0023A5BE`); |   |
| 3 | re-keys the unit, `0x00322050(unit)`, when the kind byte is not 0 or the previous id differs from both the new id and `0xFFFF`; with `0x00303EC0()` set, the re-key is skipped, without that check, when `0x00304630()` (`0xFF` read as `0xFFFF`) equals the previous id and the new id is `0xFFFF`. | `0x0023A5F4`-`0x0023A60A`<br>`0x0023A5CD`-`0x0023A5F2` |

`0x00322050(unit)` zeroes the attacker mask `+0xEA4` and count `+0xEA8` and stores
`0x003220E0(actor)` at `+0x08`: that function encodes the actor's current handle, advances the actor's
discriminator¹, encodes the new handle, and, when the party focus record `0x00327150()`
held the old handle, stores the re-keyed unit's stats byte `+0x04` (or `0xFF`) as a dword at
`[0x02EBF190] + 0x5AA4` and runs `0x00326500`, which picks the default controlled member and requests its handle
([Party leader](../Party/party-leader.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002659D0` |

</details>

A null actor gives 0 for both handles and a null focus record counts as handle 0, so with both null the store
still runs¹. The re-keyed unit is the one `0x003588B0` resolves from the new
handle, read through `0x00263E30` only while `0x02089340` bit `0x10` is set; without that bit, a unit or its stats
record, the dword is `0xFF`². `0x003220E0` returns the new handle³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003220F9`, `0x00322111`, `0x0032212C` |
| ² | `0x00322130`-`0x00322164` |
| ³ | `0x00322183` |

</details>

### The enemy path

With kind 1 the unit must have flag bit `0x4000000` set, else the installer returns 0¹; it also returns 0 when step 2 finds no spawn record². It then:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A641`-`0x0023A648` |
| ² | `0x0023A77E`-`0x0023A781` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | takes row `index` of the enemy table `0x02EBF120` (count at `+0x04`, row stride at `+0x08`, rows from the section `0x0020E600(table dword +0x0C)`; `0x0023A664`-`0x0023A694`), and the class row the enemy row's word `+0x00` names in `0x02EBF150`, found the same way, and makes five bound tests, returning 0 at the first that fails:<br>• the row index against the enemy table's count;<br>• the enemy row's word `+0x00` against the class table's count at `+0x04`;<br>• the word `+0x50` against the count word at `+0` of `0x02EBF168`;<br>• the word `+0x22` against the count at `+0x04` of `0x02EBF148`;<br>• the word `+0x24` against the count at `+0x04` of `0x02EBF140`. | `0x0023A6C1`-`0x0023A6FC`<br>`0x0023A63A`<br>`0x0023A64A`-`0x0023A662`<br>`0x0023A6A1`-`0x0023A6BB`<br>`0x0023A70B`-`0x0023A726`<br>`0x0023A72C`-`0x0023A747`<br>`0x0023A74D`-`0x0023A768` |

   Each test compares the index with `count - 1`, the count read as 0 for a null table. Four are unsigned (`ja`):
   with a null table or a count of 0, `count - 1` is `0xFFFFFFFF` and they pass every index.

   With a count of 0
   the row taken after them lies past the table's end. With a null enemy or class table the row address is 0 and
   is read there¹; a null `0x02EBF148` or `0x02EBF140` leaves
   the unit's row pointer at `+0xE70` or `+0xE78` null². The `+0x50` test is signed
   (`jg`) on a zero-extended word, so a null or empty `0x02EBF168` makes it refuse every enemy;

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A69F` and `0x0023A6B4`; `0x0023A708` and `0x0023A8E6` |
| ² | `0x0023A9A3`, `0x0023A9EA` |

</details>
| Step | What happens | Where in the code |
|---|---|---|
| 2 | resolves the spawn record: `0x00236100(unit +0x40, unit +0x57)` reads the lane map's byte `1 + lane` (lane below the map's count byte, entry not `0xFF`) and returns `[0x0208E690] + entry * 0x250`, from the bank pointer held at `0x0208E690`; a null map, a negative lane, a lane at or past the count or a `0xFF` entry returns 0. The stats record is that record's `+0x80`; | `0x0023612D`<br>`0x00236107`<br>`0x0023A76E`-`0x0023A787` |
| 3 | for a fresh record (record byte `+0` without bits `0x1` and `0x4`) it initialises the stats record, `0x0023AC80(stats record, id)` (below), and stores record byte `+0x14` = the steal bits, the byte being zeroed first: bits `0x1`, `0x2` and `0x4` when the row's words `+0x32`, `+0x34` and `+0x36` are not `0xFFFF`; | `0x0023A7AE`<br>`0x0023A791`-`0x0023A7E4` |
| 4 | still for a fresh record, when the row's byte `+0x02` is not `0xFF`, it reads the spawn counter `0x0208D354 + (0x0208D454 * 64 + byte) * 2`, stores the old value's low byte at record `+0x12` and writes back `old + 1`, or 1 once `old` reaches `0x00254A40()`; with a byte of `0xFF` it stores 0 at `+0x12`; | `0x0023A7E7`-`0x0023A840` |
| 5 | resolves the name text: the row's word `+0x08` split as bank (high 5 bits) and entry (low 11 bits) through `0x02EBF170`, each step an offset turned into an address by `0x0020E600(offset)`, then `0x002B58B0(block, 0)`. `0x00269F20` stores that text and the `+0x12` ordinal at the actor's `+0xF8` and `+0x100`; | `0x0023A84A`-`0x0023A8E1`<br>`0x00238EB8` |
| 6 | stores `+0xE60` = the enemy row, `+0xE68` = the class row, `+0x6E0` = the `0x02EBF168` row named by word `+0x50`, `0x0020E600(table dword +0x04 + 4 * word)`, `+0xE70` = the `0x02EBF148` row named by word `+0x22`, `+0xE78` = the `0x02EBF140` row named by word `+0x24`, the last two from `0x0020E600(table dword +0x0C)`; | `0x0023A915`-`0x0023A91C`<br>`0x0023A92F`-`0x0023A95E`<br>`0x0023A965`-`0x0023A9A5`<br>`0x0023A9AC`-`0x0023A9F4` |
| 7 | registers the unit, `0x00328FF0(0, row byte +0x03 & 3, unit byte +0xEA9)`: the class to `0x02EC1384` and the slot to `0x02EC1380`, written only when the class is not 0 or the slot is negative, and sets flag bit `0x80000000000` when `row byte +0x03 & 3` or `row byte +0x15` bit `0x4` is set, else clears it. | `0x0023A9EC`-`0x0023AA04`<br>`0x0023AA09`-`0x0023AA41` |

In step 7 the slot is zero-extended¹, so from this call the write happens exactly when the class
is not 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A9EC` |

</details>

The row addresses of this path and of the party path are formed in 32 bits, the stride times the index plus
the low dword of the section address: the enemy row¹, the class row², `+0xE70`³, `+0xE78`⁴ and the party
row⁵. A section address of 0 from `0x0020E600` is treated like a null table⁶, and a null `0x02EBF168` stores 0 at `+0x6E0`⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A690`-`0x0023A694` |
| ² | `0x0023A6F8`-`0x0023A6FC` |
| ³ | `0x0023A99C`-`0x0023A99F` |
| ⁴ | `0x0023A9E3`-`0x0023A9E6` |
| ⁵ | `0x0023AA99`-`0x0023AA9D` |
| ⁶ | `0x0023A674`, `0x0023A6D1`, `0x0023A97C`, `0x0023A9C3`, `0x0023AA7D` |
| ⁷ | `0x0023A94B` |

</details>

With the row's table, its section or `0x02EBF170` null, the name block is 0, `0x002B58B0(0, 0)` answers 0 and the
name text stored at `+0x18` is null¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023A84D`-`0x0023A868`, `0x0023AAC7`-`0x0023AAE1`, `0x002B58B0`-`0x002B58B5` |

</details>

For the party table the two cases differ. `0x00322C50` refuses every index for a null table, so the null test
at `0x0023AA70` is not taken; it does not test the section. With a table whose section address is 0¹ the index is accepted, the row address is 0, and `0x0023AB5F` reads the byte at address `0x2B`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AA7D` |

</details>

The name drawer `0x00272CE0` adds a letter to that name when the actor's word `+0x102` is negative, so that the
name is the text at `+0xF8`¹, and the ordinal is not 0². `0x002B58F0`, through
`0x0024ABE0`, writes entry `0x21` + (ordinal - 1) mod 26 of the text the font sheet names at `+0x14`, or at `+0x18`
when the language test `0x00254A10` is true³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263990`, `0x00263A10` |
| ² | `0x00272D3A` |
| ³ | `0x002B5957`-`0x002B5997` |

</details>

The common stores then take, from the class row (read at `0x0023A8E6`-`0x0023A940`): `+0x64` = byte `+0x22`
times 2π/360 (`0x01CEBC78` over `0x00902438`), `+0x55` = byte `+0x04`, `+0x68` = float(byte `+0x23`), `+0x56` =
byte `+0x05`, `+0x6C` = float(byte `+0x27`), `+0x52` = word `+0x06`.

### The party path

With kind 0 the index must pass `0x00322C50(2, index, 1)`, the party table's count, else the installer
returns 0¹. It takes row `index` of the party table `0x02EBF130`, from the section
`0x0020E600(table dword +0x0C)`², points the stats at the party block's element
`[0x02EBF190] + 8 + index * 0x1C8` with no spawn record³, and resolves the name from the
row's word `+0x30` the same way as the enemy path, ending in `0x002B58B0(block, 0)`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AA49`-`0x0023AA60` |
| ² | `0x0023AA66`-`0x0023AA9F` |
| ³ | `0x0023AAAA`-`0x0023AAC1` |
| ⁴ | `0x0023AAC4`-`0x0023AB5A` |

</details>

Its stores (`0x0023AB5F`-`0x0023ABC3`, the floats and bytes with the common stores below) are:
`+0x6E0` = `0x02089378 + index * 0x170`, `+0x6F0` = `0x01E09350`,
`+0xE60` = the row, `+0x64` = 2π, `+0x6C` = row byte `+0x2B` times 1.5, `+0x68` = float(row byte
`+0x2B`), `+0x55` = `0xFF`, `+0x56` = `0xFF`, `+0x52` = `0xFFFF`.

The party path reads the party table (its count, section, stride, and the row's word `+0x30` and byte
`+0x2B`), the party block pointer `[0x02EBF190]`, of which it only forms the member's record address, and the
name table `0x02EBF170`; it reads nothing of the unit's actor: no actor field, no seat map and not the roster
array `0x0209A1F0`¹. The path does not call the fresh-stats function `0x0023AC80`: the
member's record is used as it stands.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AA49`-`0x0023ABC3` |

</details>

The installer's own first read of the record is at `0x0023AC35`, in the common stores. Before it,
`0x00237040(unit)` at `0x0023AC1C` reads the record through `0x00308010(unit, 1)`: the kind byte `+0x05`¹ and, for kind 0, the status words `+0x64` and `+0x3C`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00308021` |
| ² | `0x0030814C` |

</details>

An index the check refuses returns 0 with the unit reset and its flag bit `0x4000000` as it was¹; an accepted one neither tests nor sets that bit, which the enemy path
requires², though the common stores can clear it for a member with any of the status bits `0x80000003`
in `+0x64 | +0x3C` outside a town³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AA59`-`0x0023AA60`, `0x0023A63A` |
| ² | `0x0023A643` |
| ³ | `0x0023AC4B` |

</details>

Three direct calls reach the installer: no other direct call or jump instruction has it as its target, and no
pointer to it is stored in the file.

`0x0023A3B0(actor, row)`, which the begin handler `0x00510160` of the script verb `btlAtelSetUnit` calls¹, takes the unit `0x0031B760(actor)` and returns 0 without one; with one it calls
`0x002355A0(actor)` and then `0x0023A570(unit, row | 0x100)`, or `0x0023A570(unit, 0xFFFF)` for a row of `0xFF`,
and returns the installer's answer (`0x0023A3C4`-`0x0023A3F1`;
[Enemy spawning](../Enemy-Spawning/enemy-spawning.md)). The teardown `0x00300E40` calls
`0x0023A570(unit, 0xFFFF)` for a unit with no stats record or with one of a kind other than 0².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0051017D` |
| ² | `0x00300EDA`-`0x00300EEC`, `0x00300F6D`-`0x00300F75` |

</details>

Of the three, only the call in the seat rebuild `0x003266C0` can pass a party id: for seat
0 to 3 it takes the roster actor `0x00263750(seat)` and that actor's unit `0x00263E30(actor)`, and calls
`0x0023A570(unit, seat word)` with the whole word of map 1's seat (`0x00326A40`-`0x00326B0A`;
[Party slots](../Party/party-slots.md)).

A seat with no roster actor, or whose actor has no unit, is
skipped¹; otherwise the call is made only when the seat word differs from the unit's
present id². When the present id is not `0xFFFF`, the rebuild itself clears flag bit
`0x4000000` before the call³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00326A4A`, `0x00326A5E` |
| ² | `0x00326A7F`-`0x00326A82` |
| ³ | `0x00326AFD` |

</details>

### The common stores

Both paths end with: `+0x48` = 0 (the HP floor), `+0x698` = the stats record, `+0x6A0` = the spawn
record or null, `+0x18` = the name text, `+0x54` = `0xFF`, and `+0x64`, `+0x6C`, `+0x68`, `+0x55`, `+0x56`
and `+0x52` as given above¹, then `0x00237040(unit)` and `0x002FEAB0(unit)`, which
clears the 8 bytes at `+0xEAC`². `0x00237040(unit)` calls `0x00308010(unit, 1)` and jumps
to `0x002FED60(unit, 1)` when that answered non-zero, else to `0x002FEDC0(unit, 1)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023ABCA`-`0x0023AC18` |
| ² | `0x0023AC1C`-`0x0023AC24` |
| ³ | `0x00237046`-`0x00237074` |

</details>

When the stats record is null, or the OR of its status words
`+0x3C` and `+0x64` carries bits `0x1`, `0x2` or `0x80000000` outside a town (`0x0023AC29`-`0x0023AC52`, through
the jump `0x00313F60()` to `0x00377C20`), flag bit `0x4000000` is cleared and bit `0x2` set. Bit `0x4` is set and
the installer returns 1¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0023AC56`-`0x0023AC59` |

</details>

The party path writes none of `+0xE68`, `+0xE70` and `+0xE78`, makes no `0x00328FF0` call and leaves flag bit
`0x80000000000` as it was. The reset `0x00236A60` nulls `+0xE60` and `+0xE68`¹ and
not `+0xE70` or `+0xE78`, so a unit that was an enemy keeps those two pointers after a party install.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00236ABB`, `0x00236AC2` |

</details>

### The fresh stats record

`0x0023AC80(record, id)` fills a stats record from nothing:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `memset` of `0x1C8` bytes, then `+0x50` = all ones (8 bytes), `+0x58` = `0xFFFF`, `+0x1C3` = `0xFFFF`, `+0x1C5` = `0xFF`; with `0x02089300` = 0 it returns 0; |   |
| 2 | kind 0 takes the party row and the level `max(row byte +0x2E, 1)`; kind 1 takes the enemy row and level 1; any other kind returns 0; |   |
| 3 | `+0x04` = the whole id, so the byte `+0x05` is the kind by construction; then the level grower `0x0030C470(record, level, baseLevel)`; |   |
| 4 | kind 0: the LP `0x00323790(record, row word +0x44)`; for an index below 7, every licence entry of `0x02EBF038` whose byte `+0x07` has the bit `1 << index` set is granted (`0x00323910(record, entry, 1, 1)`); |   |
| 5 | kind 0: equipment slots 0-4 from the row's words `+0x0A`, `+0x0C`, `+0x0E`, `+0x10`, `+0x12`; the gambit preset `0x00327CB0(record, row word +0x14)`, `0x00326030([0x02EBF190], index)` and `0x00327DE0([0x02EBF190] + 8 + index * 0x1C8)`; and record `+0x00` bit `0x4` when the row's byte `+0x2C` has bit `0x40`; | `0x0031A630` |
| 6 | kind 1: equipment slot 0 from the row's word `+0x16`, slot 1 from `+0x1C`, slots 2-4 `0xFFFF`. |   |

### The level grower

`0x0030C470(record, level, baseLevel)` starts from level 0 and grows up:

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `+0x1C2` = 0, then by kind:<br>• kind 0: the base values come from the party row named by `+0x04`: `+0x08` = word `+0x16`, `+0x0C` = word `+0x1A`, `+0x10`, `+0x14`, `+0x18`, `+0x1C` = the floats of bytes `+0x1E`, `+0x21`, `+0x24`, `+0x27`, `+0x20` = the larger of byte `+0x46` and the licence rank `0x00324100(record)`;<br>• kind 1: only `+0x88` = `baseLevel` (1 from the initialiser, the minimum level from `0x002398F0`, 0 from the four other callers);<br>• any other kind returns; |   |
| 2 | `0x0030C650(record, level, 2)` grows to the level ([stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md)); |   |
| 3 | `+0x18C` = `min(0x002F8F20(level - 1), 99999999)`, the experience of the level reached ([EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md)); |   |
| 4 | when the status masks `0x0208D320` or `0x0208D324` are non-zero, the statuses in their union are removed (`0x0030F690(record, union)`); HP and MP are reconciled to their capacities; | `0x0030F340`, `0x0030F5A0` |
| 5 | the starting MP: `cap` = `+0x28` when the layer bytes `+0x6C` and `+0x7C` are both non-negative, else 0; kind 0 sets `+0x4C` = `cap * row byte +0x47 / 100`, kind 1 sets `+0x4C` = `cap`; |   |
| 6 | `0x0030FED0(record, 0)` rebuilds the derived state ([augments](../Damage-And-Battle-Formulas/augments.md)). |   |

For kind 0 the party row is the table's word `+8` times byte `+0x04` plus the value `0x0020E600` returns for the
table's `+0xC`, added in 32 bits¹, so the upper half of that pointer is dropped. Nothing
guards the read: when `[0x02EBF130]` is null² or `0x0020E600` returns 0³, the base stays 0 and
`0x0030C4F9` reads the word at address `0x16`, which faults, because the first 64 KB of a Windows x64 process are
never mapped.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030C4EC`-`0x0030C4F7` |
| ² | `0x0030C4C7` |
| ³ | `0x0030C4D4` |

</details>

### The kind byte and the type partition

Stats byte `+0x05` is the kind: 0 for a party-table unit, 1 for an enemy. Stats byte `+0x04` is the
row index, and for kind 0 it is the type the code partitions:

| Type | Span | `0x0050FF20` class | Experience (`0x002F8BB0`) | Licence points (`0x002F90C0`) |
|---|---|---|---|---|
| 0-6 | the main characters | 0 | yes | yes |
| 7-25 | the guest range | 1 | yes | no |
| 26 | the Chocobo | 3 | yes, but not counted in the split | yes |
| 27-39 | the thirteen Espers, Belias to Zodiark | 2 | no | no |
| 40 and above | | 0 | yes | yes |

- `0x002F8E90(record)` classifies a record: kind 0 gives 2 for an Esper and 1 otherwise; kind 1 gives
  4 when the owning unit's actor class nibble¹ is 3, 8 when it is 1, 2 or 7, else 16.
  A null record and any other kind give 16². For kind 1 it stores the unit `0x0031B860` finds at
  `0x02EBF188`³; with no unit the class nibble is 0⁴, so the result is 16.
- `0x002F8BB0(recipient, source)` pays experience only for a kind-0 recipient with a unit, outside the
  Espers (the Chocobo, type 26, included), without a terminal status, from a kind-1 source. The amount is
  `(source level +0x1C2 - +0x88) * [source +0xE78] +0x34 + [source +0xE70] +0x34`.
- When `0x003135C0()` is 0 that amount becomes `amount / n` (`idiv`, `0x002F8D1C`-`0x002F8D1D`; 0 when
  `n` is 0) for the count `n` of party members (`0x0031B810(0..3)`) that are alive, not Espers
  and not the Chocobo (type 26); otherwise it is paid whole to the `0x00313800` member. It is doubled when
  `(+0x6B | +0x7B) & 0x08` and zeroed when `(+0x6B | +0x7B) & 0x20`⁵.
- `0x002F90C0(recipient, source)` pays licence points, when `0x00264150()` is 0, for a kind-0 recipient
  of type 26 (the Chocobo), below 7 or above 39 without a terminal status, from a kind-1 source: `(level - +0x88) * [source +0xE78] +0x2F + [source +0xE70] +0x2F`,
  doubled when `(+0x6B | +0x7B) & 0x10`⁶.
- A kind-1 source is a non-null unit whose stats record `+0x698` is non-null and of kind 1⁷. The terminal statuses are the bits `0x80000003` of `+0x64 | +0x3C`⁸. `0x002F90C0` asks for no unit on the field.
- A null recipient skips every recipient test and the doubling and zeroing⁹. `0x002F8BB0` then pays the whole amount when `0x003135C0()` is not 0, since the `0x00313800` member is
  not compared¹⁰, and the split amount otherwise. `0x00312280` calls both that way for the reward display
 ¹¹.
- `0x00309230(unit, actionRow)` returns the row's word `+0x24` as the presentation code, except for
  action row `0x113`, where an Esper type gets `42 + 3 * (type - 27)`.
- That table is 13 dwords built on the stack from `0x00D103B0` and `0x4E`¹², indexed by the
  unit's stats byte `+0x04` minus 27 with no range test¹³, so another type reads a stack
  dword outside the table.
- Row `0x113` is the action table `[0x02EBF138]`'s word `+8` times `0x113` plus the value
  `0x0020E600` gives for its `+0xC`, added in 32 bits¹⁴, or 0 when `[0x02EBF138]` is null or
  `0x0020E600` gives 0¹⁵; `0x003092C0` compares the row argument with that zero-extended value.
- `0x0050FF20`, a script verb's handler, resolves its operand through `0x00320AB0(value, 3)` and pushes
  -2 for no record, -1 for kind 1, and the class above for kind 0.
  Any other kind pushes 0¹⁶. The operand, popped with `0x00267DB0`, is truncated (`cvttss2si ecx, xmm0`)
  from its float¹⁷, and the push is the tail jump to `0x0026B4E0`¹⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263C20` |
| ² | `0x002F8F09` |
| ³ | `0x002F8EC9` |
| ⁴ | `0x002F8EDB`, `0x00263C2D` |
| ⁵ | `0x002F8D26`-`0x002F8D40` |
| ⁶ | `0x002F914B`-`0x002F9157` |
| ⁷ | `0x002F8C11`-`0x002F8C2E`, `0x002F9104`-`0x002F9119` |
| ⁸ | `0x002F8C06`, `0x002F90FD` |
| ⁹ | `0x002F8BCF`, `0x002F8D21`, `0x002F90DD`, `0x002F9146` |
| ¹⁰ | `0x002F8C42` |
| ¹¹ | `0x003124BE`, `0x003124CA` |
| ¹² | `0x00309249`-`0x00309282` |
| ¹³ | `0x003092CB`-`0x003092DB` |
| ¹⁴ | `0x003092B0`-`0x003092BA` |
| ¹⁵ | `0x003092BE` |
| ¹⁶ | `0x0050FF92` |
| ¹⁷ | `0x0050FF30`-`0x0050FF35` |
| ¹⁸ | `0x0050FFA3` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

```python
definition id (u16)
mask 0xFF00  kind       0 party table 0x02EBF130, 1 enemy table 0x02EBF120, other: nothing installed
mask 0xFF   index      the row; for kind 0 also the type byte at stats +0x04
```

Struct EnemyRow table=`0x02EBF120` (stride at table `+0x08`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | classRow | row of `0x02EBF150` (the class row at unit `+0xE68`) |
| `+0x02` | `u8` | counterSlot | spawn counter index, `0xFF` for no counter |
| `+0x03` | `u8` | flags | mask `0x3` the tracked-HP class (`0x00328FF0`, flag bit `0x80000000000`); bit `0x10`: unit `+0x58` = 7 (`0x00238BF0`), the motion height without its random part (`0x002362A4`), a test of the gambit selector (`0x0030268D`); bit `0x20`: the shadow kind, through `0x002E8A10` |
| `+0x08` | `u16` | nameRef | bank << 11 \| entry into `0x02EBF170` |
| `+0x0A` | `i16[3]` | scalePercent | 0 means 100; divided by 100 and handed to `0x002E5FD0` (`0x00238D1B`-`0x00238D68`) |
| `+0x11` | `u8[2]` | variant | `+0x12` then `+0x11`, the model's variant bytes (`0x0031C5AB`, `0x0031C5B1`) |
| `+0x13` | `u8` | animSet | `0xFF` for the weapon's (`0x003202F0`) |
| `+0x15` | `u8` | flags2 | bit `0x1` Attack and weapon evade, bit `0x2` shield and magick evade from the stat rows (`0x002FEF30`); bit `0x4` also sets flag bit `0x80000000000`; bit `0x8` (`0x0031AACF`) and the bits under mask `0x18` (`0x0031AB39`) in the target-information query `0x0031AA30` |
| `+0x16` | `u16` | equipment0 |  |
| `+0x18` | `u32` | startHp | 0 for no starting HP (`0x0023A410`) |
| `+0x1C` | `u16` | equipment1 |  |
| `+0x22` | `u16` | rewardRow | row of `0x02EBF148` (unit `+0xE70`) |
| `+0x24` | `u16` | rewardLevelRow | row of `0x02EBF140` (unit `+0xE78`) |
| `+0x26` | `i16` | voiceBank | negative for the model's (`0x003212E0`) |
| `+0x28` | `u16[5]` | drops | the five drop slots (`0x003180F0`) |
| `+0x32` | `u16` | steal0 | `0xFFFF` for no item; record `+0x14` bit `0x1` |
| `+0x34` | `u16` | steal1 | bit `0x2` |
| `+0x36` | `u16` | steal2 | bit `0x4` |
| `+0x38` | `u32[2]` | partIds | part 8 entries 0 and 1 of the model rebuild (`0x0031C000` through `0x0031BEC0`) |
| `+0x40` | `u8[2]` | partLinks | their attach links, `0x00D107F8`[byte] (`0x0031BE30`) |
| `+0x42` | `u8[2]` | extraChance | the two Monograph drop chances (`0x003180F0`) |
| `+0x44` | `u16[2]` | poach | 95 % and 5 % (`0x00390680`) |
| `+0x48` | `u16[4]` | extraDrops | key item, item, key item, item (`0x003180F0`) |
| `+0x50` | `u16[4]` | logicRows | rows of `0x02EBF168` for orders 0-3; `+0x50` at install (unit `+0x6E0`), all four through `0x002FDDA0` and `0x00239040` |

Struct PartyRow table=`0x02EBF130` (stride at table `+0x08`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x0A` | `u16[5]` | equipment | slots 0-4 |
| `+0x14` | `u16` | gambitPreset |  |
| `+0x16` | `u16` | baseHp |  |
| `+0x1A` | `u16` | baseMp |  |
| `+0x1E` | `u8` | baseStat0 | with `+0x21`, `+0x24`, `+0x27`: the four float stats |
| `+0x2B` | `u8` | scale | unit `+0x68` and `+0x6C` (times 1.5) |
| `+0x2C` | `u8` | flags | bit `0x40` sets record `+0x00` bit `0x4` |
| `+0x2E` | `u8` | startLevel | 0 means 1 |
| `+0x30` | `u16` | nameRef |  |
| `+0x44` | `u16` | startLp |  |
| `+0x46` | `u8` | baseStat4 | unit stat `+0x20`, raised to the licence rank |
| `+0x47` | `u8` | startMpPercent |  |

Class row¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EBF150` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | model | a bound id, letter class in the bits under mask `0xFF0000` (`0x0031C2F0`) |
| `+0x04` | `u8` | type | unit `+0x55` |
| `+0x05` | `u8` | kind | unit `+0x56` |
| `+0x06` | `u16` | clanEntry | unit `+0x52` |
| `+0x10` | `i16` | separation | tenths; a positive value / 10 to `0x0026DAC0` (`0x00238CEB`) |
| `+0x12` | `u8` | flags | bits `0x7` the effect column (`0x00329FB3`); bit `0x10` actor `+0x09` bit `0x40` (`0x0026A3A0`); bit `0x20` the view query's kind (`0x0031B394`); bit `0x40` actor `+0x08` bit `0x8` and `+0x09` bit `0x40` (`0x0026A430`); bit `0x80` `0x003879C0`, `0x00390AB0`, `0x0033D660` |
| `+0x18` | `u8` | group | bits `0xE` a movement group, 4 noticing every unit (`0x003248F8`); mask `0x70` the placement height (`0x00239E10`) |
| `+0x20` | `u8` | comboCap | hits at most this - 1 (`0x00388845`) |
| `+0x21` | `u8` | flags21 | bit `0x2` an enemy may back off (`0x00334204`) |
| `+0x22` | `u8` | facing | unit `+0x64` = value * 2π / 360 |
| `+0x23` | `u8` | scale | unit `+0x68` |
| `+0x25` | `u8` | sightRadius | `0x003247F0` |
| `+0x26` | `u8` | lowHpRadius | units below 40 % HP (`0x003247F0`) |
| `+0x27` | `u8` | scale2 | unit `+0x6C` |
| `+0x28` | `u8` | flags28 | bit `0x1` the view query's height (`0x0031B08D`); bit `0x2` no chain (`0x00317F09`) |
| `+0x29` | `u8[5]` | affinity | absorb, halve, nullify, weak, potency (`0x002FEF30`) |
| `+0x30` | `u16[8]` | words30 | no reader among the four readers of `0x02EBF150` and the 47 loads of unit `+0xE68`, each followed to its fields |
| `+0x40` | `u16` | modelFamily | the loot quantity group of the kill chain's run (`0x00317F77`); not the model, which is `+0x00` |
| `+0x52` | `u16` | species | `0xFFFF` no entry (`0x003171C0`) |

</details>

## Modding notes

- An enemy's statuses and augments are not in its row: the installer writes no status or augment, and the masks
  the recompute reads come from the enemy's script ([augments](../Damage-And-Battle-Formulas/augments.md)).
- Giving a party member a starting level sets its experience to exactly that level's threshold
  and strips every status in the two masks; the MP starts at the row's percentage of capacity.
- A type between 27 and 39 earns nothing and is tested by one predicate (`type - 27 <= 12`)
  wherever the Espers matter; the Chocobo, type 26, is a separate test with its own rule.

## Related

- [Battle units](battle-units.md): the pool, the bind and the handle the re-key replaces.
- [Battle unit fields](battle-unit-fields.md): the unit record the installer fills.
- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md): the stats record field by field.
- [EXP, LP and level ups](../Rewards-EXP-Gil-And-Loot/exp-lp-and-level-ups.md) and [stat growth per level](../Rewards-EXP-Gil-And-Loot/stat-growth-per-level.md): the curve and the grower.
- [Spawn placement and retirement](../Enemy-Spawning/enemy-spawning.md): the spawn record and the lane map.
- [Bestiary](../Enemy-Spawning/bestiary.md): every shipped enemy definition with these fields decoded.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 5 calls with 5 other topics</summary>

**Combat** (explained on [battle units](battle-units.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse) | is called by | [`0x003206E0`](battle-units.md) (on battle units) |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00254A10`](../Menus-And-HUD/text-string-tables.md) (on text string tables) | calls | [`0x00229E40`](../Story-Events-And-Hunts/script-language-differences.md) (on script language differences) |

**Steam and achievements** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00312280`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle unit: process defeat rewards and loot (on strong and weak mode) | calls | [`0x00316A50`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Saving, loading and settings** (explained on [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00254A10`](../Menus-And-HUD/text-string-tables.md) (on text string tables) | is called by | [`0x005832B0`](../Game-Files-And-Data-Tables/standard-file-formats.md) (on standard file formats) |

**Story, events and hunts** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | calls | [`0x0032A930`](../Engine-Core/identifier-spaces.md) Persistent flag: query bank2048 (on identifier spaces) |

</details>
