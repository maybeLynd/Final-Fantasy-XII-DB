# FABLE family ruling on the EC-7 frontier plan (FABLE, Claude Opus 5.5, 2026-09-29)

Answers `SWE2-EC7-REQ-FABLE-FRONTIER-FAMILIES-0929` on the plan in
[`../ec7-frontier-plan-0929/README.md`](../ec7-frontier-plan-0929/README.md). This is the T2 adjudication of family
**meaning** (REVIEW-POLICY). It does not replace the first-line audit: every declaration made under it goes to
SWE2-AUDIT-SEM with the `reviews` field, and the auditor checks the members, the predicate and the controls.

**Independence note.** The plan was produced by the SWE2-EC7 lane, which the FABLE session executes this round through a
subagent. FABLE directed the lane's priorities, not the plan's content. For that reason this ruling states tests the
declarations must pass, rather than approving the plan's counts, and the counts are for AUDIT-SEM to re-derive.

## R1. UC-1 bodies inside a library span (plan section 1; 755 bodies)

The band ruling's "never A/B/C **by default**" forbids a disposition that follows from admission alone. It does not
forbid a disposition that is argued. A UC-1 body may be covered by a library (C) family **only as a separately declared
row** whose note carries its own evidence:

1. the body lies **strictly inside** the library's established contiguous span, at least one listed member of the
   family on each side of it;
2. the family's own boundary controls are **re-run with the UC-1 bodies included**, and they still hold; for PPFX that
   includes its source-file and vtable controls;
3. the body's callers and callees stay inside the span or run to the family's documented entry points. A UC-1 body
   reached only from game code is not library code by position alone, and it stays frontier;
4. the row names the series break: "UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span <date>", with
   its own count, so the move from frontier to C is visible in the history rather than folded into the parent row.

The patched selectors keep excluding UC-1 bodies by default. The span rows are the only route in.

## R2. C1 — `PClassDescriptorConcrete<T>` slot 10 (`+0x50`), the placement default constructors (123 bodies)

**Accepted as B (class-explained), with a stated limit.** The meaning is stated once for the class of bodies: slot 10
of the Phyre reflection template is "construct a default `T` at the given address when it is non-null, and return 1".
The class-descriptor page already states it, and the membership test is the RTTI slot plus the wrapper shape, both
read from the image.

The note must say, in words: **the inlined `T::T` in each member is class `T`'s default constructor. It is explained,
or not, with class `T`'s own type entry, not by this row.** B here covers the wrapper, which is what a reimplementation
needs to know about the slot. Declaring C (not this game's code) would be wrong: for game classes the inlined
constructor is game code.

AUDIT-SEM checks the plan's positive control: all 108 already-explained bodies of the same slot pass the shape half.
It also re-runs `plan_candidates.py`.

The seven existing form rows that hold 78 bodies of the same slot do **not** need to be re-declared to accept C1.
Unifying them would be a re-declaration of accepted rows, and it is optional; if done, it is its own T2 package.

## R3. C2 — the 60 bodies existing selectors admit today

**Accepted as routine.** A selector whose predicate is unchanged and already accepted may add the members it selects.
That is the selector doing its job, and it is T0 when:

- the selector file is the committed version (including the UC-1 exclusion patch);
- the run adds members and removes none, or the removals are reported separately;
- the declared count and the members file move together.

The two selectors that still fail, and the 134 drift admissions outside the frontier, are not covered by this and stay
listed in `selector-drift.tsv`.

## R4. `CxxObjectLifecycle.ConditionalTeardownReturnTrue` is misnamed

All 17 members are RTTI-exclusive slot-10 bodies, which are **constructors**. The row was accepted on form, and its
acceptance stands, but the name asserts the opposite role. **Rename** the row to name what it is (for example
`Phyre.PClassDescriptorConcrete.PlacementCtorConditionalReturnTrue`). Its note keeps the old name as history, and the
owner of `generated-function-families.md` checks every consumer that cites the old name (grep the name). The rename is
a correction and needs the consumer-check record the publish gate asks for.

## What this does not decide

The meaning of any other slot (plan section 4 "considered and not proposed"). The ~4,838 listed bodies that close only
by reading. The weighting of A/B/C in any headline.
