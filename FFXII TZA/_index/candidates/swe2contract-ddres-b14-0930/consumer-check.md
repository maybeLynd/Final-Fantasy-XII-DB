# Consumer check: DD batch 14 corrections on four pages (SWE2-CONTRACT for OPUS) - owner re-status pending, 2026-09-30

SWE2-CONTRACT's batch 14 (this folder's README) answered the questions batch 10 proposed as register rows, in place on
their pages, and struck the statements those answers supersede. No status word was moved; OPUS re-statuses after its
owner read.

- **Corrects:**
  - in efx-and-efb-effect-containers.md: §2b's "Not read: what mode 0 is for, and whether a mode-0 and a mode-1
    request can both be pending for one map (each publishes at 02ADD088)";
  - in fef-and-motion-entries.md: "Remaining caveat: a reader through a *copied* pointer, or via the magic dispatcher
    003EDAD0, is not excluded", "(the residual caveat is a copied-pointer or 003EDAD0-dispatched reader, not a direct
    one)", the batch-10 bullet "The embedded EFX0010's remainder (a reader through a copied pointer, or a
    003EDAD0-dispatched use)" and the Residue item "Not excluded: a copied-pointer reader or a 003EDAD0-dispatched use
    — a bounded remainder, not a live lead";
  - in ftr-node-table.md: the §4 statements "its field semantics stay open (UQ-218 residue)" and the four batch-10
    notes that called the bone semantics, the aux values, FCP section 2 and the consumers' field use open or proposed
    rows; the R3 sentence "Their full field use is proposed as a register row (the batch record)"; and the front
    matter's "the record flag vocabulary is not established. Not read - the runtime consumers of the 0x290 records and
    of the relinked tail beyond the address pass";
  - in fte-fct-texture-colour-tables.md: the front matter's "Not read - the FTE +0x1C cache-key semantics, the FCT
    +0x08 id word's use, and how @FCT sub-indices are chosen" (answered by batch 10, T2, T4-T5, T8).
- **Affected:** 17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md, 17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the four pages' own sections, front matter and status lines | revised-here (status lines unchanged; proposals in the README) |
  | the-map-ctrl-pack.md §3.1 (00377DC0 requests the loose PS2Data\efb\<map>.efb, completions 003788F0 / 003789A0) | agrees |
  | map-ref-field-packs.tsv (own and block indices per field) | agrees (control Q11: equal in all 1,315 rows) |
  | uq218-embedded-efx-sweep/README.md ("Not claimed: a reader through a copied pointer ... or any native effect of the magic") | agrees; the caveat it leaves is closed by A1-A9 (routed, not edited) |
  | fcp-character-parameter-block.md, the UQ-220 box (section 2 = the rig, ANSWERED 2026-09-26) | agrees and is cited (D1); the page carries SWE2-STRUCT's uncommitted batch-12 edits and was not opened for editing |
  | the-rig-of-seventeen-controllers.md (the rig at +0x94) | agrees; C6 lists the rig's +0x94 readers |
  | the-bone-trails.md (003711D0 refuses a bone index at or past the skeleton's count) | agrees and is cited (B2) |
  | fef-and-motion-entries.md's @FMW apply-path table (node +0x190 / +0x1B0 / +0x1D0 staging, +0xF0 translation, +0x100 scale) | agrees; G5 and C4 read the same fields |
  | b10 record (swe2contract-ddres-b10-0930/README.md, proposed rows P1, P3-P7) | answered here; P2 by OPUS (opus-look-bit7-0930) |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b14-0930/b14_checks.py (317 checks, FAILS 0,
  including the map_ref.bin and .efb census against the archive, the unicorn control on 00674A00, both structflow
  censuses with their positive controls, and the 27,561-record aux-pool walk).
- run: b14_checks.py at e2cb21305 (317 PASS, FAILS 0)
