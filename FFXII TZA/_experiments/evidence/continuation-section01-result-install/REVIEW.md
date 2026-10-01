# SECTION-01 — Result application and battle-unit installation

**Production checkpoint:** 2026-09-22. **Disposition:** incorporate bounded findings with corrections; formal T2 peer review and canonical acceptance remain pending. **Overall database goal:** NOT MET.

This is actual database production against `FFXII TZA(20260922-211246).zip`, not a fresh terminal audit. It rewrites two canonical contracts, corrects their two mechanism pages, and places current consumption/correction notes on EXP-148/149/150. Original experiment programs and result records are unchanged. TEAM ownership, L2 verdicts, completion counters, reconstruction sources, and live workstation state are not changed.

## Inputs and provenance

- Baseline archive SHA-256: `fc02c2fcc0fd305c53e0c8c2949b7b4dad6225921db1328cbfd8cfffea34aeaf`.
- Original EXE SHA-256: `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`; image base `0x120000`.
- [Pinned retained-input hashes](input_manifest.json) identify the six unchanged experiment program/result files.
- [Original body ranges and hashes](original_body_manifest.json) cover seventeen bodies. Their supplied historical Ghidra boundaries were used to re-read current original bytes; no new GN162 import or current annotation certification is claimed.
- [Original disassembly](original_disassembly.txt) contains the relevant source instructions.
- [Reproduction summary](results/summary.json), [native checks](results/native_results.json), [mutant outcomes](results/mutation_results.json), and [retained-record review](results/retained_review.json) preserve actual results.

## Validation performed

| Method | Result | Meaning and limit |
|---|---:|---|
| Original body hash check | 17/17 | Exact bytes of the selected original bodies match. Not whole-executable semantic certification. |
| New original-instruction controls | 42/42 | Linux x86-64, Microsoft x64 ABI, synthetic state and explicit private-image bridges. Forty-two named checks; some assertions share one fixture invocation. Not a live FF12 session. |
| Repeat original baseline | Identical results | One repeated baseline, not 84 distinct controls. |
| Relevant private-image mutants | 4/4 detected | Deliberately skip a direct copy, suppress the caller dirty flag, use the wrong tracked-table base, or omit the invalid-class bit clear. Original EXE on disk unchanged. |
| EXP-148 retained assertion replay | 43/43 | Extracted CASES/check logic evaluated against retained outputs. No emulator re-execution; the intended null fault remains an expected observation. |
| EXP-149 retained assertion replay | 36/36 | Same distinction. Passing retained assertions does not prove every prose inference. |
| Deliberately corrupted retained records | 4/4 rejected | Sensitivity of selected recorded assertions, not additional original-game executions. |
| EXP-150 retained integrity | 39 consistent records | Includes three producer mutant cases. Its world-dependent assertion function was not replayed here. |

The supplied Unicorn campaigns, their multi-process repeatability statements, live installed-game behavior, complete transitive execution, T2 acceptance and L2 system completion are **not** newly certified.

## Result-application corrections

### R1. Stats receivers are distinct from their owning units

`003112F0` receives result/source-stats/target-stats/action/caller-flags. `0031B860` resolves a stats pointer to the owning BattleUnit by comparing the unit's `+0x698`. The high-offset owner accesses at `+0xE9A`, `+0xE60` and `+0x6A0` are not fields of the stats record. EXP-149's `tgt/src` denote stats and `trec/srec` denote owners despite some earlier prose reversing the distinction.

### R2. Parameter forwarding and direct copies both occur

Original `003115B6..00311606` copies nonnegative result dwords `+0x5C+4i` into target stats `+0xBC+4i`, and nonnegative signed words `+0xDC+2i` into stats `+0x13C+2i`. These loops run even with both status masks zero. Negative values preserve existing destination bytes; zero is a present value. Copying alone does not set the caller's `r14d` flag.

EXP-149's statement that these were not direct copies is withdrawn. Its retained `ap-copythrough` selects a status as well and therefore does not isolate the two possible writers. New controls `copy_without_any_status_mask`, `negative_copy_values_leave_destination` and `zero_copy_values_are_present` discriminate them. The skip-copy mutant is rejected.

### R3. The outer recompute flag records dispatched branches, not confirmed changes

At `0031153F`, `003115A4`, `003117D0` and `0031180C`, original code sets `r14d=1` after a selected status/layer call without testing whether the callee changed state. The tail at `00311AAF..00311AC5` tests target, caller bit9 and this flag. Refused or idempotent calls may therefore still lead to the outer recompute.

New no-effect argument-recording sink controls demonstrate that caller property. Retained real-callee `ap-st-idempotent` and `ap-st-d38lock` records corroborate it in their respective fixtures. The suppressed-dirty-flag mutant is rejected. This does not mean every direct store or temporary owner flag sets `r14d`.

### R4. No outer numeric-tail call does not mean no transitive recomputation

The numeric paths themselves do not set that dirty flag. A lethal HP path can nevertheless reach status code and `0030FED0` internally: the retained `ap-lethal` trace contains `fed0_real` without `fed0_tail`. The old broad claim that damage cannot recompute stats, or cannot refresh a stat panel, is not supported. No UI refresh observation was performed here.

### R5. A neutral result has field-specific sentinels

Zero masks/presence bits, `0xFF` layer/level bytes, negative copy/timer values, and the appropriate absent item/counter fields are different rules. An all-`FF` result is not neutral: it selects both 32-bit status masks. The new all-FF control records 64 status dispatches. Even an effect-neutral fixture may run metadata handling and owner temporary-bit cleanup.

The apply and remove masks select the same 32 IDs, not 64 distinct statuses. Layer set/remove modes are likewise distinct from normal status masks.

### R6. HP call flags and source presence are corrected

For input flags A at result `+0x2C`, outgoing target HP flags are `A19->8`, `A10->5`, `!A18->6`, `!A6->4`. There is no unconditional `0x400`; target-presence alone yields `0x50`. Source HP uses presence bit7 and flags `A9->5`, `!A17->6`, `!A5->4`; source MP presence is bit13. Target MP uses `A16->5,!A12->4`, source MP `A15->5,!A11->4` from the original instruction reading. The secondary-resource negative-multiplier path has its own `0x400`, not a contradiction of the HP result.

New controls vary the HP bits and source-presence paths. EXP-060's existing correct bit7 mapping is not retrospectively described as a published bit31 error.

### R7. An advertised nested-entry intercept was not tested

EXP-149's entry shortcut (`addr == self.entry`) precedes the nominal nested-applier interception branch. Current fixtures leave the re-entry trigger clear. This section does not claim an exercised intercept or recursive behavior. The original program/result are retained, and repair plus a deliberately triggered rerun is pending.

## Battle-unit installation corrections

### U1. Preserve canonical class identity despite reversed local case names

Selector class0 is party; class1 is spawn-backed enemy. EXP-150's historical `in-member` uses class1 and `in-foe` uses class0. Those case identifiers remain unchanged, with their meaning stated explicitly. The two stats/owner paths are not interchangeable.

### U2. Unsupported-class and terminal masks clear bit26

The original AND mask at `0023A633` and `0023AC4B` is `0xFFFFFFFFFBFFFFFF`: bit26 clears, not bit42. The older page's terminal bit24 interpretation is also corrected. EXP-150 starts its invalid-mode case with bit42 already clear, so that check could not establish the claimed bit clear. New controls seed both bits26 and42 and show only26 clearing; the omitted-clear mutant is rejected.

### U3. Registration uses `02EC1380` and is conditional

`00328FF0` resolves its base to `02EC1380`, stride24. It writes `{slot,code}` only when `(code != 0 || slot < 0)` and its signed row check is below2. The installer's slot is zero-extended from a byte; code zero therefore does not register that install. EXP-150 captures `02E81380` instead and does not assert those captured values. New controls verify correct and wrong locations, row1 stride, row2 rejection and negative-slot behavior. The wrong-base mutant is rejected.

### U4. Pulse reset is a narrow ten-byte original body

`002FEAB0` clears the qword at receiver `+0xEAC` (covering `+0xEAC/+0xEB0`) and returns. It is not a heavy float calculation at `+0x2E0`. A surrounding-canary control verifies the narrow write. The all-ones reset control shows these pulse bytes surviving `00236A60` until the separate pulse-reset stage; reset is not whole-object zeroing.

### U5. Failure can follow reset and rekey; it is not transactional rollback

Reset precedes the master-enable rejection. With the master enabled, rekey/bypass selection precedes class validation, so class2 can change the handle and then return0. The selected-teardown bypass at `0023A5CD..0023A5F2` is retained; a universal nonzero-class rekey statement would be too broad. New disabled and mode2 controls execute those original paths, with selection and the inner key resolver explicitly bridged.

### U6. The two class-specific floats were conflated

Class1 uses `float(classRecord.byte+0x27)` without `x1.5`; the multiplication at `0023ABAD` belongs to class0's byte+0x2B path. This is an original-instruction correction, not a new live value observation.

## Precisely which native boundaries were substituted

The full `003112F0` caller body remains original. For its caller-contract controls, stats-owner resolution, eligibility, metadata, status/layer sinks, recompute, HP/MP setters, secondary/level/item/gil and event boundaries are explicit no-effect or argument-recording C bridges. The source lists every patched address. These controls isolate the caller; they do not recreate EXP-149's real-callee transitive coverage.

The pulse reset, tracked writer and blob helper execute original bodies. Reset uses its original helper chain and a memset bridge, with optional cleanup `003105D0` suppressed. Invalid/disabled installer paths additionally bridge selection `00303EC0` and inner rekey `003220E0`. Success-path authored joins, engagement, full spawn initialization and live lifetime were not newly executed.

All bridges and mutants exist only in a private process mapping. No original executable, original experiment file, game process or PC repository was written.

## Canonical propagation and reviewer handoff

Updated contracts:
- [Apply result](../../../07-Combat-Action/CONTRACT-apply-result-to-target.md).
- [Battle-unit installation](../../../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md).

Updated mechanisms:
- [Applying a result](../../../07-Combat-Action/applying-a-result-to-a-target.md).
- [Building a unit from its definition](../../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md).

Current correction notes were also added to [EXP-148](../../EXP-148-apply-result-callees-exec.md), [EXP-149](../../EXP-149-apply-result-whole-exec.md), and [EXP-150](../../EXP-150-battle-unit-construct-exec.md). Their recorded historical executions are preserved, while unsupported prose is corrected. The two mechanism pages now say DOCUMENTED rather than implying the newly edited content has already passed the historical AUDITED process. Earlier audit metadata remains labeled historical.

This package answers the substance of the pending OPUS findings requests for these experiments without claiming their TEAM tasks or impersonating their reviewers. The accepted T2 workflow still requires the actual peer/owner decision. Existing EXP-060/062 evidence is incorporated at its original bounds; no missing review-tool result or frontmatter tier promotion is fabricated.

## Remaining work, not section-completion blockers

Repair EXP-149's recursive intercept test and EXP-150's wrong table read/nondiscriminating flag assertion, then rerun the affected original producer controls where its emulator environment is available. Preserve old outputs; publish a new receipt rather than rewriting historical results. Continue the outstanding real callback, valid-state reachability, installed-game and broader L2 ownership/contract questions.

The section closes the local production/propagation package, not the complete result subsystem, battle-unit system, full database, or independent acceptance process. No global percentage or MET verdict is raised by this overlay.

## Reproduce

The overlay must first be merged with the full matching database, because unchanged experimental inputs are intentionally not duplicated. On Linux x86-64 with Python 3.10+ and a GCC-compatible compiler:

```sh
python run_review.py --exe /path/to/FFXII_TZA.exe --output /path/to/fresh/section01-results
```

The script locates the database from its nested location; `--database` can override that. It verifies pinned hashes before execution, compiles a PIE host in a temporary directory, repeats the native baseline, runs only the four impacted mutants, replays 79 retained assertion cases, checks EXP-150 record integrity, and confirms inputs are unchanged. It refuses to overwrite an existing nonempty output directory. No EXE, compiler binary, Unicorn package or full database is redistributed.
