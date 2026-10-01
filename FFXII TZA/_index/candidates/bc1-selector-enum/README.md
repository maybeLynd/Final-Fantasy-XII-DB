# BC-1 — the renderer selector is the port's blend-emulation class

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `bc1_selector.py` (6 checks, FAILS 0).

**Where the row stood.** BC-1 already had:
- `6` / `7` = `SRC_ALPHA` / `INV_SRC_ALPHA`;
- slot 15 read;
- the seventh argument, stored at renderer `+0x7C` and mirrored at `+0x208D4`, read only by five tests in `006C8CA0`
  that ask for "3 or 5".

It left open what the `{3, 5}` pair names, and so what the selector is. This record finds its other producer.

## The GS translator produces 0–5 (S1–S4)

**The table (S1).** `001EE650(alphaRegister, out, flag)` turns a PS2 GS ALPHA register into D3D11 blend state. It
indexes an 81-entry table at `00902750` by `27·A + 9·B + 3·C + D`. Those are the register's four fields: the equation
`(A − B)·C + D`, with A, B, D ∈ {Cs, Cd, 0} and C ∈ {As, Ad, FIX}. Each entry is `{selector, op, src, dest}`, and the
selector goes to `out + 0x1C`, the argument `0020FF10` passes through slot 15.

**What the selector values cover (S2).**

| selector | GS equations |
|---|---|
| 0 | 67, including standard alpha #10 `(Cs − Cd)·As + Cd` → `SRC_ALPHA` / `INV_SRC_ALPHA` |
| 1 | 8 |
| 2 | 3, the `(Cd − 0)·X + Cd` forms |
| **3** | **exactly one: #9, `(Cs − Cd)·As + Cs`** |
| 4 | 2: `(Cs − 0)·As + Cd` and `(Cs − 0)·As` |
| **5** | **none**: it is a substitution (S3) |

**5 is a substitution (S3).** When the flag argument is set, #10 (standard alpha) takes selector 5. For selector 3 or
5, `001EE650` then overrides the fixed-function factors to `ONE` / `ZERO`. Separately, it remaps every source-derived
factor to its dual-source form (`SRC1_*`).

**Where the flag comes from (S4).** The chain runs:
1. `0020FF10` reads the flag from byte `01F83560`.
2. `01F83560` has one writer, `002105B0`. The `GiVmax` replay `001DB3D0` calls it with the command's byte `+0x638`,
   and with 0 after the packets.
3. `+0x638` is `002105C0()`, which reads byte `01FD3698`, taken when the command is built (`001DB840`).
4. `01FD3698`'s only writer is `002105D0` (thunk `003A3D00`). The effect-element drawers call it with the element
   definition's byte `+0x74`, then with 0.

**So, for the GS side:**
- **3** is the one GS blend equation `(Cs − Cd)·As + Cs`.
- **5** is standard alpha drawn while an effect element whose definition byte `+0x74` is set is replaying.

These are the two cases the port does not leave to fixed-function blending. For both, `006C8CA0` binds the
resources at renderer `+0x1C0` / `+0x1D0` through `00623FA0` into slot `+0x160` (S6). Every other selector skips that
bind.

## DynGeo produces 0, 9 and 10 (S5)

The DynGeo text classes pass the selector as an immediate:
- 0 (`00213FE0`);
- 10, ShadowFinal (`002143E0`);
- 9, Shadow (`00214540`).

The selector's only reads are the five `{3, 5}` tests, so 9 and 10 take the general branch at all five sites — the
same path as every GS class except 3 and 5.

**The answer.** The `+0x7C` selector is one enum shared by two producers:
- the GS translator's blend-emulation class, 0–5;
- the DynGeo shadow classes, 9 and 10.

`{3, 5}` names the two GS blend cases emulated outside fixed-function blending.

## Not claimed

- **What the resources at `+0x1C0` / `+0x1D0` are.** A copy of the render target is the natural reading, not a
  measured one.
- **What the effect definition's byte `+0x74` is authored as.**
- **What selectors 1, 2 and 4 change downstream.** Only the `{3, 5}` tests read the selector, so 1, 2 and 4 affect
  only the blend factors their table entries carry.
