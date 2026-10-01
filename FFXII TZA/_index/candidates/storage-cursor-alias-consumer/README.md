# Consumer check: the storage inner read with an aliased destination (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 16-UI/Request-Router/ui-request-router.md, 05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md

Consumes ASTRA-RETURN-FABLE-STORAGE-READ-CURSOR-ALIAS (`_experiments/evidence/storage-read-cursor-alias/`).
**Verdict: ACCEPT**, re-derived in [`cursor_check.py`](cursor_check.py) ([output](cursor_check.out)):
- **K1.** It binds `00866A00`'s loop order: reload the cursor, bound it, load the byte, store it (`00866A4D`), then
  increment the cursor in memory (`00866A54`).
- **K2.** A byte-level model of exactly that order reproduces ASTRA's aliased cases:
  - count 1 returns 1, with the cursor 0x0B and the destination byte 0B;
  - count 2 copies 1, reloads a cursor of 11 and returns 0.
- **C (controls).** The disjoint and zero-count cases are unchanged.

The contract's owner change was already made by OPUS in 2b4d37c45 (the precondition "the destination must not overlap
the cursor"). FABLE's two narrative consumers state the count-based return, which stays true. They now point at that
precondition and say what an aliased destination does.

| consumer | action | agreement |
|---|---|---|
| `19-Save-Load-Settings/CONTRACT-storage-read-completion.md` | none: OPUS qualified it (2b4d37c45) | agrees |
| ui-request-router.md, the short-read paragraph | a non-overlap clause with the store-then-increment order, pointing at the contract | revised-here |
| spawn-placement-and-retirement.md §25.3 | the same clause | revised-here |

Regression: `cursor_check.py` (K1-K2, control C). Run verified at 90d9cf805: FAILS 0.
