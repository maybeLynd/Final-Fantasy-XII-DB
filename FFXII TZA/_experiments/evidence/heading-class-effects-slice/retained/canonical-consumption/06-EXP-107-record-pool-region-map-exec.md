---
experiment: EXP-107
title: Actor record pool allocator + region map (002679F0 / 00266AD0) under isolated original execution
contract: ../04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md
method: B
live_game: false
tool: evidence/record-pool-region-map-exec/check.py
---
# EXP-107 — record-pool-region-map-exec

**Status:** complete · **27/27 cases, 26/26 mutants, stable across four
processes**
**Evidence:** `evidence/record-pool-region-map-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-actor-record-pool-and-region-map` §7 recorded that three of
its §15 claims carry isolated original-code evidence but **"the
negative and the arithmetic do not."** This experiment closes the
arithmetic half: the allocate-and-initialize body `002679F0` (the pool
layout arithmetic and `packedKindAndSequence` planting) and the
region-map dispatch `00266AD0` (the eight pointer arms the contract
describes). The §15 negative — that no other arm writes those offsets —
is an absence claim and is **not provable by replay**; it stays open
and is disclosed, not silently promoted.

| VA | role | execution |
|---|---|---|
| `002679F0` | ALLOC subject — size arithmetic, fn-ptr alloc, memset, pointer-table + packed-byte planting, prefix sums, per-record init loop | **real** (436 B) |
| `00266AD0` | RMAP subject — `b[rec+3]&0x1F` 8-arm jump-table dispatch + sub-flag addend | **real** (211 B) |
| `00861EC0` | CRT memset thunk (`jmp qword IAT` — target outside image) | entry-intercepted; zero-fill done harness-side |
| `00266530` | per-record init ctor (~600 B, 8 callees — calls `00266AD0` itself) | scripted `i<idx>` arg capture |
| `qword[mgr+0x88]` | indirect allocator fn-ptr | planted stub returns fixture pool; `a<size>` capture |

## Measured semantics (native execution, not static reading)

### ALLOC `002679F0(rcx = manager slot)`

```
r12 = q[rcx]                       ; descriptor
r11d = d[rcx+0x20]                 ; record count  -> [rsp+0x50]
r13d = w[desc + movsxd(d[desc+0x14])]        group count
r9d  = sum_i  ((w[TAB+i*4+2]+0xF)>>4) * w[desc+off+2+i*2] << 4
       TAB = 0x1E0C328 (shipped)   ; per-group align16(recsize)*count
esi  = (r11d*8 + 0x17) & 0xFFFFFFF0          ; ptr-table span
edi  = 2*esi                       ; records begin at pool+edi
ebx  = edi + r9d                   ; total bytes
pool = call qword[rcx+0x88](ebx)   ; indirect allocator
memset(pool, 0, ebx)               ; CRT thunk (boundary)
d[pool]        = r11d              ; header = record count
q[rcx+0x1F0]   = pool + esi        ; manager's ptr-table view
per group i < r13d:
    w[rcx + TAB[i].kind*2 + 0x1D0] += w[desc+off+2+i*2]   ; kind count
    per record j in group (r9b = i&0x1F):
        q[pool + j*8 + 8] = rdx              ; ptr-table entry
        b[rdx+3] = (old&0xE0) | (i&0x1F)     ;   (dead: overwritten)
        b[rdx+3] = (i&0x1F) | (TAB[i].kind << 5)  ; packedKindAndSequence
        rdx += align16(w[TAB+i*4+2])         ; record stride
prefix row (4 iters, edx=0):
    w[rcx+0x1D8+k*2] = sum of kind counts so far
per ebp < r11d:
    00266530(rcx, pool, ebp)       ; per-record init (boundary)
ret pool
```

### RMAP `00266AD0(rcx = record)`

```
seq = b[rcx+3] & 0x1F
seq > 7  ->  ret rax = seq           ; cdqe, no writes
jump table 0x266BA4 (shipped):
  seq 0:    +0xB8=0        +0xC0=0        r8 = rec+0x120
  seq 1,2:  +0xB8=rec+0x120 +0xC0=0        r8 = rec+0x1A0
  seq 3,4:  +0xB8=rec+0x120 +0xC0=0        r8 = rec+0x140
  seq 5-7:  +0xB8=rec+0x120 +0xC0=rec+0x350 r8 = rec+0x4D8
tail (all arms):
  +0xA0 = r8
  +0xA8 = r8 + (b[0x1E0C329+seq*4]==1 ? 0xA0 : 0xC8)   ; see finding 2
ret rax = the +0xA8 value
```

### The shipped table `0x1E0C328` (real image bytes — the shared key)

8 records × `{u8 kind, u8 subflag, u16 recsize}`:

| grp | kind | sub | recsize | RMAP arm |
|-----|------|-----|---------|----------|
| 0 | 0 | 0 | 0x328 | g0 |
| 1 | 1 | 0 | 0x3A8 | g1/2 |
| 2 | 1 | 1 | 0x330 | g1/2 |
| 3 | 2 | 0 | 0x348 | g3/4 |
| 4 | 2 | 1 | 0x2D0 | g3/4 |
| 5 | 3 | 0 | 0x6E0 | g5-7 |
| 6 | 3 | 0 | 0x6E0 | g5-7 |
| 7 | 3 | 1 | 0x668 | g5-7 |

One shipped table feeds all three consumers: ALLOC's loop-1 reads the
`+2` recsize word at `0x1E0C32A+i*4`, loop-2 reads `+0` kind and `+2`
stride at `0x1E0C328+i*4`, and RMAP reads the `+1` sub-flag at
`0x1E0C329+seq*4`.

## Findings

1. **The region map dispatches on the GROUP index, not the kind.** The
   allocator plants `b[rec+3] = (kind<<5) | (i&0x1F)` where `i` is the
   outer group index; `00266AD0` consumes `b[rec+3]&0x1F` — the *group*,
   and the three high bits (kind) do not affect the dispatch (verified
   by `rm-g2-hikind`/`rm-g5-hikind`: `pk=0xE2`/`0x65` behave exactly as
   `pk=2`/`5`).

2. **The sub-flag addend is inverted from the naive reading.**
   `cmp flag,1; mov eax,0xC8; jne skip; mov eax,0xA0` — flag `==1`
   selects **0xA0**, everything else selects **0xC8**. Sub-flagged
   groups (2, 4, 7 per the shipped table) get the *smaller* +0xA8.

3. **ALLOC reads two fields of the same shipped table**, not two
   tables: loop-1's size word is `w[0x1E0C32A+i*4]` = `TAB[i].recsize`
   and loop-2's base is `0x1E0C328` = `TAB[i]` itself — the `lea`
   displacements differ by `0x12` only because they anchor on different
   fields of one 32-byte structure. The `+1` sub-flag byte that RMAP
   reads is the same record's second field.

4. **`d[pool]` is written before the record loop** — with `edi==0`
   (negative/huge record counts collapse `esi` to 0) the first record
   sits at `pool+0` and its `b[rec+3]` write clobbers header byte 3.
   Observed and modelled (`alloc-neg-cnt`: `hdr` reads `0x00FFFFFE` for
   `count=0xFFFFFFFE`).

5. **Kinds 4–7 are dead writes.** `w[mgr+kind*2+0x1D0]` for `kind` 4–7
   lands on `mgr+0x1D8..0x1DE` — the prefix-sum output row, which the
   prefix loop overwrites afterwards. Only kinds ≥8 would survive (past
   `mgr+0x1E0`); the shipped table only uses kinds 0–3.

6. **`ret` of the region map is the `+0xA8` pointer**, not the record;
   the `seq>7` exit returns `cdqe(seq)`.

7. **`and cl,0xE0` at `0x267B00` is provably dead**: the first store to
   `rec+3` is unconditionally overwritten by the second store in the
   same iteration — recorded as an equivalent-mutation exclusion, not a
   surviving mutant.

8. **The sub-flag seq mask at `0x266B82` is provably equivalent**: only
   `seq<=7` reaches it, where bit 4 of the masked value is already 0 —
   `&0x1F` and `&0x0F` are indistinguishable there.

9. **Group indices beyond 7 are legal inputs to ALLOC** (the bound is
   the descriptor's own group count): `alloc-grp16` drives group 16
   through `TAB[16]` (`{kind 3, sub 0, size 0}` — the bytes that happen
   to follow the table) and the `i&0x1F` packing wrap is observed
   (`pk=0x70` for `i=16`). This kills the `i&0x1F→0x0F` mutant that is
   equivalent for `i<16`.

## Suite

27 functional cases: 13 ALLOC (1/2/4/8 groups, empty count/group,
negative count, seeded kind counts, alternate descriptor offset,
zero-count groups, 17-group wrap) + 14 RMAP (all 8 arms, high-kind
packed bytes, seq 8/0x1F/0x20/0xFF refusal and wrap).

26 byte-level mutants, all killed. Two further sites were analysed and
excluded as provably equivalent (findings 7–8) rather than reported as
survivors.

## Method notes

- Both subjects run from shipped bytes end to end; the only injected
  state is the manager slot, descriptor, pool memory, record, and the
  allocator fn-ptr (which is indirect by construction — the shipped
  code reads `qword[rcx+0x88]`).
- `00861EC0` is an import thunk (`ff 25 …` into IAT); entry-intercepted
  and zero-fill implemented harness-side. A pool poisoned with `0xAA`
  proves the fill ran (`tail` observable).
- `00266530` is the real per-record ctor (it calls `00266AD0`
  internally); scripted as a boundary with `(mgr, pool, idx)` capture —
  its own closure is outside this package's claim.
- The shipped table is read from the image at runtime by the model
  (`raw_tab`), never transcribed — the fixture carries no copy of it.
- Model equality is on the full final memory image: header, ptr-table
  pointer, 4 kind counts, 4 prefix words, 12 xtra window words,
  ptr-table entries, record packed bytes, memset tail, return value,
  and the boundary-call trace.
