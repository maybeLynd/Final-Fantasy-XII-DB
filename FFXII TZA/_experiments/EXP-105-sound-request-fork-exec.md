---
experiment: EXP-105
title: Sound-request fork (00210C00 / 0021B5B0 / 00219EA0 / 00212950 / 00224540+00224570 / 00223160+00223190) under isolated original execution
contract: ../18-Audio/Audio-Boundary/CONTRACT-sound-request.md
method: B
live_game: false
tool: evidence/sound-request-fork-exec/check.py
---
# EXP-105 — sound-request-fork-exec

**Status:** complete · **30/30 cases, 20/20 mutants, stable across three
processes**
**Evidence:** `evidence/sound-request-fork-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-096 executed the sound-request front half — verb `00357040`,
wrappers, resolvers, liveness gates, and the `001DBDB0` dispatch — and
explicitly stopped there: *"the pilot stops at `001DBDB0` before
executing the Seb/Sep fork."* This experiment closes that residual: the
two-way selector fork `00210C00`, both dispatch bodies, the receipt
allocator, and both voice workers with their real setter/pool/list
closure.

| VA | role | execution |
|---|---|---|
| `00210C00` | FORK subject — `sel==0` -> Seb, else Sep; `vol &= 0x7F`, `pan` -> `zx r9b` | **real** (40 B) |
| `0021B5B0` | SEB dispatch — signed bucket `sar((id + (id<0 ? 0x1FF : 0)), 9)` on `elem+0x3C` | **real** (138 B) |
| `00219EA0` | SEP dispatch — raw-id match on `elem+0x38` | **real** (157 B) |
| `00212950` | RCAL — counter++, `&0x7FFFFFFF`, zero->1 | **real** (28 B) |
| `00224540`/`00224570` | Seb worker shim + body (209 insns) | **real** (36+763 B) |
| `00223160`/`00223190` | Sep worker shim + body | **real** (36+356 B) |
| `00225580`–`002257E0` | leaf setters: `+0x18` rcpt, `+0x10` state, `+0x14` slot, `+0x24` sid, `+0x2C` kind, `+0x1C` vol, `+0x20` pan; `002256B0` full reset; `00225670/680/690/6A0` getters | **real** (12 bodies) |
| `002255C0` | voice ctor: vtable `0x9087C0`, `+0x14`q=-1, `+0x1C=0x7F`, `+0x20=0x40`, `+0x24=-1`, `+0x28=0` | **real**, quiet `~vc` (74 B) |
| `00221D10` | lazy `elem+0x20` pool-B init via `220CE0(G_VCTX)` | **real**, quiet `~l` (70 B) |
| `00221D60` | voice alloc: pool pop + DLL splice at list end | **real**, quiet `~a` (146 B) |
| `00221E00` | Seb get-or-alloc: `222280`×2 sweeps + `221E60` slot-find + `221D60` | **real**, quiet `~e` (83 B) |
| `00221E60`/`00221F40` | prev-chain finds on `elem+8` list (`+0x14` slot / `+0x24` sid) | **real**, quiet `~f1`/`~f2` (108 B ea) |
| `00222050`/`00222280` | dead-voice reaper (state ∈ {0,2} -> free + unlink + allocator `obj+0x18` call); `222050` sweeps `elem+8` and `G_LST` | **real**, quiet `~o`/`~sw` (36+191 B) |
| `00220CE0`/`00220D30`/`002204A0`/`00220550` | pool pops (`vctx+8` pool-B / `vctx+0xA0` voice pool) | **real** (79+12+161+161 B) |
| `00221710`/`00221210`/`00219D80` | `G_VCTX` getter, reap push, busy-tree insert | **real** (8+12+161 B) |
| `00210A60`/`00212910` | grow path (only on empty pool — not exercised; fixtures keep freelists nonempty) | **real**, measured (41+51 B) |
| `005CD4F0`/`005CD820`/`00808C40` | lock/unlock on planted mutexes; stack-cookie check | **real** (9+32+33 B) |
| `0016D6A0` | shipped no-op (`d` token) | **real** (3 B) |
| `00210B30`/`00210710` | `G_C2` getter (`c`, calls `16D6A0` inside); xref `objA.virt() or objB.virt()` (`x`) | **real** (33+68 B) |
| `005CC930`/`005CCB80` | mixer-wait fences (entry + loop + exit, only when `elem+0x30==1`) | scripted `~spin`/`~spn2` |
| `007A6DB0`/`007A7010`/`007A78B0`/`007A7A20`/`007A8CF0` | shared_ptr/refcount/weak-lock/bounds carriers | scripted `~s6d`/`~s70`/`~s78`/`~s7a`/`~s8c` |
| `007A5A00`/`007A8060`/`007A81F0`/`007A87C0`/`007A7E00`/`007A7E90` | `0x7a*` carriers inside attach arms and PAN/VOL tails | scripted `~s5a`/`~s80`/`~s81`/`~s87`/`~se0`/`~se9` |
| `00221940`/`00221C70` | bus-attach arms (callback / normal) — separate contract's subject | scripted `~at`/`~ac` |
| `0016D6D0`/`0016DA60`/`00199DB0` | pool tree extract/relink + `std::map` insert (STL bookkeeping inside the pops; silent in quiet zones) | scripted `~d6d`/`~da6`/`~m99` |
| `elem.vtable+0x50` | worker vtail | planted scratch body `~vt` |
| `obj+0x10`/`+0x18` member fn-ptrs | list allocator alloc/free | planted scratch bodies |

## Measured semantics (native execution, not static reading)

### FORK `00210C00(bank rcx, sel edx, id r8d, pan r9b, vol [sp+0x28])`

```
  edx=sel: sel==0 -> rcx=[bank+8]  (sebc) -> jmp 21B5B0
           sel!=0 -> rcx=[bank+0x10] (sepc) -> jmp 219EA0
  callee args: (rcx=sub, edx=id, r8d=zx pan, r9d=vol&0x7F)
```

### SEB `0021B5B0(sebc rcx, id edx, pan r8d, vol r9d)`

```
  bucket = sar(id + (cdq() & 0x1FF), 9)   ; signed floor(id/512)
  esi = RCAL()                            ; receipt ALWAYS allocated
  walk sebc+8 list: match elem+0x3C == bucket
  hit -> 224540(elem, esi, id, pan, vol)  ; miss -> ret esi
```

### SEP `00219EA0(sepc rcx, id edx, pan r8d, vol r9d)`

```
  walk sepc+8 list: match elem+0x38 == raw id
  r14 = RCAL()                            ; receipt ALWAYS allocated
  hit -> d (16D6A0, ecx = elem+0x30==2)
      -> 223160(elem, r14, id, pan, vol)  ; miss -> ret r14
```

### WSEB `00224570(elem rdi, rcpt r14d, id r12d, pan [rsp+0x24], vol arg5, arg6/7 stack)`

```
  elem+0x30==1 -> spin(5CC930) + while(==1) spn2(5CCB80) + spin
  slot = id & 0x1FF ; sid = id | 0x80000000 ; d (ecx = elem+0x50!=0)
  lower_bound(elem+0x60 tree, slot) on node+0x20 keys
  miss(rax==sentinel) -> exit             ; sd = [node+0x28]
  ~l = 221D10: elem+0x20==0 -> 220CE0(G_VCTX) pool-B pop -> store
  ~s8c(lazy+8, slot) -> al==0 -> exit
  sd+4 & 8  -> ~f2 find voice+0x24 == (sid&0xFFFFFE00)+7
               slot!=7 && found -> exit
  sd+4 & 20 -> c=210B30 (d inside) ; x=210710(id,vol) -> al!=0 -> exit
  ~e = 221E00 -> voice (222280 x2 + 221E60 slot-find + 221D60)
  T10 = voice+0x10 state
  state==1:  ~s6d copy (flag byte at dst+0x110)
    flag && sd+4 & 0x80 -> REUSE: ~s70 (==3 -> ~s7a)
        W14=slot W24=sid W18=rcpt
        arg6==0 -> PAN+VOL ; arg6!=0 -> exit  (no s78/vt either way)
    else -> ~a = 221D60 realloc -> fresh arm
  fresh:    sd+9 = sd+4&0x80 ? 0 : sd+4&0x20 ? (b&1)|0x40 : b
            W14=slot W24=sid W18=rcpt W10=1
            arg6 && arg7 -> W2c=3 + ~at(221940) ; else W2c=2 + ~ac
            (221C70) + PAN + VOL
  tail:     ~s78(voice+8) -> eax!=0 -> RST=2256B0 full reset
            ~vt = [elem.vtable+0x50](elem, voice)
```

### WSEP `00223190(elem rbx, rcpt ebp, id edi, pan r14d, vol arg5, arg6/7 stack)`

```
  spin gate identical to WSEB
  elem+0x44 & 0x20 -> c=210B30 (d) ; x=210710(id,vol) -> al!=0 -> exit
  ~o = 222050 (222280 x2 on elem+8 and G_LST)
  ~a = 221D60 -> voice
  elem+0x49 = b44&0x80 ? 0 : b44&0x20 ? (b&1)|0x40 : b44
  W14=0 W18=rcpt W10=1
  arg6!=0 -> W2c=5 + ~at ; else W2c=4 + ~ac + PAN + VOL
  tail: ~s78 (xmm1 = 0x9089BB const when b44&0x20 else 0)
        -> eax!=0 -> RST ; ~vt
```

### Voice layout (measured)

```
  +0x00 vtable (ctor 2255C0 plants 0x9087C0)
  +0x08 carrier ptr (shared_ptr object for the 0x7a* helpers)
  +0x10 state  +0x14 slot  +0x18 receipt  +0x1C vol  +0x20 pan
  +0x24 sid    +0x28 ?     +0x2C attach-kind (2/3 Seb, 4/5 Sep)
  RST 2256B0: +0x14q=-1 +0x1C=0x7F +0x20=0x40 +0x24=-1 +0x28=0 +0x10=2
```

## Findings measured by the suite

- **Both dispatches always allocate and return a fresh receipt**;
  playback (worker invocation) is the conditional half. `seb-rcpt-wrap`
  (`0x7FFFFFFE+1 -> 0x7FFFFFFF`) and `seb-rcpt-zero`
  (`0x7FFFFFFF+1 & mask -> 0 -> cmove 1`) pin the exact RCAL boundary.
- **Seb matches a signed bucket, Sep the raw id.** `id=0xFFFFFE00`
  (-512) buckets to `0xFFFFFFFF` via `(id + (cdq & 0x1FF)) sar 9`;
  `m-seb-sar` (shift 9->8) and `m-seb-key`/`m-sep-key` field mutants
  are killed.
- **The Seb flag byte is `sd+4` on the tree node's value**, not on the
  elem (the elem+0x44 byte is the *Sep* worker's). `sd+9` is the
  writeback target — the same `b&0x80 ? 0 : b&0x20 ? (b&1)|0x40 : b`
  derivation Sep applies to `elem+0x49`.
- **Seb reuse requires `state==1` + `~s6d` flag byte + `sd+4` bit7**;
  all three must hold or it falls to `221D60` realloc and the fresh
  arm. Reuse exits at `0x224842` — no `~s78`/vtable tail — and
  `arg6!=0` skips even the pan/vol setters.
- **Callback arms differ asymmetrically**: WSEB needs `arg6 && arg7`
  for kind-3 `~at`; WSEP needs only `arg6` for kind-5. Both skip
  pan/vol on the `~at` arm. The shims zero stack args 6/7, so the
  callback cases enter `224570`/`223190` directly (`wsebx`/`wsepx`).
- **`2257E0` clamps signed**: `vol<0 -> 0`, `vol>=127.0f -> 0x7F`,
  writes `voice+0x1C`, then tail-jumps `7A81F0`. `2256F0` writes
  `voice+0x20` directly and contains a `16D6A0` no-op call plus the
  `7A7E00`/`7A7E90` carriers.
- **The spin fence runs only when `elem+0x30==1`** — entry `5CC930`,
  `5CCB80` while still 1, exit `5CC930`. `state!=1` skips all three.
- **Pool pops run real**: `221D10` lazily pops pool-B (`vctx+8`) into
  `elem+0x20`; `221D60` pops the voice pool (`vctx+0xA0`), runs ctor
  `2255C0`, and splices an allocator-produced node at list end.
  `222280` reaps `state ∈ {0,2}` voices (free + unlink + `obj+0x18`
  allocator call) on both the elem list and `G_LST`.

## Mutation coverage

20 mutants, all killed (patch site -> case):

| mutant | site | kills via |
|---|---|---|
| m-fork-sel | `0x210C14` jne->je | fork-sel1-sep-hit |
| m-fork-vmask | `0x210C0F` `&0x7F`->`0x7E` | fork-sel1-sep-hit |
| m-seb-sar | `0x21B5E1` sar 9->8 | fork-sel0-hit |
| m-seb-key | `0x21B5FD` `+0x3C`->`+0x3D` | fork-sel0-hit |
| m-sep-key | `0x219EDD` `+0x38`->`+0x39` | fork-sel1-sep-hit |
| m-rcal-mask | `0x21295E` mask `0x7FFFFFFF`->`0x7FFFFFFE` | seb-rcpt-wrap |
| m-rcal-zero | `0x212963` cmove->cmovne | seb-rcpt-zero |
| m-sep-hitgate | `0x219EF3` je->jne (worker skip on hit) | fork-sel1-sep-hit |
| m-wseb-slot | `0x2245D5` `&0x1FF`->`&0xFF` | wseb-fresh |
| m-wseb-state | `0x2245AE` `cmp eax,1`->`cmp eax,2` | wseb-spin |
| m-wseb-f2gate | `0x22465A` `sd+4 &8`->`&4` | wseb-flag8 |
| m-wseb-slot7 | `0x224679` `cmp ebp,7`->`cmp ebp,6` | wseb-flag8 |
| m-wseb-xgate | `0x224687` `sd+4 &0x20`->`&0x10` | wseb-flag5-pass |
| m-wseb-freshgate | `0x2246C4` `sub eax,1`->`sub eax,2` | wseb-reuse |
| m-wseb-cb6 | `0x2247B3` arg6 `cmp 0`->`cmp 1` | wseb-cb-arm |
| m-wseb-kind | `0x2247BC` kind `3`->`2` | wseb-cb-arm |
| m-wsep-cb | `0x223249` arg6 `cmp 0`->`cmp 1` | wsep-cb-arm |
| m-wsep-kind | `0x223250` kind `5`->`4` | wsep-cb-arm |
| m-wsep-flag | `0x223220` `|0x40`->`|0x20` | wsep-flag5-pass |
| m-vol-store | `0x225813` `+0x1C`->`+0x1D` | wseb-fresh |

Two first-draft mutants were replaced after probing: `m-sep-state`
(`cmp edx,2` feeding the `16D6A0` no-op — provably dead) became
`m-sep-hitgate`; `m-wseb-state` needed the new `wseb-spin` case
(`elem+0x30==1`) to be reachable.

## Model notes / limitations

- Observations dedupe **byte-level last-wins**: the ctor's
  `+0x14` qword=-1 and `2256B0`'s reset qword legitimately overlap the
  W14/W18 setter dwords; final memory is compared, not write order.
- `210B30`'s `c` token brackets an inner `d` (`16D6A0` call); trace
  order `c=<ctx> d x=<xr>`.
- Quiet zones suppress inner tokens; scripted stubs still execute
  inside them silently (the pool-pop STL helpers never appear in any
  trace — all callers sit inside `~l`/`~e`/`~a`/`~o`).
- Grow path (`210A60`/`212910` refill on empty voice pool) and the
  `222280` reap unlink path are real but unexercised: fixtures keep
  freelists nonempty and voice lists clean. Marked in `bodies.json`.
- Attach arms `221940`/`221C70` are scripted stubs — the bus-attach
  closure belongs to a separate contract and is not claimed here.

## Results

- `cases: 30/30`, `mutants: 20/20 killed` — `run.log`, `run2.log`,
  `run3.log` (three independent processes, identical results).
- `result.json` records per-case trace, observations, diffs and faults.
- `bodies.json` records measured spans and sha256 for all 43 real
  bodies plus the scripted/intercepted boundary entries.
