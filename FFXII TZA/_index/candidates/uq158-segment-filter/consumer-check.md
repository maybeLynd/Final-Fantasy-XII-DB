# Affected-consumer check — UQ-158's `004023D0` clause (FABLE, Claude Opus 5.5, 2026-09-26)

FABLE's 2026-09-17 answer to UQ-158 said `00402A40` "where `004023D0` answers 1 applies `004027D0` and links the node".
The branch is the other way round. `00402B25` calls `004023D0`, and `00402B2A cmp eax, 1` / `00402B2D je 0x402bac`
jumps straight to the next record. `004023D0` returns 1 (`00402484`) when a listed node already holds the same
undirected segment: the ids at `+0x80`/`+0x82` and the endpoints at `+0x84`/`+0x86` and `+0x8C`/`+0x8E` match in either
order. So the node is built and linked only for a segment **not yet listed**.

The same read identifies the element nodes, and UQ-156 is narrowed with it: they are the location's area connections,
each drawn once.

**Regression:** `_index/candidates/uq158-segment-filter/segment_filter.py` re-reads the branch and the duplicate test from
the image and asserts both directions. As a planted known positive, a return of 1 must reach the skip target, not the
node build.

| consumer | state |
|---|---|
| `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` UQ-158 answer box | revised-here (struck, restated) |
| `_index/OPEN-QUESTIONS.md` UQ-158 row (the same clause) | revised-here |
| `00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-F-ids-172-203.md` "`004023D0` filters each" | agrees (direction-neutral) |
| same map page, 2026-09-26 arm-14 narrowing ("builds the element array `+0xBBD0` through `00402A40`") | agrees |
