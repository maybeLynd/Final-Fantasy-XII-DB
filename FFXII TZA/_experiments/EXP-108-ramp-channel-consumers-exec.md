---
experiment: EXP-108
title: Authored-command ramp channel consumers (003B6020 / 003B62D0) under isolated original execution
contract: ../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md
method: B
live_game: false
tool: evidence/ramp-channel-consumers-exec/check.py
---
# EXP-108 — ramp-channel-consumers-exec

**Status:** complete · **38/38 cases, 45/45 mutants, stable across three
processes**
**Evidence:** `evidence/ramp-channel-consumers-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-authored-command-ramp-channels` described the authored ramp
channels and their producer side, but its consumers were recorded as
unexecuted: the per-frame shadow-draw pass `003B6020` (slot iteration,
enable/hide gates, record copy, buffer swap/finalization) and the
shadow-draw record builder `003B62D0` (ramp-channel-derived values,
blend logic, trigonometric rotation, slot writeback, output-record
construction). This experiment executes both shipped bodies — plus the
full shallow callee cone — under Unicorn and diffs them against an
f32-precise model on state, memory, and boundary-call traces.

| VA | role | execution |
|---|---|---|
| `003B6020` | PASS subject — 160-slot draw pass | **real** (677 B) |
| `003B62D0` | BLD subject — 0xA0 record builder | **real** (1301 B) |
| `003A1DB0` | SWAP — bufidx toggle + FIN + cursor reset | **real** (84 B) |
| `0036F360` | FIN — ring terminator append/overwrite | **real** (150 B) |
| `00264670` | K3F — kind-3 record float read | **real** (35 B) |
| `0046FAE0` | RLUT — ramp LUT row/index lookup | **real** (84 B) |
| `003B6BF0` | RES1 — actor-rec resolve (stride 0x740) | **real** (43 B) |
| `003E6F70` | GATE — `q[rec+0x400]!=0` validity | **real** (17 B) |
| `00421FF0` | RES2 — secondary object resolve | **real** (85 B) |
| `0020E600` | BASE — `ecx + q[0x1F83530]` | **real** (10 B) |
| `003E56A0` | deep object resolver | scripted, `s<rcx>` arg capture |
| `002ED570` | mid-array resolver | scripted, `m<rcx>:<edx>` capture |
| `00370F60` | outer resolver | scripted, `o<rcx>:<edx>` capture |

## Measured semantics (native execution, not static reading)

### PASS `003B6020()`

```
copy 0x1A0 head template T_HEAD=0x2AEA0D0 -> stack
patch 4 xmm consts from T_XMM=0x2AEDDB0 (+0xD0/E0/F0/100)
write head to ents[d[G_BUFIDX]].cursor; cursor += 0x1A0
rsi = 003A1DB0()                          ; swap: bufidx ^= 1,
                                          ;   FIN(old), ret &ents[new]
copy 0xA0 slot template T_SLOT=0x2AEA030 -> stack
for i in 0..0x9F:  rbx = q[G_SLOTS] + i*0xE0
    if !(b[rbx+0x40] & 1): continue       ; bit0 = ENABLE (not skip)
    eax = b[rbx+0x41] | d[G_GATE]
    if eax & 2: continue                  ; local|global hide, bit1
    ecx = d[rbx+0x10]                     ; resolved channel id
    if 003B62D0(ecx, stackbuf) == 0: continue
    copy 0xA0 stackbuf -> ents[idx].wr base
    cursor += 0xA0
    rsi = 003A1DB0()                      ; buffers ALTERNATE per record
ret rax = last leftover (swap ptr | b41|gate | bld ret)
```

### BLD `003B62D0(ecx = channel id, rdx = out)`

```
rslot = q[G_SLOTS] + u8(ecx)*0xE0
d[rslot+0x10] != ecx          -> ret 0    ; index echo gate
w[rslot+4] == 0xFFFF          -> ret 0    ; no actor
rbp = sx16(w[rslot+4])*0x740 + q[G_RECS]
d[rbp+0x284] == 0             -> ret 0    ; actor validity
r14 = 00421FF0(rbp, w[rslot+0x3C])        ; resolver 1
r15 = 00421FF0(rbp, w[rslot+0x3E])        ; resolver 2
rsi = 003B6BF0(w[rslot+4]) -> 003E6F70 -> 003E56A0   ; build source
any null -> ret 0
edx = cvt((w[rsi+6]-w[rsi+4]) * f[rslot+0x14]) + w[rsi+4]
out+0x14 = edx ; out+0x6C = d[0xD11580 + edx*4]      ; dword LUT
eax = (cvt((w[rsi+2]-b[rsi+1]) * f14) + b[rsi+1]) * 2
out+0x10 = eax ; out+0x30 = d[rsi+8]
out+0x20 = (f14*f[rsi+0x3C]+f[rsi+0x38]) [/ (edx-1) if edx>1]
eax<4 or eax>0x64 -> ret 0 (partial record written)
b40&0x40:  out+0x40=f[rsi+0x14]+f[rsi+0x10], +0x44=0, +0x54=r14.d34
else:      out+0x54=K3F(q[rbp+0x108]), +0x40/+0x44=rsi.d10/d14
out+0x48=d[rsi+0x34] ; out+0x4C=d[rsi+0x30]
out+0x60/64/68 = rslot.d20/d24/d28
out+0x34 = f18*f08*f44 ; out+0x38 = f1C*f08*f44
out+0x28 = f0C*rsi.f0C*1.0*f2C*0.5
if b[rslot+0x43] != 0:                    ; ramp path
    xmm3 = 0046FAE0(1, 2, f[rslot+0x98])  ; ramp row 5, cnt=60
    xmm2 = 1.0 - xmm3
    b40&0x20: x4/x5 = f50/f54 direct, then xmm3=1, xmm2=0
    else: x4..x9 = xmm2*f80..f94 + xmm3*f50..f78 (row interp)
    blend (w3a==w38 ? (w3c==w38 ? r14 : r15) direct
           : w3c==w38 ? xmm2*r15+xmm3*r14 : xmm2*r14+xmm3*r15)
    -> out+0x50 (+0x30 field), out+0x58 (+0x38 field)
else: x4..x9 = f50..f78 direct; blend w38==w3c ? r14 : r15
wb rslot+0xC0..0xD4 = x4,x5,x7,x8,x6,x9   ; pre-transform row
x4 = (x4+f48)*f44 ; x5 = (x5+f4C)*f44 ; x6 = x6 + actor.f124 + fBC
out+0x34=x7*v34 ; +0x38=x8*v38 ; +0x28=x9*v28 ; +0x24=x6
idxr = cvt(actor.f124/2pi * 32768)
sin = TRIG[idxr & 0x7FFF] ; cos = TRIG[(0x2000+idxr) & 0x7FFF]
out+0x50 = (x4+f18)*cos + x5*sin + prev50
out+0x58 = x5*cos - (x4+f18)*sin + prev58
ret 1
```

### Callees

```
003A1DB0 SWAP:  edx=d[G_BUFIDX]; d[G_BUFIDX]=1-edx
                rcx=q[ents[old]]; edx=(q[ents[old]+8]-rcx)>>4
                0036F360(rcx, edx); ents[new].cursor=ents[new].base
                ret &ents[new]
0036F360 FIN:   edx==0 -> ret
                r9 = rcx + edx*16; hdr = d[r9-0x10]
                if hdr&0x70000000 == 0x30000000:
                    dst = r9 if edx<0x200 else r9-0x10   ; append|overwrite
                    q[dst]={0x10000000}; q[dst+8]=0
                G_RING = ecx&0x3FF0; G_RING = edx
                spin: reload G_RING x3, bound-check, converge
                G_RING = 0x100
0046FAE0 RLUT:  row = 0x1F20E60 + (3*edx+r8d)*0x1E0
                cnt = d[0x1F20A98] (=60)
                idx = cvttss2si((cnt-1)*xmm0)
                cmovs eax,r9d(r9d==0): idx<0 -> 0        ; symmetric clamp
                jbe: idx>cnt-1 -> cnt-1
                ret f[row+idx*4]
003B6BF0 RES1:  cx==0xFFFF -> 0
                rec = sx16(cx)*0x740 + q[G_RECS]
                d[rec+0x284]==0 -> 0 else tail 003E6F70
003E6F70 GATE:  q[rec+0x400]==0 -> 0 else tail 003E56A0 (stub)
00421FF0 RES2:  ebx=d[rcx+0x18]; ebx==-1 -> 0
                rax = 0020E600(d[rcx+0x10]); rcx=q[rax+0xD98]
                rax = 002ED570(rcx, ebx) stub; ==0 -> 0
                else tail 00370F60(rax, edi) stub
0020E600 BASE:  ret ecx + q[0x1F83530]
00264670 K3F:   rcx==0 or (b[rcx+3]&0xE0)!=0x60 -> xmm0=0
                else xmm0 = f[q[rcx+0xB8]+0xD4]
```

## Findings

1. **Slot `+0x40` bit0 is an ENABLE, not a skip flag** — `test al,1;
   je skip`. Disabled slots leave `eax` untouched; hidden slots
   (`(b41|gate)&2`) leave `eax = b41|gate` — the pass's return value is
   the last such leftover, observed `ret=2` on all-hidden passes.

2. **The hide gate ORs the slot byte with the global cell**:
   `(b[rslot+0x41] | d[0x2B40524]) & 2` — bit1 set in either hides the
   slot; gate bit0 alone does not.

3. **`ecx` is a resolved channel id, re-validated by echo**: BLD
   recomputes `rslot = slots + u8(ecx)*0xE0` and requires
   `d[rslot+0x10] == ecx` — the table is self-describing and
   mismatched indices early-out.

4. **Every produced record costs a buffer swap** — `003A1DB0` is
   called after the head template AND after each copied record, so
   successive 0xA0 records land in *alternating* draw buffers and each
   buffer retains only its most recent record.

5. **`0036F360`'s four rip-relative ops all hit one cell
   `0x2EBA3F8`** — write `ecx&0x3FF0`, write `edx`, then three reads;
   the spin loop converges in one pass single-threaded and the cell
   always ends `0x100`. The terminator is appended at `r9` when
   `edx<0x200`, else it *overwrites* the last entry — `fin-bound`
   (edx=0x200, tagged last entry + `0xAA` guard) discriminates the
   bound.

6. **The ramp index is symmetric-clamped**: `cvttss2si((60-1)*x)` then
   `cmovs eax,r9d` (r9d==0) clamps negative to 0 and `jbe` clamps above
   `cnt-1` — the count cell is `d[0x1F20A98]`=60, not the byte at
   `…A97`. Row = `(3*edx+r8d)*0x1E0` = row 5 for the `(1,2)` call.

7. **The blend selects on three slot words**: `w3a==w38` picks a
   direct object copy (r14 if `w3c==w38` too, else r15); `w38==w3c`
   (w3a apart) blends `xmm2*r15 + xmm3*r14`; fully distinct blends
   `xmm2*r14 + xmm3*r15` — the operands swap between the two blend
   arms.

8. **The slot writeback is the pre-transform row** `+0xC0..+0xD4`
   (interleaved store order C0,C4,D0,C8,CC,D4), written *before* the
   f48/f4C offset-scale, the actor-angle add (`f124+fBC`), and the
   sin/cos rotation of `+0x50`/`+0x58`.

9. **Trig index**: `cvttss2si(f124/2pi*32768)`, cos via the
   `+0x2000` LUT offset, both masked `&0x7FFF` — `bld-angle-pi`
   (f124=pi → idx 0x4000) discriminates the mask width.

10. **Three mutants were initially survivors and were resolved by
    discriminating fixtures, not removed**: `m-rstride` (0*stride==0 —
    added `bld-rec5`), `m-trigmask` (idx bit14 never set — added
    `bld-angle-pi`), `m-finbnd` (bound never approached — added
    `fin-bound` direct-FIN case). No equivalent mutants remain.

## Suite

38 functional cases: 24 BLD (ok, hi-channel, all 6 early-outs, both
resolver nulls, size bounds, bit6/bit5, nolut both blends, three blend
arms, ramp lo/hi/neg, k3 badkind/null, rec-index 5, angle pi) + 13 PASS
(empty, one, hide local/global, gate bit0, multi3, bldfail, cross,
terminator, bufidx1, slot159) + 1 FIN direct (edx=0x200 bound).

45 byte-level mutants, all killed: 9 PASS (enable, hide mask/or/jcc,
loop count, stride, cursor advance, template advance, bldret jcc),
23 BLD (idx cmp, w04neg, d284, spans, double, bounds, bit6/bit5, b43,
3 blends, f44, trig off/mask, wboff, f98, f14), 13 callees (toggle,
cursor field, tag, fin bound, ring, k3 kind/off, res1 stride/validity,
gate off, d18neg, d98, base op, ramp stride, clamp jbe, cmovs).

## Method notes

- Both subjects plus all eight shallow callees run from shipped bytes
  end to end; injected state is only BSS fixture memory (slot/rec
  tables, object array, draw buffers, ring, templates — all
  runtime-populated cells in game) and the three scripted boundary
  returns.
- Shipped `.data`/`.rdata` read with **zero fixture**: ramp LUT
  `0x1F20E60` + count `0x1F20A98`, trig LUT `0x1F004E0`, dword LUT
  `0xD11580`, float consts `0xD10820/28` (±32768), `0x1CEBC78` (2pi),
  `0x1EFE314` (1.0), `0x1CEBB70` (0.5).
- `00370F60` (OUTR) is tail-called once per `00421FF0` pair — the stub
  cycles its return list per *pair*, so each BLD call sees r14=first,
  r15=second.
- Model equality covers: return value, the full 0xA0 out record, the
  0x18 writeback window per watched slot, both draw buffers'
  head/record/tail windows, entry cursor state, G_BUFIDX, G_RING, the
  fin memory window (FIN cases), and the ordered callee-trace tokens.
- Evidence class: NATIVE/STATIC authority for body bytes +
  MODEL-PROVEN for the fixture harness; nothing here is engine-in-loop
  or live replay.
