---
experiment: EXP-134
title: nav path-validator execution — PVAL 00335B60 consumer executed
  real over MLOAD/MCPY/ROTX/MXVW/AWRA P/RBUILD/VSCALE/VADD/GATE
  (scripted)/AGENTQ (scripted)/QWALK/PRED/LQUERY/DE6A0 plus the
  deferred rotation pair 00202E90/00217790 and the 5-byte
  dispatcher tail 0032A6A0
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-path-validator-exec/check.py
---
# EXP-134 — nav-path-validator-exec

**Status:** complete · **205/205 functional cases, 201/201 mutants,
stable across three processes**
**Evidence:** `evidence/nav-path-validator-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the `00335B60` path-validator consumer — the
caller that combines EXP-132's transform builders, EXP-130/131's
QWALK/PRED navigation probes, and EXP-133's LQUERY line-of-sight
query into one corridor check — plus the deferred rotation pair
`00202E90`/`00217790` and the dispatcher tail `0032A6A0`.

| VA | role | execution |
|---|---|---|
| `00335B60` | PVAL — path validator | **real** (768 B, 178 insns) |
| `00202E90` | MCPY — matrix copy + cosf/sinf → ROTX | **real** (100 B, 27 insns) |
| `00217790` | ROTX — in-place column (y,z) rotate | **real** (236 B, 58 insns) |
| `0032A6A0` | DE6A0 — `jmp 0026E100` dispatcher tail | **real** (5 B, 1 insn) |
| `00391410` | LQUERY — segment LOS (EXP-133) | **real** (758 B, 156 insns) |
| `003912E0` | BMASK — AABB bitmask (EXP-133) | **real** (286 B, 83 insns) |
| `003A1920` | DIST — dead 3D distance (EXP-133) | **real** (53 B, 12 insns) |
| `00468D50` | CAPT0 — capsule test A (EXP-133) | **real** (250 B, 67 insns) |
| `00468E50` | CAPT1 — capsule test B (EXP-133) | **real** (305 B, 79 insns) |
| `004691A0` | CPSEG — closest point on segment (EXP-133) | **real** (315 B, 68 insns) |
| `00468580` | TRIGD — trig-table edge helper (EXP-133) | **real** (325 B, 69 insns) |
| `00469410` | CAPV — sibling capsule variant (EXP-133) | **real** (336 B, 74 insns) |
| `0032A6E0` | RDEC — nav-record decode (EXP-133) | **real** (153 B, 36 insns) |
| `00861EC0` | TMS — `jmp [IAT]` memset (EXP-133) | **real** (6 B, 1 insn) |
| `00861F02` | TAT2 — `jmp [IAT]` atan2f (EXP-133) | **real** (6 B, 1 insn) |
| `0033A3D0` | PATHW — path-width probe (EXP-132) | **real** (405 B, 88 insns) |
| `00335F90` | BLKCHK — corridor-blocked check (EXP-132) | **real** (161 B, 42 insns) |
| `0033CB70` | AWRAP — angle wrap (EXP-132) | **real** (128 B, 32 insns) |
| `00203170` | MLOAD — axis-bank copy (EXP-132) | **real** (44 B, 9 insns) |
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

- `003357B0` GATE — corridor gate. A ~944 B subsystem/object-pool
  walk with its own nav-grid helpers and subsystem leaves; entry-
  intercepted with `eax` planted per case. Deferred to a follow-up
  package (EXP-135) on the same boundary discipline as AGENTQ.
- `0026E100` DE100 — object-root dispatcher reached through the real
  `0032A6A0` tail jump; entry-intercept, `eax` planted per case.
- `00318CA0` AGENTQ — mode-3 subsystem query; entry-intercept
  (EXP-132).
- `memset` via real thunk `00861EC0` + IAT `q[0x8C2A60]`,
  `atan2f` via `00861F02` + `q[0x8C2BD0]`, `sqrtf` via `00861F14` +
  `q[0x8C2BB8]`, `cosf`/`sinf` via `00861F08`/`00861F0E` +
  `q[0x8C2BA8]`/`q[0x8C2BB0]`, `_fdclass` via `q[0x8C2C10]`,
  `_isnan`/`_finite` via `q[0x8C2C68]`/`q[0x8C2C70]` — all real
  IAT/thunk bodies, import-dir proven, planted host trampolines.

## Verified behavior contract

`PVAL(rcx=agent, xmm1=angA, xmm2=angB, xmm3=tol, [rsp+0x28]=cap,
[rsp+0x30]=flags)` — frame `rbp = entry-rsp − 0x18`,
`rsp = entry-rsp − 0x118`:

1. `ucomiss tol, 0` → ordered-equal returns `0` immediately (jp and
   jne both continue; NaN and nonzero both continue).
2. `clamp = maxss(0.2f, minss(0.8f, cap))` — cap cells
   `d[0x8F3108]`=0.8f hi, `d[0x8F30F8]`=0.2f lo.
3. If `angB` is NaN or nonzero: `tol /= cosf(angB)` (real CRT cosf
   via `00861F08` thunk); `angB == 0` skips the divide.
4. `dir = ROTCOL(awrap(angA)) · ROTX(−angB) · {0,0,1,1}`:
   `MLOAD(mat)` copies `{+X,+Y,+Z,W}` from the signed axis bank
   `0x8C5F80..0x8C5FE0`; `xorps angB, [0x1CEBDA0]` sign-flips;
   `MCPY(mat, mat, −angB)` copies in place then calls real cosf/sinf
   and tail-`jmp`s `ROTX`; `MXVW(v30, mat, d[0x1F004C0])`. Then a
   second `MLOAD`, `RBUILD(mat, mat, awrap(angA))` (ROTCOL tail),
   `MXVW(v30, mat, v30)`.
5. `sub = q[agent+0x108]`; `v50 = v30·(tol + d[sub+0x110]) + agent.pos`,
   `v50.w = 1.0f`; `v40 = v30·tol + agent.pos`, `v40.w = 1.0f`;
   `v60 = v30·(rad110 − rad110·clamp + tol) + agent.pos`.
6. `GATE(agent, &v60, agent, q[agent+0xF0], stk: q[agent+0xE0],
   ((flags&4|0x10)<<2)|(flags&2))` — scripted; `gate==1 → ret 1`.
7. `mode = b[sub+0x174]`; if `mode == 3`:
   `AGENTQ(agent, &v50, 0, 0)` — scripted; nonzero → `ret 1`.
8. `flags & 8` → `QWALK(agent, &v40, mode)`; `1 → ret 1`.
   else `PRED(agent, &v40, d[sub+0x10C]·d[0x8FCC8C], mode)`;
   nonzero → `ret 1`.
9. `LQUERY(agent, &v60, clamp·d[sub+0x110])`; nonzero → `ret 1`.
10. `DE6A0(&v50, mode, mode==3)` → `DE100` scripted; `0 → ret 1`;
    else `ret gate==2 ? 2 : 0` (`cmove`).

`MCPY(dst, src, ang)`: four `movups` row copies interleaved with
register saves (each faults as two 8-byte accesses under emulation),
then `cosf`/`sinf` through the real `00861F08`/`00861F0E` IAT thunks,
`rcx = dst`, and a tail `jmp 00217790` (`rotx`). `rax = dst`.

`ROTX(mat, sin=xmm1, cos=xmm2)`: per 16-byte column
`y' = y·cos − z·sin`, `z' = y·sin + z·cos`, all four columns;
`rax = mat`.

`DE6A0`: 5-byte `jmp 0026E100` — the dispatcher sees the caller's
registers unchanged.

## Findings

1. **GATE stack-arg slot is callee-relative `+0x28/+0x30`.** The
   caller stores the gate's two stack args at `rsp+0x20`/`rsp+0x28`
   pre-call; the World intercept initially read callee `rsp+8/+0x10`
   (the caller's shadow space, always zero). Fixed to `+0x28/+0x30`.
2. **`movups` faults as two 8-byte accesses under emulation.** The
   MCPY copy model must issue per-8-byte fault checks, not a single
   16-byte one — the fault tuple carries size 8.
3. **SSE both-NaN propagation is dest-operand-first under the
   emulator.** `mulss xmm_s, [v]` with both operands NaN produced the
   dest's payload (`0x7FC00000` from the scalar), not the src's. The
   shared `_n2` helper was src-first since EXP-133 (never exercised
   on a both-NaN pair); flipped to dest-first. All 132 EXP-133
   mutants still kill.
4. **Missing `sq` store-qword helper** was latent in the shared
   model — `norm`'s zero path never ran until PVAL's `radius=0`
   PRED cases. Added.
5. **`jp`/`jnp` mutants at `0x335B9E`/`0x335BD8` are unobservable** —
   both successors converge. Replaced by `jp→jmp` mutations that
   force the guarded path.
6. **Retargeted-call mutants must land past the copied prefix.** An
   MLOAD `+8` retarget was invisible because the second MLOAD
   rewrote the whole matrix; `+0x20` (row-3-only copy) diverges.
7. **The third gate flag word is `((flags&4|0x10)<<2)|(flags&2)`** —
   `flags&8` selects the QWALK arm vs the PRED arm later; they are
   independent flag bits.
8. **PRED scale cell is `0x8FCC8C` = 0.9f** (verified through
   `disasm_fn.py`, matching EXP-132's BLKCHK site which reads the
   same cell).

## Method

Same as EXP-133: Unicorn world vs Python model over planted heap/BSS
fixtures; trace = scripted-boundary hits; mem = watched bytes;
rets/faults/ends byte-compared. Mutants patch a single shipped byte
(old-byte asserted) and must diverge observable state.

## Scope boundary

`003357B0` (GATE) is the remaining scripted boundary inside this
consumer — a ~944 B subsystem/object-pool walk calling nav-grid
helpers (`00391D10`, `003920F0` family) and subsystem leaves. It is
the next coherent package (EXP-135). `0026E100`/`00318CA0` remain
entry-intercepted pending their own packages.
