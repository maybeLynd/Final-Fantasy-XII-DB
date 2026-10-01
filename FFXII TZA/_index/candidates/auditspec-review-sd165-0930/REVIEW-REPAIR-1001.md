# REPAIR REVIEW: SD-165 repair on REJECT

- **Task:** `OPUS-REQ-AUDITSPEC-SD165-REPAIR-1001`
- **Commit reviewed:** `0ea7dbefc`
- **Reviewer:** SWE2-AUDIT-SPEC — this lane issued the original REJECT; review covers whether the repair resolves it.
- **Verdict: ACCEPT**

## What the original REJECT charged

The original census was incomplete/incorrect: wrong entry set (thunk jumps counted as allocators, real
entries `0036A230` and the realloc `0036CAD0` missing) and a null-test classifier with five defect classes
(dK/dL/dJ/dS/dN named in the original review).

## Repair verification (independently re-run on the certified image, sha `73461d08…21f8`)

Repaired census: **253 call sites over five entries** — `0036A100` (110), `0036A190` (81), `0036A230` (47),
`0036B160` (13), `0036CAD0` (2); thunk jumps removed; realloc added.

All targeted controls reproduce `FAILS 0`:

- E1: entry sites 110/81/47/13/2 = 253. ✓
- C1: tested-then-deref classes verified. ✓
- dK … `STORED`, dL … `STORED`, dJ … `TESTED`, dS … `PASSED`, dN … `DEREF` — every charged defect class now
  has a named-control pin. ✓
- Classifier agreement vs this reviewer's independent per-site classifier: **252/253** identical.

**The one differing site — `0050EF2C`:** independently decoded. `call 0036CAD0` (realloc) → `mov edx,eax` →
tail `jmp 0026B4E0` — the result is forwarded as arg2 to a tail-callee **untested on this site**. OPUS labels
it `PASSED`, my classifier labelled it `RETURNED`; both agree on the substance (unchecked at this site) —
a naming-level difference only. Substantively immaterial.

## Corrected picture the repair establishes

253 sites: **98 test for null, 32 dereference unchecked, 121 hand it on** (passed/returned/stored). The
original record's implicit "all sites check" claim is replaced by a per-site classified census — the
substance of the REJECT stands corrected.

**Verdict: ACCEPT** — all five defect classes resolved as named controls; entry set, site count and
classifier independently reproduced; the single label disagreement is benign and disclosed in the record.
