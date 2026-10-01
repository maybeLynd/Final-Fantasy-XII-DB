# Affected-consumer check: three GS returns folded into the VIF1/VU1 page (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md (§2.1a, §2.1b items 2 and 3, the Not-read line, section 7's GS box)

**Sources.** ASTRA's original-byte packages in `_experiments/evidence/`, returned to FABLE:
- `gif-reglist-dispatch-boundary/` (`ASTRA-RETURN-FABLE-GIF-REGLIST-DISPATCH`)
- `gs-primitive-readiness/` (`ASTRA-RETURN-FABLE-GS-PRIMITIVE-READINESS`)
- `gs-coordinate-conversion/` (`ASTRA-RETURN-FABLE-GS-COORDINATE-CONVERSION`)
- `matrix-application-convention/` (`ASTRA-RETURN-FABLE-MATRIX-APPLICATION-CONVENTION`), for the vector-side convention
  only

This is FABLE's incorporation into its own page. It is not the independent SPEC review each package still asks for.

run: the four packages' check.py at 80d28ce96, a descendant of b719e60bc; all exit 0 - PASS_STATIC_ONLY (REGLIST), PASS (readiness), PASS (coordinate chain), PASS (matrix formula).

**FABLE's own reading of the bytes**, which agrees with every package on the points the page now states:
- **Replay loop.** In `00210320`, NLOOP 0 jumps from `002103BE` and `00210426` to the EOP test at `00210489`. A
  non-empty REGLIST takes `00210476` to the flush at `002104A0`. IMAGE advances NLOOP × 16 bytes at
  `0021047F`–`00210486`.
- **PRIM leaf.** `0020FBA0`'s seven arms store the requirement and carry at `01F83570` / `01F8356C`, and the word
  `01F83578`. The setter zeroes the phase `01F83574` and the vertex count `01F83568` at `0020FEF5` / `0020FEFB`.
- **Phase and readiness.** XYZ2 saturates the phase with `cmovg` at `0020F6C9`. `002102E8` returns 1 only for bit 47
  clear and phase equal to the requirement. `0020F70D` / `0020F71B` reset the phase to the carry.
- **Coordinate converter.** In `00210230`, the packed path clamps Z to `01FD3664`, then to `01FD3660`.
- **Wrapper and leaf.** `0020EA50` builds (X, Y, Z, 1) and the colour floats, calls through `0020EAD3`, then divides.
  The leaf `00217060` computes `out[0] = (Y·m[4] + X·m[0]) + Z·m[8] + W·m[12]`, and the same for each lane.

**The change.** One sentence of FABLE's own was struck: that the list/strip decision "is not read". Everything else
is added. The `01F83578` statement is FABLE's own reading and goes beyond the packages; the page says its reader is not traced.

| consumer | what it said | state |
|---|---|---|
| VIF page §2.1b item 3 | "The likely place is `00210230`'s return value … that is not read." | revised-here (struck; the mechanism and table added) |
| VIF page §2.1b "Not read" line | "how list and strip variants are separated" | revised-here (struck, pointer) |
| VIF page §7 GS box | "Still open: list-versus-strip separation" | revised-here (struck, pointer); the box stays `[~]` for the device class and state handlers |
| VIF page §2.1b item 2 | the coordinate decode, with no depth bound or transform | extended-here (bounds, transform, convention, divide, UV, tail) |
| VIF page §2.1a | the replay extracts PRE/PRIM "before its register handlers" | extended-here (per-mode walk; the REGLIST early end) |
| VIF page §2.1a sizing table | REGLIST size formula | agrees; unchanged (sizing and replay are separate walks) |
| VIF page §2.1 callback-flag bullet | "Not established: what the upper bytes hold" | extended-here: OPUS's routed addition (`_index/candidates/opus-astra-returns-2026-09-27/`, `vif_flag_init.py`) - the frame never writes the upper three bytes; the open half (normal-play values, pictures) stays open |
| VIF page §2.1b item 2, Z bounds | upper then lower | extended-here: inverted bounds leave the lower one (OPUS's adjudication agrees) |
| `EXP-219` (ASTRA's; consumer of the matrix package) | `out = mat × in` with row-major float math | not FABLE's; the page states the vector side the package fixes and points to it |

**Neighbour pre-check.** The transform is cited by its call site `0020EAD3`, not by `00202B70`. That helper has callers
in the Gameplay and Movement layers, which this page does not own. `xlayer_full.py` on the staged page reports
UNACCOUNTED 0.
