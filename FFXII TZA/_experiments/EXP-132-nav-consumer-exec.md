---
experiment: EXP-132
title: nav consumer layer — PATHW 0033A3D0 path-width probe and
  BLKCHK 00335F90 corridor-blocked check executed real over the
  EXP-130 PRED family and the EXP-131 nav-grid query tree
contract: none — consumer anchor for the same PRED 00335E50 /
  QWALK 0033D3E0 pair EXP-130/131 executed; no reciprocal contract
  names this experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-consumer-exec/check.py
---
# EXP-132 — nav-consumer-exec

**Status:** complete · **98/98 functional cases, 99/99 mutants,
stable across three processes**
**Evidence:** `evidence/nav-consumer-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the consumer layer above the now-real
nav-grid query tree: callers of `0033D3E0`/`00335E50`. Both execute
real under Unicorn against the planted synthetic nav mesh, closing
EXP-130's last scripted seam (PRED's deep `0033D3E0` boundary runs
real inside BLKCHK):

| VA | role | execution |
|---|---|---|
| `0033A3D0` | PATHW — path-width probe, 5× QWALK | **real** (405 B, 88 insns) |
| `00335F90` | BLKCHK — corridor-blocked check | **real** (161 B, 42 insns) |
| `0033CB70` | AWRAP — angle wrap to `[−π, π]` | **real** (128 B, 32 insns) |
| `00203170` | MLOAD — shipped const 4×4 matrix copy | **real** (44 B, 9 insns) |
| `00202F00` | RBUILD — rotation-matrix builder | **real** (100 B, 27 insns) |
| `00217880` | ROTCOL — in-place column rotation | **real** (234 B, 58 insns) |
| `00217060` | MXV — matrix × vector | **real** (235 B, 56 insns) |
| `00202B70` | MXVW — frame-temp MXV wrapper | **real** (31 B, 10 insns) |
| `00861F08` | CTHUNK — `jmp [IAT]` cosf | **real** (6 B, 1 insn) |
| `00861F0E` | STHUNK — `jmp [IAT]` sinf | **real** (6 B, 1 insn) |
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

- `api-ms-win-crt-math-l1-1-0.dll!cosf` / `sinf` — real thunks
  `00861F08`/`00861F0E` + IAT cells `q[0x8C2BA8]`/`q[0x8C2BB0]`
  (import-directory proven), planted to `0x63080000`/`0x63090000`
  host trampolines computing exact f32 results.
- `_fdclass` via real IAT `q[0x8C2C10]` (EXP-131 host class map);
  `sqrtf` via real thunk+IAT `q[0x8C2BB8]`; `_isnan`/`_finite` via
  real IATs `q[0x8C2C68]`/`q[0x8C2C70]` (EXP-130, import-dir proven).
- `00318CA0` AGENTQ — mode-3 subsystem query; entry-intercept with
  per-case planted `eax` (its callee chain enters an object tree).

Planted fixture globals (disclosed; all BSS — ship zero):
`q[0x2AEDFB0]` root, `q[0x1F83530]` BASE pool, `d[0x209A3E0]`
bit-pair table — plus the five CRT IAT cells.

## Measured semantics (native execution, not static reading)

**PATHW** (`0033A3D0`, `rcx=A`, `rdx=B`): corridor path-width probe.
`QWALK(B→A, flag=1) != 1` → return `1` immediately (direct path
exists). Otherwise two rounds (`+π/4`, `−π/4`):

- `w = B + R(θ)·((A−B)·0.5)` — VSUB, VSCALE by `d[0x1CEBB70]` (0.5f),
  MLOAD const basis, AWRAP, RBUILD+ROTCOL, MXVW, VADD.
- `QWALK(B→w) == 1` → round passes (w unreachable from B).
- else `QWALK(w→A) == 1` → round passes; `!= 1` → jumps to the
  `0x33A40B` dead tail (`add [rax],al` ×2 then epilogue — faults on
  the small-int return; a full B→w→A path makes the round fail).
- Both rounds pass → `xor eax` → return `0`.

**BLKCHK** (`00335F90`, `rcx=agent`): `sub = q[agent+0x108]`;
`scale = d[sub+0x10C] · d[0x8FCC8C]` (0.9f); `mode = b[sub+0x174]`.
`PRED(agent, agent+0x20, scale, mode) != 0` → `1`;
`QWALK(agent, agent+0x20, mode) == 1` → `1`; `mode == 3` →
`AGENTQ(agent, agent+0x20, 0, 0) != 0` → `1`; else `0`. All
nonzero exits return literal `1`.

**AWRAP** (`0033CB70`): `x > 4π` (`d[0xD10B0C]`) or `−4π > x`
(`d[0xD10B20]`) → mod-2π via `divss`/`cvttss2si`/`cvtdq2ps`/`mulss`
(all `d[0x1CEBC78]` = 2π); else looped `addss`/`subss` ±2π
(`d[0x915624]`/`d[0x1CEBC78]`) against ±π gates
(`d[0x1CEBC50]`/`d[0x915620]`). `rax` residual: mod path returns the
`cvttss2si` truncation zero-extended; loop paths preserve entry
`rax` — the wrapped value is only in `xmm0`.

**MLOAD** (`00203170`): four `movups` rows from shipped cells
`0x8C5F80`, `0x8C5F90`, `0x8C5FB0`, `0x8C5FD0` — the shipped
matrix is identity. The cells are **not** an oddity of MLOAD:
the region `0x8C5F80..0x8C5FE0` is a shared engine-wide
**signed axis-basis bank** at 16-byte stride — `+X` `0x8C5F80`,
`+Y` `0x8C5F90`, `−Y` `0x8C5FA0`, `+Z` `0x8C5FB0`, `−Z`
`0x8C5FC0`, `W` `0x8C5FD0` (OPUS reading, verified from the
image). MLOAD selects the identity subset `{+X,+Y,+Z,W}`;
a reimplementation should carry the bank, not the four
addresses.

**RBUILD** (`00202F00`): copies the matrix, calls `cosf`/`sinf`
through the real IAT thunks, tail-`jmp`s ROTCOL. **ROTCOL**
(`00217880`): per column `(x,z) → (z·sin + x·cos, z·cos − x·sin)`.

**MXV** (`00217060`): per output component
`w·m[o+0x30] + ((y·m[o+0x10] + x·m[o]) + z·m[o+0x20])`, f32-rounded
in native order; vector read order `x, z, w, y` — `rax` becomes
`dst` at `0x217069`, *after* the first vector read (a first-read
fault returns `0`). **MXVW** (`00202B70`): MXV into frame temp
`vsp−0x18`, `movups` copy to dst.

## Scope corrections found by execution

1. **BKSC took three mis-adds to land** — `0x91CC89` (misaligned
   string bytes) → `0x91CC8C` (bad disp sum) → **`0x8FCC8C` = 0.9f**
   (`0x335FC4 + 0x5C6CC8`). Fourth occurrence of the rip+disp class.
2. **PATHW's probe directions are asymmetric** — `Q(B→w)` then
   `Q(w→A)`, flag arg `r8d = 1` — cases designed for `A→w` never
   reach the probe2 `jne` sites (the round-2 mutants' survival
   traced this).
3. **PATHW calls `0x202B10` = VADD, not MXV** — the two per-round
   transforms are MXVW→MXV (real `0x217060`) then VADD for `+B`.
4. **AWRAP's result is xmm0-only** — arithmetic/branch mutants
   inside the wrap loops are invisible to ret/fault/trace compare;
   killable sites are the ±4π gate disps (forces the mod path →
   `rax` diverges), the loop-back branches (infinite loop →
   `emuerr`), the `cvttss2si` opcode, and the `divss` opcode
   (changes the truncation → `rax`).
5. **Mutable fixture lists must not be shared** — the World's
   AGENTQ intercept popped `case["agrets"]` directly, consuming
   the model's scripted result before it ran; World now owns a copy.
6. **MLOAD's sources skip a row** — `0x8C5F80/90/B0/D0` selects
   `{+X,+Y,+Z,W}` from the shared signed axis-basis bank at
   `0x8C5F80..0x8C5FE0` (skipping `−Y`/`−Z`, not padding); the
   shipped matrix is identity, so `w` simplifies to
   `B + rot(A−B)·0.5` in the (x,z) plane.

## Validation

- **98/98 functional cases** — leaf (AWRAP/MXV/MXVW/ROTCOL/RBUILD/
  MLOAD), BLKCHK (clear, pred-block, flag-gate, radius NaN, mode
  0/3/7, AGENTQ positive/negative/zero), PATHW (direct, open,
  blocked, mixed, rotated-fail, probe2-reached r1/r2), and
  pointer-fault residuals for every new body.
- **99/99 byte-precise mutants** — each patches one verified
  shipped byte; all sites byte-asserted against the EXE image.
- Stable across three independent processes; exit 0.

Evidence class: **NATIVE-REPLAY** over a disclosed synthetic fixture
— proves the shipped bodies' semantics, not production integration.
