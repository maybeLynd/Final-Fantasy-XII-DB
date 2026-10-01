---
experiment: EXP-027
title: Ordinary enemy death state-establishment control
status: PARTIAL — menu recipe established, no observed damage or enemy death
date_designed: 2026-09-11
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - the state recipe, not the transition. PARTIAL: no damage and no enemy death were observed, so CONTRACT-hp-write-and-lethal-transition gained nothing. The recipe is a precondition for a later experiment, not evidence for a contract.
---

# EXP-027 — establish one ordinary fight before handler tracing

FABLE-REQ-ASTRA-HANDLERS needs a fight containing an enemy death. Previous group
approaches did not produce one, and adding debugger uncertainty cannot fix missing
gameplay coverage. This package tests only the state recipe, with no debugger.

Load the known Stepping save under exact build/module/code controls and preserve all
26 save/config files. Use the visible battle menu to select Attack and a visibly
named nearby ordinary enemy. Retain screenshots before each menu decision, validated
bounded input pulses, and raw unit/actor/HP/self-index reads. Do not infer enemy identity
from a guessed pool slot; bind a visible name to the selected target where possible.

Allow at most six one-second movement pulses and one initial Attack selection. Once
the command is established, observe for at most30 seconds at20Hz, with no further
command or movement adaptation. Stop the fight observation on player HP below35,
loss of controls, or after a target's observed positive HP reaches zero followed by
retirement/visible defeat evidence. If the target is not securely identified or no
death occurs, retain a partial control and do not claim handler coverage.

The live observer must retain all active units and raw HP values, frames and times,
not just its interpretation of death. A disappearing unit alone is insufficient
because zoning/streaming could cause retirement. No group completion claim follows
from an ordinary enemy death; group/mode/ledger data are contextual only.

Close only the owned reference, restore the complete original save/config census
and verify cleanup. Bank any successful recipe for a later separately controlled
handler trace, whose debugger trust boundary remains unresolved.

## Prospective command-limit clarification

The first Attack-menu inspection at the starting position displayed **No Available
Targets**, and no target was confirmed or command issued. Before movement, clarify
the command limit as one issued Attack command; the empty inspection remains an
observed setup failure. The six movement pulses and30-second observation limit stay
in force. A later menu inspection may select a target if one becomes available.

## Prospective second window — queued command with closer range

The first30-second window expired with a visibly full Attack gauge and a still-live
Cactite outside contact range. No new command was issued. Preserve `fight.json` as
the failed no-movement control. Before further input, authorize a separate bounded
second window: at most two additional W pulses of1second, checking HP after each,
then one more30-second observer with the same HP35 stop. This changes physical
separation while retaining the queued command; it is not a retroactive expansion of
the original six-pulse/30-second window. If unsuccessful, stop rather than extending
again. No second target confirmation or attack command is permitted in this window.

## Result

PID38872 loaded the verified Stepping save. At the initial position and after two W
pulses, the target list showed **No Available Targets**. After five total W pulses,
the sole visible Attack target was **Cactite A**, retained in `final-targets.jpg`.
One Space confirmation produced a drawn weapon and a full yellow Attack gauge,
retained in `during-command.jpg`. The player did not automatically close the gap
in this observed window. No command-state memory field was captured, so the visible
display alone does not prove the entire internal command state.

The nearest non-player actor at target selection was slot7, address754798080, HP84,
about9.11 world units from Vaan. It was selected as the observer's candidate target.
This is a spatial association with the sole visible Cactite, **not a direct read of
the UI target pointer**; the unit-name binding remains unproven. All active units
were retained, so the outcome is not based solely on that candidate.

Both30-second windows expired with590 samples each. Player HP stayed103; candidate
HP stayed84. No captured numeric HP declined in either window. Some other actors'
stats pointers became null and later readable, without a preceding sampled zero;
those are not deaths. No visible defeat or enemy death was observed. This package
does not satisfy the ordinary-kill prerequisite and supplies no handler hit/zero
coverage. The observer's health/death stop branches did not trigger live.

Candidate/player distance ranged5.826–16.944 in the first window and5.475–14.685 in
the second. Proximity was not held constant, and no authoritative attack-range
threshold was measured. The initial suggestion that reach alone explained the idle
command is therefore a hypothesis, not a resolved cause. The two extra W pulses
changed position but did not produce a close-contact control. After movement the
Attack display and drawn weapon were absent in `second-window-view.jpg`; the
assumption that the command remained queued was not established. Movement itself
is not proven to be the cancellation cause, since time/target state also changed.

The first five movement pulses belong to the original window; the two additional
pulses were prospectively documented as a second window. Neither failed window is
relabeled a success or discarded. These are1180 samples in two observation windows
of one loaded scene, not1180 distinct states. Reads and HP rechecks are non-atomic.

## Controls, cleanup and next discriminator

Full selected .text and watched-module identity passed before and after. All input
pulses verified focus, the expected sole held index, and complete release. The
known raw-read constant and active-unit self-index controls passed. Exact sources,
raw numeric/byte HP reads, positions and frame brackets are retained in the evidence
directory. No debugger, R2 press, memory write, save or zone transition was requested.

Owned PID38872 was closed, and all26 original save/config hashes restored with no
extra files. Only the adapter LUIDLow setting differed. Runtime is released.

Before another combat run, resolve a read-only selected-target/queued-command anchor
and the approach/retention behavior needed to distinguish an idle out-of-range
command from a canceled one. Do not repeat the same stationary30-second wait or
add debugger instrumentation until the enemy-death prerequisite is established.
