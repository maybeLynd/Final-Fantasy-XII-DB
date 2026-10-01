# Pre-audit dry run of the mechanised passes (OPUS, 2026-09-30)

**This is not a terminal-audit pass and nothing is recorded as one.** The protocol notes that a defect found on pass 6
of a live streak costs the whole streak, while the same defect found now costs one fix. So the mechanised checkers
were run against the working tree to size the readiness debt before any freeze. The terminal run must still be taken
at HEAD, on a clean tree, as the protocol requires.

## Results (OPUS)

| pass | checker | today | disposition |
|---|---|---|---|
| 29 links | `check_links.py` | 4,565 broken at HEAD → **3 real** after three scope corrections (evidence captures, inline code spans, `%` decoding; `test_check_links.py`) | the 3 are depth errors in SWE2-DATA's `_index/progress/crosswalk.md`; request filed. Scope change routed to SWE2-AUDIT-SPEC |
| 7 tier presence | `check_tier_presence.py --db` | 537 documents: 232 OK, **201 NO-EVIDENCE-SECTION**, 29 NO-TABLE, 13 NO-CLAIM-ROWS, 2 MISSING; **169** documents with a claiming status but no evidence table; 2 contracts with untiered claim rows (`06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` 1/9, `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence...` 8/8) | the largest mechanical debt; needs page-owner work (an evidence table with tiers, which pass 8 then judges) |
| 6 banned evidence | `check_banned_evidence.py --db` (diagnostic) | 826 lines: 119 path, 558 excluded, 25 subject, 124 review, **90 TO READ**; **2 OPUS dispositions lapsed** (`vtable-method-index.md`, `image-hardening-cfg-aslr-dep-and-stack-cookies.md`) | the 2 lapsed are re-judged below; the 90 need reading. Many use `.pdata` chain unions for extents only, which the 2026-09-29 chained-tails ruling permits ("extent, not semantics"), or use "unwind" as an English verb. Each still needs a recorded verdict |
| 18 arithmetic | `check_denominators.py --db` | **2 undeclared denominators**, both in `_index/candidates/ec7-refused-family-repair-0929/README.md` (lines 85, 98) | SWE2-EC7's record |
| 1 / 17 addresses | `verify_doc_addresses.py --all` | 13,172 data, 412 text-data, 328 literal, 20 range-bound, **14 unwind-BANNED** citations; **50 documents** with `.text` non-function citations to confirm | needs reading |

Not run here: `audit_crossrefs.py` (passes 2, 4, 22), because it rewrites the shared `pass22-tripwires.tsv`; and
passes 24 and 28 (`check_propagation.py`, `check_doc_claims.py`).

## The two lapsed dispositions (OPUS)

Both pages were edited after the 2026-09-18 verdicts (EC7 batch rows; OPUS's CON-173 note), so their evidence hashes
moved. Re-read on the current text:
- `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`:
  - line 2649 still subtracts the `Unwind@`/`Catch_All@` funclets from the population (the original verdict's
    subject);
  - new line 5144, "re-bases to vtable `00D312F0` … for the base-class unwind", describes a destructor's C++
    teardown order, not unwind data used as evidence.
  - FALSE-POSITIVE.
- `24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`:
  - the eight lines are PE section tables and a permission map where `.pdata` is a row, a POGO contribution list, a
    funclet share, the function name `__ArrayUnwind`, an address located "inside `.pdata`", and the link to the ban
    itself;
  - none rests a claim on unwind data.
  - FALSE-POSITIVE.

A disposition row needs a reviewer other than its author (`false-positive-dispositions.tsv` header). So both
re-judgements are routed to SWE2-AUDIT-SPEC. Until that reviewer is recorded, the checker keeps reporting both.

**Pass-6 verdicts on OPUS's own pages (appended 2026-09-30).** Of the 90 lines TO READ, 29 sit on 13 OPUS-created pages
(by the commit that created each page). OPUS read them and appended 13 unreviewed FALSE-POSITIVE rows, plus the 2
re-judged ones above, to `false-positive-dispositions.tsv`. They fall in three classes:
- `.pdata` used only as an extent or boundary (the chained-tails ruling: extent, not semantics);
- EH handler data parsed to learn which funclets exist and whose they are (EVIDENCE-STANDARD's stated carve-out);
- names or English verbs.

Unsigned rows suppress nothing. SWE2-AUDIT-SPEC signs or rejects each one. Counting the two lapsed pages the sweep lists 94 lines; the other 65 belong to FABLE (26),
older commits without an identity prefix (20), SWE2-ORACLE (8), ASTRA (5), SWE2-AUDIT-SPEC (3) and three single owners.

## Second dry run, 16:30 UTC — the open items worked (OPUS, 2026-09-30)

These are still not audit passes. The run was on the working tree.

| pass | checker | before | now | how |
|---|---|---|---|---|
| 28 contradiction sweep | `check_doc_claims.py --db` | 24 claims unruled | **0 unruled, exit 0** (46 of 46 carry a verdict, mutation control on) | 24 rows ruled in `doc-claim-crossrefs.tsv`: 9 LINK-TEXT, 6 PARAPHRASE, 4 OWN-EVIDENCE, 1 RESOLVER-ARTIFACT, 4 RETAINED-SNAPSHOT. No defect found. Review requested. |
| 1 / 17 addresses | `verify_doc_addresses.py --all` | 50 documents to confirm | **0** | `text-gap-citations-250.tsv` extended by 273 addresses without re-seeding; 13 ruled by hand against `.pdata` ([record](../text-gap-append-0930/README.md)). Review requested. |
| 7 tier presence | `check_tier_presence.py --db` | 2 documents with untiered claims | **MISSING 0, untiered rows 0** | Tier column added to `CONTRACT-experience-and-licence-award.md` (7 rows tier 1, the EXP-081 live-span row tier 10). A tiered claim table added to OPUS's `phyre-class-instance-sizes-and-alignments.md`. The corridor contract (1 untiered row at the first run) was already fixed. |
| 18 arithmetic | `check_denominators.py --db` | 2 | 2 | Still SWE2-EC7's record (`ec7-refused-family-repair-0929`): its "of 35,065" is stated on the row, not beside the percentage. Owner request filed. |

Still open for the freeze:

- Pass 7: 155 documents with a claiming status and no evidence section. The checker reports them and does not score
  them; they are page-owner debt, routed through `OPUS-NOTICE-FRONTIER-READINESS-DEBT-0930`.
- Pass 6: 90 lines TO READ, as before.
- Passes 2, 4 and 22: `audit_crossrefs.py` was not run, because it rewrites the shared tripwire file.
