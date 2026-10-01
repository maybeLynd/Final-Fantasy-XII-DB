# EXP-188 — nonzero `22F8B0` occupancy inside `231400`

Harness: `C:\Users\Kristian\AppData\Local\Temp\exp166_check.py`
Evidence class: NATIVE-REPLAY / MODEL-PROVEN (hand-built egrid +
entity fixtures on the shipping EXE; not initialized-gameplay proof).
Result: **256/256, stable x3**.

## Scope

The `231400` position-commit query's final stage — the `22F830`
occupancy walk — previously ran with empty lane spans only (EXP-186
asserted `z22f8b0==2` on zero-length spans). This round plants nonzero
entity spans in the occupancy lanes and executes the full hit and
filter paths.

## Decoded structure

`22F830(ctx)` iterates lane bits `b[ctx+0x16]` for lanes 0..3:

- `C = w[lane+0x40]` cells per lane; bounds `q[lane+0x20]`;
  `span_idx = lane*(C+1) + w[ctx+0x10]` (cell).
- `w[ctx+0x12] = w[bt+span_idx*2]` (start),
  `w[ctx+0x14] = w[bt+(span_idx+1)*2] - start` (signed len).
- `call q[ctx]` per masked lane.

`231400` builds ctx on its stack: `q+0 = 0x22F8B0` (clean qword via
`lea rax,[rip-0x1c5e]` — the earlier "dword store" note was wrong),
`q+8 = ectx` (the lane IS the egrid context — `q[ectx+0x20]` bounds
and `q[ectx+0x28]` id array are shared with `233110`'s lane-0 tri
scan), `w+0x10 = re-derived cell`, `b+0x16 = 6` (lanes 1,2),
`q+0x18 = probe quad` (pos + snapped y), `d+0x20 = found`,
`d+0x24 = 1` (filter on).

`22F8B0(ctx)`:

- Early-out if `d[ctx+0x20] != 0` (first hit wins).
- Per span entry `i`: `eid = w[q[lane+0x28] + (start+i)*2]`;
  skip unless `eid-0x4000 <=u 0xFFF` (entity-id range).
- `ent = q[lane+0x18] + (eid-0x4000)*0x90`.
- Filter (`d[ctx+0x24]`): `idx = (d[ent+4]>>0xD&0x1F)+0x20`;
  `{A,B} = d[0x209A3E0+idx*8..+4]`; `r8 = (A&B) | (~A & d[ent+4])`;
  `r8 >=u 0x80000000` -> skip entity.
- Else `381EB0(ent, probe)`; nonzero -> `d[ctx+0x20] = 1`.

`381EB0(rec, probe)`: `202B70` transforms probe by rec's matrix at
`+0x50`; `d[rec]` = kind; kind 2 = strict containment of all three
transformed components in `(-1.0, +1.0)` (`hi` = shared `K=1.0f` at
`0x1CEBBA8`, `lo` = `-1.0f` at `0x1CEBC9C`) -> returns 2.

`231400` return: `ebx = 1 iff found==0` via
`cmp d[rsp+0x40], ebx; cmove ebx, edi` — `eax = ebx` is semantic
(1 = committable, 0 = blocked).

## Cases (all value-verified)

| case | setup | observed |
|---|---|---|
| t231400-occ | lane-1 span rows[4]=0x4000, kind-2 ent, identity mtx | eax=0 (blocked); z22f8b0=2 (lane2 early-outs on found); z381eb0=1; probe y 0,0 |
| t231400-occ2 | same entity on lane 2 | eax=0; z381eb0=1 — mask bit 2 verified |
| t231400-filt | lane-1 entity + mux {A=0x80000000,B=0xFFFFFFFF} | eax=1 (free); z22f8b0=2; **z381eb0=0** — filter veto precedes volume test |

## Boundary disclosure

- Entity record contents (kind 2, identity +0x50 matrix) are
  MODEL-PROVEN fixtures matching the `t22f830-hit` pattern; the
  mux table row planted at `0x209A3E0+0x20*8` for `-filt`.
- `861F14` sqrtf remains a disclosed host-libm MATH stub.
- `22F830`'s lane-0 bit (mask bit 0) not exercised — `231400`
  always passes mask 6.

## Stability

`python exp166_check.py` -> **256/256** in three separate processes.
