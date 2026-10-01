# Assigned A16 gate verification

Question: does the supported finish CLI refuse ambiguous/malformed review verdicts
without changing the task, admit the policy verdicts, preserve plain research,
and distinguish narrowing from missing verdicts?

This is a direct completion prerequisite, not optional dashboard work. Existing
ASTRA reproduction7068c250a already demonstrates the old defect; do not rerun it
against the repaired source. OPUS ed127d443 owns the repair. ASTRA owns only these
bounded independent fixtures/receipts; no shared source edits.

Method: requirement-derived offline actual team.apply seed and team.py CLI finish
on new disposable boards. Five specified invalid forms, all six policy verdicts
(including the four explicitly requested), plain research and real transitions.plan.
Use current live-board validation read as a separate control. Require actual exit,
before/after bytes, task state and result refs; no stdout-only PASS. A prerequisite
failure invalidates the run. Check source identities before/after. Preserve any
failed attempt; never overwrite it or silently repeat the same failed method.

No test writes the live board; peer writes may change it concurrently. A live
board unchanged assertion would therefore be inappropriate. No game/PC/native
instrumentation, production transition, deployed host test or full A16/M2 award.
