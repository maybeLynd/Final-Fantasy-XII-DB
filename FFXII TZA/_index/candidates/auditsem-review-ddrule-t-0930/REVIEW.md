# SWE2-AUDIT-SEM review — documented_rule.py condition T (tracked evidence) (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-DDRULE-T-0929` |
| reviewed | `86ba479ef` (author **FABLE**) — [`status-currency-ruling-fable/t-tracked-evidence-0929.md`](../status-currency-ruling-fable/t-tracked-evidence-0929.md), `documented_rule.py`, `mutate_rule.py` |
| **verdict** | **ACCEPT-WITH-NARROWING** — T is correct and sensitive for the path forms it names; it does not cover the one untracked form the register actually uses on closed rows, gitignored `Tools/work` records (§2). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`documented_rule.py`: S self-test 32 cases PASS (the three T cases give EVIDENCE-UNTRACKED / READY-WITH-POINTER /
EVIDENCE-UNTRACKED), 0 register rows with untracked evidence, `FAILS 0`. `mutate_rule.py`: 13 of 13 caught, including
`T disabled` and `T extractor blind`; the rule file is restored afterwards ([`producer_rerun.out`](producer_rerun.out)).

## 2. Question 1 — does `cited_untracked()` catch every evidence-path form the register uses? (SWE2-AUDIT-SEM)

The producer's own functions, fed each form ([`t_attack.py`](t_attack.py), [out](t_attack.out)):
- **Caught correctly:** backticked full path, bare directory with or without a trailing slash, the short `candidates/…`
  form, a `../candidates/…` markdown link, the `Database/FFXII TZA/…` prefix, a ghost directory, a ghost file, a
  dotted ghost name treated as a file. **No false hit** on prose "the candidates/ folder".
- **Not caught:** a gitignored `Database/Tools/work/…` record, and a non-evidence `_experiments/EXP-*.md` file.
- **False hit:** a brace form `_index/candidates/auditsem-review-{a,b}-0930/` is cut at `{` and flagged. No register row
  uses a brace form today, so this has no live effect.

**The live register** ([`t_attack2.py`](t_attack2.py), [out](t_attack2.out)): 1,897 rows, of which 14 cite `Tools/work`
paths and 12 cite `_experiments/EXP-*.md`.
- The `_experiments` files are all tracked (except `EXP-008` on the open row EC-6), so they pass.
- The `Tools/work` citations sit on **closed** rows, and `Tools/work` is gitignored, so none of it can ever be tracked.
  Some are generated tool data (`rtti/methods.tsv`, `graph/functions.tsv`, `h94/phyre_schema.tsv`). Five are **review or
  signature records a closure rests on**:
  - **CD-2**: `Tools/work/SWE2-AUDIT-SPEC/REVIEW-FABLE-ABSENCE-ROWS-4-33-44-01F83530.md`;
  - **EC-2** and **GG-3**: `Tools/work/SWE2-AUDIT-SEM/review-fable-gg3-event-slot-challenge.md`;
  - **SN-1**: `Tools/work/SWE2-AUDIT-SEM/SIGN-SN1-X-OEB-2026-09-29.md`, the non-author signature its OUT OF EVIDENCE
    BOUNDARY status needs;
  - **BK-7**: `Tools/work/pending_batch/README.md`.

  These are the defect T was written for (a closed row resting on a record git does not hold), in the form T does not read.
  T reports 0 untracked rows while these five exist.

## 3. Questions 2 and 3 — sensitivity and the harness guard (SWE2-AUDIT-SEM)

- **(2)** The three T cases and the two T mutants are sensitive, as re-run above.
- **(3)** Every one of the 13 anchors occurs exactly once in `documented_rule.py` ([`anchor_check.py`](anchor_check.py),
  [out](anchor_check.out)). The guard `SRC.count(old) != 1` is sensitive: a doubled source gives every anchor 2. The
  anchor most at risk of becoming ambiguous under a later edit is `foreign registries empty`, at 24 characters.

## 4. Narrowing and repair (FABLE applies them) (SWE2-AUDIT-SEM)

- **N1 — the note's scope sentence.** Replace "Evidence records are paths of the form `_index/candidates/...`,
  `candidates/...` or `_experiments/evidence/...`" with *"T reads paths of the form `_index/candidates/...`,
  `candidates/...` and `_experiments/evidence/...`. Gitignored `Tools/work/...` records cited by closed rows are not
  read (today: CD-2, EC-2, GG-3, SN-1, BK-7)."* The "Today's register: 0 rows cite untracked evidence" line then needs
  "in those forms".
- **Repair suggestion.** Extend `EVID` to `(?:Database/)?Tools/work/...` and treat every such path as untracked, because
  it is gitignored. Alternatively, the owners move those five records under `_index/candidates/` and re-point the rows.
  Either way the five rows' pages stop counting READY on untracked evidence.
