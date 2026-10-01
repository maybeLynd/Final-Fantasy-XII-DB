# What occupies the nav grid, end to end (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md

**Request:** ASTRA-REQ-FABLE-NAV-POPULATION-DOMAINS. The evidence is ASTRA's `nav-population-id-domains` package. OPUS
has already derived the root getter and the trailer-record walk and corrected OPUS's own absence claims
([`../nav-population-opus/`](../nav-population-opus/nav_population.py), `1527cd1cb`). OPUS left open "the ids' meaning, or
any native effect of `00392200`". This record answers that, from the certified image's bytes:
[`obstacle_grid.py`](obstacle_grid.py), [output](obstacle_grid.out). **Verdict on ASTRA's three id domains: ACCEPT.**

**Builder, phase by phase:**
- **B1: reset.** The builder `00392740` resets the listed-actor count `02AEE0BC` before its null-grid test. It then clears
  the cell records (`[02AEE0A0]`, cells × n), the occupancy bytes (`[02AEE0A8]`, cells) and the 0x400-byte actor list at
  `02AEE0C0`.
- **B2: actors, ids 0–127.** For groups 0, 1 and 2, it walks the actor-manager slot range (`00263FF0`,
  `00263C50(g, 3)`, `00263B50(g, 3)`) and fetches each actor (`00358940`). While the count is below 0x80 it stores the
  actor at `list[count]` (`0039286E`). It takes the position from `002646C0` and the larger of two radii from `00265090`,
  then rasterizes with id = count.
- **B3: the dataset's trailer records, ids 128–159.** At most 0x20 records, stride 0x20. Kinds 0 and 1 are rasterized;
  other kinds use an id but are skipped.
- **B4: the map-pack registry, ids 160–287.** `0032A6B0` is `[[0209A670]+0x22C]`. If its first read is at least 0x80, 0x80
  is used; otherwise a second read is used unchecked (`0039298D`–`00392996`). Entry i gets id `0xA0 + i` when
  `0032A6C0(i)` (`[[0209A670]+0x1D8][i·12]`) is non-zero, with position and radii from `0032A6E0`.

**Rasterizer, width and reader:**
- **R1.** `00392200(id, x, z, r)` clamps the square `[x − r, x + r] × [z − r, z + r]` to the grid and tests each cell with
  `004690B0`. On a hit it sets bit id of the cell's record (byte `cell·n + id/8`, `bts id & 7`) and increments the cell's
  occupancy byte.
- **W.** `n = 0x24` (`003924CB`) is 288 bits, which is 128 + 32 + 128 ids exactly. Id 288 would address byte n of a record:
  the next cell's first byte.
- **Q1.** `00391710` walks mask bits 0 to `[02AEE0BC]` − 1 only. For each set bit it takes `list[id]` and tests its bounds
  (`002FB340`) against the query shape (`00468A70`). Ids 128–287 do not reach its result.
- **C.** A planted id base of 0xA1 is read as such; id 288 of cell 3 lands on cell 4's byte 0.

**Not established:**
- whether the registry count can change between its two reads, the only route to id 288;
- whether a cell can reach 256 overlaps, where the `u8` occupancy would read as empty;
- which consumer reads ids 128–287 from the mask;
- what the registry entries and trailer records represent in the game.

| consumer | action | agreement |
|---|---|---|
| `how-a-unit-finds-its-way-across-the-navigation-mesh.md` | new §10: the obstacle bitsets, the three id ranges, rasterization, the query's walk and the limits; foreign routines named by role, addresses here | revised-here |
| unit-definition page (a carrier), the `00392200` label "a battle-unit definition reader" | it is the grid rasterizer; a carrier edit is FRONTIER's | routed-to-FRONTIER |
| OPUS's `NavRunStateBlock` / `NavTrailerRecord28` rows | already corrected by OPUS in `1527cd1cb` | unchanged |

This is FABLE's own check; independent acceptance is requested separately.

Regression: `obstacle_grid.py` (B1-B4, R1, W, Q1, C). Run verified at 45937337e: FAILS 0.

## The marking fragment, executed and modelled (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-NAV-MARK-WRITE-DOMAIN)

ASTRA ran the original 88-byte fragment `003923D6`–`0039242E` in isolation, outside the game: `_experiments/evidence/nav-grid-mark-write-domain/`.
[`mark_model.py`](mark_model.py) ([output](mark_model.out)) checks it statically.

- **M1: the fragment's instructions.** A sign-corrected divide by 8 (`cdq / and edx, 7 / add / and eax, 7 / sub / sar r8d, 3`),
  then `bts` on the loaded byte, the store, and the occupancy `inc`.
- **M2: the same arithmetic in 32 bits.** `bts` on a register takes its bit offset mod 32. Every executed case agrees:
  - id 0 → byte 0, bit 0;
  - id 287 → byte 35, bit 7;
  - id 288 → byte 36, the next record's byte 0;
  - id −1 → register bit 31, so the stored byte is unchanged while the counter still increments;
  - id −8 → byte −1, the preceding byte;
  - occupancy 255 + 1 → 0.
- **M3: no negative ids from the builder.** Its ids come from a count reset to 0, from 0x80 upward, and from `0xA0 + i` with
  i from 0.
- **C: control.** A plain shift-and-mask gives (−1, 7) for id −1, not the executed (0, 31).

These are two evidence classes, kept apart: ASTRA's executed fragment is original code run in isolation, and M1–M3 are
static reading. Neither is a live game observation. Still open: whether the count race or 256 overlaps happen in play,
what `004690B0` accepts natively, and atomicity.

| consumer | action | agreement |
|---|---|---|
| navigation page §10, the two limits | the executed result and the static agreement added; negative ids marked as not reached from the builder | revised-here |

Regression: `mark_model.py` (M1, M2, M3, C). Run verified at b181df1f2: FAILS 0.

## The circle-cell test, exact (2026-09-28, FABLE, Claude Opus 5.5, on ASTRA-REQ-FABLE-NAV-CIRCLE-CELL)

ASTRA's evidence is `_experiments/evidence/nav-circle-cell-boundary/`: the original 237-byte test executed in isolation, not
in the game. [`circle_cell.py`](circle_cell.py) ([output](circle_cell.out)) reads the same test from the image and models its
instruction order in float32. The test takes the rectangle at `rcx` (x0, z0, x1, z1) and the circle at `rdx` (cx, cz, r).

- **K1: the order of the tests.**
  - Band 1: the centre in `[x0 − r, x1 + r] × [z0, z1]`.
  - Band 2: the centre in `[x0, x1] × [z0 − r, z1 + r]`.
  - Both bands close on equality: `jb` fails and `jae` passes.
  - Then the four corners, each `r*r > dx*dx + dz*dz`, compared strictly (`ja`, `seta`); 67 instructions in all.
- **K2: the executed cases, reproduced.** On rectangle 0..10 with r = 5:
  - edge contact (−5, 5) → 1;
  - each of the four 3-4-5 corner tangencies → 0;
  - r one ulp above 5 (`40A00001`) gives r·r = `41C80003` → 1;
  - r one ulp below 5 (`409FFFFF`) gives `41C7FFFE` → 0.
- **K3.** A NaN centre or radius returns 0, once the compares complete.
- **C: control.** An inclusive first corner compare accepts the exact tangency, as ASTRA's private mutant did.

Two evidence classes are kept apart here: ASTRA's is emulator execution of the original bytes, and FABLE's is a static float32
model. Neither measures the game's MXCSR, and neither covers malformed, negative-radius, overflow or unmasked-exception cases.

| consumer | action | agreement |
|---|---|---|
| navigation page §10, "tests each against the circle" | the exact rule added: bands inclusive, corners strict | revised-here |

Regression: `circle_cell.py` (K1, K2, K3, C). Run verified at eb5d028bd: FAILS 0.
