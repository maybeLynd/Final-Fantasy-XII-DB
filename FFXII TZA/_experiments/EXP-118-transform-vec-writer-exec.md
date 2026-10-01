---
experiment: EXP-118
title: Transform-vec writer — the three-arm get_vec 003E5B30 plus the gate/T51 helper 00422D50 and scan leaf 0041C970 executed real
contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md
method: B
live_game: false
tool: evidence/transform-vec-writer-exec/check.py
---
# EXP-118 — transform-vec-writer-exec

**Status:** complete · **26/26 functional cases, 22/22 mutants, stable
across three processes**
**Evidence:** `evidence/transform-vec-writer-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-117's limitations named the residual: `003E5B30` — the sibling
that calls `00422D50`/`0041C970`/`003E6DA0` — plus the
`00422D50 → 0051B9E0` and `00370E20` deep families. This package
executes that sibling: a **three-arm transform-vec writer**
`get_vec(record, field, out)` that produces a vec4 `{x,y,z,1.0f}` and
a word tag through three different resolution paths depending on the
requested field.

| VA | role | execution |
|---|---|---|
| `003E5B30` | GETV — the three-arm writer | **real** (338 B, 102 insns) |
| `00422D50` | G42 — record gate + codec resolve → T51 tail | **real** (57 B, 16 insns; second execution after EXP-109) |
| `0041C970` | G41 — `0xA0`-stride keyed-entry scan leaf | **real** (42 B, 13 insns) |
| `003E6DA0` | D6A — fallback's MIDS consumer driver | **real** (67 B, 22 insns; rerun in-tree after EXP-117) |
| `002ED570` | MIDS — handle+index middle resolver | **real** (146 B, 44 insns; rerun in-tree) |
| `003AB7F0` | RES — handle-mode dispatcher + result bound | **real** (99 B, 32 insns; rerun in-tree) |
| `0020E600` | BASE — arena codec base | **real** (10 B, 3 insns; rerun in-tree) |
| `0051B9E0` | T51 — G42's tail (deep resolver) | scripted boundary — EXP-109's scripted T51; args traced as `t51:rcx:rdx` |
| `0036B130` | RES's nonzero-mode resolver | scripted boundary — **executed real in EXP-084**; arg traced as `hres:` |
| `00370E20` | D6A's tail-call target | disclosed scripted boundary; arg traced as `e20:`; its return is the fallback's `p` |

All object/table/pool memory is planted fixture (disclosed): the
record, the T51-returned scan object with its `0xA0` entries, the
payload pointer's two embedded vec blocks, the `+0x400` field table,
and the MIDS/D6A contexts. Global inputs — `q[0x01F83530]` codec base
— are planted at real shipped addresses inside the mapped image.

## Measured semantics (native execution, not static reading)

**GETV `003E5B30(rcx=record, edx=field, r8=out) -> eax`:**

Arm 1 — `field == 0xb` (the material path, four chained resolves):

1. `obj = G42(record)`; `obj == 0` → fallback.
2. `sel = b[obj+0x328]`; `sel == 0` → fallback.
3. `entry = G41(obj, sel)`; `entry == 0` → fallback.
4. `ptr = q[entry+0x70]`; `ptr == 0` → fallback.
5. `mode = d[ptr+4] & 3`: `0 → base = ptr+0x30`; `1 → base = ptr+0x60`;
   `2`/`3` → fallback.
6. `out = {d[base+0x34], d[base+0x38], d[base+0x3C], 1.0f}`;
   `ret = w[base+0x30]` (movzx).

Arm 2 — the fallback (reached **only** from arm-1 null paths):

7. `p = D6A(record)`; `p != 0 → out = {d[p+0x4C], d[p+0x50],
   d[p+0x54], 1.0f}`, `ret = 0`; `p == 0 → out = {0,0,0,1.0f}`,
   `ret = 0`.

Arm 3 — `field != 0xb` (the record's own indexed table):

8. `ftab = q[record+0x400]` (the same field table FLDR resolves
   through in EXP-117); `ftab == 0` → zero-out.
9. `off = w[ftab+0xC]`; `off == 0` → zero-out.
10. `rdx = sx32(ftab + off)` (32-bit add, sign-extended);
    `rdx == 0` → zero-out.
11. `entry = rdx + field*16` (signed field; `rcx = r8*2` then
    `*8` → 16-byte rows); `out = {d[entry+4], f[entry+8],
    f[entry+0xC], 1.0f}`; `ret = w[entry]`.

Zero-out arm: `out = {0,0,0,1.0f}`, `ret = 0xFFFFFFFF` (`or eax,-1`).

**G42 `00422D50(rcx=record)`:** `d[record+0xC4] == -1 → 0`; else
`rcx = q[BASE(d[record+0x10]) + 0xDA8]`, `edx = d[record+0xC4]`,
tail-jmp `0051B9E0` — the gate dword doubles as the T51 index arg.

**G41 `0041C970(rcx=obj, edx=sel)`:** `cnt = sx16(w[obj+0x28])`;
`cnt <= 0 → 0`; else scan `obj+0x30 + i*0xA0` for `d[entry+0x80] ==
sel` → entry ptr or `0`.

**D6A/MIDS/RES/BASE:** unchanged from EXP-117's measured semantics
(rerun inside this tree — the `e20:` return becomes arm-2's `p`).

## Execution findings (beyond the static reading)

1. **Field `0xb` is a material-props arm with a four-deep resolve
   chain.** record →(gate+codec+T51)→ obj →(sel byte + keyed scan)→
   entry →(`+0x70`)→ payload →(`&3` mode)→ base. Every null hops to
   the D6A fallback — graceful degradation, not an error path: all
   six `arm1-*-zero`/`neg` cases produce the fallback's output.
2. **The payload carries exactly two embedded vec blocks** —
   `d[ptr+4]&3` selects `+0x30` or `+0x60`; modes 2/3 **fall back**
   rather than read further. `arm1-mode4` proves the mask is exactly
   `&3` (4 selects the `+0x30` block); the `&7` mutant is killed there.
3. **The fallback is field-`0xb`-specific.** `field != 0xb` never
   reaches D6A — it goes to the record's own `+0x400` table with a
   signed 16-byte-stride index. `arm3-negfield` (`field=-1`) reads
   `rdx-16` — the index arithmetic is `rcx = sx32(field)*16`, not a
   bound check.
4. **The return word distinguishes four outcomes.** material tag
   `w[base+0x30]` (arm 1) · `0` (arm 2, resolved or not) · row tag
   `w[entry]` (arm 3) · `0xFFFFFFFF` (arm 3 zero-out). A caller can
   tell "no field table" (`-1`) from "resolved through the fallback"
   (`0`) from a real tag.
5. **G42's gate dword is both sentinel and argument.** `d[+0xC4]==-1`
   short-circuits to `0`; any other value is passed verbatim as T51's
   `edx` — `t51:rcx:rdx` traces record `tctx:7` on `g42-ok`.
6. **Arm 3's table base is a 32-bit sum.** `rdx = sx32((ftab+off) &
   0xFFFFFFFF)` — the field table resolves through a dword add, and
   the `je` on the sum catches `ftab+off == 0` as a third null arm.

## Mutation campaign

22 byte-precise mutations, every site verified against shipped bytes
before patching:

- **GETV arm 1 (7):** field cmp `0xb`→`0xc` (arm 1 unreachable),
  sel disp `0x328`→`0x329`, entry-ptr disp `0x70`→`0x78` (reads the
  key's high bytes → `0` → fallback), `and eax,3`→`and eax,7`
  (mode 4 falls back — killed only on `arm1-mode4`), `cmp eax,1`→`0`
  (mode-1 base unreachable), `+0x60`→`+0x70` and `+0x30`→`+0x40` base
  displacements.
- **GETV arm-1 stores (3):** out.x source `+0x34`→`+0x38` (`x = y`),
  `1.0f` imm low byte → `0x3F800100`, ret-word disp `+0x30`→`+0x34`
  (returns the low half of out.x).
- **GETV fallback (1):** `+0x4C`→`+0x50` (out.x = out.y).
- **GETV arm 3 (5):** ftab disp `0x400`→`0x408`, off disp `0xC`→`0xE`,
  `add rcx,rcx`→`sub rcx,rcx` (field index → 0 — the real encoding
  is `48 03 C9`, the `03 /r` add form), z disp `+0xC`→`+0x10`,
  `1.0f` imm → `0x3F800100`.
- **G42 (3):** gate cmp `-1`→`0` (the `g42-neg1` case gains a `t51:`
  token instead of returning `0`), coff disp `0x10`→`0x14` (killed
  only with a nonzero `coff` — `g42-ok` plants `0x40`), ctx disp
  `0xDA8`→`0xDA0`.
- **G41 (3):** count disp `0x28`→`0x2A` (reads `0` → `jle` → `0`),
  key disp `0x80`→`0x88`, stride `0xA0`→`0xA8` (the scan walks past
  every real key).

**22/22 killed.** Two mutations needed discriminating fixtures:
`arm1-mode4` (a `d[ptr+4] = 4` payload that separates `&3` from `&7`)
and `g42-ok`'s `coff=0x40` (so the `+0x14` misread lands on a
different dword than `+0x10`).

## Limitations

- `0051B9E0` (T51) is a scripted boundary — it was also EXP-109's
  scripted T51; the deep resolver family below it remains open
  residual. Only its arguments (`t51:rcx:rdx`) and planted return are
  synthetic.
- `0036B130` is scripted inside RES but was executed real in EXP-084;
  `00370E20` (D6A's tail) is disclosed scripted — its planted return
  is arm-2's `p`. The `00370E20` deep family remains open residual.
- G42/D6A/MIDS/RES/BASE are re-executions — already proven real in
  EXP-109/117/084 — included here because GETV's tree calls them and
  byte-precise re-verification is free corroboration.
- The `b[obj+0x328]` selector byte is fixture-chosen; what writes it
  in the live object is upstream of this package's boundary.
- All object/table/pool memory is planted fixture; the executed code
  and `q[0x01F83530]` codec base are the real shipped bodies and real
  global address.
- `bodies.json` holds body span + sha256 over shipped bytes for all
  seven real bodies; instruction-start coverage convention matches
  EXP-107–117.
