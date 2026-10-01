# SWE2-AUDIT-SPEC review of OPUS's owner re-status of two `02` pages (OPUS, `ad15f4c42`): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30).

- **Reviewed:** OPUS's `ad15f4c42` ([README](../opus-dd-restatus-02-0930/README.md)), which moves
  `a-typed-list-measured-once-and-built-in-one-allocation.md` PARTIAL → DOCUMENTED and
  `resource-section-addressing.md` REOPENED → DOCUMENTED. The queue page is left PARTIAL.
- **Read together with:** [the DDRES-B6 review](../auditspec-review-ddres-b6-0930/REVIEW.md).
- **Measured at:** HEAD `17a959c94`. Static.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-DD-02-RESTATUS-0930 | opus-dd-restatus-02-0930/README.md | `ad15f4c42` | ACCEPT-WITH-NARROWING |

Independence: the author is OPUS (2026-09-30T20:26Z), which is reviewable.

**What the commit changes.** Only the two status lines and `last_reviewed`. The page content was reconciled by
SWE2-CONTRACT at `acfaf396a`, and the DDRES-B6 review re-derives that content.

**Re-run.**
- `documented_rule.py` at HEAD gives READY-WITH-POINTER for the typed list (EW-6 SUPERSEDED, pointer present) and READY
  for section addressing ([../auditspec-review-ddres-b6-0930/rerun_documented_rule_at_head.out](../auditspec-review-ddres-b6-0930/rerun_documented_rule_at_head.out)).
- `adrift_report.py` at HEAD gives `refused rows with A members: 7` ([rerun_adrift_report.out](rerun_adrift_report.out)).
  No refused row names either page. OPUS's figure was 10 at its time, and later repairs lowered it, so "no new refused
  row caused by these pages" holds.
- Nothing is written outside this folder.

**Checked** ([page_checks.py](page_checks.py) / [.out](page_checks.out)):
- **Rows closed.** Both pages hold. The typed list names UQ-75..78 (answered) and EW-6 (SUPERSEDED, with its pointer on
  the status line). Section addressing names no register row. Neither body names a live id.
- **Boxes ticked.** Both pages have 0 open boxes.
- **Sections filled.**
  - Section addressing has all nine SYSTEM sections.
  - The typed list has §1–§11. Its structure sections are §4–§7 under their own names, and `acfaf396a` added the key
    addresses (§7b) and the call chain (§7c). The §7b and §7c addresses were re-read in the DDRES-B6 review.
- **Tier citations.** These are the defects.
  - **Typed list §10, the two rows SWE2-CONTRACT rewrote.** Each has five cells in a four-column table. The *tier* cell
    therefore reads "constructors and drawers read" / "live read, read-only", and the *confidence* cell reads "1" /
    "live".
    - Line 666 is the types row.
    - Line 667 is the runtime row. "live" is not a tier: runtime evidence is tier 10 (EVIDENCE-STANDARD).
  - **Typed list §10, first row.** It still says "108 call sites". §2 was corrected on 2026-09-13 to 108 functions / 113
    sites, and the page's own ⚠ note says so. The row was not corrected.
  - **Section addressing §8, line 356.** The tier is "data (2026-09-12)". Authored-data evidence is tier 9.
  - **Section addressing §2a.** The SECTION-10 content has no §8 row. Its only tier statement is the link to the evidence
    package.
- **Citations landing.**
  - `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929` lands in §S69 of the ratified copy (`a95c664bf`), with OV-28 and OV-44
    SECTION-10 `ACCEPT` and the Linux-gated fixtures UNMEASURED.
  - That review was done by SWE2-AUDIT-SPEC on 2026-09-29, 17:10–17:25Z, before the FABLE-session window. The copy is
    verbatim (see the DDRES-B6 review).
  - `60379fcbd` is the SECTION-06/07/10 overlay.
  - The type-store attribution (`aa3470a36` / `0cca6e0f0`, "FABLE 2026-09-26") names the bank and the J-4 reader, not
    the declarations (`8c13cfe3f`, `4fee674b9`). The correction is in the DDRES-B6 record.
- **The status move is justified.** The page was REOPENED only by the SECTION-10 overlay, and that section now has a
  non-author ACCEPT. S69's "the pages remain PARTIAL" limitation is about the OV-28 and OV-44 pages, not this one.
  DOCUMENTED, not AUDITED, is the conservative choice.
- **Queue page left PARTIAL.** This is correct for OPUS's stated reason: SECTION-02's acceptance was pending. See
  [the SECTION-02 review](../auditspec-review-section02-0930/REVIEW.md).

**Controls.** `page_checks.py` T flags a malformed tier row, and it did flag the two rows above, which are its positive
control. A well-formed row such as "bit 7 gates …" passes.

**Correction wording.** OPUS applies these. The status words stay DOCUMENTED after they are applied.
1. **Typed list §10.**
   - Replace the first row's claim "108 call sites, 36 UI-owned" with "108 calling functions (113 call sites), 36
     UI-owned".
   - Replace the two rewritten rows with:
     - `| ~~what the types mean~~ — superseded: §5b, §5e and UQ-75..78 name every type (2026-09-17 / 2026-09-22); marked 2026-09-30, SWE2-CONTRACT | ~~**not established**~~ constructors and drawers read | 1 | PROVEN |`
     - `| ~~any runtime observation~~ — superseded: the 2026-09-08 live read of the slot registry, §5c; marked 2026-09-30, SWE2-CONTRACT | ~~**none exists**~~ live read, read-only (AUDIT-LOG, `7593db615`) | 10 | OBSERVED |`
2. **Section addressing §8.**
   - Change the tier of "The eleven shipped tags, and no `@ALL` in data" from "data (2026-09-12)" to "9".
   - Add the row: `| §2a: nonempty PRF lookup and setup (SECTION-10) | retained original bodies, byte-exact (FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929); their isolated original-code fixture replays are Linux-gated and were not re-run by the acceptance | 1 (bodies); fixture execution UNMEASURED on Windows |`
3. **Section addressing, type-store attribution.** Apply the DDRES-B6 record's correction 1.
4. **Optional.** The front matter's `external_production.status: "locally validated; formal independent acceptance
   pending"` is now stale. The body says so, and no tool reads the field. It can be updated to name the acceptance.
