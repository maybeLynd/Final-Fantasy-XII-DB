# EXP-186 — 231400 position-commit query (233110 egrid commit) — EXEC

Harness: `Temp\exp166_check.py` — 5 new cases, **249/249, stable ×3**.
The `233110` "egrid commit" chain is now executed end-to-end natively:
pos→cell, containing-triangle scan, plane-height solve, occupancy walk.

## Executed discoveries

### `233110(ctx, out, cell=r8w, pos=r9)` — containing-triangle scan
- `w[out+0x52] = 0xFFFF` init ("no containing triangle").
- Null guards: `ctx==0` or `q[ctx]==0` → early ret (w+0x52 stays -1).
- Span: `start = w[q[ctx+0x20]+cell*2]`, `end = w[q[ctx+0x20]+(cell+1)*2]`,
  `span = end-start`; span==0 → early ret.
- Loop `i ∈ [0,span)`: `tri = w[q[ctx+0x28]+(start+i)*2]`;
  `tri > 0x3FFF` → skip; `230A40(ctx, tri, w[out+0x50])==0` → skip;
  `2324F0(ctx, tri, &scratch)` with `q[scratch+8]=pos` — ret<0 means the
  point is INSIDE the triangle → `w[out+0x52]=tri`, break.
- `w[out+0x50]` = the kind/mask word the caller plants (`231400` stores
  its r8w there) → forwarded as `230A40`'s kind arg.
- No hidden stack args — clean 4-arg signature.

### `231400(ctx, pos, kind=r8w, mode=r9d)` — position-commit query
- `cell = 233050(ctx, pos)`; `233110(ctx, &out, cell, pos)`.
- `blk = w[out+0x52]`; `blk<0` → ret 0 (no containing triangle).
- **Plane-height solve**: cellrec = `q[ctx+0x10]+blk*0x20` carries a
  plane equation: `f[+0]/f[+4]/f[+8]` = normal (nx,ny,nz);
  `w[+0x10]` = vertex-0 index → v0 = `q[ctx+8]+idx*0x10`.
  If `ny > f[0x8C5B2C]` (≈0.001 walkable-slope gate):
  `y = (nx*(v0x-px) + nz*(v0z-pz))/ny + v0y`.
- **mode==0**: probe quad y = solved y (snap to plane).
  **mode!=0**: probe keeps pos.y; `y > pos.y` → ret 0 (below plane).
- **Inline cell re-derive** (233050's staggered math re-implemented,
  remainder form): `col = trunc(gox+px)/cellw`; odd col →
  `zint -= (cellh - zint%cellh)/2`; `row = zint/cellh`;
  bounds vs `d[gdesc+8]/d[gdesc+0xC]` → `cell2 = cols*row+col`
  (−1 on bounds fail) → `w[ctx+0x10]` of the occupancy ctx.
- **Occupancy walk**: inline 22F830 ctx `{cb dword=0x22F8B0,
  q+8=ectx(lane struct), w+0x10=cell2, b+0x16=6 (lanes 1,2),
  q+0x18=probe quad, d+0x20=found, d+0x24=1}`.
  Quirk: the callback is stored as a **32-bit dword** (relies on the
  upper dword being zero — holds in practice, verified live).
- `22F830` lane indexing: `idx = lane*(w[lane+0x40]+1) + cell` →
  span `[w[ridx+idx*2], w[ridx+(idx+1)*2])` → `w[ctx+0x12]=start`,
  `w[ctx+0x14]=len` → cb per lane.
- `22F8B0` entity-id space: ids in `[0x4000, 0x4FFF]` (id−0x4000 ≤
  0xFFF) → entity rec `q[lane+0x18]+(id−0x4000)*0x90`. Span len uses a
  **signed** word compare — negative spans exit cleanly.
- Return `ebx = (d[ctx+0x20]==0)` → **1 = position committable**.

### `231890(ctx, pos, cell)` — standalone plane-height evaluator
- Same formula as 231400's inline solve: `r8w<0` or `ny ≤ const` →
  returns pos.y; else plane y. (Disassembled; direct case not added —
  identical math already covered via 231400.)

## Cases (all value-verified)

| case | pos / mode | expected | observed |
|---|---|---|---|
| t231400-in | (1,2,1) mode0 | ret 1, probe y=0.0 ×2 | pass |
| t231400-elev | v0y=5, mode0 | ret 1, probe y=5.0 ×2 | pass |
| t231400-out | (3.9,0,0.5) outside | ret 0, no occupancy | pass |
| t231400-m1hi | y=5 > pos.y=4, mode1 | ret 0 (reject) | pass |
| t231400-m1lo | y=5 < pos.y=6, mode1 | ret 1, probe y=6.0 (unsnapped) | pass |

Probe-Y capture: `on_code` records `f[q[rdi+0x18]+4]` at each `22F8B0`
entry when `probecap` — proves the mode0 snap writes the solved height
into the occupancy probe, and mode1 leaves the original pos.y.

## Boundary disclosure

- Occupancy spans reuse the `ridx`/`rows` arrays (entity lanes share
  the egrid ctx in this fixture): lanes 1,2 produce len −1/0 → empty.
  Nonzero `22F8B0` entity-conflict coverage remains in EXP-173's
  dedicated `f830` fixture cases.
- `231890` disassembled only (same formula as the inline solve).
- `232760` (233110 wrapper: blocker-cell record + notify chain via
  `22EF20`/`22F9B0`/`22F250` → globals `0x2088FE0/0x20891E0/0x20891E4`)
  disassembled; not yet a case.

## Stability

`python exp166_check.py` → **249/249** in three separate processes.
