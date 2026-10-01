---
experiment: EXP-129
title: vec3 basis normalize/perpendicular pair — DB70 0040DB70 wrapper,
  B430 0040B430 two-stage normalize, XPROD 00202E10 cross product, the
  real 00861F14 sqrtf IAT thunk, and __security_check_cookie, executed
  real
contract: none — consumer anchor is
  ../03-World-Area-Field/Weather/mweather-resource-format.md (names
  0040B430 the basis normalise/publish and already carries the correct
  02CA43Ax cells); the page is outside this package's _experiments
  scope, so back-link adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/vec3-normalize-exec/check.py
---
# EXP-129 — vec3-normalize-exec

**Status:** complete · **15/15 functional cases, 34/34 mutants, stable
across three processes**
**Evidence:** `evidence/vec3-normalize-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was the vec3 normalize/perpendicular pair behind the
MWeather basis publish and the shared transform helpers — the first
float/SSE-heavy package in the lane. All bodies execute real:

| VA | role | execution |
|---|---|---|
| `0040DB70` | DB70 — flag-clear + seed-vec wrapper | **real** (49 B, 9 insns) |
| `0040B430` | B430 — two-stage basis normalize/publish | **real** (416 B, 82 insns) |
| `00202E10` | XPROD — vec cross product, w=0 | **real** (115 B, 26 insns) |
| `00861F14` | IAT thunk → `sqrtf` | **real** (6 B, 1 insn) |
| `00808C40` | `__security_check_cookie` | **real** (33 B, 8 insns) |
| `00809654` | `__report_gsfailure` | **real, partial** (209 B, 38 insns — head only; reached under the cookie-fail mutant, faults deeper through an unplanted indirect cell) |

Scripted boundary (entry-intercepted, traced, NOT executed):
`api-ms-win-crt-math-l1-1-0.dll!sqrtf` — reached through the **real**
B430 body, the **real** `00861F14` thunk (`jmp qword [rip+disp]`), and
the **real** IAT cell `q[0x8C2BB8]`; the cell ships the unbound hint
record `0x1CCED52` and is planted to a trampoline at `0x63040000`. The
host computes the same CRT `sqrtf` — correctly-rounded f32 on both
sides — and the call is observable as `sqrtf:in:out` bit tokens. The
import body itself is external code and stays disclosed-scripted
(same shape as EXP-126's `VCRUNTIME140!memcpy`).

## Scope correction — the row's preliminary constants were wrong

The board row's `scope` text (written from static disasm before
execution) recorded `b[0x22CA390]`, `f[0x22CA3A0]`, `f[0x22CA3B0]`,
`d[0x908EA0] = 16842.25f`, and XPROD as `r8 × rdx`. Every one of those
was wrong — the rip+disp arithmetic was misapplied. The executed
write-trace resolves the true cells:

| claimed | actual | role |
|---|---|---|
| `b[0x22CA390]` | `b[0x2CA4390]` | flag byte cleared by DB70 |
| `f[0x22CA3A0]` | `f[0x2CA43A0..+0xC]` | stage-1 published direction |
| `f[0x22CA3B0]` | `f[0x2CA43B0..+0xC]` | stage-2 published direction |
| `d[0x908EA0]` = 16842.25f | `d[0xD108A0]` = `0x3727C5AC` ≈ 1.0001e-5f | stage-2 local.z constant |
| `r8 × rdx` | `d × a` = `[rdx] × [r8]` | XPROD operand order |

The weather page's SWE2-EC7-39 block already carries the correct
`02CA43A0..02CA43B8` range — consistent.

## Measured semantics (native execution, not static reading)

**DB70** (`0040DB70`): `sub rsp,0x38`; builds the local vec at
`rsp+0x20` = `{d[0x1CEBBA8]=1.0f, 0, 0, uninit}` — `+0x20` gets the
seed, the `qword` store covers `+0x24..+0x2B` (y=z=0), and `+0x2C` (w)
is never written (fixture reads 0; the field is dead anyway — see
below). `b[0x2CA4390] = 0`, `call B430`, `add rsp,0x38`, `ret` —
returning B430's residual rax.

**B430** (`0040B430`, `rcx = vec4*`):

- Cookie prologue: `movaps` saves xmm6–9/xmm11 below the return
  address, `rax = q[0x1F44830] ^ rsp` (rsp after `push rbx` +
  `sub rsp,0x90` = entry − 0x98) stored at `[rsp+0x30]`; the same xor
  reloads into `rcx` for CHKCK. Exit `rax` keeps the
  `cookie ^ frame-rsp` residual — deterministic per fixture stack.
- **Stage 1** — reads `y=[v+4]`, `x=[v+0]`, `z=[v+8]` in that order
  (each read can fault; the fault rip is the read site);
  `len² = (x²+y²)+z²`; `sqrtf` through the real thunk;
  `eps = d[0x908E10]` (`0x358637BD` ≈ 1e-6f);
  `comiss eps, len` → `jbe` takes `s = 1.0f/len`, else `s = 0`
  (xorps xmm6). Unordered (NaN len) sets CF → `jbe` → `s = 1/NaN`,
  so **NaN propagates rather than zeroing**. `dir = v·s` stored to
  `f[0x2CA43A0..+0xC]`.
- **Local build** — `rsp+0x20 = {0, 1.0f, d[0xD108A0]≈1e-5f, w=v[0xC]}`.
  `r8 = &DIRA`, `rdx = rcx = &local` → `XPROD(local, local, DIRA)`:
  `dst = d × a` → `local = {az − c2·ay, c2·ax, −ax, 0}`.
- **Stage 2** — reads back `local.y/local.x/local.z`,
  `len²' = (y²+x²)+z²`, second `sqrtf`; `comiss eps, len'` → `ja`
  takes `s2 = 0`, else `s2 = 1.0f/len'` — the **same boundary
  predicate as stage 1 in opposite branch polarity** (`ja`-to-zero
  vs `jbe`-to-divide), so `len' == eps` divides in both stages and
  unordered still divides. `dirB = local·s2` stored
  to `f[0x2CA43B0..+0xC]`.
- Epilogue: cookie check → `movaps` restores → `add rsp,0x90`,
  `pop rbx`, `ret`.

**XPROD** (`00202E10`, `rcx=dst, rdx=d, r8=a`): computes the cross
product `d × a` into `rsp` temporaries first (`dst.x = dy·az − dz·ay`,
`dst.y = dz·ax − dx·az`, `dst.z = dx·ay − dy·ax`, `dst.w = 0`), then a
single `movups` copies all 16 bytes to `dst` — **`dst == src` aliasing
is safe**, verified by the `xprod-alias` case.

**CHKCK** (`00808C40`): `cmp rcx, q[0x1F44830]`; `bnd jne` →
`__report_gsfailure`; `rol rcx,0x10`; `test cx,0xFFFF`; `bnd jne` →
report; `bnd ret`. On mismatch the tail jmps `00809654`
(`__report_gsfailure`), which stores the bad cookie, calls
`0087AF34`, and faults deeper through an unplanted indirect cell in
the fixture — the `m-b430-xor` mutant dies on that divergence.

## Execution findings beyond the static reading

1. **The w field is dead end to end** — `v[+0xC]` is copied into
   `local.w` and XPROD overwrites it with 0; DB70 leaves the slot
   uninitialised. No case, mutant, or caller can observe it.
2. **The two "1.0f" divides share one constant cell** — `d[0x1CEBBA8]`
   is read by DB70's seed, stage-1's `divss`, and stage-2's `divss`
   (three rip+disp sites, one cell).
3. **`len == eps` and `len²` overflow both divide** — the `b430-eps-edge`
   case proves the `jbe` boundary includes equality (s = 1/eps), and
   `b430-inf` shows `len² = inf → len = inf → s = 1/inf = 0` → both
   published vecs zero, not NaN.
4. **NaN flows through both stages** — `comiss` unordered sets CF;
   stage 1's `jbe` and stage 2's `ja`-not-taken both reach the
   `1/len` arm, so a NaN component produces all-NaN published vecs
   (`0x7FC00000`), never the zero arm.
5. **The cookie residual is the exit rax** — `GSCOOK ^ (entry_rsp −
   0x98)` for a direct B430 call and `GSCOOK ^ (entry_rsp − 0xD8)` for
   DB70's nested call (its `sub 0x38` + call shift); the model tracks
   the caller vsp so both observations match bit-exactly.
6. **The stage-2 constant is ~1e-5f, not 16842.25f** — `d[0xD108A0]`
   ships `0x3727C5AC`; the published second direction is the
   normalised cross `{0,1,~1e-5} × dir` — for `{1,0,0}` in, dirB ≈
   `{0, ~1e-5, −1}`.

## Functional coverage (15)

`db70-basic` (flag clear + seed publish) · `b430-basic` ({3,4,0} →
{0.6,0.8,0} + perpendicular) · `b430-neg` (all-negative vec)
· `b430-eps-zero` (zero vec → both published zero) ·
`b430-eps-under` (len < eps → zero) · `b430-eps-edge` (len == eps →
divide) · `b430-inf` (len² overflow → inf → s=0 → zero) ·
`b430-nan` (NaN propagates, both vecs NaN) · `b430-w-dead` (w=7.5
invisible) · `b430-two` (B430 then DB70 on the same globals) ·
`b430-badptr` (unmapped arg → read fault at `0x40B461`) ·
`xprod-basic`/`xprod-neg`/`xprod-alias`/`xprod-two` (direct XPROD:
basis vectors, signed mix, dst==src, two calls).

## Mutant coverage (34)

DB70 flag-imm/seed-disp/vec-slot/yz-imm ×4 · B430 stage-1 eps disp,
`jbe→ja`, `divss→mulss`, 1.0f disp, `mulss` operand, three DIRA store
disps ×8 · local-build x-imm/y-imm/c2-disp/`mulss xmm9` operand ×4 ·
XPROD call rel32, stage-2 `ja→jbe`, `divss→mulss`, 1.0f disp, three
DIRB store disps, cookie `xor rax,rsp→xor rax,rax` ×7 · XPROD three
`subss→addss`, two operand disps, two store slots, `movups` dst ×8 ·
thunk IAT disp ×1. Every site byte is verified against the shipped
image before patching; all 34 killed.

## Disclosure — planted cells / scripted boundaries

- `q[0x8C2BB8]` — IAT slot for `sqrtf`. Ships the unbound hint record
  `0x1CCED52` (a rdata pointer, not code); planted to `0x63040000`.
- `0x63040000` — SQF trampoline (0xC3-filled page, entry-intercepted);
  host computes `sqrtf` via the real `api-ms-win-crt-math-l1-1-0.dll`
  on the fixture's xmm0 low dword and emits the `sqrtf:in:out` token.
- `b[0x2CA4390]`, `f[0x2CA43A0..+0x10]`, `f[0x2CA43B0..+0x10]` —
  BSS-range published cells (inside the shipped image map; planted
  flag value for DB70's clear).
- `VEC = 0x40010000`, `VDST/VSRC/VA/VDS2 = 0x40020000..` — fixture vec
  args on the planted heap.
- `q[0x1F44830]` — the shipped `__security_cookie` `0x2B992DDFA232`;
  read from the real image, not planted.
- `0x809654` `__report_gsfailure` — real head executed under the
  cookie mutant only; its `call 0x87AF34` faults deeper through an
  unplanted indirect cell (`memr` at 0). The deeper report/terminate
  tree is not claimed native.
