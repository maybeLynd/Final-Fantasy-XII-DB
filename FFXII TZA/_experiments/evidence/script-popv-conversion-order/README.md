# POPV conversion precedes width saturation — 70

**Method B, isolated original instructions in disposable emulator state.** The
reference EXE SHA256 is `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The full retained POPV span is `00267E60..00267F60` (256B); only the selected
integer-kind post-resolve stage at `00267EF2` through stop `00267F1E`, with its
original tails `00267F4C..00267F60`, executes. Then an explicit second-entry ABI
intervention invokes the already-verified original `0026D530` store leaf and its
six-target table. This is **not full POPV, native CPU or live-game execution**.
No resolver or notification callback is stubbed; both are omitted at boundaries.

Question: does float assignment clamp the float directly, or convert to signed32
first, then saturate that dword by storage width? Static original code selects
the integer-kind stage when resolved record+4=1, stores the converted dword at
record+20, then reaches the notification gate and original store call `00267F37`.
That establishes local encoded ordering, not a normal gameplay caller observation.

Initialized state: depth1 with tag2=float32 or tag1=int32, explicit bit patterns,
resolved48B record, destination guards, stack/shadow layout and masked MXCSR1F80.
Each guest has a32-instruction conversion budget and64-instruction store budget.
No unexpected call/read/write or incomplete boundary exit is accepted. Raw evidence
separately records input, stage registration/execution, converted bits and store
effects; a successful emulator API call alone is insufficient.

| supplied input | original converted dword | u8 stored byte | s16 stored word |
|---|---|---|---|
| float32 1.75 (`3FE00000`) | `00000001` | `01` | not tested |
| largest float32 below2^31 (`4EFFFFFF`) | `7FFFFF80` | `FF` | `8000` |
| float32 +2^31 (`4F000000`) | `80000000` | `00` | `8001` |
| tag1 INT_MAX (`7FFFFFFF`) | raw `7FFFFFFF` | `FF` | not tested |
| empty stack, injected stale payload1.75 | zero | `00` | not tested |

The positive +2^31 float becomes the masked conversion's signed32 indefinite
value before storage. The store interprets that dword as negative: u8 clamps to0;
s16 clamps to the previously established unusual floor−32767, storing8001. A
real-number clamp directly applied to the float would produce different results.
Do not normalize this sequence in a reconstruction. The s16 signed-load view is
a separate established representation; PUSHV is not executed in this package.

A labelled private **CVTTSS2SI→CVTSS2SI** mutation under the same nearest-rounding
MXCSR makes1.75 convert to2 and store02, instead of original1/01. Visits prove
the actual changed opcode executed. The largest-below-boundary, integer-tag and
empty-stack paths provide controls; guards, record, stack sentinel and exact code/
table preservation are checked. Actual shared adapter invocation classifies the
value store and conversion load. Three checker faults reject direct float clamp,
round-instead-of-truncate, and accepting the private mutation as original.

Initial reader setup omitted module `__file__` during direct source execution and
failed **before image load, guest execution, raw or results**. Original helper and
failure metadata are retained. Corrected actual invocation supplies that namespace
precondition, without cache imports. A regression executes AST-selected statements
from the actual producer; default succeeds and omitting the assignment fails at
the original reader. No semantic conclusion depended on the failed setup.

Consumer: OPUS contract/spec and FABLE variable-storage prose must preserve kind
conversion before signed width saturation, masked boundary behavior and tested
values. DATA propagation and SPEC independent review remain pending. Do not extend
the result to callback effects before the store, actual bank initialization,
caller reachability, lifetime or valid shipped descriptor combinations.
The emulator's MXCSR status is recorded, **not native flag/exception parity**;
unmasked behavior is unproved. No general float-domain claim or live run.

All guests are disposable; no host native executable allocation, FF12 process,
PC control, save/configuration or reference binary change. S19 spent setup budget
and unapproved extension persist. Full L1+L2 DB_GOAL=NOT_MET.
