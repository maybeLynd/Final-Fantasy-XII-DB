---
experiment: EXP-009
title: Does the reconstruction give the same answer the running game gives, on the game's own input?
status: RUN 2026-09-08 — 2 distinct inputs, captured at the game's own call site; game, original and reconstruction all agree
contract: ../18-Audio/CONTRACT-field-music-selection.md
tool: Database/Tools/analysis-kit/gfz-scripts/hwbp.py, field_music_table.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-009 — the running game as the oracle

## What a player sees

Load a save and the right music starts. This is the first time this project has checked its own
reimplementation of that decision **against the game making it**, rather than against the shipped
bytes replayed in an emulator.

## The question

`INTEGRATION` is `NOT COVERED` for all six pilots, and
[the parity standard](../../../Reconstruction/PARITY-STANDARD.md) §3 asks for the reconstruction
to be exercised *"through the caller the game actually uses, with inputs the game actually
supplies"*. Every differential in this tree so far compared the reconstruction against **the same
static artifact it was derived from**, executed rather than read.

## Method

Three hardware breakpoints inside `FieldMusic_Select` (`003EAA70`), placed so that one call
yields both its inputs and its answer:

```text
003EAA7D   just after the progress getter returns
             rbx = the field id      (set by `mov ebx, ecx` at the entry)
             rax = the progress      (what 00265270 just returned)
003EAAFE   the first  ret            rax = the track id
003EAB54   the second ret            rax = the track id
```

Entry and exit are paired **within a thread, in order**. The game's own table is then read out of
the same process (`[0x02B5E0D0]`, magic `MUS0`), and the same field id and progress are put
through the emulated shipped bytes and through the reconstruction at that table's real address.

**Both captures were taken with the corrected `hwbp.py`** — the version that sets `EFLAGS.RF` and
clears `DR6`. The previous version re-fired on the instruction it had just reported, and every
count it produced was retracted.

## Result

| field | progress | the game | shipped bytes, emulated | the reconstruction |
|---:|---:|---:|---:|---:|
| 227 | 68 | **100** | 100 | 100 |
| 253 | 1,580 | **20** | 20 | 20 |

**126 entry→exit pairs in each run, 0 unpairable rows**, and within a run every pair carries the
same triple — which is what standing in one area should produce.

Two areas, reached by loading two different saves while the breakpoints were armed. Raw traces:
[field 227](evidence/EXP-009-field227-trace.tsv) · [field 253](evidence/EXP-009-field253-trace.tsv).

> ### Every call left through the SECOND `ret`
>
> `003EAAFE` recorded **0 hits** across both runs while `003EAB54` recorded 126 in each. The
> function has two exits and the game, on these inputs, never took the first.

## CORRECTED 2026-09-10 — timing and observer-effect conclusions withdrawn

The original text concluded **"Field music is not selected per frame"** from 126 calls over a
reported 70-second run. That conclusion is withdrawn. The raw traces contain no timestamps,
frame counters or phase boundaries, so they cannot locate calls relative to the load or measure
frame progress while the observer is attached. An unreached hit cap does not supply those controls.
This capture does not discriminate load-only selection from a frame-gated or perturbed caller.

The original text also concluded **"A hot breakpoint does not starve input."** That general
claim is withdrawn. The reported menu/load navigation and keypress-counter change `0 → 6`
support response during those actions only. They do not establish absence of observer effects
or loaded-state survival after detach. Historical armed stalls remain open under RT-1;
[EXP-010](EXP-010-loaded-state-no-arm.md) establishes only its matched no-arm control.

## Confidence

| claim | confidence | why |
|---|---|---|
| the game passes the area id as the field id | **PROVEN** | `rbx` = 227 and 253, matching the area id observed in each run |
| the game's answers are 100 and 20 | **PROVEN** | read from `rax` at its own `ret`, 126 times each |
| the reconstruction agrees on those inputs | **PROVEN** | same table, same address, same inputs |
| every call exits through `003EAB54` | **HIGH** | 252 of 252 pairs, but only two distinct inputs |
| field music is selected at map load, not per frame | **WITHDRAWN** | missing frame/time/phase and observer-effect controls |

## What this experiment does not settle

**It is not `INTEGRATION` coverage.** The reconstruction is still invoked by a test driver.
Substitution through the native caller remains untested, as do its broader consequences across
table binding/lifetime, state changes and scheduling. The former claim that substitution was
the entire remaining gap is withdrawn. A matching return on two input conditions does not close
those evidence requirements or demonstrate that the intended music plays.

**The observed input population is two.** ASTRA reparsed both preserved TSVs on 2026-09-10:
each has 252 rows, 126 within-thread entry/return pairs, no unpaired rows, and one distinct tuple:
`(227,68,100)` or `(253,1580,20)`. These are 252 repeated observations over two input conditions,
not 252 distinct states. Columns are `tid,rip,rax,rbx,rcx,rdx`; none records time or frames.

**Nothing is claimed about the progress value.** `1,580` and `68` were read from the getter's
return; **what the progress counts is not established**, and the contract's `DG-1` note about the
table's provenance is unaffected.

**No claim that the two `ret`s differ in meaning.** `003EAAFE` was never taken here. Whether it is
an error path, an early-out, or simply unreached on these inputs is **not read**.

## Related

- [`EXP-008`](EXP-008-the-real-music-table.md) — the `MUS0` table these runs use
- [`EXP-007`](EXP-007-navigating-the-front-end.md) — the navigation that reaches a loaded save
- [the field-music contract](../18-Audio/CONTRACT-field-music-selection.md) — §16's parity plan
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) §8e — the storm, and why these counts are trustworthy when the earlier ones are not
