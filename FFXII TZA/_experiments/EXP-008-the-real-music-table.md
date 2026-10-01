---
experiment: EXP-008
title: What the captured field-music table contains — and whether the reconstruction agrees
status: RUN 2026-09-08 — the table is a `MUS0` resource; 400 cases over the game's own data, 0 mismatches
contract: ../18-Audio/CONTRACT-field-music-selection.md
tool: Database/Tools/analysis-kit/gfz-scripts/field_music_table.py, Reconstruction/Tests/Differential/diff_field_music.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-008 — the field-music table, read out of the running game

## What a player sees

Walk into a zone and the right music plays. The rule that picks the track was reimplemented months
of work ago and tested only against **tables this project invented**, because nobody had ever seen
the real one. This is the real one.

## The question

`DG-1` had traced `0x02B5E0D0` as far as *"an allocated buffer sized from a table; what fills it is
`0032E620` (340 B), **unread**"*. The contract's §15 carried the row *"What fills the table — not
established"*, and `diff_field_music.py` declared `INTEGRATION: NOT COVERED — tables here are
synthetic`.

The capture can establish the buffer's contents. It does not identify the producer or owner.

## The answer is in the first four bytes

```text
[0x02B5E0D0]  ->  0x653B0FC0        a heap buffer; it moves between launches
  +0x00   4D 55 53 30               "MUS0"
  +0x04   1F 05 00 00               max field id = 1311
  +0x08   11 absolute page addresses
```

**`"MUS0"`** — a four-character format tag the static reading never mentioned, because the
function does not check it. And the header is internally consistent in a way that could not be
coincidence: `⌈(1311 + 1) / 128⌉ = 11`, and there are exactly **11 page pointers**.

The buffer holds **`MUS0`-tagged bytes**. `DG-1` remains open for what fills it and its lifetime.

## It parses cleanly under the documented format

`field_music_table.py` walks the live table under the format the contract documents — packed
`u16` where `start = v & 0x7FF` and `length = v >> 11`, run stride `4 + 3*count` — and reports
every disagreement rather than assuming there are none.

| page | field ids | runs | runs with a track | highest start | ends above its top? |
|---:|---|---:|---:|---:|---|
| 0 | 0..127 | 13 | 9 | 129 | yes |
| 1 | 128..255 | 30 | 29 | 260 | yes |
| 2 | 256..383 | 41 | 37 | 390 | yes |
| 3 | 384..511 | 29 | 26 | 511 | yes |
| 4 | 512..639 | 31 | 27 | 640 | yes |
| 5 | 640..767 | 34 | 31 | 767 | yes |
| 6 | 768..895 | 36 | 25 | 898 | yes |
| 7 | 896..1023 | 20 | 15 | 1036 | yes |
| 8 | 1024..1151 | 29 | 23 | 1151 | yes |
| 9 | 1152..1279 | 28 | 28 | 1283 | yes |
| 10 | 1280..1407 | 25 | 13 | 1810 | yes |

**316 runs, 263 of them naming a track. No empty pages.**

> ### A prediction the harness made from a crash, confirmed
>
> `diff_field_music.py` carries a comment earned the hard way: **the format has no chain
> terminator**, so the walk stops only when a run's start exceeds the query, and *"the shipped
> data must therefore always end a page with a run whose start is above every field id that can
> reach it"*. A generator that did not do the same produced access violations rather than test
> failures.
>
> **Every one of the 11 pages does exactly that.** The property was inferred from a bug in a
> synthetic table and is now observed in the real one.

## The differential, against the game's own data

Both sides get the real bytes at the real address — the reconstruction through
`field_music_driver.exe`'s `VirtualAlloc`, the original in Unicorn at `653B0FC0` — because the
`page[]` entries are absolute and at any other base the two would not be receiving the same input.

```text
cases            : 400 over THE GAME'S OWN TABLE
  resolved a track: 112
  resolved -1     : 288
  distinct tracks : 35
mismatches       : 0
no-state check   : 80 of 400 cases re-read the whole table image and the table pointer
                   afterwards; 0 showed ANY byte changed
```

### The driver had a bug that only real data could find

```text
asked VirtualAlloc for 653B0FC0   ->   got 653B0000   ->   refused, correctly
```

**`VirtualAlloc` rounds a reservation down to the 64 KB allocation granularity.** Every synthetic
table had been placed at `0x30000000`, a round address, so this never fired. The requirement was
never that the *allocation* start at the base — it is that the **image bytes** land there, since
that is what the absolute `page[]` entries point into. The driver now reserves the containing
granule, copies at the offset, and **asserts the bytes are where they must be** before running.

> The refusal was right and the reasoning behind it was too narrow. It failed loudly, which is
> why this took one build rather than a debugging session.

## What this moved

**CORRECTED 2026-09-10:** the original promotion to `CONTRACT COVERED` (8/8) confused
captured contents with the producer. The source map now records 7/8 rows exercised and the
producer row NOT EXERCISED. The two original updates were:

- *"What fills the table"* was promoted because the captured bytes became the input. That
  inference is withdrawn: a substituted input cannot exercise its absent producer.
- *"Writes no state"* was `NOT EXERCISED`. The emulator holds every page the function can address,
  so the run re-reads the whole table image and the table pointer afterwards and counts changed
  bytes: **0 of 80 sampled cases**.

The numerical differential results above remain historical observations; the full contract
coverage promotion is withdrawn.

## What this experiment does not settle

**It is not `INTEGRATION` parity.** [`PARITY-STANDARD.md`](../../../Reconstruction/PARITY-STANDARD.md)
§3 asks for the game's **caller** *and* the game's **inputs**. This has the inputs. **The caller is
still a test driver**, and the declaration says so rather than claiming the dimension.

**"Writes no state" is proven only for the pages the function can reach.** A store to an address
never mapped would have faulted and been reported as an emulation error, so nothing silently
escaped — but that is a different statement from "the body contains no stores".

**Nothing here says the right music plays.** 35 distinct track ids were resolved from real data;
**no track id was mapped to a piece of music**, and no audio was observed.

**The table was captured at the front-end**, not in a loaded save. It was already fully populated
there. This establishes populated bytes at that capture point. The writer, binding, ownership,
rebuild and release behavior were not observed; `DG-1` is not closed by the capture.

## Related

- [`EXP-007`](EXP-007-navigating-the-front-end.md) — the capability that made a running game routine
- [the field-music contract](../18-Audio/CONTRACT-field-music-selection.md) — §15 preserves the producer gap
- [`PARITY-STATUS.md`](../_index/PARITY-STATUS.md) — the dimension table
- Raw capture: `evidence/EXP-008-mus0-table.bin` (64 KB read from `653B0FC0`)
