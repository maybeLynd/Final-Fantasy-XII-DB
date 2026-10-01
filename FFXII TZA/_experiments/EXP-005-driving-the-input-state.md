---
experiment: EXP-005
title: Can the game be driven by writing the input state it reads?
status: RESOLVED 2026-09-08 by [`EXP-006`](EXP-006-the-array-is-written-on-transition.md) — the chain stands; the array is TRANSITION-written, so a level cannot drive it
contract: none — a harness-capability question; resolved by `EXP-006`
tool: Database/Tools/analysis-kit/gfz-scripts/runtime_poke.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-005 — driving the game through its own input state

> ## Resolved — read this first
>
> **Every measurement below is correct.** What was wrong was the conclusion drawn from the
> value persisting. [`EXP-006`](EXP-006-the-array-is-written-on-transition.md) held a key for real, wrote `0` over the game's own `1`, and
> **the game never put it back** — fifteen polls, 300 ms, key still down.
>
> **The game writes this byte on a state CHANGE and at no other time.** So a written level
> persists because nothing rewrites levels, and nothing responds because what is consumed is
> the change. Explanation 3 below was the right family. **Explanation 1 is contradicted** —
> unfocused input is not ignored, it never arrives.
>
> The *“genuinely irreducible manual step”* named at the end of this page **was not
> irreducible**: the operating system can hold the key and the harness can hold the
> foreground. Charter §16 makes the operator a fallback, and it was reached for too early.

## Question

`EXP-004` established that neither scan-code nor virtual-key `SendInput` has any detectable effect
on the game. **The operator proposed the better route**: find the input state the game itself reads
and write it directly, rather than feeding the operating system and hoping.

## The chain, and that it is not new

[Binding profiles, remapping and control state](../15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md)
already documents `0079E6A0`, the `(code - 0x1C)` bias, and the backend reached as
`*(void **)(FUN_00796E20() + 0xDF8)`. **That reading is confirmed exactly.** What is new here is
its **runtime validation** — the same chain resolved in a live process, with the addresses it
actually produces.

```
[0x02EA5368]                  ->  0x01F7E350   the input manager
manager + 0xDF8               ->  0x01F7F150   the backend
backend + device*8 + 0x118    ->  0x0E1814C0-ish, HEAP -- it moves between launches
block + 0x30 + (code - 0x1C)  ->  one byte per input, non-zero means held
```

**Device 0 is the only non-null of the seven** at the title screen — devices 1–6 are `NULL`, which
is what a machine with no gamepad attached should look like.

**The codes are the numbers in `GameSetting.ini`'s `[Keyboard1]` section.** Their minimum is
**28**, which is exactly the `0x1C` the query subtracts — so `index = keymap_value - 28`, and
`Cross=30` lands at index 2, `Start=64` at 36, `Circle=80` at 52.

## Observed result

**The array is all zero at an idle title screen** — a clean baseline, and the reason `runtime_poke`
refuses to write when anything is already held.

**Writes succeed and restore cleanly.** `Start`, `Cross` and `Circle` were each written to `1`, held
12 frames, written back to `0`, and the restore verified by reading back. **No state change**: 128
of 128 entity slots still free, `st2e` still 16 of 28, area id still 12.

> ### The decisive follow-up: the game does not clear the byte
>
> Written to `1` and polled for 400 ms **without** being cleared by the tool:
>
> ```
> observed: [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
> ```
>
> **The value survives.** So it is not a case of the device poll overwriting the write each frame —
> the byte simply sits there and **nothing consumes it**.

## Interpretation

**The chain is right and something else is wrong.** Three readings are established:

1. the static reading of `0079E6A0` is confirmed against a live process;
2. a write to the array **persists**, so no per-frame poll is stamping over it;
3. and **nothing responds** to it.

**A candidate that fits all three, untested:** the game may not be *processing* input at all while
its window is not foreground — which would leave the array unrefreshed *and* unread, and would also
explain `EXP-004`'s two negatives. **Not claimed**, because it was not tested: every measurement
here was taken with the harness in the foreground, not the game.

## Confidence

| claim | confidence | why |
|---|---|---|
| the documented chain resolves in a live process | **PROVEN** | manager, backend and block all non-null and self-consistent |
| device 0 is the only non-null device | **PROVEN** | 1–6 all NULL |
| the array is 256 bytes, one per input, zero when idle | **PROVEN** | read live |
| codes are the `GameSetting.ini` values, biased by 28 | **HIGH** | their minimum is exactly the `0x1C` the query subtracts; no key was independently confirmed by observing a press |
| a write persists and is not cleared | **PROVEN** | 20 polls over 400 ms |
| writing it drives the game | **CONTRADICTED** | no observable change |
| the window must be foreground for input to be processed | **HYPOTHESIS** | fits all three readings; untested |

## What this experiment cannot settle

**Why nothing consumes the byte.** Three explanations survive — the game ignores input when
unfocused, the title screen reads a different path, or the "held" array is downstream of an edge
buffer that is what actually gets polled. **None was tested.**

**Whether the code mapping is right.** The `keymap_value - 28` inference is strong and
**unconfirmed**: nobody watched a real keypress set a specific byte. Doing that needs the operator
to hold a key while the harness polls — which is a genuinely irreducible manual step, and a small
one.

## Related

- [Binding profiles, remapping and control state](../15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md) — the static chain this validates
- [`EXP-004`](EXP-004-input-reaches-the-game.md) — the two OS input paths, both negative
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) — `runtime_poke` and why it is a separate tool
