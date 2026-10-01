# UQ-218: selector kinds 0, `0xA` and `0xB`, the locomotion classifier (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md` (the selectors paragraph's
"Still open: kinds `0`, `0xA` and `0xB`")

This follows [`criteria.md`](criteria.md). A subagent read `004256E0` whole, and FABLE re-checked every load-bearing claim
against the image. [`classifier.py`](classifier.py) ([output](classifier.out)) runs B, F and R, FAILS 0, static. Three of
FABLE's working assumptions were wrong:
- `+0x254` is the **previous facing yaw**, not a target yaw. `heading-speed-to-position-delta.md` l.1193 records the
  save-then-store, so D is the last turn.
- The five packed constants are **FCP model-property ids** (`fcp-character-parameter-block.md` l.240), not motion-name hashes.
- The selector **never returns −1**: it always chooses.

**The classifier (B, R).**
- **Override:** band `0xE` when the render-pool slot's field (`003E7D10(rec+0x6A4, 4)`) is set.
- **Below the model's speed threshold** (`003E58B0`, compared with `+0x23C`):
  - band 0 when the last turn is 0 or inside ±C1, where C1 is 1.0 at 30 fps and 0.5 at 60 (`01DFE0BC`);
  - otherwise band 6, or 7 when the model allows it and the turn reaches the model's turn angle;
  - the offset bit is the turn's sign.
- **Between that threshold and `+0x420`:** the movement heading `+0x244` against the facing. Within ±45° gives 1, (45°, 135°]
  gives 3, [−135°, −45°) gives 4, else 5.
- **At or above `+0x420`:** band 2. When view query `0x1000` answers flag `0x20` (by the reading, when the actor is the
  party-focus actor) and a target record resolves, the target's bearing gives 2, `0xA`, 9 or `0xB` by the same windows.
- **Result:** `+0x2A0` keeps the band. Arguments 0 and 2 lower bands 9–`0xB` by one, and `0xE` becomes `0xB`, `0xC` or
  `0xD` by argument. The track offset is `1 − esi`.
- **The model check (F):** before a band is used, a model property read through `004FE2F0` (ids `0x63070F30`, `0x62070E30`,
  `0x61070D30`, `0x60070C30`, `0x63070B2D`) says whether the model has that motion. If not, the band falls back to a simpler
  one.

**Read but not pinned by a check.** This is the subagent's full reading; FABLE saw the matching instructions in its own dump.
- **Fallbacks by the property value q:**
  - bands 1 and 2 fall to 0 when q is 0 (committing the look controller's state first);
  - bands 3 and 4 fall to 0 or 1;
  - bands 5 and 7 fall to 0 or 1;
  - bands 9 and `0xA` fall to 0 or 2;
  - band `0xB` falls to 2;
  - band 6 also consults the `@FRM` header byte `+2`.
- **Dwell timers** (arguments 1 and 2): `+0x456` holds a new walk band for 3 × `frameLimit` calls before accepting it.
  `+0x457` counts time in the fast family; after 30 × `frameLimit` of it, band 0 becomes band 8.
- **Shipped model data:** 723 of the 1,066 `.cm` files carry the property section. Slot 48's bytes take 0–5, 0–2, 0–2 and 0–3.

**Inference only:** 0 = idle, 6/7 = turn in place, 1/3/4/5 = walk forward / side / side / back, 2 = run, 9/`0xA`/`0xB` =
facing a target, 8 = stopping from a run.

**Not claimed:** which yaw sign is left; what `+0x23C` measures (typed `animPhaseFloat`); the `003E7D10` field; the `@FRM`
header byte.

| consumer | action | agreement |
|---|---|---|
| handler page, the selectors paragraph's "Still open: kinds `0`, `0xA` and `0xB`, the locomotion classifier …; each band's meaning is not read" | replaced with the band geometry, the model check and the result; the inference labelled | revised-here |
| `criteria.md`, "Still open" (the classifier) | answered here | agrees |
| UQ-218 (SWE2-DATA's row) | the `@FMC` selector residue is now only the unlabelled band names and the three unread fields | routed-to-FABLE-REQ-FRONTIER-UQ218-HANDOFF-AND-REGISTER-CLAIM |

Regression: classifier.py B F R. R rejects "the selector can return −1". run: classifier.py at e10b71e70, FAILS 0.
