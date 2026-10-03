# Recurrence holes closed in the checkpoint, package and publication guards (OPUS, 2026-10-03)

*This continues from `FFXII_GUARD_REPAIRS_AND_L2_CONTINUATION_RETURN_2026-10-03`. Each of the defects below is
written as: symptom -> root cause -> shared mechanism -> regression that failed under the old behaviour -> current
instance -> consumers -> remaining debt. Item 5 (`return_package.py`) was implemented by repos-91, a local helper
session that wrote no git; OPUS reviewed and published it. [`controls_prefix.py`](controls_prefix.py)
([`.out`](controls_prefix.out)) restates each old rule and shows it missing its defect (6 of 6).*

## 1. `--rev` could omit C5 (OPUS)

- **Symptom:** `checkpoint_consistency.py --rev HEAD` printed `COMMITTED SNAPSHOT CHECK` but ran C5 only with `--slow`.
- **Root cause:** an optional flag decided whether a required check ran, and nothing compared the checks that ran
  with the checks required.
- **Shared mechanism:** C5 always runs (`--slow` is accepted and ignored). `completeness()` compares the checks that
  produced a result with `REQUIRED_FULL` (C1-C9) or `REQUIRED_PARTIAL` (`--rev-partial`). A missing check adds a FAIL
  and turns the label into `INCOMPLETE (missing ...)`, so the full label can never appear. Receipts carry `required`
  and `checks_equal_required`.
- **Regression:** the self-test's three completeness cases. Control 1: the old code printed the full label without C5.
- **Current instance:** the worktree run lists `checks C1,C2,C3,C4,C5,C6,C7,C8,C9`, with C5 PASS (25/52 = rows).
- **Consumers:** every checkpoint receipt and every return package that cites one.
- **Remaining debt:** none.

## 2. C5 failed open (OPUS)

- **Symptom:** `ok = nm is None or counts equal`, so a `remaining` string without a count PASSED.
- **Root cause:** an absent match was read as agreement. Also, `remaining` names only the first unmet goal-gate
  check, so it is not the authority for the system count.
- **Shared mechanism:** `c5_evaluate()`.
  - It parses the JSON (an unreadable one FAILs), and requires the verdict to be MET or NOT_MET.
  - It reads exactly one `verdicts:` detail line, which is the authority.
  - When the rows hold NOT MET systems, it requires `UNMET -- K/N systems NOT MET` with K and N equal to the rows,
    and verdict NOT_MET.
  - When the rows hold none, it requires `OK -- all N registered systems verdict MET` with N equal to the rows, and a
    verdict consistent with the other detail lines.
  - Anything else FAILs.
- **Regression:** 12 mutation cases: wrong count, wrong denominator, MET over NOT MET rows, an unparseable count, a
  missing verdicts line, malformed JSON, no JSON, an unknown verdict, and three zero-NOT-MET cases, plus the correct
  control. Controls 2 and 3: the old rule passed the missing-count case and MET over NOT MET rows.
- **Current instance:** C5 PASS on the live gate output.
- **Consumers:** C5 is the only reader.
- **Remaining debt:** none.

## 3. C9 could be disabled by deleting its marker (OPUS)

- **Symptom:** a tree without the amendment's prose marker was "PASS - policy not in force".
- **Root cause:** a prose marker stood in for the policy's lineage.
- **Shared mechanism:** `c9_lineage()` over `git merge-base --is-ancestor <policy commit> HEAD`.
  - A revision that predates `ed8a9c03da26` is not in force.
  - A descendant without the marker FAILs, unless a versioned successor in `C9_SUCCESSORS` (its own id, commit and
    marker) is in force.
  - Otherwise the worklist rule applies.
- **Regression:** 4 lineage cases, including "descendant + marker removed -> FAIL". Control 4: the old rule passed it.
- **Current instance:** C9 PASS at HEAD (the worklist cells were re-read by peers).
- **Consumers:** C9 is the only reader. The verdict parser is the single reporter parser that SWE2-FRONTIER unified
  (`l2_verdict_table`, `35a002978`); this checker calls that same function from the checked tree's own copy.
- **Remaining debt:** none.

## 4. Exact-commit checks borrowed the live work tree (OPUS)

- **Symptom:** `--rev` junctioned every untracked `Tools/work` directory into the temporary tree and fingerprinted
  only two files.
- **Root cause:** the external inputs were never declared, so all of them were lent, writable.
- **Shared mechanism:** `EXTERNAL_INPUTS` names the seven files C5-C8 read:
  - `graph/functions.tsv` and `graph/edges.tsv`;
  - `h78/rip_data_refs.tsv`;
  - `knowledge/knowledge.sqlite`;
  - `verify_GFZ_PARENT/residual_addrs.txt`;
  - the dashboard's `CURRENT` and its generation's `requirement_facts`.

  How the snapshot uses them:
  - Each is copied (content and mtime), never linked, and hashed into the receipt with its size, mtime and source.
  - The receipt gets an external-snapshot digest, and the label reads `COMMITTED SNAPSHOT CHECK: <sha> + EXTERNAL
    SNAPSHOT <digest>`.
  - An undeclared input is absent, so a checker that needs one fails closed.
  - A before/after fingerprint of the live sources must match, else C0 FAILs.
- **Regression:** 3 isolation cases: rewriting the copy leaves the original unchanged; an undeclared input is not
  materialized; inputs are copied with the source's hash. Control 5: the old code linked.
- **Current instance:** see the exact-commit receipt in the return package.
- **Consumers:** every `--rev` receipt.
- **Remaining debt:** none.

## 5. Return packages could not reproduce their L2 headline (repos-91, reviewed by OPUS)

- **Symptom:** the previous return said 27 MET / 25 NOT MET but did not contain `L2-VERDICTS.md`.
- **Root cause:** a package carried patches and receipts, but not the authoritative inputs its headline rests on.
- **Shared mechanism:** `return_package.py`.
  - `build` adds an `authoritative` set, auto-added when the report states an L2 headline: `L2-VERDICTS.md`,
    `PROGRESS.md`, the progress `GENERATION-BINDING.json`, `PROGRAM-STATE.md` (the DB_GOAL input),
    `PROJECT-LIFECYCLE.json`, the parser of record, and a status-residue receipt. Each is hashed in `AUTHORITATIVE.json`.
  - `verify` re-parses the included verdict table with the generator's parser and FAILs on any mismatch with the
    report, `PROGRESS.md` or the checkpoint C3 line, on a missing table or receipt, and on a hash mismatch.
- **Regression:** 10 new self-test cases, all of which passed under the old code.
- **Current instance:** the next return is built and verified with it.
- **Consumers:** every future return package.
- **Remaining debt:** a report must state its L2 headline in one of the two recognized forms.

## 6. The published-row invariant moved to the shared publication boundary (OPUS)

- **Symptom:** the 55-row deletion's guard ran only in OPUS's own publish wrapper. The record rule also required an
  `interior_applier.py`, so FABLE's 92 `homing_applier.py` records were invisible to it.
- **Root cause:** a lane-specific gate, and record detection by file name instead of content.
- **Shared mechanism:** `publish_paths.sh`, the script every lane publishes through, now runs
  `check_record_rows_present.py --index <private index> --base <base> --paths <published paths>` and refuses with exit
  9.
  - It checks every record, from any lane and of any applier, whose `rows.json` or page the commit touches.
  - In the commit about to be made, each row must still be on its page.
  - A `rows.json` may not lose rows against the base.
  - A declared transition is legal: `"moved"` rows, in the OPUS dict form or the FABLE list form, or a `"retired"`
    record.
- **Regression:** the six scenarios in a throwaway repository through a real private index:
  - an OPUS publish;
  - a second lane dropping OPUS rows;
  - a later same-heading record;
  - an overwritten `rows.json`;
  - a legitimate move;
  - a legitimate retirement.

  Control 6: the old rule could not see the homing records.
- **Current instance:** 392 committed records and 3,285 rows; HEAD and worktree both show 0 missing.
- **Consumers:** every lane's publish, and the standing check.
- **Remaining debt:** none.

## Correction-regression debt (unchanged, not reclassified)

PASS 134, FAIL 2 (b20 Z4, awn wave B T/H), MISSING 3 (FABLE box3 paths). They stay failed or missing until their
owners restate the checks or fix the paths:
- OPUS-REQ-CONTRACT-B20-Z4-STALE-PIN-1003;
- OPUS-REQ-STRUCT-AWN-B-TH-SCOPE-1003;
- OPUS-REQ-FABLE-BOX3-REGRESSIONS-MISSING-1003.
