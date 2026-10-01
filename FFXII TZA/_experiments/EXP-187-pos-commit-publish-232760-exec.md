# EXP-187 — 232760 position-commit publish + wall-slide — EXEC

Harness: `Temp\exp166_check.py` — 3 new cases, **252/252, stable ×3**.
The `232760` commit-publish chain now executes fully natively:
containing-tri scan → region transforms → recursive wall-slide →
pending rebase. All helpers real (pure math, no scripted boundary).

## Executed discoveries

### `232760(ctx, out, cell, pos)`
- `233110(ctx, out, cell, pos)` — containing-tri scan → `w[out+0x52]`.
- `22EF20(out)` — rebuild world↔region transforms (below).
- Publish: `d[0x20891E0] = 0` then, if `w[out+0x52] >= 0`:
  `d[0x2088FE0] = tri`, `d[0x20891E0] = 1`. **`d[0x2088FE0]` is a
  visited-triangle LIST** (cap 0x80), `d[0x20891E0]` its count — the
  publish seeds it with the containing tri.
- `d[0x20891E4] = 0` — clears the pending-point list.
- `22F9B0(ctx, out, out, tri)` — wall-slide flood (r9w = tri still in
  register from the publish load).
- Tail `jmp 22F250(out)` — pending-point rebase.
- **Return value is a dead stack-cookie xor** — the function is
  effectively void; callers ignore eax (verified: `22F250` returns
  the `cookie^rsp` value, not a count).

### `22EF20(out)` — region transform rebuild
- `d[0x2089270] = 1`, `d[0x2089274] = 1` — dirty flags.
- `380A60(out, 0x2089280)` — yaw-basis: row0 = `{-f[out+0x10], 0,
  f[out+0x18], 0}`, up row const `{0,1,0,1}` (0xD22740), row2 =
  `202E10` cross normalized; writes region A.
- `q[0x20892B0] = 0`, `d[0x20892B8] = 0`.
- `202D50(0x20892C0, 0x2089280)` = `217610` — **4×4 inverse** →
  region B (region→world).
- Two 4×4 identity matrices via `203170` (const `0x8C5F80..0x8C5FD0`);
  `max(f[out+0x80], 0.01)` / `max(f[out+0x84], 0.01)` (clamp const
  `f[0x8F30E4]` = 0.01) → scale diag; reciprocals → inv-scale.
- `202D70(A, A, scale)` = `217150` — A = basis × S; B = A⁻¹ × S⁻¹.
- **`f[out+0x80]/+0x84` = the query bbox extents** (region scale).

### `22F9B0(ctx, out, point, tri)` — recursive wall-slide flood
- First loop (3 iters): `w[cellrec+0x10+i*2]` vert ids →
  `q[ctx+8]+id*0x10` verts → `202B70` transform into region space.
- Per edge i (next-vert via `0x908DE8` dword table {1,2,0,1}):
  - `nbr = w[cellrec+0x16+i*2]`; `nbr >= 0` → `230A40(ctx, nbr,
    w[out+0x50])`; unusable → treated as -1 (wall).
  - `202B70` transforms `f[point]` (the query position) once per edge.
  - `t = clamp(dot(P - v_i, ê)/|e|, 0, 1)` → closest point c;
    `d = P - c`; `len = |d|`; **`len >= 1.0` → skip** (K = 1.0f).
  - `rdi` = vertex ptr when the closest point clamps to a vertex,
    else 0.
- **Wall edge (nbr<0)**: `rdi != 0` → queue `q[0x20891F0+cnt*8] = rdi`,
  `d[0x20891E4]++` (cap 0x10) — pending rebase; `rdi == 0` →
  **direct push**: world-space delta = `(len-1)/len` along the
  back-transformed normal → `f[point] += push`, `f[out+0x40..0x48] +=
  push`, `d[out+0x60] |= 0x10`. count = 1.
- **Portal edge (nbr≥0, usable)**: dedup against `d[0x2088FE0..]`
  (count `d[0x20891E0]`, cap 0x80); new → append, `d[0x20891E0]++`,
  **recurse** `22F9B0(ctx, out, point, nbr)`.
- Returns `d[rsp+0x20]` = processed-edge count (0/1 arms).

### `22F250(out)` — pending-point rebase
- `d[0x20891E4] <= 0` → early ret (cookie-xor return).
- Per pending ptr `q[0x20891F0+i*8]`: `d3 = f[out] - f[p]` →
  region-space via `202B70`/`0x20892C0`; `len > 1.0` → pull
  `n*(1-len)` back-transformed via `202B90`/`0x2089280` →
  `f[out] += pull` — enforces the ≤1.0 region constraint against
  queued vertex points.

## Cases (all value-verified)

| case | setup | observed |
|---|---|---|
| t232760-idle | (10,0,10) inside 40-tri, walls only | visits=1, pos unchanged, flags 0 |
| t232760-push | (0.5,0,10), 0.5 from wall edge x=0 | **pushed x→1.0**, accum +0.5, flags \|=0x10 |
| t232760-portal | nbr[0]=1 shares edge v0v1 | visits={0,1}, recursion ×2, no push on portal |
| t232760-pend | portal into tri1; P projects past shared vertex v0 on tri1's wall edge | **pending ptr queued**: `d[0x20891E4]=1`, `q[0x20891F0]=sectab` (v0 slot), no direct-push flag |

The push magnitude lands exactly at region-dist 1.0 — the wall
constraint is hard (point placed ON the 1.0 boundary).

### Pending-pointer arm (t232760-pend)

- Per edge: `t = dot(P-v_i, ê)`; `t<0` clamps to `v_i`, `t>len` clamps
  to `v_next` — the closest point is a **vertex** → `rdi = vert slot`.
- If that vertex-clamped distance is still `<1.0`, the vertex pointer
  is queued at `q[0x20891F0 + d[0x20891E4]*8]` (cap 0x10) and
  `d[0x20891E4]++` — deferred handling instead of a direct push.
- Fixture detail that mattered: tri0's own wall edge pushed P to
  x=1.0 *before* the portal recursion, moving it >1.0 from the vertex.
  Fix: `nbr[0]=0` (self-neighbor) — dedup skips it as already-visited,
  no push; P then vertex-clamps on tri1's e2 within 0.707 → queued.

## Boundary disclosure

- `861F14` sqrtf = scripted host-libm MATH stub (disclosed; not
  bit-exact vs shipped CRT).
- `22F250`'s >1.0 pull arm exercised only at count-0 (pending arm
  now covered at enqueue; a pull-positive case needs a pre-seeded
  pending list — fixture boundary noted).
- Entity-lane `22F8B0` occupancy inside `231400` remains
  empty-span-only (EXP-173 fixture covers nonzero separately).

## Stability

`python exp166_check.py` → **253/253** in three separate processes.
