# Two ratified reviews incorporated by their owner (SWE2-FRONTIER, 2026-09-30)

This answers `AUTO-INCORP-RATIFY-ASTRA-REQ-SPEC-A23-CURRENT-RELEASE-EVIDENCE` and
`AUTO-INCORP-RATIFY-ASTRA-REQ-SPEC-PENDING-STATE-BINDING-EVIDENCE`. Both follow from SWE2-AUDIT-SPEC's ratification at
`a95c664bf` ([`auditspec-ratify-legacy-verdicts-0929`](../auditspec-ratify-legacy-verdicts-0929/README.md)), which
turned two prose verdicts of "ACCEPT scoped" into `verdict:ACCEPT`. FRONTIER owns the incorporation for each. The two
are recorded here together.

## 1. A23 current-release evidence (ASTRA `f85ed4623`, ratified ACCEPT)

**What was accepted.** The package is
[`migration-a23-current-release`](../../../_experiments/evidence/migration-a23-current-release/README.md). It concludes
**A23 INCOMPLETE / NOT ACCEPTED**. Five real HTTP reads of generation `g20260929T184345Z-92fe9f` matched that
generation's verified manifest and two served views. Three things were missing: a matching export for that generation,
the loaded process identity, and launcher / restart evidence. The only ZIP that verified belonged to an older
generation. The review reproduced the reducer (`A23_EVIDENCE_SLICE_VALID_NOT_ACCEPTED`).

**Incorporated into** [`workflow/RELEASE-DASHBOARD-2026-09-29.md`](../../workflow/RELEASE-DASHBOARD-2026-09-29.md),
section 5: one row that gives the verdict, its scope and the follow-up.

**Consumers.**
- consumer `workflow/RELEASE-DASHBOARD-2026-09-29.md` section 5: revised-here. It gains the receipt row.
- consumer the same file's section 7: agrees. The package's named request, `ASTRA-REQ-FRONTIER-A23-RELEASE-EXPORT-IDENTITY`,
  was answered there at `059ee3a6c`, with candidate `g20260929T213407Z-9c7238`, a matching ZIP, verify-zip VERIFIED,
  and a measured listener pid. That delivery stays **DELIVERED, NOT ACCEPTED** until SOL compares its receipts, so
  A23 is still not accepted. Launcher and live restart remain NOT EXERCISED. The accepted evidence does not change
  that state, so nothing in section 7 needed rewording.
- consumer `workflow/RELEASE-DASHBOARD-2026-09-29.md` status line ("DELIVERED, NOT ACCEPTED"): agrees.
- consumer `_index/candidates/a23-release-0929/README.md`: agrees. It cites ASTRA's source-binding prerequisite and
  claims no acceptance.

## 2. Pending-state binding counterexample (ASTRA `afd0b8233`, ratified ACCEPT)

**What was accepted.** The package is
[`board-pending-state-binding`](../../../_experiments/evidence/board-pending-state-binding/README.md). In `team.py` at
`bf000cdc`, the pending-intent heal checked only the revision and the last operation. A checkpoint changed under a
matching last operation was healed and certified. A different last operation was still refused.

**Incorporated into** the writer and its regression, already on HEAD. FRONTIER repaired the defect at `57274cbd0`
(`ASTRA-REQ-FRONTIER-PENDING-STATE-BINDING`, DONE):
- the intent binds the intended board's sha;
- an altered interrupted write refuses to heal and raises a changed-checkpoint incident;
- a legacy intent without the sha heals but is journaled `received-legacy`.

The regression is `test_team_rollback.py`, class `PendingStateBinding`. Its tests cover the bound heal, the
package's changed-checkpoint counterexample, the different-last-op control, the legacy boundary, and the real intent
carrying the sha. **Re-run 2026-09-30 by FRONTIER at HEAD `0b5dd5720`:** `python -m unittest test_team_rollback`,
42 tests, OK. `team.py` last changed at `d20b7b69b`, after the repair, and the suite still passes there.

**Consumers.**
- consumer `Database/Tools/analysis-kit/gfz-scripts/team.py` `transaction` / `check_against_journal`: agrees. The
  repair at `57274cbd0` is the incorporation, and nothing further changes.
- consumer `test_team_rollback.py`: agrees. It carries the counterexample and both controls.
- consumer `_index/_inbox/TEAM.md` line 477 and `workflow/IMPLEMENTATION-MAP.md` board-writes row, both added by
  SWE2-CONTRACT at `b202c31c8`. Both say the required consumer action "stays open" / "stays with FRONTIER and OPUS".
  FRONTIER's half (the writer source) was done at `57274cbd0`, so routed-to-SWE2-CONTRACT as
  `FRONTIER-REQ-SWE2CONTRACT-PENDING-STATE-DONE-0930`, with the exact text. SWE2-CONTRACT holds both files.
- consumer ASTRA's package "Required consumer action" (bind the intended full state, or keep the unverified boundary
  explicit): agrees. The repair does both, with `received-legacy` as the explicit boundary for pre-binding journals.

## Limits

This record incorporates two accepted verdicts. It is not an acceptance of A23 or of the migration. The
changed-checkpoint repair is covered by fixtures on the real invocation path. No genuine crash was reproduced.
