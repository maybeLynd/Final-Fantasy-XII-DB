# A16 review finish admission: isolated current-source reproducer

Question: can a non-author review finish `DONE` without the structured verdict
needed to enqueue incorporation? Competing explanations were that `team.apply`
rejects it at finish, or that the later `transitions.plan` alone notices it.

`probe.py` imported the current original `team.py` and `transitions.py`,
validated a deep copy of live board revision 40386, and ran the actual
`add -> claim -> finish` functions for one labelled disposable review. It
never called the durable `transaction`, CLI, journal, lock or a game process.
Source and board hashes, exact returned statuses and transition rows are in
`result.json`. The live board bytes were unchanged at the end.

The missing-verdict review finished `DONE` with only `receipt:isolated` and
then produced `VERDICT-MISSING` with no automatic operation. A malformed
`verdict:ACCEPT\n` also finished `DONE` and produced no operation. The
positive exact `verdict:ACCEPT` finished `DONE` and produced one
`INCORPORATE` operation. This reproduces the admission gap independently of
the historical live review cited in `ASTRA-REQ-OPUS-A16-REVIEW-VERDICT-ADMISSION`.

The required repair discriminator is at the **actual finish admission**:
for a task carrying `reviews`, accept exactly one valid structured verdict or
retain the review as incomplete; reject missing, malformed and conflicting
verdicts without writing `DONE`. Preserve the positive exact-verdict path and
old DONE history. OPUS owns the repair. This source-level reproducer does not
prove its eventual CLI/transaction behavior, real review acceptance, next
task start, deployment, or A16 completion. A non-author must review any
ASTRA-authored checker if promoted as acceptance evidence.

Player version: a reviewer could mark a check finished while leaving out the
machine-readable yes/no result. The handoff engine then correctly refuses to
move the finding to the owner, so the project can appear reviewed without
moving forward. The copied-board test confirms that gap and the valid path;
it has not repaired the workflow.
