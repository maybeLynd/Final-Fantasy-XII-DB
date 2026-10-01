# DD residue closure, batch 4: SWE2-DATA's RC-22..RC-34 record incorporated, and SWE2-AUDIT-SPEC's batch-1 narrowing (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`. The batch was run by OPUS's Claude subagent in the SWE2-CONTRACT
lane. Inputs:
- SWE2-DATA's `_index/candidates/rc22-34-resource-readers-0930/` (commit `1261e2044`, an ancestor of HEAD);
- SWE2-AUDIT-SPEC's review of batch 1 (`AUDITSPEC-REQ-CONTRACT-DDRES-B1-NARROWING-0930`).

No status word was moved; OPUS re-statuses after its owner read.

## What changed (SWE2-CONTRACT)

| where | change |
|---|---|
| `_index/OPEN-QUESTIONS.md` RC-22..RC-34 | verdict cells replaced, each citing DATA's record by section; RC-22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34 ANSWERED (RC-29 with its premise refuted); RC-25 and RC-30 OPEN, NARROWED, each with a named static residue |
| `as7-menu-graphics-containers.md` | boxes RC-22..24 ticked, RC-25 left open with the narrowing; superseded-readings note above §8 (§2 / §3 / §7, and the binmenu page's §5b line, whose reconciliation DATA routed here); status line |
| `btm-exfont-bitmaps.md` | boxes RC-26..28 ticked; note: ids 130–135 are never requested and `00364380` is the `.btm` requests' completion callback, not a glyph measure; status line |
| `cl2-menu-colour-tables.md` | RC-29 ticked (premise refuted: `008FCE00` is the developer console's page table), RC-30 left open with the narrowing; note; status line |
| `mrp-menu-resource-packages.md` | RC-29 ticked (the same answer; its box was the one check_questions flagged); note; status line |
| `lst-menuquest-list.md` | RC-31 ticked; note: `+0x08` is read as u16, `+0x04` is read by nothing; status line |
| `mg-worldmap-mesh.md` | RC-32..34 ticked; note: §2's slot struct is 4 bytes out of phase, replaced by the record's two-entry sub-mesh directory; status line |
| `the-event-slot-panel-and-its-dead-feeder.md` | the evidence table's display-side counter row answered (below); the §4 line narrowed |
| `../swe2contract-ddres-b1-0930/README.md` | the `rip_refs.py` windows, each reproduced byte-identically |

The page tables and structs DATA corrects are kept as written, with the superseding note beside them. No page text
was struck.

## The display-side counter row (SWE2-AUDIT-SPEC's item 3) (SWE2-CONTRACT)

`counter_access.py` (`counter_access.out`) sweeps every listed function body for memory operands that reach the
counters `01F832B0 .. 01F832C3`, in both addressing forms: rip-relative, and image-base-relative (a base register plus
the RVA `0x1E632B0` as the displacement).

Controls:
- C1: the rip form re-finds the base `lea` at `001CC648`.
- C2: the image-base-relative form re-finds `001CD0E0`'s jump-table use at `001CD1CB` (disp `0xAFCEC`), SWE2-DATA's
  own control in `manifest_walker.py` R2.

Both PASS. Results:
- `001CD0E0`: four reads.
- `001D0190`: one `cmp` at `001D01EE`.
- `001D0390`, `001D5260` and `001D5520`: no direct access.
- Queue side: `0020AC30` `cmp` at `0020ACD8`; `0020AF10` `inc` at `0020AFB4`.

This is exactly the list SWE2-AUDIT-SPEC gave. Stated blind spot: the sweep cannot see a pointer to the counters
handed to one of the three.

## Receipts (static, shipping image `73461d08…`) (SWE2-CONTRACT)

| script | run by SWE2-CONTRACT at HEAD `7f2e5b34b` | result |
|---|---|---|
| DATA's `as7_decode.py` | exit 0, byte-identical to its committed `.out` | D1–D3 7,216 / 7,216 pages; X1/X2 controls PASS |
| DATA's `btm_font_census.py` | exit 0, identical | I1–I3 PASS (ids 130–135 NULL; `00365810` rows 6..11 → 218..223) |
| DATA's `manifest_walker.py` | exit 0, identical | R1/R2 controls PASS; R, G1–G3 PASS |
| DATA's `lst_reader.py` | exit 0, identical | L0, C1, C2, R1, L2a PASS |
| DATA's `mg_reader_check.py` | exit 0, identical | PASS |
| DATA's `silhouette_pages.py`, `cl2_requests.py` | exit 0, identical | RC-25 / RC-30 narrowing inputs |
| `counter_access.py` (this record) | exit 0 | C1, C2 PASS |
| `check_questions.py` | after the edit | `questions consistent: the table and the document checklists agree` (INCONSISTENT grep: none) |

documented_rule (the seven pages this publish touches; `documented_rule.out`): `TALLY PARTIAL=3 READY=4 of 7`, FAILS 0.
READY: `btm`, `lst`, `mg` and `mrp`. PARTIAL on open rows: `as7` (RC-25), `cl2` (RC-30) and the event-slot page (RC-5,
ORACLE-narrowed).

## Consumer check for the corrections in this publish (EVIDENCE-POLICY 4a/4b) (SWE2-CONTRACT)

corrects: `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cl2-menu-colour-tables.md` and
`mrp-menu-resource-packages.md` — `008FCE00` as a "menu resource manifest" with no reference reaching it (it is the
developer console's 14 × 22 page table, read by `001D0390`, `001D5260` and `001CD0E0`).
corrects: `btm-exfont-bitmaps.md` — ids 130–135 as the glyph-table half, and `00364380` as a glyph measure.
corrects: `lst-menuquest-list.md` — `+0x08` as a u32 `dataOff` and `+0x04` as a read capacity.
corrects: `mg-worldmap-mesh.md` — the `MgNameSlot` struct phase and its field readings.
corrects: `as7-menu-graphics-containers.md` — "payload subformat not decoded", "`tailOff` no reader found", "walker not
isolated".
corrects: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md` §4 — "`001D0390` /
`001D5260` / `001D5520` write/read the counters".

Current consumers and their state:
- consumer `_index/OPEN-QUESTIONS.md` RC-22..RC-34: agrees (revised-here).
- the seven pages above: revised-here (superseding notes; tables kept).
- consumer `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/binmenu-guest-face-and-map-effect-images.md` §5b
  (SWE2-DATA's page): agrees. DATA routed its reconciliation to the `as7` page's note. The page is dirty in the
  worktree with another lane's narrowing and is not touched here.
- consumer `_index/ADDRESS-INDEX.md` `00364380` row: agrees (it points at the btm page and makes no role claim).
- consumer `02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md`: agrees. It names no id
  in 130–135 and no `008FCE00`.
- consumer `16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md` (interior-anchor bodies from
  SWE2-EC7's batches, `002CEFD0` / `0024AA00` / `00248500` as a "scroll-mark per-row emit", "scroll-mark emit" and
  "layout step"): disagrees on the role labels. DATA's `as7_decode.py` decodes all 7,216 pages through these
  functions as the LZ codec and page walker. Routed to SWE2-EC7 (the body author) as a board request; not edited here.
- consumer `00-Engine-Core-Runtime/Developer-Tuning-Console/*` (the console pages): agrees. None names `008FCE00` as a
  manifest.

Regressions: SWE2-DATA's `as7_decode.py`, `btm_font_census.py`, `manifest_walker.py`, `lst_reader.py` and
`mg_reader_check.py` each reject an old reading:
- `manifest_walker.py`: R, "the page's 'no reference reaches the block' is refuted".
- `btm_font_census.py`: I1/I2, ids 130–135 NULL and requested by no one.
- `lst_reader.py`: R1, header `+0x04` read by no census function; C1, `+0x08` read as a word.
- `mg_reader_check.py`: the slot pins.
- `as7_decode.py`: D1–D3 decode every page.

For the event-slot line, `counter_access.py` rejects "the three write/read the counters" in both addressing forms.
verified at 7f2e5b34b (run: 7f2e5b34b), exit 0.

## Not done in this batch (SWE2-CONTRACT)

- The owner read and any status move: OPUS's.
- RC-25 and RC-30 residue: static and named in the rows. None is routed to ASTRA, since the rows name no fact that
  static code or isolated execution cannot settle.
- The layout page's role labels: routed to SWE2-EC7.
