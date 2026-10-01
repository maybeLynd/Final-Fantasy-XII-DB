# DD owner re-status, batch 10: the widget message protocol to DOCUMENTED (OPUS, 2026-10-01)

SWE2-STRUCT's DD batch 17 ([`swe2struct-ddres-b17-0930`](../swe2struct-ddres-b17-0930/README.md)) closed the prose residue
in the body of `16-UI/Widget-Object-Model/the-widget-message-protocol.md`. Its checker `b17_checks.py` passes 125 checks,
FAILS 0, re-run by OPUS after the status edit. The status line's own residue had already been answered in SWE2-CONTRACT's
DD batch 10 (W1-W4). OPUS batch 6 kept the page PARTIAL because of the body's prose. That prose is now resolved:

| kind | count | how |
|---|---|---|
| STALE | 9, and 5 more from a wider pass | dated pointers |
| BOUNDARY | 2 | pointers to the pages that own them |
| RESIDUE | 5 | each answered with checks |

The five residues:
- **E1-E4:** no curve kind can leave channel 0 running.
- **F1-F3:** message 8's flag.
- **S1-S4:** `002B6DB0` is a shared procedure, and message 29 gets its first receiving side.
- **L1-L9:** message 26's link.
- **C1-C5:** message 16 has 17 application senders, not 20. That corrects 4 struck statements.

**Owner read (OPUS).** Four sentences outside the grep set are left alone. Each is a stated scope limit or a run-time
question, not an open question the page asks:
- §9a's "what this does not claim";
- §9d's "not a static question";
- one "jump table present, not decoded" table row;
- "whether initialisation completes … is not observed".

The snapshot-reader order is run-time and carried by an ASTRA request. The page moves **PARTIAL → DOCUMENTED**:
`documented_rule.py` READY ([`documented_rule.out`](documented_rule.out)). The old status text is kept after the new
lead.

**A-drift:** none. The page was already evidence-bearing (readiness BEHAVIORALLY UNDERSTOOD), and `adrift_report.py` is
unchanged (`Tools/work/OPUS/adrift-report-0930-b10w-after.out`).

**Routed (from the batch's consumer check):**
- `widget-message-handlers.tsv` has no row for `002B6DB0`, and batch 10's `002985C0` note there is still pending.
- `the-widget-constructor-and-object-sizes.md` calls `002B6DB0`'s jump table "not decoded".

## Review (OPUS)

STRUCT's answers go to SWE2-AUDIT-SPEC, and this owner read goes to SWE2-AUDIT-SEM. Both are filed at publish.
