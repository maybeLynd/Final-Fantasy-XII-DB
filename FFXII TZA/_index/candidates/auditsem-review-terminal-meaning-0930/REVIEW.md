# SWE2-AUDIT-SEM review — DASHBOARD-MEANINGS §4e (the terminal count) and the heading page's alias evidence row (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-TERMINAL-MEANING-HEADING-ALIAS` |
| reviewed | `4e32dd8df` (author **FABLE**) — `_index/workflow/DASHBOARD-MEANINGS.md` §4e; the new evidence row in `06-Movement-And-Navigation/heading-speed-to-position-delta.md` |
| sources read | `_index/FINAL-AUDIT-PROTOCOL.md` (preamble, lines 15–17, "Recording" 133–141); `gfz-scripts/goal_gate.py` `check_acceptance` |
| **verdict** | **ACCEPT-WITH-NARROWING** — §4e reads the protocol right on every point asked; one condition the protocol attaches to a counting run is missing from "`T` is 30 only when …" (§1). The evidence row holds. |

## 1. §4e against the protocol (question 1) (SWE2-AUDIT-SEM)

- **0 or 30.** The protocol: "If any pass disproves anything, fix it by evidence and restart all thirty from pass 1.
  Passing 29 and failing 30 means you have run zero complete audits" (lines 15–17), and "One AUDIT-LOG.md entry per
  complete run … A run that restarted after a failure is logged as a failed run plus a new run — never amended into a
  pass" (133–138). An accepted `T` of 0 or 30, never between, follows. **Holds.**
- **A partial streak is observed progress, shown apart.** Nothing in the protocol lets a partial run be counted; showing
  it as "observed, not accepted" beside `T` is the only honest display. **Holds.**
- **A failed pass or drift ends the run.** A failed pass: lines 15–17. Drift: the finishing run is "in one uninterrupted
  run, against a program state" (140–141), and a fix is a new program state. `goal_gate.check_acceptance` implements the
  same: a receipt counts only if its commit is an ancestor of `HEAD` and `git diff` shows no change in the database since
  (AUDIT-LOG and `_inbox` excluded). **Holds.**
- **Missing condition.** The protocol's preamble and its finishing sentence attach preconditions to a counting run: it is
  run "only when … unresolved = 0, every system documented, OPEN-QUESTIONS.md empty, and check_provenance green", and the
  database is finished by a clean run "against a program state with unresolved = 0". §4e makes `T` = 30 on the
  acceptance check alone, and `check_acceptance` does not test those preconditions (the other gate families do). A clean
  thirty-pass receipt against a state that failed a precondition would read `T` = 30 under §4e's wording.

## 2. The heading evidence row (question 2) (SWE2-AUDIT-SEM)

Every byte the row cites reads as stated ([`heading_own.out`](heading_own.out); the same derivation is the basis of
[`../auditsem-review-heading-alias-0930/REVIEW.md`](../auditsem-review-heading-alias-0930/REVIEW.md)): `002E438B mov r14, r9`;
the clear `002E4389`–`002E4394`; the reads `002E43BC` / `002E43C2` / `002E43C7`; the caller's `002E50C0 lea rdx,
[rsp+0x30]` and `002E50BD mov r9, r14` with `r14 = r8` at `002E504C`; and `002E45E0` spans 963 bytes with 21 call
instructions. The row claims a conditional calculation, not a run, and keeps partial overlap, `sqrtf`, `+0xF8` and live
pointers out of scope. It states only what the bytes support.

## 3. Narrowing (exact wording; FABLE applies it) (SWE2-AUDIT-SEM)

- **N1 — §4e first bullet.** After "It is 30 only when `goal_gate`'s acceptance check passes: a committed receipt of one
  complete clean run, naming a program state that is an ancestor of `HEAD`, with no database drift since" add *"and whose
  program state met the protocol's preconditions (unresolved = 0, every system documented, the register empty,
  `check_provenance` green); a receipt against a state that did not is not a counting run."*
