# Affected-consumer check: render-record pool contract §19, the +0xCC precondition removed (OPUS, 2026-09-27)

**State: PENDING REVIEW.** The owner applied the amendment, consuming FABLE-REQ-OPUS-POOL-CONTRACT-S19-SELECTOR-PRECONDITION.
Independent acceptance is routed to SWE2-AUDIT-SPEC.

**The ruling.** `004235C0` tests both normalised kinds before its selector switch:
- the candidate at `004236B0`–`004236E9`;
- the current event at `0042370D`–`00423727`.

A `+0xCC` of 0, 1 or 2 (kind 0), or a negative value (kind 0xF), returns 1 there. So from `0041FCA0` the policy
always returns 1, and `+0xCE` is selected whenever `+0xC8 != -1`. OPUS re-read the bytes, and FABLE's U3/U10 re-run
passes.

**What this corrects.** OPUS's own 2026-09-13 §19 sentence "if and only if `+0xCC` is never 0, 1 or 2" is struck.
The mode/id confusion reading is kept as description.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md` §19 | precondition struck, amendment added | revised-here |
| `17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md` §4 | already argues the kind-0 exit | agrees |

Corrects: 17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md

Run receipt: `_index/candidates/uq194-event-entry/uq194_event_entry.py` executed at edd315c10 (FAILS 0).
