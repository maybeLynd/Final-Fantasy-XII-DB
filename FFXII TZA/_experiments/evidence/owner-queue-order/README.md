# Older-request order on the ordinary queued primary path

Producer-valid conditional source proof; independent review and canonical
consumption pending. This package supplies one ordering premise for the
owner-admission/reset question. It does not settle global owner uniqueness.

Question: can primary B's ordinary queued completion run while indexed-owner
request A, already pending before B's accepted insertion, is still pending?
The competing explanation is a pump that skips or overtakes the older slot.

Method A is sufficient for this conditional question. Seven original bodies
are reused from SECTION09's immutable retained disassembly/manifest and checked
against the certified shipping EXE. Only the 24-byte pump switch table is newly
read statically. No native execution, game session or native sample recapture.
The actual capture and byte-validator paths use the reviewed access-role adapter
with memory-store, LEA/address and read-modify-write controls.

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base `0x120000`, Capstone 5.0.7. See source02, source-run02 receipt and
the result for full range, table, adapter and checker identities. Source01
qualified five bodies; it is retained with its exact driver preimage as history.
Source02 adds the existing completion helper and original RET0 leaf so callback
association and the recycle tail are explicit. Source01 is not another experiment.

## Original source establishes the local queue operations

* Requester32E620 has exactly two local32E870 call sites. Mandatory stores
  at32E6B9 and32E742 put1 in outgoing sixth argument `[RSP+28]`.
  Receiver32E870 pushes three registers/subtracts20, then reads `[RSP+68]`
  (entry+30, the sixth argument) into ECX before32E990.
* Insertion32E990 takes the free head and uses nonzero atTail to select32EA1A.
  On a valid nonempty list it sets tail to the new node, oldTail.next to new,
  new.prev to oldTail and new.next to zero. Empty insertion makes head=tail=new.
  The zero-argument arm instead inserts at head. Valid finite, disjoint lists
  and a fresh free token are premises; irregular-list branches are not a sanitizer.
* Removal32EC40 updates head/tail only for endpoints, connects previous.next
  to next and next.prev to previous, and puts the removed node on the free list.
  The redundant neighbor writes have the same value on a valid list. Its final
 16D6A0 is the shipping three-byte `RET0`, not a harness stub.
* Pump32E070 loads pending head022C51C0 into RBX at32E090. Complete local CFG
  and computed-jump table are checked; only the epilogue otherwise redefines
  RBX. No local next-node advance or direct head permutation exists. The real
  RCX provenance at every completion/recycle call is checked through branches
  and calls; opaque calls clobber RCX in that analysis. Dominance alone would
  not establish the argument. Completion32E330 reads that head slot's callback
  +40, destination+70 and data+60 and calls it with R8D=1 when nonnull.

## General order argument

Immediately after accepted tail insertion, arbitrary finite list
`P ++ [A] ++ Q ++ [B] ++ R` has A before B. Head/tail insertion of another fresh
token adds a prefix/suffix. Removing a different token deletes only from P/Q/R.
These operations preserve A-before-B while both tokens coexist. Removing A/B
ends that antecedent; reusing its physical slot is a new token. Thus head-only
completion cannot select B while A still precedes it. A must retire before B
delivery under these operations and the stated noninterference premises.

This is an arbitrary-list invariant, not an inference from many no-hit samples.
Three algebraic illustrations preserve tail ordering, refute a head-primary
extension and show that removal destroys the antecedent. They are not FF12
machine-code executions. Four actual reducer-CLI refusal controls ensure failed
qualification, changed original tail flag, omitted removal and absent switch
table cannot yield a result. Positive/source/control receipts preserve exits,
stdout/stderr and driver hashes; missing evidence is not empty valid output.

## Required limits and consumers

Normal ABI, stable caller stack argument, valid nonaliasing queue memory,
unchanged request identities and only stated normal queue transitions are
premises. Recursive pump, concurrent corruption, queue reset/permutation or
opaque effects that bypass them remain outside this lemma. Non-progress can
retain/revisit the head or return; no fairness or deadline is proved. The
receiver can pump while the pool is full before accepting the new request.

Retirement can be error/cancellation, not successful owner completion.
Requests submitted after B's enqueue are not covered. Neither head-primary
32E780, synchronous D4/direct3304A0 nor world-reset paths inherit this proof.
No live state, lifetime guarantee, safe reload or whole OV19/21 closure.

SPEC independently reviews this scoped proof. Existing FABLE owner-admission
and OPUS owner-reload consumer tasks receive the package after acceptance,
without duplicate requests or edits to their pages. The supported change is
an explicit older-before-queued-primary premise, alongside the still-open
later-submission/producer-disable and direct-call cases. Next discriminator:
original32ED80 disable interval and32F850 re-enable-before-bind, followed by
the exact D4 cached-payload/caller bounds where needed.

Cleanup: all original/retained reads only, disposable outputs in the claimed
work directory. No FF12/PC control, save/config/reference writes or retained
processes. All finite children terminal. Goal L1+L2 remains ACTIVE/NOT_MET;
independent acceptance, canonical consumption and final audit remain separate.
