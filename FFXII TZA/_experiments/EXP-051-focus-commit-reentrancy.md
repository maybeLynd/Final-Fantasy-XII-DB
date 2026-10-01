---
experiment: EXP-051
title: deferred focus publication after controlled teardown replacement
status: COMPLETE - bounded isolated original-code evidence
contract: none - Deferred focus commit 00358BC0 is outside the existing party-slot assignment contract; controlled teardown changes do not prove native reentrancy.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original deferred commit with recording stubs and labeled pending/kind interventions; new-actor tail callee omitted.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-051-focus-commit-reentrancy/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-051: deferred focus publication after controlled teardown replacement

**Result:** ten original-body controls passed; omitting the pending-handle reread
was detected. ASTRA, 2026-09-11. Native callees are controlled dependencies, not
executed game behavior. No game process was accessed.

## Question and authority

The [party page](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md)
says teardown can replace the pending focus request. This experiment tests the
original commit's ordering and response to that controlled intervention. It also
distinguishes an entry guard from later request-kind reads.

[check.py](evidence/EXP-051-focus-commit-reentrancy/check.py) verifies the certified
executable hash and extracts the complete 156-byte `00358BC0` body through RET at
`00358C5B`. Exact [bytes](evidence/EXP-051-focus-commit-reentrancy/function.bin) and
[disassembly](evidence/EXP-051-focus-commit-reentrancy/disassembly.txt) are retained.

## Original publication sequence

The entry tests byte request kind at `022C7FF8`; zero returns immediately. Otherwise
it loads pending dword `022C7FE4` and current dword `022C7FE0`. If they differ:

1. Resolve the old current handle through `003588B0`.
2. Call `00358B40`, then `00259800(0)`.
3. Choose `0025A680(oldActor,0)` when the cached old handle is nonzero and the
   **then-current** request kind is not 2; otherwise choose `0025A690(oldActor,0)`.
4. Reread pending at `00358C24` after that teardown call returns.

Equal handles skip that sequence. Both paths then write current at `00358C2F`,
clear the request-kind byte at `00358C35`, and resolve the published handle.
A null resolution returns. A nonnull resolution restores the stack and
tail-calls `002681D0(newActor)` at `00358C52`.

## Controlled cases

Each case uses fresh Unicorn memory and a patterned page containing all three
globals. Resolvers, preparation and teardown calls have explicit recorded stub
results. Selected stubs can change pending/kind; these changes are logged as
**controlled interventions**, separately from original-instruction writes.
They demonstrate how the caller responds if a native callee performs that change;
they do not prove any native callee actually does so.

| Input/intervention | Observed local result |
|---|---|
| Entry kind 0 | return, no calls or non-stack writes |
| Current equals pending | no teardown; current written, kind cleared, new handle resolved |
| Different handles, kind 1 | ordinary teardown, pending published |
| Different handles, kind 2 | alternate teardown, pending published |
| Old current zero, kind 1 | alternate teardown |
| Teardown replaces pending with 3333h | replacement published |
| Teardown replaces pending with zero | zero published |
| Preparation changes kind to 2 | alternate teardown selected by the later read |
| Preparation changes kind to 0 | commit still publishes; no second cancellation guard |
| Equal handles, nonnull new resolution | publication occurs, then stop before native `002681D0` |

For nonnull old resolution the stub returns a fixed synthetic actor. The old-zero
case deliberately uses the same controlled resolver return to test the branch's
dependence on the cached handle, not on actor nullness. Native zero-handle resolver
behavior is separately established by EXP-034 and is not redefined here.

Every stub legally clobbers volatile RCX to BADF00Dh. This distinguishes the
explicit reread from accidentally relying on a callee leaving the desired value
in a register. Full-page equality, exact call identity/arguments/order, and the
two original global stores (current dword, then kind byte zero) are asserted.
Return paths require RSP+8 at the sentinel; the new-actor tail path requires the
original stack and actor argument at its unexecuted callee boundary.

A private mutant replaces only the six-byte pending reread with NOPs. It publishes
the volatile-register clobber instead of the controlled replacement; both the
memory and resolver-argument checks reject it. Original bytes are unchanged.
[Results](evidence/EXP-051-focus-commit-reentrancy/result.json) retain every trace,
call, original store, intervention and before/after global state. The
[manifest](evidence/EXP-051-focus-commit-reentrancy/manifest.json) seals this package.

## Limits and integration

This supports deferred publication and the documented post-teardown reread. It
does not demonstrate concurrent thread safety or real native reentrancy. A new
request made by the controlled teardown is consumed by this commit because its
kind is subsequently cleared; later native effects are untested.

The party page's categorical "nothing is notified" and no-frame-lag conclusion
need separate evidence: this body invokes preparation/teardown callees and a
new-actor tail callee whose downstream effects this experiment does not cover.
Their presence alone does not prove a notification, but these local controls
cannot prove global absence of one. Return that scope concern to FABLE alongside
the positive ordering evidence. Run `check.py` with the existing Windows Python
and Unicorn environment; all objects and interventions are synthetic.
