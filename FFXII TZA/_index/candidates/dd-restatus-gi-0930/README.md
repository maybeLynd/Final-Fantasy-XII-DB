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
