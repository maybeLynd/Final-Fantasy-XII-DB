# Affected-consumer check: HM-1, what highmodelreplace.bin's replacement ids name (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (`_index/candidates/hm1-high-ids/hm1_high_ids.py`, 3 checks): an upper-case id X:M is entry M of the
high-model file kind for its letter (C 15, N 20, S 24). The file kinds come from the PS2 disc file list decoded under
UQ-70 (`21dc8ff09`).

**Discriminators:**
- The lists are unsorted, yet the resolved models rise strictly in record order.
- The one double record resolves to two variants of one model.

**Not claimed:** the executable's letter-to-kind step, and the lower-case source ids.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` HM-1 | narrowing prepended; earlier text kept | revised-here |
| the character-model replacement page carrying HM-1's box | the box stays open (lower-case ids and the letter-to-kind step remain) | agrees |

Run receipt: `hm1_high_ids.py` executed at 4c0e3fc35 (FAILS 0).
