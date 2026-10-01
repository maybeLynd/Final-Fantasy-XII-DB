# SECTION-09 — owner initialization, arming, allocation and terminal queue composition

Date: 2026-09-23. **Local production complete and validated; formal independent acceptance pending.**
Apply Update09 AFTER Updates01–08 to `FFXII TZA(20260922-211246).zip`.
This is an incremental changed-files production overlay, not a numbered EXP or an L2 ruling.

## 1. Scope and reason for this work

SECTION-08 established owner deletion/completion and borrowed views but did not execute the full
allocation/request-selection producer. This section executes that original producer, its original
initializers/arming/providers and actual allocation failure. It then connects real queued requests
to the original pump's terminal behavior without pretending the OS read has occurred.

The main result is a separation of owner state, production-mask bit, queue slot and backing-handle
lifetime. A latched bit does not rearm state0. State1 does not submit merely when a hold flag clears.
A queue request can retire without an owner callback. Numeric handle equality is not a request ID.

## 2. Provenance and execution boundaries

Authorized EXE SHA-256:

`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`

The [manifest](original_body_manifest.json) pins **138 selected original bodies**. Complete recorded
ranges are decoded in [original disassembly](original_disassembly.txt). [Direct-call supports](direct_call_supports.tsv)
verify63 selected original call instructions. Historical Ghidra ranges are reused; no new Ghidra
import, GN162 population proof, complete indirect-call census or instruction-coverage percentage
is claimed. Range hashes establish byte identity, not which instructions every case reached.

The original code runs in a privately mapped image with the Microsoft x64 ABI and synthetic
arenas, owner records, metadata, actor slots, queue slots and plain TEST source headers.

| Boundary | Explicit treatment |
|---|---|
| Application0017D2E0 diagnostic formatter | Empty destination and invocation counter; formatting/error display not validated. |
| IAT008C2A60 memset | Host MS-ABI adapter; original thunk remains. |
| IAT008C2A68 memcpy | Host MS-ABI adapter for non-overlap only; overlap rejects the fixture. |
| IAT008C2F70 strncpy | Bounded host adapter; original selected matching logic remains. |
| GS/stack probe | Minimal synthetic stack-limit environment, not Windows loader/observer state. |
| Group metadata/modes/ActorManagerSlot flags | Fixture values supplied to the ORIGINAL providers; not retained live-game observations. |
| Terminal pump boundary | The original producer creates the request. Fixture sets queued state3/status0215EFF4; original poll/status helpers, whole pump, callbacks, cancel and recycle run. No read issuance or actual IO. |
| Common pump services | Original code, configured idle/empty branches; not all service behavior. |
| Cleanup after error controls | Explicit fixture queue reset/source release after observing the result; not evidence of normal higher recovery. |

No owner, provider, allocator, queue requester, terminal pump, completion, cancellation, bank
matcher or source free is replaced with a success/no-op application stub. Plain headers avoid
claiming the specialized authored PRF/EFX branch. Full frame caller002E65A0 and selected arming
caller003492A0 are read statically, not executed as sessions.

## 3. Established claim groups

**P09-1 — original reset and arm footprints.**003DD7E0 resets all80 records and five masks;
003DD790 resets one group. Handle/state/route clear; group+0C and slot+0E are assigned; annotation+8
and request arguments+10..1B survive.003DDA20 accepts only state0 and stores its third argument,
state2 and the pending bit. This is not a destruction proof or semantic identification of every
annotation consumer. The record is still SIGNATURE RESOLVED.

**P09-2 — pending is not sufficient for production or retry.** The full003DD4C0 requires both
state2 and its bit. Disabled/negative selection, inactive/nonpositive length and allocation failure
leave state0 with the bit retained. Fixing the condition and rerunning the producer alone does
nothing; the original armer is required and can successfully rearm0. The pending-record common tail
also overwrites route, including on non2 skips. It is not a permanent allocation-identity receipt.

**P09-3 — concrete provider mapping.** Group0 maps to kind5/index3*selector; groups1..3 map to
kind8/index4*selector. The producer narrows to WORD and increments the index WORD before signed
submission. Length/offset come from separate DWORDs in eight-byte slot records. Group4 has a
mapping but its length provider returns-1, so its selected record returns0/pending in this path.
No whole-game dead-data claim follows. Readable metadata pointers and bounded indices are required.

**P09-4 — allocation choice, pinning and hold.** Mode2 plus ActorManagerSlot+17 mask40 permits
arena11 first; failure/default uses arena6. Mode override makes the original mode getter return4,
skipping arena11. Actual exhausted arenas are used, not allocation stubs. Stack restoration and
allocation route are checked. Source acquisition pins separately from allocation reclassification
to1. ActorManagerSlot+201 holds a source in1 without queueing; otherwise it submits and records3.
Either consumes the bit. Clearing hold later does not submit1 through this sweep. Deleting an
armed2 does not cancel it; the producer still processes it.

**P09-5 — constrained capacity and same-call work.** All80 records are armed. The same original
producer queues32 requests with32 fixture handles and64 with128 handles; group4 rejects length.
Byte capacity remains available in the32 case. The original failing tagged-allocation path
releases provisional raw backing, and successful request order is group/slot FIFO. These numbers
are fixture capacities, not a new declaration of native arena configuration or per-frame budget.

**P09-6 — original queue retirement is not owner notification.** Pending status retains3.
Success dispatches original completion then recycles the queue slot, publishing the owner4 and
unpinning. Positive-count service error or actual queue cancellation retires the queue without
calling this owner completion, leaving owner3, its source pin and no bank entry. Producer bit is
already clear; running the producer does not recreate the request. A following owner delete
selects5 with no remaining callback in the fixture. Actual outer recovery remains open; no shipped
permanent leak/stall or real IO completion is inferred.

**P09-7 — rejected submission and identity reuse are distinct.** A large synthetic selector
narrows to signed request index0x8001. Requester rejects but the owner becomes3 and consumes its
bit; delete then selects5. In a separate valid completion/free/rearm sequence the source's exact
numeric handle is reused and the callback again names the same static owner. Equality cannot prove
a new request token. Delivery uniqueness, actual producer bounds and stale-callback reachability
are not established.

## 4. Validation and impacted falsification

**190/190 named original-instruction assertions pass**, with an identical separate-process repeat.
Some assertions summarize many records; this is not190 distinct game states or full path coverage.
Ten private-image instruction variants each fail exactly the intended first assertion:

| Variant | Required discriminator |
|---|---|
| Initialize only four groups | All80 initialized identity/state/route records. |
| Arm state1 rather than2 | Armer must enter2. |
| Do not consume production bit | Successful group0 pending bit clears. |
| Skip index increment | Mapped file index includes low-WORD+1. |
| Use length accessor for offset | Offset must match independent metadata value. |
| Resolve without pin | Source must be excluded from movable membership. |
| Replace preferred arena11 with6 | Actual arena identity must match the qualifying route. |
| Ignore hold gate | State1 retained without any queue entry. |
| Dispatch success callback for positive errors | Error-retired request must leave owner3 in this tested chain. |
| Sweep only fifteen entries | The selected sixteenth owner must submit. |

Only impacted mutations run. All binaries live in temporary build locations and are omitted from
this overlay. The original executable is hash-checked before and after; no instructions on disk
are patched.

A development expectation that a new allocation must use a new numeric handle was refuted; the
final control records the observed equality rather than forcing a false identity assertion. A
second development fixture expected64 requests with an arena configured for32 handles. Explicit
32/128-capacity controls corrected that mistaken assumption and now distinguish byte capacity
from handle capacity. Neither fixture mistake is called an FF12 defect.

## 5. Canonical changes and acceptance

Six existing files change: ownership contract, queue contract, the Section08 owner/view mechanism,
the two type stores and the external continuation handoff. One new mechanism page specifies the
producer-to-terminal-pump path. Only IndexedExternalSourceRequest changes in the stores: one type
row remains one; its nine fields become ten by resolving the writer/identity split in+8..+0F.
Every unrelated TSV line remains byte-identical. The annotation's downstream meaning remains open,
and no whole-type readiness is promoted.

The new mechanism remains PARTIAL. Historical source evidence and audit receipts remain historical;
TEAM claims, L2 verdicts, global dashboards, old experiments and reconstruction are untouched.
Local passing tests do not award independent acceptance or close another agent's task.

Still required: actual read/status production and higher error recovery, the held-state1 dispatcher,
metadata/caller reachability and lifetime, callback single-delivery/reuse, specialized nonempty
resource consumers and relevant scheduling. The original Windows overlap-copy behavior from07
is not answered here. The next substantive section is nonempty PRF/@FEF registration/specialized
lifetime, or a concrete remaining caller recovery path if original evidence exposes it.

## 6. Reproduction and installation

From this evidence directory on Linux x86-64 with Python3.10+ and GCC:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

The output must not exist. The driver rejects incompatible image/body hashes, compiler warnings,
unexpected faults, differing repeats or the wrong mutation failure. Nothing is downloaded. This is
not Windows/game deployment. Optional content checking additionally uses PyYAML, but installation
requires no user commands.

Apply the overlay AFTER Updates01–08. Merge its FFXII TZA folder into the parent containing the
existing FFXII TZA directory; do not nest it or delete/replace the whole database. Back up touched
files and merge any newer local edits. The optional read-only preflight is:

```sh
python verify_overlay.py --target '/path/to/FFXII TZA'
```

## Evidence index

- [Original bodies](original_body_manifest.json), [disassembly](original_disassembly.txt), [selected call supports](direct_call_supports.tsv)
- [Native source](native_controls.c), [driver](run_review.py), [mutation plan](variant_plan.json)
- [Summary](results/summary.json), [body checks](results/body_verification.json), [baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [mutants](results/code_mutations.json)
- [Claim matrix](claim_matrix.tsv), [canonical row changes](canonical_row_changes.json), [canonical preimages](canonical_preimages.json), [exact diff](canonical_changes.diff)
- [Content checker](validate_content.py), [content checks](results/content_validation.json), [overlay checks](results/overlay_checker_controls.json), [unchanged-file checks](results/unchanged_files.json)
- [Delivery verification](results/delivery_validation.json), [input chain](source_inputs.json), [patch manifest](PATCH_MANIFEST.json), [read-only preflight](verify_overlay.py)
