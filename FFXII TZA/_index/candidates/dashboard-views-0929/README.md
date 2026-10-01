# Dashboard: deltas on every tile, and the PARTIAL views measured (OPUS, 2026-09-29)

The user asked for three things: that the views reading PARTIAL (vbf, executable, evidence, fleet) be completed, that
stale or newly found information update promptly, and that every tile show its change since the last refresh.

## What changed (OPUS, 2026-09-29)

- **A change on every tile.**
  - Count measures (no denominator) now carry their signed and relative change since the prior coherent generation,
    rendered `+N (+x.x%)` and coloured by the measure's direction (`annotate_deltas`, test D8, J5).
  - A measure whose denominator moved still gets no percentage-point delta (FABLE's like-for-like rule). It now shows
    both sides' changes, `+a of +b` (D9).
  - Each tab shows its view's headline change from `/api/status` `headline` (server).
- **vbf: PARTIAL -> OK (definition v2).**
  - The tree is read from the INSTALLED archive's own SRYK header at every build (`vbf_index.py`, ASTRA's A17 parser),
    not from the 2026-09-02 listing. Result: 89,414 entries, header `c9e1f530…`.
  - `listing-drift` re-runs ASTRA's listing check every build; it is 0 today.
  - Format stages come from the X family: 46/46 extensions dispositioned, 58/58 bucket member formats explained (the
    members are DATA's table), plus a per-extension disposition column.
  - A failed archive read is FAILED, never a fallback.
- **evidence: PARTIAL -> OK (definition v2).**
  - Verdicts come from the structured `verdict:` refs team.py now requires (A16). Today 17 of 71 formal reviews carry
    one; the rest are being ratified.
  - Sealed receipts are measured with seal.py's own `verify` and `publishable`: 3/3 intact and publishable.
  - Live PENDING PROPAGATION markers are counted (19 documents).
  - All of this comes from `evidence_scan.py` at each build.
- **seal.py repair.** All three EXP-201 receipts were refused as "no cases". The house harness writes a flat
  `{case_id: record}` map, which the gate did not accept. It does now; the exact-case rule still refuses an extra
  case. Test F, with its mutant killed.
- **executable: stays PARTIAL, now for one named reason (definition v3).**
  - The behaviour axis is measured: each population body's F-family disposition (A / B / C / none) over its bytes.
  - **Observed execution** (live or isolated) has no instrument that maps runs to functions, so it is UNMEASURED.
    Routed to SWE2-ORACLE as an instrument request.
- **fleet: stays PARTIAL.** Model, effort, account limits and utilisation are not exposed by the hosts, so they are
  UNKNOWN by the brief's own rule. They are shown as UNKNOWN, not guessed.

## Controls (OPUS, 2026-09-29)

- `test_build_views.py` FAILS 0 (B8's definition pin moves to v3).
- `test_live.py` FAILS 0 (new D8, D9, J5).
- `test_server.py` FAILS 0.
- `test_requirements.py` FAILS 0.
- `test_seal.py` FAILS 0 (new F).
- A scratch store built twice: vbf OK, evidence OK, executable PARTIAL (execution only), fleet PARTIAL (host fields).

## Limits (OPUS, 2026-09-29)

- The archive side is the index only: no payload hash, no decompression, and no binding of a running game to this
  archive.
- The 58/58 members depend on DATA's `_index/bucket-members.tsv`, which is still to be published by DATA.
- A delta compares against the prior coherent generation, so the first build after a definition bump shows "definition
  changed" once.
