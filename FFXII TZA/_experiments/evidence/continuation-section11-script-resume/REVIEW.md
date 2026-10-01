# SECTION-11 — script execution, native commands and resume state

Date: 2026-09-23. **Local production complete and validated; formal independent acceptance pending.**
Base: `FFXII TZA(20260923-205605).zip`, SHA-256
`f52ffea6e6f2bdc27218b0499e8d0d7941669a8ba26dfed3d38cce6c0da57c1c`.
That snapshot already incorporates Updates01–10 and subsequent Devin changes. This is a
changed-files production overlay, not a new global audit, numbered EXP or L2 ruling.

## 1. Scope and value

Original0025E4C0 bytecode execution now connects to original002621D0 and actual wait/getmyid/
getx/nowmap callbacks. The full original0025DF00 request-driver entry is exercised for selected
runnable requests. This fills the former boundary between EXP-106's scripted interpreter and
EXP-085's planted callbacks without rebranding either earlier experiment.

The new specification covers persistent actor/request state, shared evaluation depth, phase-based
resumption, target/issuer identity, typed/default results, capacity refusal and local stop behavior.
It is not exhaustive semantics for100 opcodes, every wait kind, all native commands or the full
outer field-frame driver. Live actor allocation/reuse work remains a separate task.

## 2. Provenance and exact fixture boundaries

Original EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The manifest pins58 selected contiguous original bodies and7 data spans. Historical Ghidra ranges
were reused and decoded against the EXE; there is no new Ghidra import or current GN162/population
certificate. Original EXE and six historical input files are checked before and after reproduction.

The child privately maps the original image at00120000 and calls it with the Microsoft x64 ABI.
Synthetic maps supply managers, two actors, request arrays, bytecode, labels, numeric pools, selected
save-state values and idle service predicates. Original003DC2D0 initializes the family table.

**Application substitutions: ZERO. Import bridges: ZERO. Planted command callbacks: ZERO.**
All reached instructions are original except during explicitly named private-image mutation runs.
Host code supplies inputs and observes outputs; it does not simulate successful callbacks.

The full0025DF00 call uses runnable-kind1 and idle service paths. Other kinds, nonempty service
branches and outer0025D9E0 execution are not certified. The actor-table replacement control is a
synthetic rebind, not live allocator reuse. The guard-page fault is expected in an isolated child,
not induced in a running game. No Windows loader, OS I/O, live schedule or observer deployment runs.

## 3. Main findings

**S11-1 — the evaluation stack is image-backed, not a caller-frame object.**0025E4D8 resets depth at
02099AC0 on every interpreter entry, even refusal. Array sentinel bytes survive. Actor registers,
selected request accumulator/phase/scratch persist across a return and another actor's execution.
The previous lifetime inference from an argument register was invalid. Standalone helpers still
accept an explicit stack object; that does not define the interpreter's allocation.

**S11-2 — CALL resumes, not reinitializes.** Real wait2 produces counters1,0,-1 across three calls,
with the PC retained at CALL for the first two and following instructions executed after completion.
Begin and argument pops do not repeat while phase1. Wait0 can complete immediately. Another original
predicate setup scales3 to6 before polling. These are invocation-count cases, not exact live frames.

**S11-3 — target, issuer and indexed control are different objects.** CALLACT/ACTPOPA retain the
popped ordinal. The lifecycle re-resolves it; original getmyid writes the result into the issuer's
selected request. The slot index is signed and has stride0x28, tested at0 and1. Original wait reads
an indexed byte via target actor+15 and00267310; it is NOT commandPhase in the issuer's request.
The same phase1 with different control bytes produces different countdown behavior. The old CE-5
reentrancy-guard conclusion is withdrawn, not replaced with an unproved global skip meaning.

**S11-4 — phase resets and result delivery is conditional.** Original result writers select int2
or float3; completion resets0. A callback can write result storage while depth63 denies append.
Missing callbacks complete with implicit int0 when space allows. New tests use actual callbacks,
not the historical planted functions. Complete runtime service semantics are not inferred.

**S11-5 — not every epilogue request makes progress or returns immediately.**25E60A requests stop;
25E613 only advances. Nonempty depth at the stop boundary is discarded and execution continues.
An extra operand under wait's argument causes another poll in that SAME invocation. Opcode00's
length0 spins to budget;01 stops at the same PC;03 sets actor flag40 and cancels its own advance.
A self-jump and a66000-byte discard stream distinguish the65,536-iteration budget. These are
synthetic bytecode states, not a full authored-corpus reachability analysis.

**S11-6 — an unused predecoded operand can still fault.**47 is length1 but reads PC+2 andPC+1.
An isolated child faults specifically at25E5AF/PC+2;19 at the same boundary safely returns.
The prior "unused so harmless" argument is false. Above63, length lookup remains opcode-indexed
outside the documented rows; no general malformed-input safety/progress guarantee is added.

**S11-7 — typed execution and native results are not uniformly floating point.** Signed literals,
int addition/wrap, mixed float addition, float register bits and truncating pops are discriminated.
Label-based branches land at the intended offset; request accumulator and actor registers are
separate persistent state. Other arithmetic and variable/reference opcode families remain open.

## 4. Retained evidence and validation

146 named assertions pass and an identical second process repeats them. A count is assertions over
fixtures, not146 distinct game systems or complete branch coverage. Ten wrong private-image code
variants fail exactly their intended first assertion:

| Variant | Discriminator |
|---|---|
| Omit entry-depth reset | Refused entry still clears shared depth. |
| Repeat begin on phase1 | Second wait invocation remains busy with retained countdown. |
| Omit busy-PC rewind | Saved PC remains the CALL. |
| Keep phase1 on completion | Third wait invocation resets phase0. |
| Mark float as integer | Real getx bits reach the float register correctly. |
| Force issuer as target | CALLACT reads the other actor's ID. |
| Omit stop-depth discard | Nonempty stack marker discards the operand. |
| Shorten budget | Advancing stream runs65,536 iterations before return. |
| ACTPOPA selects issuer | Popped target ordinal remains1. |
| Omit implicit-zero append | An absent-callback command still appends one zero. |

Only affected mutations run. No full-project mutation campaign is claimed. A wrong mutant rejected
by an unrelated fault does not count: the driver checks the exact failing assertion and exit code.

The independent retained reducer checks14 selected EXP-085 order/return/phase/depth records and
rejects8 content-corruption controls. It does not trust stored pass booleans. All35 historical
records, including producer mutation cases, are retained, but the other rows are not newly
independently accepted. The historical Unicorn driver is pinned, not rerun.

Two fixture assumptions were corrected during development: the signed literal is opcode4F,
not4E (which reads the int pool); ACTPOPA's branch skips the neighboring issuer reload rather than
executing it. Both were checked against actual targets before canonical publication. These fixture
mistakes are not game defects and failed development outputs are not called successful evidence.

## 5. Canonical changes

Ten existing files change: three ScriptVM contracts, two mechanism pages, two experiment writeups,
two type stores and the external handoff. One new connected mechanism page is added.
Only two type rows and seven field rows change. ActorWaitSlot's first12 bytes are retiled from
stamp4+unknown8 into kind-selected head8+targetordinal4. Row counts are unchanged. The accumulator
and scratch descriptions are corrected. Unrelated TSV lines remain byte-identical.

VmValueStack becomes SIGNATURE RESOLVED pending review of its repaired lifetime; this is not a new
full-type acceptance. The two previously AUDITED mechanism pages are REOPENED, with old audit dates
and counters preserved as history. Only touched colon-bearing provenance scalars are quoted for
strict YAML. Original programs/raw evidence, prior production sections, TEAM, L2 verdicts, global
metrics, Ghidra annotations, game image and reconstruction remain untouched.

Correcting the bridge's source-kind enum restates the existing canonical type evidence's explicit
uncertainty, not a new complete variable-load census. Required uncertainty is not erased to make
this package appear to close the whole system.

## 6. Reproduction

On Linux x86-64 with Python3.10+ and GCC, from this directory:

```sh
python run_review.py --exe '/absolute/path/FFXII_TZA.exe'   --database '/absolute/path/FFXII TZA' --output '/absolute/path/new-results'
```

The output must not exist. Nothing is downloaded. Hash mismatch, altered historical input, compiler
diagnostics, unexpected fault, changed repeat or wrong mutant failure rejects the run. Binaries
exist only in a temporary build directory. Native/retained reproduction uses Python's standard
library and GCC; optional document validation uses PyYAML. No user commands are required to install.

## 7. Remaining work and safe delivery

Next substantive work: original actor-call/request arming and non-kind1 waits, or another selected
native service whose ownership has been checked. Preserve the separate ASTRA live register/allocation
question. Whole frame scheduling, reentrancy, full opcode/verb populations, script-resource lifetime
and shipped input bounds remain open. Required peer acceptance is not self-awarded here.

This overlay is based on the SEPTEMBER23 snapshot, not an instruction to overwrite newer Devin
changes. Merge its FFXII TZA folder into the existing folder's parent; replace only listed files.
Back up touched files. A newer local edit is a merge conflict, not permission to erase peer work.
The read-only verify_overlay.py compares exact preimages and accepts already-installed postimages.

## Evidence index

- [Bodies/data](original_body_manifest.json), [disassembly](original_disassembly.txt), [scope](scope.json)
- [Opcode table](opcode_dispatch_lengths.tsv), [selected callbacks](tested_callbacks.tsv)
- [Native source](native_controls.c), [driver](run_review.py), [variants](variant_plan.json)
- [Summary](results/summary.json), [assertions](results/native_baseline.json), [repeat](results/native_repeat.json), [mutants](results/code_mutations.json)
- [Retained reviewer](review_retained.py), [selected checks](results/retained_review.json), [corruptions](results/retained_negative_controls.json)
- [Canonical row changes](canonical_row_changes.json), [diff](canonical_changes.diff), [preimages](canonical_preimages.json)
- [Source identities](source_inputs.json), [historical inputs](input_manifest.json), [claim map](claim_matrix.tsv)
- [Content validation](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json)
- [Unchanged files](results/unchanged_files.json), [delivery validation](results/delivery_validation.json)
- [Manifest](PATCH_MANIFEST.json), [read-only overlay check](verify_overlay.py)
