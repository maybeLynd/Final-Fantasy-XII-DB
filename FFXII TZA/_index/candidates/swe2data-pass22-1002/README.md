# Pass-22 debt discharge — SWE2-DATA, 2026-10-02

Task `FRONTIER-REQ-SWE2-DATA-PASS22-DEBT`. Routed set per
`pass22-debt-0929/routing.md`: **307 document×subsystem pairs across 48 pages** —
the lane's own 68 (`created_by` DATA / SWE2-DATA / DATA-FMT-PS2IMG-TAIL) plus the
four folder populations 15-Input (73), 18-Audio (103), 19-Save-Load-Settings (44),
20-Platform-Online-Achievements (19).

## Method

1. `_swe2_p22_edges.py` reproduces audit_crossrefs' exact neighbour derivation
   (subject filtering, control-only citation exclusion, R6 guarded far-end
   handling, substrate/hub exclusion, whole-word alias matching, registry
   handling) for the 48 routed documents on their HEAD text.
   Result: **248 live findings on 35 pages**; the other 13 routed pages' pairs
   were already covered by earlier crossing sections.
2. `_swe2_p22_write.py` appended one bullet per unaccounted pair — the
   EC7-established format: subsystem label, CLIENT/SERVICE class from the real
   edge directions, edge count, dominant page-cited subjects and representative
   far ends, each adjacency-verified against `edges.tsv`. 31 pages extended
   inside their existing `## Cross-subsystem neighbours` /
   `## Crossings into other layers` section; 4 pages gained a new tail section.
3. `_swe2_p22_registry.py` appended **307 `CROSSING-ACCOUNTED` rows** to
   `_index/candidates/neighbour-dispositions.tsv`, one per routed pair:
   `unaccounted` marker + real edge samples for the 239 bulleted pairs,
   `CITES-THE-EDGE` for the 68 pairs already covered by existing prose.

## Verification

- Full re-run: `audit_crossrefs.py` at HEAD `1f193fec9`, inputs
  `work/graph/functions.tsv` + `edges.tsv` —
  [`audit-rerun.txt`](audit-rerun.txt). Findings 449 → 201.
- **Zero findings on all 48 routed documents** (drop equals the 248 cleared,
  so no findings moved sideways).
- All 307 routed pairs now carry a registry verdict; `load_dispositions`
  reports 0 unknown verdicts.
- No semantic-hard pair needed FABLE escalation: every bullet names real
  `edges.tsv` ends with direction-derived class; the shared-machinery
  disposition is the fleet-accepted wording for these helper-ring crossings.

## Dispositions

- 239 pairs: prose disposition (crossing-section bullet) + registry record.
- 68 pairs: already prose-accounted; registry verdict records the coverage.
- Registry rows are additive; no seeded rows were deleted.
