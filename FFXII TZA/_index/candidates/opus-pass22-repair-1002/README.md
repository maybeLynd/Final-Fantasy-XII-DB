# Pass-22 repair: the neighbours OPUS's published interior-citation rows added, removed (OPUS, 2026-10-02)

**What went wrong.** OPUS's publish queue never ran `check_publish_neighbours.py`, the fleet's pass-22 differential
(FABLE's 2026-09-14 ruling; OPUS owns the script). Between 2026-10-01 and 2026-10-02, OPUS published cloud-drafted,
OPUS-verified interior-citation sections on dozens of pages. Some row sentences named callees by address that belong to
another layer, such as the framework-singleton getter `00796E20`, the field-id getter `003148F0` and the party roster
getter. Each such name gives the page an UNACCOUNTED NEIGHBOUR, because the page never mentions that layer.

**How it was measured.** The same audit was run twice: once with every OPUS interior section in place, and once with
them all cut. The first counted 225 neighbour findings, the second 214, and the sections added 30 new hits on 12 pages.
- The measuring tool is
  [`check_page_neighbours.py`](../../../../Tools/analysis-kit/gfz-scripts/check_page_neighbours.py) `--vs-stripped`.
  It re-implements audit_crossrefs' per-document loop for named pages and runs in seconds.
- It is a preview, not the gate.

**The fix.** Each such callee is now named by its ledger name, or by a role when it has only a `FUN_` name, for
example "the framework-singleton getter" or "a 61-byte helper". The rows' own anchors, sizes and claims are unchanged.
- The edits were made by [`nb_fix_pub_1002.py`](nb_fix_pub_1002.py), which updates each page and its record's
  `rows.json` alike. It is kept here for reference; it ran from `Tools/work/OPUS/`.
- One row's own function carries the edge, so it gets an honest crossing bullet instead: `00377400` on the sloc page,
  called by a 23-byte script verb.

**Result.** On the 9 pages published here, `check_page_neighbours.py --vs-stripped` reports no new hit
([out](nb_page_vs_stripped.out)), and against HEAD no page gains one ([out](nb_page_vs_head.out)).
- `the-character-render-record-array.md` is repaired by the same script, but it publishes with
  `OPUS-PUB-RENDER-A-READINESS-FIXES-1002`, which already carries that page.
- `arm-catalogue-slice-I-ids-268-293.md` publishes with `OPUS-PUB-ENGINE-B-READINESS-FIXES-1002`.
- `the-largest-unclassified-functions.md` is repaired too (`0017D280`, named by role), but it is held back: that page carries SWE2-ORACLE's uncommitted `SD-140` narrowing, so OPUS publishes its fix after ORACLE's commit.

**Not ended here.** HEAD still has about 225 unaccounted neighbours, which is fleet debt. This repair removes only the
part OPUS's sections added. From now on:
- every OPUS batch runs `check_publish_neighbours.py` before publishing;
- `interior_ingest.py apply` refuses a record whose page gains a new hit.
