---
experiment: EXP-019
title: Group membership and completion across an observed kill
status: PARTIAL — pre-kill membership observed; completion transition untested
contract: ../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md
tool: read-only pool and ledger observer
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-10
---

# EXP-019 — establish a registered group before testing its completion

FABLE-REQ-ASTRA-LEDGER asks for memberMask before a kill, then deadMask, the
completion flag and field-table slot3 across the last death. The current
[contract](../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md)
predicts script registration before death, with immediate mode1 completion or a
deferred reaction path whose runtime reachability is not established.

Use the known save recipe and a verified backup/reference session. First qualify
the state by reading the active32-slot pool: group/mode, kind, actor bkei and lane
mapping, current HP and spawn death-count/stamp. Read all64 ledger entries, gates,
frame counter and slot3. No debugger or memory writes. Capture full code identity,
source hashes and module list, require the known read constant and active self-slot
index controls, and reject incomplete reads. An all-zero ledger with no grouped
unit is a state-selection result, not failed registration or completion evidence.

For a qualified group, record pre-kill membership and dead mask, perform ordinary
in-game combat while observing, and identify the final death by visible outcome,
HP/death-count transitions and actor identity. Predict its resolved slot bit in
deadMask; mode1 should raise the flag and post the group when gates permit. Preserve
retirement/reuse separately from death. Do not interpret every combatant as a group.

The observer keeps changed raw states and every sampling interval/frame bracket.
Reads are not atomic; a bracket crossing a frame is labeled by its endpoints.
Sampling can miss a flag consumed inside one frame. A persistent slot3 transition
can be observed but does not by itself establish the exact flag writer or same-frame
ordering. If a requested transient is missed, report that missing evidence instead
of promoting a complete per-frame proof. Capture controls before/after actions,
close the owned session, restore changed save/config files and release runtime.

## Observed pre-kill state and failed approach

Fresh reference PID 12200 loaded the Stepping save, Vaan level 1, HP 103/103.
[Named-save proof](evidence/EXP-019-ledger/stepping-save.jpg) and
[field proof](evidence/EXP-019-ledger/stepping-field.jpg) accompany the
[qualification reads](evidence/EXP-019-ledger/stepping-qualified.json).
Active pool slot 4 had kind 1, HP 134, group 1, mode 1 and resolved member slot 0.
The pool slot number is not the member bit index. Group 1 had member mask 1,
dead mask 0, flags 0, and field-table slot 3 was 0 before any attack or kill.
This establishes registration before a kill in this loaded state. It does not
observe the registration writer or the instant of zone initialization.

The first 180-second file retains its original name
[combat-window-1.json](evidence/EXP-019-ledger/combat-window-1.json), but contains
approach/menu observations without combat. The first target menu had no available
targets; a later nearby selectable target was Cactite A. No attack was confirmed.
The group-1 actor's visible name was never established; do not label it Rogue Tomato
from its HP or the save's likely story context.

The approach used bounded ordinary WASD inputs, with OS delivery, held-byte,
focus and release receipts. Camera-relative turning and terrain produced circling;
read-only actor positions were added to distinguish actual displacement. The
position reader follows actor +0xB8 only for classes 1/3, then reads three floats,
using the established Actor_GetWorldPosition layout. Position snapshots assist
navigation only; they are not a registration or completion trace. A center-screen
mouse click opened the command menu, subsequently closed with C. Right-arrow input
did not visibly rotate the camera. Preserve these unsuccessful steps.

A nearby wolf engaged Vaan before the group actor was reached. The second bounded
[observation](evidence/EXP-019-ledger/combat-window-2.json) began during that encounter.
Vaan fell while the approach remained unresolved; the
[KO screenshot](evidence/EXP-019-ledger/approach-failed-ko.jpg) records the failure.
No enemy kill was established. Therefore this experiment provides **no test of the
last-kill completion flag or the next-field-frame slot-3 post**. An unchanged ledger
in these windows cannot refute either prediction. The whole contract must not be
promoted to RUNTIME VALIDATED on this partial result.

The second window records player HP 64 down to 0, then active pool clearing and
ledger clearing, while the last sampled group actor still had HP 134. Its frame
counter eventually resets to 0. These post-KO teardown observations must not be
treated as the group's final enemy death, completion or normal respawn. Slot 3 was
0 throughout all three windows. The speed-scale read was 2.0 throughout.

The qualification has 60 samples over 2.969 seconds, including 5 cross-frame reads.
Window 1 has 17,388 samples over 179.997 seconds, maximum start-to-start gap
29.836 ms and 480 cross-frame reads. Window 2 has 17,412 samples over 179.998 seconds,
maximum gap 23.040 ms and 82 cross-frame reads. Such sampling cannot guarantee
capture of a flag consumed within one field frame. Window 2 is not a monotonic
single-field-frame sequence across teardown.

Raw reads and sources are in the experiment's evidence directory; the offline
[summary](evidence/EXP-019-ledger/normalized-observations.json) separates the three
windows, sampling gaps, frame brackets, masks, HP ranges and gates. Observer status
OBSERVED means the read loop completed, not that the scientific prediction passed.
The synthetic decoder control covers offsets, unsigned high bits and short-input
rejection only. No debugger or game-memory writes were used. The input probe opens
a read/write-capable process handle but its action here is OS SendInput.

All three observation receipts verify executable SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base 0x120000, the known read constant, and the active pool self-index controls.
The 7,996,981 compared .text bytes match the file; SHA-256 is
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
The watched-module verdict is clean; full module lists retain the overlay context.

[Cleanup](evidence/EXP-019-ledger/close-receipt.json) closed only asserted PID 12200.
[Restoration](evidence/EXP-019-ledger/save-restored.json) verifies all 26 original
save/config hashes and no extra files. Only the expected GameSetting.ini LUIDLow
change needed restoration. Runtime reservation is released.

Resume completion only with a bounded route/combat recipe that reaches the grouped
actor and establishes a final enemy death. Check the existing keymap and camera
controls before another long approach; do not repeat these circling inputs blindly.
