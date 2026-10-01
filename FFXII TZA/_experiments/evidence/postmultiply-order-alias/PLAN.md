# In-place composer: operand order and second-operand overlap

Claim/hypotheses: does complete003977B0 implement the page's flat row-major
C=A*B, or C=B*A? Does its copied destination protect exact C==B?
System/consumers: shared transform workbench; FABLE composition semantics,
OPUS ABI/preconditions. Existing349B page equation and snapshot guarantee
are the specific current claims; composer397910 is a different tested body.

Method A: original complete bytes, decoded operand ordering and small exact
conditional calculations suffice. No new isolated execution or live game.
Reference: shipping SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base120000, entry3977B0, finalRET39790C; reuse shipping reader, full hash gate.
Discriminator: diagonal A plus shear B separates BA[0,1]=3 from AB[0,1]=2.
Identity is a nondiscriminator. Same-buffer nontrivial2x2 block distinguishes
snapshotted right operand from next-column reads of overwritten right words.
Controls: complete decode/full hash, exact four left snapshot loads/stores,
four-column loop and all16 right scalar reads, source-derived output expression
trees, nonidentity discriminator and actual loop-carried hazard. Reject stale
source, incomplete decode, invented operand model or zero/non-discriminating cases.
Normal ABI, valid16-byte-aligned left matrix, stable right buffer and private
frame disjoint from arguments. No exceptional-float/general partial overlap
campaign, application caller reachability, enginewide storage convention or
live transform effect. No library effects inferred from cookie check.
Cleanup: artifact reads/writes only; PC OFF; saves/config/reference unchanged.
Publish immutable primary bytes/check/result/consumer preimage; route once to
OPUS/FABLE/SPEC. Independent acceptance and canonical owner propagation remain open.
