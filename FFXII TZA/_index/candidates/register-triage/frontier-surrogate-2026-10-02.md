# FRONTIER-RT-RUNTIME-SURROGATE — results, 2026-10-02 (SWE2-ORACLE)

Request `REQ-20260930-FRONTIER-RT-RUNTIME-SURROGATE` (TEAM rev ~43802,
P1): ASTRA's live window is closed; attempt replay-surrogate evidence
on 7 register rows — BG-6, BJ-1, BL-8, UC-2, UQ-332, GG-1, BQ-27 —
leaving each OPEN where the surrogate cannot answer.

## Per-row outcome

| row | prior state | surrogate result | row state after |
|---|---|---|---|
| BG-6 | ANSWERED (static, `bg56-gi-bodies`, FAILS 0) | executed confirmation: `006CA760` replayed over idx ∈ {0,1,3}; nonzero index honored (`imul ×0x7FE0`), index consumed-then-cleared, pointer republished at `+0xB8` — "always `dev+0x10880`" is a population fact, not a function constant. `../bg6-slot0-replay/` md5 `3198c99ce0ca05d8e3cf29e95c912511` | ANSWERED (unchanged, replay evidence attached) |
| BJ-1 | ANSWERED w/ residue carrier | OPUS's own NATIVE-REPLAY lower bound already stands (19/1681 guards, md5 `f60666a1`); residue is live by definition — carried by `OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT`. No additional surrogate run justified. | ANSWERED, residue carried |
| BL-8 | PARTIAL | surrogate cannot answer: the question is the *population* of `+0x60`/`+0xB0` descriptor-list heads across 410 statics + heap descriptors under loaded battle state. A Unicorn fixture can only replay the walk primitives already read statically — it cannot fabricate honest heap occupancy. Stays PARTIAL; live carrier remains the ASTRA queue row. | PARTIAL, surrogate-inability recorded |
| UC-2 | ANSWERED (static census: relocs/RIP-rel/branches/pdata exhausted; 63 retained blocks have no entry) | none needed — the defined question is already closed by static evidence | ANSWERED |
| UQ-332 | ANSWERED (`uq332-no-reader`, FAILS 0) | none needed | ANSWERED |
| GG-1 | OPEN | surrogate cannot answer the row's question (per-press frame ordering of 51 indirect-dispatch readers vs the arbiter's consuming store). A fixture could replay *one* reader's ordering but proves nothing about the other 50, and ordering across the frame boundary is temporal — not replayable without the real dispatch order. Stays OPEN; static alternative remains the named STATIC-LARGE indirect-dispatch pass. | OPEN, surrogate-inability recorded |
| BQ-27 | PARTIAL (567/607, 40-site residue) | pass O (`../bq27-opaque-defs/`, FAILS 0): 3 new literal settles (`00624367`=0 path-cond, `00691B06`=1, `007DDA3A`=1) → **570/607**. Remaining 37 classified: 25 forward own arg2 (caller-population residue), 3 cmov-min counts, 3 `+0x1894` counter-field sites (1 writer, caller-seeded `d[arg4]-1`), 1 global `02EA1924` (1 writer, conditional save), 1 `+0x60` generic field, 4 misc computed. No site provably passes flag 5; none excludable statically. | PARTIAL; live BP at `0016D6A0` (rcx≠0) over 37 sites remains the decisive instrument |

## Boundary

Surrogate replay is NATIVE-REPLAY evidence only — synthetic objects,
no initialized-game reachability. For BL-8 and GG-1 the surrogate was
evaluated and *declined* on the merits (population-enumeration and
temporal-ordering questions cannot be honestly staged); those rows keep
their live carriers rather than accumulating misleading fixture runs.
