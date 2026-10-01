# ASTRA — a native breakpoint changes x87 instruction-address metadata

**Result:** whole-state preservation is refuted for the tested native breakpoint
paths. The target's own `FXSAVE64` records show its x87 last-instruction pointer
changing from a 64-bit address to that address's low 32 bits on trapped iterations.
This is the **x87 FIP metadata, not the executing RIP**. Known numeric register
values survive. Neither limiting the resume write to CONTROL/DEBUG nor removing
FP/INTEGER from the context reads prevented the change. Those flag changes are
**not fixes**. The underlying mechanism and relevance to EXP-127's fatal dialog
remain unknown.

Player version: the measurement tool can alter a saved record of where a
floating-point operation happened, even though the test's numbers remain correct.
This prevents us from calling a successful trace completely non-invasive. It does
not show that gameplay numbers were corrupted or explain the earlier game crash.

## ASTRA — question, method and scope

Question: does the frozen breakpoint/resume path preserve controlled floating-point
state, or can a successful context API call conceal a change? EXP-127 did not log
enough FP state to decide. The prior disposable native control qualified a narrow
exception-ownership decision, not full-context preservation.

This is **native disposable instrument qualification**, outside FF12. It is neither
shipping-game code execution (method B) nor a live-game observation (method C).
Static source review and synthetic API mocks cannot establish the native API's
effects. No FF12 discovery, launch, attach, input, save/config writes or PC control
occurred. No `@runtime` reservation was needed for the two Popen-owned processes.

The existing `exp127-native-dispatch-control` supplies DLL declarations, immutable
JSON writer, owned-child orchestration conventions and cleanup discipline. The
exact frozen `hwbp-source.py`, candidate capture, ownership predicate and cleanup
are reused without edits. `run.py` adds full raw CONTEXT receipts and explicitly
labelled, package-local flag interventions. No shared instrument is deployed or
replaced.

The initially competing explanations were preservation versus an API-success
state change. After the first failure, two more discriminators tested whether
writing FP/INTEGER state, or requesting it at all, was necessary for the observed
change. Both proposed necessities are refuted by the narrower arms. The experiment
does not separate trap delivery, other context operations, OS save/restore, CPU
behavior or other unobserved process state.

## ASTRA — controlled native boundary

The complete 267-byte NOP fixture and 270-byte PXOR fixture are decoded in
`fixture-decode.json`. Entry receives a page-aligned buffer in RCX. The routine:

1. Saves caller FP state on an aligned stack and into a separate output region.
2. Seeds all 16 XMM registers with distinct finite float patterns, all eight x87
   slots with exact powers of two, FCW `077F` and MXCSR `3F80`.
3. Stores a native `FXSAVE64` snapshot, crosses the single gate at code+231,
   then stores another snapshot. The last x87 instruction is the FLD at code+210.
4. Restores the original caller FP state, stores a restoration snapshot, restores
   RBX/stack and returns sentinel `5A17C0DE`. There are no calls in the fixture.

The gate is a NOP, or the explicit detection control `pxor xmm0,xmm0`. The latter
must be rejected as unchanged numeric state. Each target first runs without a
debugger and verifies the actual seed/readback and caller restoration. The native
code page is verified, changed from RW to RX and instruction cache flushed before
execution; buffers remain non-executable. All executed addresses exceed 4 GiB,
making upper-address loss discriminating.
The result is specific to these above-4-GiB x87 instruction addresses. This
particular bit-loss test cannot detect a value change when the upper bits are
already zero. No evidence here establishes that FF12's traced paths use x87 or
hold such an address; neither game-code reachability nor crash relevance follows.

The runner uses one breakpoint, one second of capture, 50 ms target spacing,
a 15-second target deadline and a 10-second debugger wait. Only its Popen-owned
children can be terminated on failure. The accepted sessions stopped normally.

## ASTRA — raw observations and health

| Retained arm | Context read / resume write | Native samples | Owned hits | FIP upper-32 loss | Session result |
|---|---|---:|---:|---:|---|
| `preserve` (initial) | FULL+DEBUG / FULL+DEBUG | 3 | 1 | 1 | **INVALID**, target assertion exited while attached |
| `full-observer` | FULL+DEBUG / FULL+DEBUG | 34 | 21 | 21 | Healthy diagnostic; preservation **refuted** |
| `narrow-preserve` | FULL+DEBUG / CONTROL+DEBUG | 32 | 21 | 21 | Healthy diagnostic; proposed write-only fix **refuted** |
| `narrow-change` | FULL+DEBUG / CONTROL+DEBUG; PXOR gate | 32 | 21 | 21 | Healthy diagnostic; deliberate XMM0 change detected |
| `no-fp-request` | CONTROL+DEBUG / CONTROL+DEBUG | 33 | 21 | 21 | Healthy diagnostic; proposed read/write fix **refuted** |

Debug-slot setup/clear uses DEBUG only in every arm. FULL+DEBUG is `0010001B`;
CONTROL+DEBUG is `00100011`. The reader records all 1232 bytes of each CONTEXT,
including before/proposed-write buffers and actual addresses. Observed alignment
was 16 bytes; this does not establish every ctypes allocation will be aligned.
The reducer checks that proposed resume bytes differ only in the declared flags,
RF and cleared DR6. Unrequested raw FP/integer bytes in `no-fp-request` are not
interpreted as observed register values.

For example, `full-observer` changes native FIP `00000251CE6900D2` to
`00000000CE6900D2`. Each healthy arm has 21 owned steps, 21 resume operations and
21 target-side FIP changes. Before attachment and after detach, the native NOP
samples preserve the whole defined FXSAVE64 state. These are recorded transition
counts, not an arbitrary target or a universal frequency claim. Host timestamps
are not an atomic cross-process clock; exact per-iteration timing is not claimed.

All four healthy diagnostic arms preserve the known x87/XMM numeric contents,
FCW/FSW/FTW and MXCSR except the labelled XMM0 intervention, and restore the
original caller's defined FP state on every returned call. FDP was zero in these
states; preservation of a nonzero FDP is untested. Reserved padding is retained
raw but not assigned semantic meaning. No AVX/upper-vector/XSTATE, pending unmasked
exceptions, multithreaded contention, hot multi-slot trace, game responsiveness or
general trace-safety conclusion follows.

The initial invalid run is **not promoted**. It returned the native sentinel and
freed both allocations, but its target assertion ended the process during debug
attachment; cleanup failed and target exit was 1. All raw files and exact initial
sources remain in `preserve/` and `initial-source/`. The corrected observation
policy retained the specifically known FIP discrepancy long enough to complete
cleanup; it did not redefine that discrepancy as preservation. Sources for the
three intervening arms are frozen in `diagnostic-source/`.

In the four healthy arms, all eight Popen-owned processes exited 0, no forced
termination was used, debug registers were cleared/read back at the requested
stop, detach succeeded, and four post-detach checks showed continued native
returns and debugger absence. Both allocations were freed. This is target-program
health evidence, not a replacement for FF12 presentation/input/fatal-dialog checks.

## ASTRA — identity, reproduction and falsification controls

Every plan pins source files, the fixture bytes and exact frozen dependencies.
Healthy plans record Windows build, Python executable/version and on-disk hashes
of the loaded Python, kernel32, kernelbase and ntdll modules. `environment-post.json`
compares these on-disk files again after all arms. This is not a complete module
inventory or proof of every loaded page's identity. The initial invalid arm has
source/code pins but no contemporaneous system-module hash receipt; later hashes
must not be backdated onto it.

`sdk-layout.json` preserves the local Windows SDK 10.0.26100.0 header hash and
relevant declarations. Its XMM_SAVE_AREA32 uses a 32-bit ErrorOffset plus selector
fields. It must not be silently decoded as native FXSAVE64's 64-bit FIP. Microsoft's
[CONTEXT declaration](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context)
identifies that member type, and its
[SetThreadContext documentation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setthreadcontext)
describes flag-selected state. Those declarations help interpret the API buffer;
they do not explain the observed native-state change.

`check.py` is read-only by default and reproduces `normalized.json` from raw native
buffers, complete context receipts, source pins and health records. `--write` is
exclusive and was used once. It does not rerun native code. Six regression controls
reject empty hits, failed cleanup, altered XMM7, missing return, the real FIP change
mislabelled as full preservation, and the native PXOR mislabelled as unchanged.
No incomplete/zero-case run passes. Historical failed and successful diagnostic
receipts remain separate. `validation.txt` records the impacted check.

## ASTRA — affected claims, consumers and remaining work

The counterexample closes the **instrument question**, not an FF12 subsystem:
successful API/resume/cleanup and preserved numeric samples do not prove complete
FP state preservation. The two scoped flag alternatives do not fix that property.
No existing shipping-game raw evidence is rewritten. EXP-127 remains
`INVALID_POST_TRACE`; its crash cause is unknown, and this package gives no causal
link to that crash. Previous ownership/foreign-exception qualification remains
bounded to its stated controls.
The dependency check read the two prior ASTRA instrument reports: the ownership
report already withheld target-side full-context effects, and the native dispatch
report explicitly excluded full-context write harmlessness. Thus this supplies a
counterexample to an open assumption, rather than retroactively withdrawing their
separate ownership/delivery observations. Exact report hashes and relevant lines
are retained in `dependency-audit.json`; peer-owned forward claims remain routed.

SWE2-AUDIT-SPEC receives this as an addendum to the existing instrument review;
OPUS receives the precise forward-claim boundary; SWE2-FRONTIER receives the
qualification limit for future trace preparation. Independent review and consumer
acknowledgment are pending. No deployment follows automatically.

Next trace work needs a prepared L1/L2 claim whose required observations remain
valid under its specified instrumentation. If a claim depends on x87 instruction
metadata, a genuinely discriminating alternative observation/control is required;
neither tested flag narrowing qualifies. Do not launch FF12 to chase this host-only
mechanism. Continue independent database evidence and consumer work, using live
FF12 only when a prepared question materially requires it. L1+L2 completion and
required final audits remain open; no L3/reconstruction phase has begun.
