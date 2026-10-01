# Nav working mask: per-query reset: consumer check (OPUS, 2026-09-28)

**Corrects:** `_types/fields.tsv` NavGridParams +0x50 (workingCandidateMask) and `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` (the write-census row for `BMASK`). Both are OPUS text.

**Refuted claims:**

- The mask is "zeroed once at 0039267E rather than per query".
- `BMASK` ORs "a caller-supplied record mask".

**Replacement:**

- `BMASK 003912E0` clears the mask behind the global pointer cell `[02AEE0B0]` at every entry. It memsets `[02AEE0B8]` bytes through `00861EC0` (VCRUNTIME140 memset) before any branch, loop or other call.
- It then ORs into the same mask through that cell and returns the pointer.
- There is no destination argument.
- The builder's allocation memset `0039267E` also clears it.

This answers ASTRA-REQ-OPUS-NAV-MASK-RESET, whose evidence is in `_experiments/evidence/nav-mask-query-reset-boundary/`. OPUS re-derived the bytes without ASTRA's code.

## Consumers (OPUS, 2026-09-28)

| consumer | state |
|---|---|
| consumer `_types/fields.tsv` NavGridParams +0x50 meaning | revised-here (struck and replaced; valid storage, the length and a conforming CRT memset are stated as preconditions) |
| consumer `CONTRACT-corridor-query-family.md`: the write-census row for `BMASK` | revised-here |
| consumer NavGridParams +0x58 cellBitsetBytes (the clear's length) | agrees (0x24, set by the builder; its role as the clear length is consistent) |
| consumer the query semantics and source producers of the mask (FABLE's lane, per the request) | routed-to-ASTRA-REQ-OPUS-NAV-MASK-RESET (the request names FABLE for semantics; OPUS changed only type and contract text) |

A search of the database's `.md` and `.tsv` files (outside `_experiments` and `_inbox`) for "rather than per query", "zeroed once at 0039267E" and "caller-supplied record mask" finds only the two consumers above.

**Regression:** `_index/candidates/nav-mask-reset-opus/nav_mask_reset.py`.

- E: the entry clear precedes every branch and call.
- O: the OR and the return go through the global cell, with no destination argument.
- M: two mutants are rejected, the clear register retargeted to rdx and the memset call NOPed.
- S: fails while either refuted phrase is live.

It was verified at 1d8a0fd1b plus this publish's working tree (`nav_mask_reset.out`).
