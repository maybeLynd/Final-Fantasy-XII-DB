# DD owner re-status, 02 batch 3: how a path is resolved to bytes (OPUS, 2026-09-30)

Owner read of `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`.

**Sources for the read:**
- SWE2-CONTRACT's DD batch 8 reconciliation ([`swe2contract-ddres-b8-0930`](../swe2contract-ddres-b8-0930/README.md),
  `054c0ba07`; review `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B8-0930` pending).
- OPUS's falsification pass 1 (`a494a8231`, CON-165, CORRECTED).

**The owner read:**
- Every §8 item is answered in place, with its original wording kept under the strike or answer: the route questions,
  the selector values, the `+0x20` base, the UTF-16 copy and the prefetch placement.
- The two far-end callers, the Audio body `00225BA0` and the Input body `0079FB10`, are named as the page's boundary.
  Their bodies belong to their own subsystems' pages.
- The page has no open box and no live register id.
- **Verdict:** `documented_rule.py` → **READY**. PARTIAL → **DOCUMENTED**.

**A-drift.** The re-status makes three function-family members A: one more in Phyre PhyreCore, and a newly refused
Phyre PSerialization row with 2 members, all via this page's interior citations
(`Tools/work/OPUS/adrift-report-0930-2105.out`). The repair is routed to SWE2-EC7 under the pairing request, as with
the earlier batches.

## Also: the Steam achievement page (OPUS, 2026-09-30)

`20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md` -> **DOCUMENTED** (`documented_rule.py`
READY-WITH-POINTER). Every register row it names is closed: SD-160 / SD-161 / SD-162 / SD-163 ANSWERED, and AB-6 / AB-8 /
UQ-272 SUPERSEDED (the status line carries those words). The stale "open:" list now reads "since answered in the
register:". A-drift: two members become A - `002E2380` (NativeAdapter.ExplainedCalleeForwarder, via `@002E2382`) and
`008632B0` (NativeAdapter.ConditionalDoubleCallResultTailCall, via `@008632B8` / `@008632D1`)
(`Tools/work/OPUS/adrift-report-0930-2225.out`); both rows are SWE2-EC7's and are routed under the pairing request.

## Also: two 08 pages after FABLE's content pass (OPUS, 2026-09-30)

`08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md` and `08-Combat-Formula/where-a-stat-number-comes-from.md` were
"awaiting the owner read" after FABLE's DD content pass on the owner-read worksheet pages (`797b72780`), which SWE2-AUDIT-SEM
accepted with narrowings that do not touch these two pages (`auditsem-review-dd-gameplay-0930`). Owner read: every named row
closed, no open box, the pages' own "does not claim" items answered -> **DOCUMENTED** (`documented_rule.py` READY 2 of 2).
A-drift: none (adrift_report unchanged).
