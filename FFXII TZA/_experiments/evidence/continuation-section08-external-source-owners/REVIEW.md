# SECTION-08 — external source owners, completion/deletion, and borrowed-view lifetime

Date: 2026-09-23. **Local production complete and validated; formal independent acceptance pending.**
Apply Update08 after Updates01–07 to `FFXII TZA(20260922-211246).zip`.
This is a changed-files production overlay, not a new EXP number, fresh game observation, or L2 ruling.

## 1. Scope and original identity

The owner, request slot, resource entry, tagged source, effect ticket and acquired view are separate
objects. This section follows an actual external owner through submission, completion, deferred
deletion and source release, then follows concrete view acquisition and movement exclusion.

The authorized EXE SHA-256 is:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

[Original-body manifest](original_body_manifest.json) pins **120 selected bodies** against that
image. Complete recorded ranges are decoded in [the disassembly](original_disassembly.txt).
Historical Ghidra exports are reused; no new Ghidra import, current GN162 certification or
whole-function instruction-coverage measurement is claimed. [Direct-call supports](direct_call_supports.tsv)
verify fifteen selected historical xrefs at the actual original instruction. This is not an
exhaustive indirect-call census. [Source identities](source_inputs.json) pin the delivery chain.

## 2. What really executes, and what does not

The native fixture maps a private copy of the game at its preferred base and calls original code
using the Microsoft x64 ABI. Synthetic arena backing, owner records, queue slots, bank pages and
payloads define the input. Actual allocation/free, tree/movement, selected context/ticket cleanup,
queue requester, completion/error helpers, external-owner operations and plain-header registration
execute. An arena free is not release of the OS mapping that contains the synthetic arena.

| Boundary | Explicit treatment |
|---|---|
| Application `0017D2E0` diagnostic formatter | Writes an empty destination and increments a counter; formatting and error display are not validated. |
| IAT `008C2A60` | Host memset adapter; original imported thunk remains. |
| IAT `008C2A68` | Host memcpy adapter for NON-OVERLAP only; observes membership at the actual copy boundary. It rejects overlap. |
| IAT `008C2F70` | Bounded strncpy adapter; original name-comparison code remains. |
| Stack-limit environment | Minimal synthetic GS-backed state for the original stack probe, not Windows loader/observer behavior. |
| Completion | Direct original callback calls or the ORIGINAL queue completion/error helper; no OS IO or full queue pump. |
| Queue cleanup | Explicit fixture reinitialization after observations; not a claim of normal cancellation or recycling. |
| Payload | Plain TEST source plus a default-subtype EFX payload. No complete nonempty PRF/@FEF or specialized rendering branch. |
| `003DD4C0`, `0041FCF0`, `005371C0` | Whole original bodies inspected statically; not whole-function executed by the fixture. |

No bank matcher, registry allocator, owner completion/delete, queue helper, context destructor,
source free, membership operation or compactor is replaced with a success stub. Negative indices,
zero bank capacity, duplicate owners and nested views are discriminating synthetic controls, not
claims that ordinary loaded gameplay reaches those exact states.

## 3. Established claim groups

### O08-1: a specific external owner and state-based publication

The fixed owner table is `02B581A0 + (group*16+index)*0x1C`. The production sweep covers five
sixteen-entry groups. The indexed helpers do not validate arbitrary indices. A new structural
declaration records the handle, state, route byte and request arguments, while preserving two
unassigned spans. Static `003DD4C0` shows allocation and pinning before submit; the full producer
and the table's one-time initialization are not executed or declared completely understood.

`003DD740` returns the handle only for state4. That is a state test, not an allocation or bank check.

### O08-2: deletion during loading is deferred, not queue cancellation

`003DDA70` builds a real request with completion `003DD850`, null cancellation callback, and the
LOW32 owner-record address as argument. It writes state3 regardless of the requester's return.
State3 deletion through `003DD420` changes only the state to5; source, pin and queued callback
remain. Original `0032E330` then dispatches the owner callback and completes the pending deletion.
The completion helper does not itself recycle the queue slot.

The positive-length `0032E370` error path does not call that owner completion. This local result
does not establish the full service/recovery policy. A synthetic rejected negative index still
leaves owner state3 despite no pending queue request; normal producer reachability is not inferred.

### O08-3: completion and direct deletion clear different bytes

Completion `003DD850` unpins first. State5 then calls external disposal and source free, and clears
ONLY state+4. The freed handle and route byte remain numerically present. Direct state1/state4
deletion clears handle+state together and route+0D. Lookup hides the stale state0 value.

Original `003DD380` handles all sixteen records in one group: controls include the last slot and
an intact next-group owner. Unrelated bytes survive. A shortened-loop mutant fails the last-slot
check, not an unrelated incidental assertion.

### O08-4: ready does not prove registration, and reuse is not replacement

For completion outside state5, registration returns are ignored before writing state4. A
zero-capacity bank therefore has no entry while the owner reports state4. Plain TEST-header
new-entry registration otherwise creates a real mode1 row. Two distinct sources with the same
tag/name leave one entry holding the FIRST handle/cache, while both owners reach state4.
Deleting the second frees only its backing; deleting the first removes its entry and source.

These cases separate completed-owner publication, registry admission and replacement. They do
not implement a shared reference count or prove safe multiple-reader lifetime in loaded FF12.

### O08-5: the original owner's disposal orders consumers before backing

`0041E490` acquires then releases BEFORE the bank disposal tail call. It passes the original
representation, not the resolved pointer. The mode1 predicate compares entry+30. Raw-pointer
and tagged-handle controls therefore take different match outcomes.

Entry disposal alone does not free mode1 backing. The owner separately frees it afterward through
`00369800`. With a real attached context, cancellation releases context/tables before the source
allocation is reclaimed. Complementary render-reference sweeps can both fire across the full
chain. A development expectation that the raw-valued pair would survive was corrected after
following the second sweep; the final test asserts the actual whole-chain clearing, not the
incorrect single-sweep extrapolation.

### O08-6: a real consumer pin excludes movement, but is not independently nestable

Mode1 view `00409960` finds a section then pins its source; `00409C00` releases it. A failed lookup
acquires nothing. Original compaction cannot move the tested pinned allocation, but a single end
after TWO acquisitions restores eligibility and the next compaction moves it. The entry cache is
stale until a guarded lookup under `02B62E10` updates it; the next view returns the new base.

Copy-mode `00409A60` pins at the actual import-copy boundary and unpins afterward, even when a
caller had already pinned. Mode1 setup does not pin. Static consumer `0041FCF0` brackets its raw
view with these original calls, but the full consumer and its callees are not executed here.
Neither this bracket nor the deletion wrapper's brief pin proves arbitrary reentrancy/thread safety.

## 4. Validation and falsification

**116/116 named original-instruction assertions pass**, with an identical independent process
repeat. These are assertions over controlled states, not116 distinct game systems or full branch
coverage. The following nine private-image variants each fail exactly their intended assertion:

| Variant | Required discriminator |
|---|---|
| Copy without acquiring | Source must be pinned at actual copy-import entry. |
| View without acquiring | Successful view must remove movement membership. |
| Skip cache publication | The post-move lookup must update entry cache. |
| Compare cache instead of representation | Tagged owner deletion must match and remove its row. |
| Skip completion unpin | Normal completion must return source to movable membership. |
| Discard in-flight delete | Deletion must select state5 while request remains pending. |
| Erase cancelled handle | Deferred completion must preserve old handle bytes. |
| Submission claims ready | Original submission must write state3, not4. |
| Skip last bulk slot | Group delete must process the sixteenth record. |

Only affected mutations run. The authorized file is hashed before and after. Compilation uses
strict warnings-as-errors; all binaries are temporary and omitted from the overlay. An identical
repeat is a stability check, not another set of distinct research results.

## 5. Canonical changes and status

Seven existing files change: three resource contracts, the previous ownership mechanism, both
type stores and the continuation handoff. A new mechanism page describes the full bounded owner
and view lifecycle. The type stores gain ONE type and NINE fields; all pre-existing rows remain
byte-identical. The new type is SIGNATURE RESOLVED, not self-certified TYPE RESOLVED. Unassigned
bytes remain UNKNOWN. Layout completeness is not semantic completeness.

Historical experiments/raw results, Updates01–07 evidence, TEAM claims, L2 verdicts, global
completion surfaces, original EXE and reconstruction are unchanged. Prior audit metadata remains
historical; local passing controls are not formal independent acceptance.

## 6. Remaining obligations and next work

Full `003DD4C0` service-selection/retry behavior, queue IO/error recovery, callback-owner reuse
preconditions, other external-owner families, full consumer reentrancy and nonempty PRF/@FEF
registration remain open. The Windows copy-overlap dependency from SECTION-07 is not answered by
this fixture. Do not reinterpret a local pin, a stable handle or owner state4 as universal safety.

The next substantial section should address original producer/recovery or the nonempty authored
registration path and its specialized consumers—not repeat these completed owner controls.

## 7. Reproduction and installation

On Linux x86-64 with Python3.10+ and GCC, from this evidence directory:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

The output directory must not already exist. Wrong image/body bytes, compiler warnings, unexpected
faults, mismatching repeats or the wrong mutant failure reject reproduction. No game bytes,
dependencies or compiled files are distributed. The native driver uses only Python's standard
library and GCC. Optional content validation uses PyYAML, not required to copy the overlay.

Apply AFTER Updates01–07. Merge the ZIP's `FFXII TZA` folder into the parent containing the current
database. Back up matching files and merge newer edits rather than overwriting them. Do not delete
the existing folder or nest it inside itself. The optional preflight is read-only:

```sh
python verify_overlay.py --target '/path/to/FFXII TZA'
```

## Evidence index

- [Original bodies](original_body_manifest.json), [complete disassembly](original_disassembly.txt), [selected direct calls](direct_call_supports.tsv)
- [Native source](native_controls.c), [reproduction driver](run_review.py), [variant plan](variant_plan.json)
- [Summary](results/summary.json), [baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [variants](results/code_mutations.json)
- [Body identity](results/body_verification.json), [claim matrix](claim_matrix.tsv), [new type and rows](canonical_type_addition.json)
- [Canonical preimages](canonical_preimages.json), [exact diff](canonical_changes.diff), [source identities](source_inputs.json)
- [Content validation](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json), [unchanged-file check](results/unchanged_files.json)
- [Separate extraction and merge test](results/delivery_validation.json)
- [Content checker](validate_content.py), [patch manifest](PATCH_MANIFEST.json), [read-only preflight](verify_overlay.py)
