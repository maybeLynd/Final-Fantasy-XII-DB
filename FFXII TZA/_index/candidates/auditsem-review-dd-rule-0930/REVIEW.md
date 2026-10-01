# SWE2-AUDIT-SEM review — the DD rule repair (condition U) and the NOTE template (condition N, R1-R4), 2026-09-30

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-29/30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-DD-RULE-0930` |
| reviewed | `48391d7f6` (author **FABLE**; not an OPUS-lane production) — `status-currency-ruling-fable/documented_rule.py` (+ `.out`), [`note-template-ruling.md`](../status-currency-ruling-fable/note-template-ruling.md), `note-class-table.md`, `_templates/NOTE.md` |
| **verdict** | **REJECT** — condition U fails pages on legitimate non-register tokens, and two of the three pages the commit reports as citation defects are false positives. Condition N and the self-test need the repairs listed below; R2/R3 wording keeps the completion standard |

Evidence class: execution of the shipped rule on synthetic and real pages (`attack.py`, `u_census.py`) and mutation of
the rule in a scratch copy executed with the original `__file__`. The producer's run reproduces at HEAD
(`producer_rerun.out.txt`: S PASS, FAILS 0; TALLY `NEEDS-POINTER=12 PARTIAL=1 READY=15 READY-WITH-POINTER=2
UNKNOWN-ID=3 of 33`).

## 1. Condition U fires on non-register tokens — the defect (SWE2-AUDIT-SEM)

U treats any `[A-Z]{1,4}-\d{1,4}` token whose prefix appears in the register as a register citation. The register's
234 prefixes include single letters and short pairs that other id systems in this database also use:

| token family | what it is | register rows with that prefix | U result (`attack.out.txt`) |
|---|---|---|---|
| `S-01` … `S-51` | the subsystem ids of `L2-VERDICTS.md` / `IMPORTANT-SUBSYSTEMS.md` (e.g. `S-31` licence board, MET) | `S-1` … `S-5` (the `.gfids` / TLS questions) | **UNKNOWN-ID** (`S-31`, and zero-padded `S-05` beside the register's `S-5`) |
| `AQ-9` … | items of `_inbox/ASTRA-QUEUE.md` (`### AQ-9 — does a save at a save point re-capture…`) | `AQ-1` … `AQ-6` (Phyre questions) | **UNKNOWN-ID** |
| `I-10` … | contract invariant ids (`CONTRACT-render-command-list…` `I-10`) | `I-2` … `I-7` | **UNKNOWN-ID** |
| `MP-3` | the My Progress requirement MP-3 | `MP-1`, `MP-2` | **UNKNOWN-ID** |
| any of these in YAML front matter only | — | — | **UNKNOWN-ID** (U scans the whole text, L only the body) |

A database-wide census (`u_census.out.txt`, pages outside `_inbox/` and `candidates/`) finds **133 distinct tokens of
register prefixes that are not register ids, on 164 pages**; 49 of the token kinds are `S-NN` subsystem ids alone
(`S-18` on 19 pages, `S-23` and `S-16` on 15 each, …). Every such page is held at UNKNOWN-ID — never READY — until its
owner rewrites a canonical subsystem id, queue id or invariant id so it no longer looks like a question id. The ruling's
remedy "reword a non-register token so it is not written as an id" asks owners to deface other canonical id systems.

**The commit's own census already shows it.** Of the three pages it reports ("BI-17/18/19, S-31, AQ-9"): `S-31` on
`authored-data-table-registry.md` is the subsystem (*"because S-31's verdict turns on it"*), and `AQ-9` on
`save-image-buffers-header-and-payload.md` is the ASTRA-QUEUE item (*"AQ-9 prediction: a changed active-block byte…"*,
also in `AUDIT-LOG.md`). Only BI-17..19 is the intended catch. The self-test's non-register control (`CON-195`) uses a
prefix the register does not have, so it cannot see a namespace collision.

The same collision runs the other way and predates this commit: a register id that is also a mechanism name (`EC-7`,
`UC-1`) is read as a question citation by L. It is READY today only because those rows are closed.

**Repair asked of the producer (the rule's owner):** make U recognise the foreign id systems it collides with — at least
the L2 subsystem ids (from `L2-VERDICTS.md`), ASTRA-QUEUE `AQ-` items, contract invariant ids and `MP-` requirements —
from their own registries, not by hand-listing tokens; decide deliberately whether front matter is scanned; add a positive
control per foreign family (a real subsystem id and a real queue id must not fire) beside the existing unknown-id case;
re-run and re-state which of the census pages are real citation defects.

## 2. Condition N can be satisfied by hollow sections (SWE2-AUDIT-SEM)

With a resolvable parent, each of these reads **READY** (`attack.out.txt`):

- five headings with no content under any of them, and an evidence table that is a header row only;
- headings `## Out of scope`, `## Results`, `## Methodology`, `## No limits` (keyword search: `scope`, `result`,
  `method`, `limit` match), with a two-column `| a | tier |` header;
- `parent: .` or `parent: ..` — a directory "resolves", so the parent need not be a page (and R2's "the parent must link
  the note" is not checked at all);
- the tier column present only in an unrelated table after `## Limits`, with the Evidence section in prose.

N checks the presence of headings and of a table header, not that the Evidence table has a row or a section has a
line. The docstring's "READY is not DOCUMENTED: the owner still confirms the sections are filled" keeps the standard in
principle, but question (2) of the request — "does N refuse an incomplete note" — is answered no for an empty one.
**Repair:** require at least one data row in a tier-column table that sits under the Evidence heading, a non-empty body
under each of the five sections, `parent:` resolving to a `.md` file (not a directory, not the note itself), and ideally
the parent's back-link.

## 3. The self-test's controls (SWE2-AUDIT-SEM)

Seven mutants of the rule, each executed through the real `main()`: **six are caught** (S FAILS) — U disabled, U's prefix
test dropped, N disabled, the section check removed, the tier-column check removed, the kind check removed. **One
survives:** removing the parent-**resolution** check (`parent(unresolved)`) leaves S at PASS, because S calls `judge()`
without a `page_dir`, so that branch never runs in the self-test. Add a case with a `page_dir` and an unresolvable parent.

## 4. R2 / R3 against the completion standard (SWE2-AUDIT-SEM)

R2 and R3 drop only duplicated sections (player view, call chain, modding notes, key-address table) and restate what no
layout may omit — tier-cited claims, registered residue, a current status line, no stale contradiction — in the same words
as the status-currency ruling; that is consistent with EVIDENCE-STANDARD. R3's "content equivalence" is an owner-read
judgement with no mechanical check; it does not lower the bar as written, but it is only as strong as that read. The
ruling re-statuses nothing, as it says.

## Receipts (SWE2-AUDIT-SEM)

`receipts/attack.py` + `attack.out.txt` (adversarial pages and the seven mutants), `u_census.py` + `u_census.out.txt`
(database-wide collision census), `producer_rerun.out.txt` (run from `Database/Tools/work/SWE2-AUDIT-SEM/ddrule0930/`).
