# My Progress - metric definitions (version MP-2, OPUS)

**Owner:** OPUS (technical delivery). **Meanings:** FABLE reviews. **Metrics and data:** DATA reviews and may adopt the reader.
**Code:** `Database/Tools/dashboard/requirements.py` (catalog), `build_views.py` (`v_progress`), `server.py` (the tab).
**Tests:** `test_requirements.py`.

> **MP-2 (2026-09-29) applies FABLE's meaning review** ([`mp1-meanings-review`](../candidates/mp1-meanings-review/README.md):
> ACCEPT with four changes). A checkpoint taken under MP-1 reads "definition changed; not comparable" in the change column.
> - **C1:** the per-family table is primary; the headline reads "governing requirements accepted", with a second line
>   excluding the 35,064 function dispositions.
> - **C2:** register rows show ANSWERED and DISPOSITIONED as separate accepted counts. Runtime-superseded rows are
>   labelled "runtime remainder not queued".
> - **C3:** folder `99` places into "Code not yet tied to a game system"; `_experiments` requirements are labelled
>   evidence records.
> - **C4:** a bucketed extension (`bin`, `dat`) is not one requirement: its member formats are. Until DATA declares the
>   members in `Database/Tools/work/formats/bucket-members.tsv`, the buckets are a named **gap**, and the overall figure
>   reads **UNMEASURED, known requirements only**, with the gap and its repair task shown. **Category map:** [`my-progress/category-map.tsv`](my-progress/category-map.tsv).

The "My Progress" tab is a compact view of evidence the database already keeps. It is not a tracker, and it is not a
completion standard. It awards no acceptance and cannot start L3. **DATABASE READY** is shown only when the governing
`goal_gate.py` reads MET and every requirement below is accepted.

## 1. The unit

**One requirement = one governing criterion applied to one canonical object that the governing records already name.**
- **accepted %** = 100 × accepted requirements / all requirements in that scope.
- **remaining %** is the complement for the same scope.
- It measures requirements, not elapsed time or equal-sized engineering effort.

**Why this unit.** The governing documents state their criteria per object:
- [`COMPLETION-PLAN.md`](../COMPLETION-PLAN.md) §3: *"Every function must end in exactly one of these"*;
- §4: *"Every document needs one named falsification pass"*;
- [`FINAL-AUDIT-PROTOCOL.md`](../FINAL-AUDIT-PROTOCOL.md): every system documented, `OPEN-QUESTIONS.md` empty, provenance
  green, thirty passes;
- [`OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) header: every open page checkbox mirrored with an id.

Counting per object reuses the canonical ids and adds no subtasks. A consequence to keep in view: the function population
is 35,064 objects, so it dominates L1. That is what the plan requires, not a weighting choice.

**Accepted** means fully satisfied under the governing record's own state. Filed, produced, reviewed, incorporated and
accepted are different states; only the last counts here.

## 2. Families (MP-1)

| family | object (canonical id) | accepted when | source reader | level |
|---|---|---|---|---|
| Q register questions | register row id | ANSWERED, NAS, OEB (accepted dispositions), SUPERSEDED (accepted disposition, destination live), or NOT A QUESTION transferred to a carrier task that is DONE | `check_questions.classify`, `transfer_audit` | L1; also L2 when the owning page is a registered system page |
| P page obligations | page path + box text | never: an unticked box with no id, or one naming only closed rows, is residue | `check_questions.read_boxes` | L1 (+L2 as above) |
| F function dispositions | function entry (UC-1 population, 35,064) | explained A / B / C and not residual; D and frontier remain | `check_dispositions.evaluate` | L1 |
| DD documents documented | document path | status DOCUMENTED/AUDITED, or readiness when there is no status (FABLE ruling 2026-09-14 §4) | `progress.coverage_documented` | L1 (+L2) |
| DA falsification pass | document path | a pass with a program state, or `falsification_passes` with a written section | the `audit_coverage` rule of `progress.py` | L1 (+L2) |
| DV provenance | document path | not stale, stamped with the authority EXE | `check_provenance` | L1 (+L2) |
| R registry slots | slot address | claimed by `registry_slots:` | `check_formats` | L1 |
| X formats | archive extension; for a bucketed extension, each declared member format (MP-2, C4) | counted by `check_assets.evaluate`; a member format when a signature-scoped `archive_formats` claim explains it | `check_assets` + DATA's `bucket-members.tsv` | L1 |
| E EBP units | unit name | claimed by `ebp_units:` | `check_ebp` | L1 |
| K contradictions | CON id | kind in the gate's resolved set | `goal_gate.RESOLVED_CONTRA_KINDS` | L1 and L2 |
| L2 cells | S-id × dimension | MET, or LIVE with no unruled LIVE in that dimension (N/A is not a requirement) | DATA's reporter snapshot | L2 |
| T terminal passes | pass 1..30 | the gate's acceptance check passed (then all 30), else the receipted counter | `goal_gate` + reporter | L1 and L2 |

**Not requirements (excluded and listed, never silently dropped):**
- WITHDRAWN, DISSOLVED and NOT A DEFECT rows;
- NOT A QUESTION rows with no carrier;
- struck row ids;
- duplicate ids (counted once, at the first row).

**Deduplication:**
- A page box naming a live register row is the same obligation as that row, so it is counted once, as the row.
- A key seen twice is one requirement.
- A class-1 SUPERSEDED row's population residue (for example A-1's unclassified functions) is carried by the F family,
  which already counts those functions.
- **L1+L2** is the deduplicated union. It is never an average and never a sum of the two.

**Transfers are not closure:**
- A class-2 row is accepted only when its carrier task is DONE.
- A SUPERSEDED row whose destination `transfer_audit` reports missing is remaining.

## 3. Categories

There are twelve user-facing groups. The explicit map ([`category-map.tsv`](my-progress/category-map.tsv)) places each
requirement by the first of these that resolves:
1. the owning page's folder;
2. the register section (register rows without a page link);
3. the declaring page (functions);
4. the `owner` column;
5. the CodeDomain family;
6. the Boundary suffix.

A requirement can sit under several groups (for example 04-Actor-Entity under Enemies & AI and Player & party). It
then counts in each group's row but once in every global denominator.

Two further rows keep the table complete:
- **Whole database:** the thirty terminal passes, and integrity rows that name no page.
- **Code not yet tied to a game system:** frontier functions whose only classification is a generic shape class with
  no owner. Their system is genuinely unknown. A function leaves this row when a page explains or declares it, and the
  page's folder then places it.

A requirement no rule places is a mapping gap. The tab lists it by key, and the gap is repaired in the map.

## 4. Change since the prior checkpoint

The prior checkpoint is the newest generation committed before 00:00Z of the build day that still verifies
(`open_generation` with its recorded manifest hash) and carries this view. When no generation is that old, it is the
earliest verified one of the day. The comparison shows three things separately:
- the accepted-count change (work accepted, or reopened when negative);
- the scope change (denominator growth or shrinkage from new or withdrawn requirements);
- the percentage-point change.

A checkpoint with a different metric version reads "definition changed; not comparable".

## 5. Freshness and failure

- The tab uses the same validated generation as every other view. The server refuses to show a progress block whose
  numbers disagree with its validated measures, or a DATABASE READY while anything remains.
- INVALID, STALE, HISTORICAL and UNMEASURED stay visible.
- A family whose reader fails makes the overall figure UNMEASURED. The rest is then shown as known requirements only.
- A browser refresh reads the generation. It never recomputes the database and never calls a model.
- The facts are collected once per build, before the generation begins (about 10 s). Corpus edits after that capture
  appear at the next build.

## 6. Known limits of MP-1

- Review state per object is the governing record's own state. A register ANSWERED row counts as accepted even where no
  separate review record exists; the gate accepts it the same way.
- ~~`X` counts `bin` and `dat` as remaining.~~ Ruled by FABLE (C4): a bucket is not an accepted disposition, and its
  member formats are the requirements. Until they are declared, the buckets are a gap, so the overall figure is
  UNMEASURED.
- The terminal count comes from the governing gate's acceptance check and the receipted counter. Partial streaks are not
  shown as accepted.
