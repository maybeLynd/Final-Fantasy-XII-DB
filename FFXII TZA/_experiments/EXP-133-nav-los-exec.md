---
experiment: EXP-133
title: nav line-of-sight execution — LQUERY 00391410 wall-grid LOS
  query executed real over BMASK/DIST/CAPT0/CAPT1/CPSEG/TRIGD/CAPV/
  RDEC plus memset/atan2f IAT thunks and the full EXP-130/131/132
  tree
contract: none — consumer anchor for the same PRED 00335E50 /
  QWALK 0033D3E0 pair EXP-130/131 executed; no reciprocal contract
  names this experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-los-exec/check.py
---
# EXP-133 — nav-los-exec

**Status:** complete · **165/165 functional cases, 132/132 mutants,
stable across three processes**
**Evidence:** `evidence/nav-los-exec/` (`check.py`, `bodies.json`,
`gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the navigation line-of-sight / raycast query
tree below consumer `00335B60`. All bodies execute real under
Unicorn against planted BSS fixtures:

| VA | role | execution |
|---|---|---|
| `00391410` | LQUERY — segment LOS over the wall-record grid | **real** (758 B, 156 insns) |
| `003912E0` | BMASK — AABB → OR'd record bitmask | **real** (286 B, 83 insns) |
| `003A1920` | DIST — 3D distance (result discarded) | **real** (53 B, 12 insns) |
| `00468D50` | CAPT0 — capsule test A (point radius) | **real** (250 B, 67 insns) |
| `00468E50` | CAPT1 — capsule test B (edge + TRIGD) | **real** (305 B, 79 insns) |
| `004691A0` | CPSEG — closest point on segment | **real** (315 B, 68 insns) |
| `00468580` | TRIGD — trig-table edge helper | **real** (325 B, 69 insns) |
| `00469410` | CAPV — sibling capsule variant | **real** (336 B, 74 insns) |
| `0032A6E0` | RDEC — nav-record decode + atan2f | **real** (153 B, 36 insns) |
| `00861EC0` | TMS — `jmp [IAT]` memset | **real** (6 B, 1 insn) |
| `00861F02` | TAT2 — `jmp [IAT]` atan2f | **real** (6 B, 1 insn) |
| `0033A3D0` | PATHW — path-width probe (EXP-132) | **real** (405 B, 88 insns) |
| `00335F90` | BLKCHK — corridor-blocked check (EXP-132) | **real** (161 B, 42 insns) |
| `0033CB70` | AWRAP — angle wrap (EXP-132) | **real** (128 B, 32 insns) |
| `00203170` | MLOAD — const matrix copy (EXP-132) | **real** (44 B, 9 insns) |
| `00202F00` | RBUILD — rotation-matrix builder (EXP-132) | **real** (100 B, 27 insns) |
| `00217880` | ROTCOL — column rotation (EXP-132) | **real** (234 B, 58 insns) |
| `00217060` | MXV — matrix × vector (EXP-132) | **real** (235 B, 56 insns) |
| `00202B70` | MXVW — frame-temp MXV wrapper (EXP-132) | **real** (31 B, 10 insns) |
| `00861F08` | CTHUNK — `jmp [IAT]` cosf (EXP-132) | **real** (6 B, 1 insn) |
| `00861F0E` | STHUNK — `jmp [IAT]` sinf (EXP-132) | **real** (6 B, 1 insn) |
| `0033D3E0` | QWALK — adjacency-walk (EXP-131) | **real** (631 B, 145 insns) |
| `00384130` | WWRAP — pair wrapper (EXP-131) | **real** (40 B, 9 insns) |
| `00383F10` | GGRID — grid point query (EXP-131) | **real** (542 B, 141 insns) |
| `00383840` | ROOTL — root leaf (EXP-131) | **real** (8 B, 2 insns) |
| `00382D10` | TTEST — point-in-triangle (EXP-131) | **real** (391 B, 93 insns) |
| `0032A780` | ETHUNK — `jmp 0026E300` (EXP-131) | **real** (5 B, 1 insn) |
| `0026E300` | ECLASS — edge-class query (EXP-131) | **real** (73 B, 22 insns) |
| `00468880` | SEGT — seg orientation test (EXP-131) | **real** (496 B, 108 insns) |
| `0020E600` | BASE — pool decoder (EXP-131) | **real** (10 B, 3 insns) |
| `00335E50` | PRED — corridor-width probe (EXP-130) | **real** (305 B, 76 insns) |
| `00203080` | VSUB (EXP-130) | **real** (81 B, 17 insns) |
| `00202B10` | VADD (EXP-130) | **real** (81 B, 17 insns) |
| `00202FE0` | VSCALE (EXP-130) | **real** (67 B, 16 insns) |
| `00202DE0` | NCOPY (EXP-130) | **real** (33 B, 10 insns) |
| `00216660` | NORM — normalize-or-zero (EXP-130) | **real** (186 B, 49 insns) |
| `00202E10` | XPROD (EXP-130/131) | **real** (115 B, 26 insns) |
| `00861F14` | THUNKF — `jmp [IAT]` sqrtf (EXP-130) | **real** (6 B, 1 insn) |
| `00808C40` | `__security_check_cookie` | **real** (33 B, 8 insns) |

Scripted boundaries (traced, NOT executed):

- `memset` via real thunk `00861EC0` + IAT `q[0x8C2A60]`
  (VCRUNTIME140, import-dir proven), planted to `0x630A0000`
  host trampoline writing guest memory.
- `atan2f` via real thunk `00861F02` + IAT `q[0x8C2BD0]`
  (api-ms-win-crt-math-l1-1-0.dll, import-dir proven), planted to
  `0x630B0000`.
- `sqrtf` via real thunk `00861F14` + IAT `q[0x8C2BB8]` (EXP-130);
  `cosf`/`sinf` via real thunks `00861F08`/`00861F0E` + IATs
  `q[0x8C2BA8]`/`q[0x8C2BB0]` (EXP-132); `_fdclass` via real IAT
  `q[0x8C2C10]` (EXP-131); `_isnan`/`_finite` via real IATs
  `q[0x8C2C68]`/`q[0x8C2C70]` (EXP-130) — all import-dir proven,
  planted host trampolines.
- `00318CA0` AGENTQ — kept from EXP-132; unused by the LOS tree.

Planted fixture globals (disclosed; all BSS — ship zero): the whole
LQUERY grid parameter block `q/d[0x2AEE060..0x2AEE0B8]` (grid dims,
cell size, x/z epsilons, cell-flag map, per-cell record masks, mask
accumulator, record-mask stride), nav-record root `q[0x209A670]`,
`q[0x2AEDFB0]` root, `q[0x1F83530]` BASE pool, `d[0x209A3E0]`
bit-pair table — plus the CRT IAT cells above.

## Measured semantics (native execution, not static reading)

**LQUERY** (`00391410`, `rcx=p1`, `rdx=p2`, `xmm2=rad`): reads
`p1.z`, `p2.z`, `p2.x`, `p1.x` in that order; computes
`cvtt((z1+rad−epsz)/csz)`-style clamped cell bounds (eps cells at
`0x2AEE078`/`0x2AEE080`, cell size `0x2AEE070`); calls BMASK to
OR the per-cell record masks; a dead DIST call (result discarded);
then a 160-iteration record loop: `ebx` = bit index wrapping at 8,
`r14` = mask byte index starting at **0x10** (a 16-byte mask
header), `rsi` = record index, `rdi` = `i*0x20` (loop bound
`0x1400`), `r15d` = `i−0x20`. `i<0x20`: record =
`BASE(d[root+0x28]) + i*0x20`, type `w[0]`: 0 → CAPT0, 1 → CAPT1,
else skip. `i≥0x20`: `RDEC(i−0x20, out)` then CAPT1 with
`{out.x, 0, out.z, 1.0, out+0xC, out+0x10, out+0x14}` as the wall
point. First nonzero capture → `1`; exhaustion → `0`.

**BMASK** (`003912E0`, `ecx=c0 edx=r0 r8d=c1 r9d=r1`): `memset`
of `rlen` bytes; each bound `<0` → 0 via `test/jns`, `> m−1` →
`m−1` via `cmovg`; row guard `r0>r1 → done`, col guard
`c0>c1 → skip row`; `idx = row*w + col`; flag byte ≠ 0 → OR
`rlen` bytes from `lsrc + idx*rlen` into `dst + k` (k = 0..rlen).

**DIST** (`003A1920`): `dx,dy,dz` subs, `d2 = (dy²+dx²)+dz²`,
tail-`jmp` to the sqrtf thunk.

**CPSEG** (`004691A0`, `rcx=out rdx=a r8=b r9=p`):
`t = dot(a−p, a−b)/|a−b|²`; `comiss` `0>t` ordered → full 16-byte
endpoint `a`; `t>1` ordered → endpoint `b`; else (incl. NaN t —
unordered `jbe`) mid-lerp `a + (b−a)·t`. Output is a **single
16-byte `movaps` store** (unaligned/unmapped `out` faults as one
8-byte `memw`). `rax` = `out`.

**CAPT0** (`00468D50`, `rcx=seg rdx=edge`): `ucomiss` endpoint
equality needs BOTH `p1x==p2x` AND `p1z==p2z` ordered (`jp`+`jne`
both route to the CPSEG path — NaN endpoints are non-degenerate).
Point path: `d2 = (p1−e)²` vs `rad = srad+erad`, `sqrtf`, `seta`.
CPSEG path: `closest==p1` (both coords, `jp`+`jne`) → `0`; else
`d2 = (e−c)²` vs `rad`, `sqrtf`, `seta`.

**CAPT1** (`00468E50`, same signature): CPSEG first; a point
segment (`p1==p2`) skips the `closest==p1` exclusion; otherwise
`closest==p1` → `0`. Then `TRIGD(edge, closest) + srad` vs
`sqrtf((e−c)²)`, `seta`.

**TRIGD** (`00468580`, `rcx=edge rdx=closest`): `frac =
an/NEG2PI`; `i1 = (0x2000 − cvtt(frac·TRIGN)) & 0x7FFF`,
`i2 = cvtt(frac·TRIGP) & 0x7FFF` into the shipped 0x8000-float
table `0x1F004E0`; `x8 = (t2·dz + t1·dx)/e10`,
`x7 = (t1·dz − t2·dx)/e14`; `d = sqrtf(x8²+x7²)`; `comisd`
`d ≤ eps` **or unordered** → returns `e10`; else `inv = 1/d`,
returns `sqrtf((inv·x8·e10)² + (inv·x7·e14)²)`.

**CAPV** (`00469410`, `rcx=a rdx=b r9=p xmm2=rad`): sibling
variant — `lim2 = (rad + p+0x10)²`, same `t` projection; `t<0`
ordered → `d2 = (a−p)²`; `t≤1` **or unordered** → lerp `c`;
`t>1` → `c = b`; `d2 = (c−p)²`; `seta(lim2, d2)` — **no sqrtf**.
Native read order `b.z, p+0x10, b.x, a.y, b.y, p.y, a.x, a.z,
p.x, p.z`.

**RDEC** (`0032A6E0`, `ecx=index rdx=out`):
`rax = q[0x209A670]` (survives to early faults — the residual on a
record-pool fault is the root pointer, not zero); `rec =
q[nro+0x1A0] + sx32(idx)·16`; `vtx = q[nro+0x188] +
sx16(w[rec+2])·64`; `movsx eax, w[rec+4/6/8]` → three stack lanes
plus a **stale fourth lane** at `rsp+0x2C`; `cvtdq2ps` +
`mulps [0x908E30]` (1/4096 fixed-point scale) → `movdqu` scratch
`0x22D91B0` *(corrected from `0x23151B0` — a `+0x3C000` rip+disp
mis-add surfaced by OPUS's mechanical write census; the harness
always planted/watched the real target `RSCRATCH = 0x22D91B0`)*;
`out = {vtx30, vtx34, vtx38, sv0, sv1,
atan2f(vtx28, vtx20)}`.

## Scope corrections found by execution

1. **`f32_round` dropped the sign** — it computed `sgn` but
   returned an unsigned result, so `f32div(−4, 16)` returned
   `+0.25`. This silently broke every negative projection (`capv`,
   `cpseg`, `capt0/1` mid-lerp paths) while leaving positive-path
   cases green.
2. **SSE NaN propagation is operand-payload-exact** — the model's
   canonical `float("nan")` produced `7FC00000` where native
   produces the real-indefinite `FFC00000` (`0/0`, `inf−inf`,
   `0·inf`) or propagates the source operand's quieted payload
   (source operand wins, then dest). All float arithmetic in the
   new bodies now goes through NaN-exact `_m/_a/_s/_d` helpers;
   `sqrtf(neg)` input bits differ identically (`FFC00000` vs
   `7FC00000` — visible in the CRT trace).
3. **The record bitmask has a 16-byte header** — LQUERY tests
   `dst[0x10 + i/8]` while BMASK ORs at `dst+k`; fixtures planting
   bits at `lsrc+0` produced trivial all-zero parity (both sides
   return 0) and let all eight loop mutants survive. Real bits
   live at `lsrc + idx*rlen + 0x10 + i/8`.
4. **`rdx` in the CAPT calls is the wall point, not an edge** —
   the query capsule `{p1v3, p2v3, srad}` is built at `rsp+0x40`,
   the wall point `{x,0,z,1,e10,e14,angle}` at `rsp+0x20`/`+0x70`.
5. **RDEC's early-fault `rax` is the root pointer** —
   `mov rax, qword [rip]` at `0x32A6E6` survives to the
   `q[rax+0x1A0]`/`w[r8+2]` fault sites; each subsequent
   `movsx eax`/`mov eax` updates the residual.
6. **LQUERY's shl-src is the last pre-fault rax write** —
   `mov eax,1` at `0x39157E` means a `d[root+0x28]` fault returns
   `1`, not the mask pointer.
7. **BMASK's col guard swallows clamp mutants** — a `cmovg→cmovl`
   mutant leaves `c0 > c1` and the `jg` at `0x391374` skips the
   row entirely; the discriminating case needs a flag at the
   clamped column (`w−1`) so native's OR diverges from the skip.
8. **CAPV's `t>1` test is ordered-only** — `comiss t,1.0f; ja`
   skips the lerp only on ordered `t>1`; NaN `t` falls into the
   lerp and produces NaN coords, which then propagate into `d2`.

## Validation

- **165/165 functional cases** — LQUERY (null/empty/clamp/z-wide/
  far-row/t0-block/t0-miss/t1-block/type-skip/nav/multi/bit1/bit8/
  badp1/badroot/badcflg/badrec/badnroot/badnav), BMASK (range/
  clamp/invrow/rlen4/flip/wild/badcflg/badlsrc), DIST, CPSEG
  (pre/post/mid/degen/badout), TRIGD (gen/eps/large/badptr),
  CAPT0/CAPT1 (block/miss/degen/p1eq/nan/divlim/badedge/badseg),
  CAPV (pre/pre2/post/mid/badptr), RDEC (0/neg/1/noroot/nopool/
  badout) — with pointer-fault `rax` residuals for every body.
- **132/132 byte-precise mutants** — each patches one verified
  shipped byte; all sites byte-asserted against the EXE image.
- Stable across three independent processes; exit 0.

Evidence class: **NATIVE-REPLAY** over a disclosed synthetic fixture
— proves the shipped bodies' semantics, not production integration.
