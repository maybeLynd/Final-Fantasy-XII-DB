# SWE2-AUDIT-SPEC review of SD-41 (sd41-stamp-digits-0930 at fc23093ce): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: OPUS.
Reviewed: `fc23093ce`, [the record](../sd41-stamp-digits-0930/README.md) and `sd41_stamp_digits.py`. Static, the
certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD41-0930 | [sd41-stamp-digits-0930](../sd41-stamp-digits-0930/README.md) | `fc23093ce` | ACCEPT |

**Re-run.** `sd41_stamp_digits.py` at HEAD: F1-F3 PASS, `FAILS 0`; the output is identical to the committed
`sd41_stamp_digits.out` ignoring CR ([rerun_sd41_stamp_digits.out](rerun_sd41_stamp_digits.out)).

**Re-derived independently** ([sd41_review.py](sd41_review.py), [sd41_review.out](sd41_review.out)):

- **Order compares near the value (R1).** F1 searches only the exact four bytes, so a range or order test such as
  `cmp eax, stamp-1` / `ja` would escape it. I decoded every dword in `.text` within 0x10000 of either stamp as an
  instruction immediate or displacement: 21 decodes. Four are the known sites (`002EF2A0`, `00235E90`, `002370DF`,
  `00233C4D`). The other 17 are unrelated constants (`mov edi, 0x2005ff81`, `mov edx, 0x20058b01`, ...) or misaligned
  decodes (`add byte ptr [rbx + 0x507c7ce], cl`). None compares or masks a stamp.
- **The one test is an equality (R2).** `00233C4D cmp dword ptr [rax], 0x5071901` is followed by `00233C53 je`. So it
  is an equality test, not an order test.
- **The getters feed only the header (R3).** Each getter has one raw call site, both in
  `SaveRuntime_InitializeHeaderAndImageBackedState` `00253A80`: `00253AAC` stores its result at header `+0x58`, and
  `00253ACA` at `+0x60`. No caller splits or formats the returned value.

So the image stores both values, returns them, and tests one of them for equality, and does nothing else with them.
The OUT OF EVIDENCE BOUNDARY disposition is supported.

**Controls.**
- F1 is sensitive to a stray use because it counts exact file occurrences; a fifth site would fail it.
- F2 reads `op_str` over catalogued functions only. A use in unlisted code would escape F2, but not F1 (a raw byte
  search), so the pair is sound.
- F3's string patterns are narrow (ANSI date spellings and one UTF-16 form). They support "no digit string" and
  cannot prove "no date meaning". The record claims no more than that.
- R1's positive control is the four known sites, all found.

**Limit kept.** As the record says, the shipped data archives are not searched.
