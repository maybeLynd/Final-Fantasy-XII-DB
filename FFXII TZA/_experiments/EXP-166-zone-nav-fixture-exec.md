---
id: EXP-166
title: "Zone-context fixture — 383F10 navmesh cell/link lookup + 391410 layer scan + 231400 entity-grid commit, all real"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 143/143 (stable x3)
---

# EXP-166 — zone/navigation context, executed

Closes the shared blocker found in EXP-164/EXP-165: the
navmesh/zone-context object at `q[0x2AEDFB0]` plus the layer-grid
globals at `0x2AEE060..0x2AEE0B9` and the entity-grid ctx pair at
`q[0x209A670]`/`q[0x209A678]`. With them planted, the full
scatter-validation pipeline runs **real end-to-end, including an
accepted spawn**.

## `383F10(pos={f x,f z})` — decoded + executed

Navmesh cell→link lookup:

- `rbx = 20E600(d[zctx+0x20])` — cell-group descriptor:
  `b[0..3]` = cell_w, cell_h, cols, rows; `w[+4]/w[+6]` = origin;
  `d[+8]` = cell-id table off; `d[+0xC]` = link-byte array off.
- `rdi = 20E600(d[rbx+0xC])` — per-cell link-id byte list base.
- `_fdclass(x)==2 || _fdclass(z)==2` → reject `0xFF` (NaN guard).
- Bounds: origin ≤ pos < origin + dims×cell — else `0xFF`.
- `idx = (z-z0)/cell_h * cols + (x-x0)/cell_w` →
  `cellid = w[celltab + idx*2]`; `0xFFFF` → reject.
- `b[rdi + cellid]` = link list head; `0xFF` → empty → `0xFF`.
- Per link byte `L`: sublink count `w[celltab2 + L*0x22 + 2]`
  (via `zctx+0x18`); for `i<count`: linkdesc idx =
  `w[celltab2 + (L*0x11+i)*2 + 0x14]`; desc =
  `20E600(d[zctx+0x10]) + idx*8`; `382D10(desc, pos)` — `eax==1`
  → **return `L`** (the link id). Exhaust → `0xFF`.

## `382D10(linkdesc, pos)` — decoded + executed

Point-in-convex-polygon (triangle) winding test over a static
vertex ring `{0,1,2,0}` at `0xD112B0`: verts indexed by
`w[linkdesc + ring[i]*2]` into `20E600(d[zctx+0xC])` (8-byte xy
pairs). Per edge: 2D cross of (pos−v0)×(v1−v0); all crosses must
share the first sign — `cross*acc < 0` → ret 0; else ret 1.

## `391410` / `3912E0` — layer occupancy pre-scan, executed

- Globals: `d[0x2AEE060]` row pitch, `d[0x2AEE064]` col bound,
  `f[0x2AEE06F]`/`f[0x2AEE077]` origin offsets,
  `f[0x2AEE08F]` cell-size divisor (zero → `cvttss2si` poison,
  **the first misdiagnosed fault**), `q[0x2AEE0A0]` cell data,
  `q[0x2AEE0A8]` occupancy grid, `q[0x2AEE0B0]` scratch bitmask
  (memset by `3912E0` to `d[0x2AEE0B8]`, stride `d[0x2AEE0B9]`),
  layer bitmask `b[tab+i] & (1<<i)` gates each layer scan.
- **`0x2AEE*` not `0x2AEB*`** — the fixture's first fault came
  from a hand-computed RIP-relative slip; all globals re-derived
  from raw bytes with tooling.

## `337700(rec, pos)` — full validator, executed

1. `265090(q[rec+0x10], &y0, &y1)` — **kind-3 only**
   (`b[obj+3]&0xE0==0x60`): `3DA710` writes y0/y1 from
   `q[obj+0xB8]+0x50`; any other kind → outs untouched
   (`0xCD` garbage → probe NaN → reject — proven).
2. `391410(pos)` occupancy scan → nonzero rejects.
3. `384130` → `383F10` → `0xFF` rejects.
4. `336390(pos, maxss(y0,y1), b[rec+0x1F4])` — 5-point footprint:
   centre + 4 corners at ±height; each calls `32A6A0` →
   `26E100` → `231400`; any zero → reject. `eax!=0` → accept.

## `26E100`→`231400` — entity-grid commit/query, executed

- `rcx = q[0x209A678]` iff `q[0x209A670] != 0` — runtime grid ctx.
- `233050(ctx, pos)` — pos→cell: int origin offs `d[ctx+0x38]`/
  `+0x3C`, `idiv` by `d[gdesc+0x10]`/`+0x14` (odd-col stagger via
  `test al,1` half-row shift), bounds `d[+8]`/`+0xC`, ret
  `col+row*cols` else `-1`.
- `233110(ctx, out, cell)` — row select: span
  `w[ridx+cell*2]..w[ridx+(cell+1)*2]` over `q[ctx+0x20]`,
  row idx `w[q[ctx+0x28]+i*2]` ≤ `0x3FFF`, `230A40` mask filter
  (shipped table `0x20942D0`), `2324F0` surface eval →
  `w[out+0x52]` = selected row.
- `231400` tail: `w[out+0x52]<0` → ret 0; else surface height
  solve (`q[ctx+0x10]` 0x20-stride rows → `q[ctx+8]` 16-byte
  sector planes; `f[row+4] ≤ const` skips), then inline
  `233050` + `22F830` span query w/ `0x22F8B0` callback →
  `d[q+0x20]` stayed 0 → **ret 1**.

## Proven

- `t2730-scat`: empty link list (`b[link]=0xFF`) → 9 real iters →
  `383F10` ×9, `382D10` ×0, `336390` ×0 → `312DF0` −2 → `eax=0`.
- `t2730-nozone`: no ctx → authentic fault `0x383F23`
  (`expect_fault`, disclosed).
- `t2730-accept`: pos (1,2) inside tri (0,0)-(8,0)-(0,8) →
  `382D10` ret 1 → link 0 → 5 probes all ret 1 → `336390` 1 →
  **`eax=1` — accepted spawn on iteration 1**.
- `t2730-outside`: pos outside tri → `382D10` ret 0 ×9 → all
  links exhausted → `eax=0`.
- `t1f70-aux`/`t1f70-mode1` (EXP-164 arms): now run the **entire
  24-node transform chain** real — `m_cosf`/`m_sinf`/`m_sqrtf` ×24,
  `z383f10` ×48, `e600` ×96+; `q[rec]|=0x4000000`,
  `d[rec+0x15C]` = `0x3FC912DC` (≈π/2 — a computed angle).
- All 140 prior cases re-proven — 143/143 across three processes.

## Fixture disclosures (planted)

- `zonectx`: `q[0x2AEDFB0]` ctx `{+0xC verts, +0x10 linkdescs,
  +0x18 celltab, +0x20 grpdesc}` — all `20E600` (elemb+off)
  resolved; grid `0x2AEE060..0xB9`; `_fdclass` IAT cell
  `0x8C2C10` → stub ret 8 (NN); `rand` cell `0x8C3098` → stub
  ret `case.randv`.
- `egrid`: `q[0x209A670]` gate + `q[0x209A678]` ctx
  `{+0 gdesc{+8 cols,+0xC rows,+0x10/0x14 cellwh}, +8 sectab,
  +0x10 rowtab, +0x20 ridx, +0x28 rows, +0x38/0x3C origin}`.
- `MATH` hooks host-compute `cosf`/`sinf`/`sqrtf`/`tanf`/
  `atan2f`/`asinf`/`acosf` at thunks `0x861F02..0x861F22` —
  **not bit-exact vs shipped CRT** (disclosed); `_fdclass` and
  `rand` are deterministic stubs.
- `zverts`/`zldescw`/`zlink`/`erow` shape the link triangle and
  row span. Static ring `0xD112B0` and mask table `0x20942D0`
  are shipped data read real.

NATIVE-REPLAY only — planted ctx is a disclosed fixture; no
initialized-gameplay reachability claimed.
