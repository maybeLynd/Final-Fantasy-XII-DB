---
experiment: EXP-035
title: Command and resolved-target census pairing
status: PREPARED — component and ambiguity controls pass; no live observation
contract: none - bounded preparation of a command/target binding reader; a Method A tooling record that executes no shipping game code. Checked BOTH directions 2026-09-13: it names no contract and no contract names it
date_designed: 2026-09-11
method: A - offline instrument preparation
live_game: false
---

# EXP-035 — join the command to a verified target row

EXP-032 captures current command bytes; EXP-034 resolves the handle through the
original registry contract. This composition supplies the missing check before a
future combat observer attributes an HP value to that command. It does not run the
game or infer what occurred in EXP-027's uninstrumented command state.

[binding.py](evidence/EXP-035-command-target-binding/binding.py) accepts the qualified
Reader interface already used by the field observer. It takes a field census, reads
the selected player's command, resolves the target, repeats command/resolution and
takes another census. Each nonzero resolved unit must match both the unit pointer
and actor pointer in a unique census row before that row's HP is returned as bound.

Changed player identity, current command bytes, resolution result, conflicting actor
identity or a target appearing/disappearing between censuses produces
AMBIGUOUS_SELECTION. A legitimate null resolution is `unresolved`. A nonzero resolved
unit absent from both censuses is `outside_filtered_census`, with no guessed HP. The
existing census filters inactive/unrepresented actors; absence is not death proof.
Read failures propagate as errors rather than becoming null resolutions.

The output preserves both raw command snapshots, both resolution receipts, selected
player rows, target rows and outer frame endpoints. CONSISTENT_SAMPLE means only
that these checks agree. It does not establish atomicity, absence of an ABA reuse,
same-frame ordering, current action execution or causality of HP changes. A retained
target field beside a sentinel context is not promoted to an active command.

## Controls and intended use

Seven tests cover stable binding, changed command/resolver/player/actor, missing
filtered rows, null resolution, a disappearing target and an unreadable input. One
test additionally runs the actual EXP-032/034 helpers across all17 saved original-chain
fixtures, comparing the bound unit with the original code's result. The policy tests
use injected component values to exercise changes between reads; those are synthetic
controls, not game transitions. The [test receipt](evidence/EXP-035-command-target-binding/unit-tests.txt)
and [manifest](evidence/EXP-035-command-target-binding/manifest.json) preserve identities,
including the imported components and original-fixture source.

For the next qualified combat attempt, record bounded samples before command commit,
after commit, and after any separately specified movement. Reject ambiguous pairings
and corroborate the UI separately. Do not infer range waits, command cancellation
writers or enemy death solely from these rows. No extra runtime process, input
action, debugger or persistent writer is introduced by this preparation.
