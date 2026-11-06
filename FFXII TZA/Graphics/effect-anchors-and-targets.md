---
title: "Effect anchors and targets: the target and anchor queries, target slots, and reading and renaming an owner or target"
kind: "system"
category: "Graphics"
addresses: "0x020910F0, 0x02F97348, 0x003A4290, 0x003A40F0, 0x003A6FC0, 0x003A6C30, 0x003A69F0, 0x0057A040, 0x004220F0, 0x0046F4B0, 0x003E5700, 0x003E5600, 0x003E5810, 0x01EFAC60, 0x0209A71C"
---

## What the player sees

An effect piece follows the point it is anchored to: a bone of the character that cast it, a point
on its target, or a fixed spot in the world.

## How it works

### Target and anchor queries

Some tails ask for a point from a sub-record. `0x002F3360` switches on the sub-record's byte `+0x90`;
value 3 calls `0x003A56F0`, which samples a vector track (`0x00430B90`) and switches on the byte `+0x48`
minus 1 over 14 cases (`0x002F3384`–`0x002F33EA`, `0x003A575E`–`0x003A5797`). `0x003A4290` has the same
14-case switch on the same byte (`0x003A4303`–`0x003A4319`).

Their arms are in
[`effect-element-runtime-switch-family-3a42-3a56.tsv`](effect-element-runtime-switch-family-3a42-3a56.tsv); [`effect-element-runtime-switch-family-jump-tables.tsv`](effect-element-runtime-switch-family-jump-tables.tsv)
decodes `0x00442170` and `0x00442460` (the emitter-record subtype switches) and the record-store
fronts `0x00500980` / `0x00500850`, together with dispatchers outside the effect code.

### Columns of effect-element-runtime-switch-family-3a42-3a56.tsv

One row per value of the byte `+0x48`, 1 to 14, between a first row for the switch head and two last rows for the
switches inside the kind-6 arm, 17 rows. The arms agree with the tables at `0x003A5540` (`0x003A4290`) and
`0x003A68E4` (`0x003A56F0`): all 28 match.

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
`+0xFC` (`0x00430B90`, `0x003A4303`), resolves the anchor descriptor into the matrix `out`, adds the offset to `out`'s
position and returns 1. When the anchor cannot be resolved it keeps `work` from the frame before, or on frame 0
zeroes `work` and `out` and returns 0 (`0x003A53DC`-`0x003A542B`). The descriptor's bytes:

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
| 8 | the centre of the instance's targets as the position (`0x003A6C30`): the mean of the `n_hara` (`0x100`) translations of the render records of target slots 0 to count − 1 (`0x003A5640`, `0x00421E20`), the count being `+0x372`, or `0x02096B24` with `+0x378` bit `0x200`. `0x003A6C30` returns 0, and the query goes to `0x003A53DC`, with no targets or when any target has no live record (`0x003A6C73`, `0x003A6CBD`-`0x003A6CEF`, `0x003A5215`) | no |
| 9, 13 | the path object `0x003A8240(key, +0x4E)` finds, first advanced by `0x004FF0D0(object, 2.0)` while its `+0x103` bit `0x1` is clear, with the key the work object's byte `+0x42` (kind 9) or `[0x02F97348] + 0x388` (kind 13) | no |
| 10 | the targets' centre (`0x003A6C30`); the offset's height is added only when `0x0026E350` finds ground there | no |
| 12, or any other | no anchor: the identity matrix at the offset (`0x003A54DD`) | no |
| 14 | a screen position turned into a matrix (`0x0057A040`): the menu record's `+0x10`-`+0x18` for a menu-effect instance (id top nibble 4, `0x003B2CA0`), else `0x02096B2C`-`0x02096B34`. `0x0057A040(out, x, y, z)` returns 0 while byte `+0xDEA` of `[0x0209AC30]` is 0, and the query then places the identity at the offset (`0x0057A073`, `0x003A54D7`). Otherwise it puts the position into the translation of an identity matrix (`0x00203170`) and has `0x00217150` (through `0x00202D70`) multiply it with the matrix `0x0208ED10` (`0x002465C0`) into `out` (`0x0057A1BB`-`0x0057A1C3`). While `[0x0209AC30]` + `0x158` is set and its byte `+0x187` is 0, x and y go through `0x00561CA0` and `0x00561D30`, z is 0, and a copy of `0x0208ED10` with its `+0x30` and `+0x34` scaled by `[0x01F2CAF0]` (`0x0055F730`) is used (`0x0057A0A4`-`0x0057A142`). Otherwise the position is (x, y, z × 0.0001), with 10.5 added to y while `+0x158` is set, and −18.5 more when the current instance's word `+4` is 1 (`0x0024E3F0`) (`0x0057A144`-`0x0057A1AD`) | no |

On a record, the point kind picks the point; the point ids are those of
[character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table).
"Child" means a record of the record's tree with that point (`0x00426770`), for example the weapon a character
holds.

`0x00426770` asks the record itself first (`0x004267B7`), then its first child `+0x08` (`0x004267FC`), then
that child's children and next siblings `+0x0A` with their descendants, through `0x0042EF90` and the body
`0x0042DA00` (`0x00426829`, `0x00426844`). Each hit replaces the stored result (`0x004267C1`, `0x00426806`, `0x0042DA1F`),
so the last record in that order with the point gives it.

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

When a point is missing the query falls back to `n_hara` and then to a child's `n_grip` (`0x003A471A`-`0x003A4777`).
On a record, and for record kinds 3 and 11, the position is then divided (`x / [0x02096810]`, `y / [0x02096814]`,
`z / [0x02096818]`, `0x003A478C`-`0x003A47B3`) by the published instance scale `0x02096810`. Unless `+0x4A` bit `0x2` is
set, the record's own scale (`0x003E5710`) is applied when it is not 1, 1, 1 (`0x003A47B8`-`0x003A4861`). The height rule
follows (`0x003A4868`-`0x003A489F`):

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
takes them as `@FCP` special ids (`0x003E5AD0`, `0x00421F46`); a named one would index the name table past its end.

`0x003A69F0(record, list, work, frame)` keeps the drawn id in the work object's word `+0x40` and `frame` (from
`0x003A4290` the element's frame `+0xFC`) in its `+0x44`; while `+0x44` is not −1 it only looks the kept id up again
(`0x003A6A73`, `0x003A6B29`). The second draw is kept as well, whether or not the record has that point: `+0x44` is
set before that look-up (`0x003A6B14`-`0x003A6B2D`).

A missing point, or a list number above 2 (`0x003A6A19`), gives 0, and the query then falls back to `n_hara`
(`0x003A4BE0`, `0x003A471A`). An id other than `0x100` is looked up only on a live record
(`0x003A6AD6`-`0x003A6AF7`, `0x003A6B4A`-`0x003A6B6B`).

### Target slots

An instance names its targets in the dword array at `+0x10`, with its count in byte `+0x372`.
With bit `0x200` of word `+0x378` set, both readers below take the global list `0x02096A24` (count
`0x02096B24`) instead.

`0x003A5640(slot)` treats slot −1 as slot 0. In a kind-3 instance it returns the `+0x10` entry as it
is; otherwise it takes the `+0x90` entry, or the `+0x10` entry when that is 0, and returns it through
`0x002E9B80` (the first dword of the actor's `+0xC0` object, or −1).

`0x003A3E30(slot)` returns the `+0x10` entry, or −1 past the count. In a kind-1 instance whose word
`+0x368` is below `0x8000` it first checks the target (`0x003229E0`, `0x00322760`): a target that fails
adds one to byte `+0x374` and gives −1, and a replacement that `0x00322760` reports goes into `+0x10`,
with the old entry kept at `+0x90`, after an effect `0x62` is played on it (`0x003B02A0`).

`0x003A4220(id)` picks one of three lookups by the instance: `0x0036E620` when the bits under mask `0x7000` of word
`+0x36A` are 3, `0x0036E4B0` in a kind-2 instance, and `0x0036E4E0` (a 64-entry table at `0x022D97B0`)
otherwise or when the first finds nothing; it returns the result through `0x002E9B80`.

Two wrappers hand these to element handlers:

- `0x0024DCE0(mode, n)`, for `0x00524320`: mode 0 gives the current instance's owner `0x003A3FD0(−1)`
  (−1 with no instance current), mode 2 gives `0x003A4220(n)`, and mode 3 the render index of the
  n-th actor of manager 0 (`0x02098E10`) that has one (`0x00358940`, `0x003589B0`, `0x002E9B80`); any
  other mode, or no match, gives −1.
- `0x0024DDD0(&owner, &target)`, for `0x0045FD50` and `0x00529200`, returns `0x003A3FD0(slot)` and
  `0x003A6BA0(slot)` for the slot byte `+0x13B` of the current emitter `[0x02EBEF80]`.
- `0x003A6BA0(slot)` returns a kind-3 instance's `+0x10` entry for the slot (slot 0 for −1) as it is; otherwise it
  passes the slot's `+0x10` entry, or for −1 the `+0x90` entry and else the first `+0x10` one,
  through `0x002E9B80`. With `+0x378` bit `0x200` it reads the global list `0x02096A24` instead.

The three 64-entry tables are filled by script verbs, each taking an index clamped, `n < 0 ? 0 : n > 63 ? 63 : n`
(0 to 63; `0x0036E880`, `0x0036E7E0`, `0x0036E7B0`), and storing the calling script's actor (`0x00263F10`, `0x003589B0`):

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
  `[0x02EBA4F0]` (`0x003B9A5F`).
- `0x003A4070(slot)`: with the bit set, `[0x02096A20]`. Otherwise −1 for a kind-3 instance, and for a
  kind-5, 6 or 9 instance whose request (`0x003B0BF0(+0x04)`) is missing or has target test `+0x11` =
  1; else the slot's `+0x90` entry, or the owner `+0x08` for slot −1 or a zero entry. `0x003B99D0`
  calls it (`0x003B9AA1`).

### Renaming an owner or target

`0x0024C600(old, new)` does nothing unless both ids are non-zero. It then replaces `old` by `new` in
the owner `+0x08` and in both target arrays `+0x10` and `+0x90` (count `+0x372`) of three sets of
instances:

- `0x002FBFA0`: every instance on the kind-1 list `0x020910F0[1]` (`0x020910F8`), through `+0x348`;
- `0x003B0190`: the instance `+0x08` of each of the 36 request entries at `0x02EBEC00` whose handle is
  non-zero and whose target test `+0x11` is not 1;
- `0x003B14F0`: every instance on the kind-7 list `0x020910F0[7]` (`0x02091128`).

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00203170` is called by `0x003F1E90`; `0x0024B6F0` calls `0x00265020`, `0x003588B0`; `0x0024C870` calls
  `0x0026A3A0`, `0x0026A430`, `0x003588B0`; `0x0024DCE0` calls `0x00263C30`, `0x00263FF0`, `0x00358940`, `0x003589B0`; `0x0024F9B0`
  calls `0x0026A430`, `0x003588B0`; `0x00263C30` is called by `0x0032F1B0`; `0x00263F10` calls `0x003587C0`.
- Actor entity: `0x00263FF0` is called by `0x0032F1B0`, `0x0032F850`, `0x0032FA10`, `0x0032FAC0`, `0x0032FB70`, `0x00330060`,
  `0x00330110`, `0x00330190`, `0x00330220`, `0x003302B0`, `0x00330310`, `0x003304A0`; `0x00263FF0` is also called by `0x003306E0`,
  `0x00331610`, `0x003316B0`, `0x00331760`, `0x003317C0`, `0x00331820`, `0x00332130`, `0x003587C0`, `0x003588B0`, `0x0035A590`,
  `0x0035A7A0`, `0x0035A990`.
- Actor entity: `0x00263FF0` is also called by `0x003B6F80`, `0x003DB1F0`, `0x003DBCF0`, `0x003DDC20`, `0x0046BAC0`; `0x00264670` is
  called by `0x00236300`; `0x00265020` is called by `0x00236300`, `0x0037B4D0`, `0x003B73B0`, `0x003B7440`, `0x003B7510`; `0x002E9B80`
  calls `0x003588B0`; `0x00322760` calls `0x00263E30`, `0x003588B0`, `0x003589B0`; `0x003229E0` calls `0x00263E30`, `0x003588B0`.
- Actor entity: `0x00326D60` calls `0x00236820`, `0x00236850`, `0x00263E30`, `0x0030A880`, `0x0031B770`, `0x003588B0`; `0x00352270`
  calls `0x003589B0`; `0x00352940` calls `0x003589B0`; `0x00358940` is called by `0x0025AE00`, `0x0025B070`, `0x0025B250`,
  `0x0025B820`, `0x0025C070`, `0x0025C170`, `0x0025D9E0`, `0x00263A30`, `0x00264010`, `0x00264050`, `0x00265A20`, `0x00266C50`.
- Actor entity: `0x00358940` is also called by `0x00268B10`, `0x00268D10`, `0x002693D0`, `0x00269800`, `0x00269AD0`, `0x00269BA0`,
  `0x0026B8E0`, `0x0026CE60`, `0x0026D3E0`, `0x0035A590`, `0x0035A7A0`, `0x0035A990`; `0x00358940` is also called by `0x003B6F80`,
  `0x003DB1F0`, `0x0046BAC0`; `0x003589B0` is called by `0x00234480`, `0x0025C230`, `0x0025C830`, `0x00268650`, `0x00268D10`,
  `0x0037B4D0`, `0x003B6F80`.
- Actor entity: `0x003590D0` is called by `0x0025B600`, `0x0025D9E0`, `0x00263050`, `0x00263230`, `0x00263AC0`, `0x00264010`,
  `0x00264050`, `0x0026C5D0`, `0x0026C8C0`, `0x0026DFB0`; `0x003A40F0` calls `0x00265020`, `0x003588B0`; `0x003A4290` calls
  `0x00263C30`, `0x00263FF0`, `0x00358940`, `0x003589B0`; `0x003A56F0` calls `0x00263C30`, `0x00263FF0`, `0x00265020`, `0x003588B0`,
  `0x00358940`, `0x003589B0`.
- Actor entity: those functions are documented on [hud](../Menus-And-HUD/hud.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [battle unit construction](../Characters-And-Objects/battle-unit-construction.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
- Actor entity: and on [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
- Actor entity: and on [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md),
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md),
  [ebp lighting lgt2](../EBP-Script-Files/ebp-lighting-lgt2.md),
  [ebp script container](../EBP-Script-Files/ebp-script-container.md).
- Actor entity: and on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Actor entity: and on [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [actor managers](../Characters-And-Objects/actor-managers.md), [target selection](../Battle-Actions/target-selection.md).
- Actor entity: and on [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [field runtime](../Characters-And-Objects/field-runtime.md),
  [battle units](../Characters-And-Objects/battle-units.md); and on
  [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md).
- Audio: `0x00265020` is called by `0x00362850`; `0x002E9B80` is called by `0x00332C40`; `0x003590D0` is called by `0x00362850`;
  `0x003A3FD0` is called by `0x003B99D0`; `0x003A4070` is called by `0x003B99D0`; `0x003A6BA0` is called by `0x003B99D0`;
  `0x003A6D90` is called by `0x003B99D0`; `0x003A8240` is called by `0x00332C40`, `0x003B99D0`.
- Audio: `0x003B99D0` calls `0x002DEE80`, `0x002DEF40`, `0x002DEFA0`, `0x002DF0F0`, `0x002DF150`, `0x002DF1A0`, `0x003616F0`,
  `0x003617B0`, `0x00361CF0`, `0x003A0E20`, `0x003A0E50`, `0x003A1070`; `0x003B99D0` also calls `0x003D7C50`; `0x00421E20` is called
  by `0x00332C40`, `0x003B99D0`.
- Audio: those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [animation sounds](../Sound-And-Music/animation-sounds.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [map sounds](../Sound-And-Music/map-sounds.md),
  [audio manager](../Sound-And-Music/audio-manager.md).
- Audio: and on [sound effects](../Sound-And-Music/sound-effects.md), [sound banks](../Sound-And-Music/sound-banks.md).
- Combat action: `0x00265020` is called by `0x002F8060`, `0x00307300`, `0x00320E10`; `0x003229E0` calls `0x002FFA60`, `0x00306BB0`;
  `0x003589B0` is called by `0x00319F50`, `0x00325260`; `0x003590D0` is called by `0x00317E60`, `0x00319090`.
- Combat action: those functions are documented on [traps](../World-Areas-And-Travel/traps.md),
  [battle unit fields](../Characters-And-Objects/battle-unit-fields.md),
  [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md),
  [quickenings and summons](../Battle-Actions/quickenings-and-summons.md).
- Combat action: and on [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [jump thunks](../Engine-Core/jump-thunks.md).
- Combat formula: `0x00265020` is called by `0x00384F40`; those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md).
- Core runtime: `0x003820C0` calls `0x00229D20`, `0x00229D60`; `0x003B99D0` calls `0x001EDDA0`; `0x00524320` calls `0x001EDDA0`;
  those functions are documented on [startup constants](../Engine-Core/startup-constants.md),
  [screen mode and aspect](screen-mode-and-aspect.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Gameplay: `0x00203170` is called by `0x00339630`; `0x00265020` is called by `0x0031ADB0`, `0x00339630`; `0x003589B0` is called
  by `0x0031ADB0`; `0x003590D0` is called by `0x0031ADB0`; those functions are documented on
  [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [bestiary](../Enemy-Spawning/bestiary.md).
- Input: `0x00263FF0` is called by `0x00226BE0`, `0x002E09A0`; `0x00358940` is called by `0x00226BE0`; `0x003590D0` is called by
  `0x00226BE0`; those functions are documented on
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00203170` is called by `0x0022EF20`, `0x00230790`, `0x0026EB30`, `0x00334220`, `0x00334AB0`, `0x00334E00`,
  `0x00335B60`, `0x00336E40`, `0x00338490`, `0x00339F00`, `0x0033A3D0`, `0x0033BAA0`; `0x00203170` is also called by `0x0033C310`,
  `0x0033CBF0`, `0x0033CC80`, `0x0033D890`, `0x0033DB60`, `0x0033DFD0`, `0x003ED190`, `0x003ED3F0`; `0x0024B6F0` calls `0x00265200`;
  `0x0024C600` is called by `0x00326D60`.
- Movement: `0x0024C870` calls `0x0024C6B0`, `0x0026AF80`, `0x0026B5A0`; `0x0024C870` is called by `0x0024C6B0`; `0x0024F9B0` calls
  `0x0026AF80`, `0x0026B5A0`; `0x00263FF0` is called by `0x002E28E0`, `0x00392740`; `0x00264670` is called by `0x003B7F40`;
  `0x00265020` is called by `0x0024B6F0`, `0x002E45E0`, `0x002EBFA0`, `0x002EC2C0`, `0x00300310`, `0x00310920`, `0x00311E20`,
  `0x00311F70`, `0x00326BB0`, `0x00336710`, `0x00337C10`, `0x00337D90`.
- Movement: `0x00265020` is also called by `0x0033CA00`, `0x003B7E20`, `0x003B7F40`, `0x00505240`; `0x0026E350` calls `0x00231820`,
  `0x00231900`; `0x002F5550` calls `0x0026E5D0`, `0x0026E5F0`; `0x00326D60` calls `0x003003F0`, `0x00311F70`; `0x00358940` is called
  by `0x00392740`; `0x003589B0` is called by `0x002E5610`, `0x002EBFA0`.
- Movement: `0x003590D0` is called by `0x0026C3E0`, `0x0026D6F0`, `0x0026D810`, `0x002E45E0`, `0x002E5180`, `0x00319490`,
  `0x00325D90`, `0x00326BB0`, `0x00326D60`, `0x00343E20`, `0x00345430`; `0x003820C0` calls `0x00233230`, `0x0026E500`; `0x003A4290`
  calls `0x00264670`, `0x0026E350`; `0x003A56F0` calls `0x00264670`, `0x0026E350`; `0x003A6D90` is called by `0x0024B6F0`,
  `0x0024C870`, `0x0024F9B0`.
- Movement: those functions are documented on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md).
- Movement: and on [bestiary](../Enemy-Spawning/bestiary.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [traps](../World-Areas-And-Travel/traps.md),
  [party control modes](../Engine-Core/party-control-modes.md), [party slots](../Party/party-slots.md).
- Movement: and on
  [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md).
- Movement: and on [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [world lock](../Scripts-And-Script-Commands/world-lock.md).
- Movement: and on [battle units](../Characters-And-Objects/battle-units.md),
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [party data](../Party/party-data.md).
- Movement: and on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [subsystem update flags](../Engine-Core/subsystem-update-flags.md),
  [collision mesh movement](../Movement-And-Pathfinding/collision-mesh-movement.md).
- Movement: and on [texture animation lists ta](../Game-Files-And-Data-Tables/texture-animation-lists-ta.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [player movement](../Movement-And-Pathfinding/player-movement.md),
  [debug menu](../Engine-Core/debug-menu.md); and on [effect file loading](effect-file-loading.md).
- Party: `0x00265020` is called by `0x00303CC0`, `0x00304180`, `0x00359150`; `0x00326D60` calls `0x003590D0`; `0x003589B0` is called
  by `0x00269C70`, `0x00326500`, `0x00353530`, `0x0050C610`, `0x0050D2F0`; `0x003590D0` is called by `0x00263770`, `0x00269C70`,
  `0x00327270`, `0x003272A0`, `0x003272F0`, `0x003273B0`; `0x003A4290` calls `0x003590D0`; `0x003A56F0` calls `0x003590D0`.
- Party: those functions are documented on [party control modes](../Engine-Core/party-control-modes.md),
  [map screens](../Menus-And-HUD/map-screens.md), [frame update order](../Engine-Core/frame-update-order.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
- Party: and on [player movement](../Movement-And-Pathfinding/player-movement.md),
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md),
  [debug menu](../Engine-Core/debug-menu.md); and on
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md).
- Resource: `0x00421E20` calls `0x002ED570`; `0x004220F0` calls `0x002ED570`; those functions are documented on
  [resource sections](../Game-Files-And-Data-Tables/resource-sections.md).
- Rewards progression economy: `0x00265020` is called by `0x002FB150`, `0x00312280`; those functions are documented on
  [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md),
  [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md).
- Script VM: `0x00203170` is called by `0x00356160`; `0x00263C30` is called by `0x0034AF50`; `0x00263F10` is called by
  `0x00340230`, `0x00340640`, `0x00340CB0`, `0x00341070`, `0x00341140`, `0x00341690`, `0x00341B20`, `0x00341EE0`, `0x00342150`,
  `0x003421D0`, `0x00342500`, `0x003429F0`.
- Script VM: `0x00263F10` is also called by `0x00342D40`, `0x00343180`, `0x00343290`, `0x003434F0`, `0x003438F0`, `0x00344CC0`,
  `0x003460C0`, `0x00346620`, `0x00346A10`, `0x00348800`, `0x00348C50`, `0x00349220`; `0x00263F10` is also called by `0x00349620`,
  `0x00349AD0`, `0x0034A110`, `0x0034A4C0`, `0x0034AAD0`, `0x0034B060`, `0x0034B5D0`, `0x0034BB80`, `0x0034C0C0`, `0x0034C1D0`,
  `0x0034C500`, `0x0034C6A0`.
- Script VM: `0x00263F10` is also called by `0x0034C8D0`, `0x0034CC60`, `0x0034DA30`, `0x0034E190`, `0x00352270`, `0x00352940`,
  `0x00357F00`; `0x00263FF0` is called by `0x0033F7F0`, `0x00342490`, `0x00342A30`, `0x00343010`, `0x00343470`, `0x00348130`,
  `0x003484A0`, `0x00348A70`, `0x00348DA0`, `0x0034AF50`, `0x0034E460`, `0x0034F3C0`.
- Script VM: `0x00263FF0` is also called by `0x0034FC50`, `0x00351C90`, `0x00352000`, `0x00352560`, `0x00352D70`, `0x00357170`,
  `0x003574B0`, `0x0050D0C0`; `0x00264670` is called by `0x00343520`; `0x00265020` is called by `0x0033FD60`, `0x00344AF0`,
  `0x00345180`, `0x00345830`, `0x003461B0`, `0x00346710`, `0x00346D40`, `0x00347170`, `0x00347580`, `0x003478A0`, `0x00347AB0`,
  `0x00347FF0`.
- Script VM: `0x00265020` is also called by `0x0034BE50`, `0x0034CC00`, `0x00350DD0`, `0x003516E0`, `0x003562B0`, `0x00357DE0`,
  `0x0050E060`, `0x0050F6E0`, `0x00510040`, `0x00510080`, `0x005100C0`; `0x00342010` calls `0x00267E10`; `0x003423C0` calls
  `0x00267E10`; `0x00352270` calls `0x00267E10`; `0x00352940` calls `0x00267E10`.
- Script VM: `0x00358940` is called by `0x0025E4C0`, `0x002621D0`, `0x00267420`, `0x002674B0`, `0x00346FA0`, `0x0034A640`,
  `0x0034B350`, `0x0034C500`, `0x0034C630`, `0x0034CC60`, `0x00350DD0`, `0x003516E0`; `0x00358940` is also called by `0x00357620`,
  `0x0050D5E0`, `0x0050D780`, `0x0050D860`, `0x0050DB80`.
- Script VM: `0x003589B0` is called by `0x00342150`, `0x00342D40`, `0x003438F0`, `0x00349C90`, `0x0034B5D0`, `0x0034BB80`,
  `0x00352270`, `0x00352940`, `0x00354F20`, `0x003555F0`, `0x00357620`, `0x0050C7A0`; `0x003590D0` is called by `0x00341CB0`,
  `0x00345800`, `0x00346FA0`, `0x0034F800`, `0x0034FF00`, `0x00350DD0`, `0x003516E0`, `0x00352580`, `0x003530F0`, `0x00355830`,
  `0x00356570`, `0x0050C7A0`.
- Script VM: `0x003590D0` is also called by `0x0050C930`, `0x0050E060`; `0x0036E040` is called by `0x003423C0`; `0x0036E160` is
  called by `0x00342010`; `0x0036E1A0` is called by `0x00342010`; `0x0036E7B0` is called by `0x00352940`; `0x0036E7E0` is called
  by `0x00352270`; `0x0036E880` is called by `0x00352270`.
- Script VM: those functions are documented on
  [generated function families](../Compiler-And-C-Runtime/generated-function-families.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Script VM: and on [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md),
  [script censuses](../Story-Events-And-Hunts/script-censuses.md),
  [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: and on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [field runtime](../Characters-And-Objects/field-runtime.md), [debug menu](../Engine-Core/debug-menu.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
- Script VM: and on [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Script VM: and on [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [actor record](../Characters-And-Objects/actor-record.md),
  [ebp text sections](../EBP-Script-Files/ebp-text-sections.md); and on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Spawn encounter lifecycle: `0x00265020` is called by `0x00234AF0`, `0x00234DA0`, `0x002350C0`; those functions are
  documented on [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- UI: `0x00203170` is called by `0x00247AE0`, `0x002D2600`, `0x002D28E0`, `0x00368010`, `0x003C5500`, `0x003F26F0`, `0x003F2A70`;
  `0x00265020` is called by `0x003C5130`; `0x003590D0` is called by `0x00299BD0`, `0x002C7660`.
- UI: those functions are documented on [hud](../Menus-And-HUD/hud.md), [menu lists](../Menus-And-HUD/menu-lists.md),
  [ui typed lists](../Game-Files-And-Data-Tables/ui-typed-lists.md), [map screens](../Menus-And-HUD/map-screens.md),
  [battle units](../Characters-And-Objects/battle-units.md), [party list](../Menus-And-HUD/party-list.md).
- World area: `0x00358940` is called by `0x0025E400`, `0x002623A0`; `0x003590D0` is called by `0x0025E400`, `0x002623A0`; those
  functions are documented on [actor record fields](../Characters-And-Objects/actor-record-fields.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- World area: `0x00326D60` calls `0x00313F60`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
