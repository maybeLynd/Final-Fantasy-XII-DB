# Cache fill key provenance and conditional release on failure

Method A, exact shipping EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Producer SOL in ASTRA; independent acceptance/canonical incorporation pending.
Consumers existing FABLE cache/OV33 E2 and OPUS ownership contracts.

The cache fill inherits the key computed by the original direct-cache lookup
from its original raw path. It does not recompute from the separately prepared
lowercase archive lookup name. 001D6D20 supplies source+28 as the fifth key-output
argument of0020C1B0. A nonempty normalization stores the computed hash there
before an ordinary map miss. After archive success,0059EE90 reads that slot's
lowDWORD intoEDX for0059A9B0; that function retains it inESI and forwards it to
001D6A20 unchanged. These facts close this chain's local key provenance.

An empty normalized cache path is different:0020C1B0 returns-1 without writing
the key output. Do not apply the nonempty miss result to that branch, or infer
that shipped paths naturally enter it. The abstract arm/lookup analysis carries
two boolean facts, with SETNE conservatively permitting both values; every
admitted fill state has lookup performed and arm set. This is finite source
reachability under ordinary ABI, not a trace of gameplay states.

The ownership boundary also has a precise conditional consequence. On a valid
equal-key hit, the incoming buffer first reaches0020B0F0's release boundary.
If the subsequent16-byte wrapper allocation normally returns null,0020C300
returns0 and registration propagates it. The fill caller still holds its
original nonnull buffer in the same stack slot and takes its nonpositive-result
cleanup:001D6B00 ->0020BE40 ->0020B0F0. Thus two original release-boundary
invocations receive the same incoming pointer under that null-return and
normal-return/noninterference premise. The local routines do not clear the
caller buffer slot to suppress the second invocation.

00210EC0 ->0085E730 tailcalls statically declared malloc; it is not a local
throwing operator-new wrapper. Microsoft's malloc contract allows null on
allocation failure, and describes configurable new-handler behavior.
[Official malloc contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/malloc?view=msvc-170).
This is a named external API premise, not verification of FF12's loaded CRT,
handler or heap. In particular, whether malloc16 can fail immediately after
freeing this particular allocation in the real process remains unproved.

No natural double-free/crash/OOM, successful second free or process survival is
claimed. No malloc/free stub, original-code execution or game session occurred.
Valid disjoint objects/stack/incoming allocation, normal ABI/callee returns,
ordinary contracts and no interfering mutation are explicit premises. One
chain does not close all insertion callers/indirect writers or archive-only
population. Accepted six-path namespace b810fbcad/f24457dc7 remains separate;
no archive census was repeated.

Producer checks bind12 complete original boundaries, byte/role/import/frame
identity, inherited immutable parent manifests and checked new source exits/
outputs. Four actual CLI controls refuse failed upstream, coherent truncated
resolver, coherent output-pointer change and false malloc attribution.
The first positive refused unconditioned CFG domination before creating a
result: it admitted impossible bypass-then-armed combinations. The producer
now carries the original nonvolatile arm bit; failed receipt/preimage remain.
No generic graph helper or identity gate was relaxed.

The tiny release/allocator thunk source was originally captured inline, with
tool exit0 but no prehashed named outer wrapper. This limit is retained. The
checked qualifier verifies retained bytes against the exact shipping image,
re-decodes roles and adds the static import declaration without recapturing.
That qualifies source content prospectively; it does not invent stronger
historical invocation receipts. Inputs/results and failed runs stay immutable.

Reproduce into fresh owned output with pinned repository external dependencies:
`python prove-filecache-fill-and-failure.py --out <fresh.json>`.
Missing/moved parent manifests or source inputs refuse rather than pass empty.
All own helpers are finite; no PC/game/save/config/reference/peer processes
changed. L1+L2 goal ACTIVE/NOT_MET; live-only gaps, parked menu stop-loss and
invalid EXP127 remain explicit.
