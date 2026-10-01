---
experiment: EXP-109
title: Render-record pool lifecycle — six free functions (004269A0 / 004278E0 / 004279B0 / 00428710 / 00427C90 / 00429140) under isolated original execution
contract: ../17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md
method: B
live_game: false
tool: evidence/render-pool-lifecycle-exec/check.py
---
# EXP-109 — render-pool-lifecycle-exec

**Status:** complete · **45/45 cases, 79/79 mutants, stable across three
processes**
**Evidence:** `evidence/render-pool-lifecycle-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-render-record-pool-lifecycle` listed six remaining unexecuted
operations on the render-record pool `q[0x022C6F28]` (160 records ×
`0x740`, list tail at `+0x48800`). This experiment executes all six
shipped bodies — plus the full shallow callee cone — under Unicorn and
diffs them against an independent index/link model on return values,
list heads/tails, `live`/`nextFree`, record link/flag/image bytes,
boundary-call traces, and external table side effects.

| VA | role | execution |
|---|---|---|
| `004269A0` | CTOR — pool constructor | **real** (741 B) |
| `004278E0` | LKUP — lookup by name | **real** (208 B) |
| `004279B0` | ALOC — pending-record allocate | **real** (329 B) |
| `00428710` | PROM — pending→active promote | **real** (403 B) |
| `00427C90` | RETI — retire flagged actives | **real** (328 B) |
| `00429140` | RELE — release | **real** (358 B) |
| `0041F730` | CLR — `0x740` reset/default writer | **real** (1208 B) |
| `006C0520` | F4W — float4 default writer | **real** (26 B) |
| `0046D110`→`00202C70` | CPY — `0x40`-B const copy from `0x1F204E0` | **real** (12+31 B) |
| `003E5D00` | A8W — array default writer | **real** (44 B) |
| `003E37E0` | Z50 — `memset(0x580,0,0x50)` thunk | **real** (11 B) |
| `0020E600` | BASE — `ecx + q[0x1F83530]` | **real** (10 B) |
| `0020E620` | BAS2 — `ecx − d[0x1F83530]` | **real** (9 B) |
| `0041D6C0/D0/E0` | T1W/T2W/T3W — name-table writers | **real** (15/15/8 B) |
| `00426EC0` | DRAIN — child-chain unlink | **real** (216 B) |
| `003B6000` | HC1 — slot-table enable clear | **real** (27 B) |
| `003AFBE0` | HC2 — handle-table id clear | **real** (35 B) |
| `003E68E0` | G68 — `q[rec+0x400]` gate | **real** (40 B) |
| `00422D50` | L2D — `d[rec+0xC4]` gate | **real** (57 B) |
| `003B6890` | SLTI — slot-table init (`0x2B40528`) | **real** (110 B) |
| `003AFCD0` | HTI — handle-table init (`0x2B3F570`) | **real** (45 B) |
| `004778A0` | T3I — `0x40`-stride table init | **real** (46 B) |
| `003AF2B0` | T4I — table init | **real** (102 B) |
| `0042F000` | T5I — table init → E0720 | **real** (33 B) |
| `003B53C0` | S53 — globals init | **real** (119 B) |
| `003E0720` | E0720 — init tail (S512+D40 calls) | **real** (18 B) |

Scripted boundaries (entry-intercepted, args captured, planted returns):
`00420480` RINIT, `0041FCF0` PTD, `003B56D0` HID, `0042C410` PHOOK,
`004200A0` TDOWN, `0042F4C0`, `003E56A0`, `002ED570` MIDS, `0051B9E0`
T51, `00512EF0`, `0040DB70`, `0032E400/620/520`, allocator trio
`0036C1D0/0036A100/0036C140` (unplanted-table paths only), `00861EC0`
memset thunk (implemented as a real byte-fill — its writes ARE the
semantics).

## Measured semantics (native execution, not static reading)

### CTOR `004269A0()`

```
for i in 0..0x9F: 0041F730(pool + i*0x740)          ; reset image
hAct=tAct=-1; nextFree=live=0 (qword); hPend=tPend=-1
lea rcx = 0x1F000A0 -> T3W                          ; name-table 3 reg
T2W(5) -> q[0x2CA4670] = 0x520C50                    ; name-table 2 reg
T1W(i) for i in 0x11..0x48 -> q[0x2CA4410+i*8]      ; name-table 1 reg
tail +0x48840..0x4886C config writes
SLTI/HTI/T3I/T4I/T5I/S53 inits (global writes real;
  E0720's S512+D40 calls and S53's E400/E620/E520 calls scripted)
+0x48818 |= 5 ; +0x4881C = 34.0f ; +0x48824 = 4.0f ;
+0x48828 = 0x3E2AAAAB (epoch, ~0.16667)
ret = pool
```

### LKUP `004278E0(rcx = name)`

```
for i in active chain (hAct, +4 links):
    if b[rec+0x290] & 2: continue            ; retired/hidden SKIP
    if name_eq(rec+0x1C, rcx): ret w[rec]
for i in pending chain (hPend, +4 links):    ; NO flag gate
    if name_eq(rec+0x1C, rcx): ret w[rec]
ret -1
```

### ALOC `004279B0(rcx = name, rdx = buf1, r8 = buf2, r9d = flags)`

```
LKUP(name) != -1 -> ret 0
live >= 0xA0     -> ret 0
i = nextFree ; CLR(rec_i)
if hPend == -1: hPend = i ; w[rec+2] = -1
else: w[tPend*0x740+pool+4] = i ; w[rec+2] = tPend
tPend = i ; w[rec] = i
RINIT(rec, name, buf1, BASE(d[+0x48830]),
      stack: orig r8d, orig r9d)            ; scripted
d[rec+0x290] |= 1 ; live++
nextFree = live >= 0xA0 ? 0 :
    first j from nextFree+1 (wrap at 0xA0) with d[rec_j+0x284]==0
ret rec_i
```

### PROM `00428710()`

```
while (i = hPend) != -1:
    PTD(rec)                                 ; scripted
    f[rec+0x414] = f[+0x48828]               ; epoch stamp
    G68: if q[rec+0x400] != 0:
        r = E56(rec)                         ; scripted
        if b[r] != 0: d[rec+0x114] = HID(w[rec])   ; scripted
    old = d[+0x48818] ; PHOOK(rec)           ; scripted
    d[+0x48818] = (new & ~1) | (old & 1)     ; bit0 PINNED pre-call
    d[rec+0x290] &= ~1                       ; clear pending bit
    unlink pending (prev.next/next.prev, hPend/tPend fixups)
    if hAct == -1: hAct = i ; w[rec+2] = -1
    else: w[tAct*0x740+pool+4] = i ; w[rec+2] = tAct
    w[rec+4] = -1 ; +0x48818 |= 0x20 ; tAct = i
hPend = tPend = -1                           ; ALWAYS, even on empty
```

### RETI `00427C90()`

```
hAct == -1 -> no-op
for i in active chain (saved next before unlink):
    if !(b[rec+0x290] & 2): continue
    unlink active; live--; hAct/tAct fixups; live==0 -> nextFree=0
    F4C0(rec)                                ; scripted
    while (c = w[rec+8]) != -1: DRAIN(rec_c) ; REAL
    if d[rec+0x114] != 0: HC1(d114)          ; slot enable clear
    if d[rec+0x118] != 0: HC2(d118)          ; handle id clear
    TDOWN(rec)                               ; scripted
    +0x48818 |= 0x20
```

### RELE `00429140(rcx = rec)`

```
rcx == 0           -> ret 0
d[rec+0x284] & 4 (retired):
    d[rec+0x290] |= 2 ; b[rec+0x2AE] |= 1 ;
    q[rec+0x108] = 0 ; d[rec+0x110] = 0 ;
    d[rec+0x284] = (d & ~4) | (1 << 30)
    L2D: if d[rec+0xC4] != -1:
        o = BASE(d[rec+0x10]) ; r = T51(q[o+0xDA8], d[rec+0xC4])
        if r: d[r+0xC] &= ~2
    if d[rec+0x18] != -1:
        o = BASE(d[rec+0x10]) ; m = MIDS(q[o+0xD98], d[rec+0x18])
        if m: d[m] &= ~4 ; d[m+0xA0] = BAS2(0)
    ret 1
b[rec+0x290] & 1 (pending):
    unlink pending; live--; hPend/tPend fixups;
    live==0 -> nextFree=0 ; CLR(rec) ; ret 1
else -> ret 1 unchanged
```

### DRAIN `00426EC0(rcx = child)` — the retire-time child unlink

```
p = sx16(w[c+6])                     ; parent
p == -1 -> ret                       ; NO -1 writes on this path only
if d[p+0x284] != 0:
    if w[p+8] == w[c]: w[p+8] = w[c+0xA]       ; head splice
    else: walk +0xA sib chain (each node d284-gated);
          on w[node+0xA]==w[c]: w[node+0xA] = w[c+0xA]
w[c+6] = w[c+0xA] = -1               ; ALL other exits
```

## Execution findings (beyond the contract's static reading)

1. **LKUP's active-list gate is a skip, not a compare-enable** —
   `test b[rec+0x290],2; jne skip`: retired/hidden records are invisible
   to name lookup while still linked. Pending records are compared with
   no flag gate. This unifies bit1's two roles: it hides a record from
   lookup AND marks it for retirement.
2. **ALOC seeds RINIT with `BASE(d[+0x48830])`** — the tail cell
   `+0x48830` (distinct from the `+0x48828` epoch) holds the resolver
   index passed as RINIT's fourth argument; `buf1` and the caller's
   original `r8d/r9d` ride the stack.
3. **PROM pins `+0x48818` bit0 across PHOOK** —
   `d[+0x48818] = (post_PHOOK & ~1) | (pre_PHOOK & 1)`: the hook may
   change any flag bit except bit0, which is force-restored.
4. **PROM's pending prev-write is unreachable during a clean drain** —
   each record's `+2` is already `-1` when its unlink runs (the previous
   iteration's `next.prev` update cleared it). The `prev.next` splice
   only fires on stale/corrupt links; verified via `prom-staleprev`.
5. **DRAIN writes `w[c+6]=w[c+0xA]=-1` on every exit except the
   `parent==-1` fast path** — including the parent-free terminate and
   the mid-chain `d284`-gated exits.
6. **RETI saves `next` before unlinking** — the walk follows the
   pre-splice successor, so a corrupted `+4` write cannot redirect the
   loop; `live==0` forces `nextFree=0` (matching RELE's pending path).
7. **RELE's retired path sets bit30 of `+0x284`, not a new flag** —
   `(d & ~4) | (1<<30)` clears the retired bit and sets bit30; the
   release is a state rewrite, not a list op.
8. **HC1/HC2 are `cl`-indexed table clears, not table scans** —
   HC1: `entry = u8(ecx)*0xE0 + q[0x2B40528]`, `d[entry+0x10]==ecx` →
   `b[entry+0x40] &= ~1` (the same slot table EXP-108's pass reads).
   HC2: `entry = u8(ecx)*0x70 + 0x2B3F570`, `d[entry+4]==ecx` →
   `d[entry+4] = 0`.
9. **CTOR's `+0x4881C` is 34.0f** (`0x42080000`), not the 32.5f the
   earlier static pass recorded — verified against live replay.
10. **CLR is a 1208-byte default writer, not a bare memset** —
    `0x740` clear plus ~100 stores: `-1` sentinels (links, `+0xC4`,
    `+0xC8`, `+0x450`, …), `1.0f` fields (xmm6 = const `0x1CEBBA8`),
    `0x1000` A8W values (`cvt(1.0 × 4096.0)`), `0x2A0=0xF`,
    `0x2F4=0x03050303`, `b[0x4B7]=0x20`, `b[0x66D]=2`, and the
    `0x40`-byte const struct copied from shipped `0x1F204E0` via
    `0046D110→00202C70`. The full image is byte-exact-verified on every
    `ctor-*`/`aloc-*`/`rele-pending*` case.

## Mutation campaign

79 byte-precise mutations across all six ops and 15 callees — flag
masks, condition-code inversions, list-head/tail field repoints, link
offsets (`+2/+4/+6/+8/+0xA`), stride imms (`0x740/0xE0/0x70`), capacity
and scan bounds, epoch/handle/resolver field offsets, flag-pin mask
width, and CLR default-write offsets. **79/79 killed.** Six initial
survivors were fixture-coverage gaps, resolved with new discriminating
cases:

- `m-pr-xormsk` (`(new^old)&1`→`&3`) → `prom-pinbit1` (PHOOK flips
  bit1: orig pins bit0 only → `0x62`, mutant pins both → `0x60`)
- `m-pr-prevunlink` (`prev.next` write `+4`→`+2`) → `prom-staleprev`
  (stale `prev` outside the drained chain — the only state in which
  that splice executes)
- `m-dr-sib` (walk sib `+0xA`→`+8`) → `drain-mid` (direct DRAIN call on
  a mid-chain child — the walk is unreachable from RETI, which only
  drains chain heads)
- `m-l2d-c4` (`+0xC4`→`+0xC8`) → `rele-retired-c4neg` (`dC4=-1`,
  `dC8≠-1`: orig skips L2D, mutant enters it)
- `m-g68-400` (`+0x400`→`+0x408`) → `prom-nohandle` (fixture `q408=0`)
- `m-al-rinitarg` (`+0x48830`→`+0x48828`) → `aloc-first` with distinct
  `d30`/`epoch` tail cells
