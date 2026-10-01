---
experiment: EXP-047
title: attacker registration ends at a reset boundary
status: COMPLETE - bounded isolated original-code evidence
contract: ../07-Combat-Action/CONTRACT-commit-action.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original reset wrappers to delegate entry, then separate controlled-return cases; native delegate effects omitted.
contract_coverage: Attacker-mask lifetime constraint from reset wrappers 00322050/00322080; does not execute commit, native renewal delegate or live reuse.
tool: evidence/EXP-047-attacker-mask-reset/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-047: attacker registration ends at a reset boundary

**Result:** original code resets unit+EA4 and unit+EA8 before delegation. The
action-commit page's "once per attacker, ever" claim is corrected to suppression
while the corresponding attacker bit remains set. ASTRA, 2026-09-11. Offline only.

## Question and original authority

The commit path sets an attacker's slot bit in its target's mask and skips repeated
registration when that bit is set. Does that prove a permanent attacker history?
The unit access map identifies reset writers at `00322059/63`, `003220A3/AD`, and
reuse initialization. This experiment inspects the first two wrappers directly.

[check.py](evidence/EXP-047-attacker-mask-reset/check.py) verifies the certified
executable SHA-256 and extracts `00322050` (44 bytes), `00322080` (89 bytes including
its alternate tail-call path), and the five-byte getter `00263E30`, which loads
qword actor+30 into RAX. Exact bytes and
[disassembly](evidence/EXP-047-attacker-mask-reset/disassembly.txt) are retained.

## Original control flow

`00322050(unit)` unconditionally writes dword unit+EA4=0 and byte unit+EA8=0.
It passes qword unit+10 to `003220E0`, then writes returned EAX into unit+8.
It has no null-unit guard.

`00322080(actor)` first tests actor for null; if nonnull it calls the original
actor+30 getter and tests the resulting unit. With a unit, it clears the same
mask/count, passes **unit+10** to the delegate, and stores returned EAX into unit+8.
Without an actor or without its unit, it restores the wrapper's stack and
**tail-calls `003220E0` with the original actor argument**. Those paths perform no
local unit reset, but they are not a general no-op or an early return from the
full operation.

Static inspection of the delegate's opening shows additional native calls,
including `003589B0`, `002659D0` and `00327150`, plus a preferred-selector write
later in that function. Its full semantics and side effects are outside this
experiment. A null argument does not justify eliding that delegate.

## Discriminating controls

Every fixture starts with mask 80000021h, count 3, patterned surrounding bytes,
separate actor/unit pages and distinctive saved registers. The bound actor in
unit+10 deliberately differs from the input actor to distinguish forwarding.

| Entry/input | Local reset | Delegate RCX |
|---|---|---|
| Unit wrapper, nonnull unit actor | mask and count zero | unit+10 actor |
| Unit wrapper, null unit actor | mask and count zero | 0 |
| Actor wrapper, bound unit | mask and count zero | unit+10 actor, not incoming actor |
| Actor wrapper, null actor+30 | none | incoming actor |
| Actor wrapper, null input | none | 0 |

Five cases execute only original instructions and stop at the delegate entry,
before any delegate instruction or stub. Full-page equality and ordered write
addresses/widths require exactly a dword mask clear then a byte count clear on
reset paths. The actor page must remain unchanged. The originals therefore
establish those local effects without assuming the delegate succeeds.

Five separate cases inject a controlled delegate return of FEDCBA9876543210h,
with no delegate memory effects, to check only the wrapper's remaining behavior.
Reset paths write low dword 76543210h into unit+8; tail-call paths do not. All
reach the return sentinel with RSP+8 and saved RBX/RDI preserved. This gives the
stub no credit for native handle changes, preferred selector updates or any
other downstream behavior.

A private mutant replaces only the unit wrapper's mask-clear instruction with
NOPs. It still reaches the delegate, but the full-page/write-footprint comparison
detects the retained mask. The original bytes remain unchanged.
[Results](evidence/EXP-047-attacker-mask-reset/result.json) preserve all ten cases,
their exact instruction traces, writes, delegate arguments, before/after unit
snapshots and the fault control. The
[manifest](evidence/EXP-047-attacker-mask-reset/manifest.json) seals the package.

## Consequences and limits

The [commit page](../07-Combat-Action/the-moment-an-action-is-committed.md) now bounds
duplicate suppression by the lifetime of the recorded bit. No reset frequency,
live enemy lifetime, whole enmity model or new runtime observation is claimed.
The initializer's call to `00322050` remains a separate caller-level question;
the delegate is not reconstructed by these wrapper controls.

Run `check.py` with the repository's existing Windows Python and Unicorn library.
The inputs are embedded fixtures, not captured game objects. The first five
cases are original execution to an explicit stop boundary; the next five are
original wrapper execution with a controlled native dependency return.
