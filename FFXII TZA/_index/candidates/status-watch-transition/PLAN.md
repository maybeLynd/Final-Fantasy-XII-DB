# Status sparse columns: the transition and window to watch (FABLE, Claude Opus 5.5, 2026-09-27)

Answers `ASTRA-RETURN-FABLE-STATUS-WATCH-LIMITS` for the owner of
[the thirty-two statuses](../../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md). ASTRA's preflight
(`_experiments/evidence/status-watch-preflight/`) is consumed as stated:
- 42 populated bytes;
- row 3 is Stop, with three populated bytes; row 6 (Doom) has none;
- no single 8-byte watch covers the populated span;
- the existing breakpoint backend is execute-only.

This note names what to watch and when. It runs nothing.

## Why this transition

The page's column law: in each of `+0x11`, `+0x12` and `+0x14`–`+0x1D`, the *n* rows that are not `0xFF` hold exactly
the values `32 − n … 31`, each once. That is the shape of **a per-slot rank among the statuses that share a slot**.
If it is one, the reader compares two active statuses' bytes in a shared column, so a reader shows up only when **two
statuses sharing a column are active on one unit**. A single status on its own may never make anything read these
bytes.

**Float (row 26) and Immobilize (row 14) share three columns:**

| column | Float | Immobilize | Stop (row 3) |
|---|---:|---:|---:|
| `+0x14` | 31 | 28 | — |
| `+0x15` | 31 | 30 | — |
| `+0x1A` | 31 | — | — |
| `+0x1C` | 30 | 29 | 31 |

## The capture

- **State:** a normal battle, one party member as target. Cast Float on it, then Immobilize on the same unit while
  Float is still active. Float's default timer is 60 s and Immobilize's is 50 s (`+0x08`), so both stay active for the
  window.
- **Window:**
  - *Positive-control window:* from Float's status write, until 600 frames (10 s) after it.
  - *Test window:* from Immobilize's status write, until 600 frames after it.
  - *Removal window:* the 600 frames after Immobilize expires or is cured.
- **Watch:** four data read/write watches of 8 bytes, `[row + 0x10, row + 0x17]` and `[row + 0x18, row + 0x1F]` for
  rows 14 and 26. Each row starts at `table + 0x20 + 40 × row`.
  - *Precondition:* the live table base must make those starts 8-byte aligned. Check it before arming.
  - *Coverage:* this covers every populated sparse byte of both rows, and also `+0x10` and `+0x13`.
- **Classify every hit by the reading instruction, not by the watch.** Decode the instruction at the hit and compute
  the address it accesses:
  - `+0x10` and `+0x13` have known readers (the status-listing order key and the query-record copy). A hit on either
    is the **in-session positive control** that the watch detects reads. Opening the status list in the menu produces
    it.
  - A hit whose access falls in `+0x11`, `+0x12` or `+0x14`–`+0x1D` is a **positive reader on this path**. Record the
    instruction, its function, the frame and which window it fell in.
- **What a result can mean:**
  - A positive in the test window but not in the positive-control window supports the shared-slot reading.
  - No qualifying hit in all three windows is a **bounded no-read**: no reader of these bytes ran in this state, for
    these two statuses, in these windows. It says nothing about other statuses, the field (outside battle), cutscenes
    or other systems. It never makes the bytes authored-dead.

## Prerequisites (ASTRA's list, unchanged)

- a qualified read observer (the current backend cannot do this);
- fresh table and row pointer identity;
- bounded event and time budgets;
- responsiveness and fatal-dialog checks;
- detach and restore.

The S19 input stop-loss still applies to any new setup. If a read observer cannot be qualified, the capture does not
run, and the columns stay OPEN as they are.
