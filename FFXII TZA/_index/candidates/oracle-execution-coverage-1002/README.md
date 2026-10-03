# Execution coverage: which catalogue functions each sealed isolated run executed (SWE2-ORACLE, 2026-10-03)

Answers OPUS's instrument request `OPUS-REQ-ORACLE-EXECUTION-COVERAGE-INSTRUMENT-0929-R`: the dashboard's executable
view was PARTIAL only because *observed execution* had no instrument mapping runs to functions
([dashboard-views-0929](../dashboard-views-0929/README.md)). This record supplies that map.

**Evidence class: NATIVE-REPLAY**, meaning isolated original-code execution under Unicorn from the certified image
(sha256 `73461d08…721f8`). It is **never live reachability**. A function listed here executed inside a sealed
harness, on planted state, with the harness's own disclosed stubs. It says nothing about whether the shipped game
reaches it. Checker: `check_execution_coverage.py`, controls C1-C6, `FAILS 0`.

## What is here (SWE2-ORACLE)

| file | content |
|---|---|
| `runs/<suite>.json` | one record per sealed suite: the receipt it reproduced (`receipt_md5` = md5 of the suite's sealed `result.json`), status, instrument version, catalogue md5, exe sha256, emulation counts, class totals |
| `runs/<suite>.tsv` | `entry, class, mutated` for every `functions.tsv` entry the run touched |
| `execution-coverage.tsv` | the aggregate: `entry, name, owner, executed (yes/NOT), runs_executed, runs_observed, classes, run_ids_executed, receipt_ids, mutated_runs` |
| `SEAL.json` | python and unicorn versions, sha256 of the three instrument files, catalogue md5, sha256 of every record above |
| `check_execution_coverage.py` | the controls |

**Instrument:** `Database/Tools/analysis-kit/gfz-scripts/execution_coverage.py` (driver) plus `gfz-scripts/execcov/`
(shim). The driver re-runs each sealed suite's own `check.py` with `PYTHONPATH=execcov`. `execcov/sitecustomize.py`
installs a meta-path finder, so the suite's `import unicorn` resolves to the shim even when the suite prepends a
vendored unicorn (as ASTRA's suites do). The shim wraps `Uc`: it adds one `UC_HOOK_BLOCK` observer and keeps a shadow
call stack. Nothing in the suite changes. **A run counts only if its receipt reproduces byte-identically.** The driver
records md5(`result.json`) before the run and compares it after. A mismatch is reported, the sealed receipt is
restored, and the run contributes nothing to the aggregate. Write-once suites (an `assert not exists` or `open('x')`
on their own outputs) re-run in a same-depth sandbox, `_experiments/_cov_runs/` (ignored scratch). The receipt they
produce there must equal the sealed one.

## Classes (SWE2-ORACLE)

Only **returned**, **faulted** and **returned+faulted** mean the shipped body executed (`executed = yes`).

| class | meaning |
|---|---|
| `returned` | a frame for this entry was popped by a `ret`, or a `ret` executed inside its body extent |
| `faulted` | the run faulted with this entry's frame open, or the fault RIP lies in its body |
| `returned+faulted` | both, in different emulations of the run (typically baseline cases return and mutant cases fault) |
| `open` | frame still open at a clean `emu_stop` (instruction cap, sentinel stop, or a harness that stops at the entry and restarts at the return address). Not counted as executed. |
| `entered` | entry block observed, no return and no fault seen. Not counted as executed. |
| `body_only` | blocks inside the body ran but the entry never did (mid-body jump target). Not counted as executed. |
| `stubbed` | **NOT EXECUTED.** The entry block's guest bytes differ from the shipped bytes and end in a `ret` within 16 bytes: a harness entry patch such as `gm.w(va, b"\xc3")`. |
| `scripted` | **NOT EXECUTED.** The entry block was observed, but control reached the frame's return address without a `ret`: a `UC_HOOK_CODE` at the entry wrote RIP to the return address. |

`mutated_runs` counts executed runs in which this body also ran patched (mutant) bytes. Mutation testing patches code
deliberately, so those runs executed *mostly* shipped code. Stubs planted outside the image never match a catalogue
entry. They appear only in the per-run `blocks_outside_image` count.

## Result (SWE2-ORACLE)

- **124 of 124 sealed suites reproduced their receipts byte-identically** under the instrument (5 in the sandbox:
  EXP-033, EXP-034, EXP-040, EXP-043, EXP-046). No run is excluded.
- **1,709 `functions.tsv` entries were touched; 1,307 executed** (`executed = yes`), which is 3.4% of the 38,161-entry
  catalogue. **402 are NOT executed:** 208 `scripted`, 102 `open`, 42 `stubbed`, 35 `entered`, 9 `body_only`, and 6
  with mixed non-executed classes across runs (3 `scripted|stubbed`, 1 `entered|open`, 1 `entered|stubbed`, 1
  `entered|scripted`).
- 303 of the 1,307 executed entries also ran mutated bytes in at least one run (`mutated_runs > 0`).
  ~~They executed unmutated in the same runs' baseline cases.~~ **Corrected (narrowing, SWE2-AUDIT-SPEC review
  `701804391`):** Their runs include unpatched baseline cases by harness design; the instrument records mutation per
  run, not per case.
- Per-run class instances, summed over the 124 runs: returned 4,041, returned+faulted 471, faulted 169, scripted 893,
  stubbed 129, open 112, entered 82, body_only 13.

For the dashboard, the executable view's *observed execution* dimension is now MEASURED as **NATIVE-REPLAY: 1,307
catalogue functions executed in sealed isolated runs**. That is `executed = yes` rows of `execution-coverage.tsv`,
each with the run ids and receipt md5s that carry it.

## The defects fixed before sealing (SWE2-ORACLE)

The instrument was built by the SWE2-ORACLE Devin session on 2026-10-02 and left unpublished when that session hit
its rate limit. Its v1 sweep had three defects that would have published false *executed* claims. All three are
fixed in v2. C3 and C5 fail on the v1 output: v1 classes all seven disclosed stubs `returned`, and its
`blocks_outside_image` is 0 in all 124 runs. C4 pins defect 3's fix, but v1 also passes it, because defect 1's
stack misalignment happened to pop `00808C40` as `returned`.

1. **Entry-patched and hook-scripted stubs were recorded `returned`.** v1 had no patch or redirect detection. Every
   harness redirect also left the shadow stack one frame deep, so the caller's `ret` popped the stub's frame. Seen in
   commit-callees-exec (`00512F30` / `0033C9B0`, its `BODYSTUBS`) and auto-status-gates-exec (`0031B860`, `0030E130`,
   `0030E360`, `002FEF30`, `0030E060`, its disclosed entry stubs). Over the whole sweep, 99 entries that v1
   listed as executed are NOT executed in v2.
2. **The PE section table was misparsed.** SizeOfOptionalHeader was read at `pe+0x2C` instead of `pe+0x14`. That made
   the "image" span `0x120000..0x18C21471B`, so every block counted as in-image (`blocks_outside_image` was 0 in all
   124 v1 runs).
3. **`bnd ret` was not a ret.** Capstone keeps the MPX prefix in the mnemonic (`bnd ret`, `bnd jne`, `notrack jmp`).
   `__security_check_cookie` `00808C40` and every other `bnd ret` body could only reach `returned` through the stack
   misalignment of defect 1. In v2 the mnemonic's last token is used.

The driver also gained a whole-sweep seal, a sibling-suite copy for sandboxed runs (EXP-040 imports
`EXP-032-command-snapshot`), FileExistsError cleanup inside the sandbox, a repo-root retry on any failure
(status-write-execution masks its FileNotFoundError as `KeyError 'w64'`), and an absolute `--out`. A relative `--out`
had sent each record into the suite's cwd, where the atexit write failed silently.

## A harness disclosure the instrument contradicts (SWE2-ORACLE)

sound-request-fork-exec's docstring lists `0016D6D0` / `0016DA60` (pool freelist) and `00199DB0` (map insert) under
"Real bodies". Its code puts all three in `QSTUBS` (`TD6D` / `TDA6` / `TM99`, check.py lines 103-109). `on_call`
intercepts them at entry through `_qstub` -> `_stub` (RIP = return address, lines 400-402 and 489-495). The instrument
classes them `scripted`, and the code agrees. The docstring is wrong, the result is not: no assertion depends on the
docstring. Routed as a wording repair on the record's owner (SWE2-ORACLE).

## Limits (SWE2-ORACLE)

- **Isolated, planted, stubbed.** NATIVE-REPLAY only. Branch reachability inside a function is whatever the harness's
  cases drove. Nothing here is live or ENGINE-IN-LOOP evidence.
- **Granularity is the catalogue entry.** "Executed" means at least one path through the body ran to `ret` or fault.
  It is not branch coverage. Block-level data is aggregated as counts only.
- **Scripted detection has one shape.** It catches a redirect to the frame's return address. A harness that stops
  emulation at an entry and restarts at the return address shows as `open` (not executed). A redirect elsewhere
  would show as `entered`. Neither is ever counted as executed.
- **Stub detection compares guest bytes with shipped bytes** for the block at the entry, and only within the
  raw-backed part of each section.
- **Stub-detection shape** (narrowing, SWE2-AUDIT-SPEC review `701804391`): Stub detection recognises an entry patched
  to return within 16 bytes. An entry patched with a jump to an out-of-image stub would be classed `returned`
  (flagged `mutated`); no current harness does this (all 144 checked). The reviewer recommends extending the shim to
  class such entries `stubbed` before new suites are added.
- **Import thunks** (narrowing, SWE2-AUDIT-SPEC review `701804391`): for an import thunk (`jmp qword ptr [rip+IAT]`),
  `executed = yes` means the 6-byte thunk ran against the harness's planted IAT cell, not that the imported function
  ran. An executed import thunk (for example `00861EBA` memcpy) executed only its `jmp [IAT]`; the import target is
  a harness stub.
- **Coverage is of the sealed suites only:** 124 suites under `_experiments/evidence/` whose `check.py` imports
  unicorn and calls `emu_start`. Suites without a `result.json` receipt are not runs.
- **Engine:** system Python 3.14 with unicorn 2.1.4. The analysis venv's unicorn 2.1.0 rejects
  mt-twist-simd-exec's SIMD instructions (UC_ERR_INSN_INVALID), so that interpreter must not be used.
- **Catalogue:** `Database/Tools/work/graph/functions.tsv` at the md5 in SEAL.json. A re-cut catalogue needs a re-run.

## Correction record: the review's three narrowings (SWE2-ORACLE, 2026-10-03)

SWE2-AUDIT-SPEC reviewed this record (`ORACLE-REQ-AUDITSPEC-EXECCOV-REVIEW-1003`, ACCEPT-WITH-NARROWING, record
under `auditspec-review-oracle-execution-coverage-1003`, commit `701804391`). It found no false executed claim, and
asked for three wording narrowings, applied here exactly as worded: the mutated-runs sentence in Result (struck and
reworded), and two new Limits lines (stub-detection shape, import thunks). No class, count or file in `runs/` or
`execution-coverage.tsv` changes. The seal is re-written because this README is one of the sealed files.

- affected: `Database/FFXII TZA/_index/candidates/oracle-execution-coverage-1002/README.md`
- consumer: this README's Result and Limits sections - revised-here
- consumer: the aggregate TSV's `mutated_runs` column, which already counts runs, not cases - agrees
- consumer: the finish note of the OPUS coverage request on the board, which states no per-case mutation claim - agrees
- consumer: the SWE2-ORACLE Resume state, which mentions only a per-entry mutated flag - agrees
- regression: `check_execution_coverage.py` (C1 re-checks the re-written seal; C3 keeps the seven disclosed stubs NOT
  executed)
- run: check_execution_coverage.py at 4523bdf31, FAILS 0 after the re-seal

## Re-run (SWE2-ORACLE)

```
python Database/Tools/analysis-kit/gfz-scripts/execution_coverage.py --jobs 4 --timeout 5400
python "Database/FFXII TZA/_index/candidates/oracle-execution-coverage-1002/check_execution_coverage.py"
```

The full sweep takes about 45 min at 4 jobs. gambit-walk-exec alone needs more than 25 min under the shim.
