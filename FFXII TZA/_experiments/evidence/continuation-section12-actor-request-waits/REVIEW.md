# SECTION-12 — actor request arming, start/return notification and non-kind-1 waits

Date: 2026-09-24. **Local production complete and validated; required independent acceptance pending.**
Base: `FFXII TZA(20260923-205605).zip` plus Update11. This is a changed-files database overlay,
not a new globally numbered experiment, current Ghidra import, L2 ruling or reconstructed subsystem.

## 1. What this section adds

Update11 connected the interpreter to real native-command callbacks for selected runnable requests.
This section adds original cross-actor request submission, entry admission, channel selection,
start/return notification, and the original wait-driver branches. It does not repeat the countdown
campaign or rebrand EXP-085/106's scripted boundaries as original execution.

The important distinction is between request mode, entry run state, wait kind, receipt identity and
capacity. A target can be selected before its script executes; it can start or return even when
its requester has no space for a notification. Completing a wait can run following bytecode in the
same driver invocation. These are different outcomes, not one atomic success condition.

## 2. Original identity and fixture boundaries

Original EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

[The original-body manifest](original_body_manifest.json) pins85 selected bodies and8 data spans.
Each range is verified against the uploaded executable. Historical Ghidra extents are reused and
decoded; body-hash agreement is not an instruction-coverage or current-population certificate.

The fixture runs in a separate Linux x86-64 process, privately maps the original image at00120000,
and calls the original instructions with GCC's Microsoft x64 ABI. Managers, two actors, bytecode,
function tables, value stacks, request arrays and wait-list buffers are synthetic inputs.

**Application-function substitutions: ZERO. Import bridges: ZERO. Planted command callbacks: ZERO.**
Original initializers, free/active/detached entry-list operations, the submission path, selection,
start, interpreter request opcodes/RET, notification helpers, wait predicates and full0025DF00 entry
execute. Setup supplies readable manager-image and idle-service state, not a game loader.

The full outer0025D9E0 frame pipeline, nonempty outer services, runtime actor allocation/reuse,
OS scheduling, actual authored script/resource lifetime, malformed-list safety and live game health
are not validated. A single representative for a branch class is not exhaustive opcode coverage.
No new live FF12 session or full historical Unicorn campaign is claimed.

## 3. Established claims

### A12-1 — the insertion-state gate belongs to the issuer

At002689F0/002689F7 the original00268850 tests issuer+02==1 and issuer+10==0 using R15.
RBX holds the resolved target. The previous page incorrectly attributed those fields to the target.
Contradictory actor values discriminate the identities; the targeted wrong-receiver variant fails.

The immediate insertion path promotes/reselects only when target and issuer differ. Another higher
priority entry can be selected ahead of the newly inserted lower-priority entry. Reserved-bit
rejection happens before target lookup; a later capacity refusal already updates the saved caller
continuation and can decrement target+10. These failures are not interchangeable no-op returns.
A missing target pointer is not certified as safe: that untested case remains outside the fixture.

### A12-2 — admission, channel selection and run state

003DB580 initializes the finite entry free list, detached list, channel heads/tails and active bits.
003DBCF0 checks function-count bounds and available entries before insertion. Admission kind0
requires an empty channel; kind2 permits another entry including the same ID; kind4 refuses an
existing matching ID but can admit a distinct ID. A refused candidate returns to the free list.

The selector scans high channels first and head-to-tail within a channel. State1 entries are skipped,
state2 starts and becomes3, and a started entry resumes. A high channel containing only a queued
state1 entry does not prevent a lower runnable channel being selected.

Placement clamps a high channel to count-1, but submission's separate actor+26 mask uses the original
channel. With a synthetic channel7 and three configured channels, placement/active state is channel2
while that separate mask contains bit7. This is an interface-boundary test, not proof shipped
bytecode uses those out-of-domain values.

### A12-3 — starting a function preserves command scratch

003DBDC0 selects the wait slot, calls0025D460, sets kind1 and computes PC from the function table.
The core reset clears bytes+00..+16 only. Scratch+18..+27 and the other wait slots survive.
Storage initialization, logical entry removal, and freeing an actor allocation are distinct.
The store retains the types' existing SIGNATURE RESOLVED labels rather than self-promoting them.

### A12-4 — REQSW waits for selection/start, REQEW waits for return

Descriptor modes1/2/3/4 are distinct from admission kind and entry runState. Mode1 has no notification
in the tested start/end paths. Mode2 posts at selection/start, before the target's first opcode.
Mode3 posts on original removal/RET through003DC0D0. Mode4 is the detached notification itself.

The original interpreter's REQSW24 path can resume its caller while the target register still shows
that its bytecode has not run. REQEW27 stays blocked until the target executes its code and original
RET2D. Once a matching notification is consumed, following caller bytecode runs in the same original
0025DF00 invocation under the configured service gates. No extra frame is imposed by that transition.

### A12-5 — receipt capacity and identity are explicit preconditions

Both producers ignore failure to allocate the requester's notification entry. With no caller free
entry, target start or return still occurs but no detached receipt exists and the caller remains
kind4 in the fixture. This does not establish shipped deadlock, duplicate delivery, or automatic
retry; the actual producer bounds and recovery policy require separate evidence.

003DC050 matches channel plus low32(savedPC-bytecodeBase). Wrong-channel and wrong-offset receipts
leave the caller waiting; the matching receipt is removed/recycled. A request generation token is
not part of that tested key. Pointer/value equality cannot by itself prove lifetime or uniqueness.

### A12-6 — the older wait table had reversed its branch destinations

0025E127 is the blocked/no-interpreter exit, not the proceed path.0025E0BE enters the interpreter.
A completing branch sets kind1 and retries at0025DFA0 in the SAME invocation.

| Kind | Holds while / condition | Completion | +27 |
|---|---|---|---|
| 0 / >=8 | no runnable arm | no completion inferred | unchanged |
| 1 / 2 | opcode-dependent original interpreter | opcode-dependent | opcode-dependent |
| 3 | target entry exists, including state1 | entry absent | set1 |
| 4 | matching detached receipt absent | receipt present and removed | unchanged |
| 5 | list cursor sees matching actor/entry | cursor completes | unchanged |
| 6 | selected target channel bit set | selected bit clear | set1 |
| 7 | list cursor sees active selected channel | cursor completes | set1 |

The original opcode32 producer is also exercised: an existing entry causes target reference/ID,
kind3 and next-PC storage; an absent entry continues without arming the wait. The +16 serviced
marker has a conditional skip/clear gate through001EDDA0/001ED180, not a universal frame-delay rule.

### A12-7 — list waits are ordered progress, not simultaneous barriers

00267420/002674B0 read the encoded list reference at request+1C and WORD cursor at+22.
The list contains a DWORD count and four-byte actor/ID elements. Resource waits inspect the element
ID; channel waits use request+26 and ignore the element's second WORD.

The cursor advances past satisfied elements and stops at the first active one. Later polls begin
at that cursor. The test reactivates the already-passed first actor while clearing the second:
completion still occurs without rechecking the first. A null resolved list completes in the helper.
The list producer, ownership, signed count validity and complete authored domains are not certified.

## 4. Validation and falsification

**139/139 named original-instruction assertions pass.** A separate process produces an identical
baseline. Counts are assertions over fixtures, not139 game systems or exhaustive branches.
Eight wrong private-image code variants fail exactly their intended first assertion:

| Variant | Discriminator |
|---|---|
| Gate reads target rather than issuer | Conflicting issuer/target class values |
| Omit start notification | Receipt exists before target bytecode |
| Omit return notification | Original RET posts receipt |
| Reverse entry-existence polarity | Kind3 waits on a queued entry |
| Reverse receipt-existence polarity | Kind4 consumes a present receipt |
| Decrement list cursor | Cursor advances to second actor |
| Reset scratch rather than serviced byte | Start preserves scratch |
| Omit channel completion marker | Kind6 writes+27 |

Only affected mutations are run. A fault or unrelated assertion is not accepted as the intended
rejection. Original EXE hashes are checked before/after. Compiled binaries are temporary and are
not distributed. See [results](results/summary.json) and [named assertions](results/native_baseline.json).

Two development fixtures were corrected before final validation: a refused insert initially lacked
a readable manager image, and a serviced-gate control set only one of the two required globals.
Those were fixture failures, not FF12 defects. The final tests supply the missing state explicitly.

## 5. Canonical production

Nine existing files change: two mechanism pages, two contracts, Update11's connected mechanism,
EXP-106 interpretation notes, two type stores and the external continuation handoff. One new
mechanism page connects arming, selection, target return and caller resumption.

Only two type rows and nine field rows change; no type/field rows are added or removed. The previously
unassigned+1C/+22 wait fields now describe list reference/cursor at their demonstrated kind-specific
scope. Unrelated exact TSV lines remain unchanged. Two previously AUDITED mechanism pages are
REOPENED for their corrected claims, preserving old audit receipts as historical records.

Historical experiment programs/raw results, Update11 evidence, TEAM, global metrics, L2 verdicts,
current Ghidra annotations and reconstruction source are untouched. No required independent
acceptance, whole-system completion or live actor-reuse result is self-awarded.

## 6. Reproduction and application

On Linux x86-64 with Python3.10+ and GCC, from this evidence directory:

```sh
python run_review.py --exe '/absolute/path/FFXII_TZA.exe' --output '/absolute/path/new-results'
```

The output must not exist. The driver rejects an incompatible original image/range, compiler
diagnostics, unexpected fault, changed repeat, or wrong mutant failure. Nothing is downloaded.
Optional content validation additionally uses PyYAML. No command is required to install the ZIP.

Two inherited contract links point outside the database into Reconstruction. The two target files
are present in Reconstruction(8).zip and their hashes are recorded in
[the external-target receipt](results/external_link_targets.json); that archive is not bundled, and
on-PC relative-path resolution is not claimed.

Apply after Update11 to the September23 snapshot. Merge the ZIP's FFXII TZA folder into the existing
folder's PARENT. Do not nest or delete the database. Back up touched files; newer peer edits require
merging rather than blind replacement. verify_overlay.py is a read-only compatibility check.

## 7. Remaining frontier

Original list-wait producers and lifetime, additional variable/reference storage opcodes, higher
notification recovery/uniqueness, other native wait services and full outer scheduling remain open.
Astra's live actor/register allocation-reuse question stays separate. Formal peer review must
accept, narrow or reject these production claims before updating the corresponding L2 assessment.

## Evidence index

- [Original manifest](original_body_manifest.json), [selected disassembly](original_disassembly.txt)
- [Native source](native_controls.c), [reproduction driver](run_review.py), [variants](variant_plan.json)
- [Scope](scope.json), [source identities](source_inputs.json), [claim map](claim_matrix.tsv)
- [Baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [mutants](results/code_mutations.json)
- [Body checks](results/body_verification.json), [summary](results/summary.json)
- [Row changes](canonical_row_changes.json), [canonical diff](canonical_changes.diff), [preimages](canonical_preimages.json)
- [Content checks](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json)
- [Unchanged files](results/unchanged_files.json), [delivery check](results/delivery_validation.json)
- [Manifest](PATCH_MANIFEST.json), [read-only preflight](verify_overlay.py), [content checker](validate_content.py)
