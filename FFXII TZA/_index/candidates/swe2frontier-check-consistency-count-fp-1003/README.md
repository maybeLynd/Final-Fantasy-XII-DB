# check_consistency CALLER-COUNT false positives (SWE2-FRONTIER, 2026-10-03)

*Answers `FABLE-REQ-FRONTIER-CHECK-CONSISTENCY-COUNT-FP-1003`, items 1 and 2. Item 3 (`0031B760`, a scoped "19 actor
bodies") is FABLE's reword. SWE2-FRONTIER, Claude stand-in for `calm-lamp`.*

1. **Struck counts.** `003A1DB0` "(~~16 callers~~ 47 direct ...)" kept producing "16 callers". The strike sits
   inside the match, where the 240-character retraction look-behind cannot see it. Struck spans are now blanked
   (same length, so offsets hold) for the count extraction only. The look-behind still reads the original text.
2. **Bullet subject.** "**00194290** (...) `005CDAA0` call ... [`001942C0`] - 4 callers" gave the 4 to `005CDAA0`,
   because the forward pattern's 80-character gap stepped over nearer quoted addresses. When another quoted address
   sits between the matched address and the number, the count now goes to the line's leading address (bold or quoted,
   after an optional list marker), or else to the nearest quoted address. It never goes to the farther one.
3. Exposed by (2) once `00379CD0` received its own count: "whose other 53 callers" / "N more callers" is a scoped
   count. It is now keyed as its own kind (`[other]`), like direct/total, and never compared with a total.

**Result at HEAD:** CALLER-COUNT disagreements 3 -> 1. The remaining one is `0031B760`, FABLE's item 3. Addresses with
a stated caller count go 326 -> 321: struck counts are no longer claims, and reattributed counts merge.

**Control:** [`count_fp_control.py`](count_fp_control.py) builds a scratch database, one case per page because the
look-behind spans 240 characters. Repaired checker: FAILS 0, with the positive control (12 vs 13 callers) still
reported ([`count_fp_control.out`](count_fp_control.out)). Pre-repair checker: FAILS 2 (C1 and C2 reported), so the
control is sensitive to both defects.
