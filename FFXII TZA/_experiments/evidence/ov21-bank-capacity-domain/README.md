# OV-21: located bank initialization and failure discriminator

## Question and result

Does a zero-capacity registration fixture establish ordinary initialized bank
exhaustion? Does failure at `0040A1CC` identify a full bank?

No to both. Method A uses shipping bytes, local control flow and conditional
Windows x64 argument continuity. It does not execute FF12 instructions.

The located caller `0033263C` supplies ten groups to `0041E3A0`.
That initializer locally binds root `+D90` to itself, saves the group argument in
nonvolatile EBX and forwards it through `00409F10`. The wrapper supplies stride
`0x50` and shift 5. At `0051FAA6`, the constructor's local DWORD `+54` store is
`low32((1 << 5) * 10) = 320`; `320 * 0x50 = 0x6400` is arithmetic, not a
captured allocation size. These statements assume ordinary ABI, normal calls,
valid root/table/frame identities, disjoint tables and no interfering writes.
Opaque calls after that store have not been shown to preserve it. Dominance of
the store over a local normal return is not completed-startup state evidence.

Constructor `0051FA38` and reset `0051FB97` each clear eight bytes at `+50`,
including the four-byte capacity at `+54`. A writer search limited to stores
whose starting offset is `+54` omits these real overlapping stores.

Original allocator `0051FBB0` has separate immediate failure paths:

| Condition | Path | Result |
| --- | --- | --- |
| signed32 used `+58` >= signed32 capacity `+54` | `0051FBCA` -> `0051FBD5` | EAX FFFFFFFF, no helper call on this path |
| signed32 used < capacity, `0051F7A0` returns NULL | `0051FBE8` -> `0051FBF8` | EAX FFFFFFFF after the helper |

`0051F7A0` itself can locally return NULL after `0051F6B0` returns -1.
That opaque helper and feasibility of the combined initialized state are not
proved. This is not a claim that allocation fails physically or that normal
play can enter either path. The registration -1 outcome alone loses the
distinction between them.

## Evidence and reproducibility

`source-01.json` contains eight exact shipping-code ranges. `capture.py` invokes
the shared reviewed access-role adapter by default; it checks store, LEA and
read/modify/write controls in the actual path. The producer verifies capture
exit/result/exception status, source annotations, full reference hash, original
bytes, explicit local CFG and named external tails, required operations and
register continuity. Volatile carriers have no intervening opaque call; saved
EBX continuity across calls is explicitly an ABI premise.

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Tool/interpreter/dependency identities and raw stdout/stderr are retained in
the capture, proof and control receipts.

Run `run.py proof-new prove.py result-new.json` with the project's existing
Python environment. Outputs refuse overwrite. `result-03.json` and
`proof-03.*` are the current producer result. `control-01.*` records three actual
CLI refusals: failed capture, missing source, and a coherent same-size change
from boot groups 10 to 9 rejected against original bytes. These controls
exercise evidence validation; they are not FF12 executions or gameplay tests.

## Failed producer and correction

`proof-01` exited 1 before producing a semantic result: the local CFG omitted
the original final root-initializer tail at `0041E484 -> 005211F0`.
`prove-01-driver.py` preserves the failed invocation's exact driver. The repair
names this external boundary rather than dropping its branch or claiming to
analyze the callee. The body restores its frame before that tail. The callee's
native effects remain unknown. `proof-02` and `prove-02-driver.py` retain the
intermediate result; proof 03 adds an explicit volatile-call boundary check,
the original zero source for constructor clearing, signed comparison wording
and the narrower local-store/startup distinction. No failed run passes.

## Affected consumers and remaining discriminator

FABLE's external-source owner/lifetime page and OPUS's resource-bank contracts
should incorporate only the local capacity store, overlapping reset and
failure distinction after independent agreement. Existing isolated zero-bank
fixtures remain valid for their injected state. Their natural loaded-state
interpretation must remain open. No whole OV-21 closure is asserted.

Before any future real-process failure observation, prove the bank identity,
initialization/teardown phase, capacity `+54`, used `+58`, and whether the
`0051FBCA` or `0051FBE8` path ran. A positive known registration and healthy
observer/session are required. Recording only `0040A1CC` is insufficient.

Cheaper next work is the original backing/free-list invariant and authored
simultaneous key/owner bounds, if current ownership permits it. Actual completed
startup, other roots and bulk/alias writers, metadata consistency, callback
timing, teardown, same-key ownership and natural exhaustion remain unresolved.

## Cleanup and acceptance

No game, PC control, native harness, process instrumentation, saves, settings,
reference bytes or peer files were changed. All producer/control subprocesses
are finite and terminal. Source validity and manifest integrity are distinct
from independent acceptance and canonical incorporation. The full L1+L2 goal
remains ACTIVE and unfinished; the parked menu allowance remains spent and its
extension unapproved.
