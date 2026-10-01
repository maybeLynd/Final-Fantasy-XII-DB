# Licence mask builder: clear size comes before the signed loop gate

**B bounded original-code witness + A caller/ordering evidence, pending review.**
The underlying EXP140 request is already answered and consumed by OPUS. This
separate package tests previously uncovered output/count boundaries, reusing its
unchanged World/loader rather than replaying57 cases or35 mutations.

| supplied descriptor count (u32) | original clear argument | observed endpoint | supplied46-byte output |
|---|---:|---|---|
|0|0|normal return0|warmA5 bytes unchanged|
|8|1|normal return0|first byte0, other45 remainA5; both canaries intact|
|FFFFFFF9 (signed−7)|0|normal return0|warmA5 bytes unchanged|
|FFFFFFF8 (signed−8)|536870911|planned stop at scripted callback entry|unchanged; clear not executed|

Counts/rows/output are **controlled guest fixtures**, not shipped-data or live
reachability observations. The original builder, decoder and classification
instructions execute from the exact shipping EXE73461d... . The memset IAT thunk
is original, but its target is the existing disclosed scripted bridge. Only clear
sizes<=46 may enter it. The oversized case stops before the bridge and before
the signed loop test. It proves the argument/order, not a large write, corruption,
crash or completed function. No native CRT effects are certified.

**Why the ordering matters.**002F8FD3 computes lea r8d,[rax+7], wrapping to32 bits
and zero-extending, then002F8FD9 logically shifts r8 by3.002F8FE0 calls the clear
thunk. Only afterwards does the function reload the count and test r14d/jle at
002F8FFC/002F8FFF. A nonpositive signed loop count therefore cannot be used as a
guarantee that no clear request occurred. The upper-bit raw count supplied here
is deliberately malformed; normal loader validation/reachability is not settled.

**Separate output extent from physical initialization.** Count0 describes a
zero-byte logical mask. Calling that logical mask empty/all-zero is compatible
with these results; it does not guarantee that a caller's preexisting46 bytes
were physically cleared. Original PREREQ00323BB0 independently zeroes five
qwords, one dword and one word at stack+20..4D BEFORE calling the builder. That
46-byte guarantee belongs to the caller, qualified here statically, not to a
zero-sized builder clear. The current contract section13 should say this
explicitly and qualify malformed-count preconditions; its normal predicate and
EXP140's absent-action edge remain intact.

**ABI and observer controls.** The local wrapper supplies Win64 entry RSP%16=8
and observes the same alignment at the bridge entry; it does not use the older
World.run_one stack recipe. Registers, mapped stack/descriptor/output and return
marker are explicit. A native count8 control reaches a1-byte scripted clear and
changes exactly that byte. Each run is bounded at2 seconds/6000 instructions;
all three small cases reach the return marker with no guest fault, the fourth
has its explicit planned stop. Raw inputs, before/after78-byte spans, event order,
RSP, call arguments, returns and terminal addresses are preserved. No result is
inferred from an attach or zero-case receipt.

The initial source guard stopped BEFORE import/execution because Git's LF driver
and the unchanged working copy's CRLF bytes differ. Normalized bytes AND AST
matched; only that serialization difference was allowed, both hashes recorded.
Peer source was untouched. The first reducer campaign also failed its corrupted
event-order control; no valid receipt was issued. `validation-failure.txt` retains
that defect. The smallest repair requires positive strictly increasing event
sequences within the instruction budget; only the impacted reducer was rerun.
The original four B observations were preserved, not rerun to seek a green result.

`check.py` qualifies exact original287/170-byte code/transcripts and raw witnesses,
and rejects7 counterexamples: a zero-count full-buffer guarantee, signed-loop
skip suppressing the earlier request, boundary stop called a completed clear,
lost event order, invalid ABI entry alignment, missing positive bridge effect,
and wrong reference identity. These are producer controls, not independent
acceptance. Historical57/35 controls remain in EXP140 and are not added to this
package's counts. Existing fixtures and their evidence limits stay with ORACLE.

Canonical propagation is **PENDING** through OPUS/FABLE and independent AUDIT-SPEC.
Actual initialized descriptors, valid shipped counts, normal gameplay and native
CRT consequences are not newly proved. No game process, PC session, OS-memory/
input/debugger/instrument or save/config/reference write occurred. Guest sessions
ended; no restoration was required. Source/driver/tool/interpreter identity and
raw receipts are retained. Never execute the oversized callback from these
inputs; the capture requires its bounded entry stop.

Player version: an empty licence table does not erase a whole existing mask by
itself. The usual caller clears its own mask first. We also confirmed that a bad
row count reaches the size calculation before the loop rejects it; the test
stopped there safely and says nothing about a normal-game crash.
