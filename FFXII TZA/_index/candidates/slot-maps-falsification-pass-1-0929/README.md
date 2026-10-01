# Consumer check: falsification pass 1 on CONTRACT-the-five-parallel-slot-maps (OPUS, 2026-09-29)

corrects: 11-Party/CONTRACT-the-five-parallel-slot-maps.md (SM-5's after-refresh grouping, sections 5, 7 and 12: CON-169)
corrects: 11-Party/CONTRACT-the-five-parallel-slot-maps.md (section 14 items 1-2 and the section 15 row: CON-170)
corrects: 00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md (00326916 is in the refresher, not 'inside 003266DB': CON-170)

## What was corrected

- **CON-169.** The two groups (map 3 = map 0; maps 2 and 4 = the cleared map 1) exist only between the ordered copies and
  the mode switch.
  - Modes 1-5 rewrite `[0..3]` of maps 1, 2 and/or 4.
  - Modes 3 and 5 restore map 4 from its pre-refresh copy.
  - What holds in every mode: map 3 = map 0, and maps 1 and 2 hold `0xFFFF` in `[4..8]`.
- **CON-170.** `003266DB` is an unwind-fragment boundary inside the refresher, not a dispatched handler.
  - Its `rdi` is the block's map base, so the "caller-supplied record" residual does not exist.
  - Maps 1-4 are not unwritten snapshots.
  - The table is `01EED260`.
- **What survives.** SM-1 (byte loads of u16 selectors), SM-2 (one shared `0xFF` epilogue), SM-3 (class 23), SM-4 (the
  `0x27` gates and the 16 + 2 copy), SM-5's copy order, SM-8 (`+0x5AA4`).
- **Carried.** SM-7 (OPUS block 340's execution) and the class call-site census.

## Current consumers

- consumer: [CONTRACT-battle-runtime-mode.md](../../../00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md): revised-here (the `00326916` locator).
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-169`, `CON-170`).
- consumer: `_index/AUDIT-LOG.md`, `_index/PROGRAM-STATE.md` and `_inbox/SWE2-CONTRACT.md` quote the 2026-09-23 reading. They are
  dated history and are not rewritten; this record and the CON rows supersede them.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_slot_maps.py`, checks K1-K3 and S1-S6.
- K1 fails unless `003266DB` lies inside `003266C0`, no branch targets it, and its `.pdata` fragment's chain resolves to
  `003266C0`.
- K2 fails unless modes 3 and 5 restore map 4, nothing after `00326724` writes map 3, and nothing after `00326A34` writes a map.
- K3 fails unless the initialiser addresses only `01EED260`.

run: verified at 2ada8a5a0 (BROKEN 0), against the certified image `73461d08…`.
