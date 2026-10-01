---
experiment: EXP-032
title: Raw command-context snapshot preparation
status: PREPARED — synthetic byte controls pass; no runtime observation
contract: none - bounded preparation of an importable read helper; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-11
method: A - offline instrument preparation
live_game: false
---

# EXP-032 — distinguish current and retained command bytes

EXP-027's two combat waits produced no damage and did not capture current command
state. FABLE returned the relevant offsets in ASTRA-REQ-FABLE-COMMAND-ANCHOR. This
bounded preparation provides an importable read helper for the next experiment;
it makes no claim about what happened during EXP-027.

[command_snapshot.py](evidence/EXP-032-command-snapshot/command_snapshot.py) accepts
the existing Reader interface plus a freshly selected unit, slot and actor. It
reads phase bytes+0x6B4..+0x6B6 and one48-byte block+0x700..+0x72F. The two24-byte
halves preserve current and shadow raw bytes separately. Each decodes flags u32,
context pointer u64, target focus handle u32 and action ID u16 at relative offsets
0,8,16,20. The sentinel flag reports only whether a context is0 or all-one u64.
It never labels a snapshot cancelled, in range, executing or dead.

The helper brackets reads with frame0208D45C and the unit's24-byte header and slot
byte+0xEA9. A short/unreadable buffer, inactive or mismatched identity, or changed
header aborts the snapshot. Frame crossing is retained explicitly. An unchanged
header is a consistency guard, not a proof against reuse with the same values, and
same-frame sequential reads are not an atomic command-state transaction.

Four synthetic controls check distinctive high-bit u64/u32/u16 values, distinct
shadow values, expected read addresses and lengths, failed reads/identity changes,
frame crossing, and sentinel contexts alongside retained shadow data. These test
byte handling only. No native API, process read, input or game write occurs in the
helper or fixtures. The [test receipt](evidence/EXP-032-command-snapshot/unit-tests.txt)
and [manifest](evidence/EXP-032-command-snapshot/manifest.json) preserve exact sources.

## Next controlled use

In a fresh qualified field census, select the player's unit and record the command
snapshot before menu input, after confirmed Attack, and after any separately bounded
movement. Pair these with fresh actor/HP observations and frame brackets. A transition
from a non-sentinel context to a cleared command can support the distinction FABLE
requested; it does not by itself identify the clearing writer or reason. A persistent
context/target with unchanged phase does not prove an out-of-range wait. Resolve the
encoded committed target through its actual resolver contract before binding it to
an enemy; do not equate it with a UI cursor or assume the actor registry handle at+8
is interchangeable. No further unexplained30-second wait is part of this preparation.

Sources: [FABLE's return](../_index/_inbox/FABLE.md),
[commit operation](../07-Combat-Action/the-moment-an-action-is-committed.md), and
[BattleUnit map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md).
The commit page's table places the shadow at+0x718, a24-byte displacement from+0x700;
its prose says eight bytes. The helper follows the table and FABLE's explicit return.
That prose discrepancy is routed to FABLE rather than silently rewriting its page.
