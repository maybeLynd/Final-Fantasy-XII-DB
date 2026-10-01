---
experiment: EXP-024
title: Bounded group approach after camera input correction
status: PARTIAL — approach progressed; group actor not reached
date_designed: 2026-09-10
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - navigation method, and it did not arrive. PARTIAL: the approach progressed and the registered group actor was never reached, so CONTRACT-group-completion-and-respawn gained no observation. Naming it here would credit the contract with evidence this record explicitly says it does not have.
---

# EXP-024 — reach the registered actor without repeating the blind approach

EXP-023 establishes a usable horizontal-camera input packet. EXP-019 already proves
group 1 has member 1/dead 0 before the first kill in the Stepping save, but its
approach ended in player KO. The new question is whether controlled camera heading
and short movement pulses can reach and visibly identify that group actor, then
observe its final death. Do not infer its name from the save/story or HP.

The seven historical position snapshots have player-to-group-actor Euclidean
distances 65.14, 53.59, 64.22, 63.05, 74.55, 50.24 and 40.44 coordinate units.
These are geometric distances between independently moving sampled actors, not
walkable route lengths. They confirm that some old movement increased the gap;
they do not define a fresh-start route or prove terrain connectivity.

Use a fresh verified reference and complete save/config backup. Load the observed
Stepping save through the existing bounded input receipt. Qualify code/module
identity, player HP, actor pointer/self-slot/group/mode and ledger again. Read fresh
positions; never reuse historical pointers or assume the target remains in slot 4.

Begin with the validated horizontal-camera packet and inspect the field. Keep each
ordinary movement hold short (at most 1 second), then inspect current position,
health and visible terrain. A decreasing geometric gap is progress evidence, not
proof of traversability. Stop the approach after 60 seconds of input-driven field
work, after two consecutive non-progressing steps, or if an unrelated encounter
reduces player HP below 70, whichever comes first. These are experiment stop rules,
not claims about safe combat thresholds in the game.

If the grouped actor becomes selectable, preserve its visible name and connect the
selection to the live actor with read evidence before promoting identity. Run the
existing ledger observer only across the bounded intended combat interval, retaining
sampling/frame brackets, the resolved member bit, HP/death stamp and slot3. Permit
one short ordinary combat attempt (at most 30 seconds); preserve a failure instead
of expanding into blind movement or repeated combat. Distinguish KO/teardown from
the enemy's death. A read observer may miss a same-frame completion flag; an unchanged
sample is not a negative proof.

No debugger, process-memory writes, keymap edits or autonomous gameplay learner.
Close only the owned process, restore the verified save/config census and release
runtime. A failed route becomes a precise state-establishment blocker; a successful
death observation still supports only the transitions actually captured.

The original checkpoint was design only. The result and the prospective amendment
below preserve how the run differed from that first plan.

## Prospective amendment after the first approach window

The first window stopped after two one-second W pulses and a 0.25-second Right
camera pulse. The elapsed-time check was 72.20 seconds after the first pulse command
started; no further approach input was sent after that check. Inter-call agent,
approval and observation overhead dominated the 2.25 seconds of intended held input.
Player HP remained 103 and no attack was attempted. Preserve all three receipts;
this was not a successful route or a 60-second continuous movement run.

Before resuming, define one second bounded attempt from the current still-living
state, with fresh position/HP qualification. One preset camera Left pulse of 0.125
seconds adjusts the inspected heading. Then at most eight one-second W pulses may
run as a predefined sequence in a single command, with fresh position/group/HP reads
and complete release between every pulse. Stop the sequence after two non-decreasing
distance steps, HP below 70, disappearance of the tracked actor, or 20 seconds of
wall time. The geometric distance check remains only a conservative stop condition;
it does not navigate around obstacles or identify the enemy. Do not add adaptive
pathfinding. A further course decision requires a fresh screenshot and reviewed
positions. This amendment is prospective and does not turn the expired first
window into a pass.

## Observed result

Fresh PID 17072 loaded the named Stepping save, Vaan level 1/HP 103. Initial
qualification verified the authority executable, base, known read constant, complete
selected .text bytes, watched-module classification and active unit self-indices.
Full module names retain the overlay context. Group 1 again had member 1/dead 0/
flags 0/slot3 0, with HP 134 and immediate mode 1. No group-completion claim changes.

The new pulse helper opens the process read-only, requires exact read lengths and
the expected sole held-key index, and releases on a short read or wrong-code failure.
Three injected controls validate positive delivery classification and those two
failure paths without sending OS input. All 16 live pulse/snapshot receipts completed;
these are instrument outcomes, not 16 successful gameplay transitions.

The second attempt's preset eight W pulses reduced the sampled 3D distance from
85.8795 to 44.8665 coordinate units in 13.1675 seconds, with a fresh read between
every pulse. Each of the eight post-pulse checks had player HP 103 and target HP 134.
The target retained actor pointer 1734199984 during this bounded sequence. The player
ended at (116.4246, 34.7890, 240.2929); the target was then at
(140.1570, 30.8096, 202.4255). These coordinates are local to this run, not persistent
handles, a general route or measurements of world units in metres.

After the block ended, the screenshot shows a wolf attacking and Vaan at HP 86.
The per-pulse reads do not cover the interval after the last pulse. The screenshot
must not be described as proving HP stayed 103 until shutdown. No attack command
was submitted, the grouped actor was not visibly identified or reached, and no
enemy death was established. The original 60-second approach timed out; the separate
amended block hit its eight-pulse limit without a stop-condition failure. Neither
attempt satisfied the final-death objective. There was no combat ledger trace.

Close/restoration receipts record only owned PID 17072 closed and all 26 original
save/config hashes restored, with no extra files. Only the expected GameSetting.ini
adapter LUIDLow rewrite differed. Runtime was released.

## Next discriminating work

The immediate obstacle is now the intervening encounter, not arrow delivery or
movement progress. The existing R2 modal-toggle page leaves its visible behavior
explicitly unknown (PROPOSED-repos2d-7) and supplies the toggle/latch/output globals.
A stationary press/release observation can resolve that semantic gap and determine
whether the mode offers a usable way past the encounter. It must not be called flee
mode from plausibility alone. Do that bounded control before another group approach;
do not replay this unsuccessful route unchanged.
