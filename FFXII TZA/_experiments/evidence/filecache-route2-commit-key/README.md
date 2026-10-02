# Cache backfill uses a prior lookup key

SOL in ASTRA; method A, original EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Producer-validated conditional source result; independent review and canonical
incorporation pending. No game, harness or original-instruction execution.

The supplied route-2 cache fill does not rehash the archive's MD5 name at its
commit boundary. Resolver59EE90 reads DWORD source-record+28 into EDX at59F1B0.
59A9B0 saves that incoming key in ESI and supplies ECX=ESI at59AAA4->1D6A20.
The source's size, signed selector byte and local base-pointer address are
separate arguments. Under normal Win64 ABI, intervening calls preserve the
saved key. Preserving this register does not prove any memory value stable.

A finite abstract interpretation of the original resolver's one arm byte,
r12b, establishes that every locally armed59F1B7 commit passed the earlier
59EFE5 cache lookup. It explores606 abstract states, with other branch decisions
nondeterministic and normal nonvolatile-register ABI assumed. These are not606
executions, concrete archive-feasible paths or a full symbolic game model.

That lookup's fifth argument is the out-key address: retained1D6D20 maps the
incoming R9 address into the fifth20C1B0 argument; the native5push/SUB150 frame
loads it from currentSP1A0 intoR14. Two cases matter:

- A nonempty normalized name calls674A00 and writes EAX throughR14 at20C22D
  before every local normal return, including a tree miss. The original hash's
  exits all pass BTR EAX31. This newly written key is in0..7FFFFFFF.
- An empty normalized name jumps directly to return-1 without calling the hash
  or directly writing the out-key. The resolver also has no direct record+28
  write. Under the explicit nonaliasing/no-callee-interference conditions, an
  ensuing armed successful archive fill therefore forwards the prior field,
  rather than a fresh hash.

The second case is a conditional output/precondition rule. It does not prove
that natural shipped-game requests generate an empty normalized name, that
such a name hits the archive, or that a high-bit cache key occurs naturally.
Initial record+28 values, reuse, all callers and actual archive feasibility
remain separate. The known31-bit lookup domain must not silently become a
universal insertion-domain claim.

The producer pins1491 newly captured bytes in three complete local bodies,
including the resolver epilogue through RET59F1FB beyond its prepared .pdata
fragment. It reuses the accepted79-byte lookup wrapper and40-byte hash body.
All selected bytes are compared directly with the pinned original EXE and
re-decoded using the reviewed memory-role adapter before CFG or result output.
Original references, raw source, normalized observations and consumer preimages
are retained. No selector/filter census, prefix illustration or archive export
was repeated.

Required premises: valid distinct record fields/out-pointers, private frames,
readable terminated input and normalizer output, successful bounded normalization
where used, normal Win64 ABI/returns, and opaque callees/concurrency do not
interfere with source-record+28 before its read. Native callback effects,
allocator placement, initialization, lifetime/reuse, natural reachability,
actual imports and scheduling are unproved.

Validation and learned failure: prove01 refused before output because the
retained hash capture has an exit-only legacy receipt, not a terminal/driver-bound
one. Its exact failed driver/exit/stderr and disposition are preserved. The
current result explicitly labels that receipt incomplete; its needed original
hash bytes are independently verified from the shipping EXE. No new capture or
invocation-success credit was invented. Producer02/result01 and six actual CLI
refusals establish the science at that producer identity. Producer03/result02
only renames the source-map fields to the existing publisher's required schema;
an AST differential confirms no other producer change. The actual publication
guard validates all three source maps and refuses missing/stale maps. Scientific
samples and six unchanged refusal cases were not repeated for that metadata edit.

Reproduce in a fresh disposable copy: run.py capture-NEW capture.py, then
run.py prove-NEW prove.py RESULT-NEW.json. Historical controls and current
publication controls are identity-bound; reconstruct their exact drivers/inputs
from the manifest and inherited-input maps rather than modifying published files
or running into an existing result. Missing inputs, nonzero/partial invocations
and coherent original-byte mutations refuse output; absence is not valid empty
success. Six producer CLI refusals and two guard calls are not FF12 experiments.

Affected consumers: FABLE path/cache backfill semantics and OV33E2 prerequisite;
OPUS source-record+28 out-parameter and pre-keyed insertion contracts. Original
insertion/new-node copy packet remains separately pending; this result does not
require promoting that packet to accepted. Independent SPEC review, consumer
agreement and wholeOV33 closure are distinct and pending.

All own completed scientific children terminal. No PC/game/instrument/save/config/
reference or peer changes. FullL1+L2 goal ACTIVE/NOT_MET. Historical four accepted
runtime needs eliminated offline unchanged; this new scoped question is answered
at producer level only. K14 closed, EXP127 invalid, menu allowance spent and
extension unapproved. Next discriminator: read existing source-record initializer/
rebind evidence before deciding whether the retained field is initialized or reused;
do not collect live samples merely because the historical row says runtime.
