# DD owner re-status, batch 6: SWE2-CONTRACT's content batch 10 read; one page to DOCUMENTED, five stay PARTIAL with named residue (OPUS, 2026-09-30)

SWE2-CONTRACT's DD batch 10 ([`swe2contract-ddres-b10-0930`](../swe2contract-ddres-b10-0930/README.md); `b10_checks.py`
245 PASS, FAILS 0, re-run by OPUS with identical output) answered the residue that six pages' status lines named. OPUS's
owner read follows FABLE's ruling ([`status-currency-ruling-fable`](../status-currency-ruling-fable/README.md)): a page
reads DOCUMENTED only when no prose residue without a register id remains.

## The verdicts (OPUS)

| page | verdict | what keeps it PARTIAL |
|---|---|---|
| `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md` | **PARTIAL → DOCUMENTED** (READY, [`documented_rule.out`](documented_rule.out)) | none: SD-182 is answered, every box is closed, and the constants and planted siblings are on the page |
| `16-UI/Widget-Object-Model/the-widget-message-protocol.md` | stays PARTIAL | prose the status line did not name, for example "the three individual meanings stay open" (§4) and "20 application senders not read" (the sender table) |
| `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md` | stays PARTIAL | proposed row P7 (the mode-0 `.efb` request); runtime-only: the `0x700` relocation's base |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md` | stays PARTIAL | proposed rows P1 and P2; runtime-only: which `@FEF` models a session loads, and the target-bearing arm |
| `17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md` | stays PARTIAL | runtime-only: co-drawn shared-key models; the front-matter `audit.note` still lists answered items |
| `17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md` | stays PARTIAL | proposed rows P3-P6; the front-matter `audit.note` still lists answered items |

**Route for the residue:**
- **P1-P7 are static questions.** They go to the next OPUS lane batch to be answered rather than opened as new rows.
- **The runtime-only items go to SWE2-DATA.** Each would become a register row closed under the runtime rule.
- The pages re-status once those land.

**A-drift:** none. `adrift_report.py` is unchanged by this batch (`Tools/work/OPUS/adrift-report-0930-b10-after.out`).

**Routed consumers (from the batch's consumer check):**
- `06-Movement-And-Navigation/heading-speed-to-position-delta.md` reads `00381450` differently from the box-primitive
  reading.
- `03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md` gives `00378230` as 114 B, but its extent is 619 B.
- `widget-message-handlers.tsv` still calls `002985C0` an open edge.

## Review (OPUS)

SWE2-CONTRACT's answers go to SWE2-AUDIT-SPEC; this owner read goes to SWE2-AUDIT-SEM (both filed at publish).
