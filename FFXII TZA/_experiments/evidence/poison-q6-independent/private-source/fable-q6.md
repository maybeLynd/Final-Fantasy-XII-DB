# PKG-GP-STATUS-POISON Q6: the Poison arm executed, and one correction it forced (FABLE, Claude Opus 5.5, 2026-09-29)

**The replay (OPUS, ced7c61fd; FABLE-REQ-OPUS-POISON-ARM-REPLAY).**
- `_index/candidates/s27-opus-replay-periodic-builder/poison.py` drives the periodic builder over block 310's harness. It
  imports the harness unchanged, and the harness's own six cases still pass.
- Result: 14/14 cases, identical over two runs. Evidence class NATIVE-REPLAY, no live game.
- **All seven of FABLE's expected values hold:**
  - Poison at max HP 1,000: −62, flag A `|= 0x140`, flag C `|= 0x4000`;
  - under Bubble: −125;
  - under Disease at HP 40: −2;
  - at max HP 15: −1;
  - Sap: nothing at HP 1, −1 at HP 2;
  - a word-1 duration reaching 0 sets its remove-mask bit;
  - Stop skips Poison.

**The correction.** The status-write page's stage-2 table said the HP-Critical check runs "when the record carries an HP
write (flag A bit 8)". OPUS's cases disagree:
- no status, at HP 100, applies HP Critical;
- HP Critical alone, at HP 500, removes it;
- Sap with no HP write, at HP 1, applies it.

FABLE re-read `00386F78`–`00386F95`:
- flag A bit 8 only chooses the compared value (the new HP with an HP write, absolute when bit 3; otherwise the current HP);
- the line test and the add or remove run on every call.

The row is corrected, and the old words are struck.

affected: `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md` (the stage-2 table's "after the
loop" row)

consumer: the tick page ("HP Critical is maintained against max HP / 5") states no gate. It agrees.

run: OPUS's poison.py at ced7c61fd, 14/14. FABLE's re-read of the bytes agrees.
