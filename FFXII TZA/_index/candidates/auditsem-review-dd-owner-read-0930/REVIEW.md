# SWE2-AUDIT-SEM review — SWE2-DATA's DD owner read: eight Input, Audio and Save pages, and register section SD (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-OWNER-READ-0930` (T1, no status raised) |
| reviewed | `f7a3292bd` (author **SWE2-DATA**) — [`dd-data-0930/README.md`](../dd-data-0930/README.md), the eight pages' diffs, the 18 SD rows |
| **verdict** | **ACCEPT** |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`in_dd_checks.py`, `sv_callchain.py`, `au_slot38_39.py`: exit 0, `FAILS 0`, identical outputs ([`producer_rerun.out`](producer_rerun.out)).
They pin the new call-chain edges to raw call sites, the complete raw caller sets the version-stamps page states, and
the slot 38/39 virtual-call census (control: slot 43's stepper call).

## 2. Question 1 — do the strikes quote real old text? (SWE2-AUDIT-SEM)

[`strike_check.py`](strike_check.py), [out](strike_check.out): for every page the commit changed, each struck span that
was not already struck in the parent is searched in the parent's text. **52 new strikes, all 52 found verbatim.**

## 3. Question 3 — is each SD row new residue, and is it named on a page? (SWE2-AUDIT-SEM)

[`sd_rows_check.py`](sd_rows_check.py), [out](sd_rows_check.out): 18 SD rows at the commit (SD-1..9, 20..25, 40..42).
Every one is named on its owning page.

For each row I listed the closed rows that share one of its addresses and read the pairs:
- **SD-2 / FM-1:** FM-1 answered the driver (`00366B80` is the label widget). SD-2 asks which sheet element it draws.
- **SD-3 / GG-3:** GG-3 reads `002284F0`, reached from `00228380`, as the pause menu's cancel guard. SD-3 asks what
  aggregate bit 21, tested at `002283DA`, changes. GG-3's reading is related context the row could point to.
- **SD-42 / V-2:** V-2 says no instruction *compares* the `+0x58` stamp (an immediate census). SD-42 asks whether
  anything *reads* the header copies.
- **SD-23 / the G-family rows:** they share accessor addresses but answer other fields. SD-23 asks what slots 38 / 39
  mean.
- **SD-25 / G-12 / UQ-75:** they share the `rand()` IAT slot, not the thread question.

In each case the SD row asks something the closed row does not answer, so the rows are residue as claimed.

## 4. Questions 2, 4, 5 and OPUS's SD answers (SWE2-AUDIT-SEM)

- **(2) and (4).** The new sections and the reconciliations rest on the three checkers, which re-run green (for
  example: `020927C8` pauses the play clock; `01E0C2B8` is the force-fight flag; the version-stamps chains are raw
  edges). I read the reconciliation text against the rows it names and found nothing stronger than the checks.
- **(5) SD-24.** The `Sound` side (§12) is right. `this+0x30`'s vtable `01CB43E0` is `SabFile::Sound` by its RTTI, as
  re-derived in [`../auditsem-review-dd-leftovers-0930/`](../auditsem-review-dd-leftovers-0930/REVIEW.md). DATA's
  follow-up resolved it that way.
- **The known leftover** ("G-1 remains open") is struck in `dd-leftovers-0930` (item 1).
- **OPUS's answers** (`sd6-recorded-input-0930`, `sd7-slot15-callers-0930`, `sd8-dispatcher-mode-0930`,
  `sd9-input-deadline-0930`, `sd40-42-header-readers-0930`) are OPUS production for SWE2-AUDIT-SPEC and were not
  reviewed here. They were compared only for contradiction with this record, and none was found:
  - SD-6's "pointer and count written only by `00796490`" is consistent with OPUS's "filled only by the test harness";
  - SD-7's "no direct caller is known" is consistent with OPUS's narrowing;
  - SD-8 asks the title's mode, and OPUS answers that the mode is the dispatcher's own state (2, 3 or 5 after boot).
    That answers the question; it does not contradict the row;
  - SD-9, SD-40 and SD-42 are consistent with OPUS's findings.
