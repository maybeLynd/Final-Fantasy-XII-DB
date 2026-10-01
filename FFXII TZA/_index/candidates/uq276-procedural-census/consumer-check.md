# Affected-consumer check: UQ-276 census; the "paired seed" label at 022D92E0 superseded (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `21-RNG-And-Determinism/members/procedural_stream_census.py` (5 checks, FAILS 0).
- P1 through P4 establish the census: 114 consumer functions (10 accessors of the state `01EF93E8` and 104 callers).
- P5 establishes the label correction: 113 functions store or load a whole `xmm` register at `022D92E0`.

| consumer | what it said | state |
|---|---|---|
| `21-RNG-And-Determinism/rng-streams.md`, section 4 data-structures block | `022D92E0 u32 paired seed value` | revised-here (marked SUPERSEDED in place; the corrected note is in the new census subsection) |
| same page, section 3 table (two helpers and the seeder) | presented as the stream's functions | revised-here (the census subsection says it is three of ten accessors) |
| same page, the section 7 `UQ-276` box | open | revised-here (ticked) |
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-shared-transform-workbench.md` | `022D92E0` is the workbench's slot A, a scratch row with about 250 writers | agrees (this correction adopts its reading) |
| `_index/OPEN-QUESTIONS.md` UQ-276 | OPEN | revised-here (ANSWERED; the previous status kept as history) |

A search for `022D92E0` over every `.md` finds no other page that calls it a seed.
