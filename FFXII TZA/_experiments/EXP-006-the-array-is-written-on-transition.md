---
experiment: EXP-006
title: What actually reads the input state — and why writing it never worked
status: RUN 2026-09-08 — ANSWERED. The array is written on TRANSITION, and real input drives the game.
contract: none — measures the key-to-index mapping and the harness's reach, not a contract claim
tool: Database/Tools/analysis-kit/gfz-scripts/runtime_input_probe.py, window_focus.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-006 — the input array is a transition-written cache, not a command buffer

## What a player sees

Press Start at the title screen and the game answers. Nothing here changes that. What this
experiment settles is why **the harness** could press Start for two experiments running and the
game ignored it — and it turns out the harness had been pressing the wrong thing in the wrong
way, and could not tell because its window was never in front.

## The question

[`EXP-005`](EXP-005-driving-the-input-state.md) found the input state the game reads, wrote a `1`
into it, watched the value **persist for 400 ms**, and observed **no response**. Three
explanations survived and none had been tested:

1. the game does not process input while its window is not foreground;
2. the title screen reads a different path;
3. the held-array is downstream of an **edge** buffer, and the edge is what gets polled.

It also recorded that the cheapest discriminator was *"one irreducible manual step — the operator
holds a key while the harness polls."*

> **It was not irreducible.** The operating system can hold the key, the harness can hold the
> foreground, and the harness can poll. Charter §16 makes the operator the fallback, and this is
> exactly the case where the fallback was reached for too early.

## Method

`window_focus.py` takes the foreground **and verifies it with `GetForegroundWindow`** — a
`SetForegroundWindow` that fails does so silently, so a probe that does not check is measuring its
own terminal. `runtime_input_probe.py` then, for each of 18 keys: presses it through `SendInput`
(virtual-key *and* scan-code forms together), polls the 256-byte array every 10 ms for 350 ms,
releases, and re-checks focus on every poll.

**Two controls, because the negatives in this thread have been wrong twice.** A no-key polling
window of the same length establishes the noise floor, and any index that moves in it is
disqualified from every result. Focus is re-verified at every poll and the losses are counted
rather than averaged away.

## Result 1 — every key moves a byte, and the mapping is now measured

**18 of 18 keys moved exactly one index. Control clean. 0 of ~630 polls lost focus.**

| key | index | code (`index + 28`) | `GameSetting.ini` name |
|---|---:|---:|---|
| Escape | 36 | 64 | **Start** |
| Space | 52 | 80 | **Circle** |
| Tab | 51 | 79 | **L3** |
| LControl | 89 | 117 | **R2** |
| LShift | 90 | 118 | **WalkMode** |

`EXP-005` *inferred* `index = keymap_value − 28` from the fact that the smallest
`GameSetting.ini` code is 28 and the query subtracts `0x1C`. That was a good argument and it was
not a measurement. **Five independent keys now confirm it by observation**, so the claim moves
from `HIGH` to `PROVEN`.

The other thirteen keys land on codes with no `GameSetting.ini` name — `A`→28, `D`→31, `Z`→53,
`Up`→108, `Enter`→77 and so on. **The array is indexed by physical key, not by game action**;
the `[Keyboard1]` section is the binding *from* this space, and most of the space is unbound.

## Result 2 — the game writes the byte only on a TRANSITION

This is the mechanism, and it is what makes the whole thread make sense.

```text
A.  hold Escape for real, so the GAME sets index 36 to 1
    then WRITE 0 over it, and keep holding
    -> 000000000000000        fifteen polls, 300 ms, the game NEVER puts the 1 back

B.  WRITE 1 with no key down
    real press    -> still 1     (no transition in the value the game tracks)
    real release  -> 0           the RELEASE wrote
```

**A is decisive.** If the array were a per-frame snapshot of keyboard state, the still-held key
would have restored the `1` on the very next frame. It did not, for fifteen consecutive polls. So
the game writes this byte **when the key's state changes and at no other time**.

That explains every observation in `EXP-005` at once:

- a written level **persists**, because no transition occurred and nothing rewrites the level;
- and **nothing responds**, because what downstream code consumes is the change, not the level.

**Explanation 3 was the right family.** Explanation 1 is now **CONTRADICTED** — see below — and
explanation 2 is unnecessary.

## Result 3 — real input drives the game, and `EXP-004`'s negative was a focus artifact

Four presses (`Start`, `Circle`, `Enter`, `Circle`) delivered through `SendInput` with the game
verifiably foreground, measured with the same churn instrument and the same symmetry check that
produced `EXP-004`'s null:

| | NEW bytes | the REVERSAL |
|---|---:|---:|
| **`EXP-004`**, unfocused | 319 | 311 |
| **`EXP-006`**, focused | **17,584** | **31** |

`EXP-004` was symmetric — 319 against 311 is noise measuring itself, which is exactly what its
own symmetry check said. **This is 567:1 and one-directional.** Same instrument, same game, same
keys; the only difference is which window had the foreground.

And the game visibly moved:

```text
before   area id  12    save buffer  00000000000000000000000000000000
after    area id  306   save buffer  195ca3aa010000007f96980066040100
```

> **`EXP-004` and `EXP-005` were both measuring an unfocused window.** Two experiments, four
> negatives, one confound — and the confound was never in either experiment's variable list.

## Confidence

| claim | confidence | why |
|---|---|---|
| the array is the live keyboard state | **PROVEN** | 18 of 18 keys, control clean, focus verified every poll |
| `index = GameSetting.ini code − 28` | **PROVEN** | five named keys land on their own codes; was `HIGH` and inferred |
| the array is indexed by physical key, not by game action | **PROVEN** | 13 of 18 keys land on codes no binding names |
| the game writes the byte only on a state change | **PROVEN** | a still-held key never restored an overwritten `0`, 15 polls |
| writing a level cannot drive the game | **PROVEN** | follows from the above, and matches `EXP-005` |
| `SendInput` drives the game when it is foreground | **PROVEN** | 17,584 NEW against a 31-byte reversal; area id and save buffer both moved |
| the game ignores input while unfocused | **CONTRADICTED** | it is not that input is ignored — it is that **unfocused input never arrives** |

## What this experiment does not settle

**What screen the game reached.** Area id 306 and a populated save buffer say it left the title;
**nothing here says what it is showing.** Filed as `EW-1`.

**That the harness's own state verdict is trustworthy.** `ffxii_runtime.py state` still printed
`TITLE` after the game had plainly moved, because its verdict keys on the entity free list and a
menu spawns no entities. **The indicator is too coarse and is now known to be**; it is recorded
here rather than quietly relied on.

**Which `SendInput` form works.** Virtual-key and scan-code were sent together, deliberately —
`EXP-004` tested them separately and got two negatives, and the question of which one works is a
later question than whether either does.

## Related

- [`EXP-005`](EXP-005-driving-the-input-state.md) — found the chain; its leading hypothesis is contradicted here
- [`EXP-004`](EXP-004-input-reaches-the-game.md) — the negative this overturns
- [Binding profiles, remapping and control state](../15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md) — the static reading, now runtime-validated
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) — the harness, and the dbgeng blocker found on the way here
