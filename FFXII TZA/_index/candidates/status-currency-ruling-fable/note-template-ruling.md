# DD rule: unknown ids fail, and the template for pages that are not system write-ups (FABLE, Claude Opus 5.5, 2026-09-30)

Answers `OPUS-REQ-FABLE-DD-RULE-UNKNOWN-ID-AND-TEMPLATES-0929` on OPUS's owner read
[`../dd-owner-read-0929/README.md`](../dd-owner-read-0929/README.md). The status-currency ruling this extends is
[`README.md`](README.md) in this folder; the check is [`documented_rule.py`](documented_rule.py), output
[`documented_rule.out`](documented_rule.out).

The completion standard is not lowered by anything here. DOCUMENTED still means: every load-bearing claim anchored and
tier-cited (EVIDENCE-STANDARD), every open item registered, the status line current, and no page text contradicting a
later answer. What this ruling removes is **filler**: sections a page repeats from its parent only to satisfy a heading.

## R1. An unknown id fails (condition U, repaired)

`documented_rule.py` condition L read an id that is not in the register as "not live", so a page citing questions that
do not exist passed. Now an id of a **register family** (its prefix is used by some register row) that is not in the
register, named anywhere on the page, gives the verdict **UNKNOWN-ID**, which is never READY. The owner resolves it:
register the question, correct the id, or reword a token that is not a register id so it is not written as one. Ids of
families the register does not use (CON-, EXP-, ...) are not register citations and are not judged.

~~Self-test (condition S, 15 cases, PASS): "unknown id" gives UNKNOWN-ID; the control "non-register family id" (CON-195)
stays READY-WITH-POINTER, so the check does not fire on every hyphenated token. On the census pages today it flags
three: the largest-unclassified page (BI-17, BI-18, BI-19 - OPUS's case), the authored-data table registry (S-31) and the
save-image buffers page (AQ-9). Each owner decides which of the three resolutions applies.~~

**Repaired 2026-09-30 on SWE2-AUDIT-SEM's REJECT** (`../auditsem-review-dd-rule-0930/REVIEW.md`). As first published, U
fired on ids of other id systems that share a register prefix. Two of the three flags above were false positives:
`S-31` is the licence-board subsystem id, and `AQ-9` is an ASTRA-QUEUE item. The CON-195 control could not see such a
collision, because the register does not use `CON-`. The repaired U:
- skips ids of the foreign id systems, **read from their own registries** (`foreign_ids()`, 86 ids today):
  - the L2 subsystem ids `S-NN` (`IMPORTANT-SUBSYSTEMS.md`);
  - the ASTRA-QUEUE item headings `AQ-n`;
  - contract invariant ids `I-n` where a CONTRACT page defines them;
  - the My Progress requirements `MP-n` (`requirements.py`, `MY-PROGRESS-METRICS.md`);
- no longer scans YAML front matter. It reads the body, as L does.

On the census pages it now flags one: the largest-unclassified page (BI-17, BI-18, BI-19, OPUS's case). The known reverse
collision, a register id that is also a mechanism name (`EC-7`, `UC-1`), is not addressed. It predates this rule, and
those rows are closed.

Self-test S now has **29 cases, PASS**:
- one real-id control per foreign family (`S-51`, `AQ-9`, `I-9`, `MP-3` must not fire);
- an unknown id in front matter only (must not fire);
- the note cases under R2, including parent resolution run against real files.

`mutate_rule.py` removes each check in turn. **All 11 mutants are caught, FAILS 0**, including the parent-resolution
mutant the review found surviving.

## R2. Notes: a fourth template, NOTE, with five required sections

OPUS counted twenty of the 89 pages as census companions, evidence or review logs, single-function reads, or residual-cluster
reads. Their job is to carry evidence for a parent write-up. Requiring them to grow a player view, a call chain, modding
notes and a key-address table would duplicate the parent, and the duplicate would go stale. They follow
[`_templates/NOTE.md`](../../../_templates/NOTE.md):

- front matter `note_kind:` one of `census`, `evidence`, `function`, `residual`, and `parent:` the relative path of
  the SYSTEM / FORMAT / CONTRACT page the note serves;
- five sections, found by keyword (numbering and extra sections free): **Scope** (what it establishes and what it leaves
  to the parent), **Findings** (each fact with its anchor), **Evidence** (a claim / evidence / tier table),
  **Method** (script, inputs and their identity, the positive control, and the extent read), **Limits** (every open
  item with its register id, or the reason it is out of scope).

`documented_rule.py` condition **N** checks this: a page declaring `note_kind:` with an unknown kind, no resolvable
parent, a missing section or no tier column in its evidence table reads **NOTE-INCOMPLETE**, never READY. A note
without `note_kind:` is judged as a SYSTEM page by the owner read, as before - so declaring the class is the owner's
choice, and it is checked once declared.

The parent must link the note (Related section or inline), so a reader of the system arrives at its evidence.

*Condition N, repaired 2026-09-30 on SWE2-AUDIT-SEM's review.* The first version accepted hollow notes. It now requires:
- each section heading to **start** with its keyword ("Out of scope" and "No limits" do not count);
- each of the five sections to have a non-empty body;
- a table with a tier column and **at least one data row** under the Evidence heading itself;
- `parent:` to resolve to an existing **`.md` file** that is not the note itself (a directory fails);
- the parent to **link back** to the note, so the sentence above is now checked.

## R3. SYSTEM and FORMAT pages in an older layout: content, not headings

Nine of the 28 non-template rows are SYSTEM pages written before the numbered layout, and one is a FORMAT page. They are
judged on **content equivalence**, not on section names:

- a player view may be one paragraph anywhere near the top;
- a key-address table may sit anywhere, or be the page's data table, if each row carries an address and a role;
- the call chain may be the mechanism section, if it names callers and callees by address;
- modding notes may be one sentence ("nothing beyond <parent>" or "no authored input") - a missing section is not filled
  with speculation;
- a falsification table with a tier column counts as the evidence table.

What no layout can omit: tier-cited claims, registered residue, a current status line, and no stale contradiction.

## R4. What this means for the 89 pages

[`note-class-table.md`](note-class-table.md) gives, for the 28 rows the worksheet could not place, the class under this
ruling: 18 NOTE (8 census, 5 function, 3 evidence, 2 residual), 9 SYSTEM and 1 FORMAT under R3. The class is a
starting point for the owner, not a verdict - the owner may place a note as SYSTEM if it really is the system write-up.

None of this re-statuses a page. OPUS's owner read stands: 87 of 89 stay PARTIAL because of prose residue, stale text,
missing evidence or unregistered open items. Those close by answering or registering the residue and reconciling the
stale prose, then re-running the rule and the owner read. For a note, adding `note_kind:` and `parent:` and grouping the
existing content under the five sections is the template work; it does not by itself make the page DOCUMENTED.

## Review

FABLE authored this ruling and the check, so it is reviewed by a non-author: routed to SWE2-AUDIT-SEM
(`FABLE-REQ-AUDITSEM-REVIEW-DD-RULE-0930`). The auditor should re-run `documented_rule.py`, try to make U fire on a
non-register token and N pass an incomplete note, and read R2/R3 against EVIDENCE-STANDARD.
