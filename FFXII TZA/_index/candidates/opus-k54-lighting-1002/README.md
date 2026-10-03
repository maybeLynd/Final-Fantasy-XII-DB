# What the five kind-0x54 lighting routines write into the lit per-normal table (OPUS, 2026-10-02)

The residue on [`effect-mesh-records-kind-54.md`](../../../17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md)
reads: "What stays open is what the lighting routines write into the per-normal table (`003962F0` / `00396A30` /
`00396560` / `00395CF0` / `00395780`), which decides what the regenerated UVs mean." This record answers it by
execution. The page leads to SWE2-DATA; the suggested text is routed to it (OPUS edits nothing on the page).

## The answer

The five routines are PS2 VU0 microcode translated to x86:
- The globals from `022D8F10` on are the emulated register file.
- vf00 = (0, 0, 0, 1) at `01EF93F0`, loaded by `0036DD80`.

Each routine takes the mesh's normal list (16 bytes per normal), an output table and a count. Every one first forms
m = M·n, where M is the three matrix columns the caller loads into `022D91B0` / `91C0` / `91D0`, each four lanes wide.
It then writes one 16-byte entry per normal.

The draw path's pass byte `param + 0x1B0 + p` picks the routine (`004355D0` + 0x415). For modes 1, 3 and 4, a second
byte, `param + 0x1B4 + p`, picks the axis.

| mode | routine | entry L[n] (lanes 0..2) | lane 3 |
|---|---|---|---|
| 1, `+0x1B4` = 0 | `00395CF0` | reflection sphere map about y: 0.5 + 0.5 · unit(r.x, r.z, r.y + 1) | (M·n).w |
| 1, `+0x1B4` ≠ 0 | `00395780` | reflection sphere map about z: 0.5 + 0.5 · unit(r.x, −r.y, r.z + 1) | (M·n).w |
| 2 | `003962F0` | planar: (−s · m.x, s · m.y, 0) with s the float at `param + 0x1D8 + 4k` | (M·n).w |
| 3 or 4, `+0x1B4` = 0 | `00396A30` | normal sphere map ("matcap") about y: 0.5 + 0.5 · unit(m.x, m.z, m.y + 1) | carried |
| 3 or 4, `+0x1B4` ≠ 0 | `00396560` | normal sphere map about z: 0.5 + 0.5 · unit(m.x, −m.y, m.z + 1) | carried |

- **The reflection vector.** r = 2(m·V)m − V, where V is (0, 0, 1, 0) (`008C5FB0`) transformed by `00394DA0`
  through `02AEEAA0`.
- **The matrices.** Modes 1 and 3 build M from `02AEEA20`; modes 2 and 4 from `02AEEBF0`. Both are the matrices
  `0024C060` writes (register row BI-9).
- **Normalisation.** unit() divides by `sqrtf` of the squared length. A zero vector divides by FLT_MAX instead and
  lands on the centre (0.5, 0.5, 0.5).
- **"carried".** Lane 3 is whatever the register at `022D9310` already held: the routine never writes it.
- **The planar mode's lane 2.** It is the sign-extension bits of s, 0.0 for every positive s.
- **Mode 0 and modes above 4** build no lit table.

**What this decides.** The pass operator `00396F20` copies L[n]'s first two floats over the UV, so the regenerated UVs
mean the following:
- **Modes 1, 3 and 4:** sphere-map (environment) coordinates, already in [0, 1] around 0.5:
  - modes 3 and 4 map the view-rotated normal itself (a matcap);
  - mode 1 maps the view reflection, the classic sphere map with v flipped for the z axis.
- **Mode 2:** a planar projection of the rotated normal, scaled by ±s. Its screen term `00394B70` and the offset /
  scale operators then place it.
- **Lane 3 and alpha.** `00432CC0` reads lane 3 for alpha. For modes 1 and 2 it is the normal dotted with the matrix's
  fourth lane, (M·n).w.

## Evidence

[`k54_light.py`](k54_light.py) runs each routine to its own `ret` over the certified image (FABLE's SD-140 Unicorn
harness, imported). The only bridge is the CRT import `sqrtf` (IAT `008C2BB8`), computed in float32.
- **E-checks:** 600 random normal / matrix / V / s rows per routine, 0 off the model; lane 3 checked on 1,200 rows.
- **N-checks:** four deliberately wrong models are each rejected on 600 / 600 rows:
  - the planar sign;
  - the axis swap;
  - the v flip;
  - reflecting the raw normal instead of M·n.
- **A-checks:** nine selector sites in `004355D0`.
- **K-check:** the V constant.
- Result: FAILS 0 ([`k54_light.out`](k54_light.out)).

## Limits

- **Static and conditional.** Which pass modes and matrices shipped effects use, and what `02AEEA20` / `02AEEAA0` /
  `02AEEBF0` hold at draw time, is not executed here. BI-9 records `02AEEA20` as the identity at the title screen.
- **The other draw paths.** Only `004355D0`'s selector is anchored. `00437130`, `00438860`, `004434D0` and `00444340`
  call the same five routines; their selectors were not read.
- **The planar index.** The planar scalar's index k comes from `rbx`, which is not shown to equal the pass index (the
  other selector sites index with `rdi` / `[rsp+0x70]`).
