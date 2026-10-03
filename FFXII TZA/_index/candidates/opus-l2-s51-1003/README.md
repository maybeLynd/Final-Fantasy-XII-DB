# S-51: BattleUnit +0x080 claimed as the unit seen by the corridor query (OPUS, 2026-10-03)

*One sentence in one row, applied by [`apply_s51.py`](apply_s51.py). This is part of AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003
item (a), "propagate S-51 BattleUnit +0x080 (EVIDENCE-POLICY 4a)".*

## Applied (OPUS)

The row said "NOT CLAIMED: what the object is". `CONTRACT-corridor-query-family.md` (OPUS blocks 249/250) had already
resolved it: the corridor agent's `+0x108` sub-record is BattleUnit seen from `+0x80`. OPUS re-read the chain:
- `00308673 lea rcx,[rbx+0x80]` -> `0030867A call 0033A240`;
- `00317E9D lea rcx,[rax+0x80]` -> `00317EA4 call 0033C9B0`, which passes it as `rdx` at `0033C9C9`;
- each wrapper reaches `00336710`, which stores it at agent+0x108 (`003367B4`).

Nine of ten call sites pass unit+0x80. The tenth passes an edited 0x610-byte copy of this region (`00301830`). So
agent+0x108's `+0x10C`/`+0x110`/`+0x174` are this type's `+0x18C`, `+0x190` and `+0x1F4`.

The row keeps its measured extent, evidence and readiness. The members on this base are not separately claimed.
