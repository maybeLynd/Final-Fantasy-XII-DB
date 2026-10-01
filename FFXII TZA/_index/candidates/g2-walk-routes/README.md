# G-2: the walk routes to the Sequence entry's flag and float are closed (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

G-2's residue is who reads `SabFile::Sequence`'s entry flag (`+0x28`, byte) and float (`+0x2C`).

**Already closed.** The earlier narrowing (`g2-entry-readers/`) found that no caller of the accessor family reads
either field. It left an indexed walk, and a copy, as the open routes.

**Closed here** (`g2_walk_routes.py`):
- **W1, indexed walks.** Nothing in the image reads `[base + idx*16 + 0x28 / 0x2C]`. Nothing reads those
  displacements with an index shifted by 4, or multiplied by `0x10`, just before either. The same scanner finds 17
  accesses scaled by 8, which is the positive control.
- **W2, stepped-pointer walks.** In the audio range, no pointer stepped by `0x10` reads a byte at `+8`. There are nine
  functions where a `0x10`-stepped register reads a dword at `+0xC`. All nine are dispositioned, and none walks the entry
  table:
  - three float readers: vector products, a lerp, and a record with a byte index at `+4`;
  - six integer readers: five on the `007D0400` / `007D06B0` / `007D0600` descriptors, and image arithmetic.
- **The largest raw candidate.** `007CA560`, with 58 callers, is a float ramp, not a Sequence.

**Negative, not claimed:**
- A receiver-signature filter found one function, `00844090`, a byte-array routine. That filter's positive control is
  ambiguous, because the range float and the weight byte share `+0x10`. So it supports the result but is not a check.

- **W3, block copies.** None of the record's 99 known consumers copies it or its entry as a block: the accessor family,
  every function that calls into it, and the walkers `007E5000`–`007E7000`. Their only 16-byte moves over those
  offsets are stack spills, and none calls memcpy.

**Open:**
- A copy of the record, or of its entry, by code outside those consumers. 16-byte loads at `+0x20` are common in the audio
  range's vector code, and they are not dispositioned here.

**Run receipt:** W1–W3 PASS, FAILS 0 (2026-09-27).

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` G-2 | narrowing prepended; row stays PARTIAL | revised-here |
| `18-Audio/Sound-Selection/sound-variant-selection.md` G-2 bullet | the same narrowing, placed before the earlier one | revised-here |
