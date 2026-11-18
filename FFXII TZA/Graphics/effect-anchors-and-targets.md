[Home](../../README.md) / [Graphics](README.md) / Effect anchors and targets

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Effect anchors and targets: the target and anchor queries, target slots, and reading and renaming an owner or target | system | Graphics | Visual effects / Effect Elements And Drawing | Where an effect element is placed: the target and anchor queries that turn an anchor descriptor into a matrix, the point kinds, the target slots of an instance, the raw owner and target reads, and renaming an owner or target. | 0x020910F0, 0x02F97348, 0x003A4290, 0x003A40F0, 0x003A6FC0, 0x003A6C30, 0x003A69F0, 0x0057A040, 0x004220F0, 0x0046F4B0, 0x003E5700, 0x003E5600, 0x003E5810, 0x01EFAC60, 0x0209A71C |

## What the player sees

An effect piece follows the point it is anchored to: a bone of the character that cast it, a point
on its target, or a fixed spot in the world.

## How it works

### Target and anchor queries

Some tails ask for a point from a sub-record. `0x002F3360` switches on the sub-record's byte `+0x90`;
value 3 calls `0x003A56F0`, which samples a vector track¹ and switches on the byte `+0x48`
minus 1 over 14 cases². `0x003A4290` has the same
14-case switch on the same byte³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00430B90` |
| ² | `0x002F3384`-`0x002F33EA`, `0x003A575E`-`0x003A5797` |
| ³ | `0x003A4303`-`0x003A4319` |

</details>

Their arms are in
[`effect-element-runtime-switch-family-3a42-3a56.tsv`](effect-element-runtime-switch-family-3a42-3a56.tsv); [`effect-element-runtime-switch-family-jump-tables.tsv`](effect-element-runtime-switch-family-jump-tables.tsv)
decodes `0x00442170` and `0x00442460` (the emitter-record subtype switches) and the record-store
fronts `0x00500980` / `0x00500850`, together with dispatchers outside the effect code.

### Columns of effect-element-runtime-switch-family-3a42-3a56.tsv

One row per value of the byte `+0x48`, 1 to 14, between a first row for the switch head and two last rows for the
switches inside the kind-6 arm, 17 rows. The arms agree with the tables at `0x003A5540`¹ and
`0x003A68E4`²: all 28 match.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A4290` |
| ² | `0x003A56F0` |

</details>

| Column | Holds |
|---|---|
| `selector` | the value of byte `+0x48` the row describes (the switch takes it minus 1); `kind_byte` for the switch head; `inner_10case` and `inner_40case` for the two switches inside the kind-6 arm |
| `front_3A4290_arm`, `front_3A56F0_arm` | the arm address in each function's table; on the head row the switch expression, and on the inner rows the jump site and the table it reads |
| `arm_size_4290`, `arm_size_56F0` | the arm's length in bytes, from its start to the next arm's start in address order; `(shared with n)` when value n uses the same arm; the last arm of each function in address order has no next arm and runs through the epilogue it shares with other arms to the function's `ret` (97 bytes on value 12 of `0x003A4290`, to the `ret` at `0x003A553D`; 173 on value 14 of `0x003A56F0`, to the `ret` at `0x003A68E1`); on the inner rows the case count and the count of distinct targets; `-` on the head row |
| `calls_4290`, `calls_56F0` | the functions the arm calls in its first stretch, joined by `+`, with `x2` or `xN` for a repeated call; `same as kind n` for a shared arm; on the head row the work done before the switch, and on the inner rows the arm addresses |
| `evidence` | the instruction addresses and ranges read for the row in each function, separated by a semicolon |

### Columns of effect-element-runtime-switch-family-jump-tables.tsv

One row per case of a decoded jump table, 450 rows from 12 tables in 10 dispatchers. Every `arm` equals the
table's entry for the row: the table's dword at `case` (125 rows, nine tables) or, when a byte map comes first, at
the byte map's entry for `case` (325 rows, tables `0x00277854`, `0x0028144C` and `0x00282590`), plus the image base.

| Column | Holds |
|---|---|
| `dispatcher` | the start address of the function holding the switch |
| `disp_name` | that function's name in the disassembly's function list; `FUN_` and the address when it carries no name |
| `selector` | the operand the switch reads its case from; a `byte ptr` with a displacement above `0x100000` is a byte map at image base plus that displacement; on the 7 rows of table `0x00282574` the case is `dword ptr [rcx + 0xc0]` minus 1 (`0x00281ED7`-`0x00281EE7`) |
| `arm` | the address the case jumps to |
| `handler` | the function the arm calls or jumps to first, a function start in the function list (165 rows); `-` on the other 285: 276 arms make no direct call or jump in their first 11 instructions, 7 jump only within the dispatcher, and 2 (`0x002F6CFE`, `0x00280FD4`) reach a function only after a conditional branch |
| `handler_name` | the handler's name in the function list, empty when `handler` is `-` |

### The anchor query

`0x003A4290(anchor, element, work, out)` places an element. It samples the element's offset track at its frame
`+0xFC`¹, resolves the anchor descriptor into the matrix `out`, adds the offset to `out`'s
position and returns 1. When the anchor cannot be resolved it keeps `work` from the frame before, or on frame 0
zeroes `work` and `out` and returns 0². The descriptor's bytes:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00430B90`, `0x003A4303` |
| ² | `0x003A53DC`-`0x003A542B` |

</details>

| Field offset | Meaning |
|---|---|
| `+0x40` | `n` for the record kinds 4, 6 and 7 |
| `+0x48` | the record kind (first table) |
| `+0x49` | the point kind (second table) |
| `+0x4A` | bit `0x1` resolve on frame 0 only and keep the result after; bit `0x2` skip the record's scale; bits `0xC` the height rule (third table) |
| `+0x4B` | the mode `0x00421E20` takes: 0 the bone's origin, 1 the bone's end, 2 its middle |
| `+0x4C` | a bone index for the point kinds 6 and 7 |
| `+0x4E` | the object slot for the record kinds 9 and 13 |

The element's byte `+0x102` is the slot the owner and target reads take ([target slots](#target-slots)).

| Record kind (`+0x48`) | Whose matrix | Point kind used |
|---|---|---|
| 1 | the owner's record (`0x003A3FD0`, `0x003A440B`) | yes |
| 2 | the target's record (`0x003A6BA0`, `0x003A4432`) | yes |
| 3, 11 | the camera matrix `0x02AEDEF0`; kind 11 takes the position `0x02AED600`, `0x02AED604` and `0x02AED608`, x, y and z (`0x003A449C`, `0x003A44A9`, `0x003A44B6`), which `0x003820C0` moves on by a vector each call (`0x0038241F`, `0x00382434`, `0x0038244A`). The third axis is scaled by tan(pi/8) / tan(fov / 2), fov the angle `0x02AED568`, or 45 degrees in Super Wide mode while `0x02AED568` and `0x02AED56C` are above 1.0 (`0x003A44C3`-`0x003A4553`) | no |
| 4 | the record of the actor in `effectactor` slot `n` (`0x003A40F0`, through the tables `0x003A4220` uses). `0x003A40F0` returns 0 when no table names an actor, and the query then goes to `0x003A53DC`, the path for an anchor that cannot be resolved (`0x003A4194`, `0x003A45A6`). For an actor without a render index (`0x002E9B80` gives −1) it writes the actor's position (`0x003588B0`, `0x00265020`) into the work matrix's `+0x30`-`+0x38` and gives no record; it resets that matrix to the identity (`0x00250010`) first only on the `0x0036E4E0` lookup (`0x003A4145`-`0x003A41CF`). The query then goes to `0x003A53DC` as well (`0x003A4696`): frame 0 zeroes `work` and `out`, and later frames place the element at that position plus the offset (`0x003A43B9`). A render index whose low word is `0xFFFF`, or a record whose `+0x284` is 0, also gives no record (`0x003A416C`, `0x003A41ED`) | yes |
| 5 | the record of the party-focus actor (`0x003590D0`, `0x002E9B80`) | yes |
| 6 | the `n`-th member of manager 0 that has a record (`0x00263FF0`, `0x00263C30`, `0x00358940`) | yes |
| 7 | the matrix of map model `n` (`0x003A6FC0`), copied to `out` as it is, without the offset (`0x003A5368`-`0x003A5386`): the draw-list build `0x002F5550` stores each model's index in the 32 words at `0x0209A71C` under the anchor number its placement row names (`0x002F6533`-`0x002F6554`); `n` is the instance's byte `+0x376` while its `+0x368` bit `0x200` is set. `0x003A6FC0` returns 0 when the map model list `[0x0209A670]` is null or the model's word at `0x0209A71C` is `0xFFFF`, and the query then goes to `0x003A53DC` (`0x003A6FCE`, `0x003A6FE6`, `0x003A5366`). Otherwise it returns the model's placement matrix, the `0x40`-byte row of list `+0x188` that word `+2` of the model's `0x30`-byte entry in list `+0x178` names; when the model's `0x70`-byte entry in list `+0x1C0` has a matrix pointer at `+0x50`, it returns that entry instead, after `0x00217150` (through `0x00202D70`) has multiplied the placement matrix and `+0x50` into it (`0x003A6FF0`-`0x003A702E`) | no |
| 8 | the centre of the instance's targets as the position (`0x003A6C30`): the mean of the `n_hara` (`0x100`) translations of the render records of target slots 0 to count − 1 (`0x003A5640`, `0x00421E20`), the count being `+0x372`, or `0x02096B24` with `+0x378` bit `0x200`. `0x003A6C30` returns 0, and the query goes to `0x003A53DC`, with no targets or when any target has no live record (`0x003A6C73`, `0x003A6CBD`-`0x003A6CEF`, `0x003A5215`). It does not test what `0x00421E20` returns (`0x003A6D02`-`0x003A6D13`): a target whose record has no model (`+0x18` −1 or no `0x002ED570` entry, `0x00421E49`-`0x00421E77`) or no `n_hara` node (`0x00370FBF`-`0x00370FE3`, `0x00370E55`-`0x00370E65`) is still counted, with the translation an earlier target left in the buffer, or for the first target what the stack held | no |
| 9, 13 | the path object `0x003A8240(key, +0x4E)` finds, first advanced by `0x004FF0D0(object, 2.0)` while its `+0x103` bit `0x1` is clear, with the key the work object's byte `+0x42` (kind 9) or `[0x02F97348] + 0x388` (kind 13) | no |
| 10 | the targets' centre (`0x003A6C30`); the offset's height is added only when `0x0026E350` finds ground there | no |
| 12, or any other | no anchor: the identity matrix at the offset (`0x003A54DD`) | no |
| 14 | a screen position turned into a matrix (`0x0057A040`): the menu record's `+0x10`-`+0x18` for a menu-effect instance (id top nibble 4, `0x003B2CA0`), else `0x02096B2C`-`0x02096B34`. `0x0057A040(out, x, y, z)` returns 0 while byte `+0xDEA` of `[0x0209AC30]` is 0, and the query then places the identity at the offset (`0x0057A073`, `0x003A54D7`). Otherwise it puts the position into the translation of an identity matrix (`0x00203170`) and has `0x00217150` (through `0x00202D70`) multiply it with the matrix `0x0208ED10` (`0x002465C0`) into `out` (`0x0057A1BB`-`0x0057A1C3`). While `[0x0209AC30]` + `0x158` is set and its byte `+0x187` is 0, x and y go through `0x00561CA0` and `0x00561D30`, z is 0, and a copy of `0x0208ED10` with its `+0x30` and `+0x34` scaled by `[0x01F2CAF0]` (`0x0055F730`) is used (`0x0057A0A4`-`0x0057A142`). Otherwise the position is (x, y, z × 0.0001), with 10.5 added to y while `+0x158` is set, and −18.5 more when the current instance's word `+4` is 1 (`0x0024E3F0`) (`0x0057A144`-`0x0057A1AD`) | no |

On a record, the point kind picks the point; the point ids are those of
[character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table).
"Child" means a record of the record's tree with that point¹, for example the weapon a character
holds.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00426770` |

</details>

`0x00426770` asks the record itself first¹, then its first child `+0x08`², then
that child's children and next siblings `+0x0A` with their descendants, through `0x0042EF90` and the body
`0x0042DA00`³. Each hit replaces the stored result⁴,
so the last record in that order with the point gives it.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004267B7` |
| ² | `0x004267FC` |
| ³ | `0x00426829`, `0x00426844` |
| ⁴ | `0x004267C1`, `0x00426806`, `0x0042DA1F` |

</details>

| Point kind (`+0x49`) | Point |
|---|---|
| 1 | `model` (`0x101`), with the height `[0x02F97348] + 0x36C` while the instance's `+0x368` bit `0x800` is set |
| 2, 3 | slot 2 (`n_buki_r`) or 3 (`n_buki_l`) |
| 4, 5 | a child's `j_blade` (`0x200`) or `n_grip` (`0x201`) |
| 6 | bone `+0x4C` of the record's skeleton (`0x004220F0`) |
| 7 | bone `+0x4C` of the first child that has it (`0x00426650`, then `0x004220F0`) |
| 8, 9 | `n_hara` (`0x100`), then the position replaced by the focus point `+0x670` (`0x003E5700`) or by `+0x670` plus `+0x680` turned by the record's matrix (`0x003E5810`) |
| 10, 15-19 | a point of the record's box (`0x003E5130` for record kind 2, else `0x003E5070`) turned to face a reference (`0x0046F4B0`): the camera (10); the point twice as far beyond it from the camera, so it faces away (15); the owner's `n_hara` (16; the camera for record kind 1); the target's `n_hara` (17; the camera for kind 2); the targets' centre (18; the camera for kind 8); and for 19 the record's `model` point itself, facing the camera at its height |
| 11, 12 | slot 12 or 13 (`j_kao`) |
| 13, 14 | slot 0 (`n_buki_r`) or 1 (`n_buki_l`) |
| 20, 24 | the record's own points `0x107` and `0x108` (words `+0x2F4`, `+0x2F6`) |
| 21, 22, 25, 28 | a child's `@FCP` point `0x301`, `0x302`, `0x30A` or `0x307` |
| 23 | the record's `@FCP` point `0x300` |
| 26, 27 | the record's `@FCP` point `0x308` or `0x309`, with the kind-1 height rule |
| 29, 30 | slot 4 (`j_sebo_b`) or 5 (`j_kosi`) |
| 31, 36, 39 | a random point from list 0, 1 or 2 below, drawn once and then kept in the work object's `+0x40` (`0x003A69F0`) |
| 32 | `n_hara` at the ground height (`0x00264670` on the record's `+0x108`) |
| 33 | the focus point `+0x670` at the ground height |
| 34, 35 | slot 17 (`j_kaochild_s`) or 18 (`j_blade`) |
| 37, 38 | `n_hara` with the position replaced by `@FCP` section 1's point `+0xD4` (`0x003E5600`), at the ground height (37) or not (38). `0x003E5600` reads that point through the model block `+0x400` and its word `+2`, the address summed in 32 bits, with w 1.0, or takes (0, 0, 0) without a block, and turns it by the record's matrix `+0x180` (`0x003E5FA0` with kind 0, then `0x0046D0C0`) (`0x003E561B`-`0x003E567A`) |
| 40 | `model`, with the position replaced by section 9's point (`0x003E4F50`) |
| 0, or above 40 | `n_hara` |

When a point is missing the query falls back to `n_hara` and then to a child's `n_grip`¹.
On a record, and for record kinds 3 and 11, the position is then divided (`x / [0x02096810]`, `y / [0x02096814]`,
`z / [0x02096818]`, `0x003A478C`-`0x003A47B3`) by the published instance scale `0x02096810`. Unless `+0x4A` bit `0x2` is
set, the record's own scale² is applied when it is not 1, 1, 1³. The height rule
follows⁴:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A471A`-`0x003A4777` |
| ² | `0x003E5710` |
| ³ | `0x003A47B8`-`0x003A4861` |
| ⁴ | `0x003A4868`-`0x003A489F` |

</details>

| `+0x4A` bits `0xC` | Height |
|---|---|
| 0 | as resolved |
| 1 | 0 |
| 2 | `[0x02F97348] + 0x36C` while the instance's `+0x368` bit `0x800` is set, else the height of the record's `model` point |
| 3 | the ground height (`0x00264670` on the record's `+0x108`) |

The random lists hold point ids; `0x003A6E60(count)` draws the index:

| List | Count | Point ids |
|---|---|---|
| 0 (`0x01EFAC60`) | 15 | `0x100`, `0x301`, `0x302`, 12, 13, 0, 1, `0x300`, `0x17`, `0x18`, `0x307`, `0x30A`, 5, `0x19`, and as fifteenth entry the word at `0x01EFAC7C`, which is the first two count bytes (`0x060F`) |
| 1 (`0x01EFAC80`) | 6 | `0x100`, 13, 0, 1, `0x17`, `0x18` |
| 2 (`0x01EFAC90`) | 6 | `0x100`, 0, 1, `0x17`, `0x18`, 0 |

A drawn `0x100` is looked up on the record itself alone (`0x00421E20` at `0x003A6ABA` and `0x003A6B43`), and any other id
on the record and then its children in the order above (`0x00426770` at `0x003A6AFF` and `0x003A6B73`). When the
record has no such point, the query draws once more. Ids `0x17`-`0x19` lie past the 22-entry slot tables. A keyed skeleton
takes them as `@FCP` special ids¹; a named one would index the name table past its end.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003E5AD0`, `0x00421F46` |

</details>

`0x003A69F0(record, list, work, frame)` keeps the drawn id in the work object's word `+0x40` and `frame` (from
`0x003A4290` the element's frame `+0xFC`) in its `+0x44`; while `+0x44` is not −1 it only looks the kept id up again¹. The second draw is kept as well, whether or not the record has that point: `+0x44` is
set before that look-up².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A6A73`, `0x003A6B29` |
| ² | `0x003A6B14`-`0x003A6B2D` |

</details>

A missing point, or a list number above 2¹, gives 0, and the query then falls back to `n_hara`². An id other than `0x100` is looked up only on a live record³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003A6A19` |
| ² | `0x003A4BE0`, `0x003A471A` |
| ³ | `0x003A6AD6`-`0x003A6AF7`, `0x003A6B4A`-`0x003A6B6B` |

</details>

### Target slots

An instance names its targets in the dword array at `+0x10`, with its count in byte `+0x372`.
With bit `0x200` of word `+0x378` set, both readers below take the global list `0x02096A24` (count
`0x02096B24`) instead.

`0x003A5640(slot)` treats slot −1 as slot 0. In a kind-3 instance it returns the `+0x10` entry as it
is; otherwise it takes the `+0x90` entry, or the `+0x10` entry when that is 0, and returns it through
`0x002E9B80` (the first dword of the actor's `+0xC0` object, or −1).

`0x003A3E30(slot)` returns the `+0x10` entry, or −1 past the count. In a kind-1 instance whose word
`+0x368` is below `0x8000` it first checks the target¹: a target that fails
adds one to byte `+0x374` and gives −1, and a replacement that `0x00322760` reports goes into `+0x10`,
with the old entry kept at `+0x90`, after an effect `0x62` is played on it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003229E0`, `0x00322760` |
| ² | `0x003B02A0` |

</details>

`0x003A4220(id)` picks one of three lookups by the instance: `0x0036E620` when the bits under mask `0x7000` of word
`+0x36A` are 3, `0x0036E4B0` in a kind-2 instance, and `0x0036E4E0` (a 64-entry table at `0x022D97B0`)
otherwise or when the first finds nothing; it returns the result through `0x002E9B80`.

Two wrappers hand these to element handlers:

- `0x0024DCE0(mode, n)`, for `0x00524320`: mode 0 gives the current instance's owner `0x003A3FD0(−1)`
  (−1 with no instance current), mode 2 gives `0x003A4220(n)`, and mode 3 the render index of the
  n-th actor of manager 0¹ that has one²; any
  other mode, or no match, gives −1.
- `0x0024DDD0(&owner, &target)`, for `0x0045FD50` and `0x00529200`, returns `0x003A3FD0(slot)` and
  `0x003A6BA0(slot)` for the slot byte `+0x13B` of the current emitter `[0x02EBEF80]`.
- `0x003A6BA0(slot)` returns a kind-3 instance's `+0x10` entry for the slot (slot 0 for −1) as it is; otherwise it
  passes the slot's `+0x10` entry, or for −1 the `+0x90` entry and else the first `+0x10` one,
  through `0x002E9B80`. With `+0x378` bit `0x200` it reads the global list `0x02096A24` instead.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02098E10` |
| ² | `0x00358940`, `0x003589B0`, `0x002E9B80` |

</details>

The three 64-entry tables are filled by script verbs, each taking an index clamped, `n < 0 ? 0 : n > 63 ? 63 : n`
(0 to 63; `0x0036E880`, `0x0036E7E0`, `0x0036E7B0`), and storing the calling script's actor¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263F10`, `0x003589B0` |

</details>

| Verb | Table | Set | Clear |
|---|---|---|---|
| `effectactor(n)` (`0x0126`, `0x00352270`), from manager 3 | `0x022D99B0` | `0x0036E880` | `clear_effectactor` (`0x056F`, `0x00342010`): `0x0036E1A0` |
| `effectactor(n)` from any other manager | `0x022D97B0` | `0x0036E7E0` | `clear_effectactor`: `0x0036E160` |
| `bgeffectactor(n)` (`0x0570`, `0x00352940`) | `0x022D98B0` | `0x0036E7B0` | `clear_bgeffectactor` (`0x0571`, `0x003423C0`): `0x0036E040` |

The manager is the issuer's byte `+0x15`. A clear stores 0.

### Raw owner and target reads

Two more readers take the current instance `[0x02F97348]` without the `0x002E9B80` step:

- `0x003A6D90(slot)`: with `+0x378` bit `0x200` clear, −1 for a kind-3 instance, the `+0x10` entry for
  any slot other than −1 with no compare against the count `+0x372`, and for −1 the `+0x90` entry, or
  the first `+0x10` entry when that is 0. With the bit set, entry `slot` (0 for −1) of `0x02096A24`
  while it is below `0x02096B24`, else −1.
- `0x0024B6F0`, `0x0024C870` and `0x0024F9B0` call `0x003A6D90` with 0, and `0x003B99D0` with the byte `+0x10` of
  `[0x02EBA4F0]`¹.
- `0x003A4070(slot)`: with the bit set, `[0x02096A20]`. Otherwise −1 for a kind-3 instance, and for a
  kind-5, 6 or 9 instance whose request (`0x003B0BF0(+0x04)`) is missing or has target test `+0x11` =
  1; else the slot's `+0x90` entry, or the owner `+0x08` for slot −1 or a zero entry. `0x003B99D0`
  calls it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B9A5F` |
| ² | `0x003B9AA1` |

</details>

### Renaming an owner or target

`0x0024C600(old, new)` does nothing unless both ids are non-zero. It then replaces `old` by `new` in
the owner `+0x08` and in both target arrays `+0x10` and `+0x90` (count `+0x372`) of three sets of
instances:

- `0x002FBFA0`: every instance on the kind-1 list `0x020910F0[1]`¹, through `+0x348`;
- `0x003B0190`: the instance `+0x08` of each of the 36 request entries at `0x02EBEC00` whose handle is
  non-zero and whose target test `+0x11` is not 1;
- `0x003B14F0`: every instance on the kind-7 list `0x020910F0[7]`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x020910F8` |
| ² | `0x02091128` |

</details>

Its one caller is the party snapshot read `0x00326D60` (`0x00327117`,
[party slots](../Party/party-slots.md)). For each staged member it passes the unit id saved at
record `+4` and the handle `+0x08` of the unit that now holds the member's party record, when the
two differ.

## Related

- [Effect element runtime](effect-element-runtime.md): instances, emitters, the update and timeline tracks.
- [Effect drawing](effect-drawing.md): the display layers and the draw list.
- [Effect file loading](effect-file-loading.md): battle effect slots and the loaded-file queue.
- [Effects on actors and scripts](effects-on-actors-and-scripts.md): numbered effects on actors and script effect slots.
- [Effect element types](effect-element-types.md): what each type does in its methods.
- [Character render records](character-render-records.md): the records an anchor names.
- [Skeleton entries and bones](skeleton-entries-and-bones.md): the bones and bone points an anchor names.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 423 calls with 57 other topics</summary>

**Characters and objects** (explained on [hud](../Menus-And-HUD/hud.md), [debug menu](../Engine-Core/debug-menu.md), [frame update order](../Engine-Core/frame-update-order.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md), [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md), [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md), [ebp lighting lgt2](../EBP-Script-Files/ebp-lighting-lgt2.md), [ebp script container](../EBP-Script-Files/ebp-script-container.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [actor managers](../Characters-And-Objects/actor-managers.md), [target selection](../Battle-Actions/target-selection.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [field runtime](../Characters-And-Objects/field-runtime.md), [battle units](../Characters-And-Objects/battle-units.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is called by | [`0x003F1E90`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x0024B6F0`](effect-anchors-and-targets.md) | calls | [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x0024C870`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x0026A3A0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x0026A430`](effect-file-loading.md) (on effect file loading)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x0024DCE0`](effect-anchors-and-targets.md) | calls | [`0x00263C30`](effect-anchors-and-targets.md)<br>[`0x00263FF0`](effect-anchors-and-targets.md)<br>[`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes)<br>[`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |
| [`0x0024F9B0`](effect-file-loading.md) (on effect file loading) | calls | [`0x0026A430`](effect-file-loading.md) (on effect file loading)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x00263C30`](effect-anchors-and-targets.md) | is called by | [`0x0032F1B0`](../Scripts-And-Script-Commands/event-scenes.md) Actor resource: finalize manager runtime after loads (on event scenes) |
| [`0x00263F10`](effect-anchors-and-targets.md) | calls | [`0x003587C0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is called by | [`0x0032F1B0`](../Scripts-And-Script-Commands/event-scenes.md) Actor resource: finalize manager runtime after loads (on event scenes)<br>[`0x0032F850`](../Compiler-And-C-Runtime/memory-and-allocation.md) Actor resource: on definition payload loaded (on memory and allocation)<br>[`0x0032FA10`](../EBP-Script-Files/ebp-camera-tables.md) (on ebp camera tables)<br>[`0x0032FAC0`](../EBP-Script-Files/ebp-camera-tables.md) (on ebp camera tables)<br>[`0x0032FB70`](../EBP-Script-Files/ebp-actor-manifest.md) (on ebp actor manifest)<br>[`0x00330060`](../Game-Files-And-Data-Tables/tim2-images.md) (on tim2 images)<br>[`0x00330110`](../EBP-Script-Files/ebp-lighting-lgt2.md) (on ebp lighting lgt2)<br>[`0x00330190`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00330220`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003302B0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003304A0`](../EBP-Script-Files/ebp-position-entries.md) Actor resource: on primary payload loaded and dispatch subresources (on ebp position entries) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is also called by | [`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions)<br>[`0x00331610`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x003316B0`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00331760`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x003317C0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00331820`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump)<br>[`0x00332130`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x003587C0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens)<br>[`0x0035A590`](effect-anchors-and-targets.md)<br>[`0x0035A7A0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0035A990`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is also called by | [`0x003B6F80`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003DB1F0`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x003DBCF0`](../Scripts-And-Script-Commands/script-requests.md) Actor resource: allocate and submit entry (on script requests)<br>[`0x003DDC20`](../Characters-And-Objects/actor-managers.md) (on actor managers)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x00264670`](effect-anchors-and-targets.md) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x003B73B0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003B7440`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003B7510`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x002E9B80`](effect-anchors-and-targets.md) | calls | [`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x00322760`](../Battle-Actions/target-selection.md) (on target selection) | calls | [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens)<br>[`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |
| [`0x003229E0`](effect-anchors-and-targets.md) | calls | [`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x00326D60`](effect-anchors-and-targets.md) | calls | [`0x00236820`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item)<br>[`0x00236850`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets)<br>[`0x00263E30`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor work: get battle unit raw (on character se tables chse)<br>[`0x0030A880`](../Enemy-AI-And-Gambits/enmity.md) (on enmity)<br>[`0x0031B770`](../Enemy-AI-And-Gambits/gambit-conditions.md) Battle unit: find by combatant id (on gambit conditions)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x00352270`](effect-anchors-and-targets.md) | calls | [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |
| [`0x00352940`](effect-anchors-and-targets.md) | calls | [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x0025AE00`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0025B070`](../Characters-And-Objects/actor-lifecycle.md) Actor system: release manager records (on actor lifecycle)<br>[`0x0025B250`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025B820`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x0025C070`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0025C170`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00263A30`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00264010`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00264050`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00265A20`](../Engine-Core/frame-update-order.md) Actor system: bind battle units for eligible records (on frame update order)<br>[`0x00266C50`](../EBP-Script-Files/ebp-script-image.md) (on ebp script image) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is also called by | [`0x00268B10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x002693D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00269800`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x00269AD0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00269BA0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0026B8E0`](effect-anchors-and-targets.md)<br>[`0x0026CE60`](../Characters-And-Objects/actor-managers.md) Actor system: initialize manager runtime (on actor managers)<br>[`0x0026D3E0`](../Scripts-And-Script-Commands/script-variables.md) (on script variables)<br>[`0x0035A590`](effect-anchors-and-targets.md)<br>[`0x0035A7A0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0035A990`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is also called by | [`0x003B6F80`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003DB1F0`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x00234480`](../Characters-And-Objects/battle-unit-fields.md) Battle unit: allocate slot and bind actor (on battle unit fields)<br>[`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x00268650`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x003B6F80`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x0025B600`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00263050`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x00263230`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x00263AC0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00264010`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00264050`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability)<br>[`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse)<br>[`0x0026DFB0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x003A40F0`](effect-anchors-and-targets.md) | calls | [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |
| [`0x003A4290`](effect-anchors-and-targets.md) | calls | [`0x00263C30`](effect-anchors-and-targets.md)<br>[`0x00263FF0`](effect-anchors-and-targets.md)<br>[`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes)<br>[`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |
| [`0x003A56F0`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x00263C30`](effect-anchors-and-targets.md)<br>[`0x00263FF0`](effect-anchors-and-targets.md)<br>[`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens)<br>[`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes)<br>[`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry |

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md), [animation sounds](../Sound-And-Music/animation-sounds.md), [force fight mode](../Engine-Core/force-fight-mode.md), [map sounds](../Sound-And-Music/map-sounds.md), [audio manager](../Sound-And-Music/audio-manager.md), [sound effects](../Sound-And-Music/sound-effects.md), [sound banks](../Sound-And-Music/sound-banks.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x002E9B80`](effect-anchors-and-targets.md) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003A3FD0`](position-to-scalar.md) (on position to scalar) | is called by | [`0x003B99D0`](effect-anchors-and-targets.md) |
| [`0x003A4070`](effect-anchors-and-targets.md) | is called by | [`0x003B99D0`](effect-anchors-and-targets.md) |
| [`0x003A6BA0`](effect-anchors-and-targets.md) | is called by | [`0x003B99D0`](effect-anchors-and-targets.md) |
| [`0x003A6D90`](effect-anchors-and-targets.md) | is called by | [`0x003B99D0`](effect-anchors-and-targets.md) |
| [`0x003A8240`](effect-anchors-and-targets.md) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound)<br>[`0x003B99D0`](effect-anchors-and-targets.md) |
| [`0x003B99D0`](effect-anchors-and-targets.md) | calls | [`0x002DEE80`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DEF40`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DEFA0`](../Sound-And-Music/spatial-sound.md) (on spatial sound)<br>[`0x002DF0F0`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DF150`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x002DF1A0`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x003616F0`](../Sound-And-Music/map-sounds.md) (on map sounds)<br>[`0x003617B0`](../Sound-And-Music/spatial-sound.md) (on spatial sound)<br>[`0x00361CF0`](../Sound-And-Music/animation-sounds.md) (on animation sounds)<br>[`0x003A0E20`](../Sound-And-Music/sound-banks.md) (on sound banks)<br>[`0x003A0E50`](../Sound-And-Music/animation-sounds.md) (on animation sounds)<br>[`0x003A1070`](../Sound-And-Music/sound-banks.md) (on sound banks) |
| [`0x003B99D0`](effect-anchors-and-targets.md) | also calls | [`0x003D7C50`](effect-anchors-and-targets.md) |
| [`0x00421E20`](effect-anchors-and-targets.md) | is called by | [`0x00332C40`](../Sound-And-Music/spatial-sound.md) (on spatial sound)<br>[`0x003B99D0`](effect-anchors-and-targets.md) |

**Battle actions** (explained on [traps](../World-Areas-And-Travel/traps.md), [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [quickenings and summons](../Battle-Actions/quickenings-and-summons.md), [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [jump thunks](../Engine-Core/jump-thunks.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x002F8060`](../World-Areas-And-Travel/traps.md) Battle unit: try trigger nearby authored field action (on traps)<br>[`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect)<br>[`0x00320E10`](../Battle-Actions/action-range.md) (on action range) |
| [`0x003229E0`](effect-anchors-and-targets.md) | calls | [`0x002FFA60`](../Battle-Actions/target-selection.md) Battle action: is target eligible for current action (on target selection)<br>[`0x00306BB0`](../Battle-Actions/quickenings-and-summons.md) (on quickenings and summons) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over)<br>[`0x00325260`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle action timeline event (on ko and game over) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00317E60`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00319090`](../Characters-And-Objects/battle-units.md) (on battle units) |

**Damage and battle formulas** (explained on [spawn record fields](../Enemy-Spawning/spawn-record-fields.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00384F40`](../Battle-Actions/action-results.md) (on action results) |

**Engine core** (explained on [startup constants](../Engine-Core/startup-constants.md), [screen mode and aspect](screen-mode-and-aspect.md), [global state accessors](../Engine-Core/global-state-accessors.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003820C0`](scripted-camera.md) (on scripted camera) | calls | [`0x00229D20`](screen-mode-and-aspect.md) (on screen mode and aspect)<br>[`0x00229D60`](screen-mode-and-aspect.md) (on screen mode and aspect) |
| [`0x003B99D0`](effect-anchors-and-targets.md) | calls | [`0x001EDDA0`](effect-lifecycle.md) (on effect lifecycle) |
| [`0x00524320`](effect-anchors-and-targets.md) | calls | [`0x001EDDA0`](effect-lifecycle.md) (on effect lifecycle) |

**Gameplay** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [bestiary](../Enemy-Spawning/bestiary.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is called by | [`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement)<br>[`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement) |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263FF0`](effect-anchors-and-targets.md) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x002E09A0`](../Menus-And-HUD/menus.md) (on menus) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00226BE0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |

**Movement and pathfinding** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [bestiary](../Enemy-Spawning/bestiary.md), [force fight mode](../Engine-Core/force-fight-mode.md), [traps](../World-Areas-And-Travel/traps.md), [party control modes](../Engine-Core/party-control-modes.md), [party slots](../Party/party-slots.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md), [frame update order](../Engine-Core/frame-update-order.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [world lock](../Scripts-And-Script-Commands/world-lock.md), [battle units](../Characters-And-Objects/battle-units.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [party data](../Party/party-data.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [collision mesh movement](../Movement-And-Pathfinding/collision-mesh-movement.md), [texture animation lists ta](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [player movement](../Movement-And-Pathfinding/player-movement.md), [debug menu](../Engine-Core/debug-menu.md), [effect file loading](effect-file-loading.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is called by | [`0x0022EF20`](../Movement-And-Pathfinding/collision-mesh-movement.md) (on collision mesh movement)<br>[`0x00230790`](../Movement-And-Pathfinding/collision-mesh-movement.md) (on collision mesh movement)<br>[`0x0026EB30`](../World-Areas-And-Travel/weather.md) (on weather)<br>[`0x00334220`](animation-playback.md) (on animation playback)<br>[`0x00334AB0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00334E00`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00335B60`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: test forward step clearance (on battle locomotion)<br>[`0x00336E40`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x00339F00`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033A3D0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033BAA0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion) |
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is also called by | [`0x0033C310`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033CBF0`](../World-Areas-And-Travel/traps.md) (on traps)<br>[`0x0033CC80`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033D890`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033DB60`](../EBP-Script-Files/ebp-position-entries.md) (on ebp position entries)<br>[`0x0033DFD0`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x003ED190`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x003ED3F0`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |
| [`0x0024B6F0`](effect-anchors-and-targets.md) | calls | [`0x00265200`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x0024C600`](effect-anchors-and-targets.md) | is called by | [`0x00326D60`](effect-anchors-and-targets.md) |
| [`0x0024C870`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x0024C6B0`](effect-element-runtime.md) (on effect element runtime)<br>[`0x0026AF80`](effect-file-loading.md) (on effect file loading)<br>[`0x0026B5A0`](effect-file-loading.md) (on effect file loading) |
| [`0x0024C870`](effect-element-runtime.md) (on effect element runtime) | is called by | [`0x0024C6B0`](effect-element-runtime.md) (on effect element runtime) |
| [`0x0024F9B0`](effect-file-loading.md) (on effect file loading) | calls | [`0x0026AF80`](effect-file-loading.md) (on effect file loading)<br>[`0x0026B5A0`](effect-file-loading.md) (on effect file loading) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is called by | [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00392740`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |
| [`0x00264670`](effect-anchors-and-targets.md) | is called by | [`0x003B7F40`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x0024B6F0`](effect-anchors-and-targets.md)<br>[`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002EBFA0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x002EC2C0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock)<br>[`0x00300310`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x00336710`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: build solver context (on battle locomotion)<br>[`0x00337C10`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00337D90`](../Random-Numbers/which-roll-uses-which-generator.md) (on which roll uses which generator) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is also called by | [`0x0033CA00`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x003B7E20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003B7F40`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00505240`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |
| [`0x0026E350`](effect-anchors-and-targets.md) | calls | [`0x00231820`](../Movement-And-Pathfinding/collision-mesh-movement.md) (on collision mesh movement)<br>[`0x00231900`](../Movement-And-Pathfinding/collision-mesh-movement.md) (on collision mesh movement) |
| [`0x002F5550`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) | calls | [`0x0026E5D0`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x0026E5F0`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes) |
| [`0x00326D60`](effect-anchors-and-targets.md) | calls | [`0x003003F0`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position and facing (on spawn record fields)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x00392740`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x002E5610`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Movement: integrate position and measure displacement (on heading speed to position delta)<br>[`0x002EBFA0`](../Scripts-And-Script-Commands/world-lock.md) (on world lock) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x0026D6F0`](../Scripts-And-Script-Commands/world-lock.md) Movement: set requested speed (on world lock)<br>[`0x0026D810`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002E5180`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) (on heading speed to position delta)<br>[`0x00319490`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x00325D90`](../Scripts-And-Script-Commands/battle-verbs.md) Battle unit: can advance combat navigation (on battle verbs)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x00326D60`](effect-anchors-and-targets.md)<br>[`0x00343E20`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00345430`](../Scripts-And-Script-Commands/verb-table.md) (on verb table) |
| [`0x003820C0`](scripted-camera.md) (on scripted camera) | calls | [`0x00233230`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x0026E500`](field-camera.md) (on field camera) |
| [`0x003A4290`](effect-anchors-and-targets.md) | calls | [`0x00264670`](effect-anchors-and-targets.md)<br>[`0x0026E350`](effect-anchors-and-targets.md) |
| [`0x003A56F0`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x00264670`](effect-anchors-and-targets.md)<br>[`0x0026E350`](effect-anchors-and-targets.md) |
| [`0x003A6D90`](effect-anchors-and-targets.md) | is called by | [`0x0024B6F0`](effect-anchors-and-targets.md)<br>[`0x0024C870`](effect-element-runtime.md) (on effect element runtime)<br>[`0x0024F9B0`](effect-file-loading.md) (on effect file loading) |

**Party** (explained on [party control modes](../Engine-Core/party-control-modes.md), [map screens](../Menus-And-HUD/map-screens.md), [frame update order](../Engine-Core/frame-update-order.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [player movement](../Movement-And-Pathfinding/player-movement.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md), [debug menu](../Engine-Core/debug-menu.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00303CC0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x00304180`](../Engine-Core/party-control-modes.md) (on party control modes)<br>[`0x00359150`](effect-anchors-and-targets.md) Party focus: try get current actor world position |
| [`0x00326D60`](effect-anchors-and-targets.md) | calls | [`0x003590D0`](effect-anchors-and-targets.md) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x00269C70`](../Party/party-members.md) (on party members)<br>[`0x00326500`](../Party/party-leader.md) Party focus: select and request default actor (on party leader)<br>[`0x00353530`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x0050C610`](../Party/party-leader.md) (on party leader)<br>[`0x0050D2F0`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00263770`](../World-Areas-And-Travel/doors-gates-and-map-changes.md) (on doors gates and map changes)<br>[`0x00269C70`](../Party/party-members.md) (on party members)<br>[`0x00327270`](../Party/party-leader.md) (on party leader)<br>[`0x003272A0`](../World-Areas-And-Travel/treasure-chests.md) Battle unit: get party leader (on treasure chests)<br>[`0x003272F0`](../Party/party-leader.md) (on party leader)<br>[`0x003273B0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |
| [`0x003A4290`](effect-anchors-and-targets.md) | calls | [`0x003590D0`](effect-anchors-and-targets.md) |
| [`0x003A56F0`](effect-element-runtime.md) (on effect element runtime) | calls | [`0x003590D0`](effect-anchors-and-targets.md) |

**Game files and data tables** (explained on [resource sections](../Game-Files-And-Data-Tables/resource-sections.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00421E20`](effect-anchors-and-targets.md) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones) |
| [`0x004220F0`](effect-anchors-and-targets.md) | calls | [`0x002ED570`](skeleton-entries-and-bones.md) Resource table: resolve entry by index (on skeleton entries and bones) |

**Rewards: EXP, LP, gil and loot** (explained on [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x002FB150`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) Loot: find overlapping pickup index (on loot pickups)<br>[`0x00312280`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle unit: process defeat rewards and loot (on strong and weak mode) |

**Scripts and script commands** (explained on [generated function families](../Compiler-And-C-Runtime/generated-function-families.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [script censuses](../Story-Events-And-Hunts/script-censuses.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [field runtime](../Characters-And-Objects/field-runtime.md), [debug menu](../Engine-Core/debug-menu.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [force fight mode](../Engine-Core/force-fight-mode.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [actor record](../Characters-And-Objects/actor-record.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is called by | [`0x00356160`](effect-anchors-and-targets.md) |
| [`0x00263C30`](effect-anchors-and-targets.md) | is called by | [`0x0034AF50`](effect-anchors-and-targets.md) |
| [`0x00263F10`](effect-anchors-and-targets.md) | is called by | [`0x00340230`](../Compiler-And-C-Runtime/generated-function-families.md) (on generated function families)<br>[`0x00340640`](effect-anchors-and-targets.md)<br>[`0x00340CB0`](effect-anchors-and-targets.md)<br>[`0x00341070`](effect-anchors-and-targets.md)<br>[`0x00341140`](effect-anchors-and-targets.md)<br>[`0x00341690`](effect-anchors-and-targets.md)<br>[`0x00341B20`](effect-anchors-and-targets.md)<br>[`0x00341EE0`](effect-anchors-and-targets.md)<br>[`0x00342150`](effect-anchors-and-targets.md)<br>[`0x003421D0`](effect-anchors-and-targets.md)<br>[`0x00342500`](effect-anchors-and-targets.md)<br>[`0x003429F0`](effect-anchors-and-targets.md) |
| [`0x00263F10`](effect-anchors-and-targets.md) | is also called by | [`0x00342D40`](effect-anchors-and-targets.md)<br>[`0x00343180`](effect-anchors-and-targets.md)<br>[`0x00343290`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x003434F0`](effect-anchors-and-targets.md)<br>[`0x003438F0`](effect-anchors-and-targets.md)<br>[`0x00344CC0`](effect-anchors-and-targets.md)<br>[`0x003460C0`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346620`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00346A10`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs)<br>[`0x00348800`](effect-anchors-and-targets.md)<br>[`0x00348C50`](../Compiler-And-C-Runtime/generated-function-families.md) (on generated function families)<br>[`0x00349220`](effect-anchors-and-targets.md) |
| [`0x00263F10`](effect-anchors-and-targets.md) | is also called by | [`0x00349620`](effect-anchors-and-targets.md)<br>[`0x00349AD0`](effect-anchors-and-targets.md)<br>[`0x0034A110`](effect-anchors-and-targets.md)<br>[`0x0034A4C0`](effect-anchors-and-targets.md)<br>[`0x0034AAD0`](effect-anchors-and-targets.md)<br>[`0x0034B060`](effect-anchors-and-targets.md)<br>[`0x0034B5D0`](effect-anchors-and-targets.md)<br>[`0x0034BB80`](effect-anchors-and-targets.md)<br>[`0x0034C0C0`](effect-anchors-and-targets.md)<br>[`0x0034C1D0`](effect-anchors-and-targets.md)<br>[`0x0034C500`](effect-anchors-and-targets.md)<br>[`0x0034C6A0`](effect-anchors-and-targets.md) |
| [`0x00263F10`](effect-anchors-and-targets.md) | is also called by | [`0x0034C8D0`](effect-anchors-and-targets.md)<br>[`0x0034CC60`](effect-anchors-and-targets.md)<br>[`0x0034DA30`](effect-anchors-and-targets.md)<br>[`0x0034E190`](effect-anchors-and-targets.md)<br>[`0x00352270`](effect-anchors-and-targets.md)<br>[`0x00352940`](effect-anchors-and-targets.md)<br>[`0x00357F00`](../Scripts-And-Script-Commands/battle-verbs.md) (on battle verbs) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is called by | [`0x0033F7F0`](effect-anchors-and-targets.md)<br>[`0x00342490`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses)<br>[`0x00342A30`](effect-anchors-and-targets.md)<br>[`0x00343010`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses)<br>[`0x00343470`](../Story-Events-And-Hunts/script-censuses.md) (on script censuses)<br>[`0x00348130`](effect-anchors-and-targets.md)<br>[`0x003484A0`](effect-anchors-and-targets.md)<br>[`0x00348A70`](effect-anchors-and-targets.md)<br>[`0x00348DA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0034AF50`](effect-anchors-and-targets.md)<br>[`0x0034E460`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0034F3C0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x00263FF0`](effect-anchors-and-targets.md) | is also called by | [`0x0034FC50`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00351C90`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00352000`](effect-anchors-and-targets.md)<br>[`0x00352560`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x00352D70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x00357170`](effect-anchors-and-targets.md)<br>[`0x003574B0`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x0050D0C0`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x00264670`](effect-anchors-and-targets.md) | is called by | [`0x00343520`](effect-anchors-and-targets.md) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x0033FD60`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x00344AF0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00345180`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00345830`](../Battle-Actions/action-range.md) (on action range)<br>[`0x003461B0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00346710`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00346D40`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00347170`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00347580`](../Battle-Actions/action-range.md) (on action range)<br>[`0x003478A0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00347AB0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00347FF0`](../Battle-Actions/action-range.md) (on action range) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is also called by | [`0x0034BE50`](../Battle-Actions/action-range.md) (on action range)<br>[`0x0034CC00`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00350DD0`](effect-anchors-and-targets.md)<br>[`0x003516E0`](effect-anchors-and-targets.md)<br>[`0x003562B0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00357DE0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x0050E060`](effect-anchors-and-targets.md)<br>[`0x0050F6E0`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00510040`](../Battle-Actions/action-range.md) (on action range)<br>[`0x00510080`](../Battle-Actions/action-range.md) (on action range)<br>[`0x005100C0`](../Battle-Actions/action-range.md) (on action range) |
| [`0x00342010`](effect-anchors-and-targets.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003423C0`](effect-anchors-and-targets.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352270`](effect-anchors-and-targets.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352940`](effect-anchors-and-targets.md) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x0025E4C0`](../Scripts-And-Script-Commands/script-interpreter.md) World actor script vm: interpret bytecode (on script interpreter)<br>[`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter)<br>[`0x00267420`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x002674B0`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x00346FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0034A640`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships)<br>[`0x0034B350`](effect-anchors-and-targets.md)<br>[`0x0034C500`](effect-anchors-and-targets.md)<br>[`0x0034C630`](effect-anchors-and-targets.md)<br>[`0x0034CC60`](effect-anchors-and-targets.md)<br>[`0x00350DD0`](effect-anchors-and-targets.md)<br>[`0x003516E0`](effect-anchors-and-targets.md) |
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is also called by | [`0x00357620`](effect-anchors-and-targets.md)<br>[`0x0050D5E0`](effect-anchors-and-targets.md)<br>[`0x0050D780`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x0050D860`](../Scripts-And-Script-Commands/script-name-bindings.md) (on script name bindings)<br>[`0x0050DB80`](effect-anchors-and-targets.md) |
| [`0x003589B0`](effect-anchors-and-targets.md) Actor handle: encode registry entry | is called by | [`0x00342150`](effect-anchors-and-targets.md)<br>[`0x00342D40`](effect-anchors-and-targets.md)<br>[`0x003438F0`](effect-anchors-and-targets.md)<br>[`0x00349C90`](../Characters-And-Objects/actor-lifecycle.md) (on actor lifecycle)<br>[`0x0034B5D0`](effect-anchors-and-targets.md)<br>[`0x0034BB80`](effect-anchors-and-targets.md)<br>[`0x00352270`](effect-anchors-and-targets.md)<br>[`0x00352940`](effect-anchors-and-targets.md)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00357620`](effect-anchors-and-targets.md)<br>[`0x0050C7A0`](effect-anchors-and-targets.md) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00341CB0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00345800`](effect-anchors-and-targets.md)<br>[`0x00346FA0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x0034F800`](effect-anchors-and-targets.md)<br>[`0x0034FF00`](effect-anchors-and-targets.md)<br>[`0x00350DD0`](effect-anchors-and-targets.md)<br>[`0x003516E0`](effect-anchors-and-targets.md)<br>[`0x00352580`](effect-anchors-and-targets.md)<br>[`0x003530F0`](effect-anchors-and-targets.md)<br>[`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests)<br>[`0x00356570`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests)<br>[`0x0050C7A0`](effect-anchors-and-targets.md) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is also called by | [`0x0050C930`](effect-anchors-and-targets.md)<br>[`0x0050E060`](effect-anchors-and-targets.md) |
| [`0x0036E040`](effect-anchors-and-targets.md) | is called by | [`0x003423C0`](effect-anchors-and-targets.md) |
| [`0x0036E160`](effect-anchors-and-targets.md) | is called by | [`0x00342010`](effect-anchors-and-targets.md) |
| [`0x0036E1A0`](effect-anchors-and-targets.md) | is called by | [`0x00342010`](effect-anchors-and-targets.md) |
| [`0x0036E7B0`](effect-anchors-and-targets.md) | is called by | [`0x00352940`](effect-anchors-and-targets.md) |
| [`0x0036E7E0`](effect-anchors-and-targets.md) | is called by | [`0x00352270`](effect-anchors-and-targets.md) |
| [`0x0036E880`](effect-anchors-and-targets.md) | is called by | [`0x00352270`](effect-anchors-and-targets.md) |

**Enemy spawning** (explained on [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00234AF0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x00234DA0`](../Party/party-slots.md) Spawn: validate candidate distance to players (on party slots)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning) |

**Menus and HUD** (explained on [hud](../Menus-And-HUD/hud.md), [menu lists](../Menus-And-HUD/menu-lists.md), [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [map screens](../Menus-And-HUD/map-screens.md), [battle units](../Characters-And-Objects/battle-units.md), [party list](../Menus-And-HUD/party-list.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00203170`](legacy-ps2-gs-layer.md) (on legacy ps2 gs layer) | is called by | [`0x00247AE0`](../Menus-And-HUD/widgets.md) (on widgets)<br>[`0x002D2600`](../Menus-And-HUD/menu-lists.md) (on menu lists)<br>[`0x002D28E0`](../Menus-And-HUD/text-drawing.md) (on text drawing)<br>[`0x00368010`](../Menus-And-HUD/menu-lists.md) (on menu lists)<br>[`0x003C5500`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003F26F0`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x003F2A70`](../Menus-And-HUD/hud.md) (on hud) |
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x003C5130`](../Characters-And-Objects/battle-units.md) (on battle units) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x00299BD0`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002C7660`](../Menus-And-HUD/battle-menu.md) (on battle menu) |

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) | is called by | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x002623A0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x003590D0`](effect-anchors-and-targets.md) | is called by | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x002623A0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00326D60`](effect-anchors-and-targets.md) | calls | [`0x00313F60`](../Items-Equipment-Shops-And-Licenses/equipping-an-item.md) (on equipping an item) |

</details>
