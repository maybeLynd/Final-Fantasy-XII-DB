# Standing checks for the defect classes the audit found (OPUS, 2026-10-03)

*The user's root-cause directive, items 3, 5 and 6, and the "weak tests" class of item 4. Companion to
[`opus-derived-binding-1003`](../opus-derived-binding-1003/README.md) (items 1, 2, 7, published `890844135`).*

## Item 6 — accepted corrections could be silently reverted (OPUS)

**Visible symptom.** The expanded L2 audit found corrections whose later edits restored older semantics.

**Root cause.** Every correction ships a regression that fails on the pre-correction text, named in its
consumer-check record. **A regression ran exactly once — at the correction's own publish — and never again.** No
mechanism re-ran it, so a later edit that restored the old semantics passed every gate.

**Shared mechanism.** [`run_correction_regressions.py`](../../../../Tools/analysis-kit/gfz-scripts/run_correction_regressions.py)
discovers every regression the consumer-check records DECLARE (their `Regression:` lines, with the declared invocation —
e.g. `check_questions.py --db`; a script a consumer table merely mentions is not one) and runs them all against the
current tree. A regression legitimately superseded by a later accepted correction is listed in
[`_index/correction-regressions-retired.tsv`](../../correction-regressions-retired.tsv) with the superseding record and
the reason — a reviewable claim, never a silent skip; a retirement naming no existing record fails the run.

**Current result** ([`correction_regressions.out`](correction_regressions.out), [`.json`](correction_regressions.json)):
**137 declared, 4 retired, 137 run — PASS 130, FAIL 4, MISSING 3.** Triage:

| regression | state | reading | route |
|---|---|---|---|
| 4 OPUS appliers (`gi_register.py`, `apply_12items.py`, `apply_10status.py`, `apply_13rewards.py`) | retired | appliers declared as regressions; two anchors superseded by later accepted answers/corrections (`opus-gi19-sway-layout-1001`, `opus-licence-buy-gil-cost-1002`), two intact by `git blame` (line last changed by the record's own commit) | OPUS, retired with evidence |
| `swe2contract-awn-wave-a-1001/awn_a_checks.py` | FAIL 50 | a correction's checks fail on the current tree: reversion or supersession, to be read by the owner | SWE2-CONTRACT |
| three `auditsem-review-*-0930/*_sem.py` | FAIL | each reads a path that no longer exists: the declared regression is not re-runnable | SWE2-AUDIT-SEM |
| three `box3-answers-0927/*.py` | MISSING | the record declares scripts that were never committed | FABLE |

The runner's own self-test ([`correction_regressions.selftest.out`](correction_regressions.selftest.out)): a declared
regression is parsed with its invocation, a bare name resolves in its record, a table mention is not a regression, a
regression that holds passes, a reverted correction fails, a declared but absent file is MISSING.

## Item 4, weak tests — a replay that cannot fail (OPUS)

**S-46 I5** (SWE2-AUDIT-SPEC item 4 #14): the replay's I5 asserted that `"gfx"`-tagged writes lie in
`[01F7F600, +0x9C4)` — true by construction, because the tracer tags `"gfx"` only inside that interval — and the
corrected I5 (2026-09-29: the index is a pointer and a count, reset by the twist) was never examined.
[`s46-opus-replay-routing-strict/check.py`](../s46-opus-replay-routing-strict/check.py) now asserts, each able to fail:
**S** all 624 state dwords written; **P** the cursor qword `01F7FFC0` written with `01F7F600`; **C** the count dword
`01F7FFC8` written with `0x270` — and a **control**: each part is re-evaluated with the one write it reads removed and must
then fail (`i5_control` all False in [`result.json`](../s46-opus-replay-routing-strict/result.json)). Measured first in a
scratch copy: the seed writes the count `0x270` and the cursor `0x1F7F600`; the cursor cell lies inside the old `"gfx"`
window, so the old span check had counted it as state. The package now enforces the unicorn pin
(`check_unicorn.require_pinned_unicorn()`, SWE2-AUDIT-SPEC item 5).

**A package-level cannot-fail shape, systemic:** 65 OPUS replay packages recorded `"ok"` in `result.json` but always
exited 0, so no automated re-run could see one fail. 64 now exit from their own recorded verdict (a uniform tail, no
logic touched) and S-46 exits explicitly; `s16-opus-replay-placement-strict` writes another file name and is listed
for a hand fix.

## Item 5 — PARTIAL/REOPENED pages and their obligations (OPUS)

FABLE's `check_status_residue.py` (`f3b0b29d4`) already failed an UNMAPPED non-final page. Three gaps remained, each now
closed in it:
1. only PARTIAL/REOPENED/STUB were examined — **every status word outside the explicit FINAL set (AUDITED,
   DOCUMENTED) is now non-final** (fail closed), so a new "DRAFT" or "PROVISIONAL" is examined;
2. a waiting state was accepted on WORDING ("review pending") with no identifier — **it now needs an exact identifier
   that resolves**: an open board task id or an existing record, else UNMAPPED;
3. a page whose named rows are all closed is reported as **STALE-STATUS** (re-status it), apart from UNMAPPED.
Self-test 11 cases ([`status_residue.selftest.out`](status_residue.selftest.out)). Live
([`status_residue.out`](status_residue.out)): 369 production pages — AUDITED 233, DOCUMENTED 119, PARTIAL 17; all 17
map to a live register row; WAITING-ID 0, STALE-STATUS 0, UNMAPPED 0; **FAILS 0**.

## Item 3 — `knowledge.sqlite` (OPUS)

The mirror's own fail-closed dependency check was already right (stale query refused, exit 2; `--snapshot` labelled
as-of). Added: **test 11** (stale → normal query refused → snapshot query allowed and the mirror still stale → `--refresh`
→ CURRENT with a new `built_at`) — [`test_knowledge_db.out`](test_knowledge_db.out), 11 tests pass. The gap was that no
checkpoint refreshed it: `checkpoint_consistency.py --refresh-mirror` rebuilds a STALE mirror through the existing
guarded build at a checkpoint (no second freshness system), and the return-package build uses it.

**Two findings at the refresh itself (after `ed8a9c03d`).** (1) Every unpinned mirror build failed: four untracked
files literally named `NUL` (a `> NUL` redirect in a POSIX shell) sit in `_experiments/evidence/` folders, and the
build's `os.path.relpath` maps that name to the Windows null device. `knowledge_db.tree_files` now skips Windows device
names; the build completes and `test_knowledge_db.py` still passes (11). (2) `dep_digest` compares a build with the
worktree always - SWE2-DATA's stated design - so in an active fleet even a mirror pinned at HEAD reads STALE within
minutes of any peer's uncommitted edit; no checkpoint can carry a CURRENT mirror. A committed-state check mode is
routed to its owner (`OPUS-REQ-DATA-MIRROR-COMMITTED-FRESHNESS-1003`), not changed here.

## Limits (OPUS)

The regression runner proves only what each declared regression asserts. A correction whose record declares no
regression is not covered; the runner counts declarations, it does not create them.
