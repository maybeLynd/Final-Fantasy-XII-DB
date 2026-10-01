# Restore's counter is also a possible saved target

Question: does the published Restore postcondition follow from the stated
no-outstanding-Save condition when a valid saved target covers 022D8F08?
Consumer: OPUS's transform-workbench save/restore contract; FABLE's semantic
save/restore page. This is an interface precondition for hooks/modding, not a
claim that one of the nine shipped callers supplies this pointer.

H1: Restore uses the entry count, so every recorded target is restored.
H2: Restore rereads depth after each target store, so an earlier target can
alter which later entries are restored. Current source favors H2.

Method A is sufficient: retain complete verified shipping 89B Save and 66B
Restore, decode the target store and both depth reads, and account for their
ordering. No fresh original-code/live execution is required. Existing ordinary
pair differential work establishes a different, disjoint fixture; do not rerun
it to claim a first execution. Keep its exact source/contract preimages.

Discriminator: depth starts zero (no outstanding Save). Save two valid readable
16B targets, with target0=depth and target1=a separate row. Save snapshots the
zero depth before assigning count2. After the caller clobbers only target1,
Restore writes saved zero into depth before its loop comparison; source predicts
target1 stays clobbered. Contrast disjoint targets and depth as the last target.
These are conditional source calculations, not observed machine-code runs.

Controls: validate original bodies/RET boundaries/hash/reader identity; resolve
RIP depths and the pointer/value array addresses from actual decoded operands;
validate MOVUPS target width and unsigned CMP/JB ordering; preserve the disjoint
and last-target contrasts to avoid claiming every overlap fails. Do not infer
array extents, native caller reachability, scheduling or lifetime from arithmetic.

Acceptance: complete source confirms post-store counter reload and the
conditional counterexample satisfies the page's explicit starting condition.
Failure: identity mismatch, incomplete decode, unresolved address/order, or an
existing explicit target-exclusion precondition invalidates the proposed defect.
Escalate to B only if A cannot distinguish the transfer/order; no C setup.

Restoration: read-only executable/peer files, private analysis output only; no
FF12 launch, PC control, attachment, save/config/reference writes. Published
inputs remain immutable. Request independent review and owner correction once.
