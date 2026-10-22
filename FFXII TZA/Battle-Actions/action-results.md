---
title: "Action results: the result record a resolved action produces and how it is applied to target and user"
kind: "system"
category: "Battle actions"
addresses: "0x003848E0, 0x003112F0, 0x00385BA0, 0x0030B9B0"
---

## What the player sees

When an action hits, its whole outcome is first written into one record - damage or healing for the
target and the user, statuses to add or remove, items stolen or poached, levels gained, stat changes
on an enemy, gil spent - and then applied in one pass, in a fixed order. A field left at its "empty"
value is simply skipped, so each action only touches what it actually changes. Levels are applied
before the statuses, statuses before HP and MP, and the gil change comes last. When the target cannot
be affected at that moment, nothing in the record is applied.

## How it works

### The record

`0x003848E0(record)` (205 bytes) prepares the record. It zeroes `+0x08`-`+0x147`
(`0x003848EF`-`0x003848F5`), leaves `+0x00`-`+0x07` to the caller, sets bit 0 of `+0x2C`, and sets the
"nothing to do" values (`0x003848FA`-`0x003849A0`):

- `-1` in the dword at `+0x38` and in the dwords at `+0x138` and `+0x13C`;
- `-1` in the words at `+0x30`, `+0x11C` (both level bytes `0xFF`), `+0x11E`-`+0x124`, `+0x130` and
  the eight words `+0x42`-`+0x50`;
- `0xFF` in the bytes `+0x3C`-`+0x41`;
- `-1` in all 32 dwords from `+0x5C` and all 32 words from `+0xDC`.

It is called by the resolver `0x00385F60` (`0x0038600F`), the preview `0x00385680` (`0x0038586C`) and the four
status-result builders `0x00385DF0`, `0x00386A50`, `0x00386A70` and `0x00386AE0`. The record lives on the
caller's stack.

### The applier

`0x003112F0(record, sourceStats, targetStats, actionId, flags)` (2,040 bytes) is called
by the effect applier `0x00307300` (`0x00307436`, `0x00307ABD`), the periodic maintenance `0x00310DB0`
(three calls), the effect-bit write `0x0030E130` and the status write `0x0030E360`. In order:

1. **Skip test.** Unless bit 0 of `flags` is set, nothing is applied when `0x0030B9B0(targetUnit,
   sourceUnit)` is non-zero - the global part `0x0030B770` or the unit part `0x0030B7F0` of the eligibility
   mask, with the hostile flag from the relationship class ([Area of effect](area-of-effect.md))
   (`0x00311354`-`0x00311367`).
2. **Metadata** `0x00385BA0`: `+0x138` (when not -1) goes to the byte `[0x02EBF190]+0x5B0E`, `+0x13C` to the
   dword `[0x02EBF190]+0x5B00`; a non-zero steal byte `+0x32`/`+0x33`/`+0x34` clears bit 0/1/2 of
   `[targetUnit+0x6A0]+0x14`; with `+0x1C` = 1 the battle-message events are posted (`0x00469EC0`).
3. Bit 19 of `+0x2C` sets bit 3 of the target unit's `+0xE9A`; bit 14 of `+0x140` plays sound `0x34`
   (`0x003A1180`, `0x002DF220`) and sets bit 2 (`0x00311384`-`0x003113BF`).
4. **Levels.** A target level `+0x11C` other than `0xFF` is applied with `0x0030C650(target, level, 0)`,
   and the user's `+0x11D` likewise (`0x003113CB`-`0x003113FD`).
5. **Steal and poach.** For an enemy-side target, each non-zero steal byte `k` (`+0x32`-`+0x34`) adds
   one of the item at `[targetUnit+0xE60]+0x32+2k` (when not `0xFFFF`) with `0x003008A0`, clears bit `k`
   of `[targetUnit+0x6A0]+0x14` (already cleared by step 2) and calls `0x00316A50(3)`; a poach item `+0x38` other than -1 is added (`0x00311402`-`0x003114A8`).
6. **Statuses.** Each bit `n` of the add mask `+0x54` calls `0x0030E360(target, source, n, +0x5C[n],
   +0xDC[n], ..., 3)` (add); each bit of the remove mask `+0x58` calls `0x0030E360(target, source, n, 0, 0,
   ..., 0)` (remove). Bits 4 and 5 of `+0x140` choose a flag passed to those calls (`0x003114D2`-`0x003115AF`).
7. **Status parameters.** Every `+0x5C[n]` that is not negative is copied to target `+0xBC + 4n` (the
   status durations) and every `+0xDC[n]` to target `+0x13C + 2n` (`0x003115B6`-`0x00311606`).
8. **Target HP and MP.** With bit 8 of `+0x2C`, `+0x24` is applied to the target's HP - set outright
   (`0x00300520`) with bit 3, otherwise added (`0x00300530`, the HP write). With bit 14, `+0x2A` goes to the
   target's MP - set (`0x00300C90`) with bit 4, otherwise added (`0x00300CE0`). A non-zero `+0x1D` adds
   `+0x1D * [target+0x28]` (whole max-MP units) to the target's secondary resource (`0x00300BC0`) (`0x00311608`-`0x003116E0`).
9. **User HP and MP.** With bit 7 of `+0x2C`, `+0x20` is applied to the user's HP (set with bit 1);
   with bit 13, `+0x28` to the user's MP (set with bit 2) (`0x00311700`-`0x00311775`).
10. **Augment bits.** `+0x3C` and `+0x3D` (when not `0xFF`) are set in the target's augment layer
   (`0x0030E130` mode 2); `+0x3E`-`+0x41` are cleared (mode 0); bits 6 and 7 of `+0x140` choose the
   flags. The eight timers `+0x42`-`+0x50` that are not negative are copied to target
   `+0x17C`-`+0x18A` (`0x00311778`-`0x00311894`).
11. **Enemy stat changes.** For an enemy-side target, each of `+0x11E`, `+0x120`, `+0x122`, `+0x124`
    that is not -1 sets the target's modifier so that the stat becomes that value: `+0x08 += v - str`
    (`+0x2A`), `+0x0A += v - mag` (`+0x2B`), `+0x12 += v - def` (`+0x2F`), `+0x14 += v - mres`
    (`+0x30`) (`0x0031189B`-`0x00311915`).
12. **Enemy affinity bytes.** For an enemy-side target, `+0x128`-`+0x12B` are OR-ed into bytes
    `+0x7B`, `+0x79`, `+0x78`, `+0x7A` of `[targetUnit+0x6A0]`, and `+0x12C`-`+0x12F` cleared out of
    the same bytes; each change sets bit 7 of that record's first dword (`0x0031193C`-`0x00311A7E`).
13. **Gil.** A non-zero `+0x08` is subtracted from the party's gil, not below 0 (`0x00253690`,
    `0x00254EE0`) (`0x00311A84`-`0x00311A9E`).
14. Bits 2 and 3 of the target unit's `+0xE9A` are cleared; when anything above changed and bit 9 of
    `flags` is clear, the target's stats are rebuilt (`0x0030FED0(target, 0)`) (`0x00311AA3`-`0x00311AC5`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8` | flags0 | left to the caller by `0x003848E0` |
| `+0x001` | `u8[3]` | pad01 | left to the caller |
| `+0x004` | `u8` | outcome | 1-5 the evade/guard outcome of slot 41 (`0x003896B0`); 6 at `0x00386347` and `0x003858A2`; 9 at `0x0038588A`; 10 at `0x00386303` |
| `+0x005` | `u8[3]` | pad05 | left to the caller |
| `+0x008` | `u32` | gilCost | subtracted from the party's gil (step 13) |
| `+0x00C` | `u8[12]` | zero0C | zeroed by `0x003848E0`; not read by `0x003112F0` |
| `+0x018` | `u32` | flagsB | bit 1: continue a combo (`0x00388660`); bit 2: guard decision (`0x00385A1C`-`0x00385A2D`); bit 3: knockback (`0x003896B0`); `0x00307300` copies bits 0-3 to target entry bits 11, 10, 9, 8 |
| `+0x01C` | `u8` | resolved | 1: post the battle-message events (`0x00385BA0`) |
| `+0x01D` | `i8` | mpUnits | whole max-MP units added to the target's secondary resource (step 8) |
| `+0x01E` | `u8[2]` | zero1E | zeroed only by the memset of `+0x08` to `+0x147` in `0x003848E0` (`0x00861EC0`, `0x003848F5`); read by no function; nothing fixes its width |
| `+0x020` | `i32` | userHp | user HP change or value (step 9) |
| `+0x024` | `i32` | targetHp | target HP change or value (step 8) |
| `+0x028` | `i16` | userMp | user MP change or value (step 9) |
| `+0x02A` | `i16` | targetMp | target MP change or value (step 8) |
| `+0x02C` | `u32` | flagsA | bit 0 set by `0x003848E0`; bits 1-4 set-not-add; 7, 8, 13, 14 present; 19 marks the target unit |
| `+0x030` | `u16` | unused30 | `0xFFFF` by the word store `0x0038490B` in `0x003848E0`; not read by `0x003112F0` or `0x00385BA0` |
| `+0x032` | `u8[3]` | steal | steal slots 0-2 (step 5, `0x00385BA0`) |
| `+0x035` | `u8[3]` | zero35 | zeroed by `0x003848E0`; not read by `0x003112F0` |
| `+0x038` | `i32` | poachItem | item id in the low word; -1 none (step 5) |
| `+0x03C` | `u8[2]` | effectSet | augment bits to set; `0xFF` none (step 10) |
| `+0x03E` | `u8[4]` | effectClear | augment bits to clear; `0xFF` none (step 10) |
| `+0x042` | `i16[8]` | effectTimers copied to target +0x17C..+0x18A when not negative |  |
| `+0x052` | `u8[2]` | zero52 | zeroed only by the memset in `0x003848E0`; read by no function; nothing fixes its width |
| `+0x054` | `u32` | addMask | statuses to add (step 6) |
| `+0x058` | `u32` | removeMask | statuses to remove (step 6) |
| `+0x05C` | `i32[32]` | statusA | per-status parameter A (duration); copied to target `+0xBC` |
| `+0x0DC` | `i16[32]` | statusB | per-status parameter B (beat timer); copied to target `+0x13C` |
| `+0x11C` | `u8` | targetLevel | `0xFF` none (step 4) |
| `+0x11D` | `u8` | userLevel | `0xFF` none (step 4) |
| `+0x11E` | `i16[4]` | enemyStats | new Strength, Magick Power, Defence, Magick Resist; -1 none (step 11) |
| `+0x126` | `u8[2]` | zero126 | zeroed only by the memset in `0x003848E0`; read by no function; nothing fixes its width |
| `+0x128` | `u8[4]` | affinitySet | OR-ed into the enemy record bytes `+0x7B`, `+0x79`, `+0x78`, `+0x7A` (step 12) |
| `+0x12C` | `u8[4]` | affinityClr | cleared out of the same bytes (step 12) |
| `+0x130` | `u16` | packedParam | -1 by the word store `0x00384991` in `0x003848E0`; not read by `0x003112F0` or `0x00385BA0` |
| `+0x132` | `u8[2]` | zero132 | zeroed by `0x003848E0`; not read by `0x003112F0` |
| `+0x134` | `f32` | knockback | zeroed by `0x003848E0`; with flagsB bit 3 the resolver stores `0x00385E50`'s value here (`0x0038680F`-`0x0038682E`; [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)) |
| `+0x138` | `i32` | echoB | to [`0x02EBF190`]`+0x5B0E` (low byte) when not -1 (`0x00385BA0`) |
| `+0x13C` | `i32` | echoA | to [`0x02EBF190`]`+0x5B00` when not -1 (`0x00385BA0`) |
| `+0x140` | `u32` | flagsC | bits 4, 5, 6, 7: flags for the status and effect writes; bit 14: sound `0x34` |
| `+0x144` | `u8[4]` | zero144 | zeroed only by the memset in `0x003848E0`; read by no function; nothing fixes its width |

## State

The applier writes only to the records it is given and the globals named in the steps
(`[0x02EBF190]+0x5B00`/`+0x5B0E` and the party's gil).

## Modding notes

- An action's effect on HP and MP is "present" only with its bit in `+0x2C`; the values alone do
  nothing.
- An enemy's stat change is written as the new stat value, not a delta: the applier adjusts the
  modifier so the stat lands on it.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags `0x00307300` fills from `flagsB`.
- [Combos](combos.md) - `flagsB` bit 1.
- [Action phases](action-phases.md) - where the resolution runs.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the status
  numbers of the masks.
- [The status write](../Status-Effects-And-KO/status-changes.md)
  - what `0x0030E360` does with each add and remove.
