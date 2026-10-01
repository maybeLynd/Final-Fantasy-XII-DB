# Pending consumer propagation

Finding: local HP floor/cap invariant requires ordered bounds; source formula is
already correct. New original-code/live cases0, symbolic witnesses4, retained
EXP093 positive controls5. Exact primary bytes and consumer snapshots are pinned
by source.json; check.py validates branch structure and rejects the universal
two-sided bound on both inconsistent-bound witnesses. Historical mutations unchanged.

| current consumer | affected claim | disposition |
|---|---|---|
| OPUS CONTRACT-hp-write-and-lethal-transition.md §4 | floor<=HP<=cap with stats-record-only precondition; same bound survives second store | routed-to-ASTRA-RETURN-OPUS-HP-FLOOR-CAP-PRECONDITION |
| FABLE Current-HP/the-hp-write-and-the-lethal-transition.md | HP cannot violate floor/cap; only bottom result is floor | routed-to-ASTRA-RETURN-FABLE-HP-FLOOR-CAP-PRECONDITION |

PENDING PROPAGATION and independent review. This package does not edit those
peer-owned records or close their claims. Their owners supply canonical consumer
checks when incorporating the precise precondition and store/callee scope.
