# Descriptor teardown: membership is not allocation provenance

**A complete original teardown + retained EXP097, with a focused B observer
control. Independent review and owner propagation pending.** No live game run.

The current contract retains an obsolete paragraph saying an unowned node stays
linked and the destructor need not empty the lists. That is true only during the
first free-walk. The complete original body subsequently drains +80/+90/+A0/+B0
and calls the +60 drain. Valid surviving nodes are unlinked; their membership
does not survive. Earlier native correction and retained EXP097 head observations
already establish that distinction. They were consumed, not replayed.

The runtime request's further inference, “not freed here, therefore STATIC,” does
not follow. Static, external, pool or arena ownership can all be compatible with
this unlink-only operation. Actual +B0/annotation node allocation provenance and
cross-state population remain OPEN. The independently established static field
record census is not contradicted or reclassified by this entailment check.

## Two primary-evidence limits found

EXP097's report describes post-state inspection of every head and node. Its
actual `run_case` observation dictionary and saved results record descriptor
heads, registry/embedded nodes, counter and vtable; they omit individual list
member spans. Preserve those valid observations. They do not certify a full
node-heap comparison or native allocator effects: `_aligned_free` was scripted.

The historical `m-selflink` mutation is also misidentified. NOP4 at6334F1 starts
on `488b0a` (`mov rcx,[rdx]`, three bytes) and removes the first REX byte of the
next instruction. It is not an isolated selflink-store mutation. Preserve its
recorded kill as a historical modified-code result; narrow the claimed intended
mutation coverage until the owner repairs it. The correct neighbor-unlink store
is6334F8, node selflinks6334FF/633502. The contract's633557 “call” anchor is actually
the argument LEA; the CALL is63355B. No shipping bytes were modified.

Our first reducer failed on the copied false anchors before any PASS. It is
retained in `qualification-failure.txt`. The repair uses actual instruction
roles and rejects the bad mutation/anchor; original guest captures were not rerun.

## Smallest raw-node control

The unmodified original71-byte `006B6700` helper runs without calls/stubs over a
supplied valid two-node ring. One node address is above4GiB. Both complete56-byte
spans and every write are retained. Both link words become self-addresses; all
other bytes remain unchanged. The helper returns normally at the supplied marker
with the entry stack restored. This is controlled guest state, not live placement
or allocation provenance. Each of the two arms is bounded at2 seconds/1000
instructions; no native OS process or external-memory API is involved.

A labeled mutation NOPs the complete4-byte node-prev-selflink at6B6740. It still
returns with the same empty head, while the node back-links remain stale. A
heads-only observation would miss that corruption. The new raw-node reducer
rejects it. This supplies the smallest concrete observer regression; it does not
silently replace peer production or rerun EXP097's historical15/10 campaign.

Five focused controls reject the real NOP as intact node state, short node reads,
missing native return and the two false source/mutation anchors. Exact original
500/71-byte bodies, EXE/tool identity, historical driver/result/body records and
current contract preimage are pinned. `check.py` reduces the saved captures and
does not execute native code. `probe.py` is the recorded isolated execution.

Affected claims: current membership wording; intended selflink mutation coverage;
full-node observation wording; no-free-to-static inference and helper call citation.
Unmodified EXP097 head/free-call observations remain bounded evidence. FABLE/OPUS
must propagate their consumer corrections; ORACLE owns any historical driver
repair and impacted node-observation cases. Independent review remains required.

Guest instances ended. No FF12, PC control, native child, debugger, input or
save/config/reference write occurred. No restoration was required.

Player version: a list can look empty while an item still contains a stale link.
We demonstrated that blind spot with original game instructions and corrected
the evidence boundary. Removing an item from a list also does not tell us who
owns its memory, so that ownership question stays open.
