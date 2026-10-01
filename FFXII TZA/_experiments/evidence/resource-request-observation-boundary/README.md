# Resource requests: alignment correction and observation boundaries

ASTRA, 2026-09-21. Method **A: verified original instructions and prior artifacts**.
No game session, simulated input, memory write, injected call or isolated-code run.
Consumer: FABLE resource/FST semantics; OPUS queue contract and slot types;
SWE2-FRONTIER preparation of any remaining live reachability question.

## Question and method

`FABLE-REQ-ASTRA-KIND-INDEX-TRACE` proposes logging three entry points during a broad
play route to decide which resource families are used. Before capture, distinguish:
size query, rejected request, completed queue record, issued read, callback, and
delivered/used resource. Is a kind/index tuple even the correct ABI for all three?

The original functions already distinguish these hypotheses. Inspect their complete
bodies and reuse retained EO3 bytes; do not pay for a broad trace whose interpretation
is wrong. This also exposes two prose errors and a census coverage limitation.
Normal caller reachability and resource use still require their own evidence.

## Reference and controls

Reference `Database/Tools/work/exe/FFXII_TZA.exe`, SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, preferred image
base `0x120000`; Capstone version recorded in `observation.json`. Addresses below
are preferred-image VAs, not an assumed live module base.

`check.py` verifies the full executable hash, complete body decoding, exact instruction
anchors, and byte equality to already retained EO3 bodies where available. It compares
its full result with `observation.json`; altered/empty/truncated observations cannot
pass. The earlier draft is retained as `observation-initial.json` (39 anchors); the
final observation adds three slot-identity/write anchors (42). Five complete bodies:
`0032E400` (80 bytes), `0032E620` (340), `0032E7C0` (173), `0032E870` (285),
`0032E070` (605). The last three reuse prior EO3 bytes, not repeat execution.

Arithmetic controls include aligned and nonaligned positive/negative inputs, zero,
and signed endpoints. These 15 examples are **calculations of the shown instructions**,
not emulator or live results. The complete control flow is retained to inspect the
register provenance and intervening instructions rather than infer meaning from an
isolated mask. An unconditional positive bias, intervening EAX/EDX overwrite before
the addition, or a different source for the stored field would refute our reading;
none occurs on the shown builder sequence. The chunked initial rewrite is checked
separately. No negative reachability claim is made from an empty trace.

## Established corrections

### Initial offset truncates toward zero, not upward

`0032E870` reads the supplied descriptor's offset at `0032E8DB`. At `0032E8FB`:

```text
cdq                      ; EDX = sign mask of the 32-bit EAX offset
and edx, 0x7ff           ; bias = 0 for nonnegative, 2047 for negative
...                      ; index store / RBP restoration do not change EAX/EDX
add eax, edx             ; 0032E90B
...                      ; later counter load changes EDX after the addition
and eax, 0xfffff800      ; 0032E913
mov [r10+0x2c], eax      ; 0032E918
```

The signed value truncates toward zero to a multiple of `0x800`. For ordinary positive
values this rounds **down**: `0x801 -> 0x800`, not `0x1000`; `0x7FF -> 0`.
For negative values, `-0x801 -> -0x800`, `-1 -> 0`. Aligned values are unchanged.
The chunked initial rewrite at `0032E721..0032E735` has the same operation.
No assertion is made that arbitrary negative/nonaligned offsets occur in gameplay.

This contradicts the queue contract's field row and invariant I6 and the queue page's
initial-builder/layout wording. The page's **later chunk-requeue DOWN correction**
(EXP128) and the type table's requeue description are already correct; preserve them.
File-size rounding upward to **64 bytes** in `0032E400` is a distinct operation.

### Byte count and offset are different fields

`0032E88A` copies R9D (bytes) to ESI; `0032E92C` stores it to slot **+0x28**.
The descriptor offset becomes **+0x2C**, as above. The FST page's statement that the
size becomes +0x2C is stale propagation. The existing type rows +0x28/+0x2C already
distinguish the fields; this is not a new field discovery or permission to replace
their full meanings.

### +0x5C has an observed original-code writer

`0032E8C9` calls slot allocator `0032E990`; `0032E8D3` copies its RAX to R10.
No intervening call replaces this base before **`0032E974: mov dword [r10+0x5c],0`**.
The queue page already records this zeroing. The type table's `unobservedSpan005C`
is based on a census seeded only with the pump/callback/cancel/release functions;
its header excludes `0032E870`. Thus “not in this cleaned census” remains a scoped
true report, but is insufficient evidence for a globally unobserved span. Preserve
the known four-byte zero write, with semantic purpose/readers still open. Do not
infer a flag, counter, or padding role. No receiver-census algorithm failure is
established merely by an intentionally absent seed.

## Entry does not mean loaded

| Boundary | Original evidence | What a future observer must distinguish |
|---|---|---|
| Size query `0032E400` | No queue acceptance. `0032E41F` compares full RDX to `0x400`; `0032E428` indexes with full RDX. Kind FF returns -1 at `0032E438`. | Preserve raw RDX as well as low EDX; do not silently merge upper-bit differences. This does not declare every caller's source type 64-bit. |
| Indexed entry `0032E620` | Current selector/index globals are written at `0032E634/63D` before signed EDX gate `0032E64A/64C`. Negative returns -1 at `0032E64E/651` without building a slot. | Entry/global changes are requests attempted, not accepted records. |
| Named entry `0032E7C0` | RCX is a path, RDX destination, R8D bytes, R9 descriptor (`0032E7DA..7E8`). It copies the path and passes FF/low pointer to `0032E870` at `0032E833..84D`. | Raw RCX/RDX tuples are not numeric kind/index. Preserve path bytes and identity at the correct boundary, as the existing EO3 package specifies. |
| Completed record | `0032E870` fills kind +21, index +24, bytes +28, offset +2C, request ID +64; completed-record boundary precedes the epilogue at `0032E983`. | Correlate slot, request ID, thread, phase and trigger; account for reuse/wrap. A completed request can still have zero bytes. |
| Pump issue | `0032E0CA/0CE/0D1` reads/tests +28 and branches to `0032E130` on zero. That branch calls done helper `0032E330` and release `0032EC40` without traversing the read issuer. | Accepted -> callback does not alone establish file I/O. Observe matched issuer and actual delivery/use appropriate to the claim. |

The retained [EO3 package](../eo3-pointer-observation-preflight/README.md) already
provides pointer truncation and phase boundaries. This package does not repeat its
historical crash hypothesis or claim a new live cause.

## Live remainder and acceptance criteria

The broad route is **not a prepared live experiment**. Return it for one named family
and canonical consumer, an exact save/area/trigger, an expected positive request,
validated observer and finite event budget. Competing explanations should be such as
“this trigger queries size only” versus “it constructs/issues this specific request”,
not “a finite session proves a resource is never used anywhere.”

Before a run, require relocated object/function identity, pre-trigger baseline,
separate registration/acceptance/issue/delivery observations, matching identity across
phases, and health checks with normal responsiveness/fatal-dialog checks. A missed
positive control, lost correlation, exhausted budget or unhealthy session invalidates
the corresponding conclusion. A no-hit on the target is at most a bounded negative
in the controlled trigger. Use the existing backup/restore and validated observer;
do not reuse the unchanged EXP127 setup. Name the read/trace budget and stop/cleanup
sequence in that prepared request, not by inventing defaults here.

## Canonical propagation and limits

`consumer-state.json` pins the affected source excerpts, source hashes and census
header at diagnosis time; later peer edits need not match those historical hashes.
FABLE owns the queue/FST prose; OPUS owns contract/types/census disposition. Their
returns remain pending until they consume or rebut the evidence and propagate to any
dependent executable specification/probe. Independent exact-behavior review is routed
to SWE2-AUDIT-SPEC, followed by owner adjudication for the contract/type correction.

This package establishes original-code structure and arithmetic, not real scheduling,
allocator placement, delivery of a particular resource, runtime pointers, caller
population, disk contents or presentation. No reconstruction phase started.
FF12 was absent at preparation; no @runtime or PC control acquired, no saves/config/
reference files written. This is a static package, so no detach/restoration was needed.

Reproduce read-only from the repository root:

```powershell
.\Collaboration\Tools\analysis\venv\Scripts\python.exe 'Database/FFXII TZA/_experiments/evidence/resource-request-observation-boundary/check.py'
```
