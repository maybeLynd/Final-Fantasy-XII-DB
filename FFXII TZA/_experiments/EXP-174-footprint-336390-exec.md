# EXP-174 — footprint probe 336390 execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; no claim
of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **172/172, stable ×3**
(three independent processes).

## `336390(pos, ?, kind, xmm1=halfwidth)` — 5-point footprint gate

- `rcx` = 16-byte position quad `{f x, f y, f z, f w}`; `r8w` = kind
  (forwarded via `edx`); `xmm1` = half-extent; `r8d=0` on every call.
- Probe sequence (each `call 0x32A6A0`, any ret 0 → eax=0):
  1. **center** — the quad as given.
  2. corner `x+h, z+h`
  3. corner `x+h, z−h`
  4. corner `x−h, z+h`
  5. corner `x−h, z−h`
- All five pass → `eax = 1`. `y`/`w` lanes are copied unchanged to each
  corner (2D footprint only).
- Stack cookie (`808c40`) real.

## Plumbing (both sides inspected + executed)

- `32A6A0` = `jmp 0x26E100` trampoline.
- `26E100(pos, kind_w, r8)`: gate `q[0x209A670]`, ctx
  `q[0x209A678]` → `jmp 0x231400(ctx, pos, movzx kind, r8)`.
- `231400` per probe = full egrid commit: `233050` pos→cell →
  `233110` row select (`230A40` mask query → `2324F0` triangle eval) →
  `22F830` occupancy walk. This is the same path `t2730-accept` and the
  EXP-172/173 direct cases exercise — now driven per-corner.

## Executed cases

- `t336390-all`: pos `(1,1,1)`, halfwidth `0.5`, degenerate
  (all-zero-sector) row → all 5 probes usable → `eax=1`,
  `z32a6a0`/`z231400` ×5.
- `t336390-edge`: real CW triangle `(0,0)-(0,4)-(4,0)` via `erowverts`/
  `esec`, pos `(2,1,2)`, halfwidth `1.0` → center passes; corner
  `(3,3)` violates edge `v1→v2` (`normal.y = −1.414 < −1e-4`) → probe 2
  rejects → `eax=0`, `z32a6a0`/`z2324f0` ×2. Proves the corner actually
  consults the triangle geometry — the first executed
  *geometric* rejection in the footprint path.

## Why it matters

`336390` is the final accept gate inside `337700` (spawn-candidate
validator): a candidate is usable only when the whole 2×halfwidth square
footprint clears the egrid. The corner arithmetic, fail-fast ordering,
and kind/position plumbing are now execution-proven, closing the last
undecoded layer of the `26E350`/`312DF0` position-validation family.
