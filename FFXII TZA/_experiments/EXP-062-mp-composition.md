---
experiment: EXP-062
title: scratch-to-result-to-native-MP composition
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies this numeric copy-out to MP composition; HP effects and preparation members are not executed.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Same-state original copy-out, dispatch and MP composition with an explicit injected frame bridge; ownership and eligibility controlled, HP absent.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-062-mp-composition/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-062: scratch-to-result-to-native-MP composition

**Result:** nine isolated compositions passed on first execution; a sign-extension
mutant changed final resource state and was detected. ASTRA, 2026-09-11. No game
process was accessed.

## Why this probe exists

[EXP-059](EXP-059-formula-copyout-controls.md),
[EXP-060](EXP-060-result-numeric-dispatch.md), and
[EXP-061](EXP-061-mp-writer-controls.md) established separate contracts for numeric
copy-out, result dispatch and native MP/secondary writes. This probe tests their
boundary agreement in **one retained synthetic memory state**. It is a bounded
composition relevant to the charter's cross-system evidence criterion, not a claim
that the database transition gate or whole-action parity is satisfied.

## Original code and explicit bridge

The [checker](evidence/EXP-062-mp-composition/check.py) verifies the certified EXE
hash and executes original `0038643F..003866C0`, then stops at `003866C1`. It compares
both surrounding scratch pages and the complete result/stats page against an
independent model. That comparison occurs before the second phase.

The second phase retains those actual scratch, result and stats bytes. It installs
only parent-frame roles: target stats in RDI, cached HP/MP delta entries in R12/R15,
zero R13/R14, and the source stats pointer or null at stack `RSP+0x88`. RBX remains
the **same original result pointer**, and RSP remains the same synthetic frame.
Execution resumes at original `00311608` and stops at `00311778`.

This bridge deliberately skips the intervening original resolver/applier paths.
Those paths' gates, callbacks, status work and native frame construction are not
executed. The experiment therefore proves the selected contracts compose under
the stated injected roles, not that those roles describe a captured live action.

Within the dispatch phase, the native entries from EXP-061 run in full:
`00300CE0` (351 bytes), `00300C90` (73), `00300BC0` (207), `0030E060` (200), and the
original `0016D6A0 RET 0` (3). The 2040-byte applier parent and 642-byte copy-out
segment are retained with them. All bytes reproduce their prior evidence bodies.
The [disassembly](evidence/EXP-062-mp-composition/disassembly.txt), source and
[results](evidence/EXP-062-mp-composition/result.json) are sealed in the
[manifest](evidence/EXP-062-mp-composition/manifest.json).

Owner lookup `0031B860` is a controlled stub returning null. Both eligibility
helpers `0030B770` and `0030B7F0` return zero. Their calls and arguments are recorded;
volatile integer registers are clobbered on each stub return. Thus these stats
records have no native owner for presentation or accumulator-clear purposes.
The real HP entries are never called: all HP scratch inputs remain absent and
result flags start at zero. Unexpected callee execution cannot be credited as an
established native dependency.

## Inputs and observed composition

Target stats start with current MP 40, secondary word 80 and derived tier 0;
source stats start at 70/50/0. Both use maximum 100, multiplier 3 and no capacity
suppression. Numeric scratch entries are initially absent (`FFFFFFFF`), while
private difference inputs and the target-MP force flag start at zero.

The model independently derives result presence/addition/difference/absolute flags,
word outputs, and the expected final native states. In the native phase it also
compares exact call and write order, including the repeated eligibility calls on
negative deltas, secondary reconciliation and original no-op calls.

| Control | Distinguishing observation |
|---|---|
| All inputs absent | Numeric output fields become zero, but presence bits remain clear and no native MP/secondary calls occur |
| Explicit added-input zero on both sides | Presence/addition/difference flags select two MP calls with zero delta and healing-direction bit; fields remaining numerically unchanged does not mean no operation occurred |
| Target gain 30, source subtraction 25 | Target becomes MP 70 / secondary 110 / tier 1; source becomes MP 45 while secondary stays 50 |
| Absolute overrides with simultaneous difference inputs | Target requested 80 and source requested 10 replace the differences; original absolute entries are selected and native effects match their post-primary secondary checks |
| Added target `00018001`, source `00010002` | Result words are `8001` and `0002`; target is passed -32767 and reaches MP zero, source receives +2 and reaches MP 72 / secondary 52 |
| Null source pointer | A target gain is applied, but the source's populated result word and flags cause no source call |
| Target gain 30 plus private difference +1 | Primary gain updates secondary first; the applier then adds one maximum (100) to secondary, yielding target 70 / 210 / tier 2 |
| Target gain 30 plus private difference -1 | Secondary first rises to 110, then the direct -100 operation leaves 10 / tier 0 while primary MP stays 70 |
| Absolute zero on both sides | Presence plus absolute bits select real MP writes to zero; secondary words do not receive a positive top-up |

Private +1/-1 is established as a difference between two nonnegative private
scratch inputs, not by placing `FFFFFFFF` into a private input and assuming it
survives the absence normalization. The signed multiplier output is the original
low byte of that difference. No upstream authored meaning is assigned to it.

## Falsification and limits

The private mutant changes target MP `MOVSX EDX, word [RBX+0x2A]` at `00311673`
to `MOVZX`, without changing the original copy-out. The same `8001` result word
now enters the native writer as +32769 rather than -32767: target MP reaches its
cap, and secondary processing follows a positive-delta path. The exact calls,
writes and final page diverge from the expected negative-delta result. Both the
unmodified and mutant runs reach the expected stop; divergence is semantic, not
a timeout, missing output or invalid mutant.

The results retain full initial, post-copy, expected-final and actual-final pages,
copy-phase writes, expected/actual native-phase events, and phase-tagged instruction
visits. Both phases check their exact stop, RBX and RSP; the second also checks RDI.
The full surrounding pages detect unintended writes outside the selected fields.
Copy-phase write order is retained but its individual event oracle remains the
separate EXP-059 test; here the copy boundary is compared by complete memory state.

Native ownership lookup, nonzero eligibility masks, presentation, accumulator
mutation, HP effects, intervening status paths, frame timing and live action identity
are outside this experiment. None of those omitted effects is supplied by a model
and then labeled original behavior. FABLE/OPUS receive this as bounded composition
evidence for the already routed copy-out, dispatch and MP contracts.
