# EXP-152 design — spawn-record init 0023AC80 (EXP-150's largest scripted boundary)

Subject: `0023AC80(rcx=spawn_rec rdi, edx=packed sel)` — byte0=idx (esi),
byte1=mode (ebx: 0=foe, 1=member, >=2 → ret 0). 0x2CC.

## Executed semantics (from full disasm, Temp\ac80_full.txt)

1. memset(rdi, 0, 0x1C8); q[+0x50]=-1; w[+0x58]=FFFF; w[+0x1C3]=FFFF;
   b[+0x1C5]=0xFF.
2. `d[02089300]==0` → ret 0 (sentinels still written).
3. mode dispatch:
   - member(1): desc=q[02EBF120]; if desc==0 or 20E600(d[desc+0xC])==0
     → r14=0 (still proceeds → FAULT at 23ADA8 `w[r14+0x16]`).
     member_row = elemb + d[desc+0xC]_resolved + w[desc+8]*idx.
     r12d=1 (is_member to 30C470).
   - foe(0): desc=q[02EBF130]; null desc/resolve → rbp=0 → FAULT at
     23AD7B `b[rbp+0x2E]`. foe_row likewise.
     edx (count arg to 30C470) = max(b[foerow+0x2E], 1).
4. w[rdi+4] = sel16; `30C470(rdi, edx=count, r8d=is_member)`.
5. member: 4× 31A630(rdi, slot, val, 0): slot0=w[membrow+0x16],
   slot1=w[membrow+0x1C], slots 2,3 = 0xFFFF. ret 1.
6. foe:
   a. `323790(rdi, w[foerow+0x44])` — gil add clamp [0, 0x1869F]
      into d[rdi+0x190]. LEAF, real.
   b. if idx<=6: scan ability table q[02EBF038] rows i<d[tbl+4]:
      row_i = 20E600(d[tbl+0xC]) + w[tbl+8]*i; if b[row_i+7] & (1<<idx)
      → 323910(rdi, i, 1, 1) [SCRIPTED]. Null first-resolve →
      r8=0 → FAULT reading b[7] at 23AE68.
   c. 5× 31A630(rdi, 0..4, w[foerow+0xA..0x12], 0).
   d. `327CB0(rdi, w[foerow+0x14])` — real.
   e. `326030(q[02EBF190], idx)` — real; idx>0x27 → r8=0 →
      FAULT movups [0x88] at 326057.
   f. `327DE0(q[02EBF190]+8+idx*0x1C8)` — real.
   g. b[foerow+0x2C] & 0x40 → d[rdi] |= 4. ret 1.

## Callees — real/scripted split (EXP-148/150 precedent: subjects real,
proven/deep callees scripted at entry)

REAL:
- 23AC80 subject; 20E600 (eax=ecx+q[01F83530]); 861EC0 memset hook
- 323790 leaf (d[+0x190]+=edx clamp [0,99999])
- 31A630 slot writer (writes w[rec+0x50+slot*2]; r9d!=0 → 30F9A0/
  30C410 scripted hooks; si==0xFFFF → skip 317930 path; on CHANGE
  (w[+0x50+slot*2] != old) → 30FED0(rec,0x97) scripted; r9d →
  31B860→324470 scripted). inners scripted.
- 327CB0: rcx==0→ret; b[rec+5]!=0→ret; 322C50(0xA,esi) REAL (EXP-150
  proven); resolves q[02EBF0E0] row esi-0x5000; copies ≤12
  (w,w) pairs src[+i*2],[+i*2+0x20] → w[rec+0x88+i*4],[+0x8A+i*4],
  bts w[+0xB8],i; stops on FFFF src; b[+0xBA]=count; pads i..11 with
  d=-1 + btr; TAIL → 327DE0(rec) real.
- 326030: d[glob+idx*4+0x7370]=0; r8=glob+8+idx*0x1C8 (idx≤0x27 else
  0→fault); 3× movups copies [r8+0x88/0x98/0xA8]+d[+0xB8] →
  glob+idx*0x9C+0x5B10/0x5B44/0x5B78 (0x34B each +d).
- 327DE0: b[rcx+4]=order idx; row=02089378+idx*0x170; cursor
  d[glob+idx*4+0x7370]+idx*3; rdi2=glob+0x5B10+cursor*0x34; loop over
  set bits in w[rdi2+0x30]: pair (w[rdi2],w[rdi2+2]) valid(≠FFFF) →
  resolve 02EBF0D8 row (bp-0x6000) → fill row fields +0x26..0x36.
- 30C470 (0x1B0): stats header — copies w[foerow+0x16]→d[rec+8],
  w[+0x1A]→w[+0xC], f[+0x10..0x1C] floats, b[+0x46]→b[+0x20]
  (324100 override), then scripted 30C650/2F8F20(real?)/30F690/
  30F340/30F5A0/30FED0. Member path skips foe fields.
- 322C50 real (EXP-150 proven validator), 2F8F20 level→float real
  (verify leaf in harness).

SCRIPTED boundaries (entry-intercepted, args recorded, disclosed):
- 30C650 (EXP-148 proven subject — boundary here)
- 30FED0 recompute (EXP-148 proven; reached via 31A630 + 30C470)
- 30F690/30F340/30F5A0 — mutually recursive stat cluster (pulls
  377C20/3105D0/30E360/31B7E0/316CF0/316CD0/30AB40)
- 323910 (0x299, 15 calls — deep license/ability grant; gated
  b[rec+5]==0 + 322C50; special idx 0xE5/0x11)
- 317930 (slot search, calls 322C50), 318B40 (list ops),
  30F9A0/30C410 (un/equip), 31B860→324470 (member block),
  324100→324020 (override chain; 324100 real w/ 324020 scripted OK)

## Fixture surface

- rdi = heap rec 0x200. edx = sel.
- d[02089300]=1 gate.
- mkdesc model (EXP-150): q[CELL]=desc block; d[desc+0xC]=off into
  elemb (20E600 returns elemb+off); w[desc+8]=stride; d[desc+4]=count
  (02EBF038 loop bound only).
- q[01F83530]=elemb (0x90000+ heap).
- Cells: 02EBF120 member desc, 02EBF130 foe desc, 02EBF038 ability
  table desc, 02EBF0E0 pair-table desc, 02EBF0D8 order-table desc,
  q[02EBF190]=glob (heap 0x8000+).
- memb_row = elemb + memd_off + memd_stride*idx (w[+0x16], w[+0x1C]).
- foe_row  = elemb + foed_off + foed_stride*idx (b[+0x2E] count,
  w[+0x44] gil, w[+0xA..+0x12] slots, w[+0x14] pairidx, b[+0x2C]).
- ability row_i = elemb + abil_off + abil_stride*i (b[+7] bitmask).
- pair row = elemb + pair_off + pair_stride*(w[foerow+0x14]-0x5000):
  12×w at +0, 12×w at +0x20.
- order row = elemb + ord_off + ord_stride*(bp-0x6000): fields
  w[+8]→+0x28, b[+0x10]→+0x26, w[+0x18]→+0x2A, w[+0xA]→+0x2E,
  b[+0x11]→+0x2C, w[+0x1A]→+0x30, w[+0xC]→+0x34, b[+0x12]→+0x32,
  w[+0x1C]→+0x36.
- glob: d[glob+idx*4+0x7370] cursor; slotrow = glob+8+idx*0x1C8
  (b[+4]=order idx used by 327DE0; +0x88 pair array copied by 326030);
  order rows at canonical 02089378 + b[slotrow+4]*0x170 (fixture can
  point 02089378-region reads... wait — 02089378 is canonical .data;
  327DE0 writes there directly — planted canonical cells work since
  image is writable).

## Cases

- gate-off → ret 0, memset+sentinels only
- mode≥2 → ret 0
- member normal → ret 1, slots 0/1 from memb row, 2/3=FFFF
- member null desc → FAULT 0x23ADA8 (w[0x16] read)
- member null resolve (desc→off resolves 0? no — 20E600 never fails;
  null desc only) — actually second 20E600 result is base; if
  d[desc+0xC]=0 → rax=elemb+0 = nonzero always. Member-null path only
  via q[02EBF120]==0.
- foe normal → ret 1: gil clamp, 5 slots, pair copy, counter clear,
  order rows, flag or4
- foe null desc → FAULT 0x23AD7B (b[0x2E])
- foe idx>6 → scan skipped entirely (still slots/pairs/orders)
- foe count b[+0x2E]=0 → 30C470 gets edx=1
- gil clamp: +0x190 boundary 0x1869F / negative → 0
- pairidx <0x5000 → esi-0x5000 negative → imul negative → row ptr
  bogus — case documents no guard
- scan null first-resolve → FAULT 0x23AE68 (b[7])
- 326030 idx>0x27 → FAULT 0x326057
- 327CB0: b[rec+5]!=0 skip; 322C50 fail skip; pair tbl null →
  b[+0xBA]=0 + 12×pad FFFFFFFF + w[+0xB8]=0; early FFFF stop
- order bitmask w[5B10blk+0x30] bits → materialized entries
- ret values + d[rec] flag checks throughout
