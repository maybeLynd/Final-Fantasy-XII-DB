# EXP-219 — kind-`0x1C` nested catch-all `2AEB20` + emit internals `17FC90`/`17F7C0`/`2DD860`

**Status:** complete — **525/525 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`c7d7db08aed4278af631b68fa4f8848e7833aefb16e3034bcd2e82d48f5095dd`),
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..218; 525 cases, none new — promotion round)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `002AEB20` | the kind-`0x1C` nested catch-all (462 insns) — the `2AC5F0` `0x1C` arm's worker: `b[cursor]-0x40` = sub-kind; `≥0x20` → `2AB8F0` 12-entry jump-table flag lookup; `esi` = `b[+1]>>1&1`; `edi` seeded from `b[q[0x1F7FFE0]+0x38]` (`1E0C10`) then forced 1 when the sub-kind matches the 5-dword const table; `edi!=0` → two `1E0C30` mode reads (`d[q[q[0x2EA5368]+0xDF8]+0x10]`) picking byte table `0x9165F0`/`0x916670` (`[ebx*4 + ((d[0x208F574]>>4)&3)]`), `edi==0` → `d[0x22C7F84]`/`228480` gates into byte tables `0x1EECE10`/`0x1EECE30` — all four resolve a sprite-record index into the `q[0x209CC40]` ctx object's `+idx*24` record slots; `d[rec]>>2` = entry count, `q[rec+0x10]` = entry-ptr array; the pre-loop publish block reads `arr[cnt-1]` → `f[0209CC60]`/`f[0209CC64]`/`f[0209CC68]` (hi×x-scale, h×y-scale, +`f[e312+0x4C]`); loop emits `cnt-1` quad command records at `q[0209CC50]`, stride `0x70` (`q[+8]=6`/`q[+0x18]=6` headers, attr qword mix, RGBA from `copy+0x30..0x33`, float coords, UV lo12/hi12 pair, col/row at `+0x60`/`+0x64`), calling real `17FC90`, `2DD860`×2, `2DD8B0` and the scripted `181xxx` device tail per entry; `d[ctxo+0x10D4]!=0` mid-loop flush gate, then unconditional `2B4730(1)` tail flush; returns `eax=2` consumed. |
| `0017FC90` | glyph-quad UV/scale write (22 insns): saves xmm6..9, `1B5FA0()` → `q[0x1F811F8]` device object, `1E9C40(dev, xmm1..3, [rsp+0x28] scale)` → `f[dev+0x137C..0x1388]` = the four scaled products. Now real on every `2A9F00` quad build and inside `2AFDC0`/`2AEB20`. |
| `001E9C40` | `1B5FA0`'s write leaf (11 insns): `f[dev+0x137C]=xmm2*xmm3`, `+0x1380`=xmm1*xmm3, `+0x1384`=xmm2*scale, `+0x1388`=xmm1*scale. |
| `001B5FA0` | 2-insn singleton getter: `return q[0x1F811F8]`. |
| `0017F7C0` | glyph emit (30 insns): `rcx!=0` → copies a `0xA0`-byte matrix/state block to its frame, `1B5FA0()` → device, `1E8070(dev, &copy)` — the deep transform apply stays scripted (`s1e8070`). Now real on every `2A9F00` glyph emit. |
| `002DD860` | quad-corner emit (20 insns): writes `f[rcx]=xmm3`, `f[rcx+4]`=stack arg, then `202B70(out=rdx, mat=r8, in=rcx)` → `217060` → projective divide `f[rdx..+4] /= f[rdx+0xC]`. |
| `00202B70` | out-param wrapper (10 insns): `217060(&stk, mat, in)` → `movups [rcx]` copy-back. |
| `00217060` | 4×4 matrix-vector transform leaf (56 insns, no calls): `out = mat × in` row-major float math. |

Bounded helpers that now run raw-real inside `2AEB20` (all leaf/2-insn
BSS getters): `1E0C10` (`b[q[0x1F7FFE0]+0x38]` via `198790`),
`1E0C30` (`d[q[q[0x2EA5368]+0xDF8]+0x10]` via `796E20`/`225680`),
`2AB8F0` (76-insn kind→flag jump table over `w[0x1CCF2A0]`-family
globals), `2DDC50` (`53DD10` constant-1 → `eax=1`), `180150`
(`b[0x1F811E0]` flag byte), `228480` (`q[0x1FD4949]!=0` flag),
`2441E0` (`q[0x208EAB8]` getter).

## New scripted boundary (disclosed)

`001E8070` — `17F7C0`'s deep transform apply (279 insns, calls
`1E7A20`/`1E94E0`/`225690`/`79E3C0` into the device/graph subtree).
Scripted sink `s1e8070` records `(dev, &matrix_copy)` args.

## New fixtures

- `dev1` = `q[0x1F811F8]` → 0x1400 buffer (receives `1E9C40`'s
  `+0x137C` UV/scale writes); planted unconditionally.
- `dev2` = `q[0x1F7FFE0]` → 0x40 buffer; `b[dev2+0x38]` = `edi` seed.
- `emat` (opt-in): `q[e312+0x20]` → identity 4×4 matrix — the transform
  `2DD860`→`217060` consumes. **Opt-in because `q[state+0x20]!=0` is a
  semantic gate** — `c5f0-tag2` asserts the `0x20`-tail stays skipped.
- `eb20t` (`c5f0-f42`): `q[0x2EA5368]`→`o1`→`q[o1+0xDF8]`→`o2` with
  `d[o2+0x10]=2` (selects byte table C → index `edx=1` → `ctxo+0x18`
  record); record `d=8` (count 2), `q[rec+0x10]`→`arr`→`{ent,ent2}`;
  `ent` carries `w10/w12/wA/wC/wE/b39/q+0x20=ptab`; `ent2` carries
  `w10b/w12b` for the publish globals; `sprt`-style `t`/`r` with
  `w[r+0x42]` byte-base, `b[r+0x30]` pair index, `q[t+0x30]` attr.

## Corrections of record

- **`2AEB20` returns `eax=2`**, not the scripted `eb20n=3` — the
  `0x1C`-arm caller does `q[ccp] += movsxd(eax)`, so the real cursor
  advance is +2 (`nstr+3`), not +3. The stub model overstated consumed
  by 1.
- **Three singleton cells re-verified by exact RIP-relative decode:**
  `1E0C10`'s getter reads `q[0x1F7FFE0]` (not `0x1F811E0` — off by
  `0x400` in the earlier estimate) and `1E0C30` reads `q[0x2EA5368]`
  (not `0x2AEE868`). The first live run faulted on `b[0x38]` with a
  null dev2 — resolved by planting the correct cell.
- **`q[e312+0x20]` (matrix ptr) is load-bearing as a null gate** —
  planting it unconditionally flipped `c5f0-tag2`'s "state+0x20 null →
  skip tail" assertion (the `17F850`/`17FA10`/`2AB820`/`17FB00` block
  ran). The `emat` fixture is opt-in; `tag2` retains null.
- **The publish globals come from `arr[cnt-1]`** (the *last* entry),
  not the emitted head — the loop emits `arr[0..cnt-2]` while the
  pre-loop metric block reads the tail entry. `ent2` carries distinct
  `w10b`/`w12b` so the asserts prove it.
- **`2AEB20`'s record stride is `0x70`** (0x40 quad + 0x20 col/row +
  header block at `cursor+0x50` store-back), and the record index
  byte-table indexing is `tab[ebx*4 + ((d[0x208F574]>>4)&3)]` on the
  `edi=1` path — the flag dword `d[0x208F574]` selects sub-columns.

## Assert coverage added for `c5f0-f42`

`byr` counts: `eb20`×1, `fc90`×1, `dd860`×2, `dd8b0`×1, `e0c30`×2,
`bb00`×1, `b4730`×1, `cookie`≥1; scripted sinks `s181560`/`s1819a0`/
`s181870`/`s181460`/`s1816b0`/`s181910`/`s181330` each ×1; publish
globals `cc60=48` (`8*6`), `cc64=32` (`4*8`), `cc68=53` (`48+f4C=5`);
record headers `q[+8]=q[+0x18]=6`, attr mix `0x0123450001300000`,
RGBA `0x11/0x22/0x33/alpha`, col/row `5`/`7`, scale-flag=1, UVs
`48.0`/`64.0`; post-flush `q[0209CC48]=0x2EBEFD8`, `d[02EBEFF0]=1`,
cursor `nstr+3`, `d[params]=1`, `b[ctxo+0x10FC]=1`, `b[e312+0xA9]=0`.

## Remaining scripted boundaries (unchanged class)

`1E8070` transform apply, `181560` + six `181xxx` device wrappers
(`q[0x1F811E8]` render-device object unplanted — `1B2410`'s
`dev+0x3930` write region not modeled), `17Fxxx` font-shim thunks,
`2AC2F0` decoder, `3FFDF0` param parser, `254A10`, `39C4A0`'s record
contents beyond the fixture, `861EC0` memset hook.

## Next candidates (EXP-220+)

- `1E8070` + the `17Fxxx` thunk family — needs the `q[0x1F811F8]`
  device's method layout mapped (279-insn body, `1E7A20`/`1E94E0`
  subtrees).
- The `181xxx`/`1Bxxxx` render-device subtree — needs a planted
  `q[0x1F811E8]` device object (`+0x3930` write region, method vtable).
- `2AC2F0` decoder — the remaining scripted interpreter boundary on
  the measure/publish paths.
- Next member-block carrier.
