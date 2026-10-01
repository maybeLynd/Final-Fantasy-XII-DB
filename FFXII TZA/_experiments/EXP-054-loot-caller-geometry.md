---
experiment: EXP-054
title: loot caller eligibility and grant/removal dispatch
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies this periodic loot eligibility and grant/removal dispatch segment; actual grant and removal are omitted.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original caller segment with injected frame and unit plus original focus predicate/getter; overlap/preparation controlled, grant/removal omitted.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-054-loot-caller-geometry/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-054: loot caller eligibility and grant/removal dispatch

**Result:** nine original-segment controls passed; reversing the stats-kind branch
was detected. ASTRA, 2026-09-11. The caller's local dispatch is established. A
universal class-3 guarantee is **not established**: native producers and earlier
callees remain outside this experiment. No game process was accessed.

## Question and original context

[EXP-053](EXP-053-loot-overlap-controls.md) demonstrated that the overlap reader's
radius outputs are initialized only for class-3 actors. Does its caller enforce
that class, and what happens to a selected pickup?

[check.py](evidence/EXP-054-loot-caller-geometry/check.py) verifies the certified
EXE hash and scans the image's `.text` raw bytes for relative E8 calls to
`002FB150`. It finds one candidate, `00311105`, and validates it as a decoded
instruction in the retained caller. This is a bounded direct-call census, not a
proof that no indirect caller exists or that this path executes in live play.

The caller begins at `00310DB0` and ends at RET `003112E9` (1,338 bytes). Its
exception-table records split that body into several ranges; the range containing
the overlap call starts at `00310F55`, which is **not** a fresh function entry.
The full caller is retained for context, alongside `003273B0` (28 bytes), its
getter `003590D0` (7), and earlier global guard `00265680` (149).

Only the caller segment beginning `003110DC`, the focus predicate and its getter
are executed here. RSI is explicitly supplied with a synthetic unit pointer;
RSP is supplied as an already-established local frame. Earlier periodic work,
global/terminal guards and native result application are omitted. This is not a
full caller execution or an ABI test of its entry/exit.

## Local decision sequence

1. Read the unit's cached handle at `+0x08`; compare it through original
   `003273B0`/`003590D0` with current-focus dword `022C7FE0`.
2. If it is not current focus, require unit action word `+0x714 == 4165h`.
3. Call overlap search `002FB150(unit, 1.0f)`. The extra radius comes from
   original image constant `01CEBBA8`, not a fixture-selected value.
4. A signed-negative overlap result skips collection processing.
5. A nonnegative result is retained in EBX. Pass the current stats pointer at
   unit `+0x698` to native `00469E30`.
6. **Reread** the stats pointer after that call. A null pointer, or a nonzero byte
   at stats `+0x05`, selects `00319830` (remove without grant). Otherwise select
   `00319A00` (collect/grant by index).
7. Both dispatches receive ECX = selected index and EDX = unit's cached handle.

The names of the dispatch functions are documented on the
[loot page](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md).
This experiment stops **before** executing either function. It proves which
boundary is selected and its arguments, not inventory changes or pickup removal.

## Controls and interventions

The overlap return and `00469E30` are explicit controlled dependencies. The latter
can change the stats pointer or byte as an intervention; that does not claim the
native callee actually makes those changes. It also clobbers RAX, ensuring that
the caller's subsequent memory read supplies the pointer.

| Case | Observed boundary |
|---|---|
| Not focus, no special action | skip; no overlap call |
| Focus, no overlap | skip |
| Not focus, action 4165h, hit 3, stats byte zero | grant index 3 |
| Not focus, adjacent action 4164h | skip |
| Focus, hit 9, stats byte zero | grant index 9 |
| Focus, hit 2, stats byte nonzero | remove index 2 |
| Preparation clears stats pointer | remove index 2 after reread |
| Preparation changes stats byte to 1 | remove index 2 after reread |
| Overlap returns signed minimum | skip |

All cases assert exact focus/overlap/preparation call identities, order and
arguments, the selected dispatch boundary/arguments, expected stack depth,
full unit/stats/focus pages including explicit interventions, and no original
non-stack writes. Raw [results](evidence/EXP-054-loot-caller-geometry/result.json)
retain the complete segment trace. Source and original bodies are sealed in the
[manifest](evidence/EXP-054-loot-caller-geometry/manifest.json); the
[disassembly](evidence/EXP-054-loot-caller-geometry/disassembly.txt) includes the
unexecuted caller context and global guard.

A private mutation reverses `JNE` to `JE` at `00311136`, making the zero-byte
fixture select removal instead of grant. The test detects the wrong boundary.
Original bytes remain unchanged. The complete run passed on first execution.

## Class guarantee remains an upstream question

The executed segment does not inspect the actor pointer or its class. The focus
predicate only compares handles. The earlier `00265680` guard reads global
manager state and calls `002E0540`/`00265720`; it is not an immediate test of the
unit's actor class. Other earlier native calls, unit construction and allowable
action/focus states may enforce the necessary input contract.

Therefore these controls do not promote the class-1 scratch dependence from
EXP-053 into a reachable game bug. The exact remaining question is whether a unit
that reaches this caller with focus or action 4165h can have a non-class-3 actor,
after the earlier native guards. Return this boundary to FABLE/OPUS alongside the
positive eligibility and dispatch evidence. No live class reachability, grant
effects, removal effects or whole-periodic-tick parity is claimed.
