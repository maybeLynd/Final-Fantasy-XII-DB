# EXP-172 — egrid row-usability semantics (230A40 + 2324F0) execution-validated

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). Fixture boundaries disclosed; no claim
of initialized-gameplay reachability.

Harness: `Temp\exp166_check.py` — **165/165, stable ×3**
(three independent processes).

## Harness bugs found and fixed (the round's biggest result)

- **Dead assert chain**: `main()`'s dispatch `elif` only matched
  `v8bf0-/t1f70-/t2700-`; every `t2730-*`/`t26e350` name fell through to the
  generic no-fault check, so all name-specific asserts written since EXP-165
  were dead code. Added `t2` prefix → dormant asserts now execute — and the
  entire EXP-165–171 backlog **passes for real** (trace counts, return
  values, output quads), retroactively enforcing those claims.
- **`epos` fixture nested inside `ownerres`**: `t26e350` never received its
  position pointer (`rcx` stayed `w.rec`). Hoisted top-level; the snap-write
  assert `d[epos+4]==0` now exercises the real buffer.
- **`t312730` entry-block tag doesn't record** (same quirk as `26E350`):
  three asserts switched to downstream tags (`t312df0`/`t3dfd00`/`t31b7e0`),
  which only exist on the real path anyway.

## `230A40(ctx, dx=rowidx, r8w=kind)` — row-usability bit query

- `row = q[ctx+0x10] + movsx(dx)*0x20`; `mask = d[row+0xC]`.
  Negative rowidx → ret 0.
- **Two-level field substitution** over a runtime-built BSS table at
  `0x209A2D0` (8-byte entries, mask dwords at `+0x110`/`+0x114`):
  - `idx1 = mask>>0xD & 0x1F` → entry1 {A1=+0x110 select, B1=+0x114 value}
  - `idx2 = mask>>3 & 0xF, +0x40` → entry2 {A2, B2}
  - `ecx = ((B1&A1) | (~A1 & mask)) & ~A2 | (B2&A2)`
    (bits where A=1 take B's value, else keep)
- `test cl,7` → low-3 bits nonzero → ret 0.
- Kind dispatch (movsx r8w): **0→!bit23, 1→!bit25, 2→!bit26, 3→!bit27,
  5→!bit24; kind 4 and ≥6 → 1.**
- Callers: `233110` passes kind = `w[in+0x50]`, skips row when ret 0.
  Bits 23–27 of the merged mask are per-kind blocked/unusable flags;
  with the runtime table zeroed the merged mask reduces to `d[row+0xC]`.

Executed cases: k0 accept (ret 1) / bit23 reject, bit26 (k2) reject,
k4 unconditional 1, lo3 reject, negative rowidx reject, and the full
two-level merge proven by planted BSS entries
(A1=0xFFFFFFFF → substitute path; A2=0xFFFFFFFF, B2=bit23 → ecx=bit23
→ k0 ret 0; k4 still 1).

## `2324F0(ctx, dx=rowidx, r8=scratch)` — point-in-triangle edge eval

- `scratch` ≥ 0x60: caller seeds `q[scr+8]` = P, a 16-byte sector-style
  record `{f+0 x, f+8 z}`; everything else is output.
- 3-iteration loop over vertex-index words `w[row+0x10+i*2]`; index table
  `d[0x908DE8] = {1,2,0}` → edges **v0→v1, v1→v2, v2→v0**, vertices = 16-byte
  sector records via `q[ctx+8]`.
- Per edge: `e1 = P−A`, `e2 = (B−A)/len` (len via `sqrtf`, host-computed,
  disclosed), `normal = cross(e2,e1)` via real `0x202E10` → `scr+0x50`;
  `normal.y = e1.x*e2n.z − e2n.x*e1.z` (signed side of P vs the edge).
- An edge **qualifies** iff `normal.y < −0.0001f` AND `len > 0.0001f`.
- Score: `t = dot(e1,e2n)/len − 0.5f` (const `0x1CEBB70`); `r12d` =
  argmin |t| edge index; init −1 → **ret −1 when no edge qualifies**.
- `231900`: `test eax,eax; jns skip` — **row usable ⇔ ret < 0** ⇔ P inside
  (or on the interior side of) every edge. Ret ≥ 0 = index of the violated
  edge closest to its midpoint. Interior of CW-wound triangles (as shipped
  rows are wound) yields positive normal.y on all edges.

Executed cases: CW triangle (0,0)-(0,4)-(4,0), P=(1,1) inside →
`eax = 0xFFFFFFFF`; P=(−1,2) violating edge0 with `t = 0` exactly →
`eax = 0`, last-iteration `scr+0x54` normal.y = 2.0 observed.

## Corrected addresses this round (hand-add slips again)

- Mask table base: `0x209A2D0` (initially miscomputed `0x20942D0`;
  caught by `UC_HOOK_MEM_READ` showing actual reads at `0x209A3E0`/`0x209A5E0`).
- Midpoint const: `f[0x1CEBB70] = 0.5f` (initially read `0x1CEBB6F` → 0.125).
- Edge index table: `d[0x908DE8] = {1,2,0}` (initially `0x908DE1`).

## Combined accept semantics (both inspected, per two-sided rule)

`233110`/`231900` row select = `230A40` bit-query pass (mask-kind filter)
→ `2324F0` point-in-triangle ret < 0 (geometric containment) → `231890`/
`231820` plane solve writes `f[pos+4]`. Both predicate layers now have
direct executed positive+negative coverage plus the end-to-end
`t26e350`/`t2730-accept` proofs.
