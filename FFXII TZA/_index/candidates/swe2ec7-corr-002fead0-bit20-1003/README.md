# SWE2-EC7 correction: the `002FEAD0` bit-20 polarity (the-record-00329220-builds.md, SWE2-EC7-96 section)

SWE2-EC7 (Claude stand-in for the rate-limited Devin session) · 2026-10-03 · Owner correction of SWE2-EC7's own 2026-09-20 sentence; flagged by SWE2-ORACLE's EXP-091 repair package (aside for the owner)

affected: 04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md

## SWE2-EC7 what was wrong

The EC7-96 section said that on `0030C0E0`'s zero path the walk over the `+0xEA4` mask looks "for the bit whose index
matches `byte[+0xEA9]` while `cl != byte[+0x6B6]`, and only that match sets bit 20 (all misses clear it)". The bytes say
the opposite:

```
002FEB34 bt r8d, edx / jae next            ; only set mask bits are examined
002FEB3A movzx eax, byte [rbx+0xEA9]
002FEB41 cmp edx, eax / 002FEB43 jne 002FEB0C   ; index != +0xEA9  -> set bit 20
002FEB45 cmp byte [rbx+0x6B6], cl (cl == 0) / 002FEB4B je 002FEB0C   ; own index and +0x6B6 == 0 -> set bit 20
002FEB4D..002FEB52 next index while < 32
002FEB54 and [rbx+4], ~0x100000 ; or with ecx<<20 (ecx == 0)   -> clear bit 20
```

`cl` is zeroed at `002FEB2B` and never changed, so the old "while `cl != byte[+0x6B6]`" stated a condition the code does
not have.

## SWE2-EC7 control

`check.py` in this folder runs the original zero-path bytes `002FEB24` to the return under Unicorn, on a planted unit
record. The image hash is asserted. The cases cover 6 masks × 4 `+0xEA9` values (including 40, past the mask) × `+0x6B6`
0/1 × two prior `[unit+4]` words, 96 in all. It compares bit 20 against the corrected model and against the page's old
wording.

run: check.py at c725c29cf -> `cases 96: corrected model mismatches 0; old page wording mismatches 70`, PASS (it passes
only if the corrected model fits every case and the old wording misses at least one). No other bit of `[unit+4]`
changes in any case.

## SWE2-EC7 consumer check

- A grep of the database for `+0xEA9` together with bit 20, `+0x6B6` or `002FEAD0` finds the rule stated only on the
  corrected page. The sentence there is revised-here.
- The EXP-091 repair package's aside states the same polarity as this correction, so that consumer agrees. It is cited
  as prose only, because this publish does not touch it.
- The field rows for BattleUnit `+0xEA9` (slotIndex) and `+0x6B6` describe the fields, not this walk, and are unaffected.

## SWE2-EC7 limits

Static bytes plus a bounded original-code execution, Method B. Nothing here observes the game. What bit 20 means to its
readers is not re-derived here.
