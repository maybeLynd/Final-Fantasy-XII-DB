# EXP-262 — `0051BA40`/`0051F240` mode-0 and `&2` arms + `0041CF00` block loop / `0x1000` arm

**Status:** complete — **577/577 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 prefix `1d1a86bf`;
577 cases), fault census 26** (the 24 from EXP-261 plus the new pinned
`0x37228D` null dereference — one `mem` + one `uc` stop record).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the existing `dcntr`/`c2` fixtures;
nothing claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..261).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes, new `d422c20-*` cases)

`0051F240(container, slot)` mode dispatch — `d[C+4] & 3`:

```
mode == 0: desc = 3AB7F0(q[C+8]) + (zx(slot) * 3) * 0x10
mode == 1: desc = q[C+8] + (zx(slot) * 3) * 0x10
otherwise: ret 0
if b[desc] & 2:
    q[desc+0x18] = sx(3AB7F0(q[desc+0x10]) + d[desc+0x20])
ret q[desc+0x18]
```

So mode 0 resolves the *array base* through the tagged-pointer
resolver while mode 1 uses `q[C+8]` directly — both then stride by
`slot * 0x30`. The `&2` descriptor flag is a *lazy record pointer*:
the true record base is `q[desc+0x10] + d[desc+0x20]`, re-resolved
and **stored back** into `q[desc+0x18]` on each lookup (overwriting
whatever caller-planted pointer was there).

`0041CF00(record)` — the reset called by `0051BA40` before release:

```
ecx = 0; r8d = 0
while r8d < sx(w[R+0x28]):               # r8d counts; cx stays 0
    rdx = R + 0x38 + i*0xA0
    d[rdx-8]   = -1          w[rdx-4]   = cx        # always 0
    q[rdx]     = 0           q[rdx+8]   = 0
    d[rdx+0x10]= 0x1E0000    d[rdx+0x18]= 0x41F00000
    q[rdx+0x40]= 0
    w[rdx+0x48]= -1          w[rdx+0x4A]= -1
    q[rdx+0x58]= 0           d[rdx+0x60]= -1
    q[rdx+0x68]= 0           q[rdx+0x70]= 0
    d[rdx+0x84]= d[rdx+0x80]                       # copy
    w[rdx+0x8E]&= 0xFF7F
if d[R+0xC] & 0x1000:
    rcx = d[R+0x338] == -1 ? 0 : 2ED570(q[R+0x330], d[R+0x338])
    372280(rcx)                                     # unguarded on 0
    d[R+0xC] &= ~0x1000
jmp 41CB90   # tail reset (~0x390 bytes, no calls)
```

Correction of record (minor): the `w[blk+4]` field is **not** the
iteration counter — it stores `cx`, the pre-loop `ecx`, which is
xor'd to 0 and never written inside the loop (`r8d` is the real
counter, only compared). EXP-262 pins `w[blk+4]==0` on both blocks.
`0041CB90`'s own writes cover `+0x0..+0x2C` and `+0x2B0..+0x388`
(plus a `.data` table at `02CA4410`) — they do **not** touch
`+0x30..+0x2AF`, so the block loop's writes survive into the final
state. `0041CB90` also retires the record's own container handle:
`q[R+0x330]=0`, `d[R+0x338]=-1` — after the `0x1000` arm consumed
them.

`00372280(elem)` — the `0x1000` arm's second-level walk:

```
rdi = 20E600(d[E+0x84])                 # 0x290-array base
r9  = rdi + sx(w[E+0x88]) * 0x290       # word list lives inside it
if rdi == 0 or r9 == 0: ret
for i in w[E+0x8A]:                     # sign-checked word loop
    w = sx(w[r9]); r9 += 2
    row = rdi + w * 0x290
    w[row+0x280] &= ~0x10
    q[row+0x1A4] = 0       d[row+0x1A0] = 0     d[row+0x1AC] = 1.0f
    q[row+0x1C4] = 0       d[row+0x1C0] = 0     d[row+0x1CC] = 1.0f
```

The word list is embedded in the same `0x290`-stride array it
indexes (`r9 = base + w[E+0x88]*0x290`, entries at `+2` steps).

## Cases and pins

- **`d422c20-c4ind`** — `b[desc]&2` set: `q[desc+0x10]`=`r2-0x20`,
  `d[desc+0x20]`=`0x20` → `q[desc+0x18]` overwritten to `r2`; the
  reset signature lands on `r2`, the planted `R1` keeps `d[R1]==7`,
  and `51F190` releases desc `A[d[r2]]` = `A[2]` — the release key
  comes from the *re-resolved* record, not the planted desc link.
- **`d422c20-mode0`** — mode 0 routes `q[C+8]` through `3AB7F0`
  before indexing; a direct aligned base resolves to itself and the
  downstream pop/reset/release is identical to mode 1.
- **`d422c20-mode3`** — `d[C+4]=3` → `51F240` ret 0 → same skip as
  mode 2; `d[+0xC4]`/`w[+0xCC]` still retire (the retire belongs to
  `00422C20`, not the container).
- **`d422c20-c4rows`** — `w[R+0x28]`=2 → two `0xA0` blocks reset at
  `R+0x30`/`R+0xD0`. Pinned: `d[blk]==-1`, `w[blk+4]==0` (the
  cx-store, not a counter), `d[blk+0x10]`=`0x1E0000`,
  `d[blk+0x18]`=`0x41F00000`, `w[blk+0x48]/+0x4A]`=-1,
  `d[blk+0x60]`=-1, the `d[blk+0x80]→d[blk+0x84]` copy preserves
  planted sentinels, and `w[blk+0x8E]` clears bit 7 (`0xFF→0x7F`).
- **`d422c20-c4rc2`** — `d[R+0xC]`=`0x1000` with `q[R+0x330]`=record
  container C3, `d[R+0x338]`=0 → `2ED570(C3,0)` resolves `e3` →
  `372280(e3)`: `d[e3+0x84]`=`0x74000` list/array base, `w[e3+0x88]`=0,
  `w[e3+0x8A]`=1, `w[list]`=1 → row `elemb+0x74290` cleared
  (`w[+0x280]&=~0x10`, the four zeros, both `1.0f` writes — all
  pinned over planted sentinels); C3's resolved bases stored at
  `q[C3+0x38]`/`q[C3+0x10]`; `41CB90` then retires `q[R+0x330]`/
  `d[R+0x338]`.
- **`d422c20-c4f0`** — `d[R+0x338]`==-1 → rcx stays 0 →
  `372280(0)` reads `d[0x84]` — **unguarded null deref**, pinned by
  `expect_fault=0x37228D`. No page-0 fixture; `00422C20`'s
  retire/clear writes never run on this path (asserts skipped).

## Not claimed

- `0051BA40`'s `edx==-1` / `0051F080` / `0041D220` deep arms,
- `0051F240`'s mode-0 **tagged** array base (only a direct base was
  exercised — `3AB7F0` handle resolution is covered by EXP-260),
- `00372280`'s null-base early-outs and multi-entry word lists,
- live reachability of the `d[R+0x338]==-1` crash arm (callers'
  contract, not the callee's semantics),
- `005369C0`/`003B02A0` real — `NATIVE-REPLAY`, `live_game: false`.
