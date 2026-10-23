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
[`effect-element-runtime-switch-family-3a42-3a56.tsv`](effect-element-runtime-switch-family-3a42-3a56.tsv); [`effect-element-runtime-switch-family-frontier-decode.tsv`](effect-element-runtime-switch-family-frontier-decode.tsv)
decodes `0x00442170` and `0x00442460` (the emitter-record subtype switches) and the record-store
fronts `0x00500980` / `0x00500850`, together with dispatchers outside the effect code.

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
| `+0x4A` | bit 0 resolve on frame 0 only and keep the result after; bit 1 skip the record's scale; bits 2-3 the height rule (third table) |
| `+0x4B` | the mode `0x00421E20` takes: 0 the bone's origin, 1 the bone's end, 2 its middle |
| `+0x4C` | a bone index for the point kinds 6 and 7 |
| `+0x4E` | the object slot for the record kinds 9 and 13 |

The element's byte `+0x102` is the slot the owner and target reads take ([target slots](#target-slots)).

| Record kind (`+0x48`) | Whose matrix | Point kind used |
|---|---|---|
| 1 | the owner's record (`0x003A3FD0`, `0x003A440B`) | yes |
| 2 | the target's record (`0x003A6BA0`, `0x003A4432`) | yes |
| 3, 11 | the camera matrix `0x02AEDEF0`; kind 11 takes the position `0x02AED600`-`0x02AED608`. The third axis is scaled by tan(pi/8) / tan(fov / 2), fov the angle `0x02AED568`, or 45 degrees in Super Wide mode while `0x02AED568` and `0x02AED56C` are above 1.0 (`0x003A44C3`-`0x003A4553`) | no |
| 4 | the record of the actor in `effectactor` slot `n` (`0x003A40F0`, through the tables `0x003A4220` uses) | yes |
| 5 | the record of the party-focus actor (`0x003590D0`, `0x002E9B80`) | yes |
| 6 | the `n`-th member of manager 0 that has a record (`0x00263FF0`, `0x00263C30`, `0x00358940`) | yes |
| 7 | the matrix of map model `n` (`0x003A6FC0`), copied to `out` as it is, without the offset (`0x003A5368`-`0x003A5386`): the draw-list build `0x002F5550` stores each model's index in the 32 words at `0x0209A71C` under the anchor number its placement row names (`0x002F6533`-`0x002F6554`); `n` is the instance's byte `+0x376` while its `+0x368` bit 9 is set | no |
| 8 | the centre of the instance's targets as the position (`0x003A6C30`) | no |
| 9, 13 | the path object `0x003A8240(key, +0x4E)` finds, first advanced by `0x004FF0D0(object, 2.0)` while its `+0x103` bit 0 is clear, with the key the work object's byte `+0x42` (kind 9) or `[0x02F97348] + 0x388` (kind 13) | no |
| 10 | the targets' centre (`0x003A6C30`); the offset's height is added only when `0x0026E350` finds ground there | no |
| 12, or any other | no anchor: the identity matrix at the offset (`0x003A54DD`) | no |
| 14 | a screen position turned into a matrix (`0x0057A040`): the menu record's `+0x10`-`+0x18` for a menu-effect instance (id top nibble 4, `0x003B2CA0`), else `0x02096B2C`-`0x02096B34` | no |

On a record, the point kind picks the point; the point ids are those of
[character render records](character-render-records.md#attaching-a-record-the-pending-tie-and-the-slot-table).
"Child" means the first child record with that point (`0x00426770`), for example the weapon a character holds.

| Point kind (`+0x49`) | Point |
|---|---|
| 1 | `model` (`0x101`), with the height `[0x02F97348] + 0x36C` while the instance's `+0x368` bit 11 is set |
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
| 37, 38 | `n_hara` with the position replaced by `@FCP` section 1's point `+0xD4` (`0x003E5600`), at the ground height (37) or not (38) |
| 40 | `model`, with the position replaced by section 9's point (`0x003E4F50`) |
| 0, or above 40 | `n_hara` |

When a point is missing the query falls back to `n_hara` and then to a child's `n_grip` (`0x003A471A`-`0x003A4777`). On
a record, and for record kinds 3 and 11, the position is then divided by the published instance scale `0x02096810`. Unless `+0x4A` bit 1 is set,
the record's own scale (`0x003E5710`) is applied when it is not 1, 1, 1 (`0x003A47B8`-`0x003A4861`). The height rule
follows (`0x003A4868`-`0x003A489F`):

| `+0x4A` bits 2-3 | Height |
|---|---|
| 0 | as resolved |
| 1 | 0 |
| 2 | `[0x02F97348] + 0x36C` while the instance's `+0x368` bit 11 is set, else the height of the record's `model` point |
| 3 | the ground height (`0x00264670` on the record's `+0x108`) |

The random lists hold point ids; `0x003A6E60(count)` draws the index:

| List | Count | Point ids |
|---|---|---|
| 0 (`0x01EFAC60`) | 15 | `0x100`, `0x301`, `0x302`, 12, 13, 0, 1, `0x300`, `0x17`, `0x18`, `0x307`, `0x30A`, 5, `0x19`, and as fifteenth entry the word at `0x01EFAC7C`, which is the first two count bytes (`0x060F`) |
| 1 (`0x01EFAC80`) | 6 | `0x100`, 13, 0, 1, `0x17`, `0x18` |
| 2 (`0x01EFAC90`) | 6 | `0x100`, 0, 1, `0x17`, `0x18`, 0 |

A drawn `0x100` is looked up on the record itself, and any other id on its children (`0x00426770`). When the record has
no such point, the query draws once more. Ids `0x17`-`0x19` lie past the 22-entry slot tables. A keyed skeleton
takes them as `@FCP` special ids (`0x003E5AD0`, `0x00421F46`); a named one would index the name table past its end.

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

`0x003A4220(id)` picks one of three lookups by the instance: `0x0036E620` when bits 12–14 of word
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

The three 64-entry tables are filled by script verbs, each taking an index clamped to 0 to 63 and
storing the calling script's actor (`0x00263F10`, `0x003589B0`):

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
