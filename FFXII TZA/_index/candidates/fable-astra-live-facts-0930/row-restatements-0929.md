# Register rows restated under the user's specific-fact rule (FABLE, Claude Opus 5.5, 2026-09-29)

The user's rule: no question is ASTRA/live-only merely because its register row says RT. The row must state the
specific fact that A, B or original-code evidence cannot resolve, and ASTRA keeps final method-selection authority.

This publish appends a dated note to six OV rows. It closes nothing: each row keeps its current state. Every note either
names the one remaining fact or says what static work FABLE still owes. The facts come from this record's
[README](README.md) table.

| row | before (the row's remainder) | after (the appended note) |
|---|---|---|
| OV-5, OV-8 | (c) a state base at or above 4 GiB, and (d) over-reservation, both "RT" | (d) answered statically (t3b; save-file bytes are the only entry), with review TAKEBACKS2 pending. Remaining fact: (c) alone, the run-time value of `qword [01F83530]` (AQ-ARENA) |
| OV-16 | "key reuse while pending", RT | static pass complete (the two abandonment routes, RETN depths, REQCANCEL 0). Remaining fact: whether a recycle or replacement removes a parked wait entry and the same function re-runs to the same continuation offset before the old notification is consumed |
| OV-19 | "actual IO issuance/completion timing", RT | remaining fact: whether an owner is deleted while its read is in flight (delete versus IO completion order) |
| OV-29 | "title-asset callback order and cancellation", RT | remaining fact: whether the title is torn down while a ticket is pending, or message 16 arrives after teardown |
| OV-33 | "service issuance/status-production and loading-state timing", RT | (i) answered statically (T1 writer set; SP1 data gap closed, 1c1dfec6b). (ii)/(iii) answered statically per exit ([`../ov33-no-status-exits-fable-0929/`](../ov33-no-status-exits-fable-0929/README.md)): E1 reachable from a save-crystal menu (kind 35 id 9, size -1 everywhere); E3 and loose-route E4 unreachable. Remaining facts: E2 (a cache-only path requested while the map-jump byte is set) and archive-route E4 (a request for one of six archive-missing kind-1 rows) |

**Not restated:**
- OV-10, OV-21 and OV-42 already name their facts (concurrent outstanding requests; concurrent key registration and
  bank fill; a negative index reaching the owner submit);
- ASTRA's OV-42 packets wait for a review independent of FABLE (SWE2-AUDIT-SPEC refused them as FABLE-directed).

**Reviews:**
- FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930 covers OV-5/8 (d);
- FABLE-REQ-AUDITSEM-REVIEW-LIVEFACTS-T1T2T5-OV16-0930 covers T1 and the OV-16 pass;
- FABLE-REQ-AUDITSEM-REVIEW-SP1-GATE-0929 covers the SP1 gate.
