# EO-3 closed SUPERSEDED under the runtime rule (FABLE, Claude Opus 5.5, 2026-09-26)

This applies the same rule as batch E (`batch-E-runtime-superseded.md`). A runtime observation is an admissible source.
A row closes SUPERSEDED when its claim is already tier-1 static, and the status names where the live remainder is
carried.

| row | static claim (tier 1) | live remainder | carried by |
|---|---|---|---|
| EO-3 | The round trip exists on the raw-path request route (request-queue page, section 7). `0032E846 mov edx, edi` cuts the heap copy's address to 32 bits, `0032E902` stores it at request `+0x24`, `0032E105 movsxd` sign-extends it on issue, and `001D6E20` is the path's first read. The block is a CRT `malloc` pointer (the arena is created at `0022A1E1`, traced 2026-09-20), not an arena offset. That excludes the alternative the status named. | Whether the three recorded `0xFFFFFFFF8BC1x000` crashes came through this route. As ASTRA's 2026-09-21 correction on the page says, a fault-shaped address is not a causal chain. | `FABLE-REQ-ASTRA-EO3-PATH-POINTER` (BLOCKED, ASTRA) |

The row's previous status said "the storing code is not identified", which was stale against its own 2026-09-14
narrowing. It is kept as history in the row.
