# Affected-consumer check: HM-1, the executable's letter-to-kind step (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (`_index/candidates/hm1-high-ids/hm1_letter_kind.py`, 5 checks):
- A model id is `letter << 16 | N`.
- The model loader `002E6700` resolves it through `002ED6F0(id, &kind, &index)`, a jump table on the letter:
  - lower-case: c 14, n 19, s 23 (stride 25); m 34 (stride 11); b 22 and g 13 (stride 2);
  - upper-case and stride-1 letters: C 15, N 20, S 24, M 18, t 25, w 16;
  - any other letter: kind 1.
- The pair then goes to `0032E400`, the `.fst` size read; kind k is the disc file list's section k (UQ-70).
- Every decoded list tiles exactly into stride-sized model blocks, so `stride x N` is the Nth `.cm`.

**Discriminator.** The earlier readings (H2, H4) were fitted to the data. The same mapping now follows from the
engine's jump table. A raw-entry reading of the lower-case ids is rejected twice: the engine multiplies by 25, and the
lists interleave `.cm` and `.ca` (K4).

**Not claimed:**
- what callers do with `002ED6F0`'s return value (stride-1, the `.ca` slots per model);
- which model the second-skeleton record holds.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` HM-1 | narrowing prepended; earlier text kept | revised-here |
| the add-motion tables page (its "Not claimed: the executable's letter-to-kind step" line) | narrowing note added in the follow-up publish, once a peer's in-flight append had landed (02cc89e7e); the line now reads "Not claimed: which model the second-skeleton record holds" | revised-here |
| `_index/candidates/hm1-high-ids/hm1_high_ids.py` (H2, H4) | kept unchanged as history; still PASS; the new control grounds the same mapping in the executable | agrees |

Run receipt: `hm1_letter_kind.py` and `hm1_high_ids.py` executed at 260521390 (FAILS 0 each).
