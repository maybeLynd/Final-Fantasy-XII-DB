---
experiment: EXP-007
title: Can the harness navigate the front-end and load a save without the operator?
status: RUN 2026-09-08 — YES. Cold launch to Vaan standing in Dalmasca Estersand, autonomously.
contract: none — a harness-capability question
tool: Database/Tools/analysis-kit/gfz-scripts/window_capture.py, runtime_input_probe.py, window_focus.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-007 — from a cold launch to a loaded save, with nobody at the keyboard

## What a player sees

The title menu, the save list, and Vaan standing in the Estersand. Exactly what anyone sees. The
point is that **no one pressed anything** — the harness launched the game, read the screen, moved
the cursor, chose Load Game, picked a file and watched it load.

## Why this was the block

`INTEGRATION` parity is `NOT COVERED` for **all six** reconstructed pilots and stays that way
until the reconstruction can be exercised against the game in a real state. `ES-1` — load a save
autonomously — is the only route to that, and `ES-1` could not navigate deliberately while the
harness was **blind**: `ffxii_runtime.py state` reported `TITLE` after `EXP-006` had plainly moved
the game.

> **The missing capability was not input. It was sight.**

## The instrument, and the trap it was built to catch

`window_capture.py` photographs the game window. Two paths, tried in order:

| path | at the title menu |
|---|---|
| `PrintWindow` with `PW_RENDERFULLCONTENT` | **93.8 % one colour, black** — a Direct3D swap chain does not draw itself through GDI |
| screen `BitBlt` of the window rectangle | a real image |

**It reports which path produced the image and how close to one flat colour the result is**,
because a capture tool that cannot tell *"the screen is black"* from *"the capture failed"*
manufactures confident negatives. That distinction did work immediately: the `PrintWindow`
attempt was correctly rejected rather than written out as a photograph.

### The first run photographed the wrong window

```text
capture 1   1292 x 726    the game's title bar, off-centre, next to a NEIGHBOURING app
capture 2   1938 x 1089   the game
```

**The process was DPI-unaware.** `GetWindowRect` handed back logical coordinates while the screen
DC is in physical pixels, so the `BitBlt` grabbed the wrong part of the desktop. Fixed by
declaring `PER_MONITOR_AWARE_V2` **before any rectangle is requested** — the window is 1938 × 1089
physical, not 1292 × 726.

> The image itself is what caught this. Every number the tool printed was self-consistent.

## What the harness did, unaided

| step | key | observed |
|---|---|---|
| cold launch | — | the main menu: **New Game / Load Game / Trial Mode / Credits / Exit**, cursor on Load Game |
| one press | `Down` | cursor moved **Load Game → Trial Mode** — single-step, deliberate, photographed |
| one press | `Up` | back to Load Game |
| confirm | `Circle` (Space) | the Load screen — *"Checking save data…"* |
| wait | — | **six save files listed** |
| confirm | `Circle` ×2 | **Vaan, Dalmasca Estersand, HP 103/103, MP 33** |

The saves the machine can now reach:

| slot | place | time |
|---|---|---|
| 001 | Rabanastre, Eastgate | 00:08:30 |
| *(auto)* | Dalmasca Estersand, The Stepping | 00:08:42 |
| 002 | Giza Plains, Throne Road | 06:39:57 |
| 003 | Rabanastre, Eastgate | 06:45:50 |
| 004 | Rabanastre, Southgate | 06:53:57 |
| 005 | Dalmasca Westersand, The Western Divide | 04:47:23 |

Evidence: [the main menu](evidence/EXP-007-01-main-menu.png) ·
[the save list](evidence/EXP-007-02-save-list.png) ·
[loaded, in the Estersand](evidence/EXP-007-03-loaded-estersand.png).

## What the picture proved about the harness itself

**`state` said `TITLE` while Vaan was on screen.** Two separate errors, both now corrected:

1. **`0215FDA0` is the SCRIPT VM's entity-name table**, not a general entity table. Nothing puts a
   slot on it merely because the world has bodies in it. The harness had been reading a
   script-VM fact as a world fact.
2. **"on the free list" and "has content" are independent.** With a map loaded, all 128 records
   are *still* linked into the free list **and all 128 carry a populated body**.

The verdict now reads the two observables that actually moved, and **refuses to name a screen**:

```text
just launched   area id  -1   save buffer empty       -> UNKNOWN   (no baseline; it says so)
front-end       area id  12   save buffer empty       -> MENU
save loaded     area id 227   save buffer populated   -> IN-WORLD
```

**Both directions were controlled**: the game was closed, relaunched, and the verdict returned to
`MENU` — and passed through an honest `UNKNOWN` while the front-end was still initialising. A
verdict that could only ever say `IN-WORLD` would have been as wrong as the one it replaced.

## Two questions this moved on the way past

**`ER-1` — what a script-entity record holds once a map is loaded.** At the menu the 46 bytes
beyond the links are **zero**; with a map loaded **128 of 128 records carry a body**. So the table
is populated at map load, **not lazily when a script first names something**. Three records read
live:

```text
slot 0   +00 0215FDE0  +08 0            +10: 63a8436e 13006d00 02100000 00000000  01 01 02 02  -1 3 4 0
slot 1   +00 0215FE20  +08 0215FDA0     +10: 83a8436e 01006d00 02100100 00000100  01 01 02 02  ...
slot 2   +00 0215FE60  +08 0215FDE0     +10: b3a8436e f0006d00 02100200 01000200  01 01 02 02  ...
```

**`+0x1A` is the slot index** (0, 1, 2) and `+0x16` holds a constant `0x006D` across all three,
`+0x18` a constant `0x1002`. The dword at `+0x10` steps by `0x20` then `0x30`. **Naming any of
these from three records would be exactly the tidy story the evidence does not support** — what
is claimed here is that the table is populated at map load and that the index appears at `+0x1A`.

**`EQ-1` — are the 12 empty st2e slots unused or merely unloaded?** Measured across three states:
**0 groups just after launch, 16 at the menu, and still 16 with a map loaded.** Loading a map
filled **no** additional group. That is one map and one save, so it narrows `EQ-1` rather than
closing it — but "merely unloaded at the title" is now the weaker reading.

### A link-direction contradiction, found in passing

`ER-1` records the free list as ***“`+0x00` = `prev`, `+0x08` = `next`, head at slot 0, tail
at slot 127”***. **Those two halves cannot both be true**, and the live read says which is
wrong. Slot *i* lives at `0215FDA0 + i*64`, so `FDA0` `FDE0` `FE20` `FE60` are slots 0–3:

```text
slot 0   +0x00 = 0215FDE0 (slot 1)   +0x08 = 0            <- one end of the list
slot 1   +0x00 = 0215FE20 (slot 2)   +0x08 = 0215FDA0 (slot 0)
slot 2   +0x00 = 0215FE60 (slot 3)   +0x08 = 0215FDE0 (slot 1)
```

**Stated without the disputed labels: `+0x00` points at the next-HIGHER slot and `+0x08` at
the next-LOWER one; slot 0's `+0x08` is null.** So if the head is slot 0, `+0x00` is `next`
and `+0x08` is `prev` — the opposite of what the ledger says.

> **Which end the allocator pops is NOT established here**, and it is what decides the
> `next`/`prev` naming. The address-ordered statement above is label-free and is what this
> experiment claims; the naming is left to whoever reads the allocator. Recorded on `ER-1`
> rather than silently corrected in one direction.

## Confidence

| claim | confidence | why |
|---|---|---|
| the harness can navigate the front-end unaided | **PROVEN** | photographed at each step; a single `Down` moved the cursor one row |
| the harness can load a save unaided | **PROVEN** | Vaan in the Estersand, from a cold launch, photographed |
| area id 12 is the front-end, not a screen within it | **PROVEN** | unchanged while the cursor moved and while the Load screen listed six saves |
| area id 227 is the loaded save's area | **HIGH** | it appeared exactly when the save loaded; no second sample |
| the script-entity table is populated at map load | **PROVEN** | 0 of 128 bodies at the menu, 128 of 128 in-world |
| `+0x1A` is the slot index | **HIGH** | three consecutive records, 0/1/2; not read across the whole table |
| loading a map adds no st2e group | **PROBABLE** | 16 at the menu, 16 in-world — one map, one save |
| `PrintWindow` cannot photograph this game | **HIGH** | 93.8 % black at the menu; it did succeed once, on the in-world frame |

## What this experiment does not settle

**What area id 227 means.** It is the id present when this save is loaded. Nothing here maps ids
to places, and one sample is not a mapping.

**Anything about the save files' contents.** They were read by the game, listed on screen, and
one was loaded. **No save file was opened, parsed or modified by any tool here.**

**That navigation is robust.** The sequence worked once, with fixed delays, from a known starting
cursor. A reusable route needs the screen recognised rather than assumed — which is now possible,
and is not done.

## Related

- [`EXP-006`](EXP-006-the-array-is-written-on-transition.md) — the input mechanism this builds on
- [`EXP-003`](EXP-003-script-entity-table.md) — the script-entity table at the title screen
- [how a script names a thing in the world](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md) — the table's static reading
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) — the harness and its tools
