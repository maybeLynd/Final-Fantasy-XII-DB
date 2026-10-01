# A16 verdict-finish gate: scoped independent ACCEPT

The assigned `OPUS-REQ-ASTRA-VERIFY-A16-FINISH-GATE-0929` requirements pass
through the actual supported writer. This accepts OPUS's finish-admission repair,
not the complete deployed A16/M2 workflow or the L1+L2 database endpoint.

The current source is pinned separately from assigned repair `ed127d443`:

- team.py: b1faa731aa6d4edf638f869f679f19a0f28f0703b98f8faae0b7cc6847b5dcd6
- transitions.py: 188ed23c635d0d037fc171074a2da5d7b97c1788ec27faa7ca2b0b0eccf86555

Both current and assigned source bytes are retained. The verdict parser's AST
matches the assigned repair. The current gate uses exactly one whole-string
policy verdict; it does not normalize it. Later code changes in either file are
not silently claimed to be identical to the whole assigned snapshot.

| Independent requirement | Actual result |
|---|---|
| Missing verdict, trailing LF, two different verdicts, PARTIAL, lower case | All five CLI finishes refused; task remains ACTIVE and board bytes unchanged |
| Six policy verdicts | All six admitted, including the four requested controls; exact refs retained |
| Plain research without reviews | Admitted unchanged |
| ACCEPT-WITH-NARROWING | VERDICT-MANUAL, no next operation; checked in imported plan and actual CLI |
| Current live-board validation | Read-only CLI passes; all 55 named historical rows still present |

Cases use actual `team.apply` to prepare a disposable board and actual `team.py`
CLI/transaction to finish it. Before/after bytes, operations, actual exits,
stdout/stderr, result reductions and private transaction journals are preserved.
Source hashes are checked before and after. A missing upstream result cannot
become a success. No producer test suite was imported or credited as our run.

The first attempt stopped at an invalid lowercase fixture task id before any
finish case. Its original driver, partial preparation and outer exit1 remain.
The repaired input uses supported uppercase ids in a fresh run. `actual-cases-02`
and `verification-run-02.*` are the valid run; no failed or zero-case run passes.
No evidence depended on the failed seed. Old ASTRA reproduction `7068c250a`
demonstrates the former defect and is reused, not rerun against repaired code.

For a future rerun, copy only the preserved driver to a new empty owned directory
inside this repository, then run it with the existing analysis Python. It refuses
an existing `actual-cases-02`; published case/result bytes must stay immutable.
Compare the pinned source before interpreting a run on a later generation.

Limits: no production transition was executed by this test, no host-adapter or
whole-project acceptance is implied, and existing history was not rewritten.
Other lanes may change the live board concurrently; the test does not assert its
global bytes stayed unchanged. All writer argv explicitly name private fixtures.
All child calls terminated; no private lock remains. No game/PC/input/native
instrument/save/config/reference or peer-process mutation.

Player version: the project's review mechanism now rejects an ambiguous result
instead of marking it finished and leaving the knowledge stuck between workers.
Reviewed findings still need their owning pages to consume them.
