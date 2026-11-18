[Home](../../README.md) / [Battle actions](README.md) / Action results

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Action results: the result record a resolved action produces and how it is applied to target and user | system | Battle actions | How an action runs | The 0x148-byte result record every resolved action, status tick and effect change fills, field by field, and the applier that turns it into changes on the target and the user - levels, steals and poached items, statuses added and removed, HP and MP, Mist charges, augment bits and their timers, an enemy's stat and affinity changes, gil - in the order they happen. | 0x003848E0, 0x003112F0, 0x00385BA0, 0x0030B9B0 |

## What the player sees

When an action hits, its whole outcome is first written into one record - damage or healing for the
target and the user, statuses to add or remove, items stolen or poached, levels gained, stat changes
on an enemy, gil spent - and then applied in one pass, in a fixed order. A field left at its "empty"
value is simply skipped, so each action only touches what it actually changes. Levels are applied
before the statuses, statuses before HP and MP, and the gil change comes last. When the target cannot
be affected at that moment, nothing in the record is applied.

## How it works

### The record

`0x003848E0(record)` (205 bytes) prepares the record. It zeroes `+0x08`-`+0x147`¹, leaves `+0x00`-`+0x07` to the caller, sets bit `0x1` of `+0x2C`, and sets the
"nothing to do" values²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003848EF`-`0x003848F5` |
| ² | `0x003848FA`-`0x003849A0` |

</details>

- `-1` in the dword at `+0x38` and in the dwords at `+0x138` and `+0x13C`;
- `-1` in the words at `+0x30`, `+0x11C` (both level bytes `0xFF`), `+0x11E`-`+0x124`, `+0x130` and
  the eight words `+0x42`-`+0x50`;
- `0xFF` in the bytes `+0x3C`-`+0x41`;
- `-1` in all 32 dwords from `+0x5C` and all 32 words from `+0xDC`.

It is called by the resolver `0x00385F60`¹, the preview `0x00385680`² and the four
status-result builders `0x00385DF0`, `0x00386A50`, `0x00386A70` and `0x00386AE0`. The record lives on the
stack of the function that starts the action or status change, which first clears all `0x148` bytes with
`memset` (below).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0038600F` |
| ² | `0x0038586C` |

</details>

### The applier

`0x003112F0(record, sourceStats, targetStats, actionId, flags)` (2,040 bytes) is called
by the effect applier `0x00307300`¹, the periodic maintenance `0x00310DB0`
(three calls), the effect-bit write `0x0030E130` and the status write `0x0030E360`. The last three pass a null
`sourceStats` at all five calls²; the effect applier
passes the user's stats record `+0x698`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307436`, `0x00307ABD` |
| ² | `0x0030E2D8`, `0x0030E636`, `0x00310FA5`, `0x003110A2`, `0x0031126A` |
| ³ | `0x0030741E`, `0x00307AAA` |

</details>

Three pointers are tested before the steps that use them: a null target unit (`0x0031B860(targetStats)`) skips steps 3,
5 and 12 and the clear of step 14¹; a null `targetStats` skips the
target level of step 4, steps 6-8, 10 and 11 and the rebuild²; a null
`sourceStats` skips the user level of step 4 and step 9³, so neither runs at the five calls
above that pass one. In order:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031137F`, `0x00311402`, `0x00311919`, `0x00311AA3` |
| ² | `0x003113C6`, `0x003114C9`, `0x00311778`, `0x00311AAF` |
| ³ | `0x003113E4`, `0x003116F3` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | **Skip test.** Unless bit `0x1` of `flags` is set, nothing is applied when `0x0030B9B0(targetUnit, sourceUnit)` is non-zero - the global part `0x0030B770` or the unit part `0x0030B7F0` of the eligibility mask, with the hostile flag from the relationship class ([Area of effect](area-of-effect.md)). | `0x00311354`-`0x00311367` |
| 2 | **Metadata** `0x00385BA0`: `+0x138` (when not -1) goes to the byte `[0x02EBF190]+0x5B0E`, `+0x13C` to the dword `[0x02EBF190]+0x5B00`; a non-zero steal byte `+0x32`/`+0x33`/`+0x34` clears bit `0x1`/`0x2`/`0x4` of `[targetUnit+0x6A0]+0x14`; with `+0x1C` = 1 the battle-message events are posted.<br>• `+0x13C` is skipped when it is -1 as well, and the byte stored from `+0x138` is its low byte.<br>• The steal bytes are tested `+0x34` first, then `+0x33` and `+0x32`; each finds the target unit afresh with `0x0031B860(targetStats)`, kept in `0x02EBF188`, and a null unit or a null `+0x6A0` skips that clear.<br>• The poster is called as `0x00469EC0(word [0x02AEDFD4], sourceStats, targetStats, result)`. | `0x00469EC0`<br>`0x00385BDE`<br>`0x00385BC9`<br>`0x00385BF0`-`0x00385C6B`<br>`0x00385C75`-`0x00385C85` |
| 3 | Bit `0x80000` of `+0x2C` sets bit `0x8` of the target unit's `+0xE9A`; bit `0x4000` of `+0x140` passes sound `0x34` to `0x003A1180` and, unless that answers -1, plays it with `0x002DF220(handle, 0x40, 0x7F)`; then bit `0x4` is set. | `0x0031137F`-`0x003113BF` |
| 4 | **Levels.** A target level `+0x11C` other than `0xFF` is applied with `0x0030C650(target, level, 0)`, and the user's `+0x11D` likewise. | `0x003113C6`-`0x003113FD` |
| 5 | **Steal and poach.**<br>• For an enemy-side target, each non-zero steal byte `k` (`+0x32`-`+0x34`) adds one of the item at `[targetUnit+0xE60]+0x32+2k` (when not `0xFFFF`) with `0x003008A0`, clears bit `1 << k` of `[targetUnit+0x6A0]+0x14` (already cleared by step 2) and calls `0x00316A50(3)` through the thunk `0x00253770`.<br>• For a target of either side, a poach item `+0x38` other than -1 is added with `0x003008A0`.<br>• A poach that rolled an empty `0xFFFF` word stores item 0, so the applier passes item 0, the Potion ([item list](../Items-Equipment-Shops-And-Licenses/item-list.md)): `0x003008A0` refuses only `0xFFFF`, `0x1000`, a group above `0xE` and an index past the group's count, and group 0 counts `0x40` ids and hands them to `0x002FD150`. | `0x00311475`<br>`0x00311402`-`0x003114A8`<br>`0x003907AB`<br>`0x003008C0`-`0x00300927`<br>`0x00300960` |
| 6 | **Statuses.** Each bit `n` of the add mask `+0x54` calls `0x0030E360(target, source, n, +0x5C[n], +0xDC[n], ..., 3)` (add); each bit of the remove mask `+0x58` calls `0x0030E360(target, source, n, 0, 0, ..., 0)` (remove). Bits `0x10` and `0x20` of `+0x140` choose a flag passed to those calls. | `0x003114C9`-`0x003115AF` |
| 7 | **Status parameters.** Every `+0x5C[n]` that is not negative is copied to target `+0xBC + 4n` (the status durations) and every i16 `+0xDC[n]` that is not negative to target `+0x13C + 2n`. | `0x003115B6`-`0x00311606`, `0x003115F6` |
| 8 | **Target HP and MP.** With bit `0x100` of `+0x2C`, `+0x24` is applied to the target's HP - set outright with bit `0x8`, otherwise added (`0x00300530`, the HP write). With bit `0x4000`, `+0x2A` goes to the target's MP - set with bit `0x10`, otherwise added. A non-zero `+0x1D` adds `+0x1D * [target+0x28]` (whole max-MP units) to the target's secondary resource. | `0x00300520`<br>`0x00300C90`<br>`0x00300CE0`<br>`0x00300BC0`<br>`0x00311608`-`0x003116E0` |
| 9 | **User HP and MP.** With bit `0x80` of `+0x2C`, `+0x20` is applied to the user's HP (set with bit `0x2`); with bit `0x2000`, `+0x28` to the user's MP (set with bit `0x4`). | `0x00311700`-`0x00311775` |
| 10 | **Augment bits.** `+0x3C` and `+0x3D` (when not `0xFF`) are set in the target's augment layer (`0x0030E130` mode 2); `+0x3E`-`+0x41` are cleared (mode 0), each also only when not `0xFF`; bits `0x40` and `0x80` of `+0x140` choose the flags. The eight timers `+0x42`-`+0x50` that are not negative are copied to target `+0x17C`-`+0x18A`. | `0x003117F7`<br>`0x00311778`-`0x00311894` |
| 11 | **Enemy stat changes.** For an enemy-side target, each of `+0x11E`, `+0x120`, `+0x122`, `+0x124` that is not -1 sets the target's modifier so that the stat becomes that value: `+0x08 += v - str` (`+0x2A`), `+0x0A += v - mag` (`+0x2B`), `+0x12 += v - def` (`+0x2F`), `+0x14 += v - mres` (`+0x30`). | `0x0031189B`-`0x00311915` |
| 12 | **Enemy affinity bytes.** For an enemy-side target, `+0x128`-`+0x12B` are OR-ed into bytes `+0x7B`, `+0x79`, `+0x78`, `+0x7A` of `[targetUnit+0x6A0]`, and `+0x12C`-`+0x12F` cleared out of the same bytes; each change sets bit `0x80` of that record's first dword. | `0x00311919`-`0x00311A7E` |
| 13 | **Gil.** A non-zero `+0x08` is subtracted from the party's gil, not below 0. | `0x00253690`, `0x00254EE0`<br>`0x00311A84`-`0x00311A9E` |
| 14 | Bits `0x4` and `0x8` of the target unit's `+0xE9A` are cleared; when bit `0x200` of `flags` is clear and step 6 or 10 made a call, or step 11 met a value other than -1 or step 12 a non-zero byte, the target's stats are rebuilt (`0x0030FED0(target, 0)`). | `0x00311AB4`, `0x00311ABB`<br>`0x00311AA3`-`0x00311AC5` |

`0x00300C90(stats, value, tag)`, the MP set of steps 8 and 9, calls `0x00300CE0(stats, value - i16 +0x4C, tag)`, and, when
`value` is above the i16 `+0x06` read after that call, the secondary-resource add
`0x00300BC0(stats, value - i16 +0x06, tag)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00300C9F`-`0x00300CC4` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u32` | flags0 | left to the caller by `0x003848E0`; stored whole by `0x00303A00` (`0x00303A85`), `0x00307300` (`0x00307527`) and `0x00310DB0` (`0x00311241`); bit `0x20` tested and cleared by the resolver (`0x00386029`, `0x00386082`) |
| `+0x004` | `u8` | outcome | 1-5 the evade/guard outcome of slot 41 (`0x003896B0`); 6 at `0x00386347` and `0x003858A2`; 9 at `0x0038588A`; 10 at `0x00386303` |
| `+0x005` | `u8[3]` | pad05 | written only by the clears (below); read by no instruction; nothing fixes its width |
| `+0x008` | `u32` | gilCost | subtracted from the party's gil (step 13) |
| `+0x00C` | `u8[4]` | zero0C | written only by the clears (below); read by no instruction; nothing fixes its width |
| `+0x010` | `void*` | otherUnit | a battle unit that `0x00384F40` returns, stored by the handler `0x00390AB0` (`0x00390E39`-`0x00390E42`); the preview `0x00303A00` then previews the action again for that unit's stats record (`0x00303B45`-`0x00303B90`) |
| `+0x018` | `u32` | flagsB | bit `0x2`: continue a combo (`0x00388660`); bit `0x4`: guard decision (`0x00385A1C`-`0x00385A2D`); bit `0x8`: knockback (`0x003896B0`); `0x00307300` copies bits `0xF` to target entry bits `0x800`, `0x400`, `0x200`, `0x100` |
| `+0x01C` | `u8` | resolved | 1: post the battle-message events (`0x00385BA0`) |
| `+0x01D` | `i8` | mpUnits | whole max-MP units added to the target's secondary resource (step 8) |
| `+0x01E` | `u8[2]` | zero1E | written only by the two clears (below); read by no instruction; nothing fixes its width |
| `+0x020` | `i32` | userHp | user HP change or value (step 9) |
| `+0x024` | `i32` | targetHp | target HP change or value (step 8) |
| `+0x028` | `i16` | userMp | user MP change or value (step 9) |
| `+0x02A` | `i16` | targetMp | target MP change or value (step 8) |
| `+0x02C` | `u32` | flagsA | bit `0x1` set by `0x003848E0`; bits `0x1E` set-not-add; bits `0x80`, `0x100`, `0x2000`, `0x4000` present; bit `0x80000` marks the target unit |
| `+0x030` | `u16` | unused30 | `0xFFFF` by the word store `0x0038490B` in `0x003848E0`; read by no instruction |
| `+0x032` | `u8[3]` | steal | steal slots 0-2 (step 5, `0x00385BA0`) |
| `+0x035` | `u8[3]` | zero35 | written only by the clears (below); read by no instruction; nothing fixes its width |
| `+0x038` | `i32` | poachItem | item id in the low word, copied from the dword `0x02AEE050` (`0x00386813`-`0x00386819`); -1 from the per-action reset (`0x00384AF9`) when the action does not poach, 0 when a poach rolled an empty `0xFFFF` word (`0x003907AB`) (step 5) |
| `+0x03C` | `u8[2]` | effectSet | augment bits to set; `0xFF` when the byte sets nothing (step 10) |
| `+0x03E` | `u8[4]` | effectClear | augment bits to clear; `0xFF` when the byte clears nothing (step 10) |
| `+0x042` | `i16[8]` | effectTimers | eight timers, each copied to target `+0x17C`-`+0x18A` when not negative (`0x00311778`-`0x00311894`) |
| `+0x052` | `u8[2]` | zero52 | written only by the two clears (below); read by no instruction; nothing fixes its width |
| `+0x054` | `u32` | addMask | statuses to add (step 6) |
| `+0x058` | `u32` | removeMask | statuses to remove (step 6) |
| `+0x05C` | `i32[32]` | statusA | per-status parameter A (duration); copied to target `+0xBC` |
| `+0x0DC` | `i16[32]` | statusB | per-status parameter B (beat timer); copied to target `+0x13C` |
| `+0x11C` | `u8` | targetLevel | `0xFF` when the level does not change (step 4) |
| `+0x11D` | `u8` | userLevel | `0xFF` when the level does not change (step 4) |
| `+0x11E` | `i16[4]` | enemyStats | new Strength, Magick Power, Defence, Magick Resist; -1 when that stat does not change (step 11) |
| `+0x126` | `u8[2]` | zero126 | written only by the two clears (below); read by no instruction; nothing fixes its width |
| `+0x128` | `u8[4]` | affinitySet | OR-ed into the enemy record bytes `+0x7B`, `+0x79`, `+0x78`, `+0x7A` (step 12), the immune, absorb, weak and half masks the rebuild copies to stats `+0x43`, `+0x41`, `+0x40`, `+0x42` (`0x0031043F`-`0x0031046D`); Elemental Shift's `0x00384B10` writes `+0x129` (every element but the drawn one) and `+0x12A` (the drawn one) (`0x00384BE6`, `0x00384BFC`; [Battle buffs](../Status-Effects-And-KO/battle-buffs.md)) |
| `+0x12C` | `u8[4]` | affinityClr | cleared out of the same bytes after the sets (step 12); `0x00384B10` writes `+0x12C` (OR-ed with the drawn element), `+0x12D` (the drawn one) and `+0x12E` (every element but the drawn one) (`0x00384C0B`, `0x00384BF1`, `0x00384BDC`) |
| `+0x130` | `u16` | packedParam | -1 by the word store `0x00384991` in `0x003848E0`; the handler `0x003907E0` stores byte `+0x10` × 100 + byte `+0x11` of action row `[0x02AEDFD4]` (`0x00390877`-`0x00390893`); `0x00319F50` reads it after the resolver returns (`0x0031A0D2`, `0x0031A0DF`) |
| `+0x132` | `u8[2]` | zero132 | written only by the clears (below); read by no instruction; nothing fixes its width |
| `+0x134` | `f32` | knockback | zeroed by `0x003848E0`; with flagsB bit `0x8` the resolver stores `0x00385E50`'s value here (`0x0038680F`-`0x0038682E`; [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)) |
| `+0x138` | `i32` | echoB | to [`0x02EBF190`]`+0x5B0E` (low byte) when not -1 (`0x00385BA0`) |
| `+0x13C` | `i32` | echoA | to [`0x02EBF190`]`+0x5B00` when not -1 (`0x00385BA0`) |
| `+0x140` | `u32` | flagsC | bits `0x10`, `0x20`, `0x40`, `0x80`: flags for the status and effect writes; bit `0x4000`: sound `0x34` |
| `+0x144` | `u8[4]` | zero144 | written only by the two clears (below); read by no instruction; nothing fixes its width |

### Where records live and who clears them

A record is a local of one of nine functions. Eight clear all `0x148` bytes with `memset`¹
before use; the ninth, `0x00319F50`, hands its record straight to the resolver, whose `0x003848E0` clears
`+0x08`-`+0x147`:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00861EC0` |

</details>

| Function | Clears at | Hands the record to |
|---|---|---|
| `0x00303830` | `0x003038CB` | the preview `0x00385680` |
| `0x00303A00` | `0x00303A64` | the preview `0x00385680` |
| `0x00307300` | `0x003073D2` | the resolver `0x00385F60`, the applier `0x003112F0` |
| `0x00308B90` | `0x00308BCB` | the resolver `0x00385F60` |
| `0x0030EC00` | `0x0030EC89` | the resolver `0x00385F60` |
| `0x0030E130` | `0x0030E293` | `0x00386A50` or `0x00386AE0` (`0x0030E2BC`), the applier |
| `0x0030E360` | `0x0030E5E1` | `0x00386A50` or `0x00386A70` (`0x0030E60E`), the applier |
| `0x00310DB0` | `0x00310F7A`, `0x00311010`, `0x0031121A` | `0x00385DF0`, the resolver, the applier |
| `0x00319F50` | no clear of its own (`0x003848E0` in the resolver clears `+0x08`-`+0x147`) | the resolver `0x00385F60` |

The resolver and the preview also put the record's address at `+0x10` of the evaluation context that
`0x003847C0` builds¹, and the 202 action-effect handlers of the table `0x01EFA5C0` reach it there.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003847FF` |

</details>

The bytes `+0x05`-`+0x07`, `+0x0C`-`+0x0F`, `+0x1E`-`+0x1F`, `+0x35`-`+0x37`, `+0x52`-`+0x53`, `+0x126`-`+0x127`,
`+0x132`-`+0x133` and `+0x144`-`+0x147` are written only by these clears and by `0x003848E0`'s `memset` of
`+0x08`-`+0x147`¹, and read by no instruction; `+0x30` is also written `0xFFFF`². No function
copies a record whole.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003848F5` |
| ² | `0x0038490B` |

</details>

</details>

## State

<details>
<summary>Show the state it keeps</summary>

The applier writes only to the records it is given and the globals named in the steps
(`[0x02EBF190]+0x5B00`/`+0x5B0E` and the party's gil).

</details>

## Modding notes

- An action's effect on HP and MP is "present" only with its bit in `+0x2C`; the values alone do
  nothing.
- An enemy's stat change is written as the new stat value, not a delta: the applier adjusts the
  modifier so the stat lands on it.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags `0x00307300` fills from `flagsB`.
- [Combos](combos.md) - `flagsB` bit `0x2`.
- [Action phases](action-phases.md) - where the resolution runs.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the status
  numbers of the masks.
- [The status write](../Status-Effects-And-KO/status-changes.md)
  - what `0x0030E360` does with each add and remove.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Game files and data tables** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over) | calls | [`0x001D6AE0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) |

</details>

---

[← Action phases](action-phases.md)
