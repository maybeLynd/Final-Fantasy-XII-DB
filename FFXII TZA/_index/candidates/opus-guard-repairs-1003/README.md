# Recurrence-prevention guards repaired after independent review (OPUS, 2026-10-03)

*The user's directive of 2026-10-03, which continued from `FFXII_ROOT_CAUSE_CORRECTIONS_RETURN_2026-10-03`. Four
defects in the guards that return shipped. Each one is repaired at the mechanism, carries a discriminating regression,
and has its current instance repaired. Item 4 was implemented by repos-91, a local helper session that wrote no git;
OPUS reviewed and published it.*

## 1. The correction-regression runner counted false passes (OPUS)

| | |
|---|---|
| **Visible symptom** | `correction_regressions.json` recorded PASS for `b20_checks.py` (its output: `FAILS 1`) and `awn_b_checks.py` (`FAILS 5`). The advertised PASS 130 was not trustworthy. |
| **Root cause** | `run_one` classified by the exit code alone. Legacy checkers print their verdict and exit 0 regardless. |
| **Shared mechanism repaired** | `run_correction_regressions.py` `classify(returncode, output)`. A nonzero exit is FAIL. With exit 0, an explicit summary (a line ending in `FAILS N`, or `self-test: N failure(s)`) with N > 0 is FAIL. A malformed summary (`FAILS ?`, `FAILS -1`) is UNINTERPRETABLE, and fails closed. Prose that merely mentions FAILS is not a summary. With no summary, the exit-code contract applies. The totals line and the exit status count UNINTERPRETABLE as bad. The grammar was fitted to the real outputs of all 139 declared regressions: 124 carry the token, and only the two above carry N > 0 with exit 0. |
| **Current instance repaired** | `b20_checks.py` and `awn_b_checks.py` now exit 1 on their own fail count. Their checks are unchanged. Both failures are stale expectations, not reversions, and were routed to their owners (below). |
| **Regression added** | `run_correction_regressions.py --self-test`: 16 cases ([`run_correction_regressions.selftest.out`](run_correction_regressions.selftest.out)), including the 5 the directive names and an end-to-end script that prints `FAILS 1` and exits 0. |
| **Census** | [`correction_regressions.out`](correction_regressions.out) / [`.json`](correction_regressions.json): the full re-run with the fixed runner (see its totals line). |
| **Routed** | OPUS-REQ-CONTRACT-B20-Z4-STALE-PIN-1003 (SWE2-CONTRACT): Z4 pins absolute line counts for an EOL invariant that still holds. OPUS-REQ-STRUCT-AWN-B-TH-SCOPE-1003 (SWE2-STRUCT): T/H compare whole pages with a frozen BASE, so later packages trip them. The FABLE box3 MISSING three are a declaration typo: bare names that resolve in the wrong record; the cause was noted on OPUS-REQ-FABLE-BOX3-REGRESSIONS-MISSING-1003, and the scripts pass at their real paths. The three audit-sem FAILs are fixed in SWE2-AUDIT-SEM's uncommitted work: run there, they exit 0 with FAILS 0. |

## 2. The exact-commit checkpoint stopped before C5-C8 (OPUS)

| | |
|---|---|
| **Visible symptom** | `checkpoint_consistency.py --rev HEAD` returned after C1-C4/C9, yet its receipt read like a full checkpoint of that commit. |
| **Root cause** | C5-C8 call tools that read the working tree, so they could only run against the moving worktree. |
| **Shared mechanism repaired** | `--rev REV` resolves REV to its SHA. It materializes that commit in a temporary detached git worktree under a short root (`C:\ck`; the deepest evidence paths overflow MAX_PATH under %TEMP%), with `Database/` and every root-level file of the commit populated. The shared worktree and its index are never touched. The untracked environment inputs the tools read (`Database/Tools/work/*` directories) are linked in read-only, one junction per directory, and listed in the receipt. The checker then runs in full mode there, using the commit's own tools. Cleanup removes and verifies each junction before removing the worktree; if a junction survives, cleanup refuses and names the tree. Output: `COMMITTED SNAPSHOT CHECK: <sha> PASS/STALE/FAIL`, or `WORKTREE CHECK: <HEAD>+<dirty fingerprint> ...`. The old reading survives as `--rev-partial`, labelled PARTIAL. |
| **Found while repairing** | The first full runs failed closed, never silently: on path length, then on the tracked files under `Tools/work`, then C7 on a missing root-level charter. Each was a materialization gap, fixed in the mechanism. |
| **Receipts** | The first full exact-commit run (at `e698134898072b01e1ec1e2776a24eb3982eba66`, before these repairs were committed) read C1/C2/C3/C5/C8 PASS, C6 STALE (the mirror), C9 STALE (the worklist), and C7 FAIL - the missing root-level charter, fixed in the mechanism. The receipt for the commit that carries these repairs is taken after it lands and ships in the return package, which names the exact SHA. |

## 3. C9 ordered the exclusion policy by calendar date (OPUS)

| | |
|---|---|
| **Visible symptom** | C9 called a runtime cell "old" when its newest date was not after 2026-10-03. A cell re-scored later on the amendment's own day passed as historical. |
| **Root cause** | A calendar date stood in for the policy's identity. |
| **Shared mechanism repaired** | `C9_POLICY` holds the durable identity: id `L2-RUNTIME-EXCLUSION-AMENDMENT-1`, the commit that made the amendment authoritative (`ed8a9c03da267369ef7024f358f5304e19ee821e`), the marker text, and the explicit 12-cell historical worklist. An uncited excluding cell is tolerated as STALE only if it is on the worklist AND its text is byte-identical to its text at the policy commit. Anything else FAILs, whatever date it carries. A worklist cell leaves the list by being re-read. |
| **Regression added** | `checkpoint_consistency.py --self-test` C9 cases: an unchanged worklist cell is STALE; a same-day re-score is FAIL; a new non-worklist exclusion is FAIL; a cell citing the amendment clears the worklist. |
| **Current state** | The worklist is unchanged: S-05, S-06, S-08, S-11, S-13, S-22, S-23, S-26, S-36, S-37, S-40, S-42. The verdict-parser unification stays routed (OPUS-REQ-FRONTIER-ONE-VERDICT-PARSER-1003, still READY); C9 imports `progress_report._cell_verdict` and never reimplements it. |

## 4. A STALE relabel kept the old reason (repos-91, reviewed by OPUS)

| | |
|---|---|
| **Visible symptom** | Relabelling an output that already said `STALE (moved: old.txt)` left that text in place, while the binding's `stale_moved` named `new.txt`. |
| **Root cause** | Idempotence was implemented as "leave an existing STALE line alone". |
| **Shared mechanism repaired** | `derived_binding.relabel()` rewrites an existing stale annotation in place to the current moved set and generation. It matches the rule's own template first, then the stale token with an optional parenthesised reason. Repeated relabels stay legal. An unchanged moved set reproduces identical bytes. |
| **Regression added** | `derived_binding.py --self-test` cases 14-19c ([`derived_binding.selftest.out`](derived_binding.selftest.out), 22 checks): reason A plus moved set B gives displayed reason B, the live template is rewritten in place, and an end-to-end gate run keeps the output and the binding in agreement. Cases 14, 15, 17 and 19b fail under the old behaviour. |
