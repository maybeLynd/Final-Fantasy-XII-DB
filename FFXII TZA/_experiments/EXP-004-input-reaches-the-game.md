---
experiment: EXP-004
title: Does synthetic keyboard input reach the game at all?
status: OVERTURNED 2026-09-08 by [`EXP-006`](EXP-006-the-array-is-written-on-transition.md) — the negative was a FOCUS ARTIFACT
contract: none — a harness-capability question; overturned by `EXP-006`
tool: Database/Tools/analysis-kit/gfz-scripts/ffxii_runtime.py (snapshot / diff / churn)
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-004 — does synthetic input reach the game?

> ## Overturned the same day — read this first
>
> **This experiment's negative was correct about its own measurement and wrong about the
> world.** Every window here was taken with the **harness** in the foreground, not the game,
> and Windows delivers keyboard input to the foreground window. The keypresses never arrived.
>
> [`EXP-006`](EXP-006-the-array-is-written-on-transition.md) repeated it with the game verifiably foreground, using this same churn
> instrument and this same symmetry check:
>
> | | NEW bytes | the REVERSAL |
> |---|---:|---:|
> | **here**, unfocused | 319 | 311 |
> | **`EXP-006`**, focused | **17,584** | **31** |
>
> **The symmetry check was right both times.** 319 against 311 is noise measuring itself;
> 17,584 against 31 is an effect. The instrument was never the problem — **the variable list
> was.** Foreground was not in it.

## Question

`ES-1` needs a save loaded. An earlier attempt sent scan-code input and **nothing happened**, but
that was **not diagnosable**: the only observable separated *title* from *a map is loaded*, and a
menu cursor moves between them invisibly. `ET-1` was filed for the instrument that would make the
question answerable. This is that instrument, used on that question.

## Hypothesis

If `SendInput` with `KEYEVENTF_SCANCODE` reaches the game, **some** memory it owns changes as a
consequence — a menu index, an input-state buffer, a sound cue. If it does not reach the game,
memory changes exactly as much as it would have anyway.

## Instrumentation

`ffxii_runtime.py snapshot` captures four regions covering `.data` and the BSS spans where every
runtime table this project has found lives — **8,454,144 bytes in 0.66 s**, page-chunked so an
uncommitted page inside a span costs one page instead of the whole read, and **the holes are
counted** because a snapshot silently full of zeros would diff clean against anything.

## The control that makes this an experiment

**A running game rewrites thousands of bytes a second.** Measured, with no input at all and three
seconds between captures:

```
data          13 run(s),    95 bytes
bss_low      364 run(s), 6,565 bytes
bss_mid       18 run(s),   262 bytes
bss_high      12 run(s),   896 bytes
                          7,818 bytes changed in 3 seconds, doing nothing
```

**So a raw diff across "press a key" proves nothing**, and the instrument needs a second control:
**the noise floor** — how much a *no-input* window differs from *another* no-input window under the
same subtraction.

## Observed result

| comparison | NEW bytes |
|---|---:|
| baseline `A→B`, test `B→C` — **no input in either** | **242** |
| baseline `A→B`, test `C→D` — **keypress in the test window** | 319 |
| baseline `B→C`, test `C→D` — keypress in the test window | 251 |
| baseline `C→D`, test `A→B` — **reversed: no-input measured against the keypress** | **311** |

> ### The reversal is the result
>
> A keypress window scores **319** against a no-input baseline. A **no-input** window scores **311**
> against the keypress baseline. **The measure is symmetric.**
>
> **A real effect appears in one direction. Noise appears in both.** 319 against a floor of 242 and
> a reversal of 311 is not a signal; it is two arbitrary two-second windows of a running game
> failing to touch identical byte sets.

**Conclusion: the keypress produced no detectable change anywhere in 8.4 MB of the game's own
writable memory.**

## Interpretation

**The input is not reaching the game**, or reaches it and is discarded before anything observable
happens. The window *is* focused — `SetForegroundWindow` succeeds and `GetForegroundWindow` returns
the game's own handle — so this is not a focus failure.

That is a much stronger statement than the previous block's *"not diagnosable"*, and it redirects
`ES-1`: **the next thing to try is a different input path, not a different key.** Candidates, none
tested: virtual-key `SendInput` rather than scan codes; a virtual gamepad (the title screen may
accept only a pad); raw HID injection.

## Confidence

| claim | confidence | why |
|---|---|---|
| the game changes ~7,818 bytes per 3 s at the title screen | **PROVEN** | measured, one window |
| the instrument's noise floor is ~240–320 bytes | **PROVEN** | three independent window pairs |
| the keypress produced no change above noise | **PROVEN** | forward 319, reversal 311 — symmetric |
| the input never reached the process | **PROBABLE** | consistent with the above, but "reached and was discarded" produces the same reading |
| which input path would work | **UNKNOWN** | none tested |

## What this experiment cannot settle

**Whether the game would respond to a different input method.** It tested one method, one key,
one screen.

**Whether an effect exists outside the four captured regions.** The snapshot covers `.data` and
three BSS spans — **8.4 MB**, not the whole address space. A change confined to the heap or to a
module's own data would not be seen. That is a real limit and it is the reason the conclusion is
*"no detectable change"* rather than *"no change"*.

## Related

- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) §6 — the capability list this closes one item on
- [`EXP-003`](EXP-003-script-entity-table.md) — the free-list observable `state` is keyed on
