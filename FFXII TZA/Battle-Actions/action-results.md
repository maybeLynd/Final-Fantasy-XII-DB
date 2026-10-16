---
title: "Action results: the result record a resolved action produces and how it is applied to target and user"
kind: "system"
category: "Battle actions"
addresses: "003848E0, 003112F0, 00385BA0, 0030B9B0"
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

`003848E0(record)` (205 bytes) prepares the record. It zeroes `+08`<sub>h</sub>-`+147`<sub>h</sub>
(`003848EF`-`003848F5`), leaves `+00`<sub>h</sub>-`+07`<sub>h</sub> to the caller, sets bit 0 of `+2C`<sub>h</sub>, and sets the
"nothing to do" values (`003848FA`-`003849A0`):

- `-1` in the dword at `+38`<sub>h</sub> and in the dwords at `+138`<sub>h</sub> and `+13C`<sub>h</sub>;
- `-1` in the words at `+30`<sub>h</sub>, `+11C`<sub>h</sub> (both level bytes `FF`<sub>h</sub>), `+11E`<sub>h</sub>-`+124`<sub>h</sub>, `+130`<sub>h</sub> and
  the eight words `+42`<sub>h</sub>-`+50`<sub>h</sub>;
- `FF`<sub>h</sub> in the bytes `+3C`<sub>h</sub>-`+41`<sub>h</sub>;
- `-1` in all 32 dwords from `+5C`<sub>h</sub> and all 32 words from `+DC`<sub>h</sub>.

It is called by the resolver `00385F60` (`0038600F`), the preview `00385680` (`0038586C`) and the four
status-result builders `00385DF0`, `00386A50`, `00386A70` and `00386AE0`. The record lives on the
caller's stack.

### The applier

`003112F0(record, sourceStats, targetStats, actionId, flags)` (2,040 bytes) is called
by the effect applier `00307300` (`00307436`, `00307ABD`), the periodic maintenance `00310DB0`
(three calls), the effect-bit write `0030E130` and the status write `0030E360`. In order:

1. **Skip test.** Unless bit 0 of `flags` is set, nothing is applied when `0030B9B0(targetUnit,
   sourceUnit)` is non-zero - the global part `0030B770` or the unit part `0030B7F0` of the eligibility
   mask, with the hostile flag from the relationship class ([Area of effect](area-of-effect.md))
   (`00311354`-`00311367`).
2. **Metadata** `00385BA0`: `+138`<sub>h</sub> (when not -1) goes to the byte `[02EBF190]+5B0Eh`, `+13C`<sub>h</sub> to the
   dword `[02EBF190]+5B00h`; a non-zero steal byte `+32`<sub>h</sub>/`+33`<sub>h</sub>/`+34`<sub>h</sub> clears bit 0/1/2 of
   `[targetUnit+6A0h]+14h`; with `+1C`<sub>h</sub> = 1 the battle-message events are posted (`00469EC0`).
3. Bit 19 of `+2C`<sub>h</sub> sets bit 3 of the target unit's `+E9A`<sub>h</sub>; bit 14 of `+140`<sub>h</sub> plays sound `34`<sub>h</sub>
   (`003A1180`, `002DF220`) and sets bit 2 (`00311384`-`003113BF`).
4. **Levels.** A target level `+11C`<sub>h</sub> other than `FF`<sub>h</sub> is applied with `0030C650(target, level, 0)`,
   and the user's `+11D`<sub>h</sub> likewise (`003113CB`-`003113FD`).
5. **Steal and poach.** For an enemy-side target, each non-zero steal byte `k` (`+32`<sub>h</sub>-`+34`<sub>h</sub>) adds
   one of the item at `[targetUnit+E60h]+32h+2k` (when not `FFFF`<sub>h</sub>) with `003008A0`, clears bit `k`
   of `[targetUnit+6A0h]+14h` (already cleared by step 2) and calls `00316A50(3)`; a poach item `+38`<sub>h</sub> other than -1 is added (`00311402`-`003114A8`).
6. **Statuses.** Each bit `n` of the add mask `+54`<sub>h</sub> calls `0030E360(target, source, n, +5Ch[n],
   +DCh[n], ..., 3)` (add); each bit of the remove mask `+58`<sub>h</sub> calls `0030E360(target, source, n, 0, 0,
   ..., 0)` (remove). Bits 4 and 5 of `+140`<sub>h</sub> choose a flag passed to those calls (`003114D2`-`003115AF`).
7. **Status parameters.** Every `+5Ch[n]` that is not negative is copied to target `+BCh + 4n` (the
   status durations) and every `+DCh[n]` to target `+13Ch + 2n` (`003115B6`-`00311606`).
8. **Target HP and MP.** With bit 8 of `+2C`<sub>h</sub>, `+24`<sub>h</sub> is applied to the target's HP - set outright
   (`00300520`) with bit 3, otherwise added (`00300530`, the HP write). With bit 14, `+2A`<sub>h</sub> goes to the
   target's MP - set (`00300C90`) with bit 4, otherwise added (`00300CE0`). A non-zero `+1D`<sub>h</sub> adds
   `+1Dh * [target+28h]` (whole max-MP units) to the target's secondary resource (`00300BC0`) (`00311608`-`003116E0`).
9. **User HP and MP.** With bit 7 of `+2C`<sub>h</sub>, `+20`<sub>h</sub> is applied to the user's HP (set with bit 1);
   with bit 13, `+28`<sub>h</sub> to the user's MP (set with bit 2) (`00311700`-`00311775`).
10. **Effect bits.** `+3C`<sub>h</sub> and `+3D`<sub>h</sub> (when not `FF`<sub>h</sub>) are set in the target's effect layer
   (`0030E130` mode 2); `+3E`<sub>h</sub>-`+41`<sub>h</sub> are cleared (mode 0); bits 6 and 7 of `+140`<sub>h</sub> choose the
   flags. The eight timers `+42`<sub>h</sub>-`+50`<sub>h</sub> that are not negative are copied to target
   `+17C`<sub>h</sub>-`+18A`<sub>h</sub> (`00311778`-`00311894`).
11. **Enemy stat changes.** For an enemy-side target, each of `+11E`<sub>h</sub>, `+120`<sub>h</sub>, `+122`<sub>h</sub>, `+124`<sub>h</sub>
    that is not -1 sets the target's modifier so that the stat becomes that value: `+08h += v - str`
    (`+2A`<sub>h</sub>), `+0Ah += v - mag` (`+2B`<sub>h</sub>), `+12h += v - def` (`+2F`<sub>h</sub>), `+14h += v - mres`
    (`+30`<sub>h</sub>) (`0031189B`-`00311915`).
12. **Enemy affinity bytes.** For an enemy-side target, `+128`<sub>h</sub>-`+12B`<sub>h</sub> are OR-ed into bytes
    `+7B`<sub>h</sub>, `+79`<sub>h</sub>, `+78`<sub>h</sub>, `+7A`<sub>h</sub> of `[targetUnit+6A0h]`, and `+12C`<sub>h</sub>-`+12F`<sub>h</sub> cleared out of
    the same bytes; each change sets bit 7 of that record's first dword (`0031193C`-`00311A7E`).
13. **Gil.** A non-zero `+08`<sub>h</sub> is subtracted from the party's gil, not below 0 (`00253690`,
    `00254EE0`) (`00311A84`-`00311A9E`).
14. Bits 2 and 3 of the target unit's `+E9A`<sub>h</sub> are cleared; when anything above changed and bit 9 of
    `flags` is clear, the target's stats are rebuilt (`0030FED0(target, 0)`) (`00311AA3`-`00311AC5`).

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u8` | flags0 | left to the caller by `003848E0` |
| `001`<sub>h</sub> | `u8[3]` | pad01 | left to the caller |
| `004`<sub>h</sub> | `u8` | outcome | 1-5 the evade/guard outcome of slot 41 (`003896B0`); 6 at `00386347` and `003858A2`; 9 at `0038588A`; 10 at `00386303` |
| `005`<sub>h</sub> | `u8[3]` | pad05 | left to the caller |
| `008`<sub>h</sub> | `u32` | gilCost | subtracted from the party's gil (step 13) |
| `00C`<sub>h</sub> | `u8[12]` | zero0C | zeroed by `003848E0`; not read by `003112F0` |
| `018`<sub>h</sub> | `u32` | flagsB | bit 1: continue a combo (`00388660`); bit 2: guard decision (`00385A1C`-`00385A2D`); bit 3: knockback (`003896B0`); `00307300` copies bits 0-3 to target entry bits 11, 10, 9, 8 |
| `01C`<sub>h</sub> | `u8` | resolved | 1: post the battle-message events (`00385BA0`) |
| `01D`<sub>h</sub> | `i8` | mpUnits | whole max-MP units added to the target's secondary resource (step 8) |
| `01E`<sub>h</sub> | `u16` | zero1E | zeroed by `003848E0`; not read by `003112F0` |
| `020`<sub>h</sub> | `i32` | userHp | user HP change or value (step 9) |
| `024`<sub>h</sub> | `i32` | targetHp | target HP change or value (step 8) |
| `028`<sub>h</sub> | `i16` | userMp | user MP change or value (step 9) |
| `02A`<sub>h</sub> | `i16` | targetMp | target MP change or value (step 8) |
| `02C`<sub>h</sub> | `u32` | flagsA | bit 0 set by `003848E0`; bits 1-4 set-not-add; 7, 8, 13, 14 present; 19 marks the target unit |
| `030`<sub>h</sub> | `u16` | unused30 | `FFFF`<sub>h</sub> from `003848E0`; not read by `003112F0` |
| `032`<sub>h</sub> | `u8[3]` | steal | steal slots 0-2 (step 5, `00385BA0`) |
| `035`<sub>h</sub> | `u8[3]` | zero35 | zeroed by `003848E0`; not read by `003112F0` |
| `038`<sub>h</sub> | `i32` | poachItem | item id in the low word; -1 none (step 5) |
| `03C`<sub>h</sub> | `u8[2]` | effectSet | effect bits to set; `FF`<sub>h</sub> none (step 10) |
| `03E`<sub>h</sub> | `u8[4]` | effectClear | effect bits to clear; `FF`<sub>h</sub> none (step 10) |
| `042`<sub>h</sub> | `i16[8]` | effectTimers copied to target `+17C`<sub>h</sub>..`+18A`<sub>h</sub> when not negative |  |
| `052`<sub>h</sub> | `u16` | zero52 | zeroed by `003848E0`; not read by `003112F0` |
| `054`<sub>h</sub> | `u32` | addMask | statuses to add (step 6) |
| `058`<sub>h</sub> | `u32` | removeMask | statuses to remove (step 6) |
| `05C`<sub>h</sub> | `i32[32]` | statusA | per-status parameter A (duration); copied to target `+BC`<sub>h</sub> |
| `0DC`<sub>h</sub> | `i16[32]` | statusB | per-status parameter B (beat timer); copied to target `+13C`<sub>h</sub> |
| `11C`<sub>h</sub> | `u8` | targetLevel | `FF`<sub>h</sub> none (step 4) |
| `11D`<sub>h</sub> | `u8` | userLevel | `FF`<sub>h</sub> none (step 4) |
| `11E`<sub>h</sub> | `i16[4]` | enemyStats | new Strength, Magick Power, Defence, Magick Resist; -1 none (step 11) |
| `126`<sub>h</sub> | `u16` | zero126 | zeroed by `003848E0`; not read by `003112F0` |
| `128`<sub>h</sub> | `u8[4]` | affinitySet | OR-ed into the enemy record bytes `+7B`<sub>h</sub>, `+79`<sub>h</sub>, `+78`<sub>h</sub>, `+7A`<sub>h</sub> (step 12) |
| `12C`<sub>h</sub> | `u8[4]` | affinityClr | cleared out of the same bytes (step 12) |
| `130`<sub>h</sub> | `u16` | packedParam | -1 from `003848E0`; not read by `003112F0` |
| `132`<sub>h</sub> | `u8[2]` | zero132 | zeroed by `003848E0`; not read by `003112F0` |
| `134`<sub>h</sub> | `f32` | knockback | zeroed by `003848E0`; with flagsB bit 3 the resolver stores `00385E50`'s value here (`0038680F`-`0038682E`; [Damage formula](../Damage-And-Battle-Formulas/damage-formula.md)) |
| `138`<sub>h</sub> | `i32` | echoB | to [`02EBF190`]`+5B0E`<sub>h</sub> (low byte) when not -1 (`00385BA0`) |
| `13C`<sub>h</sub> | `i32` | echoA | to [`02EBF190`]`+5B00`<sub>h</sub> when not -1 (`00385BA0`) |
| `140`<sub>h</sub> | `u32` | flagsC | bits 4, 5, 6, 7: flags for the status and effect writes; bit 14: sound `34`<sub>h</sub> |
| `144`<sub>h</sub> | `u32` | zero144 | zeroed by `003848E0`; not read by `003112F0` |

## State

The applier writes only to the records it is given and the globals named in the steps
(`[02EBF190]+5B00h`/`+5B0E`<sub>h</sub> and the party's gil).

## Modding notes

- An action's effect on HP and MP is "present" only with its bit in `+2C`<sub>h</sub>; the values alone do
  nothing.
- An enemy's stat change is written as the new stat value, not a delta: the applier adjusts the
  modifier so the stat lands on it.

## Related

- [Area of effect](area-of-effect.md) - the target entry flags `00307300` fills from `flagsB`.
- [Combos](combos.md) - `flagsB` bit 1.
- [Action phases](action-phases.md) - where the resolution runs.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - the status
  numbers of the masks.
- [The status write](../Status-Effects-And-KO/status-changes.md)
  - what `0030E360` does with each add and remove.
