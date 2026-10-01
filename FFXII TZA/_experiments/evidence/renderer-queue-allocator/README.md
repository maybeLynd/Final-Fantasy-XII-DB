# Original renderer allocator and conditional null publication

ASTRA/SOL, 2026-10-01. Method A, producer checked; independent review and
canonical consumption pending. No native/emulated/game execution.

Question: does the bound allocator guarantee nonnull on normal return, and
does the initially-empty reserve arm check the returned pointer?

Original `902720` slots `+10/+18` name `1EDF80/1EDFE0`. Two complete normal
roots (90 and 96 bytes) and exact PE descriptor/ILT/IAT/name metadata bind
the allocator to `_aligned_malloc(size,16)` and the release tail to
`_aligned_free(pointer)`. The old `free` import is a metadata control only.
`1EDF80` retains incoming RDX across optional `malloc(32)`, then passes it
as RCX with EDX16 to the aligned allocation tail. No local return-side
nonnull test, retry or exception adapter exists. Actual DLL/heap effects
are outside this original-code boundary.

Both wrappers lazily test global `01F82E48`. A zero global triggers
`malloc(32)`. A nonnull result initializes only DWORD offsets0/4, QWORD10,
DWORD18; holes8..F and1C..1F are not covered. A null result skips those
stores, stores null to the global and continues. This proves neither
thread-safe initialization nor a native header allocation outcome.

`1EDFE0` tests the preserved incoming RDX after that header work. Null skips
the release tail; nonnull is passed as RCX. The incoming R8 byte/count
argument is unused locally. Thus a null pointer does not imply that the
entire wrapper makes no calls. No meaningful return value from this void
release import, successful free or valid ownership is inferred.

The [documented aligned allocation contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/aligned-malloc?view=msvc-170)
permits null on allocation failure. For nonzero80000/alignment16 this
external contract cannot justify an unconditional successful allocation.
This is a separately labelled API premise, not a hash/inspection of the
FF12-loaded CRT or a captured native failure. The
[aligned release contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/aligned-free?view=msvc-170)
also remains distinct from actual pointer ownership/effects. Source URLs,
read time, paraphrases and limits are in the external-contract record.

Retained shipping `188640` supplies the conditional source consequence.
For a backed unchanged bank with begin=current=end0 and any unsigned
desired count D in1..FFFFFFFF, capacity0 selects allocation; D!=0 calls it;
begin==current skips copy; original begin0 skips release. Given normal
returned pointer A and normal Win64 ABI, the subsequent local stores are
`(begin,current,end)=(A,A,(A+16*D) mod2^64)` without a nonnull gate.
For A0/D5000 this is `(0,0,80000)`. It is an abstract conditional path,
not a native execution, naturally reached failure, successful capacity,
crash or arbitrary nonempty-bank safety claim. Earlier seven-span
initialization proof/review remains a separate package; its source is
reused, not recaptured or automatically accepted here.

Actual capture controls use the reviewed shared adapter for store, LEA
and read-modify-write roles, then re-decode all records. Prover02 requires
the actual capture exit0 plus exact driver/source hashes, complete normal
extents, original full-body pins and named import metadata. Its single
successful invocation and four actual synthetic CLI refusals are retained:
failed capture exit, coherent alignment16->32, wrong native-import binding,
and missing retained reserve body. Invalid cases emit no semantic result.
They are producer controls, not original-code executions or independent
acceptance.

Prover01 failed before emitting a result because it expected an empty
string for an absent RIP index; the reviewed adapter actually represents
it as null. The original driver/exit/stderr remain. The historical preimage
filename mentions scale, but the defect was **index representation**, not
scale. Prover02 uses the actual schema and still binds exact RIP target,
size and read role. No general CFG helper was relaxed; no source recapture.

Reproduce the semantic reduction with the retained raw files, pinned
dependencies and a fresh result name:
`python prove-renderer-queue-allocator.py SOURCE_DIRECTORY CAPTURE_STATUS FRESH_RESULT`.
Use a fresh directory for `control-renderer-queue-allocator.py`. Original
capture reproductions require the existing repository working depth and
pinned EXE/shared adapter; never overwrite these recorded outputs.

Required consumer changes after independent acceptance: preserve the
allocation-success premise in FABLE renderer/title initialization prose;
bind OPUS callback RDX size/pointer, alignment16, unused local R8, null
release/header-work distinction, and the conditional reserve tuple. Do not
promote request/capacity arithmetic into live allocation or lifetime proof.
Actual loaded module, natural allocation outcome, interference, reuse,
caller ownership, nonempty failure and opaque later calls remain open.

One local allocation obligation answered without gameplay. No new entire
runtime/OV row closed; prior four scoped historical source eliminations
are not counted again. Full L1+L2/M0-M5 goal ACTIVE/NOT_MET. Parked menu
allowance remains spent/unapproved; EXP127 remains invalid. All own scripts
terminal; no game/PC/instrument/save/config/reference/peer mutation.
