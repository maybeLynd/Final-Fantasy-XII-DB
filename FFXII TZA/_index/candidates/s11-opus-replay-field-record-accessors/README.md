# S-11: the seven field-record accessors executed as shipped code over the shipped `navimapdata.bin` (OPUS, 2026-09-25, block 304)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-11's runtime cell is NOT MET: "types PARTIAL and
nothing executed". This is a narrow OPUS harness, not an ORACLE EXP.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image and **stubs nothing**.
- **Failure rule.** Entering any function outside the accessors' own reach (`003148F0`, `002EF2B0`, `002EF640`,
  `00314AA0`, `00314AC0`, `00314A60`) fails a case.
- **Data.** `[02ADD100]` points at the **shipped `navimapdata.bin`** (`in` locale, 1,154 records, loaded verbatim;
  SHA-256 in `result.json`), or at 0 for the null-table case.

Every accessor of `03-World-Area-Field/CONTRACT-field-record-accessors.md` runs:
- `00377C20`, `00377480`, `00377A40`, `00377BA0`, `003779F0`, `00377700` and `00377C70`, plus the thunk `00320160`;
- for **all 1,154 field ids**, plus ids `count`, `count+1`, `0x7FFFFFFF`, −1 and −5, and a null table.

Each result is compared with a **direct decode of the file** per the contract's §2 table. **9 / 9 checks pass, identical
over three runs, with 0 mismatches.**

## What the execution adds to the contract

| item | observed |
|---|---|
| §2: the four fields of the `u16` (bits 0–11 with `0xFFF` = none; 12–13; 14; 15) and byte 2's inverted bit 0 | every accessor agrees with the decode on every record |
| §4.1: the null table is checked by all seven | null → 0, or −1 for `003779F0`, **except `00377700` (see below)** |
| §4.2: the id is bounded unsigned against `[table+4]` | `count`, `count+1`, `0x7FFFFFFF` and the negatives are rejected by the explicit-id accessors |
| **refinement 1: the implicit accessors never see a negative id** | `00377C20` / `00377BA0` / `00377700` / `00377C70` take the id through `003148F0`, which **clamps negatives to 0** (`cmovs` at `00314903`). A negative active id reads **field 0**, not the reject value |
| **refinement 2: `00377700` reads an absent record as 1** | its reject path zeroes the byte (`00377728 xor dl, dl`), and the inverted test (`not` / `test al, 1`) turns that into "bit clear" → **returns 1** for a null table or an out-of-range id. The save gate `[payload+0x1062]` bit 0 still forces 0 (case `byte2_bit0_save_gate`, all ids). The contract's §4.1 lists the null check without saying the resulting value is 1 here |
| data | `00377C70`'s byte-2 bits 4–7 are **0 in all 1,154 shipped records**; bits 12–13 take all four values (945 / 36 / 69 / 104) |

## Related

- S-11's `CONTRACT-field-environment-variant.md` has one entry, `0026D910`. That is the weather apply, which block 303
  executed stub-free over the shipped `map_ref.bin`; its lane-environment publications `02099DB0` / `02099DBC` are
  written there.
- `CONTRACT-authored-trigger-points.md` (`002F8060`, 648 B, eleven callees) is **not executed** by this note.
