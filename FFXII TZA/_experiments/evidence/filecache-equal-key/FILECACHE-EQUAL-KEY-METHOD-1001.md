# Exact insertion/equal-key discriminator — 2026-10-01

Major system: resource/file-cache ownership. Consumers: FABLE OV33 E2/path
resolution and OPUS cache-key/ownership contracts. Existing exact-image source
shows 001D6A20 -> 0020B680; prior qualified source01 already retains 0059A9B0's
caller. That caller/domain is not an exhaustive insertion-site census.

Question: on a valid existing map entry whose unsigned 32-bit numeric key equals
the supplied key, does this insertion boundary re-check a path or replace the
payload with the incoming buffer/length, or does it retain the existing payload?
Competing explanations: path-qualified replacement versus numeric-key reuse.

Method A: close original wrapper, insertion, keyed value-slot helper, release
boundary and hit-wrapper CFGs. Exact body/instruction/register/stack pins plus
an invariant of the finite ordered tree suffice to establish this conditional
branch/data flow. Retained source alone lacks these complete boundaries. No
isolated execution, sampling or real process is needed for the local claim;
natural key population/collision/lifetime/reachability remain separate.

Required proof: supplied ECX -> EDX -> EBP unchanged; lower-bound unsigned tree
comparison and exact equality gate; incoming buffer handed to release boundary
before wrapper; existing data/length and existing mode reach wrapper; current
mode remains distinct. Observe actual wrapper allocation/constructor arguments,
not assume a stub proves constructor or lifetime effects. Mode/tag/refcount
operations may occur even when payload is reused.

Controls: source capture actually invokes reviewed role adapter (store/LEA/RMW),
re-decoding validation and original image/body pins; reducer positive has all
five closed CFGs/nonempty calls. Required capture status exit/terminal, stdout,
stderr and driver identities checked. Focused CLI negative cases: upstream
failure, incomplete body, altered original byte and incorrect stack-key source.
Missing input or invalid source cannot pass as empty output.

Premises: finite correctly ordered map, valid initialized objects/pointers,
non-aliasing valid incoming allocation, ordinary ABI and normal callee returns,
mutex/CRT behavior and no external interference. Inspect static import names
for the release boundary; declarations do not establish loaded targets.
No universal insertion-domain or thread/allocator/presentation guarantee.

Stop: once the conditional data flow and source/control checks are complete,
freeze/commit and route exact bounded result. If identity, CFG or controls fail,
retain failure and fix the producer before any semantic result. No live setup.
Restoration: read-only reference; fresh local output only; helpers must terminate.
Next discriminator after acceptance: actual insertion callers/key source domains,
then qualified archive namespace collision intersection if still needed.
