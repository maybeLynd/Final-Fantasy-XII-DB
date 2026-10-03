# Production status residue reconciled before terminal certification (FABLE, 2026-10-03)

*FABLE, on the user's `FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03` (copy in `Database/Tools/work/FABLE/`),
sections 2, 3, 4, 9 and 10. Measured at HEAD `8a00f8bd5`. No page is promoted to reduce a count. Every change below
either registers open knowledge, or carries an already-made decision to a line that never received it.*

## The instrument

`Database/Tools/analysis-kit/gfz-scripts/check_status_residue.py` is new and generated from source; it adds no
completion score.
- It reads every production system page's status word.
- For each PARTIAL, REOPENED or STUB page, it maps every register id the status line names to that row's live state.
- It classifies the page as LIVE-ROW, PROCESS-ONLY or UNMAPPED.
- `FAILS N` is the number of UNMAPPED pages.
- Its six-case self-test passes. `--json` is the input for the dashboard view the audit asks for in §9.

**At `8a00f8bd5`.**
- 369 production pages: AUDITED 233, DOCUMENTED 119, PARTIAL 15, REOPENED 2. The audit counted 376; this tool skips
  `_types/` and `_index/`, and the PARTIAL and REOPENED pages are the same 17.
- **LIVE-ROW 16, PROCESS-ONLY 0, UNMAPPED 1.** The UNMAPPED page is the kind-`0x54` page, exactly the case the audit
  named.

## The 17 non-final pages

| page | status | owned by | action here |
|---|---|---|---|
| `the-query-record-from-initialization-to-reuse` | PARTIAL | OV-8 (PARTIAL, runtime) | none |
| `the-actor-request-from-arming-through-start-and-return` | PARTIAL | OV-10 (PARTIAL, runtime) | none |
| `the-script-from-bytecode-through-wait-and-resume` | PARTIAL | OV-16 (OPEN, runtime) | none |
| `the-external-source-owner-and-borrowed-view-lifetime` | PARTIAL | OV-19, OV-21 | none |
| `the-indexed-source-request-from-arm-to-terminal-pump` | PARTIAL | OV-21, OV-33, OV-42 | none |
| `the-nonempty-prf-registration-and-specialized-relocation` | PARTIAL | OV-42 | none |
| `the-resource-owner-from-copy-or-borrow-to-disposal` | PARTIAL | OV-42 | none |
| `the-resource-request-queue` | PARTIAL | OV-19, OV-33; plus a class-2 process item (SECTION-02 peer acceptance, `SWE2CONTRACT-REQ-AUDITSPEC-SECTION02-ACCEPT-0930`) and OPUS's owner read | none; the process item stays visible on the line |
| `experience-and-license-point-award` | PARTIAL | GR-18 | none |
| `how-experience-is-computed-and-divided` | PARTIAL | GR-18 | none |
| `where-the-games-memory-comes-from` | PARTIAL | GR-18 (fourth case) | none |
| `the-title-asset-singleton-and-its-distinct-consumer` | PARTIAL | OV-29 (OPEN, runtime) | none |
| `efx-and-efb-effect-containers` | PARTIAL | SD-194 (OPEN, runtime) | none |
| `reflected-render-parameters-and-shader-assets` | PARTIAL | OV-42 | none |
| `effect-mesh-records-kind-54` | PARTIAL | **nothing** (SD-140 is ANSWERED) | **registered SD-196…SD-199** |
| `the-encoded-id-space-and-the-query-record` | **REOPENED** | OV-5 (PARTIAL) | **owner re-status to PARTIAL**: its reason was stale (§4A below) |
| `how-a-script-binds-to-an-actor-and-how-requests-are-scheduled` | **REOPENED** | OV-10 (PARTIAL) | **owner re-status to PARTIAL**: its reason was stale (§4B below) |

### §3 The kind-`0x54` page: an accounting gap, confirmed and closed by registration

The status line says three items are open; the page's *Not established* list has four. No live row owned any of
them. FABLE's own `fable-k54-residue-1003` left them as prose, and SWE2-DATA applied that prose faithfully. That was
FABLE's gap. The four are registered:

| row | open item | kind |
|---|---|---|
| **SD-196** | what the matrices `02AEEA20`, `02AEEBF0` and `02AEEAA0` hold at draw time | runtime |
| **SD-197** | the planar scalars authored as resource or curve tracks (track kinds `004309C0`, `00430540`, `004307C0`) | static |
| **SD-198** | the runtime pass index after a failed texture lookup | runtime, with a static narrowing |
| **SD-199** | what `+0x1F1` bit 3 changes in the drawing beyond selecting the path | static |

FABLE owns the two static rows and will work them. The runtime rows go to ASTRA through the usual queue. The register's
OPEN count rises by four. That is the honest number, and it is the point of the audit.

### §4A The encoded-id page: REOPENED reason stale

The line said "independent acceptance pending". SECTION-05 was independently **ACCEPTED on 2026-10-01**
(`auditspec-review-section05-1001`, `68eec56bc`). The page is re-statused PARTIAL, with OV-5 (c) and (d) open, both
runtime. This is the same owner re-status FABLE made on 2026-10-02 for two pages whose reopening cause was resolved.
The contract is OPUS's, and OPUS may restate the line.

### §4B The scheduling page: REOPENED reason stale, and a FABLE adjudication that never reached its consumers

The line said "FABLE adjudication pending (RC-12)". FABLE adjudicated RC-12 on **2026-09-30 at `a8aed6ca9`**
(`auditsem-corrections-fable-0930`). It accepted ORACLE's 0-based footer, and every reader slot in FABLE's own table was
one too high. FABLE corrected that record then. OPUS propagated the 0-based reading to the pages and the type store
(`0c7ce4d4b`). Neither this status line nor the RC-12 register cell ever received the adjudication.

FABLE re-ran ORACLE's `rc12_slots.py` at `8a00f8bd5`. Controls A, B and C all PASS: 43 sites in 19 functions. Both
consumers are now updated. The page is re-statused PARTIAL, with OV-10 (runtime) open.

## §10 Pre-terminal prerequisites mapped to existing gates

No new gate is added. Each prerequisite maps to an existing gate or to this record:

| audit §10 prerequisite | where it is enforced |
|---|---|
| all 17 PARTIAL/REOPENED pages reconciled | this record; `check_status_residue.py` FAILS 0 after this publish |
| no open status-line residue lacks a live row or disposition | `check_status_residue.py` (UNMAPPED = 0); `goal_gate.py` *questions* counts the new rows |
| the kind-54 accounting resolved | SD-196…SD-199 (this record) |
| both REOPENED pages have current reasons, or are re-statused | re-statused (this record) |
| the active `knowledge.sqlite` check passes | SWE2-DATA `8c22cbe8f`: rebuilt, pinned to HEAD. `check` lists only tables touched by uncommitted peer edits, and reads CURRENT when they land |
| dashboard and progress consumers agree with source | progress_report `check`; `check_lifecycle_consumers.py`; FRONTIER's `test_lifecycle.py`; DATA's `ps_present_tense_check.py` |
| a risk-based independent L2 sample survives | routed to SWE2-AUDIT-SPEC: the independent role, and FABLE authored many of the verdicts |
| load-bearing L1 contracts justified or completed | routed to OPUS, the contracts owner |
| reconstruction-critical low-maturity type/field residue bounded | routed to OPUS / SWE2-STRUCT, the type store |
| only then the uninterrupted 30-pass campaign | `goal_gate.py` *acceptance*; FINAL-AUDIT-PROTOCOL |

## Consumer check (FABLE)

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md`

affected: `Database/FFXII TZA/01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md`

affected: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md`

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: the three pages' status lines: revised-here.
- consumer: register row RC-12: revised-here. New rows SD-196…SD-199 were added.
- consumer: the scheduling page's section 2 table and section 2.6 sentence: already 0-based (OPUS `0c7ce4d4b`), no change.
- consumer: FABLE's record `rc121314-fable-0930`: already corrected at `a8aed6ca9`, no change.

run: check_status_residue.py at 8a00f8bd5 gives UNMAPPED 1 before the apply (the kind-54 page) and 0 after; self-test
PASS; rc12_slots.py re-run at 8a00f8bd5 with controls A, B and C PASS
