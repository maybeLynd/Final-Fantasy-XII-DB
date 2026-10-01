# Descriptor node membership, survival and provenance

Question: current contract's old paragraph says unowned nodes remain linked,
while its corrected full teardown says they are drained. The BL8 request also
infers static storage because the destructor does not free a node. Separate
phase-local membership, whole-teardown unlink effects and allocation provenance.
Consumers FABLE semantic contract/BL8, OPUS lifetime/types, ORACLE retained driver.

H1: free-walk skip means retained membership after complete teardown.
H2: later unconditional drains unlink survivors; release is a separate operation.
No-free in this body is consistent with static storage OR external ownership,
pool/arena allocation or another lifetime manager. It does not distinguish them.

Method A is sufficient for the whole-body ordering and provenance entailment;
consume accepted EXP097 instead of rerunning its 15 cases/10 mutants. Inspect
the actual driver/result, not the report's claim of every-node post-state.
Its observation dictionary records heads/registry/embedded subnodes, not the
individual list-member spans. Preserve accepted head/free-call observations;
do not describe them as full node-memory or native allocator effects.

Small method B observer control is justified for that concrete gap: run only
the original 71-byte no-call annotation drain with two controlled member nodes,
record their complete spans and every write. A single labeled NOP of the node
prev-selflink store must leave final heads unchanged but fail node integrity.
This tests why a heads-only observer can miss the effect. No historical full
campaign, live game, allocator callback/stub or lab rebuild.

Budget: original plus one mutation control, each 2 seconds/1000 instructions,
mapped six small guest pages, initialized Win64 entry stack with return address,
complete exit-point and restored-stack proof. Reject invalid identity/short
read/unexpected writes/non-return; original must self-link each node and preserve
all bytes outside the two links. Mutation must be detected by the new span check.

Exact EXE/driver/body/tool identity, raw register/memory/write sequence, historical
source/receipt and consumer preimage retained. Independent review and owner
propagation pending. Supplied nodes (including one above4GiB) do not establish
actual allocator placement or live class-descriptor list population/lifetime.
Guest sessions end; no process/input/save/config/reference write or cleanup is
needed. Keep BL8's actual allocation/purpose/global population questions open.
