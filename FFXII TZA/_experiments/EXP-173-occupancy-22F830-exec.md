# EXP-173 — egrid occupancy query (22F830/22F8B0/381EB0) execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; no claim
of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **170/170, stable ×3**
(three independent processes).

## `22F830(ctx)` — 4-lane occupancy span driver

- Lane-enable nibble `b[ctx+0x16]`; loop ebx = 0..3.
- Per enabled lane: `r9 = q[ctx+8]` lane struct;
  `span-idx = lane * (w[lane+0x40]+1) + w[ctx+0x10]` (lane row-stride is
  cells+1);
  `w[ctx+0x12] = w[q[lane+0x20] + idx*2]` (start),
  `w[ctx+0x14] = w[..idx+1..] − start` (count) — a CSR-style boundary array;
  `call q[ctx]` (callback) with rcx = ctx.
- `231400` seeds: callback `22F8B0`, cell from `233050`, `b[+0x16] = 6`
  (lanes 1+2), `q[+0x18]` = probe, `d[+0x24] = 1` (filter on),
  `d[+0x20] = 0`; `found==0` → `ebx=1` accept.

## `22F8B0(ctx)` — lane span walker + entity filter

- Early-out when `d[ctx+0x20]` already set (first-hit semantics across lanes).
- Walks `w[ctx+0x12] .. +w[ctx+0x14]` entries of `q[lane+0x28]` id table.
- Id gate: `(id − 0x4000) ≤ 0xFFF` unsigned → ids `0x4000..0x4FFF` only.
- Entity record: `q[lane+0x18] + (id−0x4000)*0x90`.
- Filter (when `d[ctx+0x24]`): merges `d[ent+4]` through the same
  `0x209A2D0`-family mask table at base `0x209A3E0` with index
  `(d[ent+4]>>0xD&0x1F)+0x20` — `r8d = (B&A)|(~A&d[ent+4])` — and skips
  when merged **bit31** set.
- `call 0x381EB0(entity, q[ctx+0x18])`; nonzero → `d[ctx+0x20]=1`, break.

## `381EB0(entity, probe)` — local-space occupancy volume test

- `202B70` → `217060(out, entity+0x50, probe)` = **4×4 matrix × point**:
  `entity+0x50` is a 64-byte transform mapping the probe into entity-local
  space (out.w = row3·probe).
- `d[entity]` = volume kind:
  - **kind 1 = box**: all three local components must satisfy
    `f[0x1CEBC9B] < comp < f[0x1CEBBA7]` (runtime-initialized bounds;
    image defaults are degenerate denormals — never conflict).
  - **kind 2 = cylinder**: `|local.y| < f[0x1CEBBA8](=1.0)` then
    `sqrt(local.x² + local.z²) < 1.0` (const `f[0x1CEBC9C] = −1.0`
    lower bound). Radius/half-height both 1.0 in image.
  - kind 0 / other → ret 0.
- Conflict ⇒ caller sets the found flag ⇒ `231400` rejects the candidate.

## Executed cases

- `t22f830-empty`: lanemask 6 → `z22f8b0` ×2, zero volume tests, found 0.
- `t22f830-hit`: ids `{0x4000,0x4001}`, kind2 entities, identity matrices,
  probe `(0.3,0.5,0.3,1)` → `z217060` transform + `z381eb0` ×1 →
  `d[ctx+0x20]=1` (breaks on first conflict).
- `t22f830-nohit`: probe `(5,0.5,5)` → `sqrt(50)>1` → `z381eb0` ×2,
  found 0 (full span walk).
- `t22f830-filt`: `d[ent+4]=0x80000000` → merged bit31 → skipped before
  the volume test (`z381eb0` ×0), found 0.
- `t22f830-oob`: ids `{0x1234,0x5000}` → range gate skips both
  (`z381eb0` ×0), found 0.

## Combined picture (producer+consumer both executed)

`231400` accept = `233050` pos→cell → `233110` row select (`230A40` mask
query + `2324F0` triangle eval — EXP-172) → `22F830`/`22F8B0` occupancy
walk (`381EB0` local-space volume conflict — this EXP) → `found==0`.
Every layer of the egrid commit gate now has direct executed
positive+negative coverage.
