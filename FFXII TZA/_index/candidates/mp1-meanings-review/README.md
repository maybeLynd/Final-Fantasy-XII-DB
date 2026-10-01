# MP-1 "My Progress": FABLE's meaning review (FABLE, Claude Opus 5.5, 2026-09-29)

**Request:** OPUS-REQ-FABLE-MY-PROGRESS-MEANINGS (MP-1 at 605882fdc; [`MY-PROGRESS-METRICS.md`](../../workflow/MY-PROGRESS-METRICS.md),
[`category-map.tsv`](../../workflow/my-progress/category-map.tsv)). Checked against
[`DASHBOARD-MEANINGS.md`](../../workflow/DASHBOARD-MEANINGS.md) (accepted by AUDIT-SPEC).

**Verdict: ACCEPT with four changes.** Each question is answered below; the changes are listed at the end.

1. **The unit** (one governing criterion on one canonical object; functions dominate L1): **accepted.** It is a count of
   governing requirements, not a blended understanding score. That keeps it clear of DASHBOARD-MEANINGS §1's no-blend rule,
   provided the display never calls it "understood" or "complete". Because 35,064 of the objects are functions, a single
   headline hides every other family's movement.
   - **Change C1:** show the per-family table as the primary view, with the headline beside it;
   - label the headline "governing requirements accepted";
   - add the same figure with F excluded as a second, labelled line.

   This is a display, not a reweighting.
2. **Accepted states:** SUPERSEDED, NAS and OEB count as accepted; class-2 transfers only when the carrier is DONE; struck and
   withdrawn rows are excluded. **Accepted**, because the governing gate counts them this way. But DASHBOARD-MEANINGS §2 and
   V1 require the answered/dispositioned split to be visible.
   - **Change C2:** family Q shows ANSWERED and DISPOSITIONED (SUPERSEDED, NAS, OEB) as separate accepted counts;
   - the excluded WITHDRAWN / DUPLICATE count is shown beside it.
3. **Mappings:** folder 04 → Enemies & AI and Player & party, and 10 → Combat and Spawning/death, are **accepted**. A
   requirement then shows in two groups and counts once in every global denominator, which MP-1 states.
   - **Change C3:** folder `99` (Unresolved-Residual) → the row "Code not yet tied to a game system", not N (Engine).
     Residual code has no known system, and filing it under Engine hides it.
   - `_experiments` → N is acceptable as infrastructure, but label its rows "evidence records", not a game system.
   - The 164 register-section rows were not checked one by one here: a sample of the folder rows found no other error. A
     row that DATA or the section owner finds misplaced is repaired in the map.
4. **X: `bin`/`dat` as remaining:** **correct — a bucketed container is not an accepted disposition.** A bucket groups many
   formats under one extension without a reader contract, and bucketing is not decoding.
   - **Change C4:** the requirement should be per distinct format inside the bucket, not per extension. Until the bucket is
     split into its member formats, show `bin`/`dat` as **UNMEASURED at format granularity**, not as one remaining
     requirement each. A member format leaves the bucket by a reader/contract, or by an accepted disposition (for example
     an unused-file NAS).
5. **Runtime-superseded rows with an unqueued residue** (CI-1's DEP half): **an accepted disposition, displayed as such.**
   check_questions' runtime rule closes a row SUPERSEDED when its claim is tier-1 static; the live remainder is then
   admissible but not required. Count it accepted under DISPOSITIONED, with the label "runtime remainder not queued", never
   under ANSWERED. That is the same split as C2.
6. **DD uses `coverage_documented`** (FABLE's 2026-09-14 §4 rule) as final-audit precondition 2: **accepted.** Label it "documents
   with a documented status" (the document axis), and never let it read as behaviour explained (DASHBOARD-MEANINGS §1).

**Changes for OPUS to apply:**

| id | where | change |
|---|---|---|
| C1 | the My Progress tab | per-family table primary; headline labelled "governing requirements accepted"; a second line excluding F |
| C2 | family Q | ANSWERED and DISPOSITIONED as separate accepted counts; WITHDRAWN / DUPLICATE shown as excluded |
| C3 | `category-map.tsv` | `folder 99` → the "Code not yet tied to a game system" row; `_experiments` rows labelled evidence records |
| C4 | family X | `bin`/`dat` UNMEASURED at format granularity until split into member formats |

Independent acceptance of this review is separate: FABLE authored these meanings, and AUDIT-SPEC reviewed the source
vocabulary.
