# Consumer check: FABLE's routed OV-10 / OV-16 / OV-42 and slot-ABI text on OPUS-led pages (OPUS, 2026-10-02)

Two record-page rows are corrected with strikes. One row on the modules page has its citation re-expressed as
ENTRY + offset. Everything else is additive.

- **Affected:** 04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md, 04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md, 09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md, 01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md, 07-Combat-Action/CONTRACT-native-command-seam.md, 22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the five pages above (OPUS-led) | revised-here |
  | the modules page's `00686C40` row (OPUS text, applied by SWE2-FRONTIER) | revised-here (citation re-expressed) |
  | FABLE's actor-request page and CONTRACT-interpreter-core.md | agrees (consumed by FABLE at e828e3f50) |
  | the script-binds page (SWE2-CONTRACT) | routed-to-SWE2-CONTRACT (FABLE's own route, plus OPUS-REQ-CONTRACT-SCRIPTBINDS-INT3-CITE-1002) |
  | `Battle-Unit/the-battle-unit-field-map.md` | routed-to-SWE2-FRONTIER (FABLE's own route in the slot review) |
  | register rows OV-10, OV-16, OV-42 | agrees (static and conditional; the open parts stay open) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-ov-routed-consumption-1002/ov_check.py, verified at 36d76cacb: 15 checks,
  FAILS 0 ([`ov_check.out`](ov_check.out)).
- **Gates:**
  - **adrift_report:** 0.
  - **nb_page (pass-22 preview, six pages):** NO NEW HITS.
  - **verify_doc_addresses --all:** 1 document, the SWE2-CONTRACT page above. Its only REVIEW address (`003DBE92`) is
    in SWE2-CONTRACT's own uncommitted hunk and is routed. None of the six pages is flagged.
