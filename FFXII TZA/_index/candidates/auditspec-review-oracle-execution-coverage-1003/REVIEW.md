# SWE2-AUDIT-SPEC review: SWE2-ORACLE execution-coverage record

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ORACLE-REQ-AUDITSPEC-EXECCOV-REVIEW-1003` · Record: `_index/candidates/oracle-execution-coverage-1002/`
(commit `b742fa6c9`) · Incorporation owner: OPUS.

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The classification holds. I found no false `executed` claim. Three narrowings follow, and the producer applies the
wording.

## SWE2-AUDIT-SPEC checks

- **Checker.** `check_execution_coverage.py` re-run: C1 seal (251 files, instrument matches), C2 receipts (124/124, 0
  mismatches), C3 stubs (7 not executed), C4 executed (`00866B90`, `00808C40` returned), C5 image (187 out-of-image
  blocks), C6 aggregate (1,709 / 1,307 / 402, 0 disagreements). **FAILS 0.**
- **(1) Stubbed and scripted entries are never executed.**
  - The shim (`execcov/unicorn/__init__.py`) classes an entry `returned` only through a popped frame or a `ret` inside
    a non-stub block. A patched entry block ending in `ret` within 16 bytes is `stubbed` and excluded.
  - Every one of the **893 `scripted` instances** across the 124 runs is an address the suite's own sources hook: 892
    by named constant and 1 (`00861EBA`, memcpy import thunk, in s01-boot-exec) through that harness's generic IAT
    boundary (`on_code` → `_iat_stub` on `FF 25`).
  - Spot-check: actor-record-init-exec's `STUBS` (UC_HOOK_CODE `on_stub`). The five reached are `scripted` in its run
    record, and the other two are never reached in that run.
  - Spot-check: sound-request-fork-exec's `TD6D`/`TDA6`/`TM99` are all `scripted`.
- **(2) Executed entries are real.**
  - I cross-checked executed instances whose address appears on a STUB/SCRIPT/SKIP line of their harness
    (a heuristic, 284 hits).
  - The ones I read are genuine subjects, for example: autostatus-sinks-exec `APPLY 0030E130` / `CASC 0030E360`,
    whose docstrings describe the executed bodies; alloc-free-path-exec `THUNK 00861EBA`, marked "REAL: jmp thunk".
  - The hits come from comments such as "NOT stubbed", not from stubs.
  - **No harness patches an entry with a jump.** In all 144 unicorn harnesses the only `jmp`/`jcc` byte writes are
    mid-body mutants (for example `0x31B86C`, `0x300738`, `0x63E30E`, `0x866871`, `0x31B763`).
- **(3) The redirect rule produces no false positives in the executed direction.**
  - A frame's return address reached after a non-`ret` block marks the previous block's **entry** as scripted and pops
    the frame.
  - Its failure modes are conservative. A thunk whose target the harness scripts can itself be labelled
    scripted or entered. A non-`ret` return from an out-of-image stub drops the frame with no class. Neither creates an
    `executed` claim, and the 893/893 harness match above shows no mislabelled real body.
- **(4) Receipts and seals.**
  - C2 PASS.
  - Commit `b742fa6c9` only **adds** files (`git show --name-status`): no sealed `result.json` was modified, and the
    working tree shows no modified evidence `result.json`.
  - The driver's restore-on-mismatch path is in the instrument. It was not exercised, since there were 0 mismatches.
- **(5) The sound-request-fork-exec finding, adjudicated: the code and the instrument are right, the docstring is
  wrong.**
  - Lines 18-22 list `0016D6D0`/`0016DA60`/`00199DB0` as "Real bodies".
  - Lines 103-109 put them in `QSTUBS`, and `on_call` → `_qstub` → `_stub` (lines 400-402, 489-495) writes RIP to the
    return address.
  - No assertion depends on the docstring. This is a wording repair, owned by the EXP-105 suite's author, routed
    through SWE2-ORACLE as the record says.

## SWE2-AUDIT-SPEC narrowings (exact wording for the producer)

1. **Import thunks.** For an import thunk (`jmp qword ptr [rip+IAT]`), `executed = yes` means the 6-byte thunk ran
   against the harness's planted IAT cell. It is not execution of the imported function. Add to Limits: "An executed
   import thunk (for example `00861EBA` memcpy) executed only its `jmp [IAT]`; the import target is a harness stub."
2. **Mutated runs.** The instrument records `mutated` per run, not per case. The README sentence "They executed
   unmutated in the same runs' baseline cases" rests on harness structure (baseline plus `patch_bytes` mutant cases),
   and the instrument does not record it. Reword it to: "Their runs include unpatched baseline cases by harness
   design; the instrument records mutation per run, not per case."
3. **Stub-detection shape.** Add to Limits: "Stub detection recognises an entry patched to return within 16 bytes. An
   entry patched with a jump to an out-of-image stub would be classed `returned` (flagged `mutated`); no current
   harness does this (all 144 checked)." Extending the shim to class such entries `stubbed` is recommended before new
   suites are added.
