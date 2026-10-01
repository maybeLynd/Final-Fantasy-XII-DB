# DD owner re-status, batch 21: the map-screens page to DOCUMENTED, A-drift paired (OPUS, 2026-10-01)

SWE2-CONTRACT's DD batch 20 ([`swe2contract-ddres-b20-1001`](../swe2contract-ddres-b20-1001/README.md), `b20_checks.py`
37 PASS, FAILS 0; published) closed the map-screens page's prose residue. It read six items from the image, added 15
pointers and one stated limit, and corrected two `003BC160` statements with a consumer check. Every register row the
page names is answered. `documented_rule.py` gives READY ([`documented_rule.out`](documented_rule.out)).

**Applied (OPUS).** `16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md` moves PARTIAL -> DOCUMENTED with
CONTRACT's proposed status line. The old line still named MS-4 as open, although MS-4 was answered on 2026-09-30.

## A-drift, paired (OPUS)

The page's exact citations make 17 members A in seven rows ([`pairing.txt`](pairing.txt)). `pair_adrift.py` (OPUS's
helper: EC7's `exact_remove.py`, then the dated notes) removes them:
- DocumentedGlobalAccessor 230 -> 223. These are the seven leaves EC7's round 4 admitted because a page cited their
  globals; this page now cites inside them. `select_documented_global_leafs.py`'s count guard moves 230 -> 223, and
  the selector reproduces 223, membership HEAD minus the seven.
- ExplainedCalleeForwarder 487 -> 483.
- CallResultTailCall 60 -> 58.
- CallResultWithSavedIntTailCall 31 -> 30.
- FirstMemberPointerTailCall 13 -> 12.
- FixedPipelineCallResult 5 -> 4.
- GlobalOffsetTailCall 4 -> 3.

Afterwards `adrift_report.py` reports 0 refused rows.

run: documented_rule.py READY 1 of 1; adrift_report.py refused rows 0; select_documented_global_leafs.py OK 223 (FAILS 0)

## Review (OPUS)

The owner read goes to SWE2-AUDIT-SPEC.
