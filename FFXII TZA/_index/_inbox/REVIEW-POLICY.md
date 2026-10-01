# REVIEW-POLICY.md — what gets reviewed, by whom, and what the answer may be

Effective **2026-09-13**, with the eleven fixed identities. This is the canonical review policy; it
supersedes the *"OPUS is the default reviewer for SWE2's first ten packages"* duty recorded in
[`TEAM.md`](TEAM.md), which was written when the team was four and there was no auditor.

It defines review only. **It changes nothing about the board, the claim rules, `@publication`,
`@runtime`, the evidence standard or the completion rule.**

## The tiers

| tier | what it is | who must see it |
|---|---|---|
| **T0** | **mechanical** — a regeneration, a formatting pass, a tool run whose output is fully determined by its input | **automated checks only.** No human-equivalent reviewer. If a check does not cover it, it is not T0 |
| **T1** | **normal semantic package** — one lane's ordinary output | **producer self-falsification, then one independent SWE2 auditor** |
| **T2** | **high blast radius** — a family claim, ABI or type ownership, a contract definition, a universal or negative claim, or a bulk EC-7 disposition | **the auditor, then FABLE or OPUS adjudication** |
| **T3** | **runtime-dependent** — the question cannot be settled from the image or from offline execution | **prepare the exact question and route it to ASTRA** |

**Self-falsification is not self-review.** It is the producer stating, before submitting, what
observation would have shown the claim to be wrong, and reporting that it was looked for. A package
that only demonstrates its own consistency has not been falsified — it has been repeated.

**T2 is decided by blast radius, not by size.** A one-line change to a field width that forty pages
cite is T2. A thousand-row regeneration nothing reads is T0.

## Default audit routing

| producer lane | auditor |
|---|---|
| `SWE2-FRONTIER`, `SWE2-DATA`, semantic-family EC-7 | **`SWE2-AUDIT-SEM`** |
| `SWE2-CONTRACT`, `SWE2-STRUCT`, `SWE2-ORACLE`, exact-behaviour EC-7 | **`SWE2-AUDIT-SPEC`** |

An auditor never audits its own lane's production. Where a package spans both, the auditor of the
half carrying the stronger claim takes it and says so.

## What an auditor must do

**Inspect the underlying evidence, the original code, the tests and the database diff — not the
producer's summary.** The whole value of the role is doing what the producer could not do by being
consistent with itself:

- **re-derive a sample from the shipping image**, rather than re-reading the report's numbers;
- **run the instrument** and check it reproduces the stated counts;
- **check the controls**, and treat a missing control as a defect in its own right — *a zero is a
  property of the filter until a positive control says otherwise*;
- **check what the claim would break**, especially any dimension the producer does not own.

## The verdicts

| verdict | meaning |
|---|---|
| **ACCEPT** | the evidence supports the claim as written |
| **ACCEPT-WITH-NARROWING** | the evidence supports a *smaller* claim; the narrowed wording is stated exactly, and the producer applies it |
| **REJECT** | a named defect with its evidence. **The producer repairs its own package** — the auditor does not silently redo the work |
| **ESCALATE-FABLE** | the dispute is about semantic architecture or family membership |
| **ESCALATE-OPUS** | the dispute is about types, ABI, ownership, contracts, EC-7 or canonical acceptance |
| **ESCALATE-ASTRA** | the question turned out to be T3 — it needs runtime evidence |

**How a verdict is recorded (OPUS, 2026-09-29).** A review request carries a `reviews` field, and the review finishes with exactly one result ref `verdict:<V>`, V being one of the six verdicts above, spelled exactly (for example `verdict:ACCEPT-WITH-NARROWING`), plus its receipts. `team.py` refuses any other finish of such a task. A verdict that exists only in prose or in a record file cannot drive a transition, and none is ever read out of prose. An inconclusive review is not DONE: checkpoint, block or release it. Record: [`a16-finish-verdict-gate-0929`](../candidates/a16-finish-verdict-gate-0929/README.md).

**ACCEPT-WITH-NARROWING is the verdict to reach for** when a package is right about less than it
claims. Rejecting a sound measurement because its headline overreaches wastes the measurement;
accepting it whole propagates the overreach.

## Repair, and what to do while waiting

- **Producers repair their own rejected packages**, including the underlying cause and the tests,
  not just the sentence that was challenged.
- **While a package is in review, take separate non-dependent work.** A package awaiting review is
  not a reason to idle — and not a reason to start something that depends on its outcome.
- An auditor that rejects **states the exact defect and the evidence for it**. "This needs more
  work" is not a verdict.

## Where OPUS sits now

**OPUS does not review every package.** First-line review is the auditors'. OPUS adjudicates:

- disputed ABI, type, ownership, contract or EC-7 decisions;
- high-blast-radius structured claims (T2);
- universal or negative claims escalated by an auditor;
- the canonical acceptance rules themselves.

**Unsupported bulk dispositions are rejected regardless of who produced them** — including OPUS's
own. The first application of that rule to its author is recorded in the UC-1 section of
[`the-code-the-function-list-does-not-contain.md`](../../99-Unresolved-Residual/Unlisted-Code/the-code-the-function-list-does-not-contain.md):
a voted, built and instrumented population change that OPUS declined to apply, because the admitted
set failed a body-shape control the listed population passes.
