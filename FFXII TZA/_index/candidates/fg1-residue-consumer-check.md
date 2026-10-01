# Affected-consumer check: FG-1's three remaining sub-questions (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The ruling** (control: `_index/candidates/fg1-residue/fg1_residue.py`, 15 checks including 2 mutants, FAILS 0):

- **R1: the rank table's `+4` count.** `00316480` walks the `menuhandbook.bin` `hcom` node at `[022C2550]`.
  - The node holds 45 `{questId, minimum}` entries: ids 128–172, minima 30/50/70/90/100, the same in all nine locales.
  - An entry counts when two things hold:
    - the quest is ordered (`+0x1000`) or cleared (`+0x1020`);
    - its scenario flag `+0x1064[id]` has reached the minimum.
- **R2: the handbook gate-input banks.** `+0x334C` (bits) and `+0x336C` (nibbles):
  - have one writer each, called only by the hdat op executor `00577A40`;
  - have one reader each, called by the hchk gate `00575E80` (and by `00577A40` for the nibbles).

  Shipped data never uses them: 2,844 / 2,844 gates carry the sentinel, and 12,168 / 12,168 op programs are empty.
- **R3: the block `+0x30`/`+0x70`/`+0x90` store** holds the remembered menu cursor positions. Two instructions
  tie it to the Cursor Position option:
  - the option's setter tail-jumps the table clear;
  - the reader asks the option's bit first.

**What this corrects.** Five store rows carried names from readings already refuted or never made:
`achievementStateBitmap100` and `achievementStateNibbles` (the refuted achievement reading, FG-1 2026-09-12), and
`imageStateWordArray`/`ByteArray`/`DwordArray`. They are renamed. The previous meaning cells are kept inside the new
ones, and their extent evidence stands. Each rung (TYPE RESOLVED) is left for the reviewer.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` FG-1 | PARTIAL → ANSWERED, prior status kept (the line rode FABLE's `dd3470a53`; this publish adds its control) | revised-here |
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md` FG-1 box | ticked, answer appended | revised-here |
| `_types/fields.tsv` ImageBackedStateBlock `+0x30`/`+0x70`/`+0x90`/`+0x334C`/`+0x336C` | renamed, meaning cells filled, evidence prefixed | revised-here |
| `16-UI/Handbook/`, `hchk-hctg-hdat-handbook-indexes.md` | already state the executor ships empty; no change needed | agrees |
| `19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md` cmd 8 | already names the table; no change needed | agrees |

**Regression.** R2a rejects any new displacement user of the two banks. R2c and R2d, with mutants M1 and M2, reject
a shipped gate or op program that starts using them. R1f rejects a changed node.

Run receipt: `fg1_residue.py` executed at 5d41f8a5c (FAILS 0; 15 PASS lines).
