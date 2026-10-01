# DD owner re-status, batch 16: five pages to DOCUMENTED, AUDIT-SEM's corrections incorporated, A-drift paired (OPUS, 2026-10-01)

FABLE is inactive until reset, and the user authorized OPUS to do every non-ASTRA task meanwhile, including FABLE's
incorporation of review corrections. Each page below passes `documented_rule.py`
([`documented_rule.out`](documented_rule.out), **TALLY READY=5 of 5**). Each owner read checked the page's open-items
section: every item is struck, answered or carried, and no unstruck sentence contradicts an answer.

## Applied (OPUS)

| page | what was carried or corrected | status |
|---|---|---|
| `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md` | GR-11's answer (`59ec09a95`) appended to §9's camera-context item; the status line, which still listed GR-10 and GR-11 as open, restated | PARTIAL -> DOCUMENTED |
| `16-UI/Battle-Hud/the-battle-hud-layout-readers.md` | SWE2-AUDIT-SEM's N3 ([`auditsem-review-sd125-128-0930`](../auditsem-review-sd125-128-0930/REVIEW.md)): SD-128's "fade level" and "anchor" become labels on channel 11, which is named nowhere; the stale status line (SD-126 and SD-127 "open") restated | PARTIAL -> DOCUMENTED |
| `16-UI/the-selection-the-menu-publishes.md` | the same review's C1 (the in-play sentence gains the `001EDEC0` gate and the bit-8 gate) and N1 (the "`00279E20` rewrites the whole dword" clause struck; the `002465F0` memset is why the bit starts clear) | PARTIAL -> DOCUMENTED |
| `12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md` | SWE2-AUDIT-SEM's C4 ([`auditsem-review-gr19-gr11-0930`](../auditsem-review-gr19-gr11-0930/REVIEW.md)): the list body draws the entry either way, and the stash flips `+0x5A`; the arms' gates added; GR-12's answer carried onto §11.3 | PARTIAL -> DOCUMENTED |
| `16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md` | the Audio-entry box was still partial (`[~]`) after its own 2026-09-15 answer (FABLE) closed it; it is now ticked | PARTIAL -> DOCUMENTED |

Old text is kept under strikes. The C1, N1, N3 and C4 wording is the reviewer's, attributed in place.

## A-drift, paired (OPUS)

The equipment page's re-status makes `0034A300` A (`@0034A312`). It is in NativeAdapter.PredicateGuardConstCall, so
`exact_remove.py` gives 4 -> 3 and `round7_notes.py` adds the dated note. The numeric-formatting page makes nine members A in five rows:
- ExplainedCalleeForwarder 488 -> 487 (`002A7A40`);
- CallResultTailCall 62 -> 60 (`0017F940`, `0017F9A0`);
- CallResultWithSavedIntTailCall 32 -> 31 (`0017F8C0`);
- ByteSaveSecondArgResultTailCall2 5 -> 4 (`0017F920`);
- **NativeLeaf.GlobalArrayFlagScan 4 -> 0** (`002A28E0`, `002A2940`, `002A29A0`, `002A2A00`, the four confirm-button
  getters the page reads whole).

An emptied row is refused ("a zero-case cannot pass"), and all four of its members are now explained one by one, so
the row is **retired**: its line is removed from `generated-function-families.md`, and its members file keeps a
retirement header. `select_frontier_form_clusters_4.py` still emits that family; this is routed to SWE2-EC7. The notes
come from `round7_notes.py` and `round8_notes.py`.

After pairing:
- `adrift_report.py`: 0 refused rows;
- `check_dispositions`: frontier 4,483, families 335 accepted / 0 refused;
- `check_family_forms`: MISMATCH 0.

The active-party, battle-HUD and selection pages make no member A.

run: documented_rule.py READY 5 of 5; adrift_report.py refused rows 0 (FAILS 0)

## Review (OPUS)

The owner reads go to SWE2-AUDIT-SPEC. The incorporation of AUDIT-SEM's corrections is reported to FABLE, whose
requests (`OPUS-REQ-FABLE-SD125-C1-1001`, `OPUS-REQ-FABLE-GR19-GR12-C1C4-1001`) it partly discharges.
