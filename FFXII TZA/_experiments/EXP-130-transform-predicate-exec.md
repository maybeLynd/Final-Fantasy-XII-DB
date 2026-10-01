---
experiment: EXP-130
title: transform-workbench predicate family — PRED 00335E50 corridor-
  width probe over VSUB/VADD/VSCALE/NCOPY/NORM/XPROD, the real
  00861F14 sqrtf thunk, and __security_check_cookie, executed real
contract: none — consumer anchor is the nav-grid query 0033D3E0
  (scripted boundary here; its own tree is a follow-on package) and
  the transform-primitive pages under
  ../00-Engine-Core-Runtime/Shared-Transform-Workbench/; no reciprocal
  contract names this experiment, so findings adoption is routed via
  REQ-OPUS
method: B
live_game: false
tool: evidence/transform-predicate-exec/check.py
---
# EXP-130 — transform-predicate-exec

**Status:** complete · **35/35 functional cases, 36/36 mutants, stable
across three processes**
**Evidence:** `evidence/transform-predicate-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the transform-workbench predicate family around
the already-real XPROD (`00202E10`, EXP-129): the `00335E50` wrapper
that composes five vec4 primitives into a three-probe corridor-width
check. All bodies execute real:

| VA | role | execution |
|---|---|---|
| `00335E50` | PRED — corridor-width probe (three nav queries) | **real** (305 B, 76 insns) |
| `00203080` | VSUB — `dst = a − b`, all 4 components | **real** (81 B, 17 insns) |
| `00202B10` | VADD — `dst = a + b`, all 4 components | **real** (81 B, 17 insns) |
| `00202FE0` | VSCALE — `dst = a · xmm2`, all 4 components | **real** (67 B, 16 insns) |
| `00202DE0` | NCOPY — movups copy + NORM + `w = 0` | **real** (33 B, 10 insns) |
| `00216660` | NORM — normalize-or-zero in place | **real** (186 B, 49 insns) |
| `00202E10` | XPROD — `dst = d × a`, w=0 (re-executed) | **real** (115 B, 26 insns) |
| `00861F14` | IAT thunk → `sqrtf` | **real** (6 B, 1 insn) |
| `00808C40` | `__security_check_cookie` | **real** (33 B, 8 insns) |
| `00809654` | `__report_gsfailure` | **real, partial** (209 B, 38 insns — head only; reached under the cookie mutant, faults deeper through an unplanted cell) |

Scripted boundaries (traced, NOT executed):

- `api-ms-win-crt-math-l1-1-0.dll!sqrtf` — via the real `00861F14`
  thunk + real IAT cell `q[0x8C2BB8]` (unbound hint `0x1CCED52`),
  planted to `0x63040000`; host computes the same correctly-rounded
  CRT `sqrtf` (same shape as EXP-129).
- `api-ms-win-crt-math-l1-1-0.dll!_isnan` — real IAT cell
  `q[0x8C2C68]` (unbound hint `0x1CCECD8`), planted to `0x63050000`;
  host computes `_isnan` on the f64 arg.
- `api-ms-win-crt-math-l1-1-0.dll!_finite` — real IAT cell
  `q[0x8C2C70]` (unbound hint `0x1CCECCE`), planted to `0x63060000`;
  host computes `_finite` on the f64 arg.
- `0033D3E0` — nav-grid point query; **entry-intercepted** at its real
  VA, `eax` planted per case, args recorded as vec-content tokens.
  Its tree (`00384130` → `00383F10` grid lookup with its own
  `_fdclass` IAT `0x8C2C10`, `00383840` root `q[0x5ADFB0]`,
  `0x382D10`/`0x32A780` walkers over BASE-decoded pools) is a deep
  nav-mesh query — a follow-on package, not part of the transform
  family's scope.

## Scope correction — the preliminary cells were wrong again

Same class of rip+disp arithmetic error as EXP-129: the predicate
cells were first scoped as `q[0x86AC68]`/`q[0x86AC70]` (int3 padding
/ code bytes — nonsense targets). The corrected cells are real IAT
slots `q[0x8C2C68]`/`q[0x8C2C70]`, resolved through the PE import
directory to `_isnan` and `_finite` — so the predicate identities are
**proven by the import table**, not inferred. The `0x1F004B0` axis
constant ships `(0, 1, 0, 1)` and the NORM epsilon cell
`d[0x907698]` ships `0x00800000` = `FLT_MIN`.

## Measured semantics (native execution, not static reading)

**PRED** (`00335E50`, `rcx=p1, rdx=p2, xmm2=scale, r9d=flag`):

- Cookie prologue: saves rbx/rsi/rdi/xmm6, `rax = q[0x1F44830] ^ rsp`
  (rsp after 3 pushes + `sub 0x80` = entry − 0x98) → `[rsp+0x60]`;
  exit rax is the 0/1 result (CHKCK preserves it).
- `rsi = p2`, `rdi = p1`, `ebx = flag`, `xmm6 = scale`.
- `tmp = p1 − p2` (VSUB → `rsp+0x20`), then **`tmp.y` is flattened to
  0** (`xorps xmm0; movss [rsp+0x24], xmm0`) — the corridor offset is
  XZ-plane only.
- NCOPY normalizes `tmp` in place and clears `tmp.w`.
- `tmp = tmp × (0, 1, 0)` (XPROD, const `f[0x1F004B0]`) — the
  perpendicular `(−z, 0, x)`.
- `tmp *= scale` (VSCALE, all four slots — `w` is already 0).
- Probe 1: `Q(p1 + tmp, p2 + tmp, flag)` — `== 1` → return 1.
- Probe 2: `Q(p1 − tmp, p2 − tmp, flag)` — `== 1` → return 1.
- Probe 3: `Q(p2 + tmp, p2 − tmp, flag)` — return `(eax == 1)` via
  `sete` (only exactly 1 counts; `pred-ret2` proves `2 → 0`).

**VSUB/VADD/VSCALE** (`00203080`/`00202B10`/`00202FE0`): all four
components computed through `rsp` temporaries then a single `movups`
store — dst==src aliasing is safe (verified by `vsub-alias` /
`vadd-alias`). Read order is `a0, b0, a4, b4, a8, b8, aC, bC` for the
binary ops; `+0, +4, +8, +0xC` for VSCALE.

**NCOPY** (`00202DE0`): `movups [rdx] → [rcx]`; `call NORM(rcx)`;
`d[rcx+0xC] = 0`. Exit rax is NORM's residual (below).

**NORM** (`00216660`, `rcx = vec*`): normalize-or-zero in place.

- `len² = (x² + y²) + z²`; `cvtps2pd` to f64.
- `call _isnan(len²)` — nonzero → **zero path**.
- `call _finite(len²)` — zero → **zero path**.
- `comiss len², FLT_MIN` — `jbe` (len² ≤ FLT_MIN, i.e. zero or
  denormal) → **zero path**.
- Else `sqrtf(len²)` via the real thunk, `s = d[0x1CEBBA8] / len`
  (`1.0f`), `x·s, y·s, z·s` written back in place — **`w` is
  untouched** on the scale path (`norm-w` proves `w=7.5` survives).
- Zero path `0x216701`: `q[v] = q[v+8] = 0` — all **16 bytes**
  zeroed, w included (`norm-zerow`).
- **Exit rax residual**: `_finite`'s return `1` survives the epilogue
  on the scale path; the zero path `xor eax,eax` → 0. Both
  observations matched bit-exactly (`ncopy-basic`/`ncopy-zero`).

## Execution findings beyond the static reading

1. **`tmp.y` is flattened before normalize** — the corridor offset is
   strictly XZ. A pure-Y delta (`pred-degen-y`: `p1−p2 = (0,8,0)`)
   normalizes to zero → offset 0 → all three probes see the
   unshifted points.
2. **NORM is normalize-or-zero, not normalize-or-leave** — the
   `0x216701` tail zeroes the whole vector on NaN / ±inf / denormal /
   zero `len²`. This matches B430's per-stage semantics but through a
   completely different gate (`_isnan`/`_finite`/`comiss FLT_MIN`
   vs `comiss eps; jbe/ja`).
3. **`w` semantics differ by path** — untouched by NORM's scale path,
   zeroed by NORM's zero path, always cleared afterward by NCOPY.
   Inside PRED the flow makes `tmp.w` dead after XPROD writes 0.
4. **The third probe uses `p2 ± off`, not `p1`** — `(p2+off, p2−off)`
   is a self-difference at `p2`, a width test of the corridor at the
   destination point.
5. **The `_finite` residual leaks out of NORM** — callers observe
   `rax = 1` after a successful normalize and `0` after a zero path;
   PRED's own flag arg (`r8d = ebx`) is immune (ebx), but the
   `m-pred-r8d` mutant (`r8d = eax`) shows the residual is live.
6. **`len² == FLT_MIN` takes the zero path** — `jbe` includes
   equality (`norm-eps-edge`).

## Functional coverage (35)

Helpers: `vsub-basic/-neg/-alias/-badptr` · `vadd-basic/-neg/-alias` ·
`vscale-basic/-neg/-zero` · `ncopy-basic/-neg/-zero/-den/-inf/-nan`
(the four zero-path gates) · `norm-w` (w survives scale path) ·
`norm-eps-edge` (len² == FLT_MIN → zero) · `norm-small` (len² =
2.5e-5 > FLT_MIN → normalize) · `norm-zerow` (zero path zeroes w) ·
`xprod-basic/-neg`.
PRED: `pred-t1`/`pred-t2`/`pred-t3` (early-outs at each probe) ·
`pred-none` (all three miss → 0) · `pred-ret2` (t3 = 2 → `sete` → 0)
· `pred-eq` (p1 == p2 → tmp 0 → off 0) · `pred-nan` (NaN component →
NORM zero path → off 0) · `pred-scale0`/`pred-scale-neg` ·
`pred-degen-y` (pure-Y delta flattened to 0) · `pred-y-same` (y
flattened despite p1.y ≠ p2.y) · `pred-badptr` (unmapped p1 → read
fault, rax = cookie residual `GSCOOK ^ (rsp−0x98)`) · `pred-two`
(two sequential probes sharing the planted-return queue).

## Mutant coverage (36)

PRED: y-flatten store disp, axis `lea` disp, `cmp eax,1` imm,
`je→jne`, `sete→setne`, `movaps xmm6` operand (scale save),
`mov r8d,ebx→eax`, five call-rel32 shifts (vsub/xprod/vscale/vadd/
q33-entry), cookie cell disp ×13 · NORM: eps disp, `jbe→ja`,
`_isnan jne→je`, `_finite je→jne`, `divss→mulss`, 1.0f disp, two
call-cell disps (each repointing to the other's IAT slot — the swap
is observable), three `mulss` opcode/disp sites, zero-path qstore
disp ×12 · NCOPY: w-clear imm, `movups` dest reg ×2 · VSCALE:
`mulss→addss`, `movaps` operand ×2 · VSUB/VADD: `subss↔addss`,
operand disp ×4 · XPROD: `subss→addss`, store slot, `movups` dst ×3
(sites proven in EXP-129). Every site byte verified against the
shipped image before patching; all 36 killed.

## Disclosure — planted cells / scripted boundaries

- `q[0x8C2BB8]` — IAT `sqrtf` (ships unbound hint `0x1CCED52`) →
  `0x63040000` trampoline.
- `q[0x8C2C68]` — IAT `_isnan` (ships unbound hint `0x1CCECD8`) →
  `0x63050000` trampoline.
- `q[0x8C2C70]` — IAT `_finite` (ships unbound hint `0x1CCECCE`) →
  `0x63060000` trampoline.
- `0x63040000/0x63050000/0x63060000` — 0xC3-filled trampoline pages,
  entry-intercepted; host computes `sqrtf` (real CRT), `_isnan`,
  `_finite` on the guest xmm0 and emits `sqrtf:`/`isnan:`/`finit:`
  tokens.
- `0033D3E0` — entry-intercepted; `eax` planted per case from the
  case's `qrets` queue; the call is observable as
  `q33:vecA:vecB:flag:ret` tokens with both arg vectors read as
  16-byte contents (so the transform output itself is checked, not
  just the call count).
- `P1/P2 = 0x40010000/0x40011000`, `VDST/VA/VB/VD2 = 0x40020000..` —
  fixture vec args on the planted heap.
- `q[0x1F44830]` — shipped `__security_cookie` `0x2B992DDFA232`;
  read from the real image, not planted.
- `0x809654` `__report_gsfailure` — real head executed under the
  cookie mutant only; `call 0x87AF34` faults deeper through an
  unplanted indirect cell. The deeper report/terminate tree is not
  claimed native.

## Known limitations

- The `0033D3E0` nav-grid query is scripted, not executed — PRED's
  proof covers the transform algebra, probe construction, and the
  `==1` decision logic against planted query returns; the grid
  semantics themselves are a follow-on package.
- The `_isnan`/`_finite` identities are proven by the PE import
  directory (hint records resolved to export names); their runtime
  bodies remain external code — disclosed scripted, host-computed.
