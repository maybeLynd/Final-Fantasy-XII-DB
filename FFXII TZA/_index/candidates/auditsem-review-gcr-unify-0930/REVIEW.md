# SWE2-AUDIT-SEM review — SWE2-EC7's GCR unification: guarded class-registration stubs as one family of 99 (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `SWE2-EC7-REQ-AUDITSEM-GCR-UNIFY-0930` |
| reviewed | `090f74f38` (author **SWE2-EC7**) — [`ec7-gcr-unify-0929/README.md`](../ec7-gcr-unify-0929/README.md), the selector, `guarded-class-registration-stubs.tsv`, the row and three sentences on `class-descriptor-and-metadata-system.md` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the membership, the information column and the retirement are right. One size range in the unified row was not widened. |

## 1. Is the TSV the selector's output, with the fixpoint unchanged? (SWE2-AUDIT-SEM)

[`gcr_check.sh`](gcr_check.sh), with [`gcr_compare.py`](gcr_compare.py) → [`gcr_check.out`](gcr_check.out) and
[`selector_rerun.txt`](selector_rerun.txt):
- **The selector at HEAD.** I ran the committed `select_guarded_class_registrars.py --write`, with its writes redirected
  to scratch through EC7's own redirector. It writes a TSV **byte-identical** (CR-stripped) to the committed one: 99
  members, 486 census predicate hits, 0 free.
- **Against the two files at `090f74f38^`.** Stubs 72 + orchestrators 25 = 97 distinct. All 97 are kept, the only
  additions are `005EFE60` and `00676A70`, and 0 are dropped.

## 2. Is the information column the ruling's GUARDED set? (SWE2-AUDIT-SEM)

[`gcr_info_check.py`](gcr_info_check.py), [out](gcr_info_check.out) recomputes it from the image, independently of the
selector. For each member, it lists the direct call targets outside the member's own body whose bodies call all three of
`_Init_thread_header` `008092FC`, `_Init_thread_footer` `0080929C` and the atexit wrapper `00808B90`.
- **99 of 99 match** the column.
- 76 are non-empty, which matches `form_split.out`'s form-based split (23 / 76, census GUARDED 525).
- Every address `form_split.out` prints on a guarded line (53) is in the non-empty column.

## 3. The retired row and the three sentences (SWE2-AUDIT-SEM)

- **The retired row.** The orchestrators row is removed, and the stubs row carries a dated sentence naming "the row
  formerly named 'guarded class-registration orchestrators' (25 members)" as history, with the ruling and the record.
  That is right.
- **The three sentences.** Each now states the call fact ("stubs that also call other guarded bodies"; "an aux target
  of guarded registration stubs that also call other guarded bodies"; "one family … counted as 76 + 26 in two rows
  until …"). None uses "orchestrator" as a kind of code any more.
- **The narrowing.** The unified row still says "members span 129..2490 B". That was the leaf row's range. The retired
  orchestrators row gave "183..3757 B", and the unified TSV's sizes run **129..3757 B** (section 2's script prints
  the range).

  **Narrowed sentence:** "PROVED BY CALL-SET SIGNATURE, NOT BY SIZE (members span 129..3757 B because each registers a
  different member set)".

  Routed to SWE2-EC7 as `AUDITSEM-REQ-EC7-GCR-SIZE-RANGE-0930`.
- **Left as written.** `ADDRESS-INDEX.md` (generated) and `PROGRAM-STATE.md`'s dated history line are right to be left
  alone.

The peer-modified pages under `22-Middleware-PhyreEngine/` in the working tree were not read as evidence. This review
reads the committed `090f74f38` text.
