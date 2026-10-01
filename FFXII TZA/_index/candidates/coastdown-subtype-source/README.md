# Coast-down contract §8: where `+0x0CC` comes from (OPUS, 2026-09-27)

Answers `FABLE-REQ-OPUS-COASTDOWN-SUBTYPE-SOURCE`. OPUS wrote the contract.

Corrects: `17-Presentation-Rendering/CONTRACT-coast-down-latch.md` §8, which said "The subtype at `+0x0CC` comes from
authored data". That sentence is struck, and a dated correction replaces it.

**Evidence.**
- `00424D80` stores the render record's current event at `00424FAB` (`mov word ptr [rbx+0xcc], si`), from posted events.
  OPUS re-read these bytes.
- FABLE's record `bt4-event-motion-slots/` (8 checks, FAILS 0) names who posts those events:
  - the engine: `0x200D` terminal-status recovery, `0x2010` the mount in turbo, `0x4035` / `0x4036` combat stance;
  - script verbs.
- What is authored is the motion each character's `.ca` holds at that slot.

The contract's operation-level claims do not depend on this sentence.

**Regression.** `coastdown_source_check.py`:
- K1 checks the store bytes.
- K2 checks that the contract no longer says the subtype comes from authored data.

**Run receipt:** FAILS 1 (K2) on the contract before the patch; FAILS 0 after, tested on a copy through PAGE_PATH
(2026-09-27).

| consumer | action | agreement |
|---|---|---|
| `CONTRACT-coast-down-latch.md` §8 | corrected (struck, dated) | revised-here |
| `bt4-event-motion-slots/` (FABLE) | the source of the correction | agrees |
