---
experiment: EXP-117
title: Slot-handle algebra — the `(gen<<8)|idx` allocator 003B56D0 plus the RES/MIDS/D6A resolver family executed real over the 0xE0 pool at q[02B40528]
contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md
method: B
live_game: false
tool: evidence/slot-handle-algebra-exec/check.py
---
# EXP-117 — slot-handle-algebra-exec

**Status:** complete · **30/30 functional cases, 25/25 mutants, stable
across three processes**
**Evidence:** `evidence/slot-handle-algebra-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The `0xE0`-stride slot pool at `q[0x02B40528]` is the same pool whose
consumer bodies ran real in EXP-113/114 — but only from the read side.
EXP-109 left thirteen callees UNKNOWN on the contract's row-550 ledger;
six of those were later executed (`0041F730`, `00426EC0`, two helpers
in EXP-108/109) and EXP-084's EFX package had already run
`003AB7F0`/`0036B130`/`0020E600`. What had never executed anywhere was
the **allocation side**: the function that issues the `(gen<<8)|idx`
handles those consumers check, plus the middle-resolver family that
turns a context handle + index into an arena pointer.

This package executes that algebra end to end:

| VA | role | execution |
|---|---|---|
| `003B56D0` | HID — slot allocator + handle issuer | **real** (444 B, 96 insns) |
| `003E5AD0` | FLDR — per-record word-field resolver | **real** (88 B, 25 insns) |
| `003AB7F0` | RES — handle-mode dispatcher + result bound | **real** (99 B, 32 insns) |
| `002ED570` | MIDS — handle+index middle resolver | **real** (146 B, 44 insns) |
| `003E6DA0` | D6A — MIDS consumer driver | **real** (67 B, 22 insns) |
| `0020E600` | BASE — arena codec base (`rax = rcx + q[01F83530]`) | **real** (10 B, 3 insns) |
| `0036B130` | RES's nonzero-mode resolver | scripted boundary — **executed real in EXP-084**; boundary arg traced as `hres:` |
| `00370E20` | D6A's tail-call target (deep, ~85 insns / 6 calls) | disclosed scripted boundary; arg traced as `e20:` |

All pool memory is planted fixture (disclosed): the `0xE0` pool, the
`0x740`-stride record pool at `q[0x022C6F28]` (the same pool/gate pair
EXP-113/114 exercised), the per-record field table, and the MIDS/D6A
context objects. Global inputs — `q[0x02B40528]` pool base,
`d[0x02B40520]` generation counter, `q[0x022C6F28]` record pool,
`q[0x01F83530]` codec base — are planted at their real shipped
addresses inside the mapped image.

## Measured semantics (native execution, not static reading)

**HID `003B56D0(ecx=arg)`** — the allocator:

1. Scans the pool `rbx = q[0x02B40528]` for the first slot with
   `b[slot+0x40] & 1 == 0`; `edx` counts to `0xA0` — a full pool
   returns `0` (early-out arm at `003B5707`).
2. Reads `d[0x02B40520]`, increments, clamps `>0xFFFFFF → 1` via
   `cmova`, stores back, then `handle = (gen << 8) | slot`.
3. Stamps the record: `d[+4] = edi` (the arg), `d[+0x10] = handle`,
   `b[+0x40] = (old & 0x81) | 1` (occupied while preserving the old
   byte's bits 7 and 0), `w[+0x41] = b[+0x43] = 0`, fourteen `1.0f`
   lanes (`+8 +C +14 q +2C +44 +58 +5C q +78 q +88 +8C q +94 q +C8
   +CC q +D4`) and eleven zero fields — the full map is byte-compared
   by the model.
4. Resolves the parent record **twice** (identical resolve before each
   field pull): `index = sx16(arg)`; `-1 → rcx=0`; else
   `rcx = q[0x022C6F28] + index*0x740` and `d[rcx+0x284] == 0 → rcx=0`
   — the same `+0x284` gate the EXP-113/114 consumers check.
5. `w[+0x3C] = FLDR(rcx, 0x104)`; `w[+0x3E] = FLDR(rcx, 0x106)`;
   `w[+0x38] = w[+0x3C]`; returns `d[+0x10]` (the handle).

**FLDR `003E5AD0(rcx=record, edx=field)`** — a leaf word resolver:
`r8 = [rcx+0x400]`; `edx < 0x20 → w[r8 + w[r8+2] + edx*2 + 0x14C]`;
`edx == 0x104/0x105/0x106 → w[r8+0x3A/0x3C/0x3E]`; else `0xFFFF`.

**RES `003AB7F0(rcx=handle)`** — dispatcher + result bound:
`rcx==0 → 0`; `dl & 3 == 0 → passthrough` (returns the input — a
direct pointer); **any nonzero mode → `0036B130`** (the `setne`/`cmp 1`
pair can only yield 0/1, so modes 1, 2 and 3 all route there);
then `movsxd rcx,eax; cmp rcx,0x40; cmovbe rax,0` — resolver results
whose low dword is unsigned-`≤ 0x40` are treated as failures and
returned as `0`.

**MIDS `002ED570(rcx=ctx, edx=idx)`** —
`if [ctx+0x30] → [ctx+0x38] = RES(it)` and
`if [ctx+8] → [ctx+0x10] = RES(it)` (the deposits are **skipped** on
null fields, not zeroed); `elem = [+0x38] + sx32(idx)*16`;
`row = [+0x10] + (sx32(idx) >> [ctx+0x4C]) * 32`; `d[elem] == -1 → 0`;
else `rcx = BASE(d[row+0x10])` and return
`rcx + cdqe((d[ctx+0x50] & esi) * d[ctx+0x48])` — the product is
computed in `eax` and **sign-extended** into `rax`.

**D6A `003E6DA0(rcx=ctx)`** — `idx = d[ctx+0x18]`; `-1 → 0`
(checked **twice** — before and after the BASE call);
`rcx = q[BASE(d[ctx+0x10]) + 0xD98]` → `MIDS(rcx, idx)`;
nonzero → tail-jmp `00370E20(result)`; else `0`.

## Execution findings (beyond the static reading)

1. **The handle's low two bits are the slot index mod 4.** Since
   `handle = (gen<<8)|slot`, RES sees `slot&3`: slots `≡0 (mod 4)`
   passthrough as *pointers* (returning the handle itself as a
   resolved value), `≡1/2/3` all route to `0036B130`. The earlier
   static read claimed modes 2/3 returned `0`; execution shows the
   `cmp ecx,1` arm is unreachable-by-construction for `ecx>1` — the
   `xor eax` arm at `003AB81E` is dead code.
2. **RES applies a result-validity bound the docs missed.**
   `0036B130`'s return is filtered: `sx32(eax) ≤ 0x40` (unsigned)
   → `0`. `res-hres-low` plants `0x30` and gets `0`;
   `res-hres-neg` plants `0x80000000` — sign-extended to a huge
   unsigned value — and gets it back verbatim.
3. **`arg = -1` is a crash path in the shipped code.** Both parent
   resolves substitute `rcx=0` and FLDR dereferences `rcx+0x400`
   unconditionally — `alloc-neg1` and `alloc-gate0` produce the
   unmapped-read fault at `0x400` after the slot is already stamped
   (the handle is written before the resolve; the post-FLDR tail
   never runs). The allocator only works with a live parent record.
4. **The gen counter clamps, not wraps.** `gen+1 > 0xFFFFFF → 1`:
   `alloc-gen-wrap` (`gen=0xFFFFFF`) yields handle `(1<<8)|slot`;
   `alloc-gen-edge` (`gen=0xFFFFFE`) yields `0xFFFFFF` unclamped.
5. **MIDS deposits are conditional, not cleared.** Null `+0x30`/`+8`
   fields skip their RES call entirely — a stale `+0x38`/`+0x10`
   survives the call; the fixture plants `0` so both agree, but a
   reimplementation that zeroes them diverges.
6. **The product is signed.** `cdqe` sign-extends the 32-bit
   `(mask&idx)*mult` before the base add — `mids-negprod` (`0xFFFF ×
   0x10000 → eax=0xFFFF0000`) returns `base − 0x10000`, not
   `base + 0xFFFF0000`.
7. **D6A guards `-1` twice.** `cmp ebx,-1; je` appears both before
   and after the BASE call — a single-site mutation of either guard
   stays unobservable on `idx=-1`; the discriminating case is
   `idx=0`, where mutating the first `cmp` to `cmp ebx,0`
   short-circuits a valid index.

## Mutation campaign

25 byte-precise mutations, every site verified against shipped bytes
before patching:

- **HID (12):** occupancy `test` mask `01`→`02`, slot cap `0xA0`→`0xA1`
  (allocates one past the pool — observable in the returned handle),
  clamp imm `0xFFFFFF`→`0xFFFFFE` (killed only on the `gen+1 ==
  0xFFFFFF` edge), `cmova`→`cmovbe`, `shl 8`→`9`, `or`→`and` slot bits,
  flag mask `and 0x81`→`or 0x81` (preserves flag bit1 — killed on the
  `0x02`-flagged free slot), `or al,cl`→`and` (slot never marked —
  second alloc reuses it), arg store `+4`→`+8`, handle store
  `+0x10`→`+0x18` (return reads the untouched field → `0`), gate disp
  `0x284`→`0x288` (reads a zeroed dword → `rcx=0` → the `0x400`
  fault), field id `0x104`→`0x105` (wrong name-table word).
- **RES (4):** `test dl,3`→`test dl,7` (killed on `low3=4` —
  passthrough vs handle-resolve), `cmp ecx,1`→`2` (mode-1 arm dead),
  `setne`→`sete` (mode inverted — a pointer routes to `0036B130`),
  hres result bound `0x40`→`0x20`.
- **MIDS (5):** element `shl 4`→`5` (killed only when the `edx*32`
  element holds `-1`), `sar`→`shr` (negative index → wild row →
  fault), record `shl 5`→`4`, `and`→`or` mask, mult disp `0x48`→`0x4C`
  (reads the shift count as the multiplier).
- **FLDR (2):** index bound `0x20`→`0x10`, field `+0x3A`→`+0x3C` disp.
- **D6A (1):** first `cmp ebx,-1`→`cmp ebx,0` — killed on `idx=0`
  (the double guard makes any `idx=-1` single-site equivalent).
- **BASE (1):** rip-relative displacement `+4` — the codec base reads
  a shifted qword.

**25/25 killed.** Seven mutations needed discriminating cases built
specifically for them: `alloc-bit2-flag` (a free slot whose flag byte
carries bit1), `alloc-gen-edge` (`gen+1 == 0xFFFFFF` exactly),
`res-low4`, `res-hres-low`/`res-hres-neg` (the result bound),
`mids-stride-gap` (the shifted element is `-1`), `mids-neg`
(sar/shr split), `d6a-zero` (the double `-1` guard).

## Limitations

- `0036B130` is a scripted boundary **inside** RES — but it was
  executed real in EXP-084 (`efx-source-rebase`), so RES's full call
  tree is proven real; only the planted per-case return is synthetic
  here. The `hres:` token records each call's argument.
- `00370E20` (D6A's tail) is disclosed scripted — ~85 insns / 6 calls
  deep; the `e20:` token records the pointer D6A hands it.
- All pool/table/context memory is planted fixture; the executed
  code, the scanned flags, the generation counter, and both pool
  bases are the real shipped bodies and real global addresses.
- `003E5B30` — the sibling that calls `00422D50`/`0041C970`/
  `003E6DA0` — is **not** in this package's call tree (earlier census
  mis-attributed those calls to `003E5AD0`'s tail; they belong to the
  next function). The `00422D50`→`0051B9E0` and `00370E20` deep
  families remain open residual.
- `bodies.json` holds body span + sha256 over shipped bytes for all
  six real bodies; instruction-start coverage convention matches
  EXP-107–116.
