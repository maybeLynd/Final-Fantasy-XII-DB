# Affected-consumer check: BI-11, what the packed-id bucket registry family holds (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (control: `_index/candidates/bi11-presentation-classes/bi11_classes.py`, 10 checks, FAILS 0):
- **Classes 5/6/9** are the presentation records. `003B02A0` is their only creator. The creator census by class
  was published at `1ff3df7cd`.
- **Class 1** is the loaded magic-effect files:
  - 48 × `0x38` records;
  - a per-id 5-bit load cost, refused above 24;
  - resource kind `0x26`/`0x0B` = `effect_finish` magic `.efx`.
- **Classes 7 and 8** keep the 2026-09-14 identification.
- **The budget.** Classes 1 and 5/6/9 share one budget of 24.

**What this corrects.** The page's own "Still open: class 1" bullet (added at `1ff3df7cd`) is struck. The page's
status line now reads "answered". No accepted knowledge from another author is replaced.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` BI-11 | OPEN → ANSWERED, prior status kept | revised-here |
| `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` | class-1 block added, residue bullet struck, status line | revised-here |
| `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md` UQ-111 | its table reading is the evidence used; no change | agrees |
| `13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md` UQ-136 | its class-5 reading is the evidence used; no change | agrees |

Corrects: 99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md
Corrects: _index/OPEN-QUESTIONS.md

Run receipt: `bi11_classes.py` executed at fcbffd545 (FAILS 0, 10 PASS lines).
