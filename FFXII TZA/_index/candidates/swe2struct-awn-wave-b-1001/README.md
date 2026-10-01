# AWN wave B: SWE2-AUDIT-SPEC's narrowings applied for fifteen reviews (SWE2-STRUCT for OPUS, 2026-10-01)

Request: `SWE2AUDITSPEC-REQ-OPUS-0930-WAVE-NARROWINGS` asks the owner to apply each ACCEPT-WITH-NARROWING review's
correction wording, or record why not. FABLE is inactive and the user authorized OPUS lanes to do this. SWE2-CONTRACT
has the other half (links-scope .. sd106); none of its reviews is touched here. Board task `SWE2STRUCT-AWN-WAVE-B-1001`
(research), added at board revision 44469 and claimed at 44470. The batch was run by a Claude session in the
SWE2-STRUCT lane, started by OPUS, with no subagents and no commits. OPUS publishes.

- **Base.** HEAD `0ea7dbefc` when the batch started. Every target file was clean then (`git status --short` empty),
  except the lane inbox (see Blocked).
- **How.** The exact old and new texts are data in [awn_b_edits.py](awn_b_edits.py): 63 edits in 26 files. They are
  applied by `Database/Tools/work/SWE2-STRUCT/awnb/apply_awnb.py`, which is idempotent (a second run reports 63
  ALREADY), requires each anchor to match exactly once, and refuses a file that is already modified.
- **Form.** Old text is kept and struck with `~~...~~`. Each change carries a dated note: *(narrowed 2026-10-01,
  SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's review link)*. Where a review's replacement is itself already a struck
  row (the typed-list §10 rows), it is written exactly as the review gives it.
- **Line endings.** All 26 targets are pure LF and stay LF (files are read and written with `newline=''`).
- **Untouched.** No front-matter `status:` line and no register row was edited. Neither was any of the four pages this
  batch may not edit.

## Outcomes (SWE2-STRUCT for OPUS)

Outcome counts: **14 applied** (5 of them with a sub-item declined), **1 proposed only** (its one correction is a page
status line), **0 already applied**, **0 blocked**.

| review | outcome | files touched | edits | proposed for OPUS |
|---|---|---|---|---|
| [dd-mixed](../auditspec-review-dd-mixed-0930/REVIEW.md) | proposed only: the correction is the measuring-text page's status line | record README (note only) | DDMIX-1 | the status-line text below |
| [types-sections](../auditspec-review-types-sections-0930/REVIEW.md) | applied; the checker sub-item declined | record README P4; `_types/types.tsv` dtor cells of `OffsetIndexedStringTable` and `CountedU32LookupTable` (TS-2/TS-3 not in OPUS's publish: the file carries a foreign rewrite, routed as `OPUS-REQ-STRUCT-AWNB-TYPES-1001`) | TS-1..3 | none |
| [sd164-167](../auditspec-review-sd164-167-0930/REVIEW.md) | applied (H2 bullets replaced; H1, A1, K1 unchanged) | record README | SD164-1 | none |
| [sd166](../auditspec-review-sd166-0930/REVIEW.md) | applied; the checker sub-item declined | record README (answer, A4 rows, S1, modding); kit `regval.py` docstring | SD166-1..6 | SD-166 lead (consequential) |
| [sd126](../auditspec-review-sd126-0930/REVIEW.md) | applied | record README (column, two cells, id-30 row, modding line, Limits block) | SD126-1..6 | none |
| [sd127](../auditspec-review-sd127-0930/REVIEW.md) | applied | record README (K1, K3, R2 limit, modding line) | SD127-1..4 | SD-127 lead (consequential) |
| [sd169](../auditspec-review-sd169-0930/REVIEW.md) | applied | record README (G3) | SD169-1 | none |
| [sd121](../auditspec-review-sd121-0930/REVIEW.md) | applied | record README (S3, S5, modding, Limits) | SD121-1..4 | none (the review keeps the row's summary) |
| [sd123](../auditspec-review-sd123-0930/REVIEW.md) | applied; the checker sub-item declined | record README (title, answer, I2, I3, modding) | SD123-1..6 | SD-123 summary (quoted wording) |
| [sd160](../auditspec-review-sd160-0930/REVIEW.md) | applied | record README (output files, C3 cell, readings limit) | SD160-1..3 | none |
| [sd161](../auditspec-review-sd161-0930/REVIEW.md) | applied | record README (headline, the correction's reason, last Limit) | SD161-1..3 | SD-161 lead (consequential) |
| [sd163](../auditspec-review-sd163-0930/REVIEW.md) | applied, including both optional Limits | record README (P2 cell range, naming sentence, two Limits) | SD163-1..3 | none |
| [sd192](../auditspec-review-sd192-0930/REVIEW.md) | applied | record README (title, Limits) | SD192-1..2 | SD-192 lead (quoted wording) |
| [dd-02-restatus](../auditspec-review-dd-02-restatus-0930/REVIEW.md) | applied (corrections 1-3); optional 4 declined | typed-list page §10; section-addressing page §8 and the type-store attribution; record README | DD02R-1..7 | none |
| [dd-02-b2](../auditspec-review-dd-02-b2-0930/REVIEW.md) | applied (corrections 1-5 and the new sections of 6); 6's status lines proposed; optional 7 declined | as7, btm, lst, mg, lmap, cmap, wmap pages; record batch2.md | DD02B-1..13 | cmap and wmap status-line texts below |

## Declined sub-items, with reasons (SWE2-STRUCT for OPUS)

- **Checker changes** (types-sections "add to P4's check a store census"; sd166 "S1 should census all four ids" and
  "A4 should also check the DIR64 slots"; sd123 "pin the mask `00500C39` and the live arms"). Each would change a
  reviewed package's instrument and its committed `.out`. That is the author's (OPUS's) to re-run and re-publish. The
  README notes now say what each checker does and does not test, and name the review's own instrument.
- **dd-02-restatus 4 and dd-02-b2 7 (optional).** These are front-matter fields (`external_production.status`,
  `evidence_tier`). They are optional, and no tool reads them.

## Proposed for OPUS: status lines and register cells (SWE2-STRUCT for OPUS)

Page `status:` lines and register rows are OPUS's. The texts below are pipe-free.

**Status lines (quoted wording).**
- `99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md`: replace "what the reveal stepper's
  modes are for is SD-100 (status line current 2026-09-30, SWE2-DATA)" with "what the reveal stepper's modes are for is
  answered (SD-100, 2026-09-30)".
- `cmap-menumap-common-sublocation-directory.md`: replace "and nothing on the page is carried as open" with "; the entry
  `+2` auxId and section 2's value semantics are stated unbound (§2.1, §2.2, §5), as declared limits".
- `wmap-menumap-world-map-graph.md`: replace "and nothing on the page is carried as open" with "; the area record's `+8`
  aux i16 and the `B2` sub-table are stated unbound (§2.2, §7), as declared limits".

**Register cells.** "Quoted" means the review names the register row and gives its wording. "Consequential" means the
row repeats a sentence the review narrowed, but the review does not word the row; OPUS decides those.
- **SD-123 (quoted).** Replace "effect record kind 0x52 is the effect container's paletted image (texture) record."
  with "~~effect record kind 0x52 is the effect container's paletted image (texture) record.~~ effect record kind 0x52
  is the effect container's image (texture) record: 4- or 8-bit indexed with one palette, or 4-byte-per-pixel direct
  colour (narrowed 2026-10-01 on SWE2-AUDIT-SPEC's review
  [`auditspec-review-sd123-0930`](../auditspec-review-sd123-0930/REVIEW.md): 11,076 of the 16,862 shipped
  records are indexed and 5,786 direct colour)."
- **SD-192 (quoted).** Replace "yes — every reader refuses." with "~~yes — every reader refuses.~~ yes — every
  movement-side reader of the attached bit (the eight checked; not the attach guard `002E274A` or the two
  presentation readers) refuses movement on it (narrowed 2026-10-01 on SWE2-AUDIT-SPEC's review
  [`auditspec-review-sd192-0930`](../auditspec-review-sd192-0930/REVIEW.md))."
- **SD-166 (consequential).** Replace "only two debug verbs could, and no shipped script calls them" with "~~only two
  debug verbs could, and no shipped script calls them~~ only four class-2 debug verbs could (0x2003, 0x2004, 0x2008,
  0x2009), and no shipped script calls any of them".
- **SD-161 (consequential).** Replace "and the displacement census finds only non-negative stores" with "~~and the
  displacement census finds only non-negative stores~~ every census store at a known offset on the field is a memset
  to 0, and SWE2-AUDIT-SPEC bounded the census's other 365 reaching stores except the backup restore `00583C00`, the
  caller-bounded bit helpers (`00315AD0`, `00252D40`, `00254E00` and the `0046B290` family) and `003112F0`, which
  stores only non-negative values". Its lead "no code writes counter 11 negative" then needs "no code found so far
  writes", or a note that those caller groups are unbounded.
- **SD-127 (consequential).** After "the console is the only pointer route" add "; indexed table reads next to the keys
  (`00266530`, `00266B83`, `002AEB20`) are not excluded by code (narrowed 2026-10-01 on SWE2-AUDIT-SPEC's review
  [`auditspec-review-sd127-0930`](../auditspec-review-sd127-0930/REVIEW.md))".

## Consumers that repeat the old wording, not edited (SWE2-STRUCT for OPUS)

The reviews' correction wording does not name these pages, so this batch leaves them for their owners. OPUS can route
them.
- `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md` line 357: "SD-192
  ANSWERED, every reader refuses" (SD-192 narrowing).
- `02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md` line 1422: "shipped scripts never call the
  two debug verbs" (the verbs are four; the conclusion stands).
- `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` line 1912: `0036E080` "dual-table" (the
  SD-121 review shows it is triple; the page's own table row says triple).
- `_index/candidates/gr2-free-target-values-0930/README.md` C5 row: "Montblanc" among the `THIRD_*` guests (SD-160
  narrowing; another record).
- `_index/candidates/sd-incorporation-fable-0930/README.md` SD-123 row: "paletted image" (FABLE's incorporation table).
- The four pages this batch may not edit were not opened for editing; whether they repeat any narrowed sentence is not
  checked here.

## Blocked (SWE2-STRUCT for OPUS)

- **The lane inbox `_index/_inbox/SWE2-STRUCT.md`** already carries another SWE2-STRUCT session's uncommitted block
  ("Route-seeded census batch 2 ... NEXT: publish batch 2"). It is not edited. A whole-file publish would sweep that
  block in. The Resume entry for this batch, for OPUS to add once that block is published:

  > **LATEST 2026-10-01 (AWN wave B, SWE2-STRUCT for OPUS):** board task `SWE2STRUCT-AWN-WAVE-B-1001` was added (rev
  > 44469), claimed (44470) and finished (44501). Record `_index/candidates/swe2struct-awn-wave-b-1001/`: README,
  > `awn_b_edits.py`, `awn_b_checks.py` (FAILS 0) and `consumer-check.md`. 63 edits in 26 files, uncommitted for OPUS to
  > publish. Proposed for OPUS: three status lines and five register cells. Current claims: none ACTIVE.

## Checker (SWE2-STRUCT for OPUS)

[awn_b_checks.py](awn_b_checks.py) / [.out](awn_b_checks.out) checks:
- each new text is present once (A);
- each old text is gone outside it (O);
- each struck span is wrapped in `~~` (K);
- the control C: at base `0ea7dbefc` every old text is present and every new text is absent, so the checks are
  sensitive to the edit;
- no `status:` line changed (T);
- every new `##` heading carries this lane's attribution (H);
- the register and the four never-edit pages carry no note from this batch (R);
- the tables here are well formed (P).
