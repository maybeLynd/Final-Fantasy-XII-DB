# Prescribed gauge registration callbacks: event zero has a local return

For the player: creating/registering a stat bar does not start its animation
through these two prescribed callbacks at their registration event. Registration
itself initializes and stores fields; this result is about the callback it then
invokes, not about all effects of registration or when a gauge first appears.

**Method A / STATIC_ONLY. Producer and focused controls complete; independent
acceptance and canonical incorporation pending. No original-code or game run.**

Question: does the synchronous event-zero call in `003F89C0`, when its supplied
callback is `0029B7D0` or `0029B810`, reach animation/helper effects or return
locally? The competing stronger claim, "event zero does not read the receiver,"
is false. Both complete shipping bodies read QWORD `[view+0x48]` before testing
the event, even though neither follows that loaded context on the zero path.

| prescribed handler | event-zero path result | explicit nonstack access |
|---|---|---|
| `0029B7D0`, 50 bytes | EAX=0; entry-relative RSP restored before RET; EDX=0 | one 8-byte read at view+0x48 |
| `0029B810`, 82 bytes | EAX=0; entry-relative RSP restored before RET; EDX=0xFFFFFFFF | one 8-byte read at view+0x48 |

Neither selected path dereferences the context/payload, makes a call or performs
an explicit object write. Both use a 40-byte stack reservation and restore it.
RET's implicit return-address access remains a validity prerequisite. Volatile
registers and flags can change; this is not an all-register preservation claim.

Registration first stores the supplied callback at view+0x38 and context at
view+0x48. At its conditional non-NULL call, RCX=view, EDX=0 and R8=the supplied
payload. The earlier native fill and registration stores are outside this local
callback proof. A matched existing registration row can retain a different
callback; this result does not constrain arbitrary callbacks or prove the
actual row selected in a running game.

The accepted physical source was retained rather than recaptured. The producer
checks the shipping PE exception-directory entry, unique RUNTIME_FUNCTION roots,
unwind headers and full body bytes against EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `0x120000`. Handler body hashes are
`f8768931c40b9c4bebb13f0927b6684c82bc93bfe30cbc02d03e2b26de38af1b` and
`8ab5f6318f42bbd53381b192b700a1c6f9d026b0549e90991248b0f11e16603c`.
Original registration instruction bytes and complete retained annotations are
checked too. Memory roles come from the reviewed shared access-role adapter in
the actual normalization/tracing path, then the reviewed annotation validator.

Current [result-03.json](result-03.json),
[normalized-result-03.json](normalized-result-03.json) and
[proof-03.status.json](proof-03.status.json) contain the paths, exact identities,
source pins and real terminal/exit/exception status. The bounded interpreter
keeps payload/memory symbolic and event arithmetic concrete. It is a purpose
built static path analysis, not an emulator or execution of FF12 instructions.

Detection controls stop at the real primary event-one call to `002973E0` and
secondary event-two DWORD store at `0029B82C`. They prove detection of those
boundaries, not their transitive effects. Five actual CLI negative controls
reject failed upstream, incomplete extents, a changed unwind header, incomplete
registration source and a coherently changed source guard. Disposable path
mutations make event zero reach the call/write detectors; an unknown predicate
is refused. These source mutations are not native interventions or executions.

The first actual producer failed because it unsigned-masked a relative stack
offset; no semantic result was emitted. Its driver and failed receipt remain
immutable. Proof02 corrected the stack model; proof03 additionally checks the
full physical metadata and annotation prerequisites. The control reproduces
the old erroneous 2^64 return delta and verifies zero under the corrected model.
Those revisions are one repaired producer, not three scientific experiments.

Premises: intact shipping code, valid readable receiver+0x48, valid return stack,
normal private-frame ABI, the stated handler/event identity and noninterference.
No live receiver, initialization, allocation, lifetime, normal reachability,
event-one cost update, scheduling, first draw or visible consequence is proved.
An event-zero receiver read means an invalid receiver can still fault; local
return does not make this path pointer-safe for arbitrary inputs.

FABLE consumes the local registration-event boundary and its receiver-read
qualification on the OV42 owning page. OPUS consumes the conditional callback
contract, access footprint and volatile EDX distinction. Keep existing-row
callback identity and live-only scheduling/resource/lifetime questions OPEN.
Independent SPEC review must precede acceptance; producer controls, package
integrity and the earlier independent reviews remain separate.

Reproduce with the repository interpreter: `python -B prove.py <fresh-result>`.
`python -B control.py <fresh-directory>` requires the retained proof03 identity.
All children are finite and exited. No PC/game/attach/input/save/config/reference
or peer-process write occurred; there was no live session to restore or detach.
The full L1+L2 goal remains ACTIVE/NOT_MET. Menu budget is spent and its extension
unapproved; EXP127 remains invalid and K14 remains independently accepted closed.
