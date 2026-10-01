# EXP-185 — `2FEF30` equip + license loops, nonzero; `322C50` bounds dispatcher

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the
exact shipping EXE, SHA256 73461D08…97f8). All callees (`322C50`,
`31E9A0`, `31E9F0`, `309440`, `20E600`) execute real — none scripted.

Harness: `Temp\exp166_check.py` — **244/244, stable ×3**.

## `322C50(kind, idx)` — bounds validator

32-case jump table at `0x323054` on `kind-1`; each case computes
`ecx`/`edx` bounds, tail is `edx <= idx <= ecx-1` (signed) → ret 1/0.

- Cases 2..5 (`0x2EBF130/120/150/100`): `ecx = d[desc+4]`, `edx = 0`.
- Cases 6..12,14..18 (`0x2EBF0F8/098/0F0/0E8/0E0/0D8/0D0/070/068/060/
  0C8/058`): `ecx = d[desc+4] + 0xN000`, `edx = 0xN000` (N = case-5);
  null desc → `ecx = 0xN000`.
- **Case 13 (`0x2EBF090/088/080/078`)**: `ecx = 0x8000 +
  d[090]+d[088]+d[080]+d[078]` — four concatenated tables share the
  0x8000 range.
- Case 19: fixed `ecx=0xEFFF`, `edx=0xE000`. Cases 22/23: `ecx=4`/`9`.
- **Case 1 re-dispatches**: `eax = 309440(idx)` → `(eax-1)<=u 0x1F` →
  jmp table again. `309440(id) = d[0x1EEBCF8 + (id>>12)*0x58]` —
  high-nibble → kind map; nibble>0xE → -1.
- kind 6 = equip desc `0x2EBF0F8`, range `[0x1000, 0x1000+count)`.

## Equip loop (`0x2FF3F0`, 5 slots)

`w[rbx+i*2]` where `rbx = r8 ?: rec+0x50`. `322C50(6, id)` gate →
row = `elemb + d[desc+0xC] + w[desc+8]*(id-0x1000)`.

- `31E9A0(row)` = class via `31E9F0`: `b[item+9]` → byte map
  `0x31EA74` (27 entries) → raw 1..9 → {raw1..5: cls1, raw6: cls2,
  raw7..9: cls3, else cls0}.
- **cls1** (gate `d[rsp+0x4C]`, =1 nonmember): `rsp+0xE8 += b[+0x1A]`
  →out+0xA; `rsp+0x24 += b[+0x1D]` →out+0xE.
- **cls2** (gate `q[rsp+0x70]`, =1 nonmember): `rsp+0x20 += b[+0x18]`
  →out+0xF; `rsp+0xD8 += b[+0x19]` →out+0x10 AND into out+0x12 sum.
- **cls3** (ungated): `rsp+0x34 += b[+0x18]` →out+0xB;
  `rsp+0x38 += b[+0x19]` →out+0xC.
- **Augment row** `aux = elemb + d[item+0x28]` (all classes):
  `w[aux]`→HP, `w[aux+2]`→MP, `b[aux+4..7]`→out+6..9,
  `d[aux+0xC]`→out+0x14, `d[aux+8]`→out+0x18,
  `b[aux+0x13/0x10/0x12/0x11/0x14]`→out+0x1C/1D/1E/1F/20 (OR).
- Invalid id (outside range) → whole item skipped incl. augment —
  proven: slot4 id 0x1400 with count 0x40 → no contribution.

## License loops (desc `0x2EBF040`)

`rdi = q[rsp+0xD0]` = the callee's rcx-home slot — the function stores
`rcx` there at `0x2FEF35`, so the bitmap base IS `rec`. Boards:
`b[rec+0x68+i]` (A) and `b[rec+0x78+i]` (B); either grants.

- **T1** `0xD10290` 16 ids `{0x40-44,0x23,0x2A-2F,0x3C-3F}` → r12/out+6.
- **T2** `0xD102A0` 16 ids `{0x45-49,0x13,0x16,0x18,0x1A,0x57,0x61-66}`
  → r13/out+7.
- **T3** `0xD102B0` 12 ids `{0x4A-55}` → r14 = **HP** — the +HP
  license augments.
- Per set bit (id>>3 byte, 1<<(id&7) bit, either board):
  `accum += w[elemb+d[desc+0xC] + w[desc+8]*id + 4]`.
- Proven both boards: 0x40/0x57/0x4A on A, 0x23/0x61/0x55 on B.
  Same licid shared across tables (e.g. 0x8C in T1 twice + T2 + T3 —
  left unset).

## Output merge map (final)

- `b[out+0x11]` = `rsp+0x54 + rsp+0x20 + rsp+0x24 + rsp+0x50` (cap 100)
- `b[out+0x12]` = `rsp+0x58 + rsp+0xD8` (cap 100)
- `d[out]` HP = `[1, cap]` where cap = `b[rec+5] ? 0x3B9ACA00 : 9999`,
  then optional `0x7FFF` re-clamp (`rsp+0x5C`, b4∈[0x1B..0x27]) on the
  RAW accum — can exceed 9999.
- Verified: HP `72+1000+52 = 1124`; MP `8+100 = 108`; out+9 clamp
  `118→99`; out+0x11 `0x42+7+6 = 79`.

## Corrections

- EXP-183's "static tables `0x1DF0290`" was the same RIP-slip class —
  real tables `0xD10290/2A0/2B0`.
- Class-1/class-3 arm fields were swapped in the first fixture draft;
  cls1 = +0x1A/+0x1D, cls3 = +0x18/+0x19 (disasm re-read).
- The `31E9F0` map is at `0x31EA74` (not `0x1DFEA74`).
- Tail (`0x2FF970+`): member + `rsp+0x64` (rdx-null path only) +
  immunity-mask `0x8000020` change → `3105D0(unit)` + `q[+0x6F8]=0` —
  in-place recompute arm, inactive under rdx-out fixtures. Disclosed.
