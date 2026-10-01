---
experiment: EXP-114
title: Computed shadow LOD — shipped siblings 003B5980/003B5C00/003B5CE0/003B5D40/003B5E20/003B6000 plus the const-reset leaf 0036DD80, isolated under Unicorn
contract: ../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md
method: B
live_game: false
tool: evidence/shadow-lod-compute-exec/check.py
---
# EXP-114 — shadow-lod-compute-exec

**Status:** complete · **38/38 functional cases, 38/38 mutants, stable
across three processes**
**Evidence:** `evidence/shadow-lod-compute-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-113 scripted `003B5980` — the computed shadow-LOD body the sync
stage calls when `!(b[rec+0xC0] & 2)`. Re-analysis showed it is not
one function but a **contiguous family of six siblings**
(`0x3B5980..0x3B6020`, bounded by PASS) plus a const-reset leaf — all
generation-checking the same `0xE0` shadow-slot pool at
`q[0x02B40528]`. This experiment executes the entire family under
Unicorn and diffs slot bytes, the `0x22D91xx`/`0x22D8Fxx` scratch
block, the leaf's global, the call trace, and the returned `xmm0`
against a Python model.

| VA | role | execution |
|---|---|---|
| `003B5980` | LODC — computed shadow LOD | **real** (629 B, 124 insns) |
| `003B5C00` | ACC — five-channel countdown accumulator | **real** (214 B, 54 insns) |
| `003B5CE0` | CPY — field-copy verb | **real** (88 B, 21 insns) |
| `003B5D40` | INIT — block copy + countdown init | **real** (213 B, 33 insns) |
| `003B5E20` | FSYNC — bitfield + field sync | **real** (473 B, 108 insns) |
| `003B6000` | CLRE — clear-enable | **real** (27 B, 7 insns) |
| `0036DD80` | LEAF — resets `0x1EF93F0` to the shipped `[0,0,0,1]` | **real** (15 B, 3 insns) |
| `00421FF0` | RES2 — bone-object resolver | scripted (EXP-108 stubs) |
| `003E6F70` | GATE — gate-position reader | scripted (EXP-108 stubs) |
| `00861F14` | `sqrtf` via IAT `api-ms-win-crt-math` | scripted |

RES2/GATE are scripted through EXP-108's proven stub layer (MIDS/OUTR/
E56 traced, controlled returns) — both were executed real in EXP-108;
the boundary is reused rather than silently re-baked. `sqrtf` is a CRT
import thunk, stubbed with the real `math.sqrt` result and its `xmm0`
operand traced.

## Measured semantics (native execution, not static reading)

**LODC `003B5980(ecx)`:** slot = `q[0x02B40528] + (ecx & 0xFF)*0xE0`.
Gen `d[slot+0x10] == ecx` and `w[slot+4] != -1`, else return the
shipped default `f[0x01CEBBA8]`. Actor record =
`q[0x022C6F28] + sx16(w[slot+4])*0x740`; `d[rec+0x284] == 0` → default.
Then `RES2(rec, zx(w[slot+0x3C]))` (bone object) and `GATE(rec)` (gate
position) run; `LEAF` reloads `[0,0,0,1]` into `0x1EF93F0` —
`xmm6 = 1.0`, `xmm3 = 0.0`. Distance uses the **first three**
bone-minus-constant deltas: `sum = dx²+dy²+dz²`, partial `dx²+dy²`
stored at `0x22D91AC`, total at `0x22D91CC`, `sqrtf` input traced and
result stored at `0x22D9198`. The fade is:

```
xmm1 = max(xmm3 + dist, gate.x)          # gate.x = f[0x22D91D0]
xmm2 = (min(gate.y, xmm1) - gate.x) * gate.w   # gate.w = f[0x22D91DC]
xmm4 = clamp(xmm6 + xmm3 - xmm2, xmm3, xmm6)   # → [0.0, 1.0]
```

The result vector `[xmm4, dy², dz², total]` lands at `0x22D91C0`
(element 0 overwritten) and is copied to `0x22D8FB0`; `0x22D91F0`
holds `xmm6+xmm3` pre-subtract. Returned `xmm0 = movss` of `xmm4` —
upper lanes zeroed.

**ACC `003B5C00(ecx)`:** gen + `b[slot+0x40] & 1`. Five countdown
channels, each `if b[ch] != 0: accum += rate; b[ch] -= 1`: ch0
(`f50+=f60, f54+=f64`), ch2 (`f58+=f68, f5C+=f6C`), ch1 (`f70+=f74`),
ch3 (`f78+=f7C`), ch0x43 (`f98+=f9C`).

**CPY `003B5CE0(ecx, edx)`:** gen. `d[+0x48]→d[+0x30]`,
`d[+0x4C]→d[+0x34]`, `w[+0x38] = edx==0 ? w[+0x3C] : w[+0x3E]`, then
`f[+0x48]=xmm2`, `f[+0x4C]=xmm3`.

**INIT `003B5D40(ecx, edx)`:** gen. Six dwords `+0xC0..+0xD4` →
`+0x80..+0x94`; `b[+0x43]=dl`; `d[+0x98]=0`; writes the two init
globals `0x22D9148/0x22D914C`; `q = 1.0f / bits2f(edx)` — the edx
dword reinterpreted as a float (so `edx=5` → `1/7e-45 = +inf`, not
`1/5`); `f[+0x9C]=q`; `if dl != 0: b[+0x43] -= 1; f[+0x98]=q`.

**FSYNC `003B5E20(ecx, rdx=arg)`:** gen. Existing `b[slot+0x40]` bits
gate four field-copy arms (bit1 `arg+A0/A4`→`+50/54`,`+80/84`, clears
`b[0]`; bit2 `arg+B0`→`+70`,`+90`, clears `b[3]`; bit3 `arg+A8/AC`→
`+58/5C`,`+88/8C`, clears `b[2]`; bit4 `arg+B4/B8`→`+48/4C`). If
`w[arg+0x32] != 0`: `arg+4C/50`→`+A0/A4`;
`f[+0xB0] = f32(sx16(w32)>>6) * f[0x00D115B0]` (const ≈ `0.0234`);
`arg+58/5C`→`+B4/B8`; `arg+10`→`+A8`, **`arg+0x54`→`+AC`** (not
`+0x14` — see findings). Then `b[+0x40]` is rebuilt: `w32` bits
`{0,1,3,2,4,5}` map onto `b40` bits `{1,2,3,4,5,6}` through six
`shl/sar/xor/and/xor` rounds, preserving bits 0 and 7; finally a dword
write `d[slot]=0` clears the countdown bytes.

**CLRE `003B6000(ecx)`:** gen → `b[slot+0x40] &= 0xFE`.

**LEAF `0036DD80`:** `movaps xmm0, [0x8C5FD0]` (shipped `[0,0,0,1]`)
→ `movups [0x1EF93F0], xmm0` → `ret`.

## Execution findings (beyond the static reading)

1. **`arg+0x54`, not `arg+0x14`** — FSYNC's second w32-block dword
   copy reads `[rdx+0x54]` into `slot+0xAC`. The hand-decode had
   `+0x14`; the byte-level diff (native `fac` high half zeroed)
   exposed it — the arg's `+0x54` field is a *seventh* payload dword
   alongside `+0x10`, distinct from the `+0x4C..+0x5C` group.
2. **`sar ax,6`, not `shl`** — the `w32` scale is an arithmetic
   *right* shift (`sx16(w32)>>6`, cwde, cvtdq2ps), then a **packed**
   `mulps` against the vec4 const at `0x00D115B0` with only lane 0
   stored via `movss`. Const = `0x3CC00000 ≈ 0.02344` — a per-tick
   fade rate; `w32=0x20` yields `0>>6=0`, so the default case writes
   `f[+0xB0]=0`.
3. **The LEAF const is `[0,0,0,1]`** — `xmm6=1.0` (the fade ceiling)
   and `xmm3=0.0` (the floor) both come from `0x1EF93F0` after LEAF
   resets it; LODC re-reads them, so the clamp bounds are the shipped
   constant, not immediates.
4. **Distance uses three components** — `dx²+dy²+dz²` from
   `G_C[0..2]`; `G_C[0]` is *then* overwritten by `xmm4`, so the
   returned vector `[result, dy², dz², total]` mixes the fade with
   intermediate squares — `0x22D8FB0` is not a clean vec4.
5. **`1/bits2f(edx)` overflows to `+inf`** for small edx — `edx=5`
   is `5·1.4e-45` as a float, so `q = +inf` lands in `f[+0x9C]`/`f98`.
   The init "rate" field is a float reinterpret, not an int divide.
6. **Upper `xmm0` lanes are always zero** — both the default exits
   and the happy tail use `movss xmm0, [mem]` (zeroing bits 32–127);
   the `movd`/`movss` pair at the tail means only lane 0 of the
   computed vector escapes.

## Mutation campaign

38 byte-precise mutations across: LODC gen disp/JCC, `w04` `-1`
compare, `d284`/`d284b`/`res2`/`gate` JCCs, delta subs, square muls,
sum adds, `fabs`, min/max/clamp SSE ops, the tail `movss`→`movups`;
ACC gen, enable `&1`, all five channel adds + countdown decs; CPY
gen, edx select, `w3c/w3e` disps; INIT gen, `divss`→`mulss`,
`test dl`, `dec`; FSYNC gen, `w32` test, mask immediates
`2`/`0x10`/`0x40`, `sar 6`→`7`, the dword clear imm; CLRE gen + `&FE`.
**38/38 killed.**

Six initial survivors were all coverage gaps, not equivalent mutants:

- `m-w04-neg` — `je`→`jne` on `w04==-1` needed `rec[-1]` *planted
  valid* (`lodc-w04-neg-live`), so the mutated arm runs the full path.
- `m-max`/`m-min`/`m-clamp-hi` — `[0,1]` clamp saturates both arms on
  the default geometry; needed `lodc-mid` (dist 35 between
  `gate.x=30`/`gate.y=100`) where the result stays in-range.
- `m-ret` — `movss`→`movups` differs only in `xmm0` upper lanes;
  needed a 16-byte `ret_v` obs plus `rdi`/stack-canary plants to
  prove the upper lanes carry saved-`rdi`/canary bytes under movups.
- `m-init-div` — `edx=0x3F800000` gives `bits2f=1.0` so `1/x == 1*x`;
  needed `init-dmid` (`edx=0x40000000` → `2.0`).
- `m-fs-sar` — `sar 6`→`7` equivalent on `w32=0x20` and `0xFFFF`;
  needed `w32=0x40` (`>>6`=1, `>>7`=0).
- `m-fs-clr` — `C7`→`C6` shrunk the `mov dword [r9],0` insn 7→3 B,
  leaving imm bytes decoding to `add [rax],al` → UC_ERR_MAP.
  Repointed to the imm byte `00`→`42` (writes `0x42` to the slot base
  — observable, same length).

## Limitations

- RES2 `00421FF0` and GATE `003E6F70` are scripted through EXP-108's
  stub layer — their returns are controlled and their calls traced;
  their own internals were executed real in EXP-108, not here.
- `sqrtf` is a stub returning `math.sqrt` — the single-precision
  result is bit-exact for the tested inputs; the stub does not model
  libm's edge-case flags.
- The actor record pool `q[0x022C6F28]`, slot pool `q[0x02B40528]`,
  gate/bone objects, `arg5` struct, and all scratch-block inputs are
  planted fixtures; their producers (the render pipeline, RES2's own
  pool) are outside this package.
- `bodies.json` holds body span + sha256 over shipped bytes;
  instruction-start coverage convention matches EXP-107–113.
