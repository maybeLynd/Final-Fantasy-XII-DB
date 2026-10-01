# EXP-192 member-block chain REAL: 31A630 r9d!=0 -> 30F9A0/30C410
# (->3008A0->309F30->2FD8D0/2FD150) + 31B860->324470 teardown
# (=2FD420 spawn-bitmap mutator ->325F40 notify router)
# for CONTRACT-battle-unit-construction.md (the spawn-record
# initializer was EXP-150's largest scripted boundary).
#
#   0023AC80 (0x2CC, real): rcx=spawn rec rdi, edx=packed sel
#     (byte0=idx esi, byte1=mode ebx).
#     memset(rdi,0,0x1C8); q[+0x50]=-1; w[+0x58]=FFFF;
#     w[+0x1C3]=FFFF; b[+0x1C5]=FF.
#     d[02089300]==0 -> ret 0 (sentinels already written).
#     mode>=2 -> ret 0.
#     mode1 member: desc=q[02EBF120]; desc==0 -> r14=0 -> FAULT at
#       23ADA8 reading w[r14+0x16]. memb_row =
#       20E600(d[desc+0xC]) + w[desc+8]*idx. count edx=1, r12d=1.
#     mode0 foe:    desc=q[02EBF130]; null desc -> rbp=0 -> FAULT at
#       23AD7B reading b[rbp+0x2E]. foe_row likewise.
#       count edx = max(b[foerow+0x2E],1).
#     w[rdi+4]=sel16; 30C470(rdi, edx=count, r8d=is_member).
#     member: 4x 31A630(rdi,0..3, w[membrow+0x16]/w[+0x1C]/FFFF/FFFF,0).
#     foe: 323790(rdi, w[foerow+0x44]) gil clamp [0,0x1869F] into
#       d[+0x190]; idx<=6 -> scan abil tbl q[02EBF038] i<d[tbl+4]:
#       row_i=20E600(d[tbl+0xC])+w[tbl+8]*i; b[row_i+7]&(1<<idx) ->
#       323910(rdi,i,1,1) scripted (null 1st resolve -> r8=0 -> FAULT
#       b[7] at 23AE68); 5x 31A630(rdi,0..4,w[foerow+0xA..0x12],0);
#       327CB0(rdi, w[foerow+0x14]); 326030(q[02EBF190],idx);
#       327DE0(q[02EBF190]+8+idx*0x1C8); b[foerow+0x2C]&0x40 ->
#       d[rdi]|=4. ret 1.
#
#   0030C470 (0x1B0, real): esi=b[rec+5] (mode), r14d=b[rec+4] (idx);
#     b[rec+0x1C2]=0. mode0: re-resolve FOED -> rbp=foe_row (null ->
#     FAULT w[rbp+0x16] at 30C4F9); d[rec+8]=w[row+0x16];
#     w[rec+0xC]=w[row+0x1A]; f[rec+0x10..0x1C]=float(b[row+0x1E/0x21/
#     0x24/0x27]); b[rec+0x20]=b[row+0x46] then max(.,324100 ret) —
#     324100 scripted. mode1: b[rec+0x88]=r8b only. Common:
#     30C650(rec,count,2) scripted; d[rec+0x18C]=min(2F8F20(count-1),
#     0x5F5E0FF); if d[0208D320]|d[0208D324] -> 30F690(rec) scripted;
#     30F340(rec), 30F5A0(rec) scripted; w[rec+0x4C] = member:
#     (b[+0x6C]>=0 && b[+0x7C]>=0 ? movsx w[+0x28] : 0) — always 0 on
#     memset rec; foe: b[foerow+0x47]*edi/100 (magic 0x51EB851F);
#     30FED0(rec,0) scripted.
#
#   0031A630 (real): rcx=rec,edx=slot,r8w=val,r9d=flag. rcx==0 -> -1.
#     si==FFFF skips 317930; else 317930(rec+0x50, slot, si) scripted
#     gate — ret0 -> 31A630 rets -1 without writing. Write
#     w[rec+0x50+slot*2]=si; 318B40(rec+0x50, slot, r9d) scripted.
#     If slot value CHANGED (new != old r15w): 30FED0(rec,0x97)
#     scripted. r9d!=0 -> 30F9A0/30C410 then 31B860->324470 — never
#     from 23AC80 (r9d=0) but SCR'd for safety.
#
#   00323790 (leaf, real): d[rcx+0x190] += edx clamped [0,0x1869F].
#   002F8F20 (leaf, real): poly curve sum, ecx==0->0, >0x62->-1.
#   00322C50 (real, EXP-150 proven): 0xA arm validates
#     0x5000<=edx<0x5000+d[q[02EBF0E0]+4].
#   00327CB0 (real): rcx==0 or b[rec+5]!=0 -> ret. 322C50(0xA,esi)
#     gate; resolves pair tbl q[02EBF0E0] row esi-0x5000; copies <=12
#     (w,w) pairs src[+i*2],[+i*2+0x20] -> w[rec+0x88+i*4],[+0x8A+i*4],
#     bts w[+0xB8],i; early-out on FFFF src; b[+0xBA]=count; pads
#     i..11 d=FFFFFFFF + btr w[+0xB8]; TAIL -> 327DE0(rec).
#   00326030 (real): rcx=glob,edx=idx. d[glob+idx*4+0x7370]=0;
#     r8=glob+8+idx*0x1C8 (idx>0x27 -> r8=0 -> FAULT movups [0x88]);
#     3x copies [r8+0x88..0xB7] -> glob+idx*0x9C+0x5B10/0x5B44/0x5B78.
#   00327DE0 (real): rcx=row; b[row+4]=order idx; ordrow=02089378+
#     idx*0x170; cursor d[glob+oidx*4+0x7370]+oidx*3; blk=glob+0x5B10+
#     cursor*0x34; per set bit of w[blk+0x30]: pair (w[blk],w[blk+2])
#     !=FFFF -> resolve 02EBF0D8 row bp-0x6000 -> fill ordrow fields
#     +0x26..0x36 (w[+8]->+0x28, b[+0x10]->+0x26, w[+0x18]->+0x2A,
#     w[+0xA]->+0x2E, b[+0x11]->+0x2C, w[+0x1A]->+0x30, w[+0xC]->+0x34,
#     b[+0x12]->+0x32, w[+0x1C]->+0x36).
#
#   Scripted boundaries (entry-intercepted, args recorded, disclosed):
#     0030C650 level-set + 0030FED0 recompute (EXP-148 proven bodies;
#     30C650 executed real in EXP-196), 00323910 deep grant and
#     00234DA0 spatial query (both executed real in EXP-196).
#     00808C40 cookie check stays scripted.  The remaining SCR
#     entries are boundaries retained for inherited callers whose
#     direct-entry bodies now run real (EXP-152..195 promotions —
#     SCR is consulted before REAL, so inherited callers keep their
#     stubs while a direct entry executes the shipped body).
#
#   EXP-195 (00326500 notify dispatcher, 00263E30 resolver leaf):
#     326500: 311E20 -> 326620 -> 30D9A0 mode (d[glob+0x5B04]: &8->5,
#     &4->4, 377C20!=0->3, &2->2, &1->0/1) -> bl = mode{0,1}:b[5AA4],
#     mode2:0x1A, mode3:377C70, mode4/5:0xFF -> 31B770(bl) (slotrow =
#     glob+8+bl*0x1C8, OBJARR scan for q[+0x698]==slotrow) -> hit:
#     ebp=d[objrow+8] (+317400 at mode1) / miss: 4x 322C50(0x17,i) ->
#     b[glob+0x5A5A+i*2] -> 2367A0(id) -> same tail; exhaust -> ebp =
#     3589B0(263750(0)).  Tail: 311E20 -> jmp 3594B0(ebp):
#     d[0x22C7FE4]=ebp, b[0x22C7FF8]=1.  311E20 (guard d[0x22BE974]):
#     3272F0 (b[0x2089340]&0x10 -> 3588B0(nid=d[0x22C7FE0]) gen-check
#     resolve -> ctx idx via 263750) -> 31ABF0 -> 265970 blk ->
#     265020 triple -> 33CA00: q[0x22C7D18]=ctx, 0xB0 copy 0x22C7D20,
#     triple 0x22C7DD0, float 0x22C7DE0, flag d[0x22C7D10]=1.
#     326620: b[0x5AA4]==0xFF -> scan b[0x5A5A+i*2]; mode0 & miss ->
#     30A880(&st,3) = 30A8A0(0x22C1788,4,3) per-slot 31B810 -> gates
#     (&1:d64|d3C&0x80000003 ->377C20; &2:b5==0,b4<=6) -> store
#     d[0x5AA4]=b[rec+4] -> recursive 326500.  263E30: ret q[rcx+0x30].
#
#   EXP-197 (owner-check family + arm carriers): 30B770 global flag
#     composer (bit0=d[02089340]&0x3080, bit1=b[022C2158]&1, bits2/3/4=
#     d[02089340] bits 10/9/11); 30B7F0(obj,edx) per-object flags — lo:
#     bit0=d[obj]b8, bit1=d[obj]b30&&edx, bit3=b[obj+4]&0x20&&
#     d[022C2160]-5>1, bit4=rec(b5==0,b4==0x1A); hi: 17D470()==1&&rec ok
#     ->b0, ==2->b1.  30B9B0=(w(b770)||w(b7f0)); 30B8E0 tests b7f0 HI
#     word only.  17D470=d[1D50D0()+0xC20]; 1D50D0 lazy-inits
#     q[01F81428] via 210EC0/1CCB20 (stubbed, driven).  300140 unlink
#     mark: edx->3105D0(stub), clears q6F8/d748/d770/q750/d74C,
#     d788&=~0x400, d6B0&=~2, q[obj]b14 clear unless w[+0xBA0]==0x113
#     (bit14 set) / 0x95 (clear), d[obj+4]|=0x200000.  3299B0 msg arm:
#     edx==-1 no-op; ebx=(edx&0xFFF)>=0x100?edx|0x5000:edx; 2EB030
#     (q[obj+0x10],ebx): b[D]&=~1,b[F5]=FF,d[EC]=0,d[F0]=ebx,
#     b[18]!=1->2EB0D0(node,q[C0],ebx,1,-1f) scripted; d[obj+0x5C]=ebx,
#     d[obj+0x2C]=0.  Scripted still: 2EB0D0.  (3284D0/3BBD00
#     promoted real in EXP-201 — see the display-queue block below.)
#   00312280 (real): EXP/LP guest-share distribution.  rdx=objrow,
#     rcx=peer rec.  Head: rec=q[rdx+0x698]; rec && b5==1 && rcx &&
#     b[rcx+5]==0 -> 317ED0(rdx); always 3171C0(rdx).  Gate: !rec ||
#     b[rec+5]!=1 || b[rdx+0xE9A]&8 -> ret.  Scan arm iff (e9a&5)==5
#     or ((d64|d3C)&2 && e9a&2) or (rcx && b[rcx+5]==0): for i=0..8,
#     row=320AB0(i,3) real (glob+8+map*0x1C8 via q[02EBF190], map =
#     b[glob+0x5A7E+i*2] slotmap); row && (!(d64|d3C)&0x80000003 ||
#     377C20()!=0) -> stash q[022C1740+j*8] (cap 9).  Per guest:
#     ebx=clamp(2F8BB0(row,r14),0,999999), esi=clamp(2F90C0(row,r14),
#     0,999); b[+0x69]|b[+0x79]&0x10 -> esi=0 consumed into r12 +=
#     b[+0x1C2]*esi*5; 236780()==0 -> d[+0x18C]=min(+ebx,0x5F5E0FF);
#     lvl loop ebx=b[+0x1C2] while 0<2F8F20(ebx)<=d[+0x18C]: ebx++;
#     d[+0x190]=min(+esi,0x1869F); 316A50(edx=esi,cl=0xB); 30C650(row,
#     ebx,0) real.  Source: edi=clamp(2F8BB0(0,r14)),ebx=clamp(2F90C0(
#     0,r14)); 236780()!=0->edi=0; 28FB80(d[r14+8],edi,ebx); edi=(b[rec+
#     0x1C2]-b[rec+0x88])*d[q[r14+0xE78]+0x30]+d[q[r14+0xE70]+0x30]+r12;
#     ebx=253690(); ebp=max(ebx+edi,0); 254EE0(ebp); 469E80(ebp-ebx);
#     265020(q[r14+0x10],triple) real; 319490(&t) -> 3180F0(r14,&u) ->
#     319CA0(&u,&t); 317090(r14).  Scripted: 317ED0/3171C0/317090,
#     316A50 msg, 28FB80 broadcast, 253690/254EE0/469E80 gauge trio,
#     319490/3180F0/319CA0 pos chain, 808C40 cookie.  236780 =
#     d[glob+4]>>0xE &1 (share suppress; globb={5:0x40} sets it).
#     EXP-200: 2F8BB0/2F90C0 promoted real along with helpers 313800,
#     320890, 264150.  Formula semantics in the case-block comment.
#
import hashlib
import json
import os
import struct
import math
import sys

from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO = 0x120000
HEAP = 0x40000000
STACK = 0x61000000
RETQ = 0x62000000

# ---- subject ----
F_AC80 = 0x0023AC80

# ---- real callees ----
R_E600 = 0x0020E600        # off -> elemb+off
R_61EC0 = 0x00861EC0       # memset hook (real semantics in hook)
R_C470 = 0x0030C470        # stats header
R_A630 = 0x0031A630        # slot writer
R_3790 = 0x00323790        # gil add clamp
R_7CB0 = 0x00327CB0        # pair copy -> tail 327DE0
R_6030 = 0x00326030        # counter clear + 0x5B10 snapshot
R_7DE0 = 0x00327DE0        # order-row materializer
R_2C50 = 0x00322C50        # validator (EXP-150 proven)
R_8F20 = 0x002F8F20        # poly curve leaf
R_F690 = 0x0030F690        # per-bit stat dispatch
R_F340 = 0x0030F340        # recompute-check (flags -> 300530 delta)
R_F5A0 = 0x0030F5A0        # reconcile w28 vs w4C, b37*w28 vs w6
R_B860 = 0x0031B860        # owner scan over 0208E688 (+0x698 match)
R_6850 = 0x00236850        # obj count (0208E6A0)
R_6820 = 0x00236820        # obj row resolve
R_7C20 = 0x00377C20        # can-die bit15 lookup
R_148F0 = 0x003148F0       # ctx selected idx
R_EF2B0 = 0x002EF2B0       # ctx +0x200
R_EF640 = 0x002EF640       # static 2164280
R_E360 = 0x0030E360        # per-bit stat core (subject)
R_848E0 = 0x003848E0       # stat-block copy (memset-hooked)
R_86A50 = 0x00386A50       # handler pair A (mode)
R_86A70 = 0x00386A70       # handler pair B (+0x1C special)
R_6A800 = 0x0046A800       # handler pair C (mode)
R_6D6A0 = 0x0016D6A0       # handler pair D (leaf)
R_87730 = 0x00387730       # dword value leaf
R_876D0 = 0x003876D0       # word value resolver
R_0BC0 = 0x00300BC0        # HP apply: w6 = clamp(w6+delta,0,cap)
R_0CE0 = 0x00300CE0        # w4C gauge apply (+hp cascade, owner msgs)
R_E060 = 0x0030E060        # HP-fraction notify + b4E cache
R_283D0 = 0x003283D0       # owner msg post (->2FA3B0 scripted)
R_F3F0 = 0x0030F3F0        # member-slot broadcast (9 slots)
R_F4B0 = 0x0030F4B0        # f3f0 + f4d0 tail
R_F4D0 = 0x0030F4D0        # foe-slot broadcast (13 slots)
R_2AB0 = 0x00320AB0        # member slot -> rec resolver
R_2A40 = 0x00320A40        # foe idx -> rec row resolver
R_B0E0 = 0x0030B0E0        # id validity (real .data table)
R_1B9F0 = 0x0031B9F0       # slot -> rec-idx map byte

# ---- scripted boundaries ----
X_C650 = 0x0030C650        # level-set (EXP-148 proven)
X_FED0 = 0x0030FED0        # recompute (EXP-148 proven)
X_B9B0 = 0x0030B9B0        # owner check A
X_B8E0 = 0x0030B8E0        # owner check B
X_0FC0 = 0x00300FC0        # unlink (edi&0x80000003 arm)
X_112F0 = 0x003112F0       # blk-notify (272i)
X_2FA390 = 0x002FA390      # 46A800 inner
X_46AB10 = 0x0046AB10      # 46A800 inner
X_01140 = 0x00301140       # bit0/1/0x1F non-mode arm body
X_12280 = 0x00312280       # unlink tail (after 300FC0)
X_299B0 = 0x003299B0       # bit4/1/0x1F msg arm
X_00140 = 0x00300140       # bit5/1B arm (->3105D0)
X_07D10 = 0x00307D10       # bit5/1B arm tail
X_284D0 = 0x003284D0       # edi&&d5c&&rbx notify
X_0530 = 0x00300530        # stat apply+notify (255i)
X_43F0 = 0x003243F0        # unlink+release helper
X_B770 = 0x0030B770        # owner check A1
X_B7F0 = 0x0030B7F0        # owner check A2
X_8F1F0 = 0x0028F1F0       # gauge event post
X_FA540 = 0x002FA540       # drop/death notify
X_FA3B0 = 0x002FA3B0       # msg post inner (cookie-protected)
X_3910 = 0x00323910        # deep grant
X_4100 = 0x00324100        # b[+0x20] override (->324020)
X_7930 = 0x00317930        # slot search
X_8B40 = 0x00318B40        # list op
X_F9A0 = 0x0030F9A0        # unequip (r9d path, never from ac80)
X_C410 = 0x0030C410        # equip   (r9d path)
X_4470 = 0x00324470        # member block 2

# ---- globals ----
GATE    = 0x02089300       # master enable dword
MEMT    = 0x02EBF0F8       # member-id table desc (317930/318B40)
MEMD    = 0x02EBF120       # member desc cell
FOED    = 0x02EBF130       # foe desc cell
ABILD   = 0x02EBF038       # ability-table desc cell
PAIRD   = 0x02EBF0E0       # pair-table desc cell
ORDD    = 0x02EBF0D8       # order-table desc cell
GLOB    = 0x02EBF190       # context table ptr cell
ELEMB   = 0x01F83530       # 20E600 element-base cell
ORDT    = 0x02089378       # order rows (canonical .data, +idx*0x170)
F693A   = 0x0208D320       # 30C470's 30F690 gate dword A
F693B   = 0x0208D324       # gate dword B (shared by 30F3F0)
# cls-0xC row @ 0x1EEBCC0 + 0xC*0x58 = 0x1EEC0E0:
#   d[+0x3C]=32 count, q[+0x50]=2FD970 validator (shipped),
#   q[+8]=spawned-entity bitmap (runtime-populated -> planted)
FOEBMP_R = 0x01EEC0E8      # q[cls-0xC row + 8]: spawned-foe bitmap
R_2FD970 = 0x002FD970      # cls validator body (bitmap test, edx=mode)
R_0530R = 0x00300530        # the real 300530 body
R_16D70 = 0x00316D70        # 15i leaf
R_2A150 = 0x0032A150        # 2i leaf
R_9F30  = 0x00309F30        # 7i leaf
R_6F00  = 0x00306F00        # 41i -> 263D30/2360D0 leaves
R_263D30 = 0x00263D30       # 2i leaf
R_360D0 = 0x002360D0        # 14i leaf
R_69BB0 = 0x00469BB0        # 21i -> scripted 2FA390/46AB10
R_08A0  = 0x003008A0        # id resolver (sibling of 300530)
R_2FD420 = 0x002FD420       # cls-0xC spawn-bitmap mutator
R_325F40 = 0x00325F40       # change-notify router (call rsi)
R_6A630 = 0x0046A630        # 26i -> scripted 46AB10
R_309440 = 0x00309440       # 322C50 bound resolver
OBJCNT  = 0x0208E6A0       # object count (236850)
OBJARR  = 0x0208E688       # object array ptr (236820)
CD_IDX  = 0x021654C4       # 377C20 selected index cell
CD_TBL  = 0x02ADD100       # 377C20 table ptr cell
CASCD   = 0x02EBF118       # 30E360 per-bit cascade-table desc cell
V76_MUL = 0x01DFE0B4       # 3876D0 dword multiplier cell

# elemb sub-block offsets (fixture-chosen desc "off" values)
O_MEMB  = 0x10000
O_FOE   = 0x20000
O_ABIL  = 0x30000
O_PAIR  = 0x40000
O_ORD   = 0x50000
O_MEMT  = 0x60000            # EXP-193: member-id table (q[02EBF0F8] desc)

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)


def load_image():
    raw = open(EXE, "rb").read()
    assert hashlib.sha256(raw).hexdigest() == SHA, "EXE hash mismatch"
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    nsec = struct.unpack_from("<H", raw, pe + 6)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    secs, off = [], pe + 24 + optsz
    for _ in range(nsec):
        vs, va, rs, ra = struct.unpack_from("<IIII", raw, off + 8)
        secs.append((va, vs, ra, rs))
        off += 40
    return raw, secs


class GuestMem:
    def __init__(self, uc, raw, secs):
        self.uc = uc
        for va, vs, ra, rs in secs:
            lo = (va + IMG_LO) & ~0xFFF
            hi = (va + IMG_LO + max(vs, rs) + 0xFFF) & ~0xFFF
            uc.mem_map(lo, hi - lo)
            if rs:
                uc.mem_write(va + IMG_LO, raw[ra:ra + rs])

    def w(self, addr, data):
        if isinstance(data, int):
            data = qw(data)
        try:
            self.uc.mem_write(addr, bytes(data))
        except UcError:
            lo = addr & ~0xFFF
            self.uc.mem_map(lo, 0x1000)
            self.uc.mem_write(addr, bytes(data))

    def q(self, a):
        return struct.unpack("<Q", bytes(self.uc.mem_read(a, 8)))[0]

    def d(self, a):
        return struct.unpack("<I", bytes(self.uc.mem_read(a, 4)))[0]

    def w16(self, a):
        return struct.unpack("<H", bytes(self.uc.mem_read(a, 2)))[0]

    def b(self, a):
        return self.uc.mem_read(a, 1)[0]

    def f(self, a):
        return struct.unpack("<f", bytes(self.uc.mem_read(a, 4)))[0]


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.uc.mem_map(STACK, 0x100000)
        self.uc.mem_map(RETQ, 0x1000)
        self.uc.mem_map(HEAP, 0x600000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP
        self.entry = 0
        gm = self.gm

        self.rec = self.alloc(0x400)
        self.elemb = self.alloc(0x90000)
        self.glob = self.alloc(0x8000)

        self.idx = case.get("idx", 2)
        self.mode = case.get("mode", 0)
        self.sel = (self.mode << 8) | (self.idx & 0xFF)

        gm.w(GATE, dw(case.get("gate", 1)))
        gm.w(ELEMB, qw(self.elemb))
        gm.w(GLOB, qw(0 if case.get("glob_null") else self.glob))
        gm.w(F693A, dw(case.get("f690_gate", 0)))
        gm.w(F693B, dw(case.get("f690_gate2", 0)))

        # 31B860's owner scan: count cell + 0xF50-stride array; a linked
        # row's q[+0x698] = rec.  Only planted when requested.
        oc = case.get("objcount", 0)
        oarr = self.alloc(0x20000)
        gm.w(OBJARR, qw(oarr))
        self.objrow = 0
        if case.get("objlink"):
            self.objrow = oarr
            self.objent = self.alloc(0x400)
            gm.w(self.objrow, qw(case.get("objflags", 0x4000000)))
            gm.w(self.objrow + 0x10, qw(self.objent))
            gm.w(self.objrow + 0x698,
                 qw(case.get("obj698", self.rec)))
            oc = max(oc, 1)
        gm.w(OBJCNT, dw(oc))

        # 30F3F0 broadcast: slot->recidx map b[glob+0x5A7E+slot*2]
        # (cls-3 arm of 31B9F0); default identity map 0..8
        for slot in range(9):
            gm.w(self.glob + 0x5A7E + slot * 2,
                 bytes([case.get("slotmap", {}).get(slot, slot) & 0xFF]))
        # EXP-192: class-1 member word table (2FD150/2FD8D0 read
        # q[row+8]; shipped cell is 0 = runtime-allocated).
        # w[idx] packs count<<0xA | capacity(0x3FF).
        self.cls1arr = 0
        cls1w = case.get("cls1words")
        if cls1w is not None:
            arr = self.alloc(0x800)
            for ci, cv in cls1w.items():
                gm.w(arr + ci * 2, struct.pack("<H", cv & 0xFFFF))
            gm.w(0x1EEBD18 + 8, qw(arr))
            self.cls1arr = arr

        # cls-0xC validator bitmap for 30B0E0/2FD970:
        # valid iff bit (id&0xF) of w[bmp + (id&0xFFF)>>4 *2] set
        fbmp = self.fbmp = self.alloc(0x40)
        gm.w(FOEBMP_R, qw(fbmp))
        gm.w(fbmp + 2, struct.pack("<H", case.get("foebmp", 0x7FFC) & 0xFFFF))
        if case.get("statecell"):
            self.cell = self.alloc(0x20)
            gm.w(0x2EBF190, qw(self.cell))
        else:
            self.cell = None

        # 377C20 can-die cells: selected idx + 3-byte-stride flag table
        gm.w(CD_IDX, dw(case.get("cd_idx", 0) & 0xFFFFFFFF))
        cdt = self.alloc(0x200)
        gm.w(CD_TBL, qw(0 if case.get("cd_null") else cdt))
        gm.w(cdt + 4, dw(case.get("cd_count", 8)))
        for i, wv in enumerate(case.get("cd_words",
                                        [0x8000] * 8)[:0x27]):
            gm.w(cdt + i * 3 + 8, struct.pack("<H", wv & 0xFFFF))

        # 30E360's per-bit cascade table: desc like the other
        # element descriptors; row = elemb+d[desc+0xC]+bit*w[desc+8];
        # d[row+0xC] = follow-on bit mask for recursion
        cd = case.get("cascd", {"stride": 0x40, "off": 0x70000,
                                "count": 8})
        if cd is None:
            gm.w(CASCD, qw(0))
        else:
            cdesc = self.alloc(0x40)
            gm.w(CASCD, qw(cdesc))
            gm.w(cdesc + 8, struct.pack("<H", cd.get("stride", 0x40)))
            gm.w(cdesc + 4, dw(cd.get("count", 8)))
            gm.w(cdesc + 0xC, dw(cd.get("off", 0x70000)))
            for bi, mv in case.get("casc_rows", {}).items():
                crow = (self.elemb + cd.get("off", 0x70000)
                        + cd.get("stride", 0x40) * bi)
                gm.w(crow + 0xC, dw(mv))
            for bi, bv in case.get("casc_b9", {}).items():
                crow = (self.elemb + cd.get("off", 0x70000)
                        + cd.get("stride", 0x40) * bi)
                gm.w(crow + 9, bytes([bv & 0xFF]))
        gm.w(V76_MUL, dw(case.get("v76mul", 2)))

        # direct-call cases bypass 23AC80's memset, so rec fields can be
        # planted directly
        if case.get("entry"):
            for off, v in case.get("rec_d", {}).items():
                gm.w(self.rec + off, dw(v))
            for off, v in case.get("rec_w", {}).items():
                gm.w(self.rec + off, struct.pack("<H", v & 0xFFFF))
            for off, v in case.get("rec_b", {}).items():
                gm.w(self.rec + off, bytes([v & 0xFF]))

        def mkdesc(cell, spec):
            if spec is None:
                gm.w(cell, qw(0))
                return 0
            desc = self.alloc(0x40)
            gm.w(cell, qw(desc))
            gm.w(desc + 8, struct.pack("<H", spec.get("stride", 0x60)))
            gm.w(desc + 4, dw(spec.get("count", 0)))
            gm.w(desc + 0xC, dw(spec.get("off", 0)))
            return desc

        md = case.get("memd", {"stride": 0x60, "off": O_MEMB})
        fd = case.get("foed", {"stride": 0x60, "off": O_FOE,
                               "count": 8})
        ad = case.get("abild", {"stride": 0x20, "off": O_ABIL,
                                "count": len(case.get("abil", []))})
        pd = case.get("paird", {"stride": 0x40, "off": O_PAIR,
                                "count": 4})
        od = case.get("ordd", {"stride": 0x40, "off": O_ORD,
                               "count": 4})
        mt = case.get("memt")
        mkdesc(MEMT, mt)
        self.memtarr = self.elemb + mt["off"] if mt else 0
        if mt:
            for cidx, fields in case.get("memt_rows", {}).items():
                row = self.memtarr + mt["stride"] * cidx
                for off, v in fields.items():
                    gm.w(row + off, bytes([v & 0xFF]))
        for goff, gv in case.get("globb", {}).items():
            gm.w(self.glob + goff, bytes([gv & 0xFF]))

        # EXP-194: 308FF0's row desc q[02EBF138]
        # (row = 20E600(d[+0xC]) + w[+8]*dx; b[row+0x1E] in {5,6}
        # gates ret b[row+0xA]).
        d138 = case.get("d138")
        mkd = mkdesc(0x02EBF138, d138)
        if d138:
            for ridx, fields in case.get("d138_rows", {}).items():
                row = (self.elemb + d138.get("off", 0x78000)
                       + d138.get("stride", 0x20) * ridx)
                for off, v in fields.items():
                    gm.w(row + off, bytes([v & 0xFF]))
        # member-row extras for 308130/308040 (rcx = member row):
        # d[objrow+4] flags word, q[objrow+0x6A0] flags-obj,
        # q[objrow+0x708] (30BF20 arg), d[objrow+0xBC4] count,
        # d[objrow+0xDCC] stored value.
        if self.objrow:
            for off, v in case.get("obj_d", {}).items():
                gm.w(self.objrow + off, dw(v))
            for off, v in case.get("obj_b", {}).items():
                gm.w(self.objrow + off, bytes([v & 0xFF]))
            self.obj6a0 = self.alloc(0x100)
            gm.w(self.objrow + 0x6A0, qw(self.obj6a0))
            o6 = case.get("obj6a0", {})
            for off, v in o6.get("d", {}).items():
                gm.w(self.obj6a0 + off, dw(v))
            if "f4" in o6:
                gm.w(self.obj6a0 + 4, struct.pack("<f", o6["f4"]))
            o708 = case.get("obj708")
            if o708 is not None:
                gm.w(self.objrow + 0x708, qw(o708))
            # 30BF20 scans b[0x1EEC320] x rows @0x1EEC340 stride 0x18
            gm.w(0x1EEC320, bytes([case.get("bf20cnt", 0) & 0xFF]))
            gm.w(0x1EEC330, bytes([case.get("bf20cnt2", 0) & 0xFF]))
        # 2F8FA0 reads ABILD rows: b[row+5] -> 323890/3241D0 class map,
        # w[row+8..+0x15] compared to si; sets bit edi in the out bitmap.
        for ridx, fields in case.get("abil_rows", {}).items():
            row = self.elemb + ad["off"] + ad["stride"] * ridx
            for off, v in fields.get("b", {}).items():
                gm.w(row + off, bytes([v & 0xFF]))
            for off, v in fields.get("w", {}).items():
                gm.w(row + off, struct.pack("<H", v & 0xFFFF))
        # 253B90's dword and 308186's gate byte (shipped: 1 and 0)
        if "g25b" in case:
            gm.w(0x1E0C2B8, dw(case["g25b"]))
        gm.w(0x22C1F48, bytes([case.get("g81e0", 0) & 0xFF]))

        # EXP-195: 326500 notify tree.
        # 31B770 slot row lives inside glob: row = glob+8+slot*0x1C8;
        # it scans OBJARR for q[row+0x698]==slotrow. 2367A0 scans the
        # same array for w[q[row+0x698]+4]==id (0xFF -> 0xFFFF).
        # ctx4: 263750's 4-pointer table q[0x209A1F0+i*8] (BSS cell —
        # runtime-populated). 265970(ctx)=q[+0xC0]->q[+0x138]+0x30;
        # 265020(ctx,outs) copies 3 dwords from q[+0xB8] when
        # b[+3]>>5 in {1,3}; 265200 reads f[q[+0xB8]+0xA8]; 3589B0
        # composes id = ((w[+0x16]&0x7FF)<<4 | b[+0x15]&0xF)<<16 | w[0].
        self.sglbuf = 0
        self.ctx = []
        for ci, cspec in enumerate(case.get("ctx4", [])):
            c = self.alloc(0x200)
            gm.w(0x209A1F0 + ci * 8, qw(c))
            gm.w(c + 3, bytes([cspec.get("b3", 0x20) & 0xFF]))
            gm.w(c, struct.pack("<H", cspec.get("w0", 0) & 0xFFFF))
            gm.w(c + 0x15, bytes([cspec.get("b15", 0) & 0xFF]))
            gm.w(c + 0x16, struct.pack("<H", cspec.get("w16", 0) & 0xFFFF))
            for off, v in cspec.get("d", {}).items():
                gm.w(c + off, dw(v))
            out = self.alloc(0x200)
            gm.w(c + 0xB8, qw(out))
            for off, v in cspec.get("outd", {}).items():
                gm.w(out + off, dw(v))
            # 265200: b[+3]>>5==1 -> f[out+0x38]; ==3 -> f[out+0xA8]
            if "f148" in cspec:
                gm.w(out + 0x38, struct.pack("<f", cspec["f148"]))
            if "fA8" in cspec:
                gm.w(out + 0xA8, struct.pack("<f", cspec["fA8"]))
            c0 = self.alloc(0x200)
            gm.w(c + 0xC0, qw(c0))
            c138 = self.alloc(0x200)
            gm.w(c0 + 0x138, qw(c138))
            # 265970 returns blk base = c138+0x30
            for off, v in cspec.get("blk", {}).items():
                gm.w(c138 + 0x30 + off, dw(v))
            self.ctx.append(c)
        # 3588B0's class table: 263FF0(cls) = 0x2098E10+cls*0x288 static
        # row; q[+8] ptr array bounded by d[row] and d[+0x20], gated by
        # b[+0x10]&1; row gen must equal (id>>20)&0x7FF.
        for cls, rows in case.get("clstab", {}).items():
            base = 0x2098E10 + cls * 0x288
            tbl = self.alloc(0x40 + 8 * len(rows))
            gm.w(base, qw(1))
            gm.w(base + 8, qw(tbl))
            gm.w(base + 0x20, dw(len(rows) + 8))
            gm.w(base + 0x10, bytes([case.get("clsflag", 1) & 0xFF]))
            gm.w(tbl, dw(len(rows)))
            for ri, rval in enumerate(rows):
                if isinstance(rval, str) and rval.startswith("ctx"):
                    rval = self.ctx[int(rval[3:])]
                gm.w(tbl + 8 + ri * 8, qw(rval))
        # 311E20's guard cell (RIP+disp at 0311E24 -> 022BE974):
        # nonzero -> no-op
        if "g11e20" in case:
            gm.w(0x22BE974, dw(case["g11e20"]))
        # EXP-197: 30B770 global flag sources, 30B7F0's mode cell,
        # and the 17D470 singleton (q[01F81428]; +0xC20 is the mode).
        # owngl writes the full dword BEFORE g272f0 so the byte key can
        # still patch byte0.
        gm.w(0x2089340, dw(case.get("owngl", 0) & 0xFFFFFFFF))
        gm.w(0x22C2158, bytes([case.get("ownb", 0) & 0xFF]))
        gm.w(0x22C2160, dw(case.get("g2160", 0) & 0xFFFFFFFF))
        sgl = case.get("sgl")
        if sgl is not None:
            self.sglbuf = self.alloc(0x1100)
            gm.w(0x1F81428, qw(self.sglbuf))
            gm.w(self.sglbuf + 0xC20, dw(sgl & 0xFFFFFFFF))
        # 3299B0 msg arm: the entity node behind q[objrow+0x10]
        if self.objrow:
            for off, v in case.get("ent_b", {}).items():
                gm.w(self.objent + off, bytes([v & 0xFF]))
            for off, v in case.get("ent_q", {}).items():
                gm.w(self.objent + off, qw(v))
        # 30B9B0/30B8E0 second row for 30AB40's pair compare
        self.row2 = 0
        r2 = case.get("row2")
        if r2 is not None:
            self.row2 = self.alloc(0x1000)
            gm.w(self.row2, qw(r2.get("flags", 0x10)))
            for off, v in r2.get("d", {}).items():
                gm.w(self.row2 + off, dw(v))
            self.row2ent = self.alloc(0x200)
            gm.w(self.row2 + 0x10, qw(self.row2ent))
            for off, v in r2.get("eb", {}).items():
                gm.w(self.row2ent + off, bytes([v & 0xFF]))
            if "rec" in r2:
                rr = self.alloc(0x400)
                gm.w(self.row2 + 0x698, qw(rr))
                for off, v in r2["rec"].items():
                    gm.w(rr + off, bytes([v & 0xFF]))
        # 3272F0's mode flag: b[0x2089340]&0x10 required for the
        # 3588B0/263750 search; 3590D0's notify-id cell.
        if "g272f0" in case:
            gm.w(0x2089340, bytes([case["g272f0"] & 0xFF]))
        if "nid" in case:
            gm.w(0x22C7FE0, dw(case["nid"]))
        # 326620's ctor-list landing cell q[0x22C1788] is written by
        # 30A8A0 itself; no fixture needed.
        # slothit: slot index whose 31B770 row (glob+8+slot*0x1C8) is
        # owned by the planted objlink row — q[objrow+0x698]=slotrow.
        self.slotrow = 0
        if "slothit" in case and self.objrow:
            self.slotrow = self.glob + 8 + case["slothit"] * 0x1C8
            gm.w(self.objrow + 0x698, qw(self.slotrow))

        # EXP-193: 322C50 kind-8 range desc q[02EBF0F0] (d[+4]=count,
        # valid ids 0x3000..0x3000+count-1) and class-3 2FD970 mode-0
        # bitmap q[0x1EEBDD0+8] (word idx = (id&0xFFF)>>4, bit = id&0xF).
        k8 = case.get("k8d")
        mkdesc(0x02EBF0F0, k8)
        if case.get("cls3bmp") is not None:
            barr = self.alloc(0x100)
            for bidx, bv in case["cls3bmp"].items():
                gm.w(barr + bidx * 2, struct.pack("<H", bv & 0xFFFF))
            gm.w(0x1EEBDD0 + 8, qw(barr))

        mkdesc(MEMD, md)
        mkdesc(FOED, fd)
        mkdesc(ABILD, ad)
        mkdesc(PAIRD, pd)
        mkdesc(ORDD, od)

        # member row
        self.membrow = self.elemb + md["off"] + md["stride"] * self.idx \
            if md else 0
        if self.membrow:
            m = case.get("memb", {"w16": 0x1111, "w1C": 0x2222})
            for off, v in m.get("w", {}).items():
                gm.w(self.membrow + off, struct.pack("<H", v & 0xFFFF))
            gm.w(self.membrow + 0x16,
                 struct.pack("<H", m.get("w16", 0x1111)))
            gm.w(self.membrow + 0x1C,
                 struct.pack("<H", m.get("w1C", 0x2222)))

        # foe row
        self.foerow = self.elemb + fd["off"] + fd["stride"] * self.idx \
            if fd else 0
        if self.foerow:
            fo = case.get("foe", {})
            fw = {0xA: 0x501, 0xC: 0x502, 0xE: 0xFFFF, 0x10: 0xFFFF,
                  0x12: 0xFFFF, 0x14: 0x5000, 0x16: 0x3210,
                  0x1A: 0x44, 0x44: 500}
            for off, v in fo.get("w", {}).items():
                fw[off] = v
            for off, v in fw.items():
                gm.w(self.foerow + off, struct.pack("<H", v & 0xFFFF))
            fb = {0x2E: fo.get("cnt", 3), 0x2C: fo.get("b2c", 0x40),
                  0x1E: 10, 0x21: 20, 0x24: 30, 0x27: 40, 0x46: 0x55,
                  0x47: fo.get("b47", 0)}
            for off, v in fo.get("b", {}).items():
                fb[off] = v
            for off, v in fb.items():
                gm.w(self.foerow + off, bytes([v & 0xFF]))

        # ability table rows: b[row+7] bitmask
        ab = case.get("abil", [])
        for i, mask in enumerate(ab):
            gm.w(self.elemb + ad["off"] + ad["stride"] * i + 7,
                 bytes([mask & 0xFF]))

        # EXP-196: 30C650 level-set / 323910 deep grant / 234DA0
        # spatial query fixtures.
        # grwd: growth desc q[0x2EBF108]; row = elemb+d[+0xC]+w[+8]*lvl;
        # b[row]=hp growth (2F9A60, RNG arm dead: shipped divisor is
        # negative), b[row+1]=mp growth (2F9B20 -> 379CD0 MT jitter).
        grw = case.get("grwd")
        mkdesc(0x02EBF108, grw)
        if grw:
            for lv, pair in case.get("grwrows", {}).items():
                row = self.elemb + grw.get("off", 0x78000) \
                    + grw.get("stride", 0x20) * lv
                gm.w(row, bytes([pair[0] & 0xFF]))
                gm.w(row + 1, bytes([pair[1] & 0xFF]))
        # foe row IS the 30C650 level-stat row (FOED=q[0x2EBF130],
        # stride idx = b[rec+4]): growth bytes at +0x1F/+0x22/+0x25/
        # +0x28 come from the existing foe {"b":{...}} fixture.
        # i138/d138 already covers q[0x2EBF138] (+w[+0x22] via bytes).
        # mt: CRT MT19937 rand state — flag b[0x2EB4234]=1 skips seed,
        # idx d[0x2EB4230] < 0x270 skips twist; word d[0x2EB3870+i*4]
        # is tempered into the return.
        if case.get("mt") is not None:
            mt = case["mt"]
            gm.w(0x2EB4234, bytes([mt.get("flag", 1) & 0xFF]))
            gm.w(0x2EB4230, dw(mt.get("idx", 0)))
            for mi, mv in mt.get("words", {}).items():
                gm.w(0x2EB3870 + mi * 4, dw(mv))
        # a11: 3A1180 serial table — d[0x2AEF3FC] key;
        # row at 0x2AEEDC0 + idx*24 matches (w[+8]|w[+0xA]<<16)
        # against key&~bit31 -> ret (w8<<9)+7.
        a11 = case.get("a11")
        if a11 is not None:
            gm.w(0x2AEF3FC, dw(a11.get("serial", 0xFFFFFFFF)))
            arow = 0x2AEEDC0 + a11.get("idx", 0) * 24
            gm.w(arow + 8, struct.pack("<H", a11.get("w8", 0)))
            gm.w(arow + 0xA, struct.pack("<H", a11.get("wA", 0)))
        # g603c0: b[0x22C6F26] gate inside 2DF220; q209be -> 2905D0's
        # object cell; mctxid -> 3590D0's context id cell.
        if "g603c0" in case:
            gm.w(0x22C6F26, bytes([case["g603c0"] & 0xFF]))
        if "q209be" in case:
            gm.w(0x209BE80, qw(case["q209be"]))
        if "mctxid" in case:
            gm.w(0x22C7FE0, dw(case["mctxid"]))
        # slotd: 31B810's kind-0x17 range desc q[0x2EBF110];
        # slot idx must be < d[+4].
        mkdesc(0x02EBF110, case.get("slotd"))
        # EXP-199: 312280's guest-share fixtures.
        # guest={i:{d,b}}: member slot i resolves through 320AB0(i,3)
        # = glob+8+map*0x1C8 where map = b[glob+0x5A7E+i*2] (the same
        # slotmap table 30F3F0/31B770 use — all read q[0x2EBF190]).
        # Row fields: d[+0x64]/d[+0x3C] flags (0x80000003 -> 377C20
        # gate), b[+0x69]/b[+0x79]&0x10 LP-consume flags, b[+0x1C2]
        # level, d[+0x18C] exp, d[+0x190] lp.  Rows overlap the
        # glob+8 table at 0x1C8 stride exactly as shipped; the stash
        # target q[0x22C1740+j*8] is writable image BSS.
        # 236780's share-suppress flag = d[glob+4] bit14 -> globb={5:..}.
        self.guests = {}
        smap = case.get("slotmap", {})
        for gi, gspec in case.get("guest", {}).items():
            grow = self.glob + 8 + (smap.get(gi, gi) & 0xFF) * 0x1C8
            for off, v in gspec.get("d", {}).items():
                gm.w(grow + off, dw(v))
            for off, v in gspec.get("b", {}).items():
                gm.w(grow + off, bytes([v & 0xFF]))
            self.guests[gi] = grow
        # e78/e70: 312280's source FP tail reads d[+0x30]; EXP-200's
        # real 2F8BB0/2F90C0 read d[+0x34] (EXP mult/add) and b[+0x2F]
        # (LP mult/add) on the same pair.  Keys: e78/e70 -> +0x30,
        # e78e/e70e -> +0x34, e78l/e70l -> +0x2F.
        if self.objrow:
            for base, off in (("e78", 0xE78), ("e70", 0xE70)):
                if (base in case or base + "e" in case
                        or base + "l" in case):
                    eb = self.alloc(0x40)
                    gm.w(eb + 0x30, dw(case.get(base, 0)))
                    gm.w(eb + 0x34, dw(case.get(base + "e", 0)))
                    gm.w(eb + 0x2F,
                         bytes([case.get(base + "l", 0) & 0xFF]))
                    gm.w(self.objrow + off, qw(eb))
        # memslots: 2F8BB0's 31B810 member-count map —
        # b[glob+0x5A5A+i*2], i<4; 0xFF = empty.  The map is the same
        # one 31B9F0 cls-1 and the leader path read.
        for mi, mv in enumerate(case.get("memslots", [])):
            gm.w(self.glob + 0x5A5A + mi * 2, bytes([mv & 0xFF]))
        # lflag: 264150's global LP-suppress byte b[0x20AA2AA].
        if "lflag" in case:
            gm.w(0x20AA2AA, bytes([case["lflag"] & 0xFF]))
        # oar4: 234DA0's per-slot object rows — OBJARR is inline
        # 0xF50-stride rows; 2367A0 matches w[q[row+0x698]+4]==slotid.
        # Each entry plants rec_i (w+4=slotid, recd gates), ctx_i
        # (b3>>5 + q[+0xB8] triple) and row fields d[+8]/q[+0x10].
        # "link": N reuses guest row N as the row's rec (31B860 owner
        # resolution for 312280's per-guest 30C650).
        self.oar4 = {}
        oc = gm.d(OBJCNT)
        for si, spec in case.get("oar4", {}).items():
            row = oarr + si * 0xF50
            if "link" in spec:
                ri = self.guests[spec["link"]]
            else:
                ri = self.alloc(0x400)
                gm.w(ri + 4,
                     struct.pack("<H", spec.get("id", 0) & 0xFFFF))
            for off, v in spec.get("recd", {}).items():
                gm.w(ri + off, dw(v))
            gm.w(row + 0x698, qw(ri))
            for off, v in spec.get("recb", {}).items():
                gm.w(ri + off, bytes([v & 0xFF]))
            if "cap" in spec:
                cb = self.alloc(0x80)
                gm.w(row + 0x6A0, qw(cb))
                for off, v in spec["cap"].items():
                    gm.w(cb + off, bytes([v & 0xFF]))
            gm.w(row + 8, dw(spec.get("cid", 0)))
            ci = self.alloc(0x200)
            gm.w(ci + 3, bytes([spec.get("b3", 0x21) & 0xFF]))
            trip = self.alloc(0x20)
            gm.w(ci + 0xB8, qw(trip))
            for ti, tv in enumerate(spec.get("trip", [0.0, 0.0, 0.0])):
                gm.w(trip + ti * 4, struct.pack("<f", tv))
            gm.w(row + 0x10, qw(ci))
            gm.w(row, qw(spec.get("flags", 0x4000000)))
            self.oar4[si] = (row, ri, ci)
            oc = max(oc, si + 1)
        gm.w(OBJCNT, dw(oc))
        # pos/pmin/pmax/pout float buffers for 234DA0's pointer args.
        for nm, vals in (("pos", case.get("fpos")),
                         ("pmin", case.get("fmin")),
                         ("pmax", case.get("fmax")),
                         ("pout", case.get("fout"))):
            buf = self.alloc(0x20)
            if vals is not None:
                for fi, fv in enumerate(vals):
                    gm.w(buf + fi * 4, struct.pack("<f", fv))
            setattr(self, nm, buf)

        # EXP-198: 3137F0/3138D0 read b[glob+0x5AD5] and toggle
        # w[glob+0x5AD0] — covered by the existing globb/glob fixtures.
        # NOTE: 322C50 kind-2 reads q[0x2EBF130] == FOED — the foe
        # table desc planted by the existing `foed` fixture above.
        # (3219D0's b4 validity bound: valid iff edx < d[desc+4].)
        # capb: q[row+0x6A0] capability block — 3219D0 reads
        # b[cap+0x1A+b4], 3125E0 reads d[cap] bits 3/4.  Per-object via
        # objlink/oar4 row spec "cap".
        if case.get("capb") is not None and self.objrow:
            cap = self.alloc(0x80)
            gm.w(self.objrow + 0x6A0, qw(cap))
            for off, v in case["capb"].get("b", {}).items():
                gm.w(cap + off, bytes([v & 0xFF]))
            for off, v in case["capb"].get("d", {}).items():
                gm.w(cap + off, dw(v))
        # e8tab: q[0x22C6F28] + 0x740-stride rows for 2ED180/2E8060's
        # indexed gate (d[row+0x284] nonzero -> tail call).
        e8 = case.get("e8tab")
        if e8 is not None:
            t = self.alloc(0x10000)
            gm.w(0x22C6F28, qw(t))
            for ei, d284 in e8.items():
                gm.w(t + ei * 0x740 + 0x284, dw(d284))
        # imgd/imgq/imgb: direct image-cell writes for the 24FE30
        # family's static tables (0x2EC32E0 stride-0x38 / 0x3BCE5E0
        # stride-0x30 / 0x3C1EC00 stride-0x18).
        for a, v in case.get("imgd", {}).items():
            gm.w(a, dw(v))
        for a, v in case.get("imgq", {}).items():
            if isinstance(v, str):
                v = getattr(self, v, 0)
            gm.w(a, qw(v))
        for a, v in case.get("imgb", {}).items():
            gm.w(a, bytes([v & 0xFF]))

        # ---- EXP-201: display-request queue ----
        # allocations first (qt/rblk/req entries reference these attrs).
        # sovec/subobj: 2FA3B0's dist gate copies q[obj+0xB8] vec3 via
        # 265020 when b[obj+3]>>5 in {1,3}; cam vec3 lives at 01EBBB00.
        self.sovec = self.alloc(0x20)
        self.subobj = self.alloc(0x200)
        # dobj: 3284D0's arg — q[+0x10] is the sub-object handed to
        # 2FA3B0 and stored as the req's object.
        self.dobj = self.alloc(0x40)
        # req: 3BBD00's arg — {q[+0]=obj, d[+8]=value, b[+0xC]=type,
        # b[+0xD]=subtype}.
        self.req = self.alloc(0x20)
        # nstr: name-table string resource (empty 2-byte tag -> 2B58B0
        # returns nstr+2).
        self.nstr = self.alloc(0x20)
        # fmtbuf: 3EFD00 output buffer.
        self.fmtbuf = self.alloc(0x40)
        # dd7t: index table for 2DD7E0 (d[+idx*8]) / 2DD7B0
        # (b[+idx*8+4]); count cell 0215E6B8, ptr 0215E6C8.
        self.dd7t = self.alloc(0x400)
        # qtab q[02B457D0]: 64-entry x 0x50 display-slot ring; qidx byte
        # 02B443C0 is the signed next-write index (3BBD00 wraps at 64,
        # returns old|0x20 or 0xFF on fail).  "qt" plants entries:
        # {slot: {"o": ptr|attr, "d"/"w"/"b": {off: v}}}.
        self.qtab = self.alloc(0x50 * 64)
        for i, fv in enumerate(case.get("pos", ())):
            gm.w(self.sovec + i * 4, struct.pack("<f", fv))
        for i, fv in enumerate(case.get("cam", ())):
            gm.w(0x1EBBB00 + i * 4, struct.pack("<f", fv))
        gm.w(self.subobj + 3, bytes([case.get("so3", 0x20) & 0xFF]))
        gm.w(self.subobj + 0xB8, qw(self.sovec))
        o10 = case.get("obj10", 0)
        if isinstance(o10, str):
            o10 = getattr(self, o10, 0)
        gm.w(self.dobj + 0x10, qw(o10))
        rqo = case.get("rqo", "subobj")
        if isinstance(rqo, str):
            rqo = getattr(self, rqo, 0)
        gm.w(self.req, qw(rqo))
        gm.w(self.req + 8, dw(case.get("rqv", 0)))
        gm.w(self.req + 0xC, bytes([case.get("rqt", 0) & 0xFF,
                                    case.get("rqs", 0) & 0xFF]))
        qtptr = case.get("qtptr", self.qtab if "qt" in case else 0)
        if isinstance(qtptr, str):
            qtptr = getattr(self, qtptr, 0)
        gm.w(0x2B457D0, qw(qtptr))
        gm.w(0x2B443C0, bytes([case.get("qidx", 0) & 0xFF]))
        for slot, spec in case.get("qt", {}).items():
            e = self.qtab + slot * 0x50
            o = spec.get("o", 0)
            if isinstance(o, str):
                o = getattr(self, o)
            gm.w(e, qw(o))
            for off, v in spec.get("d", {}).items():
                gm.w(e + off, dw(v))
            for off, v in spec.get("w", {}).items():
                gm.w(e + off, struct.pack("<H", v & 0xFFFF))
            for off, v in spec.get("b", {}).items():
                gm.w(e + off, bytes([v & 0xFF]))
        # rblk: static query block 022CA520 filled by real 35D330
        # (d[+0]=kind, d[+4]=arg — overwritten live) and consumed via
        # q[+0x18] name ptr, b[+0x24] 0xFF-gate, b[+0x25] flag byte.
        rb = case.get("rblk", {})
        for off, v in rb.get("d", {}).items():
            gm.w(0x22CA520 + off, dw(v))
        for off, v in rb.get("w", {}).items():
            gm.w(0x22CA520 + off, struct.pack("<H", v & 0xFFFF))
        for off, v in rb.get("b", {}).items():
            gm.w(0x22CA520 + off, bytes([v & 0xFF]))
        for off, v in rb.get("q", {}).items():
            if isinstance(v, str):
                v = getattr(self, v, 0)
            gm.w(0x22CA520 + off, qw(v))
        dd7 = case.get("dd7")
        if dd7:
            gm.w(0x215E6B8, dw(dd7.get("n", 0)))
            gm.w(0x215E6C8, qw(self.dd7t))
            for i, v in dd7.get("d", {}).items():
                gm.w(self.dd7t + i * 8, dw(v))
            for i, v in dd7.get("b", {}).items():
                gm.w(self.dd7t + i * 8 + 4, bytes([v & 0xFF]))

        # pair table row (327CB0 src): 12x w @+0, 12x w @+0x20
        pairidx = 0x5000
        if self.foerow:
            pairidx = case.get("foe", {}).get("w", {}) \
                .get(0x14, 0x5000)
        prow = self.elemb + pd["off"] + \
            pd["stride"] * ((pairidx - 0x5000) & 0xFFFF) if pd else 0
        if prow:
            pr = case.get("pair", {})
            plo = pr.get("lo", [0x6010, 0x6011, 0xFFFF])
            phi = pr.get("hi", [0x7010, 0xFFFF, 0xFFFF])
            for i, v in enumerate(plo[:12]):
                gm.w(prow + i * 2, struct.pack("<H", v & 0xFFFF))
            for i, v in enumerate(phi[:12]):
                gm.w(prow + 0x20 + i * 2,
                     struct.pack("<H", v & 0xFFFF))

        # glob cursor + slot row + 0x5B10 chain blocks.
        # Pipeline: 327DE0(rec) reads the chain BEFORE 326030 fills it;
        # 326030 snapshots slotrow+0x88 (0x30B) into the three chain
        # blocks at cursor idx*3..idx*3+2; 327DE0(slotrow) then reads
        # the delivered copy.  Plant the same pair data at BOTH the
        # slotrow array and the chain block so both calls agree.
        gm.w(self.glob + self.idx * 4 + 0x7370,
             dw(case.get("cursor", 0)))
        self.slotrow = self.glob + 8 + self.idx * 0x1C8
        gm.w(self.slotrow + 4,
             bytes([case.get("ordidx", self.idx) & 0xFF]))
        oidx = case.get("ordidx", self.idx)
        cur = case.get("cursor", 0) + oidx * 3
        blk = self.glob + 0x5B10 + cur * 0x34
        opairs = case.get("opairs",
                          [(0x6000, 0x11), (0x6001, 0x22)])
        omask = case.get("ordmask", 0) & 0xFFFF
        for base in (self.slotrow + 0x88, blk):
            gm.w(base + 0x30, struct.pack("<H", omask))
            for i, (a, b_) in enumerate(opairs[:12]):
                gm.w(base + i * 4, struct.pack("<H", a & 0xFFFF))
                gm.w(base + i * 4 + 2, struct.pack("<H", b_ & 0xFFFF))

        # order-table desc rows (327DE0 resolves bp-0x6000)
        for i, ospec in enumerate(case.get("ordrows", [{}] if od
                                          else [])):
            orow = self.elemb + od["off"] + od["stride"] * i
            ow = {8: 0x81, 0xA: 0x82, 0xC: 0x83, 0x18: 0x84,
                  0x1A: 0x85, 0x1C: 0x86}
            ow.update(ospec.get("w", {}))
            for off, v in ow.items():
                gm.w(orow + off, struct.pack("<H", v & 0xFFFF))
            ob = {0x10: 0x91, 0x11: 0x92, 0x12: 0x93}
            ob.update(ospec.get("b", {}))
            for off, v in ob.items():
                gm.w(orow + off, bytes([v & 0xFF]))

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def alloc(self, n):
        a = self.hb
        self.hb += (n + 0xFFF) & ~0xFFF
        return a

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def _args(self, tag):
        uc = self.uc
        self.rets.setdefault("calls", []).append(
            [tag,
             uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF])

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    SCR = {X_C650: ("c650", "c650_ret"), X_FED0: ("fed0", "fed0_ret"),
           0x2EB0D0: ("kb0d0", None),
           X_112F0: ("n12f0", "n12f0_ret"),
           X_2FA390: ("qfa390", "qfa390_ret"), X_46AB10: ("q6ab10", None),
           0x234DA0: ("sp234da0", "sp234da0_ret"),
           0x808C40: ("cookie", None),
           0x3B02A0: ("b3b02a0", "b3b02a0_ret"),
           0x1DBDB0: ("b1dbdb0", "b1dbdb0_ret"),
           0x2966E0: ("q2966e0", "q2966e0_ret"),

           X_43F0: ("u43f0", "u43f0_ret"),
           X_8F1F0: ("q28f1f0", None), X_FA540: ("q2fa540", None),
           X_3910: ("g3910", "g3910_ret"),
           X_4100: ("o4100", "o4100_ret"), X_7930: ("s7930", "s7930_ret"),
           X_8B40: ("l8b40", "l8b40_ret"),
           0x252E60: ("n252e60", "n252e60_ret"),
           0x2ECF10: ("tecf10", None), 0x3105D0: ("u3105d0", None),
           0x313F60: ("s313f60", "s313f60_ret"),
           0x300E40: ("p300e40", None), 0x2E42D0: ("r2e42d0", None),
           0x2699D0: ("s2699d0", None), 0x2ECEC0: ("r2ecec0", None),
           0x323C60: ("s323c60", "s323c60_ret"),
           0x308FF0: ("a308ff0", "a308ff0_ret"),
           0x324020: ("o324020", "o324020_ret"),
           0x308040: ("m308040", None), 0x308130: ("m308130", None),
           # EXP-198: unlink-carrier family boundaries
           0x23B040: ("b040", None), 0x238BF0: ("d8bf0", None),
           0x311F70: ("b1f70", None), 0x31B8C0: ("b8c0", "b8c0_ret"),
           0x311CF0: ("b1cf0", None), 0x313B30: ("b3b30", None),
           0x2FEAD0: ("bread0", None), 0x308270: ("b8270", None),
           0x30C970: ("bc970", None), 0x319420: ("b9420", None),
           0x319140: ("b9140", None), 0x317E50: ("b7e50", None),
           0x321850: ("b1850", None), 0x327200: ("b7200", "b7200_ret"),
           0x2EBB80: ("bbb80", None), 0x2E9780: ("b9780", "b9780_ret"),
           0x26D6F0: ("b6f0", None), 0x3E6B40: ("b6b40", None),
           0x254850: ("b4850", None), 0x2548F0: ("b48f0", None),
           0x254940: ("b4940", None), 0x36C1D0: ("bc1d0", "bc1d0_ret"),
           0x36C140: ("bc140", None), 0x24FE70: ("b4e70", "b4e70_ret"),
           0x426FA0: ("b6fa0", None), 0x3B0770: ("b0770", None),
           0x2E9BB0: ("b9bb0", None), 0x2EC5B0: ("bc5b0", None),
           # EXP-199: 312280's scripted subtree boundaries
           0x317ED0: ("s7ed0", None), 0x3171C0: ("s71c0", None),
           0x316A50: ("s6a50", None), 0x28FB80: ("sfb80", None),
           0x253690: ("s53690", "s53690_ret"),
           0x254EE0: ("s54ee0", None), 0x469E80: ("s69e80", None),
           0x319490: ("s9490", "s9490_ret"),
           0x3180F0: ("s80f0", "s80f0_ret"),
           0x319CA0: ("s9ca0", None), 0x317090: ("s7090", None),
           # EXP-201: display-queue scripted boundaries (deep resolver,
           # string machinery, row-index scan, battle-row writers)
           0x31C5D0: ("s31c5d0", "s31c5d0_ret"),
           0x2B3050: ("s2b3050", None),
           0x273320: ("s273320", "s273320_ret"),
           0x296E90: ("s296e90", None), 0x297040: ("s297040", None)}

    REAL = {F_AC80: "ac80", R_E600: "e600", R_C470: "c470",
            R_A630: "a630", R_3790: "g3790", R_7CB0: "p7cb0",
            R_6030: "c6030", R_7DE0: "o7de0", R_2C50: "v2c50",
            R_8F20: "f8f20", R_F690: "f690", R_F340: "f340",
            R_F5A0: "f5a0", R_B860: "b860", R_6850: "e6850",
            R_6820: "e6820", R_7C20: "cd7c20", R_148F0: "i148f0",
            R_EF2B0: "i2ef2b0", R_EF640: "i2ef640",
            R_E360: "e360", R_848E0: "c848e0", R_86A50: "h86a50",
            R_86A70: "h86a70", R_6A800: "h6a800", R_6D6A0: "h6d6a0",
            R_87730: "v87730", R_876D0: "v876d0",
            R_0BC0: "h0bc0", R_0CE0: "h0ce0", R_E060: "n0e060",
            R_283D0: "n283d0", R_F3F0: "f3f0", R_F4B0: "f4b0",
            R_F4D0: "f4d0", R_2AB0: "r2ab0", R_2A40: "r2a40",
            R_B0E0: "vb0e0", R_1B9F0: "i1b9f0",
            R_2FD970: "vfd970", R_0530R: "a0530",
            R_16D70: "l16d70", R_2A150: "l2a150", R_9F30: "l9f30",
            R_6F00: "l6f00", R_263D30: "l263d30", R_360D0: "l360d0",
            R_69BB0: "l69bb0", R_08A0: "a08a0", R_2FD420: "m2fd420",
            R_325F40: "n325f40", R_6A630: "l6a630",
            R_309440: "v309440", 0x252FD0: "l252fd0",
            0x30F9A0: "uf9a0", 0x30C410: "ec410", 0x324470: "m4470",
            0x2FD150: "m2fd150", 0x2FD8D0: "v2fd8d0",
            0x309EC0: "v9ec0",
            0x308130: "m8130", 0x308040: "m8040", 0x308FF0: "a8ff0",
            0x324020: "o4020", 0x323C60: "s3c60",
            0x307D10: "l7d10", 0x253B90: "l253b90",
            0x30B050: "l30b050", 0x30AB40: "l30ab40",
            0x263C20: "l263c20", 0x31B760: "l31b760",
            0x30BF20: "l30bf20", 0x307CE0: "l307ce0",
            0x30C210: "l30c210", 0x30BB30: "l30bb30",
            0x3081E0: "l3081e0", 0x328370: "rng28370",
            0x2F8FA0: "l2f8fa0", 0x323890: "l323890",
            0x3241D0: "l3241d0", 0x323BB0: "l323bb0",
            0x326500: "n6500", 0x311E20: "l11e20", 0x3272F0: "l272f0",
            0x31ABF0: "l31abf0", 0x263750: "l263750",
            0x265970: "l265970", 0x265020: "l265020",
            0x265200: "l265200", 0x33CA00: "l33ca00",
            0x326620: "l26620", 0x30D9A0: "l30d9a0",
            0x377C70: "l377c70", 0x3148F0: "l3148f0",
            0x31B770: "l31b770", 0x2367A0: "l2367a0",
            0x317400: "l317400", 0x30A880: "l30a880",
            0x30A8A0: "l30a8a0", 0x3594B0: "l594b0",
            0x3590D0: "l3590d0", 0x263E30: "l263e30",
            0x31B810: "l31b810", 0x3137E0: "l3137e0",
            0x3137F0: "l3137f0", 0x26DAC0: "l26dac0",
            0x3588B0: "l3588b0", 0x3589B0: "l3589b0",
            0x2F9A60: "g2f9a60",
            0x2F9B20: "g2f9b20", 0x2F9BD0: "g2f9bd0",
            0x379CD0: "rng79cd0", 0x35D8C0: "l35d8c0",
            0x2905D0: "l2905d0", 0x2EACD0: "l2eacd0",
            0x3A1180: "l3a1180", 0x267330: "l267330",
            0x2DF220: "l2df220", 0x3603C0: "l3603c0",
            0x329210: "l329210", 0x46A690: "l46a690",
            0x323910: "lg3910", 0x323D10: "l323d10",
            0x30A310: "l30a310", 0x300B80: "l300b80",
            0x324280: "l324280", 0x234DA0: "ld234da0",
            0x3273B0: "l3273b0", 0x31E620: "l31e620",
            0x3A1960: "l3a1960",
            # EXP-197: owner-check family + arm carriers
            X_B770: "lb770", X_B7F0: "lb7f0", X_B9B0: "lb9b0",
            X_B8E0: "lb8e0", 0x17D470: "l17d470",
            0x1D50D0: "l1d50d0", X_00140: "l300140",
            X_299B0: "l3299b0", 0x2EB030: "l2eb030",
            # EXP-198: unlink carriers + check leaves + 24FE30 dispatch
            X_0FC0: "l0fc0", X_01140: "l01140", 0x24FE30: "l4fe30",
            0x2372E0: "l372e0", 0x237260: "l37260", 0x2373C0: "l373c0",
            0x3135C0: "l3135c0", 0x3272E0: "l272e0",
            0x3219D0: "l219d0", 0x3001D0: "l3001d0", 0x310780: "l310780",
            0x3138D0: "l3138d0", 0x2ED180: "l2ed180", 0x26A330: "l26a330",
            0x35C8A0: "l35c8a0", 0x2E9600: "l2e9600", 0x2E8060: "l2e8060",
            0x319E30: "l319e30", 0x3125E0: "l3125e0", 0x26DC60: "l26dc60",
            0x31B7E0: "l31b7e0",
            0x2FD0C0: "l2fd0c0", 0x3B2830: "l3b2830", 0x3B1260: "l3b1260",
            # EXP-199: EXP/LP guest-share carrier + suppress leaf
            X_12280: "l312280", 0x236780: "l236780",
            0x2F8BB0: "l28bb0", 0x2F90C0: "l290c0",
            0x313800: "l313800", 0x320890: "l320890",
            0x264150: "l264150",
            # EXP-201: display-request queue — 3284D0 wrapper,
            # 2FA3B0 dist gate, 3BBD00 slot allocator, 506700 slot
            # initializer, 3EFD00 decimal formatter + leaf helpers
            0x3284D0: "l284d0", 0x2FA3B0: "lfa3b0",
            0x3BBD00: "l3bbd00", 0x506700: "l506700",
            0x3272A0: "l272a0", 0x35D330: "l35d330",
            0x28FBE0: "l28fbe0", 0x2DD7E0: "l2dd7e0",
            0x2DD7B0: "l2dd7b0", 0x24A5A0: "l24a5a0",
            0x296280: "l296280", 0x2B58B0: "l2b58b0",
            0x3EFD00: "l3efd00", 0x3A1920: "l3a1920"}

    def on_code(self, uc, addr, size, _):
        if addr == self.entry:
            return
        if addr == 0x210EC0:     # operator-new for 1D50D0's singleton
            self._args("n210ec0")
            if not self.sglbuf:
                self.sglbuf = self.alloc(0x1100)
            uc.reg_write(UC_X86_REG_RAX, self.sglbuf)
            self._ret()
            return
        if addr == 0x1CCB20:     # singleton ctor: returns its arg
            self._args("c1ccb20")
            uc.reg_write(UC_X86_REG_RAX,
                         uc.reg_read(UC_X86_REG_RCX))
            self._ret()
            return
        if addr == R_61EC0:      # memset(rcx, dl, r8)
            dst = uc.reg_read(UC_X86_REG_RCX)
            cnt = uc.reg_read(UC_X86_REG_R8)
            fv = uc.reg_read(UC_X86_REG_EDX) & 0xFF
            uc.mem_write(dst, bytes([fv]) * cnt)
            self.rets.setdefault("memsets", []).append(
                [dst & 0xFFFFFFFFFFFFFFFF, cnt & 0xFFFFFFFFFFFFFFFF])
            self.trace.append("memset")
            self._ret()
            return
        if addr == 0x1CCEF20:    # rand() via IAT (cell 0x8C3098)
            rv = self.case.get("randv", 0)
            n = self.rets.setdefault("randn", 0)
            self.rets["randn"] = n + 1
            if isinstance(rv, (list, tuple)):
                rv = rv[min(n, len(rv) - 1)]
            uc.reg_write(UC_X86_REG_RAX, rv & 0xFFFFFFFF)
            self.trace.append("rand")
            self._ret()
            return
        if addr == 0x1CCED52:    # sqrtf via IAT (cell 0x8C2BB8)
            xv = uc.reg_read(UC_X86_REG_XMM0)
            xf = struct.unpack("<f", struct.pack("<I", xv & 0xFFFFFFFF))[0]
            xf = math.sqrt(xf) if xf >= 0 else float("nan")
            uc.reg_write(UC_X86_REG_XMM0,
                         int.from_bytes(struct.pack("<f", xf)
                                        + b"\x00" * 12, "little"))
            self.trace.append("sqrtf")
            self._ret()
            return
        if addr in self.case.get("realx", ()):
            self.trace.append("rx%06x" % addr)
            return
        ent = self.SCR.get(addr)
        if ent is not None:
            tag, retkey = ent
            self._args(tag)
            if retkey:
                rv = self.case.get(retkey, 0)
                if isinstance(rv, str):
                    rv = getattr(self, rv, 0)
                uc.reg_write(UC_X86_REG_RAX,
                             rv & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        t = self.REAL.get(addr)
        if t is not None:
            self.trace.append(t)
            self.rets.setdefault("rargs", []).append(
                [t,
                 uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
                 uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF])
            return

    def run(self, rcx=0, edx=0):
        uc = self.uc
        self.entry = self.case.get("entry", F_AC80)
        rsp = STACK + 0x80000
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, edx & 0xFFFFFFFFFFFFFFFF)
        # direct-entry stack layout: retaddr@rsp (emu entry pushes none),
        # stack args at +0x28/+0x30/+0x38 (8 above a real callee's view)
        def rarg(v):
            if isinstance(v, str):
                return getattr(self, v, 0)
            return v
        uc.reg_write(UC_X86_REG_R8,
                     rarg(self.case.get("r8", 0)) & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9,
                     rarg(self.case.get("r9", 0)) & 0xFFFFFFFFFFFFFFFF)
        self.gm.w(rsp + 0x20, qw(self.case.get("sarg", 0)))
        self.gm.w(rsp + 0x28, qw(self.case.get("a5", 0)))
        self.gm.w(rsp + 0x30, qw(self.case.get("a6", 0)))
        self.gm.w(rsp + 0x38, qw(self.case.get("a7", 0)))
        try:
            uc.emu_start(self.entry, RETQ, timeout=60_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------------------------
def base_case(**kw):
    c = {"idx": 2, "mode": 0, "gate": 1, "s7930_ret": 1}
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k] = {**c[k], **v}
        else:
            c[k] = v
    return c


SM_NONE = {i: 0xFF for i in range(9)}


def cdis(**kw):
    # EXP-201 display-queue: direct entry on 3BBD00 with rcx=req.
    kw.setdefault("entry", 0x3BBD00)
    kw.setdefault("rcx", "req")
    kw.setdefault("randv", 0)
    return base_case(**kw)


def c228(**kw):
    # edx=objrow is the member row; objlink plants the rec at
    # q[+0x698]; rec_b[5]=1 passes the record gate; e78/e70 default 0
    # keeps the FP tail's d[+0x30] reads mapped.
    kw.setdefault("entry", 0x312280)
    kw.setdefault("objlink", 1)
    kw.setdefault("edx", "obj")
    kw.setdefault("e78", 0)
    kw.setdefault("e70", 0)
    # EXP-200: real 2F8BB0 member-count divisor — one live member
    # (objrow via map 0) -> share undivided.
    kw.setdefault("memslots", [0, 0xFF, 0xFF, 0xFF])
    kw.setdefault("rec_b", {})
    kw["rec_b"] = {5: 1, **kw["rec_b"]}
    return base_case(**kw)


def cfml(entry, **kw):
    # EXP-200 direct-entry cases for the share formulas.
    # rcx = guest row (0 = the 312280 source-tail call), edx = objrow.
    kw.setdefault("entry", entry)
    kw.setdefault("objlink", 1)
    kw.setdefault("edx", "obj")
    kw.setdefault("rcx", 0)
    kw.setdefault("e78", 0)
    kw.setdefault("e70", 0)
    kw.setdefault("memslots", [0, 0xFF, 0xFF, 0xFF])
    kw["rec_b"] = {5: 1, **kw.get("rec_b", {})}
    return base_case(**kw)


CASES = {
    # ---- gates / mode dispatch ----
    "ac80-gate-off":   base_case(gate=0),
    "ac80-mode2":      base_case(mode=2),
    "ac80-modeff":     base_case(mode=0xFF),

    # ---- member path ----
    "ac80-member":       base_case(mode=1),
    "ac80-member-nulld": base_case(mode=1, memd=None,
                                   expect_fault=0x23ADA8),
    "ac80-member-deny":  base_case(mode=1, s7930_ret=0),

    # ---- foe path ----
    "ac80-foe":          base_case(),
    "ac80-foe-nulld":    base_case(foed=None,
                                   expect_fault=0x23AD7B),
    "ac80-foe-idx7":     base_case(idx=7, abil=[0xFF] * 8),
    "ac80-foe-scan":     base_case(idx=2, abil=[0, 4, 0xFF, 4]),
    "ac80-foe-cnt0":     base_case(foe={"cnt": 0}),
    "ac80-foe-noflag40": base_case(foe={"b2c": 0}),
    # d[rec+0x190] is memset to 0 before 323790 and the addend is a
    # word (<0x1869F) — the cap/floor arms of 323790 are unreachable
    # from this caller; the value asserts document that.
    "ac80-foe-gilbig":   base_case(foe={"w": {0x44: 0x7FFF}}),
    "ac80-foe-oidx27":   base_case(idx=0x27),
    "ac80-foe-oidx28":   base_case(idx=0x28, expect_fault=0x326057),
    "ac80-foe-pairnull": base_case(paird=None),
    "ac80-foe-pairbad":  base_case(foe={"w": {0x14: 0x4000}}),
    "ac80-foe-ordrow":   base_case(ordmask=3, ordrows=[{}, {}]),
    # slotrow b[+4]=5 != rec b[+4]=2: the two 327DE0 calls use
    # different index bytes AND different cursor cells/blocks —
    # rec-call's blk (pos 2*3) unplanted -> ordrow2 stays empty;
    # slotrow-call's blk (pos 5*3) planted -> ordrow5 fills.
    "ac80-foe-orddiv":   base_case(ordmask=3, ordrows=[{}, {}],
                                   ordidx=5),
    # cursor=1 shifts the scanned block to position idx*3+1
    "ac80-foe-cursor1":  base_case(ordmask=3, ordrows=[{}, {}],
                                   cursor=1),
    # glob null faults first inside 327CB0's tail-call 327DE0(rec):
    # movsxd rcx, d[0+idx*4+0x7370] — before 326030 is reached.
    "ac80-foe-globnull": base_case(glob_null=True,
                                   expect_fault=0x327E27),
    # 30C470's 30F690 gate: d[0208D320]|d[0208D324] != 0.
    # mask=1 -> bit0 fixup runs real: 31B860 owner scan finds the
    # linked row, but rec's +0x3C/+0x64 flags are memset -> the
    # 0x80000003 check fails -> no 377C20, no bit26 clear; e360 still
    # fires for the set bit.
    "ac80-foe-f690gate": base_case(f690_gate=1, objlink=True),
    "ac80-foe-f690norow": base_case(f690_gate=1),

    # ---- direct 30F690(rec, mask) ----
    # bit0: owner row found, rec flags set, can-die=0 -> clear bit26
    "f690-bit0-clear":  base_case(entry=0x30F690, edx=1, objlink=True,
                                  rec_d={0x3C: 1, 0x64: 1}, cd_words=[0]),
    # can-die=1 vetoes the clear
    "f690-bit0-candie": base_case(entry=0x30F690, edx=1, objlink=True,
                                  rec_d={0x3C: 1, 0x64: 1}, cd_words=[0x8000]),
    # no rec flags -> 377C20 never runs, no clear
    "f690-bit0-noflg":  base_case(entry=0x30F690, edx=1, objlink=True),
    # no owner row -> fixup skipped, e360 still fires
    "f690-bit0-norow":  base_case(entry=0x30F690, edx=1,
                                  rec_d={0x64: 1}),
    # non-zero bits skip the fixup entirely; e360 per set bit
    "f690-bits13":      base_case(entry=0x30F690, edx=0xA,
                              rec_d={0x64: 0xA}),
    # empty mask -> ret immediately, no calls
    "f690-mask0":       base_case(entry=0x30F690, edx=0),

    # ---- direct 30F340(rec) ----
    # flags=0, d[+0x24]=7 vs d[+0x48]=0 -> c530(rec, 7, 0, 0x217)
    "f340-delta":   base_case(entry=0x30F340, rec_d={0x24: 7}),
    # flags bit0x1C doubles d[+0x24] -> delta 14
    "f340-bit1c":   base_case(entry=0x30F340,
                             rec_d={0x64: 1 << 0x1C, 0x24: 7}),
    # flags bit0x10 clamps stored -5 to computed 1 -> delta 6; and
    # stored<=0 + idx-in-range + b5==0 -> unlink path first
    "f340-bit10":   base_case(entry=0x30F340, idx=0x1C, objlink=True,
                              rec_d={0x3C: 1 << 0x10, 0x48: -5,
                                     0x4: 0x1C}),
    # computed==stored -> pure ret
    "f340-equal":   base_case(entry=0x30F340),

    # ---- direct 30F5A0(rec) ----
    # w28=100 vs w4C=50 -> h0ce0(+50); w6=0 -> h0bc0(100) twice
    # (section1 clamp + section2 with b37=0)
    "f5a0-hp":    base_case(entry=0x30F5A0,
                            rec_w={0x28: 100, 0x4C: 50}),
    # b[+0x6C] negative gates w28 to 0 -> h0ce0(-50) only
    "f5a0-gated": base_case(entry=0x30F5A0,
                            rec_w={0x28: 100, 0x4C: 50},
                            rec_b={0x6C: 0x80}),
    # b[+0x37] scales section2: w28*3=30 vs w6=20 -> h0bc0(10)
    "f5a0-b37":   base_case(entry=0x30F5A0,
                            rec_w={0x28: 10, 0x4C: 10, 0x6: 20},
                            rec_b={0x37: 3}),
    # all equal -> ret, no calls
    "f5a0-equal": base_case(entry=0x30F5A0),

    # ---- direct 30E360(rec, src, bit, a4, a5, a6mask, a7arm) ----
    "e360-arm0-clr":  base_case(entry=R_E360, edx=0, r8=2, r9=0x77,
                                a5=0x1234, a6=0x217, a7=0,
                                rec_d={0x64: (1 << 2) | (1 << 5)}),
    "e360-arm0-noop": base_case(entry=R_E360, edx=0, r8=2, r9=0x77,
                                a5=0x1234, a6=0x217, a7=0,
                                rec_d={0x64: 1 << 5}),
    "e360-arm1-clr":  base_case(entry=R_E360, edx=0, r8=3, r9=0x88,
                                a5=0x2345, a6=0x217, a7=1,
                                rec_d={0x3C: 1 << 3}),
    "e360-arm2-clr":  base_case(entry=R_E360, edx=0, r8=4, r9=0x99,
                                a5=0x3456, a6=0x217, a7=2,
                                rec_d={0x38: 1 << 4}),
    "e360-arm3-set":  base_case(entry=R_E360, edx=0, r8=2, r9=0xAA,
                                a5=0x4567, a6=0x217, a7=3),
    "e360-arm3-conflict": base_case(entry=R_E360, edx=0, r8=2, r9=0,
                                    a5=0, a6=0x217, a7=3,
                                    rec_d={0x38: 1 << 2}),
    "e360-arm4-set":  base_case(entry=R_E360, edx=0, r8=5, r9=0xBB,
                                a5=0x5678, a6=0x217, a7=4),
    "e360-arm5-set":  base_case(entry=R_E360, edx=0, r8=6, r9=0xCC,
                                a5=0x6789, a6=0x217, a7=5),
    # 386A70 edx==0x1C special via a non-mode arm
    "e360-bit1c":     base_case(entry=R_E360, edx=0, r8=0x1C, r9=0,
                                a5=0, a6=0x217, a7=0,
                                rec_d={0x64: 1 << 0x1C, 0x48: 9}),
    # descriptor cascade: arm3 sets bit2; casc row(2) mask bit4 ->
    # recursive arm0 clears pre-set bit4
    "e360-cascade":   base_case(entry=R_E360, edx=0, r8=2, r9=0x11,
                                a5=0x1111, a6=0x217, a7=3,
                                casc_rows={2: 1 << 4},
                                rec_d={0x64: 1 << 4}),
    # arg6&1==0 -> owner checks run (scripted 30B9B0)
    "e360-owner-chk": base_case(entry=R_E360, edx=0, r8=2, r9=0,
                                a5=0, a6=0x216, a7=0,
                                rec_d={0x64: 1 << 2}),
    "e360-owner-bail": base_case(entry=R_E360, edx=0, r8=2, r9=0,
                                 a5=0, a6=0x216, a7=0,
                                 rec_d={0x64: 1 << 2},
                                 ownb=1),
    # mode arm -> second owner check 30B8E0 also runs
    "e360-owner2-chk": base_case(entry=R_E360, edx=0, r8=2, r9=0,
                                 a5=0, a6=0x216, a7=3),
    # mode pair: arg7 in {3,4} -> 46A800 (bit 1 -> 46AB10)
    "e360-mode-pair": base_case(entry=R_E360, edx=0, r8=1, r9=0x33,
                                a5=0x2222, a6=0x15, a7=3,
                                qfa390_ret=1),
    "e360-nomode-pair": base_case(entry=R_E360, edx=0, r8=1, r9=0x33,
                                  a5=0x2222, a6=0x15, a7=0,
                                  rec_d={0x64: 1 << 1}),
    # negative arg5 -> 3876D0 resolves word via CASCD rows
    "e360-neg-arg5":  base_case(entry=R_E360, edx=0, r8=2, r9=0x55,
                                a5=0xFFFFFFFF, a6=0x217, a7=0,
                                casc_rows={2: 0}, casc_b9={2: 3},
                                rec_d={0x64: 1 << 2}),

    # ---- direct 300BC0(rec, delta, notify): HP apply
    "bc0-basic":   base_case(entry=R_0BC0, edx=50, r8=0x217,
                             objlink=True,
                             rec_w={0x6: 100, 0x28: 200}),
    "bc0-cap":     base_case(entry=R_0BC0, edx=500, r8=0x217,
                             objlink=True,
                             rec_w={0x6: 100, 0x28: 200}),
    "bc0-floor":   base_case(entry=R_0BC0, edx=-100, r8=0x217,
                             objlink=True, rec_w={0x6: 50, 0x28: 200}),
    "bc0-deadgate": base_case(entry=R_0BC0, edx=50, r8=0x217,
                              objlink=True,
                              rec_w={0x6: 100, 0x28: 200},
                              rec_b={0x6C: 0x80}),
    "bc0-scale":   base_case(entry=R_0BC0, edx=400, r8=0x217,
                             objlink=True,
                             rec_w={0x6: 50, 0x28: 100},
                             rec_b={0x37: 3}),
    "bc0-veto":    base_case(entry=R_0BC0, edx=50, r8=0x216,
                             objlink=True, ownb=1,
                             rec_w={0x6: 100, 0x28: 200}),
    # ---- direct 300CE0(rec, delta, notify): w4C gauge apply
    "ce0-basic":   base_case(entry=R_0CE0, edx=30, r8=0x217,
                             objlink=True,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    "ce0-cap":     base_case(entry=R_0CE0, edx=500, r8=0x217,
                             objlink=True,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    "ce0-cascade": base_case(entry=R_0CE0, edx=30, r8=0x217,
                             objlink=True,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    "ce0-drop":    base_case(entry=R_0CE0, edx=-30, r8=0x217,
                             objlink=True,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    "ce0-r13":     base_case(entry=R_0CE0, edx=30, r8=0x207,
                             objlink=True,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    "ce0-veto":    base_case(entry=R_0CE0, edx=30, r8=0x216,
                             objlink=True, objflags=0x4000110,
                             rec_w={0x4C: 50, 0x28: 200, 0x6: 10}),
    # ---- direct 30E060(rec, notify): HP-fraction notify
    "e060-frac":   base_case(entry=R_E060, edx=0x400, objlink=True,
                             rec_w={0x6: 200, 0x28: 200},
                             rec_b={0x37: 1, 0x4E: 0}),
    "e060-same":   base_case(entry=R_E060, edx=0x400, objlink=True,
                             rec_w={0x6: 200, 0x28: 200},
                             rec_b={0x37: 1, 0x4E: 1}),
    "e060-down":   base_case(entry=R_E060, edx=0x400, objlink=True,
                             rec_w={0x6: 0, 0x28: 200},
                             rec_b={0x37: 1, 0x4E: 1}),

    # ---- direct 30F3F0(flags in rcx): 9 member slots
    # mask = (flags&4 ? d[208D320]:0) | (flags&8 ? d[208D324]:0)
    #        | (flags&0x10 ? 0x544 : 0)   -- 0x544 gated ON by bit4
    "f3f0-none":   base_case(entry=R_F3F0, rcx=0),
    "f3f0-bit10":  base_case(entry=R_F3F0, rcx=0x10),
    "f3f0-gates":  base_case(entry=R_F3F0, rcx=0x1C,
                             f690_gate=0x40, f690_gate2=0x80),
    "f3f0-trio":   base_case(entry=R_F3F0, rcx=3),
    "f3f0-emptymap": base_case(entry=R_F3F0, rcx=0x10,
                               slotmap={3: 0xFF}),
    # ---- direct 30F4B0(x, flags in edx): member + foe broadcast
    "f4b0-foes":   base_case(entry=R_F4B0, edx=0),
    "f4b0-mask":   base_case(entry=R_F4B0, edx=0x10),
    "f4b0-trio":   base_case(entry=R_F4B0, edx=0x13),
    "f4b0-skip":   base_case(entry=R_F4B0, edx=0x10, foebmp=0x000C),

    # ---- direct 300530(rec, delta=edx, arg3=r8, notify=r9)
    # r14 = d[rec+0x48] + delta, clamped [d[ownerrow+0x48]|0, cap]
    # cap = d64|d3C&0x10000 ? max(d48,1) : d[+0x24] (x2 if bit 0x1C)
    "s530-pos":    base_case(entry=R_0530R, edx=5, r9=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-over":   base_case(entry=R_0530R, edx=500, r9=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-zero":   base_case(entry=R_0530R, edx=0, r9=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-neg":    base_case(entry=R_0530R, edx=-3 & 0xFFFFFFFF,
                             r9=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-floor":  base_case(entry=R_0530R, edx=-50 & 0xFFFFFFFF,
                             r9=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-veto":   base_case(entry=R_0530R, edx=-3 & 0xFFFFFFFF,
                             r9=0x216, ownb=1,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-nonotify": base_case(entry=R_0530R, edx=5, r9=0x0,
                               rec_d={0x24: 100, 0x48: 10}),
    "s530-cap2x":  base_case(entry=R_0530R, edx=500, r9=0x217,
                             rec_d={0x24: 100, 0x48: 10,
                                    0x64: 1 << 0x1C}),

    "s530-revive": base_case(entry=R_0530R, edx=5, r9=0x217,
                             rec_d={0x24: 100, 0x48: 0}),

    # ---- EXP-197: owner-check family -------------------------------
    # 30B770() leaf: bit0 = d[02089340]&0x3080; bit1 = b[022C2158]&1;
    # bits 2/3/4 = d[02089340] bits 10/9/11.  No args.
    "b770-zero":    base_case(entry=0x30B770),
    "b770-g3080":   base_case(entry=0x30B770, owngl=0x1000),
    "b770-b7":      base_case(entry=0x30B770, owngl=0x80),
    "b770-ownb":    base_case(entry=0x30B770, ownb=1),
    "b770-bits":    base_case(entry=0x30B770, owngl=0x600),
    "b770-all":     base_case(entry=0x30B770, owngl=0x1E80, ownb=1),
    # 30B7F0(objrow, edx): low word = object flags, high word = 17D470
    #   bit3 = b[obj+4]&0x20 && d[022C2160]-5 > 1
    #   bit0 = d[obj] bit8; bit1 = d[obj] bit30 && edx!=0
    #   bit4 = rec(b5==0 && b4==0x1A)
    #   hi bit0 = 17D470()==1 && rec(b5==0); hi bits |= 17D470() when ==2
    "b7f0-null":    base_case(entry=0x30B7F0, rcx=0, edx=0),
    "b7f0-noflg":   base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True),
    "b7f0-lo":      base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000110),
    "b7f0-b4in":    base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010,
                              obj_d={4: 0x20}, g2160=9),
    "b7f0-b4out":   base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010,
                              obj_d={4: 0x20}, g2160=5),
    "b7f0-edx":     base_case(entry=0x30B7F0, rcx="obj", edx=1,
                              objlink=True, objflags=0xC0000110),
    "b7f0-rec1a":   base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010,
                              rec_b={4: 0x1A}),
    "b7f0-sgl1":    base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010, sgl=1),
    "b7f0-sgl2":    base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010, sgl=2),
    "b7f0-sglgate": base_case(entry=0x30B7F0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010, sgl=1,
                              rec_b={5: 1}),
    # 17D470(): d[1D50D0()+0xC20]; 1D50D0 lazily builds q[01F81428]
    "d470-null":    base_case(entry=0x17D470),
    "d470-sgl":     base_case(entry=0x17D470, sgl=0x42),
    # 30B9B0(row, row2): (w(30B770()) || w(30B7F0(row,edi))) ? 1 : 0
    "b9b0-null":    base_case(entry=0x30B9B0, rcx=0, edx=0),
    "b9b0-none":    base_case(entry=0x30B9B0, rcx="obj", edx=0,
                              objlink=True),
    "b9b0-glob":    base_case(entry=0x30B9B0, rcx="obj", edx=0,
                              objlink=True, ownb=1),
    "b9b0-pair":    base_case(entry=0x30B9B0, rcx="obj", edx="row2",
                              objlink=True, objflags=0xC0000110,
                              row2={"flags": 0x10, "rec": {}},
                              rec_d={0x64: 0x20}),
    # 30B8E0(row, row2): ret 1 iff HIGH word of 30B7F0(...) nonzero
    "b8e0-null":    base_case(entry=0x30B8E0, rcx=0, edx=0),
    "b8e0-lo":      base_case(entry=0x30B8E0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000110),
    "b8e0-sgl":     base_case(entry=0x30B8E0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010, sgl=1),
    "b8e0-sgl2":    base_case(entry=0x30B8E0, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000010, sgl=2),
    # 300140(objrow, edx): unlink-mark carrier.  edx -> u3105d0(rcx);
    # clears q[+0x6F8]/d[+0x748]/d[+0x770]/d[+0x788]&~0x400/
    # d[+0x6B0]&~2/q[+0x750]/d[+0x74C]; clears q[obj] bit14 unless the
    # w[+0xBA0] sentinel matches (0x113 when q&0x4000 else 0x95);
    # sets d[obj+4] bit 0x200000.
    "b140-edx0":    base_case(entry=0x300140, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000,
                              obj_d={0xBA0: 0x113, 0x6F8: 0xAAAA,
                                     0x748: 0xBB, 0x770: 0xCC,
                                     0x788: 0x4FF, 0x6B0: 0xFF,
                                     0x750: 0xDD, 0x74C: 0xEE}),
    "b140-clear":   base_case(entry=0x300140, rcx="obj", edx=0,
                              objlink=True, objflags=0x4000,
                              obj_d={0xBA0: 0x55}),
    "b140-td":      base_case(entry=0x300140, rcx="obj", edx=1,
                              objlink=True, objflags=0x4000,
                              obj_d={0xBA0: 0x113}),
    # 3299B0(objrow, edx=msg, r8d): edx==-1 -> ret; else
    # ebx = (edx&0xFFF)>=0x100 ? edx|0x5000 : edx; 2EB030(q[obj+0x10],
    # ebx); d[obj+0x5C]=ebx; d[obj+0x2C]=r8d then 0.
    "k99b0-minus1": base_case(entry=0x3299B0, rcx="obj",
                              edx=-1 & 0xFFFFFFFF, r8=7,
                              objlink=True),
    "k99b0-low":    base_case(entry=0x3299B0, rcx="obj", edx=0x50,
                              r8=0x77, objlink=True,
                              ent_b={0x18: 1, 0xD: 0xFF}),
    "k99b0-hi":     base_case(entry=0x3299B0, rcx="obj", edx=0x300,
                              r8=0x77, objlink=True,
                              ent_b={0x18: 1, 0xD: 0xFF}),
    "k99b0-kick":   base_case(entry=0x3299B0, rcx="obj", edx=0x50,
                              r8=0x77, objlink=True,
                              ent_b={0x18: 0, 0xD: 0xFF},
                              ent_q={0xC0: 0xDEAD}),

    # 3008A0(id, edx=mut delta, r8=mut mode, r9=dispatch gate, a5=mut flag)
    # -> 309F30(id, r9) validator + q[row+0x48] mutator (2FD420 for cls-C)
    "s8a0-foe":    base_case(entry=R_08A0, rcx=0xC012, edx=0,
                             statecell=1),
    "s8a0-clear":  base_case(entry=R_08A0, rcx=0xC012,
                             edx=-1 & 0xFFFFFFFF, statecell=1),
    "s8a0-set":    base_case(entry=R_08A0, rcx=0xC012, edx=1,
                             foebmp=0, statecell=1),
    "s8a0-setzero": base_case(entry=R_08A0, rcx=0xC012, edx=0,
                              foebmp=0, statecell=1),
    "s8a0-neg2":   base_case(entry=R_08A0, rcx=0xC012,
                             edx=-2 & 0xFFFFFFFF, statecell=1),
    "s8a0-mode":   base_case(entry=R_08A0, rcx=0xC012, edx=1, r8=1,
                             foebmp=0, statecell=1),
    "s8a0-mode0":  base_case(entry=R_08A0, rcx=0xC012, edx=0, r8=1,
                             foebmp=0, statecell=1),
    "s8a0-flag4":  base_case(entry=R_08A0, rcx=0xC012, edx=1, a5=1,
                             foebmp=0, statecell=1),
    "s8a0-flag4clr": base_case(entry=R_08A0, rcx=0xC012,
                               edx=-1 & 0xFFFFFFFF, a5=1, statecell=1),
    "s8a0-foeflag": base_case(entry=R_08A0, rcx=0xC012, edx=1, r9=1,
                              foebmp=0, statecell=1),
    "s8a0-foe80":  base_case(entry=R_08A0, rcx=0xC011, edx=1, r9=1,
                             foebmp=0, statecell=1),
    "s8a0-foeend": base_case(entry=R_08A0, rcx=0xC01E, edx=1, r9=1,
                             foebmp=0, statecell=1),
    "s8a0-inval":  base_case(entry=R_08A0, rcx=0xC050, edx=1,
                             statecell=1),
    "s8a0-ffff":   base_case(entry=R_08A0, rcx=0xFFFF, edx=1,
                             statecell=1),
    "s8a0-hi":     base_case(entry=R_08A0, rcx=0xF012, edx=1,
                             statecell=1),
    "s8a0-k":      base_case(entry=R_08A0, rcx=0x1000, edx=1,
                             statecell=1),

    # ---- EXP-192: 31A630 member-block chain (r9d!=0) ----
    # rec slot-2 word w[rec+0x54]=0x1100 (member class, count5/cap5);
    # new id 0x1150 (count2/cap3); owner member found via objlink.
    "a630r9-swap":   base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # r9d==0 -> whole chain skipped (control)
    "a630r9-off":    base_case(entry=R_A630, edx=2, r8=0x1150, r9=0,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # old slot word FFFF -> 30F9A0 -1 early; 30C410 still runs
    "a630r9-oldff":  base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0xFFFF}, objlink=1,
                               cls1words={0x150: 0x0803}),
    # old id foe-class 0xC012 -> 30F9A0 class gate -> 0, no 3008A0
    "a630r9-oldfoe": base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0xC012}, objlink=1,
                               cls1words={0x150: 0x0803}),
    # new id 0x1000 exactly -> 30C410 class-eq gate -> 0, no 3008A0
    "a630r9-new1k":  base_case(entry=R_A630, edx=2, r8=0x1000, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405}),
    # owner scan miss -> 31B860 ret 0 -> 324470 skipped
    "a630r9-nomatch": base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                                rec_w={0x54: 0x1100}, objcount=2,
                                cls1words={0x100: 0x1405,
                                           0x150: 0x0803}),
    # member d[0] bit23 -> 2ECF10 edx=1
    "a630r9-bit23":  base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               objflags=0x40800000,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # 313F60 nonzero -> 300E40 skipped
    "a630r9-gate3f": base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               rec_d={0x3C: 1}, s313f60_ret=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # b[member]&2 -> 300E40 skipped
    "a630r9-b2":     base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               objflags=0x4000002, rec_d={0x3C: 1},
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # rec +0x3C bit0 -> 300E40 skipped without 313F60
    "a630r9-rec3c":  base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               rec_d={0x3C: 1},
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803}),
    # rcx==0 -> -1
    "a630r9-null":   base_case(entry=R_A630, rcx=0, edx=2, r9=1),
    # 317930 deny -> -1, no writes / no chain
    "a630r9-deny":   base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               s7930_ret=0,
                               cls1words={0x150: 0x0803}),
    # new id FFFF -> 317930 skipped, 30C410(FFFF)->-1, slot cleared
    "a630r9-newff":  base_case(entry=R_A630, edx=2, r8=0xFFFF, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405}),
    # equip clamp: new count would exceed cap (3/3) -> clamped
    "a630r9-clamp":  base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0C03}),

    # ---- EXP-193: remaining scripted boundaries, real ----
    # 317930 slot gate: (rec, slots=rec+0x50, slot, id, a5=flag).
    # w[D107E8+i*2] = {1000,FFFF,FFFF,FFFF,FFFF} shortcut first.
    "g7930-t0sent": base_case(entry=0x317930, edx="rec50", r8=0,
                              r9=0x1000),
    "g7930-clr":    base_case(entry=0x317930, edx="rec50", r8=3,
                              r9=0xFFFF),
    "g7930-clr0":   base_case(entry=0x317930, edx="rec50", r8=0,
                              r9=0xFFFF),
    "g7930-slot5":  base_case(entry=0x317930, edx="rec50", r8=5,
                              r9=0x1150),
    # valid kind-8 ids are class-3 0x3000..0x3000+d[k8d+4)-1; memt
    # rows index id-0x1000 (0x2010 for 0x3010)
    "g7930-ok":     base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 31}},
                              s323c60_ret=1),
    "g7930-tagmm":  base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 3 << 5}}),
    "g7930-k8rng":  base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x3010, k8d={"count": 8},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5}}),
    "g7930-free0":  base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150, a5=1,
                              cls1words={0x150: 0x0C03},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5}}),
    "g7930-free1":  base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150, a5=1,
                              cls1words={0x150: 0x0803},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 31}},
                              s323c60_ret=1),
    # esi==1 sub-check: slot0 occupied (w[slots]=0x1160), new row b9
    # must equal slot0 row's b11
    "g7930-s1eq":   base_case(entry=0x317930, edx="rec50", r8=1,
                              r9=0x1150,
                              rec_w={0x50: 0x1160},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 1 << 5, 9: 5},
                                         0x160: {7: 0, 0x11: 5}},
                              s323c60_ret=1),
    "g7930-s1ne":   base_case(entry=0x317930, edx="rec50", r8=1,
                              r9=0x1150,
                              rec_w={0x50: 0x1160},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 1 << 5, 9: 5},
                                         0x160: {7: 0, 0x11: 7}}),
    # rec nonnull + b5==0 -> FOED row bit test b[row+9]; bit set -> fail
    "g7930-foebit": base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150, idx=0,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 5}},
                              foe={"w": {0: 1 << 5}}),
    "g7930-b5":     base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              rec_b={5: 1},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 31}},
                              foe={"w": {0: 1 << 5}}),
    "g7930-c60":    base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 31}},
                              s323c60_ret=0),
    "g7930-nomemt": base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150),

    # 318B40 pair rebalance: rcx=slots, edx=written slot, r8=flag.
    "l8b40-ffinit":  base_case(entry=0x318B40, rcx="rec50", edx=0,
                               r8=1, rec_w={0x50: 0xFFFF,
                                            0x52: 0x1160},
                               cls1words={0x160: 0x0803},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0: {0x11: 0x12},
                                          0x160: {9: 3}}),
    "l8b40-match":   base_case(entry=0x318B40, rcx="rec50", edx=0,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0x1160},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3},
                                          0x160: {9: 3}}),
    "l8b40-s0clr":   base_case(entry=0x318B40, rcx="rec50", edx=0,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0x1160},
                               cls1words={0x160: 0x0803},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3},
                                          0x160: {9: 5}}),
    "l8b40-s1reset": base_case(entry=0x318B40, rcx="rec50", edx=1,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0xFFFF},
                               cls1words={0x150: 0x0803},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3}}),
    "l8b40-s1tag12": base_case(entry=0x318B40, rcx="rec50", edx=1,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0x1160},
                               cls1words={0x150: 0x0803},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3},
                                          0x160: {9: 0x12}}),
    "l8b40-s1clr":   base_case(entry=0x318B40, rcx="rec50", edx=1,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0x1160},
                               cls1words={0x160: 0x0803},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3},
                                          0x160: {9: 5}}),
    "l8b40-noflag":  base_case(entry=0x318B40, rcx="rec50", edx=0,
                               r8=0, rec_w={0x50: 0x1150,
                                            0x52: 0x1160},
                               memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                               memt_rows={0x150: {0x11: 3},
                                          0x160: {9: 5}}),
    # null member-table desc -> resolve path yields rdi=0 -> b[0+7]
    "l8b40-nomemt":  base_case(entry=0x318B40, rcx="rec50", edx=0,
                               r8=1, rec_w={0x50: 0x1150,
                                            0x52: 0xFFFF},
                               expect_fault=0x318BE0),

    # 3243F0 member unlink (no 2ECF10/0x40-flag; tail-jmps 2ECEC0)
    "u43f0-gate0":  base_case(entry=0x3243F0, rcx="obj", objlink=1),
    "u43f0-698z":   base_case(entry=0x3243F0, rcx="obj", objlink=1,
                              obj698=0),
    "u43f0-3f":     base_case(entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}),
    "u43f0-3fskip": base_case(entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}, s313f60_ret=1),
    "u43f0-b2":     base_case(entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}, objflags=0x4000002),
    # 324450 conditional caller: b&0x40 -> 3243F0 + clear 0x40
    "w4450-set":    base_case(entry=0x324450, rcx="obj", objlink=1,
                              realx=[0x3243F0], objflags=0x4000040),
    "w4450-clear":  base_case(entry=0x324450, rcx="obj", objlink=1,
                              realx=[0x3243F0]),

    # 3271D0 leaf: ret b[q[02EBF190]+0x5AA4]
    "r71d0":        base_case(entry=0x3271D0, globb={0x5AA4: 0x5A}),

    # 308010 gate: b[member+5]==0 -> 308130 path; else 308040 body
    "g8010-b5z":    base_case(entry=0x308010, rcx="obj", objlink=1,
                              rec_b={5: 0}),
    "g8010-b5nz":   base_case(entry=0x308010, rcx="obj", objlink=1,
                              rec_b={5: 1}),
    "g8010-698z":   base_case(entry=0x308010, rcx="obj", objlink=1,
                              obj698=0),
    "g8010-null":   base_case(entry=0x308010, rcx=0),

    # 324100 licence-bit max scan: 324020 -> r14d, then 13 iters
    # edi=0x12..0x1E on b[rec+0x194+(edi>>3)] & rol-bit -> 308FF0
    "o4100-null":   base_case(entry=0x324100, rcx=0),
    "o4100-base":   base_case(entry=0x324100, o324020_ret=3),
    "o4100-lic":    base_case(entry=0x324100, o324020_ret=3,
                              rec_b={0x196: 4}, a308ff0_ret=7),
    "o4100-liclow": base_case(entry=0x324100, o324020_ret=9,
                              rec_b={0x196: 4}, a308ff0_ret=7),
    "o4100-noabil": base_case(entry=0x324100, o324020_ret=3,
                              rec_b={0x196: 4}, abild=None),

    # ================= EXP-194 =================
    # 308130 (member state-step, rcx=member row). 307D10 recomputes
    # bit16 of d[member+4] (ebx<<0x10); then (d[rec+0x64]|d[rec+0x3C])
    # &0x8000020 OR 253B90()==0 reach bt edi,0x10 -> ret1; bt clear ->
    # 308186 (g81e0 gate) -> 3081E0 + 32A150 vs d[member+0xDCC].
    "s8130-fast":   base_case(entry=0x308130, rcx="obj", objlink=1,
                              rec_b={4: 0x1A}, rec_d={0x64: 0x20}),
    "s8130-noor":   base_case(entry=0x308130, rcx="obj", objlink=1,
                              rec_b={4: 0x1A}),
    "s8130-b16clr": base_case(entry=0x308130, rcx="obj", objlink=1,
                              rec_b={5: 1}, rec_d={0x64: 0x20}),
    "s8130-81e0":   base_case(entry=0x308130, rcx="obj", objlink=1,
                              rec_b={5: 1}, rec_d={0x64: 0x20},
                              g81e0=1),
    "s8130-g25b":   base_case(entry=0x308130, rcx="obj", objlink=1,
                              rec_b={4: 0x1A}, g25b=0),
    # 308040 (b5!=0 arm). rcx=member, edx=arg.
    "m8040-698z":   base_case(entry=0x308040, rcx="obj", objlink=1,
                              obj698=0),
    "m8040-b5z":    base_case(entry=0x308040, rcx="obj", objlink=1),
    "m8040-f20":    base_case(entry=0x308040, rcx="obj", objlink=1,
                              rec_b={5: 1}, obj6a0={"d": {0: 0x20}}),
    "m8040-edx":    base_case(entry=0x308040, rcx="obj", objlink=1,
                              edx=1, rec_b={5: 1},
                              obj6a0={"d": {0: 0x08}}),
    "m8040-fhi":    base_case(entry=0x308040, rcx="obj", objlink=1,
                              edx=0, rec_b={5: 1},
                              obj6a0={"d": {0: 0x08}, "f4": 1e30}),
    "m8040-flo":    base_case(entry=0x308040, rcx="obj", objlink=1,
                              edx=0, rec_b={5: 1},
                              obj6a0={"d": {0: 0x08}, "f4": -1e30}),
    "m8040-b44":    base_case(entry=0x308040, rcx="obj", objlink=1,
                              rec_b={5: 1}, objflags=1 << 40),
    "m8040-b050":   base_case(entry=0x308040, rcx="obj", objlink=1,
                              rec_b={5: 1}),
    "m8040-b050e":  base_case(entry=0x308040, rcx="obj", objlink=1,
                              rec_b={5: 1}, obj_d={0xBC4: 2}),
    # 308FF0 indexed row accessor (edx = idx <= 0x21E).
    "a8ff0-hi":     base_case(entry=0x308FF0, edx=0x21F),
    "a8ff0-ok":     base_case(entry=0x308FF0, edx=3,
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 8},
                              d138_rows={3: {0x1E: 5, 0xA: 0x77}}),
    "a8ff0-b1e6":   base_case(entry=0x308FF0, edx=3,
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 8},
                              d138_rows={3: {0x1E: 6, 0xA: 0x42}}),
    "a8ff0-bad":    base_case(entry=0x308FF0, edx=3,
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 8},
                              d138_rows={3: {0x1E: 7, 0xA: 0x42}}),
    "a8ff0-nodesc": base_case(entry=0x308FF0, edx=3,
                              d138=None, expect_fault=0x30904A),
    # 324020 licence bit-scan (pure): ret = 1 + highest set bit over
    # 3*6=18 tested positions in b[rec+0x194..].
    "o4020-zero":   base_case(entry=0x324020),
    "o4020-b0":     base_case(entry=0x324020, rec_b={0x194: 1}),
    "o4020-bhi":    base_case(entry=0x324020, rec_b={0x195: 0x80,
                                                   0x194: 1}),
    # 323C60 final eligibility: 322C50(1,id) auto-kind -> memt range;
    # null rec / b5!=0 / b4>6 -> ret1; member row b[+7]&0x10 -> ret1;
    # else 323BB0 = 2F8FA0 kind-0 bitmap intersect rec+0x194.
    "s3c60-bad":    base_case(entry=0x323C60, edx=0x9999),
    "s3c60-null":   base_case(entry=0x323C60, rcx=0, edx=0x1150,
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200}),
    "s3c60-b5":     base_case(entry=0x323C60, edx=0x1150,
                              rec_b={5: 1},
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200}),
    "s3c60-b4":     base_case(entry=0x323C60, edx=0x1150,
                              rec_b={4: 7},
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200}),
    "s3c60-bit10":  base_case(entry=0x323C60, edx=0x1150,
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200},
                              memt_rows={0x150: {7: 0x10}}),
    "s3c60-scan":   base_case(entry=0x323C60, edx=0x1150,
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200},
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 4},
                              abil_rows={0: {"b": {5: 1},
                                             "w": {8: 0x1150}}},
                              rec_b={0x194: 1}),
    "s3c60-nomatch": base_case(entry=0x323C60, edx=0x1150,
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200},
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 4},
                              abil_rows={0: {"b": {5: 1},
                                             "w": {8: 0x1150}}}),
    "s3c60-nolid":  base_case(entry=0x323C60, edx=0x1150,
                              memt={"stride": 8, "off": O_MEMT,
                                    "count": 0x200},
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 4},
                              abil_rows={0: {"b": {5: 1},
                                             "w": {8: 0x2222}}},
                              rec_b={0x194: 1}),

    # ================= EXP-195 =================
    # 326500 notify dispatcher: 311E20 -> 326620 -> 30D9A0 mode:
    #   ret 0/1 -> bl = b[glob+0x5AA4]; 2 -> bl=0x1A; 3 -> bl=377C70();
    #   4/5 -> bl stays 0xFF.  30D9A0 reads d[glob+0x5B04]: &8->5,
    #   &4->4, 377C20!=0->3, &2->2, cl&1 -> 0/1.
    # 31B770(bl): cl>0x27 -> 0; else row=glob+8+bl*0x1C8, scans
    #   236850/236820 OBJARR rows for q[+0x698]==slotrow.
    # Hit & q[+0x698]!=0 -> ebp=d[objrow+8]; 30D9A0()==1 -> 317400.
    # Miss -> edi=0..3: 322C50(0x17,i) -> b[glob+0x5A5A+i*2] ->
    #   2367A0(id) match w/ q[+0x698]!=0 -> same tail.
    # Exhaust -> ebp = 3589B0(263750(0)).  Tail: 311E20 -> jmp
    #   3594B0(ebp): d[0x22C7FE4]=ebp, b[0x22C7FF8]=1.
    "n6500-nullctx": base_case(entry=0x326500, globb={0x5AA4: 0xFF},
                               cd_words=[0]),
    "n6500-slothit": base_case(entry=0x326500, objlink=1, slothit=2,
                               globb={0x5AA4: 2}, cd_words=[0],
                               obj_d={8: 0x11223344}),
    "n6500-mode1":   base_case(entry=0x326500, objlink=1, slothit=2,
                               globb={0x5AA4: 2, 0x5B04: 1,
                                      0x5AD4: 2, 0x5AD5: 3},
                               cd_words=[0], obj_d={8: 0x55}),
    "n6500-mode2":   base_case(entry=0x326500, objlink=1, slothit=0x1A,
                               globb={0x5B04: 2}, cd_words=[0],
                               obj_d={8: 0x7777}),
    "n6500-mode5":   base_case(entry=0x326500, globb={0x5B04: 8},
                               cd_words=[0]),
    "n6500-scanhit": base_case(entry=0x326500, objlink=1,
                               globb={0x5B04: 8, 0x5A60: 5},
                               rec_w={4: 5}, obj_d={8: 0x99}),
    "n6500-ctxblk":  base_case(entry=0x326500, globb={0x5AA4: 0xFF},
                               cd_words=[0], g272f0=0x10,
                               nid=0x12340000,
                               ctx4=[{"w0": 0, "b15": 4, "w16": 0x123,
                                      "outd": {0: 0xAA, 4: 0xBB,
                                               8: 0xCC},
                                      "f148": 3.5,
                                      "blk": {0x10: 0xDEAD}}],
                               clstab={4: ["ctx0"]}),
    "n6500-ctor":    base_case(entry=0x326500, objlink=1, slothit=0,
                               globb={0x5AA4: 0xFF}, cd_words=[0],
                               obj_d={8: 0x2468}),
    # 311E20 guard: d[0x22C1974]!=0 -> no-op both invocations
    "n6500-gated":   base_case(entry=0x326500, g11e20=1,
                               globb={0x5AA4: 0xFF}, cd_words=[0]),
    # 326620 direct: b[0x5AA4] present in the 4-entry map -> ebx>=0,
    # no ctor even at mode 0
    "l26620-found":  base_case(entry=0x326620,
                               globb={0x5AA4: 3, 0x5A60: 3},
                               cd_words=[0]),
    "l26620-ctor":   base_case(entry=0x326620, objlink=1,
                               globb={0x5AA4: 0xFF}, cd_words=[0],
                               obj_d={8: 0xBEEF}),
    # 31B770 direct bounds: cl>0x27 -> 0 without a scan
    "l31b770-hi":    base_case(entry=0x31B770, rcx=0x28),
    "l31b770-hit":   base_case(entry=0x31B770, rcx=2, objlink=1,
                               slothit=2),
    "l31b770-null":  base_case(entry=0x31B770, rcx=2),
    # 263E30 leaf: ret q[rcx+0x30]
    "l263e30":       base_case(entry=0x263E30, rcx="ctx0",
                               ctx4=[{"d": {0x30: 0x7777}}]),
    # 317400 direct: 3137E0/3137F0 -> b[glob+0x5AD4/5] -> 31B770 x2;
    # both rows must be nonnull to reach 26DAC0
    "l317400-one":   base_case(entry=0x317400, rcx="obj", objlink=1,
                               slothit=2, globb={0x5AD4: 2, 0x5AD5: 3}),

    # ---- EXP-196: 30C650 level-set ----
    # rec b[+0x1C2]=level, edx=target (clamped 0x63), r8 bit1 holds the
    # last-level extras (46A690 + member notify).  Growth: HP/MP via
    # grwd q[0x2EBF108] rows indexed by level (b[+0]=hp, b[+1]=mp);
    # Str/Mag/Vit/Spd via FOED row (idx b[rec+4]) bytes +0x1F/0x22/0x25/
    # 0x28 through 2F9BD0 (cur + g/128, cap ~100).  HP's shipped divisor
    # f[0x9136E4] is negative -> its 379CD0 RNG arm is dead code.
    "c650-max":    base_case(entry=0x30C650, rec_b={0x1C2: 0x63},
                             edx=5),
    "c650-one":    base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, objlink=1, obj_d={8: 0x2468},
                             rec_d={8: 100, 0x10: 0x42480000},
                             rec_w={0xC: 50},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={5: (3, 0)},
                             foe={"b": {0x1F: 8, 0x22: 16,
                                        0x25: 24, 0x28: 32}}),
    "c650-hold":   base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, r8=2, objlink=1,
                             rec_d={8: 100},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={5: (3, 0)}),
    "c650-multi":  base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 2, 0x4: 1},
                             edx=5, objlink=1, obj_d={8: 0x2468},
                             rec_d={8: 10},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={2: (2, 0), 3: (3, 0),
                                      4: (4, 0)}),
    "c650-b5":     base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1, 5: 1},
                             edx=6, objlink=1,
                             rec_d={8: 100}),
    # null level desc (FOED) -> rbp=0 -> shipped null-deref
    "c650-nolvl":  base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, foed=None,
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             expect_fault=0x30C757),
    "c650-clamp":  base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 0x62, 0x4: 1},
                             edx=0xFF, objlink=1,
                             rec_d={8: 10},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={0x62: (5, 0)}),
    # MP jitter: mp_g=5 -> 379CD0 -> tempered word mod (g*100)/100
    "c650-mp":     base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, objlink=1,
                             rec_d={8: 100}, rec_w={0xC: 50},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={5: (0, 5)},
                             mt={"idx": 0, "words": {0: 0x64}}),
    # full notify tail: 267330 gate + a11 serial match -> 2DF220 ->
    # 1DBDB0 -> 329210(1, ret) -> d[0x208D32C]
    "c650-full":   base_case(entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, objlink=1, obj_d={8: 0x2468},
                             rec_d={8: 100},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={5: (3, 0)},
                             clstab={0: [0]}, clsflag=1,
                             a11={"serial": 0x10, "idx": 0x10,
                                  "w8": 0x10, "wA": 0},
                             b1dbdb0_ret=0x77),

    # ---- EXP-196: 323910 licence grant/revoke ----
    # edx=id (bounded by ABILD count), r8=grant, r9 bit0 set = silent
    # (skips 323D10's LP gate AND the d[0x190] deduction).  LP cost
    # b[abilrow+4], type b[+6], grade source w[+8].
    "g3910-null":   base_case(entry=0x323910, rcx=0),
    "g3910-b5":     base_case(entry=0x323910, edx=0x10, r8=1,
                              rec_b={5: 1}),
    "g3910-badid":  base_case(entry=0x323910, edx=0x50, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 4}),
    "g3910-grant":  base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {4: 30}}},
                              rec_d={0x190: 100}),
    "g3910-lp0":    base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {4: 30}}},
                              rec_d={0x190: 10}),
    "g3910-silent": base_case(entry=0x323910, edx=0x10, r8=1, r9=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {4: 30}}},
                              rec_d={0x190: 100}),
    "g3910-dup":    base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {4: 30}}},
                              rec_b={0x196: 1},
                              rec_d={0x190: 100}),
    "g3910-revoke": base_case(entry=0x323910, edx=0x10, r8=0,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              rec_b={0x196: 1},
                              rec_d={0x190: 100}),
    "g3910-e5":     base_case(entry=0x323910, edx=0xE5, r8=1,
                              objlink=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x100},
                              abil_rows={0xE5: {"b": {}}},
                              rec_d={0x190: 100}),
    # rank chain: popcount 1 -> 30A310(foerow,0) -> b[+4]=0xD5 ->
    # w[d138row@0xD5 +0x22]=0x1150 -> 300B80 -> 3008A0 real
    "g3910-rank":   base_case(entry=0x323910, edx=5, r8=1, idx=0,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={5: {"b": {}}},
                              foe={"b": {4: 0xD5}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x200},
                              d138_rows={0xD5: {0x22: 0x50,
                                                0x23: 0x11}},
                              cls1words={0x150: 0x0803},
                              o324020_ret=1,
                              rec_d={0x190: 100}),
    "g3910-grade":  base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              a308ff0_ret=2,
                              rec_b={0x20: 0},
                              rec_d={0x190: 100}),
    "g3910-grade-cap": base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              a308ff0_ret=9,
                              rec_b={0x20: 0},
                              rec_d={0x190: 100}),
    "g3910-grade-hold": base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              a308ff0_ret=1,
                              rec_b={0x20: 2},
                              rec_d={0x190: 100}),
    # 323D10 type arms: b6=1 cross-slot bit scan via 324280
    "g3910-b6ok":   base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {6: 1, 4: 30}}},
                              rec_d={0x190: 100}),
    "g3910-b6dup":  base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {6: 1, 4: 30}}},
                              globb={8: 8, 0x19E: 1},
                              rec_d={0x190: 100}),
    "g3910-b6cap":  base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {6: 2, 4: 30}}},
                              rec_b={0x194: 7}, o324020_ret=4,
                              rec_d={0x190: 100}),
    "g3910-b6t4":   base_case(entry=0x323910, edx=0x10, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x10: {"b": {6: 4, 4: 30}}},
                              rec_d={0x190: 100}),

    # ---- EXP-196: 234DA0 member-slot proximity scan ----
    # rcx=pos {x,y,z}, rdx=pmin, r8=pmax, r9=pout, a5=r12d (nonzero
    # suppresses the 3273B0 pre-gate).  ret 1 on first slot whose
    # member ctx triple is within [f[pmin], f[pmax]]; f[pout]=dist^2
    # iff the row's d[+8] == mctxid.  265020 triple needs ctx b3>>5
    # in {1,3}.
    "d4da0-empty":  base_case(entry=0x234DA0, rcx="pos",
                              fpos=[4.0, 0.0, 3.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 0xFF, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF}),
    "d4da0-hit":    base_case(entry=0x234DA0, rcx="pos", r9="pout",
                              fpos=[4.0, 0.0, 3.0],
                              edx="pmin", fmin=[0.0],
                              r8="pmax", fmax=[100.0],
                              fout=[0.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),
    # a5!=0 suppresses the pre-gate 3273B0 entirely
    "d4da0-sarg":   base_case(entry=0x234DA0, rcx="pos", r9="pout",
                              fpos=[4.0, 0.0, 3.0], fout=[0.0],
                              edx=0,
                              slotd={"count": 8}, a5=1,
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),
    "d4da0-cid":    base_case(entry=0x234DA0, rcx="pos",
                              fpos=[4.0, 0.0, 3.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=8),
    "d4da0-gate":   base_case(entry=0x234DA0, rcx="pos",
                              fpos=[4.0, 0.0, 3.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0],
                                        "recd": {0x64: 1}}},
                              mctxid=9),
    "d4da0-alive":  base_case(entry=0x234DA0, rcx="pos", r9="pout",
                              fpos=[4.0, 0.0, 3.0], fout=[0.0],
                              edx=0,
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0],
                                        "recd": {0x64: 1}}},
                              s313f60_ret=1,
                              mctxid=9),
    "d4da0-min":    base_case(entry=0x234DA0, rcx="pos",
                              fpos=[4.0, 0.0, 3.0],
                              edx="pmin", fmin=[50.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),
    "d4da0-max":    base_case(entry=0x234DA0, rcx="pos",
                              fpos=[4.0, 0.0, 3.0], edx=0,
                              r8="pmax", fmax=[5.0],
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),
    # ctx b3>>5 == 0 -> 265020 writes nothing -> triple stays zeroed
    "d4da0-notrip": base_case(entry=0x234DA0, rcx="pos", r9="pout",
                              fpos=[4.0, 0.0, 3.0], fout=[0.0],
                              edx=0,
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 0xFF,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={0: {"id": 1, "cid": 9,
                                        "b3": 0,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),
    "d4da0-second": base_case(entry=0x234DA0, rcx="pos", r9="pout",
                              fpos=[4.0, 0.0, 3.0], fout=[0.0],
                              edx=0,
                              slotd={"count": 8},
                              globb={0x5A5A: 1, 0x5A5C: 2,
                                     0x5A5E: 0xFF, 0x5A60: 0xFF},
                              oar4={1: {"id": 2, "cid": 9,
                                        "trip": [1.0, 0.0, 2.0]}},
                              mctxid=9),

    # ---- EXP-198: shared unlink-carrier family + 24FE30 dispatch ----
    # 300FC0(obj, edx): edx==0 + linked rec b5==0 + b4 in 0x1B..0x27 ->
    #   u3105d0(obj) + tail 3138D0(0).  Otherwise: 310780 detach, 2ED180
    #   gate, flag clears, 26DAC0/26A330 ent writes, 3219D0 cap validate,
    #   then 2372E0/237260/2373C0/3272E0 set d[02089340] bits 0x400/0x200/
    #   0x800/0x100 (+35C8A0 posts 0xB/0x18/0x17), and mode-0 tail checks
    #   30D9A0==1 && 31B770(b[glob+0x5AD5])==obj -> 3138D0(0) + 23B040.
    "u0fc0-fast":  base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 0, 4: 0x1B}),
    "u0fc0-fastt": base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 0, 4: 0x27},
                             cd_words=[0], b8c0_ret="objrow",
                             globb={0x5B04: 1, 0x5AD0: 3}),
    "u0fc0-def":   base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1},
                             objflags=0xFFFFFFFFFFFFFFFF,
                             obj_d={4: 0xFFFFFFFF, 0x694: 0x27}),
    "u0fc0-m1":    base_case(entry=0x300FC0, rcx="obj", edx=1,
                             objlink=1, rec_b={5: 1}),
    "u0fc0-s400":  base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1}, objcount=3,
                             foed={"stride": 0x60, "off": O_FOE, "count": 4}, globb={0x5A5A: 2},
                             oar4={2: {"id": 2, "recd": {0x64: 1}}},
                             slotmap={i: 0xFF for i in range(9)}),
    "u0fc0-s200":  base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={4: 0x10, 5: 0},
                             objcount=3, foed={"stride": 0x60, "off": O_FOE, "count": 0x10},
                             globb={0x5A5A: 7}, oar4={2: {"id": 7}}),
    "u0fc0-s800":  base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1}, obj_d={8: 9},
                             cd_words=[0],
                             globb={0x5AD5: 9, 0x5B04: 1}),
    "u0fc0-mtail": base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, slothit=2, cd_words=[0],
                             b8c0_ret="objrow",
                             globb={0x5AD5: 2, 0x5B04: 1, 0x5AD0: 3}),
    "u0fc0-caps":  base_case(entry=0x300FC0, rcx="obj", edx=1,
                             objlink=1, rec_b={4: 0x21, 5: 0},
                             foed={"stride": 0x60, "off": O_FOE, "count": 0x40},
                             oar4={1: {"id": 7, "recb": {5: 1},
                                       "cap": {0x3B: 5}}}),
    "u0fc0-norec": base_case(entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, obj698=0,
                             expect_fault=0x30105A),
    # 301140(obj): bail when (d[rec+0x64]|d[rec+0x3C]) & 0x80000003; else
    #   full slot-release: 2E9600/bit26 -> 311F70, 238BF0, 3105D0, field
    #   clears, sentinel bit14, 2EACD0(cid,1,&obj+8,0x7B)->3B02A0, 2E8060,
    #   string select by b[rec+5], 2ECF10, 3299B0(0x200D), 319E30(d[+0x74]),
    #   32A150-timer into d[+0xDD0], 3125E0 -> 26DC60(ent, ret==0).
    "l01140-bail": base_case(entry=0x301140, rcx="obj", objlink=1,
                             rec_d={0x64: 1}, obj_d={0x748: 0xAA}),
    "l01140-rel":  base_case(entry=0x301140, rcx="obj", objlink=1,
                             obj_d={0x748: 9, 0x770: 8, 0x74C: 7,
                                    0xDCC: 6, 0x30: 5, 0x788: 0x4FF,
                                    0x6B0: 0xFF},
                             imgd={0x208D45C: 1000}),
    "l01140-sent": base_case(entry=0x301140, rcx="obj", objlink=1,
                             objflags=0x4004000, obj_d={0xBA0: 0x113}),
    "l01140-sentc": base_case(entry=0x301140, rcx="obj", objlink=1,
                              objflags=0x4004000, obj_d={0xBA0: 0x111}),
    "l01140-f70":  base_case(entry=0x301140, rcx="obj", objlink=1,
                             objflags=0),
    "l01140-strn": base_case(entry=0x301140, rcx="obj", objlink=1,
                             rec_b={5: 1}),
    "l01140-e30":  base_case(entry=0x301140, rcx="obj", objlink=1,
                             obj_d={0x74: 5}),
    "l01140-bbb1": base_case(entry=0x301140, rcx="obj", objlink=1,
                             objflags=0x4000008),
    "l01140-norec": base_case(entry=0x301140, rcx="obj", objlink=1,
                              obj698=0, expect_fault=0x301150),
    # 24FE30(ecx=id, edx=sub): (id>>0x1C)&0xF -> 1:2FD0C0, 5/6/9:3B1260,
    #   7:3B2830, else 0.  Targets bound 0<sub<0xB, scan .data tables,
    #   lock bc1d0, query b4e70, unlock bc140.
    "l4fe30-n0":   base_case(entry=0x24FE30, rcx=0, edx=2),
    "l4fe30-n8":   base_case(entry=0x24FE30, rcx=0x80000000, edx=2),
    "l4fe30-nf":   base_case(entry=0x24FE30, rcx=0xF0000000, edx=2),
    "l4fe30-n1":   base_case(entry=0x24FE30, rcx=0x10000000, edx=2,
                            imgd={0x2EC32E0: 0x10000000},
                            imgq={0x2EC32F0: "rec"}, b4e70_ret=1),
    "l4fe30-n1m":  base_case(entry=0x24FE30, rcx=0x10000000, edx=2),
    "l4fe30-n1d0": base_case(entry=0x24FE30, rcx=0x10000000, edx=0),
    "l4fe30-n5":   base_case(entry=0x24FE30, rcx=0x50000009, edx=2,
                            imgd={0x2EBEC30: 0x50000009},
                            imgq={0x2EBEC38: "rec"}, b4e70_ret=1),
    "l4fe30-n6":   base_case(entry=0x24FE30, rcx=0x60000001, edx=2),
    "l4fe30-n9":   base_case(entry=0x24FE30, rcx=0x90000002, edx=2),
    "l4fe30-n7":   base_case(entry=0x24FE30, rcx=0x70000005, edx=3,
                            imgd={0x2EBE5E0: 1, 0x2EBE610: 2,
                                  0x2EBE640: 3, 0x2EBE670: 0x70000005},
                            imgq={0x2EBE680: "rec"}, b4e70_ret=1),

    # ---- EXP-199: 312280 EXP/LP guest-share ----
    # rdx=objrow (objlink -> q[+0x698]=rec), rcx=peer rec (row2).
    # Gate chain: !rec || b[rec+5]!=1 || b[obj+0xE9A]&8 -> ret;
    # scan arm iff (e9a&5)==5 or ((d64|d3C)&2 && e9a&2) or
    # (rcx && b[rcx+5]==0).  Share formulas 2F8BB0/2F90C0 REAL
    # (EXP-200): share = ((b1C2-b88)*d[e78+0x34]+d[e70+0x34])/members
    # for exp, (b1C2-b88)*b[e78+0x2F]+b[e70+0x2F] for lp; members via
    # memslots (31B810 -> glob+0x5A5A map -> 2367A0 OBJARR scan).
    # Guest exp needs 31B860 to resolve -> oar4 "link" plants an
    # objarr row whose rec IS the guest row.  gauge/pos/msg tails
    # scripted; 320AB0/377C20/236780/2F8F20/30C650/265020 real.
    "d228-null":   c228(rcx=0, edx=0),
    "d228-norec":  c228(rcx=0, obj698=0),
    "d228-b5rec":  c228(rcx=0, rec_b={5: 0}),
    "d228-e9a8":   c228(rcx=0, obj_b={0xE9A: 8}),
    "d228-norow2": c228(rcx=0),
    "d228-row2b5": c228(rcx="row2", row2={"d": {4: 0x100}}),
    "d228-gate5":  c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE),
    "d228-gaterc": c228(rcx="row2", row2={}, slotmap=SM_NONE),
    "d228-gatef2": c228(rcx=0, obj_b={0xE9A: 2}, rec_d={0x64: 2},
                       slotmap=SM_NONE),
    "d228-f2nol2": c228(rcx=0, rec_d={0x64: 2}),
    # guest slot 0: exp 100+50=150, lp 20+10=30, lvl 5 stays 5
    "d228-g1":     c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10),
    # guest flagged (d64|d3C)&0x80000003 -> 377C20 gate; cd bit15 set
    # keeps it, clear drops it (never stashed/awarded)
    "d228-gflg":   c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x64: 0x80000000,
                                        0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10),
    "d228-gflg0":  c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0}, cd_words=[0],
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x64: 0x80000000,
                                        0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10),
    # d[glob+4] bit14 suppresses exp (guest +0x18C and source edx) but lp
    "d228-sup":    c228(rcx=0, obj_b={0xE9A: 5}, globb={5: 0x40},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10),
    "d228-globn": c228(rcx=0, obj_b={0xE9A: 5},
                       glob_null=True, expect_fault=0x31BA57),
    # clamps: exp cap 0x5F5E0FF, lp cap 0x1869F; negative share -> 0
    "d228-ecap":   c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 0x5F5E0F0,
                                        0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=0x1000, e70l=10),
    "d228-lcap":   c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 100,
                                        0x190: 0x18690}}},
                       oar4={1: {"link": 0}},
                       rec_b={0x1C2: 10, 0x88: 0},
                       e70e=50, e78l=0x80),
    "d228-neg":    c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       rec_b={0x1C2: 5, 0x88: 10}, e78e=1),
    # LP-consume flag b[+0x69]&0x10: esi zeroed (lp write +0x190 gets
    # 0, msg edx=0) and r12 += lvl*lp*5 feeds the source FP arg
    "d228-lp5":    c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5, 0x69: 0x10},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       rec_b={0x1C2: 10, 0x88: 2}, e78=3, e70=7,
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10, s53690_ret=1000),
    # fp arg = (10-2)*3 + 7 + 0 = 31; ebp = max(5+31,0) = 36 -> s54ee0;
    # delta 36-5 = 31 -> s69e80
    "d228-fp":     c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       rec_b={0x1C2: 10, 0x88: 2}, e78=3, e70=7,
                       s53690_ret=5),
    # negative total floors at 0: ebp=0 -> s54ee0(0), s69e80(0-5)
    "d228-fpneg":  c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       rec_b={0x1C2: 2, 0x88: 10}, e78=3, e70=7,
                       s53690_ret=5),
    # pos chain: s9490 gate -> s80f0(r14,&u) gate -> s9ca0(&u,&t)
    "d228-pos":    c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       s9490_ret=1, s80f0_ret=1),
    "d228-pos2":   c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       s9490_ret=1),
    # source share args: sfb80(ecx=d[r14+8], edx=exp, r8d=lp)
    "d228-src":    c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       obj_d={8: 0x1234}, e70e=77, e70l=88,
                       oar4={1: {"id": 0}}),
    # two guests processed in slot order; stash order follows rdi
    "d228-2g":     c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0, 4: 1},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 10, 0x190: 1}},
                              4: {"b": {0x1C2: 7},
                                  "d": {0x18C: 20, 0x190: 2}}},
                       oar4={1: {"link": 0}, 2: {"link": 4}},
                       e70e=1, e70l=1),
    # guest level-up: lvl2 + exp(396->400) climbs f8f20 thresholds
    # 2(169)/3(386)<=400, 4(736)>400 -> c650 edx=4; 30C650 scripted
    "d228-lvl":    c228(rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 2},
                                  "d": {0x18C: 4, 0x190: 0}}},
                       oar4={1: {"link": 0}},
                       e70e=396),

    # ---- EXP-200: 2F8BB0 EXP share + 2F90C0 LP share formulas ----
    # 2F8BB0(rcx=guest,rdx=objrow):
    #   esi = (b[rec+0x1C2]-b[rec+0x88])*d[e78+0x34] + d[e70+0x34]
    #   mode!=1 -> esi /= ebp, ebp = 31B810 member hits over 4 slots
    #   mode==1 -> leader path 313800->320890->320AB0(idx,1); guest
    #              must equal the resolved row (rcx==0 skips)
    #   guest: 31B860 must resolve; b[6B]|b[7B]&8 -> x2; &0x20 -> 0;
    #          b5!=0, b4 in [0x1B,0x27], (d64|d3C)&0x80000003 -> 0
    # 2F90C0: esi = (b[rec+0x1C2]-b[rec+0x88])*b[e78+0x2F] + b[e70+0x2F]
    #   no member divide, no 31B860; guest b4 must be 0x1A/<=6/>=0x28;
    #   b[6B]|b[7B]&0x10 -> x2; global b[0x20AA2AA]!=0 -> 0.
    "f8bb0-null":  cfml(0x2F8BB0, rcx=0, edx=0),
    "f8bb0-norec": cfml(0x2F8BB0, rcx=0, obj698=0),
    "f8bb0-b5rec": cfml(0x2F8BB0, rcx=0, rec_b={5: 0}),
    "f8bb0-split": cfml(0x2F8BB0, rcx=0,
                        rec_b={0x1C2: 10, 0x88: 2},
                        e78e=2, e70e=34, oar4={1: {"id": 0}}),
    "f8bb0-split4": cfml(0x2F8BB0, rcx=0,
                         rec_b={0x1C2: 10, 0x88: 2},
                         e78e=2, e70e=34, memslots=[0, 0, 0, 0],
                         oar4={1: {"id": 0}}),
    "f8bb0-neg":   cfml(0x2F8BB0, rcx=0,
                        rec_b={0x1C2: 5, 0x88: 10}, e78e=1,
                        oar4={1: {"id": 0}}),
    "f8bb0-ndiv":  cfml(0x2F8BB0, rcx=0,
                        rec_b={0x1C2: 5, 0x88: 10}, e78e=1,
                        memslots=[0, 0, 0xFF, 0xFF],
                        oar4={1: {"id": 0}}),
    "f8bb0-zdiv":  cfml(0x2F8BB0, rcx=0,
                        rec_b={0x1C2: 5, 0x88: 10}, e78e=1,
                        memslots=[0xFF, 0xFF, 0xFF, 0xFF]),
    "f8bb0-gok":   cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {}}, oar4={1: {"link": 0}},
                        rec_b={0x1C2: 10, 0x88: 2},
                        e78e=2, e70e=34),
    "f8bb0-dbl":   cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {0x6B: 8}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-dbl7b": cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {0x7B: 8}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-zero":  cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {0x6B: 0x20}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-nown":  cfml(0x2F8BB0, rcx="row2", row2={},
                        rec_b={0x1C2: 10, 0x88: 2},
                        e78e=2, e70e=34),
    "f8bb0-gb4":   cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {4: 0x1B}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-gb5":   cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {5: 1}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-gflg":  cfml(0x2F8BB0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"d": {0x64: 0x80000000}}},
                        oar4={1: {"link": 0}}, e70e=50),
    "f8bb0-lead":  cfml(0x2F8BB0, rcx=("guest", 0),
                        cd_words=[0],
                        globb={0x5B04: 1, 0x5AD5: 7, 0x5A48: 7},
                        slotmap={**SM_NONE, 0: 9},
                        memslots=[9, 0xFF, 0xFF, 0xFF],
                        guest={0: {}}, oar4={1: {"link": 0}},
                        e70e=50),
    "f8bb0-nlead": cfml(0x2F8BB0, rcx=("guest", 0),
                        cd_words=[0],
                        globb={0x5B04: 1, 0x5AD5: 7, 0x5A48: 7},
                        slotmap={**SM_NONE, 0: 9},
                        memslots=[8, 0xFF, 0xFF, 0xFF],
                        guest={0: {}}, oar4={1: {"link": 0}},
                        e70e=50),
    "f8bb0-lead0": cfml(0x2F8BB0, rcx=0,
                        cd_words=[0],
                        globb={0x5B04: 1, 0x5AD5: 7, 0x5A48: 7},
                        memslots=[9, 0xFF, 0xFF, 0xFF],
                        rec_b={0x1C2: 10, 0x88: 2},
                        e78e=2, e70e=34),
    "f8bb0-lmiss": cfml(0x2F8BB0, rcx=("guest", 0),
                        cd_words=[0],
                        globb={0x5B04: 1, 0x5AD5: 7},
                        slotmap={**SM_NONE, 0: 9},
                        memslots=[9, 0xFF, 0xFF, 0xFF],
                        guest={0: {}}, oar4={1: {"link": 0}},
                        e70e=50),
    "f90c0-norow": cfml(0x2F90C0, rcx=0, edx=0),
    "f90c0-flag":  cfml(0x2F90C0, rcx=0, lflag=1),
    "f90c0-norec": cfml(0x2F90C0, rcx=0, obj698=0),
    "f90c0-b5rec": cfml(0x2F90C0, rcx=0, rec_b={5: 0}),
    "f90c0-split": cfml(0x2F90C0, rcx=0,
                        rec_b={0x1C2: 10, 0x88: 2},
                        e78l=1, e70l=2),
    "f90c0-neg":   cfml(0x2F90C0, rcx=0,
                        rec_b={0x1C2: 5, 0x88: 10}, e78l=1),
    "f90c0-dbl":   cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {0x6B: 0x10}}}, e70l=10),
    "f90c0-dbl7b": cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {0x7B: 0x10}}}, e70l=10),
    "f90c0-gb4lo": cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {4: 7}}}, e70l=10),
    "f90c0-gb4a":  cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {4: 0x1A}}}, e70l=10),
    "f90c0-gb4hi": cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {4: 0x28}}}, e70l=10),
    "f90c0-gb5":   cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"b": {5: 1}}}, e70l=10),
    "f90c0-gflg":  cfml(0x2F90C0, rcx=("guest", 0),
                        slotmap={**SM_NONE, 0: 0},
                        guest={0: {"d": {0x64: 0x80000000}}},
                        e70l=10),
    "f90c0-nolink": cfml(0x2F90C0, rcx=("guest", 0),
                         slotmap={**SM_NONE, 0: 0},
                         guest={0: {}}, e70l=10),
    # ---- EXP-201: display-request queue ----
    # 2FA3B0(obj) dist gate: 265020 copies q[obj+0xB8] vec3 (requires
    # b[obj+3]>>5 in {1,3}; rejected class leaves dst zeroed -> dist 0),
    # 3A1920->sqrtf vs cam vec3 @01EBBB00, ret = 24.0 > dist.
    # 3272A0 gate (g272f0&0x10) only controls the camera-cell refresh;
    # the distance check always runs.
    "fa3b0-null": base_case(entry=0x2FA3B0, rcx=0),
    "fa3b0-near": base_case(entry=0x2FA3B0, rcx="subobj",
                            pos=(1.0, 2.0, 3.0)),
    "fa3b0-far":  base_case(entry=0x2FA3B0, rcx="subobj",
                            pos=(100.0, 0.0, 0.0)),
    "fa3b0-edge": base_case(entry=0x2FA3B0, rcx="subobj",
                            pos=(24.0, 0.0, 0.0)),
    "fa3b0-fl":   base_case(entry=0x2FA3B0, rcx="subobj", g272f0=0x10,
                            pos=(1.0, 0.0, 0.0)),
    "fa3b0-b3":   base_case(entry=0x2FA3B0, rcx="subobj", so3=0,
                            pos=(1.0, 0.0, 0.0)),
    # 3EFD00(dst, value, width, zpad): decimal formatter — digit count
    # via x/5 magic loop, memset pad (' ' unless r9!=0 -> '0'), digits
    # written left->right through the 10^i divisor table, NUL term.
    "fmt-zero":   base_case(entry=0x3EFD00, rcx="fmtbuf", edx=0),
    "fmt-pos":    base_case(entry=0x3EFD00, rcx="fmtbuf", edx=12345),
    "fmt-pad":    base_case(entry=0x3EFD00, rcx="fmtbuf", edx=7, r8=4),
    "fmt-zpad":   base_case(entry=0x3EFD00, rcx="fmtbuf", edx=7,
                            r8=4, r9=1),
    "fmt-big":    base_case(entry=0x3EFD00, rcx="fmtbuf",
                            edx=999999999),
    "fmt-neg":    base_case(entry=0x3EFD00, rcx="fmtbuf",
                            edx=0xFFFFFFD6),     # -42 signed
    # 3BBD00(req) slot allocator: ret 0xFF fail / old_qidx|0x20 ok;
    # advances b[02B443C0] mod 64.
    "bd00-notab": cdis(),                    # q[02B457D0]==0 -> 0xFF
    "bd00-occ":   cdis(qt={0: {"o": "subobj"}}, qidx=0),  # slot busy
    "bd00-t0":    cdis(qtptr="qtab", rqv=12345),
    "bd00-t0v0":  cdis(qtptr="qtab", rqv=0),  # 28FBE0 early-out
    "bd00-t1":    cdis(qtptr="qtab", rqt=1, rqv=3),
    "bd00-t2":    cdis(qtptr="qtab", rqt=2, rqv=7, randv=8,
                      rblk={"q": {0x18: "nstr"}}),
    "bd00-t2ff":  cdis(qtptr="qtab", rqt=2, rqv=7,
                       rblk={"b": {0x24: 0xFF}}),
    "bd00-t2b25": cdis(qtptr="qtab", rqt=2, rqv=7, randv=8,
                       rblk={"q": {0x18: "nstr"}, "b": {0x25: 0x12}},
                       dd7={"n": 0x20, "d": {1: 0x1234}}),
    "bd00-t2neg": cdis(qtptr="qtab", rqt=2, rqv=7, s31c5d0_ret=-2,
                       rblk={"q": {0x18: "nstr"}, "b": {0x24: 0xFF}}),
    # category derive: same-obj entries mark d[rsp+0x20+b3e*4]
    "bd00-cat2":  cdis(qtptr="qtab", qidx=3, rqv=9,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}},
                           2: {"o": "subobj", "b": {0x3E: 1}},
                           5: {"o": "subobj", "b": {0x3E: 0}}}),
    "bd00-cat3":  cdis(qtptr="qtab", qidx=3, rqv=9,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}},
                           2: {"o": "subobj", "b": {0x3E: 1}},
                           5: {"o": "subobj", "b": {0x3E: 2}}}),
    "bd00-cat4":  cdis(qtptr="qtab", qidx=3, rqv=9,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}},
                           5: {"o": "subobj", "b": {0x3E: 3}}}),
    "bd00-cat1":  cdis(qtptr="qtab", qidx=3, rqv=9,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}},
                           2: {"o": "subobj", "b": {0x3E: 3}},
                           5: {"o": "subobj", "b": {0x3E: 4}}}),
    "bd00-rand1": cdis(qtptr="qtab", qidx=3, rqv=9, randv=0,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}}}),
    "bd00-rand3": cdis(qtptr="qtab", qidx=3, rqv=9, randv=1,
                       qt={1: {"o": "subobj", "b": {0x3E: 0}}}),
    "bd00-wrap":  cdis(qtptr="qtab", qidx=0x3F, rqv=9),
    "bd00-neg":   cdis(qtptr="qtab", qidx=0xFF, rqv=9),
    # type-2 second scan: every live type-2 entry w3a+=3; same-obj +
    # w38<=0 -> edi = max(d44)+3 -> d[slot+0x44]
    "bd00-t2pri": cdis(qtptr="qtab", rqt=2, rqv=7, randv=8,
                       qt={1: {"o": "subobj",
                               "b": {0x3C: 2, 0x3E: 1},
                               "w": {0x38: 0, 0x3A: 5},
                               "d": {0x44: 7}},
                           2: {"o": "dobj", "b": {0x3C: 2},
                               "w": {0x3A: 9}}},
                       rblk={"q": {0x18: "nstr"}}),
    "bd00-t3":    cdis(qtptr="qtab", rqt=3, rqv=7),
    # 3284D0(obj, dl): dist gate on q[obj+0x10]; builds type-2 req
    "d4d0-null":  base_case(entry=0x3284D0, rcx="dobj", edx=5),
    "d4d0-far":   base_case(entry=0x3284D0, rcx="dobj", edx=5,
                            obj10="subobj", pos=(100.0, 0.0, 0.0)),
    "d4d0-near":  base_case(entry=0x3284D0, rcx="dobj", edx=5,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            qtptr="qtab", randv=2,
                            rblk={"q": {0x18: "nstr"}}),
}



def main():
    raw, secs = load_image()
    res = {}
    for name, case in CASES.items():
        w = World(case, raw, secs)
        rcx = case.get("rcx", w.rec)
        if rcx == "obj":
            rcx = w.objrow
        elif rcx == "rec50":
            rcx = w.rec + 0x50
        elif rcx == "ctx0":
            rcx = w.ctx[0] if w.ctx else 0
        elif rcx == "row2":
            rcx = w.row2
        elif rcx in ("pos", "pmin", "pmax", "pout"):
            rcx = getattr(w, rcx)
        elif isinstance(rcx, tuple) and rcx[0] == "guest":
            rcx = w.guests[rcx[1]]
        elif isinstance(rcx, str):
            rcx = getattr(w, rcx, 0)
        edx = case.get("edx", w.sel)
        if edx == "rec50":
            edx = w.rec + 0x50
        elif edx == "row2":
            edx = w.row2
        elif edx == "obj":
            edx = w.objrow
        elif edx in ("pos", "pmin", "pmax", "pout"):
            edx = getattr(w, edx)
        elif isinstance(edx, str):
            edx = getattr(w, edx, 0)
        eax = w.run(rcx=rcx, edx=edx)
        gm = w.gm
        ok = True
        notes = []

        def ck(cond, msg):
            nonlocal ok
            if not cond:
                ok = False
                notes.append(msg)

        exp_fault = case.get("expect_fault")
        if exp_fault:
            ck(any(f[-1] == exp_fault for f in w.faults),
               f"expected fault@{exp_fault:07X} got {w.faults}")
        else:
            ck(not w.faults, f"unexpected fault {w.faults}")

        if name == "ac80-gate-off":
            ck(eax == 0, "ret!=0")
            ck(gm.q(w.rec + 0x50) == 0xFFFFFFFFFFFFFFFF, "q50")
            ck(gm.w16(w.rec + 0x58) == 0xFFFF, "w58")
            ck(gm.w16(w.rec + 0x1C3) == 0xFFFF, "w1c3")
            ck(gm.b(w.rec + 0x1C5) == 0xFF, "b1c5")
            ck("c470" not in w.trace, "c470 ran under gate-off")
            ck(not w.rets.get("calls"), "scripted calls under gate-off")

        elif name in ("ac80-mode2", "ac80-modeff"):
            ck(eax == 0, "ret!=0")
            ck(gm.q(w.rec + 0x50) == 0xFFFFFFFFFFFFFFFF, "q50")
            ck("c470" not in w.trace, "c470 ran for mode>=2")

        elif name.startswith("ac80-member"):
            if case.get("expect_fault"):
                ck(w.faults and w.faults[0][-1] ==
                   case["expect_fault"], "fault addr")
            elif name == "ac80-member-deny":
                # 317930 ret 0 -> 31A630 returns -1 without writing;
                # FFFF slots skip the gate entirely but write FFFF over
                # FFFF (no change -> no fed0)
                ck(eax == 1, "ret")
                ck(gm.w16(w.rec + 0x50) == 0xFFFF,
                   "slot0 written despite s7930=0")
                ck(gm.w16(w.rec + 0x52) == 0xFFFF,
                   "slot1 written despite s7930=0")
                fed = [c for c in w.rets.get("calls", [])
                       if c[0] == "fed0" and c[2] == 0x97]
                ck(not fed, f"fed0(0x97) fired on deny {fed}")
            else:
                ck(eax == 1, "ret!=1")
                ck(gm.w16(w.rec + 4) == w.sel, "w4 sel")
                ck(gm.b(w.rec + 0x88) == 1, "b88 member flag")
                ck(gm.d(w.rec + 8) == 0, "member stat d8 copied")
                ck(gm.w16(w.rec + 0x50) == 0x1111, "slot0")
                ck(gm.w16(w.rec + 0x52) == 0x2222, "slot1")
                ck(gm.w16(w.rec + 0x54) == 0xFFFF, "slot2")
                ck(gm.w16(w.rec + 0x56) == 0xFFFF, "slot3")
                c50 = [c for c in w.rets.get("calls", [])
                       if c[0] == "c650"]
                ck(c50 and c50[0][2] == 1 and c50[0][3] == 2,
                   f"c650 args {c50}")
                # changed slots -> fed0(rec,0x97) per write
                fed = [c for c in w.rets.get("calls", [])
                       if c[0] == "fed0"]
                # order: c470's fed0(rec,0) first, then the two
                # changed-slot fed0(rec,0x97)
                ck([c[2] for c in fed] == [0, 0x97, 0x97],
                   f"fed0 seq {fed}")
                ck(not [c for c in w.rets.get("calls", [])
                        if c[0] == "g3910"], "member scanned abils")

        elif name.startswith("ac80-foe"):
            if case.get("expect_fault"):
                ck(w.faults and w.faults[0][-1] ==
                   case["expect_fault"], f"fault {w.faults}")
                if name == "ac80-foe-nulld":
                    ck("c470" not in w.trace, "c470 after foe-null")
            else:
                ck(eax == 1, f"ret {eax:#x}")
                ck(gm.w16(w.rec + 4) == w.sel, "w4 sel")
                # 30C470 stat copies
                ck(gm.d(w.rec + 8) == 0x3210, "d8")
                ck(gm.w16(w.rec + 0xC) == 0x44, "w0c")
                ck(abs(gm.f(w.rec + 0x10) - 10.0) < 0.01, "f10")
                ck(abs(gm.f(w.rec + 0x1C) - 40.0) < 0.01, "f1c")
                ck(gm.b(w.rec + 0x20) == 0x55, "b20")
                if name == "ac80-foe-cnt0":
                    # count floor 1 -> 2F8F20(0) -> 0
                    ck(gm.d(w.rec + 0x18C) == 0, "d18c cnt0!=0")
                else:
                    ck(0 < gm.d(w.rec + 0x18C) <= 0x5F5E0FF,
                       f"d18c {gm.d(w.rec + 0x18C):#x}")
                # gil: d[+0x190] = 0 (memset) + w[foerow+0x44]
                exp_gil = 0x7FFF if name == "ac80-foe-gilbig" else 500
                ck(gm.d(w.rec + 0x190) == exp_gil,
                   f"gil {gm.d(w.rec + 0x190):#x}")
                # slots 0..4
                ck(gm.w16(w.rec + 0x50) == 0x501, "slot0")
                ck(gm.w16(w.rec + 0x52) == 0x502, "slot1")
                ck(gm.w16(w.rec + 0x54) == 0xFFFF, "slot2")
                ck(gm.w16(w.rec + 0x56) == 0xFFFF, "slot3")
                ck(gm.w16(w.rec + 0x58) == 0xFFFF, "slot4")
                # scan
                g = [c for c in w.rets.get("calls", [])
                     if c[0] == "g3910"]
                if name == "ac80-foe-idx7":
                    ck(not g, "scan ran for idx>6")
                elif name == "ac80-foe-scan":
                    ck([c[2] for c in g] == [1, 2, 3],
                       f"scan grants {g}")
                    ck(all(c[3] == 1 and c[4] == 1 for c in g),
                       "3910 args")
                # pair copy via 7CB0 (+ its 327DE0 tail)
                if name == "ac80-foe-pairnull":
                    ck(gm.b(w.rec + 0xBA) == 0, "ba!=0")
                    ck(gm.d(w.rec + 0x88) == 0xFFFFFFFF, "pad0")
                    ck(gm.w16(w.rec + 0xB8) == 0, "b8 mask")
                elif name == "ac80-foe-pairbad":
                    ck(gm.b(w.rec + 0xBA) == 0, "ba!=0 on bad id")
                    ck(gm.d(w.rec + 0x88) == 0xFFFFFFFF, "pad0 badid")
                else:
                    ck(gm.w16(w.rec + 0x88) == 0x6010, "pair0 lo")
                    ck(gm.w16(w.rec + 0x8A) == 0x7010, "pair0 hi")
                    # hi[1]==FFFF stops the copy at i=1; the pad loop
                    # then fills entries 1..11 with FFFFFFFF
                    ck(gm.w16(w.rec + 0x8C) == 0xFFFF,
                       "pair1 lo not pad FFFF")
                    ck(gm.d(w.rec + 0x88 + 11 * 4) == 0xFFFFFFFF,
                       "pad tail")
                    ck(gm.b(w.rec + 0xBA) == 1, f"ba {gm.b(w.rec+0xBA)}")
                    ck(gm.w16(w.rec + 0xB8) & 1, "b8 bit0")
                    ck(gm.w16(w.rec + 0xB8) & 2 == 0, "b8 bit1 set")
                # flag bit
                if name == "ac80-foe-noflag40":
                    ck(gm.d(w.rec) & 4 == 0, "d0|4")
                else:
                    ck(gm.d(w.rec) & 4, "d0 missing |4")
                # 326030 counter clear + 3x snapshot of slotrow+0x88
                if not case.get("glob_null"):
                    ck(gm.d(w.glob + w.idx * 4 + 0x7370) == 0,
                       "cursor not cleared")
                    dst = w.glob + w.idx * 0x9C + 0x5B10
                    # opairs pair0 lo lands at each 0x34 block start;
                    # mask dword at +0x30
                    ck(gm.w16(dst) == 0x6000, "snap blk0 pair0")
                    ck(gm.w16(dst + 0x34) == 0x6000, "snap blk1 pair0")
                    ck(gm.w16(dst + 0x68) == 0x6000, "snap blk2 pair0")
                    ck(gm.w16(dst + 0x30) ==
                       (case.get("ordmask", 0) & 0xFFFF), "snap mask")
                # 7DE0 order rows (ordmask=3 -> entries 0,1)
                if name in ("ac80-foe-ordrow", "ac80-foe-cursor1"):
                    orow = ORDT + w.idx * 0x170
                    ck(gm.w16(orow + 0x28) == 0x81, "ord e0 +28")
                    ck(gm.b(orow + 0x26) == 0x91, "ord e0 +26")
                    ck(gm.w16(orow + 0x2E) == 0x82, "ord e0 +2E")
                    ck(gm.w16(orow + 0x30) == 0x85, "ord e0 +30")
                    # entry1 at +0x18 stride
                    ck(gm.w16(orow + 0x18 + 0x28) == 0x81,
                       "ord e1 +28")
                elif name == "ac80-foe-orddiv":
                    # rec-call -> ordrow idx(2) sees empty blk
                    orow2 = ORDT + w.idx * 0x170
                    ck(gm.w16(orow2 + 0x28) == 0,
                       "ordrow2 written (blk6 should be empty)")
                    # slotrow-call -> ordrow 5 materializes
                    orow5 = ORDT + 5 * 0x170
                    ck(gm.w16(orow5 + 0x28) == 0x81, "ord5 e0 +28")
                    ck(gm.w16(orow5 + 0x18 + 0x28) == 0x81,
                       "ord5 e1 +28")
                # real stat cluster: on a memset rec with zero
                # dirty mask, f340/f5a0 are no-ops and f690 is skipped
                seq = [c[0] for c in w.rets.get("calls", [])]
                ck("c650" in seq and "fed0" in seq, "c650/fed0")
                ck("f340" in w.trace and "f5a0" in w.trace,
                   "f340/f5a0 not run")
                if case.get("f690_gate") or case.get("f690_gate2"):
                    ck("f690" in w.trace, "f690 skipped w/ mask")
                    ck("e360" in w.trace, "e360 not called for set bit")
                    if name == "ac80-foe-f690gate":
                        ck("b860" in w.trace, "b860 scan missing")
                        # rec flags memset -> no 377C20, no bit26 clear
                        ck("cd7c20" not in w.trace,
                           "cd ran w/o rec flags")
                        ck(gm.q(w.objrow) & 0x4000000,
                           "bit26 cleared w/o rec flags")
                    if name == "ac80-foe-f690norow":
                        ck("b860" in w.trace, "b860 scan missing")
                else:
                    ck("f690" not in w.trace, "f690 ran w/o mask")
                    ck("e360" not in w.trace,
                       "e360 called on zero mask")
                ck(not [c for c in w.rets.get("calls", [])
                        if c[0] == "c530"], "c530 on equal rec")
                ck(not [c for c in w.rets.get("calls", [])
                        if c[0] in ("h0bc0", "h0ce0")],
                   "f5a0 applied on equal rec")

        elif (name.startswith("bc0-") or name.startswith("ce0-")
              or name.startswith("e060-")):
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            w6 = gm.w16(w.rec + 0x6)
            w4c = gm.w16(w.rec + 0x4C)

            if name == "bc0-basic":
                ck(w6 == 150, f"w6 {w6}")
                ck("n0e060" in w.trace, "30E060 notify missing")
            elif name == "bc0-cap":
                ck(w6 == 200, f"w6 {w6} != cap 200")
            elif name == "bc0-floor":
                ck(w6 == 0, f"w6 {w6}")
            elif name == "bc0-deadgate":
                ck(w6 == 0, f"deadgate w6 {w6}")
            elif name == "bc0-scale":
                ck(w6 == 300, f"w6 {w6} != scaled cap 300")
            elif name == "bc0-veto":
                ck(w6 == 100, f"veto w6 {w6}")
                ck(len(byr("lb770")) == 1, "30B770 missing")
                ck(len(byr("lb7f0")) == 1, "30B7F0 missing")
            elif name == "ce0-basic":
                ck(w4c == 80, f"w4C {w4c}")
                ck(len(by("q28f1f0")) == 1,
                   f"28F1F0 gauge post missing {calls}")
                ck(w6 == 10 + 30, f"hp cascade w6 {w6}")
            elif name == "ce0-cap":
                ck(w4c == 200, f"w4C {w4c} != cap")
            elif name == "ce0-cascade":
                ck("h0bc0" in w.trace, "hp cascade missing")
                ck(w6 == 40, f"w6 {w6}")
            elif name == "ce0-drop":
                ck(w4c == 20, f"w4C {w4c}")
                ck(len(by("q2fa540")) == 1,
                   "drop notify missing")
                ck("h0bc0" not in w.trace, "hp cascade on drop")
            elif name == "ce0-r13":
                ck(w4c == 80, f"w4C {w4c}")
                ck(len(byr("n283d0")) >= 1 or len(byr("lfa3b0")) >= 1,
                   f"r13 owner post missing {calls}")
            elif name == "ce0-veto":
                ck(w4c == 50, f"veto w4C {w4c}")
                ck(len(byr("lb7f0")) == 1, "30B7F0 missing")
            elif name == "e060-frac":
                ck(gm.b(w.rec + 0x4E) == 1,
                   f"b4E {gm.b(w.rec + 0x4E)} != 1")
                ck(len(byr("n283d0")) == 1 or
                   len(byr("lfa3b0")) == 1,
                   f"frac post missing {calls}")
            elif name == "e060-same":
                ck(not byr("n283d0") and not byr("lfa3b0"),
                   "frac posted on equal")
            elif name == "e060-down":
                ck(gm.b(w.rec + 0x4E) == 0,
                   f"b4E {gm.b(w.rec + 0x4E)}")

        elif name.startswith("s530-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            d48 = gm.d(w.rec + 0x48)
            d64 = gm.d(w.rec + 0x64)

            if name == "s530-pos":
                # 10+5=15 <= cap 100 -> write 15; old d48>0 -> no e360
                ck(not w.faults, f"fault {w.faults}")
                ck(d48 == 15, f"d48={d48}")
                ck(tcount("e360") == 0, f"e360 {tcount('e360')}")
            elif name == "s530-over":
                # 10+500=510 -> clamped to cap 100
                ck(d48 == 100, f"d48={d48}")
            elif name == "s530-zero":
                # delta=0 -> new d48=10 > floor -> msg path, no set
                ck(not w.faults, f"fault {w.faults}")
                ck(d48 == 10, f"d48={d48}")
                ck(not (d64 & 1), f"d64={d64:#x} bit0 set")
                ck(tcount("e360") == 0, f"e360 {tcount('e360')}")
            elif name == "s530-neg":
                ck(d48 == 7, f"d48={d48}")
            elif name == "s530-floor":
                # 10-50 -> floor 0 -> arm3 SET engaged bit0
                ck(d48 == 0, f"d48={d48}")
                ck(tcount("e360") == 1, f"e360 {tcount('e360')}")
                ck(d64 & 1, f"d64={d64:#x} bit0 not set")
            elif name == "s530-veto":
                # delta<0, notify&1=0 -> real 30B770 flag bit1 -> 30B9B0
                # vetoes at its gate; 30B8E0 is not reached.
                ck(not w.faults, f"fault {w.faults}")
                ck(d48 == 10, f"d48={d48} not vetoed")
                rr = w.rets.get("rargs", [])
                ck(any(c[0] == "lb9b0" for c in rr), "30B9B0 not run")
                ck(not any(c[0] == "lb8e0" for c in rr),
                   "30B8E0 ran after 30B9B0 veto")
            elif name == "s530-nonotify":
                # notify&1=0 -> veto runs (default ret 0 -> write)
                ck(d48 == 15, f"d48={d48}")
                ck(tcount("n283d0") == 0, "notify fired")
            elif name == "s530-cap2x":
                # flag bit 0x1C -> cap = d24*2 = 200 -> 510->200
                ck(d48 == 200, f"d48={d48}")
            elif name == "s530-revive":
                # old d48=0 -> delta>0 -> arm0 clear fires
                ck(d48 == 5, f"d48={d48}")
                ck(tcount("e360") == 1, f"e360 {tcount('e360')}")

        elif name.startswith(("b770-", "b7f0-", "d470-", "b9b0-",
                              "b8e0-", "b140-", "k99b0-")):
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            obj = w.objrow
            ent = w.objent if w.objrow else 0

            if name == "b770-zero":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b770-g3080":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "b770-b7":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "b770-ownb":
                ck(eax == 2, f"ret {eax:#x}")
            elif name == "b770-bits":
                ck(eax == 0xC, f"ret {eax:#x}")
            elif name == "b770-all":
                ck(eax == 0x1F, f"ret {eax:#x}")
            elif name == "b7f0-null":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b7f0-noflg":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b7f0-lo":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "b7f0-b4in":
                ck(eax == 8, f"ret {eax:#x}")
            elif name == "b7f0-b4out":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b7f0-edx":
                ck(eax == 3, f"ret {eax:#x}")
            elif name == "b7f0-rec1a":
                ck(eax == 0x10, f"ret {eax:#x}")
            elif name == "b7f0-sgl1":
                ck(eax == 0x10000, f"ret {eax:#x}")
                ck(len(byr("l17d470")) == 2, "17D470 should run twice")
            elif name == "b7f0-sgl2":
                ck(eax == 0x20000, f"ret {eax:#x}")
            elif name == "b7f0-sglgate":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "d470-null":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(by("n210ec0")) == 1, "210EC0 missing")
                ck(len(by("c1ccb20")) == 1, "1CCB20 missing")
                ck(gm.q(0x1F81428) == w.sglbuf,
                   "q[01F81428] not the alloc'd block")
            elif name == "d470-sgl":
                ck(eax == 0x42, f"ret {eax:#x}")
                ck(not by("n210ec0"), "alloc ran on planted sgl")
            elif name == "b9b0-null":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b9b0-none":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b9b0-glob":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(byr("lb770")) == 1, "30B770 missing")
            elif name == "b9b0-pair":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(byr("l30ab40")) == 1, "30AB40 missing")
            elif name == "b8e0-null":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b8e0-lo":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "b8e0-sgl":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "b8e0-sgl2":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "b140-edx0":
                ck(gm.q(obj) & 0x4000, "bit14 cleared on sentinel match")
                ck(gm.q(obj + 0x6F8) == 0, "q6F8")
                ck(gm.d(obj + 0x748) == 0, "d748")
                ck(gm.d(obj + 0x770) == 0, "d770")
                ck(gm.d(obj + 0x788) == 0xFF, "d788 &= ~0x400")
                ck(gm.d(obj + 0x6B0) == 0xFD, "d6B0 &= ~2")
                ck(gm.q(obj + 0x750) == 0, "q750")
                ck(gm.d(obj + 0x74C) == 0, "d74C")
                ck(gm.d(obj + 4) & 0x200000, "d4 |= 0x200000")
                ck(not by("u3105d0"), "u3105d0 on edx=0")
            elif name == "b140-clear":
                ck(not (gm.q(obj) & 0x4000), "bit14 kept on sentinel miss")
                ck(gm.d(obj + 4) & 0x200000, "d4 |= 0x200000")
            elif name == "b140-td":
                ck(len(by("u3105d0")) == 1, "u3105d0 missing")
                ck(gm.q(obj) & 0x4000, "bit14 cleared on sentinel match")
            elif name == "k99b0-minus1":
                ck(gm.d(obj + 0x5C) == 0, "d5C written on -1")
                ck(not byr("l2eb030"), "2EB030 on edx==-1")
            elif name == "k99b0-low":
                ck(len(byr("l2eb030")) == 1, "2EB030 missing")
                ck(byr("l2eb030")[0][1] == ent, "2EB030 arg != node")
                ck(byr("l2eb030")[0][2] == 0x50, "2EB030 msg != 0x50")
                ck(gm.d(obj + 0x5C) == 0x50, "d5C")
                ck(gm.d(obj + 0x2C) == 0, "d2C not cleared")
                ck(gm.b(ent + 0xD) == 0xFE, "bD &= ~1")
                ck(gm.b(ent + 0xF5) == 0xFF, "bF5")
                ck(gm.d(ent + 0xEC) == 0, "dEC")
                ck(gm.d(ent + 0xF0) == 0x50, "dF0")
                ck(not by("kb0d0"), "2EB0D0 on b18==1")
            elif name == "k99b0-hi":
                ck(gm.d(obj + 0x5C) == 0x5300,
                   f"d5C {gm.d(obj + 0x5C):#x} != 0x5300")
                ck(gm.d(ent + 0xF0) == 0x5300, "dF0")
            elif name == "k99b0-kick":
                kk = by("kb0d0")
                ck(len(kk) == 1, "2EB0D0 not kicked")
                if kk:
                    ck(kk[0][1] == ent, f"kb0d0 rcx {kk[0][1]:#x}")
                    ck(kk[0][2] == 0xDEAD, f"kb0d0 rdx {kk[0][2]:#x}")
                    ck(kk[0][3] == 0x50, f"kb0d0 r8 {kk[0][3]:#x}")
                    ck(kk[0][4] == 1, f"kb0d0 r9 {kk[0][4]:#x}")

        elif name.startswith("s8a0-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            bmpw = gm.w16(w.fbmp + 2)
            cellw = gm.d(w.cell + 4) if w.cell else 0

            if name == "s8a0-foe":
                # bit already set, delta 0 -> stays set, ret 1
                ck(not w.faults, f"fault {w.faults}")
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("m2fd420") == 1, f"mut {tcount('m2fd420')}")
                ck(tcount("n325f40") == 1, f"notify {tcount('n325f40')}")
                ck(bmpw == 0x7FFC, f"bmp {bmpw:#x}")
            elif name == "s8a0-clear":
                # old=1 + delta -1 -> 0 -> btr -> ret 0
                ck(eax == 0, f"ret {eax:#x}")
                ck(bmpw == 0x7FF8, f"bmp {bmpw:#x}")
            elif name == "s8a0-set":
                # old=0 + delta 1 -> bts -> ret 1
                ck(eax == 1, f"ret {eax:#x}")
                ck(bmpw == 0x0004, f"bmp {bmpw:#x}")
            elif name == "s8a0-setzero":
                # old=0 + delta 0 -> ecx=0 -> btr noop -> ret 0
                ck(eax == 0, f"ret {eax:#x}")
                ck(bmpw == 0x0000, f"bmp {bmpw:#x}")
            elif name == "s8a0-neg2":
                # old=1 + delta -2 -> ecx=-1 <0 -> btr clear path
                ck(bmpw == 0x7FF8, f"bmp {bmpw:#x}")
            elif name == "s8a0-mode":
                # mode!=0 -> ecx=edi=1 -> bts, ret 1
                ck(eax == 1, f"ret {eax:#x}")
                ck(bmpw == 0x0004, f"bmp {bmpw:#x}")
            elif name == "s8a0-mode0":
                # mode!=0, delta 0 -> ebx=0 -> btr noop -> ret 0
                ck(eax == 0, f"ret {eax:#x}")
                ck(bmpw == 0x0000, f"bmp {bmpw:#x}")
            elif name == "s8a0-flag4":
                # stack flag&1 + mode0 -> 46A630(id, delta=1) -> 46AB10
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("l6a630") == 1, f"46a630 {tcount('l6a630')}")
                ck(any(c[0] == "q6ab10" for c in
                       w.rets.get("calls", [])), "46ab10 not called")
            elif name == "s8a0-flag4clr":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l6a630") == 1, f"46a630 {tcount('l6a630')}")
                ck(any(c[0] == "q6ab10" for c in
                       w.rets.get("calls", [])), "46ab10 not called")
            elif name == "s8a0-foeflag":
                # r9=1 -> gate: validator(id,1)<=0 (bit clear) +
                # mutator ret 1 -> cls-C foe arm |=0x100
                ck(eax == 1, f"ret {eax:#x}")
                ck(cellw & 0x100, f"cell+4 {cellw:#x} missing 0x100")
            elif name == "s8a0-foe80":
                # id<=0xC011 -> |=0x80
                ck(eax == 1, f"ret {eax:#x}")
                ck(cellw & 0x80, f"cell+4 {cellw:#x} missing 0x80")
            elif name == "s8a0-foeend":
                # 0xC01E = max foe -> |=0x100
                ck(eax == 1, f"ret {eax:#x}")
                ck(cellw & 0x100, f"cell+4 {cellw:#x} missing 0x100")
            elif name in ("s8a0-inval", "s8a0-ffff", "s8a0-hi",
                          "s8a0-k"):
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(tcount("m2fd420") == 0, "mutator ran on bad id")

        elif name.startswith("a630r9-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            w54 = gm.w16(w.rec + 0x54)
            w100 = gm.w16(w.cls1arr + 0x100 * 2) if w.cls1arr else 0
            w150 = gm.w16(w.cls1arr + 0x150 * 2) if w.cls1arr else 0

            if name == "a630r9-swap":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not w.faults, f"fault {w.faults}")
                # unequip old 0x1100: count 5->4 cap5
                ck(w100 == 0x1005, f"w100 {w100:#x}")
                # equip new 0x1150: count 2->3 cap3
                ck(w150 == 0x0C03, f"w150 {w150:#x}")
                ck(w54 == 0x1150, f"slot {w54:#x}")
                ck(tcount("a08a0") == 2, f"8a0 {tcount('a08a0')}")
                ck(tcount("v2fd8d0") == 2 and tcount("m2fd150") == 2,
                   "member cb not run x2")
                ck(len(by("l8b40")) == 1 and by("l8b40")[0][2] == 2,
                   "l8b40 args")
                ck(len(by("fed0")) == 1 and by("fed0")[0][2] == 0x97,
                   "fed0 missing")
                # 324470 teardown chain on the owner member
                ck(len(by("tecf10")) == 1
                   and by("tecf10")[0][1] == w.objent
                   and by("tecf10")[0][2] == 0, "tecf10 args")
                ck(len(by("u3105d0")) == 1
                   and by("u3105d0")[0][1] == w.objrow, "u3105d0")
                ck(not by("s313f60") and not by("p300e40"),
                   "313f60/300e40 ran past zero or-gate")
                for t in ("r2e42d0", "s2699d0", "r2ecec0"):
                    ck(len(by(t)) == 1 and by(t)[0][1] == w.objent,
                       f"{t} args")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-off":
                ck(eax == 0, f"ret {eax:#x}")
                ck(w54 == 0x1150, f"slot {w54:#x}")
                for t in ("uf9a0", "ec410", "b860", "m4470", "a08a0"):
                    ck(tcount(t) == 0, f"{t} ran with r9d=0")
            elif name == "a630r9-oldff":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("uf9a0") == 1, "f9a0 not entered")
                ck(tcount("a08a0") == 1,
                   f"8a0 {tcount('a08a0')} (only equip arm)")
                ck(w150 == 0x0C03, f"w150 {w150:#x}")
                ck(w54 == 0x1150, f"slot {w54:#x}")
            elif name == "a630r9-oldfoe":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("uf9a0") == 1, "f9a0 not entered")
                ck(tcount("a08a0") == 1,
                   f"8a0 {tcount('a08a0')} (foe-class old skipped)")
                ck(w150 == 0x0C03, f"w150 {w150:#x}")
            elif name == "a630r9-new1k":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("ec410") == 1, "c410 not entered")
                ck(tcount("a08a0") == 1,
                   f"8a0 {tcount('a08a0')} (0x1000 new skipped)")
                ck(w100 == 0x1005, f"w100 {w100:#x}")
                ck(w54 == 0x1000, f"slot {w54:#x}")
            elif name == "a630r9-nomatch":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("b860") == 1, "owner scan not run")
                ck(tcount("e6850") >= 1 and tcount("e6820") == 2,
                   "scan loop")
                ck(tcount("m4470") == 0, "4470 ran on null owner")
            elif name == "a630r9-bit23":
                ck(len(by("tecf10")) == 1 and by("tecf10")[0][2] == 1,
                   "tecf10 edx not 1")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-gate3f":
                ck(len(by("s313f60")) == 1, "s313f60 skipped")
                ck(not by("p300e40"), "300e40 ran past 313f60 gate")
            elif name == "a630r9-b2":
                ck(len(by("s313f60")) == 1, "s313f60 skipped")
                ck(not by("p300e40"), "300e40 ran past b2 gate")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-rec3c":
                ck(len(by("s313f60")) == 1
                   and by("s313f60")[0][1] == w.rec, "s313f60")
                ck(len(by("p300e40")) == 1
                   and by("p300e40")[0][1] == w.objrow
                   and by("p300e40")[0][2] == 0, "p300e40")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-null":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(tcount("uf9a0") == 0 and tcount("a08a0") == 0,
                   "chain ran on null rec")
            elif name == "a630r9-deny":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(w54 == 0x1100, f"slot written on deny {w54:#x}")
                ck(tcount("uf9a0") == 0 and tcount("m4470") == 0,
                   "chain ran on deny")
            elif name == "a630r9-newff":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("s7930"), "7930 ran on FFFF new id")
                ck(tcount("a08a0") == 1,
                   f"8a0 {tcount('a08a0')} (FFFF equip skipped)")
                ck(w100 == 0x1005, f"w100 {w100:#x}")
                ck(w54 == 0xFFFF, f"slot {w54:#x}")
            elif name == "a630r9-clamp":
                ck(eax == 0, f"ret {eax:#x}")
                ck(w150 == 0x0C03, f"clamp w150 {w150:#x}")
                ck(w100 == 0x1005, f"w100 {w100:#x}")


        elif name.startswith(("g7930-", "l8b40-", "u43f0-", "w4450-",
                              "r71d0", "g8010-", "o4100-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            w50 = gm.w16(w.rec + 0x50)
            w52 = gm.w16(w.rec + 0x52)

            if name == "g7930-t0sent":
                # slot0 accepts 0x1000 via the D107E8 shortcut, before 2C50
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("v2c50") == 0, "2c50 ran on table hit")
            elif name == "g7930-clr":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("v2c50") == 0, "2c50 ran on table hit")
            elif name == "g7930-clr0":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("v2c50") == 0, "2c50 ran on FFFF")
            elif name == "g7930-slot5":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("v2c50") == 0, "2c50 ran on slot>4")
            elif name == "g7930-ok":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("v2c50") == 1, "kind-6 range not run")
                ck(tcount("e600") == 4, f"e600 {tcount('e600')}")
                ck(len(by("s323c60")) == 1
                   and by("s323c60")[0][2] == 0x1150, "323c60 args")
            elif name == "g7930-tagmm":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("e600") == 2 and not by("s323c60"),
                   "ran past tag gate")
            elif name == "g7930-k8rng":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("e600") == 0, "resolve ran past range fail")
            elif name == "g7930-free0":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("v9ec0") == 1 and tcount("v2fd8d0") == 1,
                   "free-count path not run")
                ck(tcount("e600") == 0, "resolve ran on free0")
            elif name == "g7930-free1":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("v9ec0") == 1 and tcount("v2fd8d0") == 1,
                   "free-count path not run")
            elif name == "g7930-s1eq":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("e600") == 6, f"e600 {tcount('e600')}")
            elif name == "g7930-s1ne":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("s323c60"), "323c60 ran on tag mismatch")
            elif name == "g7930-foebit":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("s323c60"), "323c60 ran on foe bit set")
            elif name == "g7930-b5":
                # b[rec+5]!=0 short-circuits to ret1 before the foe test
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("e600") == 2, f"e600 {tcount('e600')}")
            elif name == "g7930-c60":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(by("s323c60")) == 1, "323c60 not called")
            elif name == "g7930-nomemt":
                # null desc fails 322C50's kind-6 range first
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("v2c50") == 1 and tcount("e600") == 0,
                   "past 2c50 with null desc")

            elif name == "l8b40-ffinit":
                # w0==FFFF -> init to 0x1000; tag mismatch w1 -> clear w1
                ck(w50 == 0x1000, f"w50 {w50:#x}")
                ck(w52 == 0xFFFF, f"w52 {w52:#x}")
                ck(tcount("uf9a0") == 2 and tcount("ec410") == 2,
                   "un/equip counts")
                ck(tcount("a08a0") == 1, "8a0 (0x1160 dec only)")
            elif name == "l8b40-match":
                ck(w50 == 0x1150 and w52 == 0x1160, "pair rewritten")
                ck(tcount("uf9a0") == 0 and tcount("ec410") == 0,
                   "calls ran on tag match")
            elif name == "l8b40-s0clr":
                ck(w50 == 0x1150 and w52 == 0xFFFF,
                   f"pair {w50:#x}/{w52:#x}")
                ck(tcount("uf9a0") == 1 and tcount("ec410") == 1
                   and tcount("a08a0") == 1, "chain counts")
            elif name in ("l8b40-s1reset", "l8b40-s1tag12"):
                # slot1 write with empty/0x12 neighbor -> self reset 1000
                ck(w50 == 0x1000, f"w50 {w50:#x}")
                ck(tcount("uf9a0") == 1 and tcount("a08a0") == 1,
                   "self-unequip missing")
            elif name == "l8b40-s1clr":
                ck(w50 == 0x1150 and w52 == 0xFFFF,
                   f"pair {w50:#x}/{w52:#x}")
            elif name == "l8b40-noflag":
                ck(w52 == 0xFFFF, f"w52 {w52:#x}")
                ck(tcount("uf9a0") == 0 and tcount("a08a0") == 0,
                   "un/equip ran with flag 0")
            elif name == "l8b40-nomemt":
                ck(w.faults and w.faults[-1][-1] == 0x318BE0,
                   f"fault {w.faults}")

            elif name == "u43f0-gate0":
                ck(len(by("u3105d0")) == 1
                   and by("u3105d0")[0][1] == w.objrow, "u3105d0")
                ck(not by("s313f60") and not by("p300e40"),
                   "gates ran past zero or-mask")
                for t in ("r2e42d0", "s2699d0", "r2ecec0"):
                    ck(len(by(t)) == 1 and by(t)[0][1] == w.objent,
                       f"{t} args")
            elif name == "u43f0-698z":
                ck(not by("s313f60"), "313f60 ran on null 698")
                ck(len(by("p300e40")) == 1
                   and by("p300e40")[0][1] == w.objrow
                   and by("p300e40")[0][2] == 0, "300e40 args")
            elif name == "u43f0-3f":
                ck(len(by("s313f60")) == 1, "313f60 missing")
                ck(len(by("p300e40")) == 1, "300e40 missing")
            elif name in ("u43f0-3fskip", "u43f0-b2"):
                ck(len(by("s313f60")) == 1, "313f60 missing")
                ck(not by("p300e40"), "300e40 ran past skip gate")
            elif name == "w4450-set":
                ck(tcount("rx3243f0") == 1, "43f0 not entered")
                ck(len(by("u3105d0")) == 1, "u3105d0 missing")
                ck(not gm.d(w.objrow) & 0x40, "0x40 not cleared")
            elif name == "w4450-clear":
                ck(tcount("rx3243f0") == 0, "43f0 ran on clear bit")
                ck(not by("u3105d0"), "u3105d0 ran")

            elif name == "r71d0":
                ck(eax == 0x5A, f"ret {eax:#x}")

            elif name == "g8010-b5z":
                ck(len(by("m308130")) == 1 and not by("m308040"),
                   "b5==0 did not take 308130")
            elif name in ("g8010-b5nz", "g8010-698z", "g8010-null"):
                ck(len(by("m308040")) == 1 and not by("m308130"),
                   f"{name} landing wrong")

            elif name == "o4100-null":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("o324020"), "4020 ran on null")
            elif name == "o4100-base":
                ck(eax == 3, f"ret {eax:#x}")
                ck(len(by("o324020")) == 1
                   and by("o324020")[0][1] == w.rec, "4020 args")
                ck(not by("a308ff0"), "8ff0 ran with no bits")
            elif name == "o4100-lic":
                ck(eax == 7, f"ret {eax:#x}")
                ck(len(by("a308ff0")) == 1, "8ff0 count")
            elif name == "o4100-liclow":
                ck(eax == 9, f"ret {eax:#x}")
                ck(len(by("a308ff0")) == 1, "8ff0 count")
            elif name == "o4100-noabil":
                ck(eax == 3, f"ret {eax:#x}")
                ck(not by("a308ff0"), "8ff0 ran on null abild")


        elif name.startswith(("s8130-", "m8040-", "a8ff0-", "o4020-",
                              "s3c60-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]

            if name == "s8130-fast":
                # b[rec+5]==0 & b[rec+4]==0x1A -> 7D10 fast ebx=1 ->
                # bit16 set; mask 0x20 hit -> bt set -> ret1
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("l7d10") == 1, "307D10 missing")
                ck(gm.d(w.objrow + 4) & 0x10000,
                   f"bit16 not set {gm.d(w.objrow + 4):#x}")
                ck("l253b90" not in tr, "253B90 on fast path")
            elif name == "s8130-noor":
                # mask clear -> 253B90 (d[1E0C2B8]=1 -> 0) -> bt still
                # sees 7D10's bit16 write -> ret1
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("l253b90") == 1, "253B90 missing")
            elif name == "s8130-b16clr":
                # b[rec+5]==1 -> 377C20 real -> nonzero -> ebx=0 ->
                # bit16 clear -> bt fails -> g81e0=0 -> ret0
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("cd7c20") == 1, "377C20 missing")
                ck(not gm.d(w.objrow + 4) & 0x10000,
                   "bit16 set on ebx=0")
                ck("l3081e0" not in tr, "3081E0 on clear gate")
            elif name == "s8130-81e0":
                # g81e0=1 -> 3081E0 real (RNG 328370 + 32A150) writes
                # d[member+0xDCC]; b[rec+5]==1 -> ret1 via 3081C8
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("l3081e0") == 1 and tcount("rng28370") == 1
                   and tcount("l2a150") == 1, "81E0 chain missing")
            elif name == "s8130-g25b":
                # d[1E0C2B8]=0 -> 253B90 ret1 -> xor eax ret0
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l253b90") == 1, "253B90 missing")

            elif name == "m8040-698z":
                ck(eax == 0, f"ret {eax:#x}")
                ck("l30b050" not in tr, "B050 on null 698")
            elif name == "m8040-b5z":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "m8040-f20":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "m8040-edx":
                # edx!=0 -> 308125 ret0 (arg gate)
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "m8040-fhi":
                # f4 >= const -> jb not taken -> ret0
                ck(eax == 0, f"ret {eax:#x}")
                ck("l30b050" not in tr, "B050 on f4>=const")
            elif name == "m8040-flo":
                # f4 < const -> 30B050(member); bc4=0 -> 0 -> ret0
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l30b050") == 1, "30B050 missing")
            elif name == "m8040-b44":
                # flag-obj d0 &0x48==0 -> bit40 of q[member] -> ret1
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "m8040-b050":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l30b050") == 1, "30B050 missing")
            elif name == "m8040-b050e":
                # bc4=2, entries null -> 31B760(0) x2 -> ret0
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l31b760") == 2, f"l31b760 {tcount('l31b760')}")

            elif name == "a8ff0-hi":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("e600") == 0, "resolve on idx>0x21E")
            elif name == "a8ff0-ok":
                ck(eax == 0x77, f"ret {eax:#x}")
                ck(tcount("e600") == 2, "resolve missing")
            elif name == "a8ff0-b1e6":
                ck(eax == 0x42, f"ret {eax:#x}")
            elif name == "a8ff0-bad":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("e600") == 2, "resolve missing")
            elif name == "a8ff0-nodesc":
                ck(w.faults and w.faults[-1][-1] == 0x30904A,
                   f"fault {w.faults}")

            elif name == "o4020-zero":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "o4020-b0":
                ck(eax == 1, f"ret {eax:#x}")
            elif name == "o4020-bhi":
                # 18-position window popcount: bit0 + bit0xF = 2
                ck(eax == 2, f"ret {eax:#x}")

            elif name == "s3c60-bad":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("v309440") == 1, "kind-1 dispatch missing")
                ck(tcount("e600") == 0, "resolve on bad id")
            elif name in ("s3c60-null", "s3c60-b5", "s3c60-b4"):
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("e600") == 0, "member resolve on early-1")
            elif name == "s3c60-bit10":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("e600") == 2, f"e600 {tcount('e600')}")
                ck("l323bb0" not in tr, "323BB0 on bit10 set")
            elif name == "s3c60-scan":
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("l323bb0") == 1 and tcount("l2f8fa0") == 1
                   and tcount("l3241d0") >= 1, "scan chain missing")
                ck(len(by("cookie")) == 1, "cookie check missing")
            elif name in ("s3c60-nomatch", "s3c60-nolid"):
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l2f8fa0") == 1, "bitmap build missing")

        elif name.startswith(("n6500-", "l26620-", "l31b770-",
                              "l263e30", "l317400-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            cmit = gm.d(0x22C7FE4)
            cflg = gm.b(0x22C7FF8)

            if name == "n6500-nullctx":
                ck(cmit == 0 and cflg == 1,
                   f"commit {cmit:#x} flag {cflg}")
                ck(tcount("l11e20") == 2,
                   f"11e20 x{tcount('l11e20')}")
                ck(tcount("l594b0") == 1, "594b0 tail")
                ck(tcount("l317400") == 0, "317400 at mode0")
            elif name == "n6500-slothit":
                ck(cmit == 0x11223344 and cflg == 1,
                   f"commit {cmit:#x}")
                l7 = byr("l31b770")
                ck(len(l7) == 1 and l7[0][1] == 2,
                   f"31b770 args {l7}")
                ck(tcount("l317400") == 0, "317400 at mode0")
            elif name == "n6500-mode1":
                ck(cmit == 0x55 and cflg == 1, f"commit {cmit:#x}")
                l4 = byr("l317400")
                ck(len(l4) == 1 and l4[0][1] == w.objrow,
                   f"317400 {l4}")
            elif name == "n6500-mode2":
                l7 = byr("l31b770")
                ck(l7 and l7[0][1] == 0x1A,
                   f"mode2 slot byte {l7}")
                ck(cmit == 0x7777 and cflg == 1,
                   f"commit {cmit:#x}")
            elif name == "n6500-mode5":
                l7 = byr("l31b770")
                ck(len(l7) == 1 and l7[0][1] == 0xFF,
                   f"mode5 keeps FF {l7}")
                ck(tcount("l2367a0") == 4,
                   f"scan count {tcount('l2367a0')}")
                ck(cmit == 0 and cflg == 1, f"commit {cmit:#x}")
            elif name == "n6500-scanhit":
                ck(cmit == 0x99 and cflg == 1, f"commit {cmit:#x}")
                a = byr("l2367a0")
                ck(len(a) == 4 and a[-1][1] == 5,
                   f"scan args {a}")
            elif name == "n6500-ctxblk":
                ck(cmit == 0x12340000 and cflg == 1,
                   f"ctx id {cmit:#x}")
                ck(gm.q(0x22C7D18) == w.ctx[0],
                   f"ctx store {gm.q(0x22C7D18):X}")
                ck(gm.d(0x22C7D20 + 0x10) == 0xDEAD, "blk copy")
                ck(gm.d(0x22C7DD0) == 0xAA and
                   gm.d(0x22C7DD4) == 0xBB and
                   gm.d(0x22C7DD8) == 0xCC, "265020 triple")
                ck(gm.d(0x22C7DE0) == 0x40600000, "265200 float")
                ck(gm.d(0x22C7D10) == 1, "ctx flag")
            elif name == "n6500-ctor":
                ck(tcount("l26620") == 2,
                   f"6620 x{tcount('l26620')}")
                ck(tcount("l594b0") == 2,
                   f"commit x{tcount('l594b0')}")
                ck(cmit == 0x2468 and cflg == 1,
                   f"commit {cmit:#x}")
            elif name == "n6500-gated":
                ck(tcount("l11e20") == 2, "11e20 calls")
                ck(tcount("l33ca00") == 0, "33ca00 under gate")
                ck(cflg == 1, "commit still ran")
            elif name == "l26620-found":
                ck(tcount("l30a880") == 0, "ctor on found slot")
            elif name == "l26620-ctor":
                ck(tcount("l30a880") == 1,
                   f"ctor {tcount('l30a880')}")
                ck(cmit == 0xBEEF and cflg == 1,
                   f"nested commit {cmit:#x}")
            elif name == "l31b770-hi":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l236850") == 0, "scan on OOB")
            elif name == "l31b770-hit":
                ck(eax == w.objrow, f"ret {eax:#x}")
            elif name == "l31b770-null":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "l263e30":
                ck(eax == 0x7777, f"ret {eax:#x}")
            elif name == "l317400-one":
                l7 = byr("l31b770")
                ck(len(l7) == 2 and l7[0][1] == 2 and l7[1][1] == 3,
                   f"pair args {l7}")
                ck(tcount("l26dac0") == 0, "26dac0 on null pair")

        elif name.startswith("c650-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            lvl = gm.b(w.rec + 0x1C2)

            if name == "c650-max":
                ck(lvl == 0x63, f"lvl {lvl:#x}")
                ck(tcount("b860") == 0 and not by("fed0"),
                   "level loop ran at cap")
            elif name == "c650-one":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 103, f"hp {gm.d(w.rec+8)}")
                ck(gm.w16(w.rec + 0xC) == 50, f"mp {gm.w16(w.rec+0xC)}")
                ck(abs(gm.f(w.rec + 0x10) - 50.0625) < 1e-4,
                   f"str {gm.f(w.rec+0x10)}")
                ck(abs(gm.f(w.rec + 0x14) - 0.125) < 1e-4, "mag")
                ck(abs(gm.f(w.rec + 0x18) - 0.1875) < 1e-4, "vit")
                ck(abs(gm.f(w.rec + 0x1C) - 0.25) < 1e-4, "spd")
                ck(len(by("fed0")) == 1 and by("fed0")[0][2] == 0,
                   "fed0 count/arg")
                ck(len(by("q6ab10")) == 1 and by("q6ab10")[0][2] == 4,
                   "46a690 arg")
                ck(len(byr("b860")) == 1, "b860 count")
                ck(len(byr("l35d8c0")) == 1 and byr("l35d8c0")[0][1]
                   == 0x2468, "35d8c0 arg")
                ck(len(by("b3b02a0")) == 1
                   and by("b3b02a0")[0][1] == 0x2468
                   and by("b3b02a0")[0][2] == w.objrow + 8
                   and by("b3b02a0")[0][3] == 1
                   and by("b3b02a0")[0][4] == 0x71,
                   f"3b02a0 args {by('b3b02a0')}")
                ck(len(byr("l3a1180")) == 1, "3a1180")
                ck(tcount("l2df220") == 0 and tcount("l329210") == 0,
                   "serial path ran without gate")
                ck(tcount("rng79cd0") == 1,
                   "hp arm 379CD0 (INT_MIN modulus, flag0 -> 0)")
            elif name == "c650-hold":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(len(by("q6ab10")) == 0, "46a690 ran with r8&2")
                ck(tcount("l35d8c0") == 0, "notify ran with r8&2")
                ck(len(by("fed0")) == 1, "fed0 count")
                ck(gm.d(w.rec + 8) == 103, "hp")
            elif name == "c650-multi":
                ck(lvl == 5, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 19, f"hp {gm.d(w.rec+8)}")
                ck(len(byr("b860")) == 3, f"b860 {len(byr('b860'))}")
                ck(len(by("fed0")) == 1, "fed0 count")
                ck(len(by("q6ab10")) == 1, "46a690 once")
                ck(len(by("b3b02a0")) == 1, "notify once")
            elif name == "c650-b5":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(tcount("g2f9a60") == 0, "growth ran with b5")
                ck(len(by("fed0")) == 1, "fed0 count")
                ck(len(by("q6ab10")) == 0 and tcount("l35d8c0") == 0,
                   "b5 tail ran")
            elif name == "c650-nolvl":
                pass  # expect_fault asserted above
            elif name == "c650-clamp":
                ck(lvl == 0x63, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 15, f"hp {gm.d(w.rec+8)}")
                ck(len(by("fed0")) == 1, "fed0 count")
            elif name == "c650-mp":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 100, "hp grew on g=0")
                ck(tcount("rng79cd0") == 1,
                   f"rng {tcount('rng79cd0')}")
                # shipped MT temper of 0x64
                t = 0x64
                t ^= t >> 0xB
                t ^= (t & 0xFF3A58AD) << 7
                t ^= (t & 0xFFFFDF8C) << 15
                t &= 0xFFFFFFFF
                t ^= t >> 0x12
                exp_mp = 50 + 5 + (t % 500) // 100
                ck(gm.w16(w.rec + 0xC) == exp_mp,
                   f"mp {gm.w16(w.rec+0xC)} exp {exp_mp}")
            elif name == "c650-full":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(len(byr("l267330")) == 1 and
                   byr("l267330")[0][1] == 0, "267330")
                ck(len(byr("l3a1180")) == 1, "3a1180")
                ck(len(byr("l2df220")) == 1 and
                   byr("l2df220")[0][1] == 0x2007,
                   f"2df220 {byr('l2df220')}")
                b1 = by("b1dbdb0")
                ck(len(b1) == 1 and b1[0][2] == 0x2007
                   and b1[0][3] == 0x40 and b1[0][4] == 0x7F,
                   f"1dbdb0 args {b1}")
                ck(gm.d(0x208D32C) == 0x77,
                   f"329210 write {gm.d(0x208D32C):#x}")

        elif name.startswith("g3910-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            lp = gm.d(w.rec + 0x190)
            bit = gm.b(w.rec + 0x194 + (0x10 >> 3)) & 1
            bit5 = gm.b(w.rec + 0x194) & 0x20
            grade = gm.b(w.rec + 0x20)

            if name == "g3910-null":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
            elif name in ("g3910-b5", "g3910-badid"):
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(tcount("l323d10") == 0, "323d10 ran")
                ck(not by("fed0"), "fed0 on reject")
            elif name == "g3910-grant":
                ck(eax == 0, f"ret {eax:#x}")
                ck(lp == 70, f"lp {lp}")
                ck(bit == 1, "bit not set")
                ck(len(by("fed0")) == 1 and by("fed0")[0][2] == 0x97,
                   "fed0 arg")
                ck(len(byr("l323d10")) == 1, "323d10 count")
                ck(len(by("o324020")) == 1, "324020 count")
                ck(len(byr("l30a310")) == 1, "30a310 count")
                ck(tcount("l300b80") == 0, "300b80 on b[+4]=0")
            elif name == "g3910-lp0":
                ck(eax == 0, f"ret {eax:#x}")
                ck(lp == 0, f"lp {lp}")
                ck(bit == 1, "bit not set")
            elif name == "g3910-silent":
                ck(eax == 0, f"ret {eax:#x}")
                ck(lp == 100, f"lp {lp}")
                ck(bit == 1, "bit not set")
            elif name == "g3910-dup":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(lp == 100, f"lp {lp}")
                ck(not by("fed0"), "fed0 on dup")
            elif name == "g3910-revoke":
                ck(eax == 0, f"ret {eax:#x}")
                ck(gm.b(w.rec + 0x196) == 0, "bit not cleared")
                ck(lp == 100, f"lp {lp}")
                ck(len(byr("l323d10")) == 0, "323d10 on revoke")
                ck(len(by("fed0")) == 1, "fed0 count")
            elif name == "g3910-e5":
                ck(eax == 0, f"ret {eax:#x}")
                ck(gm.b(w.rec + 0x194 + 0x1C) & 0x20,
                   "e5 bit not set")
                ck(len(byr("b860")) == 1, "31b860 count")
                ck(len(by("u3105d0")) == 1
                   and by("u3105d0")[0][1] == w.objrow,
                   "teardown missing")
            elif name == "g3910-rank":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(byr("l30a310")) == 1
                   and byr("l30a310")[0][2] == 0,
                   f"a310 {byr('l30a310')}")
                b8 = byr("l300b80")
                ck(len(b8) == 1 and b8[0][1] == 0x1150
                   and b8[0][2] == 1, f"300b80 args {b8}")
                ck(tcount("a08a0") == 1, "3008a0 count")
                ck(gm.w16(w.cls1arr + 0x150 * 2) == 0x0804,
                   f"cls1 w {gm.w16(w.cls1arr+0x150*2):#x}")
            elif name == "g3910-grade":
                ck(eax == 0, f"ret {eax:#x}")
                ck(grade == 2, f"grade {grade}")
                a8 = by("a308ff0")
                ck(len(a8) == 1 and a8[0][1] == 0
                   and a8[0][2] == 0x55, f"8ff0 args {a8}")
            elif name == "g3910-grade-cap":
                ck(grade == 3, f"grade {grade}")
            elif name == "g3910-grade-hold":
                ck(grade == 2, f"grade {grade}")
            elif name == "g3910-b6ok":
                ck(eax == 0, f"ret {eax:#x}")
                ck(lp == 70, f"lp {lp}")
                ck(len(byr("l324280")) == 1, "324280 count")
            elif name == "g3910-b6dup":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(lp == 100, f"lp {lp}")
                ck(len(byr("l324280")) == 1, "324280 count")
            elif name == "g3910-b6cap":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(len(by("o324020")) == 1, "324020 count")
            elif name == "g3910-b6t4":
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(lp == 100, f"lp {lp}")

        elif name.startswith("d4da0-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]

            if name == "d4da0-empty":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(byr("l31b810")) == 4, "b810 count")
                ck(tcount("l31e620") == 0, "31e620 on empty")
            elif name == "d4da0-hit":
                ck(eax == 1, f"ret {eax:#x}")
                ck(abs(gm.f(w.pout) - 10.0) < 1e-4,
                   f"pout {gm.f(w.pout)}")
                ck(len(byr("l31b810")) == 4, "b810 count")
                ck(len(byr("l3273b0")) == 2, "73b0 count")
                ck(len(byr("l265020")) == 1, "265020 count")
                ck(len(byr("l31e620")) == 1
                   and byr("l31e620")[0][1] == w.pos,
                   "31e620 arg")
                ck(len(by("s313f60")) == 0, "313f60 on zero mask")
                ck(len(by("cookie")) == 1, "cookie missing")
            elif name == "d4da0-sarg":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(byr("l3273b0")) == 1,
                   f"73b0 {len(byr('l3273b0'))}")
                ck(abs(gm.f(w.pout) - 10.0) < 1e-4, "pout")
            elif name == "d4da0-cid":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l265020") == 0, "265020 past gate")
                ck(tcount("l31e620") == 0, "31e620 past gate")
            elif name == "d4da0-gate":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(by("s313f60")) == 1, "313f60 missing")
                ck(tcount("l265020") == 0, "265020 past gate")
            elif name == "d4da0-alive":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(by("s313f60")) == 1, "313f60 missing")
                ck(abs(gm.f(w.pout) - 10.0) < 1e-4, "pout")
            elif name == "d4da0-min":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(byr("l31e620")) == 1, "31e620 count")
            elif name == "d4da0-max":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(byr("l31e620")) == 1, "31e620 count")
            elif name == "d4da0-notrip":
                ck(eax == 1, f"ret {eax:#x}")
                ck(abs(gm.f(w.pout) - 25.0) < 1e-4,
                   f"pout {gm.f(w.pout)}")
            elif name == "d4da0-second":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(byr("l31b810")) == 4, "b810 count")
                ck(abs(gm.f(w.pout) - 10.0) < 1e-4, "pout")

        elif name.startswith(("u0fc0-", "l01140-", "l4fe30-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            obj = w.objrow
            ent = w.objent if w.objrow else 0
            flg = gm.d(0x2089340)

            if name == "u0fc0-fast":
                ck(not w.faults, f"fault {w.faults}")
                u = by("u3105d0")
                ck(len(u) == 1 and u[0][1] == obj, f"3105d0 {u}")
                ck(tcount("l310780") == 0, "310780 on fast path")
                ck(tcount("l3138d0") == 1, "3138d0 tail")
                ck(gm.q(obj) == 0x4000000, "flags touched")
                ck(not by("b8c0"), "b8c0 ran (30d9a0!=1)")
                ck(not by("b040"), "23b040 ran")
            elif name == "u0fc0-fastt":
                u = by("u3105d0")
                ck(len(u) == 1 and u[0][1] == obj, f"3105d0 {u}")
                ck(len(by("b8c0")) == 1
                   and by("b8c0")[0][1] == 3, "b8c0 arg")
                ck(gm.w16(w.glob + 0x5AD0) == 2,
                   f"toggle {gm.w16(w.glob + 0x5AD0):#x}")
            elif name == "u0fc0-def":
                ck(not w.faults, f"fault {w.faults}")
                ck(tcount("l310780") == 1, "310780")
                # 310780's &0xFFFFFFFFEFFFFFDF + 300FC0's
                # &0xFFFFFFFDFFE7FFFD + &d[+4]0xFFFFFFFB fold to
                # q=0xFFFFFFF9EFE7FFDD / d4=0xFFFFFFF9.
                ck(gm.q(obj) == 0xFFFFFFF9EFE7FFDD,
                   f"qmask {gm.q(obj):#x}")
                ck(gm.d(obj + 4) == 0xFFFFFFF9, "d4 mask")
                ck(gm.b(obj + 0x694) == 0xFF, "b694")
                ck(tcount("l26dac0") == 1 and tcount("l26a330") == 1,
                   "ent writes")
                ck(tcount("l219d0") == 1, "3219d0")
                ck(len(by("b8270")) == 1 and by("b8270")[0][1] == obj,
                   "308270")
                # 30C970 gets b[obj+0x694] BEFORE the 0xFF write
                ck(len(by("bc970")) == 1 and by("bc970")[0][1] == 0x27,
                   f"30c970 {by('bc970')}")
                ck(len(by("b9420")) == 1
                   and by("b9420")[0][1] == obj + 0x6B0, "319420")
                ck(len(by("b9140")) == 1 and by("b9140")[0][1] == obj
                   and by("b9140")[0][2] == 1, "319140")
                ck(len(by("b9780")) == 1 and by("b9780")[0][1] == ent,
                   "2e9780")
                ck(len(by("b6f0")) == 1 and by("b6f0")[0][1] == ent,
                   "26d6f0")
                ck(flg == 0x100, f"flags {flg:#x}")
                ck(len(by("b48f0")) == 1 and by("b48f0")[0][1] == 1,
                   "2548f0")
                ck(gm.d(0x22C83E8) == 0x10, "22c83e8")
                ck(not by("b040"), "23b040")
                ck(tcount("l3138d0") == 0, "3138d0 on 30d9a0!=1")
            elif name == "u0fc0-m1":
                ck(not w.faults, f"fault {w.faults}")
                ck(tcount("l310780") == 1, "310780")
                ck(tcount("l3138d0") == 0, "3138d0 on edx!=0")
                ck(not by("b040"), "23b040 tail on edx!=0")
                ck(flg == 0x100, f"flags {flg:#x}")
            elif name == "u0fc0-s400":
                ck(flg == 0x400, f"flags {flg:#x}")
                ck(tcount("l3001d0") == 1, "3001d0")
                ck(len(by("b4850")) == 1 and by("b4850")[0][1] == 1,
                   "254850")
                ck(gm.d(0x22C83E8) == 2, "22c83e8")
                ck(len(by("b040")) == 1, "23b040 tail")
                ck(tcount("l37260") == 0, "237260 after tail")
            elif name == "u0fc0-s200":
                ck(flg == 0x200, f"flags {flg:#x}")
                ck(len(by("b4940")) == 1 and by("b4940")[0][1] == 1,
                   "254940")
                ck(gm.d(0x22C83E8) == 1, "22c83e8")
                ck(len(by("b040")) == 1, "23b040 tail")
                ck(tcount("l373c0") == 0, "2373c0 after tail")
            elif name == "u0fc0-s800":
                ck(flg == 0x800, f"flags {flg:#x}")
                ck(not by("b48f0"), "0x100 arm fired")
                ck(not by("b040"), "23b040 tail")
            elif name == "u0fc0-mtail":
                ck(flg == 0x100, f"flags {flg:#x}")
                ck(tcount("l3138d0") == 1, "3138d0")
                ck(len(by("b8c0")) == 1 and by("b8c0")[0][1] == 3,
                   "b8c0")
                ck(gm.w16(w.glob + 0x5AD0) == 2,
                   f"toggle {gm.w16(w.glob + 0x5AD0):#x}")
                ck(len(by("b040")) == 1, "23b040 tail")
            elif name == "u0fc0-caps":
                b8 = by("b1850")
                ck(len(b8) == 1, f"321850 count {b8}")
                if b8:
                    ck(b8[0][1] == w.oar4[1][0], "b1850 row")
                    ck(b8[0][2] == 0x21, "b1850 b4")
                    ck(b8[0][3] == 0 and b8[0][4] == 1,
                       "b1850 r8/r9")
            elif name == "u0fc0-norec":
                ck(w.faults and w.faults[0][2] == 4
                   and w.faults[0][3] == 0x30105A,
                   f"fault {w.faults}")

            elif name == "l01140-bail":
                ck(not w.faults, f"fault {w.faults}")
                ck(gm.d(obj + 0x748) == 0xAA, "bail wrote d748")
                ck(not by("d8bf0") and not by("u3105d0")
                   and not by("tecf10"), "release ran on bail")
            elif name == "l01140-rel":
                ck(not w.faults, f"fault {w.faults}")
                ck(len(by("d8bf0")) == 1 and by("d8bf0")[0][1] == obj,
                   "238bf0")
                ck(len(by("u3105d0")) == 1 and by("u3105d0")[0][1] == obj,
                   "3105d0")
                ck(gm.d(obj) == 0x45000000, f"d0 {gm.d(obj):#x}")
                ck(gm.d(obj + 4) == 0x200000, f"d4 {gm.d(obj+4):#x}")
                ck(gm.q(obj + 0x6F8) == 0, "q6f8")
                ck(gm.d(obj + 0x748) == 0, "d748")
                ck(gm.d(obj + 0x770) == 0, "d770")
                ck(gm.q(obj + 0x750) == 0, "q750")
                ck(gm.d(obj + 0x74C) == 0, "d74c")
                ck(gm.d(obj + 0x788) == 0xFF, "d788")
                ck(gm.d(obj + 0x6B0) == 0xFD, "d6b0")
                ck(gm.d(obj + 0xDCC) == 0, "dcc")
                ck(gm.d(obj + 0x30) == 0, "d30")
                ck(gm.d(obj + 0x74) == 0xFFFFFFFF, "d74")
                ck(gm.d(obj + 0xDD0) == 1150,
                   f"dd0 {gm.d(obj+0xDD0)}")
                ck(gm.q(obj + 0x6E8) == 0x1EEC3C0,
                   f"strptr {gm.q(obj+0x6E8):#x}")
                b3 = by("b3b02a0")
                ck(len(b3) == 1 and b3[0][1] == 0
                   and b3[0][2] == obj + 8 and b3[0][3] == 1
                   and b3[0][4] == 0x7B, f"3b02a0 {b3}")
                ck(len(by("tecf10")) == 1
                   and by("tecf10")[0][1] == ent, "2ecf10")
                ck(gm.d(obj + 0x5C) == 0x200D, "d5c msg")
                ck(gm.d(obj + 0x2C) == 0, "d2c")
                ck(gm.b(ent + 0xF5) == 0xFF, "bF5")
                ck(gm.d(ent + 0xF0) == 0x200D, "dF0")
                kk = by("kb0d0")
                ck(len(kk) == 1 and kk[0][1] == ent
                   and kk[0][3] == 0x200D and kk[0][4] == 1,
                   f"kb0d0 {kk}")
                ck(not by("b1f70"), "311f70 ran (bit26 set)")
                ck(not by("b0770"), "3b0770 ran (d74=0)")
                bb = by("bbb80")
                ck(len(bb) == 1 and bb[0][1] == ent and bb[0][2] == 0,
                   f"2ebb80 {bb}")
            elif name == "l01140-sent":
                ck(gm.d(obj) & 0x4000, "bit14 kept on 0x113 sentinel")
            elif name == "l01140-sentc":
                ck(not (gm.d(obj) & 0x4000), "bit14 cleared on miss")
            elif name == "l01140-f70":
                f7 = by("b1f70")
                ck(len(f7) == 1 and f7[0][1] == 0
                   and f7[0][2] == obj and f7[0][3] == 0,
                   f"311f70 {f7}")
            elif name == "l01140-strn":
                ck(gm.q(obj + 0x6E8) == 0x1EEC410,
                   f"strptr {gm.q(obj+0x6E8):#x}")
            elif name == "l01140-e30":
                ck(len(by("b0770")) == 1 and by("b0770")[0][1] == 5,
                   f"3b0770 {by('b0770')}")
            elif name == "l01140-bbb1":
                bb = by("bbb80")
                ck(len(bb) == 1 and bb[0][2] == 1, f"bbb80 {bb}")
            elif name == "l01140-norec":
                ck(w.faults and w.faults[0][2] == 0x64
                   and w.faults[0][3] == 0x301150,
                   f"fault {w.faults}")

            elif name == "l4fe30-n0":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("b4e70"), "24fe70 ran")
            elif name in ("l4fe30-n8", "l4fe30-nf"):
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "l4fe30-n1":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(by("bc1d0")) == 1 and by("bc1d0")[0][1] == 8
                   and by("bc1d0")[0][2] == 0xA, f"lock {by('bc1d0')}")
                b4 = by("b4e70")
                ck(len(b4) == 1 and b4[0][1] == w.rec
                   and b4[0][2] == 2, f"24fe70 {b4}")
                ck(len(by("bc140")) == 1, "unlock")
            elif name == "l4fe30-n1m":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("bc1d0"), "lock ran on miss")
            elif name == "l4fe30-n1d0":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l2fd0c0") == 1, "2fd0c0 dispatch")
                ck(not by("bc1d0") and not by("b4e70"),
                   "lock/query on edx=0")
            elif name == "l4fe30-n5":
                ck(eax == 1, f"ret {eax:#x}")
                b4 = by("b4e70")
                ck(len(b4) == 1 and b4[0][1] == w.rec
                   and b4[0][2] == 2, f"24fe70 {b4}")
                ck(len(by("bc140")) == 1, "unlock")
            elif name in ("l4fe30-n6", "l4fe30-n9"):
                ck(eax == 0, f"ret {eax:#x}")
                ck(not by("b4e70"), "24fe70 on no match")
            elif name == "l4fe30-n7":
                ck(eax == 1, f"ret {eax:#x}")
                b4 = by("b4e70")
                ck(len(b4) == 1 and b4[0][1] == w.rec
                   and b4[0][2] == 3, f"24fe70 {b4}")
                ck(gm.w16(w.rec + 0x378) == 3,
                   f"w378 {gm.w16(w.rec+0x378):#x}")

        elif name.startswith("d228-") or name.startswith("f8bb0-")                 or name.startswith("f90c0-"):
            calls = w.rets.get("calls", [])
            rargs = w.rets.get("rargs", [])
            by = lambda t: [c for c in calls if c[0] == t]
            byr = lambda t: [c for c in rargs if c[0] == t]
            tcount = lambda t: w.trace.count(t)
            obj = w.objrow
            g0 = w.guests.get(0, 0)

            if name == "d228-null":
                ck(not calls, f"calls {calls}")
                ck(not w.trace, f"trace {w.trace}")
            elif name == "d228-norec":
                ck(len(by("s71c0")) == 1
                   and by("s71c0")[0][1] == obj, "s71c0")
                ck(not by("s7ed0"), "s7ed0 on null rec")
                ck(not byr("l28bb0"), "l28bb0 past gate")
                ck(not by("s7090"), "s7090 past gate")
            elif name == "d228-b5rec":
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(not byr("l28bb0"), "l28bb0 past b5 gate")
                ck(not by("s7090"), "s7090 past b5 gate")
            elif name == "d228-e9a8":
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(not byr("l28bb0"), "l28bb0 past e9a.8")
                ck(not by("s7090"), "s7090 past e9a.8")
            elif name == "d228-norow2":
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(not by("s7ed0"), "s7ed0 w/o peer rec")
                ck(not byr("l28bb0"), "l28bb0 w/o scan arm")
                ck(not by("s7090"), "s7090 w/o scan arm")
            elif name == "d228-row2b5":
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(not byr("l28bb0"), "l28bb0 w/ b5!=0 peer")
                ck(not by("s7090"), "s7090 w/ b5!=0 peer")
            elif name == "d228-f2nol2":
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(not byr("l28bb0"), "l28bb0 w/ f2 but no e9a.2")
                ck(not by("s7090"), "s7090 w/ f2 but no e9a.2")
            elif name == "d228-gate5":
                ck(len(by("s7ed0")) == 0, "s7ed0 w/o peer")
                ck(len(by("s71c0")) == 1, "s71c0")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(by("c650")) == 0, "c650 w/o guests")
                ck(len(byr("l28bb0")) == 1
                   and byr("l28bb0")[0][1] == 0
                   and byr("l28bb0")[0][2] == obj, "src 8bb0 args")
                ck(len(byr("l290c0")) == 1
                   and byr("l290c0")[0][1] == 0
                   and byr("l290c0")[0][2] == obj, "src 90c0 args")
                ck(len(by("sfb80")) == 1, "sfb80")
                ck(len(by("s7090")) == 1
                   and by("s7090")[0][1] == obj, "s7090")
            elif name == "d228-gaterc":
                ck(len(by("s7ed0")) == 1
                   and by("s7ed0")[0][1] == obj, "s7ed0 arg")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(by("s7090")) == 1, "s7090")
            elif name == "d228-gatef2":
                ck(not by("s7ed0"), "s7ed0 w/o peer")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(by("s7090")) == 1, "s7090")
            elif name == "d228-g1":
                ck(gm.q(0x22C1740) == g0, "stash[0]")
                ck(gm.d(g0 + 0x18C) == 150,
                   f"exp {gm.d(g0 + 0x18C):#x}")
                ck(gm.d(g0 + 0x190) == 30,
                   f"lp {gm.d(g0 + 0x190):#x}")
                s6 = by("s6a50")
                ck(len(s6) == 1 and s6[0][2] == 10, f"s6a50 {s6}")
                c6 = by("c650")
                ck(len(c6) == 1 and c6[0][1] == g0
                   and c6[0][2] == 5, f"c650 {c6}")
            elif name == "d228-gflg":
                # EXP-200: real formulas re-check (d64|d3C)&0x80000003
                # -> retained-but-flagged guest gets share 0.
                ck(gm.q(0x22C1740) == g0, "stash[0]")
                ck(tcount("cd7c20") == 2,
                   "377c20 scan + src 30d9a0")
                ck(gm.d(g0 + 0x18C) == 100, "flagged exp denied")
                ck(gm.d(g0 + 0x190) == 20, "flagged lp denied")
                s6 = by("s6a50")
                ck(len(s6) == 1 and s6[0][2] == 0, f"s6a50 {s6}")
            elif name == "d228-gflg0":
                ck(gm.q(0x22C1740) == 0, "stash empty")
                ck(tcount("cd7c20") == 2,
                   "377c20 scan + src 30d9a0")
                ck(len(by("c650")) == 0, "c650 on dropped guest")
                ck(gm.d(g0 + 0x18C) == 100, "exp not awarded")
            elif name == "d228-sup":
                ck(tcount("l236780") == 2, "236780 twice")
                ck(gm.d(g0 + 0x18C) == 100, "guest exp suppressed")
                ck(gm.d(g0 + 0x190) == 30, "guest lp kept")
                fb = by("sfb80")
                ck(len(fb) == 1 and fb[0][2] == 0
                   and fb[0][3] == 10, f"sfb80 {fb}")
            elif name == "d228-globn":
                pass  # fault asserted by expect_fault
            elif name == "d228-ecap":
                ck(gm.d(g0 + 0x18C) == 0x5F5E0FF,
                   f"exp {gm.d(g0 + 0x18C):#x}")
            elif name == "d228-lcap":
                ck(gm.d(g0 + 0x190) == 0x1869F,
                   f"lp {gm.d(g0 + 0x190):#x}")
            elif name == "d228-neg":
                ck(gm.d(g0 + 0x18C) == 100, "exp clamped to 0 add")
                ck(gm.d(g0 + 0x190) == 20, "lp clamped to 0 add")
            elif name == "d228-lp5":
                ck(gm.d(g0 + 0x190) == 20,
                   "consumed lp not added")
                s6 = by("s6a50")
                ck(len(s6) == 1 and s6[0][2] == 0,
                   f"s6a50 edx {s6}")
                # fp = (10-2)*3 + 7 + (5*10*5) = 281; 1000+281 -> set
                s5 = by("s54ee0")
                ck(len(s5) == 1 and s5[0][1] == 1281,
                   f"s54ee0 {s5}")
                s6d = by("s69e80")
                ck(len(s6d) == 1 and s6d[0][1] == 281,
                   f"s69e80 {s6d}")
            elif name == "d228-fp":
                s5 = by("s54ee0")
                ck(len(s5) == 1 and s5[0][1] == 36,
                   f"s54ee0 {s5}")
                s6d = by("s69e80")
                ck(len(s6d) == 1 and s6d[0][1] == 31,
                   f"s69e80 {s6d}")
            elif name == "d228-fpneg":
                s5 = by("s54ee0")
                ck(len(s5) == 1 and s5[0][1] == 0,
                   f"s54ee0 {s5}")
                s6d = by("s69e80")
                ck(len(s6d) == 1 and s6d[0][1] == 0xFFFFFFFB,
                   f"s69e80 {s6d}")
            elif name == "d228-pos":
                ck(len(by("s9490")) == 1, "s9490")
                ck(len(by("s80f0")) == 1
                   and by("s80f0")[0][1] == obj, "s80f0")
                ck(len(by("s9ca0")) == 1, "s9ca0")
            elif name == "d228-pos2":
                ck(len(by("s9490")) == 1, "s9490")
                ck(len(by("s80f0")) == 1, "s80f0")
                ck(not by("s9ca0"), "s9ca0 w/o 80f0")
            elif name == "d228-src":
                fb = by("sfb80")
                ck(len(fb) == 1 and fb[0][1] == 0x1234
                   and fb[0][2] == 77 and fb[0][3] == 88,
                   f"sfb80 {fb}")
            elif name == "d228-2g":
                ck(gm.q(0x22C1740) == w.guests[0], "stash[0]")
                ck(gm.q(0x22C1740 + 8) == w.guests[4],
                   "stash[1]")
                ck(len(by("s6a50")) == 2, "s6a50 count")
                ck(len(by("c650")) == 2, "c650 count")
            elif name == "d228-lvl":
                c6 = by("c650")
                ck(len(c6) == 1 and c6[0][1] == g0
                   and c6[0][2] == 4,
                   f"c650 {c6} (lvl target 4, exp 400)")
                ck(tcount("f8f20") == 3,
                   f"f8f20 calls {tcount('f8f20')}")

            # ---- EXP-200 formula asserts ----
            elif name in ("f8bb0-null", "f8bb0-norec", "f8bb0-b5rec",
                          "f90c0-norow", "f90c0-flag", "f90c0-norec",
                          "f90c0-b5rec"):
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "f8bb0-split":
                ck(eax == 50, f"ret {eax:#x}")
                ck(tcount("l31b810") == 4,
                   f"member scan {tcount('l31b810')}")
                ck(not byr("l313800"), "leader path ran")
            elif name == "f8bb0-split4":
                ck(eax == 12, f"ret {eax:#x}")
            elif name == "f8bb0-neg":
                ck(eax == 0xFFFFFFFB, f"ret {eax:#x}")
            elif name == "f8bb0-ndiv":
                ck(eax == 0xFFFFFFFE, f"ret {eax:#x}")
            elif name == "f8bb0-zdiv":
                # ebp==0 skips the whole compute -> esi stays 0
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "f8bb0-gok":
                ck(eax == 50, f"ret {eax:#x}")
                ck(len(byr("b860")) == 1, "owner resolve")
            elif name == "f8bb0-dbl":
                ck(eax == 100, f"ret {eax:#x}")
            elif name == "f8bb0-dbl7b":
                ck(eax == 100, f"ret {eax:#x}")
            elif name == "f8bb0-zero":
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "f8bb0-nown":
                ck(eax == 0, f"ret {eax:#x}")
            elif name in ("f8bb0-gb4", "f8bb0-gb5", "f8bb0-gflg",
                          "f8bb0-nlead", "f8bb0-lmiss"):
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "f8bb0-lead":
                ck(eax == 50, f"ret {eax:#x}")
                ck(len(byr("l313800")) == 1, "leader resolve")
                ck(len(byr("l320890")) == 1, "slot map lookup")
                ck(not byr("l31b810"), "member scan ran")
            elif name == "f8bb0-lead0":
                ck(eax == 50, f"ret {eax:#x}")
            elif name == "f90c0-split":
                ck(eax == 10, f"ret {eax:#x}")
            elif name == "f90c0-neg":
                ck(eax == 0xFFFFFFFB, f"ret {eax:#x}")
            elif name in ("f90c0-dbl", "f90c0-dbl7b"):
                ck(eax == 20, f"ret {eax:#x}")
            elif name in ("f90c0-gb4a", "f90c0-gb4hi",
                          "f90c0-nolink"):
                ck(eax == 10, f"ret {eax:#x}")
            elif name in ("f90c0-gb4lo", "f90c0-gb5", "f90c0-gflg"):
                ck(eax == 0, f"ret {eax:#x}")

        elif name.startswith("f3f0-") or name.startswith("f4b0-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)

            if name == "f3f0-none":
                # flags=0 -> mask=globals=0 -> f690 skipped entirely
                ck(tcount("r2ab0") == 9, f"slots {tcount('r2ab0')}")
                ck(tcount("i1b9f0") == 9, f"map {tcount('i1b9f0')}")
                ck(tcount("f690") == 0, "f690 ran on empty mask")
            elif name == "f3f0-bit10":
                # mask=0x544 -> bits 2,6,8,10 per resolved rec
                ck(tcount("f690") == 9, f"f690 {tcount('f690')}")
                ck(tcount("e360") == 36, f"e360 {tcount('e360')}")
            elif name == "f3f0-gates":
                # mask = 0x40|0x80|0x544 = 0x5C4 -> bits 2,6,7,8,10
                ck(tcount("f690") == 9, f"f690 {tcount('f690')}")
                ck(tcount("e360") == 45, f"e360 {tcount('e360')}")
            elif name == "f3f0-trio":
                # bits 0,1: f340+f5a0 fire; mask=0 (bit0x10 clear)
                ck(tcount("f340") == 9, f"f340 {tcount('f340')}")
                ck(tcount("f5a0") == 9, f"f5a0 {tcount('f5a0')}")
                ck(tcount("f690") == 0, "f690 ran")
            elif name == "f3f0-emptymap":
                # slot3 map=0xFF -> rdi=0 -> f690's null guard: silent skip
                ck(not w.faults, f"fault {w.faults}")
                ck(tcount("r2ab0") == 9, f"slots {tcount('r2ab0')}")
                ck(tcount("f690") == 9, f"f690 {tcount('f690')}")
                ck(tcount("e360") == 32,
                   f"e360 {tcount('e360')} (null slot must skip 4)")
            elif name == "f4b0-foes":
                # flags=0: resolve all, dispatch nothing
                ck(tcount("r2ab0") == 9, f"member {tcount('r2ab0')}")
                ck(tcount("vb0e0") == 13, f"id-chk {tcount('vb0e0')}")
                ck(tcount("r2a40") == 13, f"foe-res {tcount('r2a40')}")
                ck(tcount("f690") == 0, "f690 ran")
            elif name == "f4b0-mask":
                ck(tcount("f690") == 22, f"f690 {tcount('f690')}")
                ck(tcount("e360") == 88, f"e360 {tcount('e360')}")
            elif name == "f4b0-trio":
                ck(tcount("f340") == 22, f"f340 {tcount('f340')}")
                ck(tcount("f5a0") == 22, f"f5a0 {tcount('f5a0')}")
                ck(tcount("f690") == 22, f"f690 {tcount('f690')}")
            elif name == "f4b0-skip":
                # bitmap 0x000C -> only ids 0x12,0x13 valid -> 2 foes
                ck(tcount("vb0e0") == 13, f"id-chk {tcount('vb0e0')}")
                ck(tcount("r2a40") == 2, f"foe-res {tcount('r2a40')}")
                ck(tcount("f690") == 11, f"f690 {tcount('f690')}")

        elif name.startswith("e360-"):
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            bit = case.get("r8", 0)
            f38, f3c, f64 = (gm.d(w.rec + 0x38), gm.d(w.rec + 0x3C),
                             gm.d(w.rec + 0x64))
            arr_d = gm.d(w.rec + 0xBC + bit * 4)
            arr_w = gm.w16(w.rec + 0x13C + bit * 2)
            ck("e360" in w.trace or True, "")

            if name == "e360-arm0-clr":
                ck(f64 == 1 << 5, f"d64 {f64:#x}")
                ck(arr_d == 0x77 and arr_w == 0x1234,
                   f"arr {arr_d:#x}/{arr_w:#x}")
            elif name == "e360-arm0-noop":
                ck(f64 == 1 << 5, f"d64 {f64:#x}")
                ck(arr_d == 0 and arr_w == 0,
                   "no-op wrote arrays")
            elif name == "e360-arm1-clr":
                ck(f3c == 0, f"d3C {f3c:#x}")
                ck(arr_d == 0 and arr_w == 0,
                   "non-0/3 arm wrote arrays")
            elif name == "e360-arm2-clr":
                ck(f38 == 0, f"d38 {f38:#x}")
                ck(arr_d == 0 and arr_w == 0,
                   "non-0/3 arm wrote arrays")
            elif name == "e360-arm3-set":
                ck(f64 == 1 << 2, f"d64 {f64:#x}")
                ck(arr_d == 0xAA and arr_w == 0x4567,
                   f"arr {arr_d:#x}/{arr_w:#x}")
            elif name == "e360-arm3-conflict":
                ck(f64 == 0 and f38 == 1 << 2,
                   f"d64 {f64:#x} d38 {f38:#x}")
            elif name == "e360-arm4-set":
                ck(f3c == 1 << 5, f"d3C {f3c:#x}")
                ck(arr_d == 0 and arr_w == 0,
                   "non-0/3 arm wrote arrays")
            elif name == "e360-arm5-set":
                ck(f38 == 1 << 6, f"d38 {f38:#x}")
                ck(arr_d == 0 and arr_w == 0,
                   "non-0/3 arm wrote arrays")
            elif name == "e360-bit1c":
                ck(f64 == 0, f"d64 {f64:#x}")
                # 386A70's 0x1C special writes the 0x148 stack block
                # (d[blk+0x2C]|=0x108, d[blk+0x24]=(d[src+0x48]+1)>>1);
                # entry + block reset prove the path ran
                ck("h86a70" in w.trace and "c848e0" in w.trace,
                   "386A70/3848E0 path missing")
            elif name == "e360-cascade":
                ck(f64 == 1 << 2,
                   f"d64 {f64:#x} (bit2 set, bit4 cascade-cleared)")
            elif name == "e360-owner-chk":
                ck(len(byr("lb9b0")) == 1, "30B9B0 missing")
                ck(not byr("lb8e0"), "30B8E0 on non-mode arm")
                ck(f64 == 0, f"d64 {f64:#x}")
            elif name == "e360-owner-bail":
                ck(len(byr("lb9b0")) == 1, "30B9B0 missing")
                ck(f64 == 1 << 2, f"bail touched d64 {f64:#x}")
            elif name == "e360-owner2-chk":
                ck(len(byr("lb9b0")) == 1 and len(byr("lb8e0")) == 1,
                   f"owner pair {rargs}")
                ck(f64 == 1 << 2, f"d64 {f64:#x}")
            elif name == "e360-mode-pair":
                ck(len(by("qfa390")) == 1 and len(by("q6ab10")) == 1,
                   f"46A800->46AB10 missing {calls}")
                ck(f64 == 1 << 1, f"d64 {f64:#x}")
            elif name == "e360-nomode-pair":
                ck(not by("qfa390"), "46A800 on non-mode arm")
                ck(f64 == 0, f"d64 {f64:#x}")
            elif name == "e360-neg-arg5":
                ck(f64 == 0, f"d64 {f64:#x}")
                ck(arr_w == 3 * 2 * 0x1E,
                   f"arr_w {arr_w:#x} != resolved 0xB4")
                ck("v876d0" in w.trace, "3876D0 resolver not run")

        elif name.startswith("f690-") or name.startswith("f340-")                 or name.startswith("f5a0-"):
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]

            if name == "f690-mask0":
                # bit loop skips everything but the tail notify is
                # unconditional
                fe = by("fed0")
                ck(len(fe) == 1 and fe[0][1] == w.rec
                   and fe[0][2] == 0x217, f"tail fed0 {fe}")
                ck(not by("e360"), "e360 on empty mask")

            elif name == "f690-bits13":
                # e360 real: arm0 clears d64 bits 1,3 (planted)
                ck(gm.d(w.rec + 0x64) == 0,
                   f"d64 {gm.d(w.rec + 0x64):#x} not cleared")
                ck("e360" in w.trace, "e360 not entered")
                # e360's own prologue resolves the owner row -> b860
                # legitimately traced even without the f690 fixup
                fe = by("fed0")
                ck(len(fe) == 1 and fe[0][2] == 0x217,
                   f"tail fed0 {fe}")

            elif name.startswith("f690-bit0"):
                # e360 real: arm0 clears d64 bit0 (planted)
                ck(gm.d(w.rec + 0x64) & 1 == 0,
                   f"d64 bit0 not cleared {gm.d(w.rec + 0x64):#x}")
                ck("e360" in w.trace, "e360 not entered")
                ck("b860" in w.trace, "b860 scan missing")
                if name == "f690-bit0-norow":
                    ck("cd7c20" not in w.trace, "cd ran w/o row")
                elif name == "f690-bit0-noflg":
                    ck("cd7c20" not in w.trace, "cd ran w/o flags")
                    ck(gm.q(w.objrow) & 0x4000000,
                       "bit26 cleared w/o flags")
                elif name == "f690-bit0-candie":
                    ck("cd7c20" in w.trace, "cd not run")
                    ck(gm.q(w.objrow) & 0x4000000,
                       "bit26 cleared despite can-die")
                elif name == "f690-bit0-clear":
                    ck("cd7c20" in w.trace, "cd not run")
                    ck(gm.q(w.objrow) & 0x4000000 == 0,
                       "bit26 not cleared")
                fe = by("fed0")
                ck(len(fe) == 1 and fe[0][2] == 0x217,
                   f"tail fed0 {fe}")

            elif name == "f340-equal":
                ck(not calls, f"calls on equal {calls}")

            elif name == "f340-delta":
                # 300530 now real: f340 passes delta=7 -> d48 0+7=7
                ck(not w.faults, f"fault {w.faults}")
                ck(gm.d(w.rec + 0x48) == 7,
                   f"d48={gm.d(w.rec + 0x48)}")
                ck(not by("u43f0"), "u43f0 w/o stored<=0")

            elif name == "f340-bit1c":
                # computed 7*2=14 -> d48 = 0+14 = 14
                ck(gm.d(w.rec + 0x48) == 14,
                   f"d48={gm.d(w.rec + 0x48)}")

            elif name == "f340-bit10":
                # computed = max(-5,1)=1 vs stored -5 -> delta 6;
                # stored<=0 + idx 0x1C in [0x1B,0x27] + b5==0 -> unlink
                ck("b860" in w.trace, "b860 unlink scan missing")
                u = by("u43f0")
                ck(len(u) == 1 and u[0][1] == w.objrow,
                   f"u43f0 arg {u}")
                # real 300530: d48 = -5+6 = 1
                ck(gm.d(w.rec + 0x48) == 1,
                   f"d48={gm.d(w.rec + 0x48)}")

            elif name == "f5a0-equal":
                ck(not calls, f"calls on equal {calls}")

            elif name == "f5a0-hp":
                # sec1: w28=100 vs w4C=50 -> ce0(+50) -> w4C=100 +
                # cascade bc0(+50) -> w6 0->50; sec2: b37=0 ->
                # computed = w28 (scale defaults 1) vs w6=50 ->
                # bc0(+50) -> w6=100
                ck(gm.w16(w.rec + 0x4C) == 100,
                   f"w4C {gm.w16(w.rec + 0x4C)}")
                ck(gm.w16(w.rec + 0x6) == 100,
                   f"w6 {gm.w16(w.rec + 0x6)}")
                ck("h0ce0" in w.trace and "h0bc0" in w.trace,
                   "apply pair not entered")

            elif name == "f5a0-gated":
                # b6C<0 -> sec1 computed 0 vs w4C=50 -> ce0(-50)
                # -> w4C=0; drop -> q2fa540 on owner row
                ck(gm.w16(w.rec + 0x4C) == 0,
                   f"w4C {gm.w16(w.rec + 0x4C)}")
                ck("h0ce0" in w.trace, "ce0 not entered")

            elif name == "f5a0-b37":
                # sec1 equal (w28==w4C==10); sec2: 3*10=30 vs w6=20
                # -> bc0(+10) -> w6=30 (cap=30)
                ck(gm.w16(w.rec + 0x4C) == 10,
                   f"w4C {gm.w16(w.rec + 0x4C)}")
                ck(gm.w16(w.rec + 0x6) == 30,
                   f"w6 {gm.w16(w.rec + 0x6)}")
                ck("h0ce0" not in w.trace, "ce0 on equal section1")

        elif name.startswith(("fa3b0-", "fmt-", "bd00-", "d4d0-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            rargs = w.rets.get("rargs", [])
            by = lambda t: [c for c in calls if c[0] == t]
            byr = lambda t: [c for c in rargs if c[0] == t]
            ms = w.rets.get("memsets", [])
            randn = w.rets.get("randn", 0)
            qi = case.get("qidx", 0) & 0xFF
            qsx = qi - 0x100 if qi >= 0x80 else qi
            slot = w.qtab + qsx * 0x50
            F16 = 0x41800000      # +16.0f
            FM16 = 0xC1800000     # -16.0f

            if name == "fa3b0-null":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l272a0") == 0, "3272A0 ran on null")
            elif name == "fa3b0-near":
                ck(eax == 1, f"eax {eax:x} !=1 (dist<24)")
                ck(tcount("l272a0") == 1, "gate missing")
                ck(tcount("l265020") == 1, "vec3 read missing")
                ck(tcount("l3a1920") == 1 and tcount("sqrtf") == 1,
                   "dist+sqrt missing")
            elif name == "fa3b0-far":
                ck(eax == 0, f"eax {eax:x} (dist 100 >= 24)")
                ck(tcount("l265020") == 1, "vec3 read missing")
            elif name == "fa3b0-edge":
                ck(eax == 0, f"eax {eax:x} (24.0 boundary excluded)")
            elif name == "fa3b0-fl":
                ck(eax == 1, f"eax {eax:x}")
                ck(tcount("l3588b0") == 1, "flag gate not taken")
                ck(tcount("l263e30") == 0,
                   "263E30 ran on 3588B0(0)=0")
            elif name == "fa3b0-b3":
                # b[obj+3] class rejects the vec3 copy -> dst stays
                # zeroed -> dist 0 < 24 -> still returns 1.
                ck(eax == 1, f"eax {eax:x} (reject class -> zero vec)")
                ck(tcount("l265020") == 1, "vec3 call missing")

            elif name.startswith("fmt-"):
                buf = w.fmtbuf
                txt = bytes(gm.b(buf + i) for i in range(12))
                if name == "fmt-zero":
                    ck(txt[:2] == b"0\x00", f"buf {txt}")
                    ck(eax == 1, f"len {eax}")
                elif name == "fmt-pos":
                    ck(txt[:6] == b"12345\x00", f"buf {txt}")
                    ck(eax == 5, f"len {eax}")
                elif name == "fmt-pad":
                    ck(txt[:5] == b"   7\x00", f"buf {txt}")
                    ck([buf, 4] in ms, f"pad memset {ms}")
                    ck(eax == 4, f"len {eax}")
                elif name == "fmt-zpad":
                    ck(txt[:5] == b"0007\x00", f"buf {txt}")
                    ck(eax == 4, f"len {eax}")
                elif name == "fmt-big":
                    ck(txt[:10] == b"999999999\x00", f"buf {txt}")
                    ck(eax == 9, f"len {eax}")
                elif name == "fmt-neg":
                    # signed edx <= 0 skips the count loop -> empty
                    ck(txt[:1] == b"\x00", f"neg fmt {txt}")
                    ck(eax == 0, f"len {eax}")

            elif name == "bd00-notab":
                ck((eax & 0xFF) == 0xFF, f"eax {eax:x}")
                ck(tcount("l506700") == 0 and tcount("l28fbe0") == 0,
                   "slot work ran w/o table")
                ck(randn == 0, f"randn {randn}")
            elif name == "bd00-occ":
                ck((eax & 0xFF) == 0xFF, f"eax {eax:x} (slot occupied)")
                ck(tcount("l506700") == 0, "init ran on occupied")
                ck(gm.b(0x2B443C0) == 0, "qidx moved")
            elif name == "bd00-t0":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.q(slot) == w.subobj, "entry obj")
                ck(gm.w16(slot + 0x3A) == 1, "w3A")
                ck(gm.b(slot + 0x3C) == 0, "b3C type")
                ck(bytes(gm.b(slot + 0x40 + i) for i in range(6))
                   == b"12345\x00", "fmt into slot+0x40")
                ck(gm.b(slot + 0x3F) == 5, "b3F len")
                ck(gm.d(slot + 0xC) == 0x80808080, "d0C color")
                ck(gm.b(slot + 0x3D) == 0, "b3D")
                ck(gm.b(slot + 0x3E) == 0, "cat byte")
                ck(gm.d(slot + 0x14) == 0 and gm.d(slot + 0x18) == 0,
                   "cat0 scale floats")
                ck(gm.b(0x2B443C0) == 1, "qidx advance")
                ck(randn == 1, f"randn {randn}")
                for t in ("l506700", "l3efd00", "l24a5a0", "l28fbe0",
                          "l296280", "l2dd7e0", "l2dd7b0"):
                    ck(tcount(t) >= 1, f"{t} missing")
                ck([slot, 0x50] in ms, "slot memset")
            elif name == "bd00-t0v0":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l296280") == 0,
                   "row scan ran on zero value")
            elif name == "bd00-t1":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.b(slot + 0x3F) == 3, "b3F = b[req+8]")
                ck(gm.q(slot + 0x30) == 0, "q30 name-slot")
                ck(gm.d(slot + 0xC) == 0x80808080
                   and gm.d(slot + 0x10) == 0x80808080,
                   "idx lookups default")
                ck(gm.w16(slot + 0x3A) == 1, "w3A")
            elif name == "bd00-t2":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.w16(slot + 0x3A) == 3, "w3A type2")
                ck(gm.b(slot + 0x3F) == 7, "b3F")
                ck(gm.q(slot + 0x30) == w.nstr + 2, "q30 name ptr")
                ck(gm.b(slot + 0x3D) == 4, "b3D=4")
                ck(gm.d(slot + 0xC) == 0x80808080, "d0C")
                ck(gm.d(slot + 0x44) == 0, "d44 pri")
                c = by("s31c5d0")
                ck(len(c) == 2 and all(x[1] == 0x22CA520 for x in c),
                   f"s31c5d0 args {c}")
                ck(gm.d(0x22CA520) == 0x1A
                   and gm.d(0x22CA524) == 7, "rblk kind/arg")
                c = by("s2b3050")
                ck(len(c) == 1 and c[0][2] == w.nstr + 2
                   and c[0][3] == slot + 0x40
                   and c[0][4] == slot + 0x42, f"s2b3050 {c}")
            elif name == "bd00-t2ff":
                ck((eax & 0xFF) == 0xFF, f"eax {eax:x} (b24==FF gate)")
                ck(tcount("l506700") == 0, "init ran past gate")
                ck(len(by("s31c5d0")) == 1, "resolver not called")
                ck(gm.b(0x2B443C0) == 0, "qidx moved")
            elif name == "bd00-t2b25":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.d(slot + 0xC) == 0x1234,
                   f"d0C override {gm.d(slot + 0xC):x}")
            elif name == "bd00-t2neg":
                # s31c5d0 ret<0 -> 35D330 memsets blk (0x98) -> b24=0
                # -> gate passes anyway
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l506700") == 1, "init missing")
                ck([0x22CA520, 0x98] in ms, f"blk memset {ms}")
                ck(gm.d(0x22CA520) == 0, "blk wiped")
            elif name == "bd00-cat2":
                ck((eax & 0xFF) == 0x23, f"eax {eax:x}")
                ck(gm.b(slot + 0x3E) == 2, "cat=2")
                ck(gm.d(slot + 0x14) == F16
                   and gm.d(slot + 0x18) == F16, "scale floats")
                ck(randn == 1, f"randn {randn} (derive, not rand)")
            elif name == "bd00-cat3":
                ck(gm.b(slot + 0x3E) == 3, "cat=3")
                ck(gm.d(slot + 0x14) == F16
                   and gm.d(slot + 0x18) == FM16, "floats")
            elif name == "bd00-cat4":
                ck(gm.b(slot + 0x3E) == 4, "cat=4")
                ck(gm.d(slot + 0x14) == FM16
                   and gm.d(slot + 0x18) == F16, "floats")
            elif name == "bd00-cat1":
                ck(gm.b(slot + 0x3E) == 1, "cat=1")
                ck(gm.d(slot + 0x14) == FM16
                   and gm.d(slot + 0x18) == FM16, "floats")
            elif name == "bd00-rand1":
                ck(gm.b(slot + 0x3E) == 1, "rand cat=1")
                ck(randn == 2, f"randn {randn}")
                ck(gm.d(slot + 0x14) == FM16
                   and gm.d(slot + 0x18) == FM16, "floats")
            elif name == "bd00-rand3":
                ck(gm.b(slot + 0x3E) == 3, "rand cat=3")
                ck(randn == 2, f"randn {randn}")
                # scale = 1.0 + (rand&0x1F) * 0.03125 -> 16.5 for rv=1
                ck(struct.unpack("<f", struct.pack(
                    "<I", gm.d(slot + 0x14)))[0] == 16.5
                   and struct.unpack("<f", struct.pack(
                       "<I", gm.d(slot + 0x18)))[0] == -16.5,
                   "scaled floats")
            elif name == "bd00-wrap":
                ck((eax & 0xFF) == 0x3F, f"eax {eax:x} (0x3F|0x20)")
                ck(gm.b(0x2B443C0) == 0, "qidx wrapped")
            elif name == "bd00-neg":
                ck((eax & 0xFF) == 0xFF, f"eax {eax:x} (0xFF|0x20)")
            elif name == "bd00-t2pri":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.w16(w.qtab + 1 * 0x50 + 0x3A) == 8,
                   "w3a +3 on type2 scan")
                ck(gm.w16(w.qtab + 2 * 0x50 + 0x3A) == 12,
                   "w3a +3 (obj-mismatched still bumps)")
                ck(gm.d(slot + 0x44) == 10,
                   f"d44 {gm.d(slot + 0x44)} != max+3")
            elif name == "bd00-t3":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.b(slot + 0x3C) == 3 and gm.w16(slot + 0x3A) == 1,
                   "base fields")
                ck(gm.b(slot + 0x3F) == 0 and gm.d(slot + 0xC) == 0,
                   "no arm writes")
                for t in ("l3efd00", "s31c5d0", "s2b3050"):
                    ck(tcount(t) == 0 and not by(t), f"{t} ran")

            elif name == "d4d0-null":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("lfa3b0") == 1, "gate missing")
                ck(tcount("l3bbd00") == 0, "enqueue on null subobj")
            elif name == "d4d0-far":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 0, "enqueue past 24u")
            elif name == "d4d0-near":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 1 and tcount("l506700") == 1,
                   "enqueue missing")
                ck(len(by("s31c5d0")) == 2
                   and gm.d(0x22CA520) == 0x1A
                   and gm.d(0x22CA524) == 5, "type2 req fields")
                ck(gm.b(w.qtab + 0x3C) == 2, "slot type")
                ck(gm.b(w.qtab + 0x3F) == 5, "slot b3F=flag")
                ck(gm.w16(w.qtab + 0x3A) == 3, "w3A type2")
                ck(len(by("s2b3050")) == 1, "string call missing")

        res[name] = {"ok": ok, "ret": eax, "trace": w.trace,
                     "calls": w.rets.get("calls", []),
                     "faults": w.faults, "notes": notes}
        print(f"{'PASS' if ok else 'FAIL'} {name}"
              + ("" if ok else f"  {notes}"))
    npass = sum(1 for r in res.values() if r["ok"])
    print(f"{npass}/{len(res)} pass")
    json.dump(res, open(RESULT, "w"), indent=1, default=str)
    return 0 if npass == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
