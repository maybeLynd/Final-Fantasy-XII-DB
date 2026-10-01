# EXP-195 — Notify dispatcher `00326500` tree + `00263E30` leaf execution

**Status:** complete — **202/202 cases, stable across 3 independent runs,
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192/193/194; 186 inherited + 16 new `n6500-*`/`l26620-*`/`l31b770-*`/
`l263e30`/`l317400-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Promotes the `00326500` notify dispatcher and its entire callee tree to real
execution (≈28 bodies newly tagged), plus the `00263E30` resolver leaf
disclosed-but-unexercised in EXP-194. Remaining scripted boundaries in this
contract shrink to `0030C650`, `00323910`, `00234DA0` (EXP-196 scope).

- `00326500` — notify dispatcher.
- `00263E30` — `ret q[rcx+0x30]` resolver leaf.
- Promoted callees: `00311E20`, `003272F0`, `0031ABF0`, `00263750`,
  `00265970`, `00265020`, `00265200`, `0033CA00`, `00326620`, `0030D9A0`,
  `00377C70`, `003148F0`, `0031B770`, `002367A0`, `00317400`, `0030A880`,
  `0030A8A0`, `003594B0`, `003590D0`, `0031B810`, `003137E0`, `003137F0`,
  `0026DAC0`, `003588B0`, `003589B0`.

## New executed facts

### `00326500` — notify dispatcher (no args)

Sequence: `311E20` → `326620` → `30D9A0` mode → slot byte → `31B770` →
hit/scan/fallback → `311E20` → `jmp 3594B0`.

- `30D9A0` mode source = `d[glob+0x5B04]`: `&8`→5, `&4`→4, `377C20`()≠0→3,
  `&2`→2, else `cl&1` → 0/1.
- Slot byte `bl`: modes {0,1} → `b[glob+0x5AA4]`; mode 2 → `0x1A`;
  mode 3 → `377C70()`; modes 4/5 → `0xFF` (initial value kept).
- `377C70` = `3148F0` (`d[2EF2B0()+0x1044]` clamped ≥0) → index N into the
  shared `q[02ADD100]` 3-byte-stride table → `b[tbl+3N+0xA]>>4 & 7`.
- `31B770(bl)`: `bl > 0x27` → 0 (no scan). Else `slotrow = glob+8+bl*0x1C8`;
  scans `236850`/`236820` rows (stride `0xF50`) for `q[row+0x698]==slotrow`.
- Hit && `q[row+0x698]!=0` → `ebp = d[objrow+8]`; `30D9A0`()==1 →
  `317400(objrow)` (pair op: `3137E0`/`3137F0` read `b[glob+0x5AD4]`/`+0x5AD5`
  → `31B770` each → both nonnull required before `26DAC0` float propagation).
- Miss or `q[+0x698]==0` → scan `edi=0..3`: `322C50(0x17, edi)` (fixed
  `0..9` bound — always passes for the loop range) → `al = b[glob+0x5A5A+edi*2]`
  → `2367A0(al)` (validates `322C50(2,id)`, scans OBJARR `0xF50` rows for
  `w[q[+0x698]+4]==id`, `0xFF`→`0xFFFF`); `q[+0x698]!=0` → same hit tail.
- Exhaust → `263750(0)` (`q[0209A1F0+i*8]` four-pointer ctx table, ecx>3→0);
  nonnull → `ebp = 3589B0(ctx)` = `((w[+0x16]&0x7FF)<<4 | b[+0x15]&0xF)<<0x10
  | w[+0]` (gen<<0x14|cls<<0x10|idx).
- Tail: `311E20` again → `jmp 3594B0` → commits `d[022C7FE4]=ebp`,
  `b[022C7FF8]=1`. Verified `ebp` = `d[objrow+8]` on hit paths, composed id
  on ctx fallback, 0 when no ctx.

### `00311E20` — gated ctx refresh

`d[022BE974]!=0` → immediate ret (verified: `33CA00` unreachable when set).
Else `3272F0` → `31ABF0`/`263750(idx)` → ctx → `265970(ctx)` =
`q[q[ctx+0xC0]+0x138]+0x30` blk (nonnull required) → `265020(ctx,&a,&b,&c)`
copies `d[q[ctx+0xB8]+0/4/8]` when `b[ctx+3]>>5 ∈ {1,3}` → `jmp 33CA00`.

`3272F0`: `3590D0`()=`d[022C7FE0]` (notify id); `b[02089340]&0x10` required;
`3588B0(nid)` = class<5 → `263FF0(cls)` (`02098E10+cls*0x288`) →
`q[+0]`/`q[+8]` nonnull + `b[+0x10]&1` + `idx<min(d[+0x20],d[tbl])` +
`w[row+0x16]==gen` resolve; loop `263750(i)`==row for `i<4` → ret `i`, else
`ret -1`.

`33CA00` (ctx nonnull): `q[022C7D18]=ctx`; 0xB0-byte `movups` copy of the
`265970` blk → `022C7D20`; `265020` triple → `022C7DD0..+8`; `265200` float
→ `022C7DE0` (`b[+3]>>5==1`→`f[q[+0xB8]+0x38]`, `==3`→`f[+0xA8]`, else 0);
`d[022C7D10]=1`. Cookie `00808C40` scripted (ret ignored).

### `00326620` — slot reconcile + ctor

`cl = b[glob+0x5AA4]`; `0xFF` → `ebx=-1`, else scan `b[glob+i*2+0x5A5A]==cl`
for `i<4` → `ebx=i`. `30D9A0`()==0 **and** `ebx<0` → `30A880(&st, 3)`:
`q[st]=0x22C1788`, `30A8A0(0x22C1788, 4, 3)` — per slot `31B810(esi)`
(=`322C50(0x17,esi)`→`2367A0(esi)`); flag `&4`→`b[row]&0x10`, flag `&1`→
`q[+0x698]` nonnull + `(d[+0x64]|d[+0x3C])&0x80000003` nonzero → `377C20`()
must be nonzero, flag `&2`→`b[rec+5]==0 && b[rec+4]<=6`. Qualifying rows
fill `q[0x22C1788+rdi*8]`; ret count. Count>0 → `d[glob+0x5AA4] =
b[q[q[st]+0x698]+4]` else `0xFF` → `call 326500` (recursion — verified
single-level: stored byte is then found by the map scan). Note the `&1`
gate's `377C20` requirement is **unreachable when `30D9A0`==0** — the or-mask
must be 0 to qualify, a real invariant.

### `00263E30` — resolver leaf

`mov rax, qword ptr [rcx + 0x30]; ret`. Verified `eax == q[ctx+0x30]`.

## Harness additions

- `ctx4`: `q[0209A1F0+i*8]` ctx pointer table (BSS — runtime-populated in the
  live game). Per ctx: `b[+3]` type bits, `w[+0]`/`b[+0x15]`/`w[+0x16]` id
  fields, `q[+0xB8]` out block (`outd`/`f148`/`fA8`), `q[+0xC0]`→`+0x138`
  chain for `265970` (`blk` writes at `blkbase+0x30`).
- `clstab`: `3588B0`'s `263FF0` class table `02098E10+cls*0x288` —
  `q[+0]`/`q[+8]`/`d[+0x20]`/`b[+0x10]` + ptr-array `d[tbl]` + `"ctxN"` rows.
- `g272f0` (`b[02089340]` mode flag), `g11e20` (`d[022BE974]` guard),
  `nid` (`d[022C7FE0]` notify id), `slothit` (objlink's `q[+0x698]` →
  `glob+8+slot*0x1C8` slotrow).
- `rargs`: REAL-entry rcx/rdx logging (separate from SCR `calls`) for
  arg assertions on promoted bodies.

## Disclosed scripted boundaries

`0030C650`, `00323910`, `00234DA0` (SCR retkeys `c650_ret`/`g3910_ret`/
`sp234da0_ret`), `00808C40` cookie. All other `326500`-tree callees run real.

## Cases (16 new)

`n6500-*` (9): `nullctx` (exhaust→ctx0 null→commit 0), `slothit` (mode0
`31B770` hit → `d[objrow+8]` commit), `mode1` (`317400` pair op), `mode2`
(`bl=0x1A` → slot-0x1A row), `mode5` (`bl=0xFF`→miss→4×`2367A0`→0),
`scanhit` (mode5 + `b[0x5A60]=5` map → `w[rec+4]` match), `ctxblk` (nid→
`3588B0` gen-resolve → `33CA00` store/triple/float/flag + `3589B0` id
commit), `ctor` (mode0 + `0x5AA4=FF` + qualifying objrow → `30A880` fill →
byte store → recursion → `594b0`×2), `gated` (`d[022BE974]=1` → `311E20`
no-op, `33CA00` absent).
`l26620-*` (2): `found` (map hit → no ctor), `ctor` (nested `326500`
dispatch → commit `d[objrow+8]`).
`l31b770-*` (3): `hi` (`cl=0x28` → 0, no scan), `hit`, `null`.
`l263e30` (1): `ret q[rcx+0x30]`.
`l317400-one` (1): pair resolve — second `31B770` misses → `26DAC0` skipped.
