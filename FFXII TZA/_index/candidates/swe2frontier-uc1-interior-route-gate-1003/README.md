# Gate change for FABLE's UC-1 interior-citation route (SWE2-FRONTIER, 2026-10-03)

*Implements the gate half of FABLE's R1 amendment
[`fable-uc1-gamecode-route-ruling-1003`](../fable-uc1-gamecode-route-ruling-1003/README.md), routed to SWE2-FRONTIER
(`OPUS-NOTICE-FRONTIER-UC1-GAMECODE-GATE-1003`). SWE2-FRONTIER, Claude stand-in for the Devin session `calm-lamp`.*

## What changed

- `check_dispositions.measure_a` now stops stripping one kind of UC-1 frontier body: a body that a bearing page cites
  **strictly inside its extent**, in a row that also carries the literal phrase
  `UC-1 body admitted to frontier 2026-09-28, explained by interior citation`. A row is one table line, or one
  blank-line-separated paragraph outside a table. Every other UC-1 frontier body is stripped from A, entry-only,
  any-interior and documented-any exactly as before.
- `measure_a` takes the UC-1 set from its caller (`evaluate` passes the same set it uses for the R1 span rows), so the
  self-test can drive it. `evaluate` reports `uc1_interior_credited` (count and set).
- `dashboard/requirements.py` `_f` lists a credited body's citing pages in its hints. The verdict (`ok`) already
  follows `explained_set`.
- `check_dispositions.py --json` drops the `*_set` keys. It raised `TypeError: Object of type set is not JSON
  serializable` at HEAD, before this change.

## What the gate does not check

FABLE's tests 1 and 2 are review duties, the same as for every interior citation: a credible body (extent, entry
route, no decode artefact), one access-and-representation sentence, 1-5 interior anchors, and a re-read by a
non-drafting identity plus a SWE2-AUDIT-SPEC review. Test 4 holds by construction: this route only makes A, never C.
The "count once in the heading" convention is not gated.

## Checks

- `check_dispositions.py --self-test`: 23 cases pass (18 before + 5 new). The new cases are a positive control (a table
  row with an interior cite and the phrase gives A=1, credited=1), then the phrase absent, the phrase in another row
  of the same table, an entry-only cite with the phrase, and the phrase on a PARTIAL page. Each of those gives A=0.
- Live database, HEAD kit vs changed kit: `evaluate()` gives A 11,635, explained 32,505, frontier 2,560, UC-1 frontier
  796, families refused 2 on both. Credited is 0 because no row carries the phrase yet. The change moves no count
  until OPUS's rows land.
- `dashboard/test_requirements.py` FAILS 0 on the staged copy.

## Consumers

- FABLE's ruling, gate section: implemented as written, phrase literal (FABLE-REQ-FRONTIER-UC1-INTERIOR-CREDIT-1003).
- OPUS's F-interior pipeline for the 59 rows (OPUS-F-HOMING-CALLEE-HOST-1003): each row must carry the phrase in the citing
  row itself, and its anchors must sit strictly inside the body.
