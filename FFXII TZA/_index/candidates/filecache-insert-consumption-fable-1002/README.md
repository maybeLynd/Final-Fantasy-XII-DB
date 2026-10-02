# File-cache insertion key: an accepted packet consumed into the path-resolution page (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148), on `ASTRA-REQ-FABLE-FILECACHE-INSERT-KEY-ADMISSION-1002`.* ASTRA's
packet `filecache-insert-key-admission` (producer `1b2154feb`) was reviewed independently by FABLE, which did not
author it: [REVIEW.md](../fable-review-astra-filecache-insert-key-admission-1002/REVIEW.md), ACCEPT-WITH-NARROWING.
The review has 81 checks and 15 controls, all as expected, and its own reader re-derived every claim.

[`apply.py`](apply.py) inserts [`section-5a.txt`](section-5a.txt) into
[how a path is resolved to bytes](../../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md),
before section 6. The section keeps the cache's insertion interface apart from section 5's lookup key producer. It
does not change section 5, whose bit-31 clear is the producer's and stays true.

The section 5a text keeps four of the review's eight narrowings:
- only the dword at node `+0x20` is the key, because `+0x24`..`+0x27` are stale stack bytes;
- `0020B5F0` is a find-or-insert;
- insertion is gated on the call at `0020B680` + 0xC6, and the `+0x90` add happens either way;
- the premises and the open limits.

The other narrowings stay in the review:
- the existing-key branch's second callee;
- the copy guard not being a null check;
- the stability premise being narrower than stated;
- the completeness method for the balancing leaf;
- carrier widths.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

- consumer: this page: revised-here (new section 5a; section 5 unchanged).
- consumer: [the TA texture-animation page](../../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md),
  which derives the 31-bit hash: agrees (it describes the lookup producer only).
- consumer: ASTRA's packet: agrees, narrowed as the review states.

run: `rv_insert.py` at 77356569f (81 PASS, 0 FAIL, 15 controls) - [script](../fable-review-astra-filecache-insert-key-admission-1002/rv_insert.py)
