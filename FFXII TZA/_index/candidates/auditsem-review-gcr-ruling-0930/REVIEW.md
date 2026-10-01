# SWE2-AUDIT-SEM review — FABLE's guarded class-registration split ruling (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GCR-RULING-0929` |
| reviewed | `e862a1dae` (author **FABLE**) — [`fable-gcr-split-ruling-0929/README.md`](../fable-gcr-split-ruling-0929/README.md), `form_split.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. The measurement script (SWE2-AUDIT-SEM)

`form_split.py` no longer runs at HEAD: its two predicate anchors were removed when SWE2-EC7 applied this ruling
(`090f74f38`, "one family … 99 members"). It is a one-shot measurement tied to the selector at `e862a1dae`, and its
committed output (control 76 / 23 PASS; form-based 23 / 76) cannot be re-run on today's selector
([`producer_rerun.out`](producer_rerun.out)). The consequence it predicted can be checked instead: the applied selector at
HEAD, dry run ([`selector_head_dryrun.out`](selector_head_dryrun.out)), reports **99 members, one family, 76 with a
guarded-form auxiliary callee (information only), census guarded-form bodies 525**. Those are the ruling's own numbers.

## 2. Is the split bookkeeping? (SWE2-AUDIT-SEM)

[`gcr_own.py`](gcr_own.py), [out](gcr_own.out) — every direct call of the four bodies, read from their `.pdata` extents:
- `0066A7B0` and `0066AB00` (836 bytes each) are guarded registration bodies of exactly the stated form:
  `_Init_thread_header` `008092FC` at `0066A80E` / `0066AB5E`, `atexit` `00808B90` at `0066A8B8` / `0066AC08`,
  `_Init_thread_footer` `0080929C` at `0066A8C5` / `0066AC15`, and three more guarded blocks each.
- The two moved bodies `00665870` and `00666380` (455 bytes each) are themselves guarded registrars of the same form
  (three header / atexit / footer triples). They differ only in calling `0066A7B0` / `0066AB00` (`00665897`,
  `006658DA`; `006663A7`, `006663EA`).

So nothing in the moved bodies' code distinguishes them from the stubs. Their row changed only because the owner of their
callee changed. The split tracked other families' bookkeeping, as the ruling says.

## 3. Is one row the right identity? (SWE2-AUDIT-SEM)

Yes. Membership stays the selector's fixpoint over the guarded form, which is a property of each body's own code. The
code-defined alternative puts 76 of 99 in one row (confirmed by the applied selector's information column), so
neither version of the split names a kind of code. Keeping the sibling-call fact as an information column, and
admitting frontier bodies only through the unified selector, keeps identity stable under other families' changes.
Executing the ruling (`090f74f38`) was SWE2-EC7's work and is not reviewed here.
