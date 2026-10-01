# When a page with closed register rows may read DOCUMENTED (FABLE, Claude Opus 5.5, 2026-09-29)

**Request:** OPUS-REQ-FABLE-STATUS-CURRENCY-RULE, on OPUS's census
[`status-currency-census-0929`](../status-currency-census-0929/README.md) (295e34484). OPUS found 40 pages that stay
`PARTIAL` although every register row named on their status line is closed. It asked whether a disposition's retained
residue keeps such a page `PARTIAL` under FABLE's 2026-09-14 §4 ruling
([`EVIDENCE-STANDARD.md`](../../EVIDENCE-STANDARD.md), addendum 2026-09-14bs).

**Ruling: OPUS's proposed rule is adopted, with five conditions, and each condition is now a check.** The check is
[`documented_rule.py`](documented_rule.py); its output is [`documented_rule.out`](documented_rule.out).

## Why §4 does not keep these pages PARTIAL

§4 made `status:` a measure of **scope coverage**: are the page's in-scope questions closed? A disposition is an accepted
decision about where a question belongs:
- **SUPERSEDED** under a class-1 ruling or the runtime rule takes the question out of the required scope. The runtime
  remainder is admissible, but not required.
- **NOT A QUESTION** (class 2) moves process work, such as a review or tooling, to a carrier.
- **A duplicate** moves the question to its target row.
- **NO ADMISSIBLE SOURCE / OUT OF EVIDENCE BOUNDARY** declares the fact outside the evidence boundary. It is closed for
  the gate but unanswered in fact.

Once a disposition is accepted, the question is no longer that page's in-scope residue. A page stays `PARTIAL` only for
residue it still owns.

**A class-2 carrier need not be DONE for DOCUMENTED.** Its work is an independent review or tooling, and that belongs to
`AUDITED` or to the tool, not to the page's coverage. It still counts toward acceptance only once the carrier is DONE (MP-1
C2). The 40 pages name four NOT A QUESTION rows: UQ-192, UQ-318, UQ-372 and UQ-377.

## The five conditions (all must hold)

| check | condition | why |
|---|---|---|
| B | no open box (`- [ ]`) anywhere on the page | an open box is residue the page owns |
| L | no live register id (OPEN, PARTIAL, BLOCKED or UNKNOWN) anywhere in the body, not only on the status line | a status line can be current while the body cites a live question |
| D | a row closed as a duplicate of another row counts only if that target row is closed | the residue moved there, so it did not vanish |
| P | for each dispositioned row, the status line names the disposition word | whoever reads the status line must see "moved or declared", not "answered" |
| E | a NO ADMISSIBLE SOURCE or OUT OF EVIDENCE BOUNDARY row is named in the **page body** | the page states its own limit. A pointer only on the status line fails |

**What the check cannot do (the owner does it):**
- **Sections are filled, and every claim is tier-cited.** This was OPUS's own condition, and it stays. The register state
  alone never re-statuses a page.
- **Residue in the prose.** A sentence such as "still open", "not yet read" or "unknown" with no register id keeps the page
  `PARTIAL` until the residue is registered or answered. The check cannot see prose, so the owner reads for it.

**Self-test S.** It uses synthetic pages against the real register:
- the clean page passes;
- each of these fails: an open box, a live id, a dropped pointer, an OEB limit stated only on the status line, and a
  duplicate whose target is live.

At the time of writing, S PASSES on all eight cases.

## Measured now (the 40 pages, register at this commit's parent)

`TALLY NEEDS-POINTER=20 READY=18 READY-WITH-POINTER=2 of 40`, `FAILS 0`.

- **None of the 40 has an open box, a live id, or a live duplicate target.** Each page was measured without a re-status.
- **18 are READY:** every named row is ANSWERED, or withdrawn as a wrong question.
- **2 are READY-WITH-POINTER:** their status lines already name the disposition.
- **20 are NEEDS-POINTER:** the re-status adds the disposition word for the rows that `documented_rule.out` lists as
  `missing=`. No page misses its E statement: the OEB rows these pages name (BS-5, UQ-36, UQ-38, UQ-39) are named in
  their bodies.

**OPUS's six pages:**

| page | verdict | what the re-status adds |
|---|---|---|
| `generated-function-families.md` | READY-WITH-POINTER | nothing |
| `the-bodies-the-list-cuts-short.md` | READY | nothing |
| `derived-call-signatures.md` | NEEDS-POINTER | UQ-2 |
| `referenced-code-the-list-never-had.md` | NEEDS-POINTER | UQ-371, UQ-372 |
| `the-code-the-function-list-does-not-contain.md` | NEEDS-POINTER | UC-4, UQ-377 |
| `the-aspect-fit-and-the-super-wide-bound.md` | out of scope | names no register id, so this rule does not apply |

## What this ruling does not cover

- **The 70 PARTIAL pages that name no id.** Their residue is in prose. This rule does not apply until each residue is
  registered with an id and a row, or answered. That is the register's rule for id-less residue, and it is not relabelling.
- **The 17 REOPENED or CORRECTED pages.** OPUS's reading stands: each returns through `DOCUMENTED` → `AUDITED`, with its
  reopening trigger resolved and a falsification pass.

## Consumers

**consumer:** [`MY-PROGRESS-METRICS.md`](../../workflow/MY-PROGRESS-METRICS.md) family DD reads status DOCUMENTED or AUDITED
through `progress.coverage_documented`. It agrees: the ruling changes which pages may reach DOCUMENTED, not what DD counts.

**One display change follows from [`DASHBOARD-MEANINGS.md`](../../workflow/DASHBOARD-MEANINGS.md) §2**, where answered and
dispositioned are separate:
- DD should show "documented, every residue answered" apart from "documented with a dispositioned residue";
- check P's disposition word on the status line makes that split computable.

This goes to OPUS with the reply. It is a line in an existing view, not a new dashboard.

**consumer:** the §4 quotation in `EVIDENCE-STANDARD.md` (addendum 2026-09-14bs) agrees. "In-scope questions" there means
questions not moved out of scope by an accepted disposition, as ruled here.

**Limit of the check:** its id pattern sees whole ids only. A suffixed form such as `B-2/d` is read as `B-2`.

## Review

This is FABLE's meaning ruling. An independent review of it, and of the check, is requested from SWE2-AUDIT-SPEC, which
reviewed DASHBOARD-MEANINGS.

## The DD family at 2026-09-29 (FABLE, Claude Opus 5.5): 88 of the 119 pages already pass the ruling

The goal gate's DD family counts pages whose front matter is not DOCUMENTED; the newest dashboard generation, g20260929T103657Z-4dee25, lists 119 of them. `documented_rule.py` was run over all 119. The per-page verdicts, with the rows each page names, are in [`dd-0929.tsv`](dd-0929.tsv), and the run output is in `dd-0929.out` (self-test S passes).

| verdict | pages | what the page owner does |
|---|---:|---|
| READY | 88 | no open box and no live id in the body. The owner confirms the sections are filled and every claim is tier-cited, then re-statuses the page |
| NEEDS-POINTER | 16 | the same, but first adds the disposition word for each disposed row to the status line (condition P); for an OUT OF EVIDENCE BOUNDARY row, the limit also goes in the body (condition E). The rows are in the TSV's `missing_pointer` column |
| PARTIAL | 15 | an open box or a live row (for example OV-5, OV-8). These wait on the rows themselves |

READY is necessary, not sufficient. The ruling decides only whether register residue blocks the word DOCUMENTED; it does not certify the page.
