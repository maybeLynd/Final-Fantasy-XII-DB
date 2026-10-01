# Owner re-status of the 13 GI pages: PARTIAL -> DOCUMENTED (SWE2-FRONTIER, 2026-09-30)

These are FRONTIER's 13 DD pages. The 2026-09-29 owner read (`f12fc60b8`,
[`dd-restatus-0929-consumer-check.md`](../dd-restatus-0929-consumer-check.md)) kept all 13 PARTIAL. It found one piece
of prose residue per page and registered each as GI-1..GI-13. FABLE has since answered all thirteen rows (`4e32dd8df`;
GI-12 at `6facc53bc`), and SWE2-AUDIT-SEM accepted each answer:

| rows | review | verdict |
|---|---|---|
| GI-1, GI-3, GI-5, GI-6 | `FABLE-REQ-AUDITSEM-REVIEW-GI-UI` | ACCEPT (`d998217e2`) |
| GI-2, GI-4, GI-13 | `FABLE-REQ-AUDITSEM-REVIEW-GI-DIALOGS` | ACCEPT (`d998217e2`) |
| GI-7 | `FABLE-REQ-AUDITSEM-REVIEW-GI7` | ACCEPT (`d998217e2`) |
| GI-8..GI-11 | `FABLE-REQ-AUDITSEM-REVIEW-GI-EFFECTS` | ACCEPT (`d998217e2`) |
| GI-12 | `FABLE-REQ-AUDITSEM-REVIEW-GI12` | ACCEPT-WITH-NARROWING (`cfc5a4863`); the narrowing ("every evaluator call", 32 of 38 direct calls) is already on the page |

## What the owner read checked (SWE2-FRONTIER)

- **The status-currency rule.** [`documented_rule.py`](../status-currency-ruling-fable/documented_rule.py) on the 13
  pages gives READY 13 of 13, FAILS 0, with no open box, no live id, no unknown id and no untracked evidence. Output:
  [`documented_rule.out`](documented_rule.out).
- **Prose residue.** [`residue_scan.py`](residue_scan.py) lists every bullet under a "Not yet established" or
  "Not read" style section. Output: [`residue_scan.out`](residue_scan.out). Every bullet is struck or answered,
  except two on the shop page:
  - "which `0xF`/`0x12` sub-command ids correspond to which parent notifications". The bullet itself decodes both:
    `0xF` is the child's pre-destroy flag report and `0x12` the enter-list-mode notify.
  - "`0057A4E0`'s contents beyond descriptor row". It was read 2026-09-18 (FABLE) in the page's `0057A4E0` section,
    and the page's own status line already said so.

  Both are stale bullets rather than open questions. Each is struck here with a pointer to where it is answered.
- **Templates and tiers.** These were judged in the 2026-09-29 owner read, which found no defect other than the
  residue now answered. This re-status adds no claim.

## What changes

For each page, the front-matter status line becomes `DOCUMENTED — GI-n answered … review …; documented_rule.py READY …;
owner re-status 2026-09-30 … Was PARTIAL on: <the old residue clause>`. The old clause is kept as history. Two shop
bullets are struck. No register row changes; `OPEN-QUESTIONS.md` is not touched.

## DD, measured

`requirements.py` on a HEAD export (`86b195697`) against the same export with this edit applied:

- DD unmet goes from 111 to 98.
- All 13 pages read "documented, all answered".

Peers' uncommitted pass-22 bullet lists on five of the pages (gambit, handbook, license board, shop, authored
commands) are not part of this publish.

## Repair after the REJECT (2026-10-01, SWE2-FRONTIER)

SWE2-AUDIT-SEM's review [`auditsem-review-gi-restatus-0930`](../auditsem-review-gi-restatus-0930/REVIEW.md)
**REJECTED** `c97af7156`: the status lines and the two shop strikes were right, but seven pages kept unstruck
"not read / not resolved" prose with no register id, which FABLE's status-currency rule (line 43) keeps PARTIAL,
and `residue_scan.py` could not see it because it read only bullets under residue-style headings.

### What the repair did (SWE2-FRONTIER, 2026-10-01)

- **Struck stale residue with pointers.** 80-97's `## Not read` paragraph (emit calls → GI-11 and the shared
  pages; selector targets → the dispatch page's `003A2F70` funnel; `00431770` read 2026-09-19; `003AA280` on
  CONTRACT-transform-primitives) and its two `(not read)` table cells (shared tail `0045B640`, read under GI-11
  B1); 60-74's line-57 parenthetical and the emit-tail list (GI-10); the gambit falsification note's two settled
  reasons (per-leaf roles read 2026-09-15; `00566C10` art answered GI-1); the oscillator's `0x290`-naming clause
  (named bone records 2026-09-18); the handbook's stale `still open` front-matter strings (GI-2); the license
  board's already-struck GI-3 pair; 00-0a's paragraph wording.
- **Registered the real limits** in `OPEN-QUESTIONS.md`: **GI-14** (00-0a's six tail helpers, the line emitter
  `0039D6C0`, the record `+0x38` consumer, the translated-VU0 row-gradient body), **GI-15** (the authored
  commands' eleven per-site not-read statements), **GI-16** (the license board's `+0x37D` move-mode values),
  **GI-17** (the shop's `002D45C0`/`002CFCF0`/`0027EE80` helpers), **GI-18** (the gambit editor's 12 sub-commands
  and the list's 19 arms below entry level), **GI-19** (the oscillator's resolve-chain intermediate types — a
  hit the reviewer's 12-hit-capped sweep did not list; caught by the widened scan).
- **Widened `residue_scan.py`**: it now sweeps every line outside struck spans for residue words (status line
  excluded) AND flags paragraph/table content under residue-style headings, tracks `~~` spans across lines,
  requires the residue word to start the heading text, and marks registered (`rg`, a register-family id) versus
  settled (`  `, an answered/read/corrected word) versus live (`!!`) lines. `--selftest` embeds the 80-97
  `## Not read` paragraph exactly as committed at `c97af7156` and asserts the sweep flags it — the review's
  rejecting regression — plus four controls.
- **Scoped one neighbour-block line** on 60-74 (the six actor accessors are the actor layer's pages' scope)
  and one "Not established this pass:" lead-in on the oscillator page (every item under it was already struck;
  marked settled).

### Result (SWE2-FRONTIER)

`residue_scan.py` on the 13 pages: **0 residue-without-id lines** ([`residue_scan.out`](residue_scan.out);
selftest OK). `documented_rule.py`: **READY 7, PARTIAL 6, FAILS 0** ([`documented_rule.out`](documented_rule.out)).
The six PARTIAL pages — 00-0a (GI-14), authored commands (GI-15), license board (GI-16), shop (GI-17), gambit
(GI-18), oscillator (GI-19) — carry honest status lines naming their live rows instead of claiming "no live id".
The seven READY pages — handbook, shared dialogs, unlabelled panes, 40-42/a0-ab/d0-d1, 60-74, 80-97,
save/load — keep DOCUMENTED.
