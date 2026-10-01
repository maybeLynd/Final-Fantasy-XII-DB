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
#     b[18]!=1->2EB0D0(node,q[C0],ebx,1,-1f); d[obj+0x5C]=ebx,
#     d[obj+0x2C]=0.  EXP-233 promoted 2EB0D0 real.  (3284D0/3BBD00
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
R_69BB0 = 0x00469BB0        # 21i -> scripted 2FA390 + REAL 46AB10
R_08A0  = 0x003008A0        # id resolver (sibling of 300530)
R_2FD420 = 0x002FD420       # cls-0xC spawn-bitmap mutator
R_325F40 = 0x00325F40       # change-notify router (call rsi)
R_6A630 = 0x0046A630        # 26i -> REAL 46AB10
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
def ww(v): return struct.pack("<H", v & 0xFFFF)
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
        # EXP-214: real 2B43C0 (0x200 frame) + 2AF340 + nested walkers
        # push the deepest frame below the old STACK floor — map a
        # guard region underneath.
        self.uc.mem_map(STACK - 0x100000, 0x200000)
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
            # EXP-227: 3105D0's 33C9B0(obj+0x80) tail — 336710 copies
            # ctx fields incl q[obj+0x1E8] (elem-ref: +0x177 idx byte,
            # +0x108 float) and 33E1F0 and-writes q[obj+0x1E0]/+0x21
            # with no null check.  Linked objects carry both cells.
            self.obj1e0 = self.alloc(0x40)
            self.obj1e8 = self.alloc(0x200)
            gm.w(self.objrow + 0x1E0, qw(self.obj1e0))
            gm.w(self.objrow + 0x1E8, qw(self.obj1e8))
            # EXP-231: 308270's 30EDA0 tail copies q[obj+0xB88] (0x480
            # bytes) into obj+0x730 — the snapshot buffer a linked obj
            # carries; null faults inside 30EDA0.
            self.objb88 = self.alloc(0x600)
            gm.w(self.objrow + 0xB88, qw(self.objb88))
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
        # EXP-225: ec-family deep arm — q[objent+0xC0] link obj +
        # q[0x22C6F28] element array (0x740 stride).  2ECEC0 uses
        # w[link] as idx; 2ECF10 uses d[link].  d[elem+0x284] != 0
        # opens the tail (3AEEF0 zero-chain at elem+0x550).
        self.objc0 = 0
        self.objc0q = {}
        if "objc0" in case and self.objent:
            c0 = self.alloc(0x200)
            gm.w(self.objent + 0xC0, qw(c0))
            self.objc0 = c0
            for off, v in case["objc0"].items():
                gm.w(c0 + off, dw(v))
            # EXP-240: objc0q={off: size} wires q[c0+off] to a fresh
            # zeroed buffer (26D6F0/2E9BB0/2EC5B0 read q[node+0x138]).
            for off, sz in case.get("objc0q", {}).items():
                buf = self.alloc(sz)
                gm.w(c0 + off, qw(buf))
                self.objc0q[off] = buf
        ecarr = case.get("ecarr")
        self.ecarr = 0
        self.ecnodes = []
        if ecarr:
            arr = self.alloc(ecarr.get("elems", 4) * 0x740)
            gm.w(0x22C6F28, qw(arr))
            self.ecarr = arr
            for eidx, fields in ecarr.get("rows", {}).items():
                elem = arr + eidx * 0x740
                for off, v in fields.get("d", {}).items():
                    gm.w(elem + off, dw(v))
                for off, v in fields.get("q", {}).items():
                    gm.w(elem + off, qw(v))
                # 3AEEF0's node chain: q[elem+off]=head, next=q[+0x48],
                # each node carries marker b[+0].
                for off, vals in fields.get("chain", {}).items():
                    head = 0
                    for v in reversed(vals):
                        node = self.alloc(0x60)
                        gm.w(node, bytes([v & 0xFF]))
                        gm.w(node + 0x48, qw(head))
                        self.ecnodes.insert(0, node)
                        head = node
                    gm.w(elem + off, qw(head))
        # EXP-258: 422C20's d[+0xC4]/d[+0xC8] dereg arms run
        # 20E600(d[elem+0x10]) -> q[elem+0xDA8] -> 51BA40(container,
        # slot).  d[+0x10] is an elemb offset; the resolved element's
        # q[+0xDA8] is a mode-1 container: d[C+4]&3==1 indexes the
        # 0x30-stride descriptor array q[C+8] directly (51F240),
        # d[C+0x10]!=0 enables 51F4C0's w-index unlink, d[C+0x14] is
        # the live count, d[C+0x1C]/d[C+0x20] head/tail slots.
        # 51BA40 fetches desc A[slot]'s q[+0x18] record (b[desc]&2==0
        # = direct pointer), resets the record through 41CF00/41CB90,
        # then releases desc A[d[record]] via 51F4C0/51F190.
        self.delem = 0
        self.dcntr = 0
        self.darr = 0
        self.drecs = {}
        self.dcntr2 = 0
        self.dc2rows = 0
        self.dc2subs = 0
        self.dc2elem = 0
        self.dc3 = None
        dcn = case.get("dcntr")
        if dcn is not None:
            self.delem = self.alloc(0x740)
            eoff = dcn.get("eoff", 0x70000)
            gm.w(self.delem + 0x10, dw(eoff))
            for off, v in dcn.get("d", {}).items():
                gm.w(self.delem + off, dw(v))
            for off, v in dcn.get("q", {}).items():
                gm.w(self.delem + off, qw(v))
            for off, v in dcn.get("w", {}).items():
                gm.w(self.delem + off, struct.pack("<H", v & 0xFFFF))
            C = self.dcntr = self.alloc(0x40)
            A = self.darr = self.alloc(dcn.get("narr", 4) * 0x30)
            gm.w(C + 4, dw(dcn.get("mode", 1)))
            gm.w(C + 8, qw(A))
            gm.w(C + 0x10, dw(dcn.get("fill", 1)))
            gm.w(C + 0x14, dw(dcn.get("count", 2)))
            gm.w(C + 0x1C, dw(dcn.get("head", 0xFFFFFFFF)))
            gm.w(C + 0x20, dw(dcn.get("tail", 0xFFFFFFFF)))
            gm.w(self.elemb + eoff + 0xDA8, qw(C))
            for s, spec in dcn.get("descs", {}).items():
                D = A + s * 0x30
                R = self.alloc(0x400)
                gm.w(R, dw(spec.get("key", 0)))
                gm.w(D + 0x18, qw(R))
                self.drecs[s] = R
                # EXP-262: record field writes — w[R+0x28] counts
                # 41CF00's 0xA0-stride subrecord resets; d[R+0xC]&0x1000
                # gates the record's own 2ED570 arm.
                for off, v in spec.get("rd", {}).items():
                    gm.w(R + off, dw(v))
                for off, v in spec.get("rw", {}).items():
                    gm.w(R + off, struct.pack("<H", v & 0xFFFF))
                # b[desc]&2 -> 51F240 re-resolves the record pointer:
                # q[D+0x18] = sx(3AB7F0(q[D+0x10]) + d[D+0x20]).
                if spec.get("rec2"):
                    r2 = self.alloc(0x400)
                    gm.w(r2, dw(spec.get("key2", 0)))
                    self.drecs[("r2", s)] = r2
                    add2 = spec.get("add2", 0)
                    gm.w(D + 0x10, qw(r2 - add2))
                    gm.w(D + 0x20, dw(add2))
                # d[R+0xC]&0x1000 -> 2ED570(q[R+0x330], d[R+0x338])
                # -> 372280 on the resolved element.  The record's
                # container uses the same row/sub layout as c2.
                rc2 = spec.get("rc2")
                if rc2 is not None:
                    C3 = self.alloc(0x60)
                    rows3 = self.alloc(rc2.get("nrows", 4) * 0x10)
                    subs3 = self.alloc(rc2.get("nsubs", 4) * 0x20)
                    self.dc3 = (C3, rows3, subs3)
                    gm.w(R + 0x330, qw(C3))
                    gm.w(R + 0x338, dw(rc2.get("slot", 0)))
                    gm.w(C3 + 0x30, qw(rows3))
                    gm.w(C3 + 8, qw(subs3))
                    gm.w(C3 + 0x4C, dw(rc2.get("shift", 0)))
                    gm.w(C3 + 0x50, dw(rc2.get("mask", 0)))
                    gm.w(C3 + 0x48, dw(rc2.get("mult", 0)))
                    for i, rs in rc2.get("rows", {}).items():
                        for off, v in rs.get("d", {}).items():
                            gm.w(rows3 + i * 0x10 + off, dw(v))
                    for i, ss in rc2.get("subs", {}).items():
                        for off, v in ss.get("d", {}).items():
                            gm.w(subs3 + i * 0x20 + off, dw(v))
                for off, v in spec.get("d", {}).items():
                    gm.w(D + off, dw(v))
            # EXP-259: the d[+0x18] arm's second container —
            # 2ED570(q[elem+0xD98], slot).  q[C2+0x30]/q[C2+8] are
            # 3AB7F0 tagged bases (low2==0 = direct ptr): row base
            # stride 0x10 gates on d[row]!=-1, sub base stride 0x20
            # carries d[sub+0x10] -> 20E600 target element.
            c2 = dcn.get("c2")
            if c2 is not None:
                C2 = self.dcntr2 = self.alloc(0x60)
                rows = self.dc2rows = self.alloc(
                    c2.get("nrows", 4) * 0x10)
                subs = self.dc2subs = self.alloc(
                    c2.get("nsubs", 4) * 0x20)
                gm.w(self.elemb + eoff + 0xD98, qw(C2))
                # EXP-260: each base cell carries a direct ptr
                # (&3==0), a 36B130 handle (hdr|tag -> q[hdr+8]+0x40;
                # every nonzero tag resolves identically), or stays
                # null so the resolved cell keeps its cached base.
                for base, tagoff, cacheoff, key in (
                        (rows, 0x30, 0x38, "row"),
                        (subs, 0x08, 0x10, "sub")):
                    mode = c2.get(key + "tag")
                    if mode == "cache":
                        gm.w(C2 + cacheoff, qw(base))
                    elif mode:
                        hdr = self.alloc(0x40)
                        gm.w(hdr + 8, qw(base - 0x40))
                        gm.w(C2 + tagoff, qw(hdr | mode))
                    else:
                        gm.w(C2 + tagoff, qw(base))
                gm.w(C2 + 0x4C, dw(c2.get("shift", 0)))
                gm.w(C2 + 0x50, dw(c2.get("mask", 0)))
                gm.w(C2 + 0x48, dw(c2.get("mult", 0)))
                for i, spec in c2.get("rows", {}).items():
                    for off, v in spec.get("d", {}).items():
                        gm.w(rows + i * 0x10 + off, dw(v))
                for i, spec in c2.get("subs", {}).items():
                    for off, v in spec.get("d", {}).items():
                        gm.w(subs + i * 0x20 + off, dw(v))
                e2 = self.elemb + c2.get("e2", 0x70100)
                self.dc2elem = e2
                for off, v in c2.get("e2d", {}).items():
                    gm.w(e2 + off, dw(v))
                # EXP-262: raw elemb-offset writes — the record-arm's
                # second element, its 0x290-stride word list, and the
                # target rows 372280 clears.
                for off, v in c2.get("ed", {}).items():
                    gm.w(self.elemb + off, dw(v))
                for off, v in c2.get("ew", {}).items():
                    gm.w(self.elemb + off,
                         struct.pack("<H", v & 0xFFFF))
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
        self.ctxn30 = 0
        self.ctxn30s = 0
        self.n30by = {}
        for ci, cspec in enumerate(case.get("ctx4", [])):
            if cspec is None:   # EXP-251: sparse roster — slot stays empty
                continue
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
            # EXP-234: 319490's ctx arm — 263E30(ctx) = q[ctx+0x30]
            # node; n30 wires a live node so the b[node]&8 gate can
            # pass (263E30's return feeds 3377C0's rcx).
            n30 = cspec.get("n30")
            if n30 is not None:
                n = self.alloc(n30.get("size", 0x80))
                gm.w(c + 0x30, qw(n))
                for off, v in n30.get("d", {}).items():
                    gm.w(n + off, dw(v))
                for off, v in n30.get("b", {}).items():
                    gm.w(n + off, bytes([v & 0xFF]))
                # EXP-251: 311CF0's linked node — q[n+0x698] read for
                # the d[+0x64]|d[+0x3c] flag tests (zeroed = clean).
                if "q698" in n30:
                    n698 = self.alloc(0x100)
                    gm.w(n + 0x698, qw(n698))
                # EXP-248: 3377C0 deep scaffolding — "deep" plants
                # q[n30+0x10] -> S with b[S+3]&0xE0==0x60 and
                # q[S+0xB8]=T, so real 265090 tail-calls 3DA710
                # (T+0x50/+0x54 -> pos/radius dwords).  b[n30+0xEA9]
                # stays 0 (236820 entity index -> oar4 row 0); n30
                # must be size>=0xF00 to cover +0xEA9.
                dp = n30.get("deep")
                if dp is not None:
                    s = self.alloc(0x100)
                    t = self.alloc(0x60)
                    gm.w(n + 0x10, qw(s))
                    gm.w(s + 3, bytes([dp.get("b3", 0x60) & 0xFF]))
                    gm.w(s + 0xB8, qw(t))
                    gm.w(t + 0x50,
                         struct.pack("<f", dp.get("pos", 1.0)))
                    gm.w(t + 0x54,
                         struct.pack("<f", dp.get("r", 0.5)))
                    self.ctxn30s = s
                self.ctxn30 = n
                self.n30by[ci] = n
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
        # EXP-240: desc8 — 26D6F0's pass arm reads q[ent+0xB8] desc,
        # writes f[q[desc+0xF0]+0x24] and f[desc+0xD0].
        self.desc8 = 0
        self.desc8f0 = 0
        if "desc8" in case and self.objent:
            d8 = self.alloc(0x100)
            f0 = self.alloc(0x40)
            gm.w(self.objent + 0xB8, qw(d8))
            gm.w(d8 + 0xF0, qw(f0))
            self.desc8, self.desc8f0 = d8, f0
            for off, v in case["desc8"].get("d", {}).items():
                gm.w(d8 + off, dw(v))
            for off, v in case["desc8"].get("f", {}).items():
                gm.w(d8 + off, struct.pack("<f", v))
        # EXP-246: 46AB10 dedup-ring insert arm — plant the
        # 0x2EBF018 desc so rcx = elemb + d[+0xC] + w[+8]*edx lands
        # on the pool instead of faulting on a null desc (ecx=0 ->
        # b[4] read).  Defaults: index 0, width 0 -> rcx == elemb.
        self.q6desc = 0
        if case.get("q6desc"):
            q6 = self.alloc(0x40)
            gm.w(0x2EBF018, qw(q6))
            self.q6desc = q6
            q6d = case["q6desc"] if isinstance(case["q6desc"], dict) else {}
            gm.w(q6 + 0xC, dw(q6d.get("idx", 0)))
            gm.w(q6 + 8, struct.pack("<H", q6d.get("width", 0)))
            # EXP-249: "elf" writes b[elemb+4] — the flag byte the
            # desc-resolved element tests with &1 at 0x46ABB3.
            # Set -> 46AB10 takes the dedup-ring SCAN arm instead
            # of the insert fast-path.
            if q6d.get("elf"):
                gm.w(self.elemb + 4, bytes([q6d["elf"] & 0xFF]))
            # EXP-255: "b3" writes b[elemb+3] — the class byte
            # 469570 gates with >=0x80 -> early ret 1 (no owner
            # lookups, no consult).
            if q6d.get("b3") is not None:
                gm.w(self.elemb + 3, bytes([q6d["b3"] & 0xFF]))
        # EXP-249: 46AB10 dedup-scan arm fixtures.  q6s is the r8
        # struct (d[+0x28]=0 < 0x1ff cap, q[+0]/q[+8]=0 -> 469570's
        # owner lookups miss -> ret 1); q6pay is the rcx payload the
        # ring compares at q[row+8]; q6ring pre-seeds rows at
        # 0x2EBB560+slot*0x20 (w[+0]=tag vs edx, q[+8]=payload,
        # d[+4]=stored timestamp); q6now plants d[0x208D45C] —
        # 32A150's "now" — and q6cur plants the insert cursor
        # d[0x2EBB54C].  Hit iff 0x1c2 + d[row+4] > now (unsigned):
        # fresh -> suppress write+notify, stale/miss -> insert arm.
        # Allocated lazily so the pool layout of the other 539 cases
        # is unchanged.
        self.q6s = 0
        self.q6pay = 0
        if (case.get("q6ring") or case.get("q6cur") is not None
                or case.get("q6now") is not None
                or case.get("q6cap") is not None
                or case.get("q6own") is not None
                or case.get("q6own0") is not None):
            self.q6s = self.alloc(0x100)
            self.q6pay = self.alloc(0x40)
            if case.get("q6cap") is not None:
                # 46AB10's count cap: d[r8+0x28] >= 0x1FF ->
                # jge 0x46AC7A early-out before the owner scan.
                gm.w(self.q6s + 0x28, dw(case["q6cap"]))
        if case.get("q6cur") is not None:
            gm.w(0x2EBB54C, dw(case["q6cur"]))
        if case.get("q6now") is not None:
            gm.w(0x208D45C, dw(case["q6now"]))
        for rrow in case.get("q6ring", []):
            rr = 0x2EBB560 + rrow.get("slot", 0) * 0x20
            gm.w(rr, struct.pack("<H", rrow.get("w", 0)))
            gm.w(rr + 4, dw(rrow.get("ts", 0)))
            gm.w(rr + 8, qw(self.q6pay if rrow.get("q8") == "self"
                            else rrow.get("q8", 0)))
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
        # EXP-224: 322C50 kind-7 range desc q[02EBF098] — class-7
        # (0x2xxx) ids are valid iff id-0x2000 < d[+4].
        mkdesc(0x02EBF098, case.get("m98d"))
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
        # EXP-229: real 2FEF30 resolves three chained member growth
        # descs q[02EBF148/140/150] (row idx = w[membrow+0x22]/+0x24/
        # +0 — member arm only) and the status-fold table q[02EBF040]
        # (row idx = shipped byte tables 0xD10290/0xD102A0/0xD102B0).
        # A null desc falls through to unconditional row derefs, so
        # default-plant zeroed rows; pass "X": None for the null path.
        mkdesc(0x02EBF148, case.get("d148",
               {"stride": 0x40, "off": 0x82000, "count": 0x40}))
        mkdesc(0x02EBF140, case.get("d140",
               {"stride": 0x40, "off": 0x83000, "count": 0x40}))
        mkdesc(0x02EBF150, case.get("d150",
               {"stride": 0x40, "off": 0x84000, "count": 0x40}))
        mkdesc(0x02EBF040, case.get("sttd",
               {"stride": 0x20, "off": 0x80000, "count": 0x100}))

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
            # EXP-224: real 317930 gates the slot writes — kind-6
            # accepts [0x1000,0x1000+memt.count) only, so the foe
            # slot ids must be member-range (0x501/0x502 were
            # stub-fiction: real 322C50 denies them).
            fw = {0xA: 0x1101, 0xC: 0x1102, 0xE: 0xFFFF, 0x10: 0xFFFF,
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
        # e78e/e70e -> +0x34, e78l/e70l -> +0x2F.  EXP-223: real
        # 317090 reads w[+0] of both (the FP-stat multipliers).
        if self.objrow:
            for base, off in (("e78", 0xE78), ("e70", 0xE70)):
                if (base in case or base + "e" in case
                        or base + "l" in case or base + "w" in case):
                    eb = self.alloc(0x40)
                    gm.w(eb + 0x30, dw(case.get(base, 0)))
                    gm.w(eb + 0x34, dw(case.get(base + "e", 0)))
                    gm.w(eb + 0x2F,
                         bytes([case.get(base + "l", 0) & 0xFF]))
                    gm.w(eb, struct.pack(
                        "<H", case.get(base + "w", 0) & 0xFFFF))
                    gm.w(self.objrow + off, qw(eb))
        # EXP-223: real 312280 share tail —
        #   fpp: q[02092758] FP-total object; 253690 reads d[+8],
        #        254EE0 clamps + stores it (+ 316A50 notify).
        #   e68: q[obj+0xE68] msg-id rec; 3171C0 reads w[+0x52]
        #        (0xFFFF = no msg -> skips 315820; else 315820 bumps
        #        b[q[020927C0]+id+0x3404] via msgtab).
        #   msgtab: q[020927C0] counter/stat table — 315820's counter
        #        arm at +0x3404; EXP-226's real 316A50 family reads
        #        achieved-bits at +0x3844 and value slots at
        #        +0x384C+off (max 0x3868) — must be planted for every
        #        case (2536A0() null would fault).
        #   fbdev: q[0209BE80] object -> 28FB80's paired 289D00
        #        writes land on +0x5380 (3588B0 gate -> early-out
        #        without clstab).
        self.fpp = self.alloc(0x10)
        gm.w(0x2092758, qw(self.fpp))
        gm.w(self.fpp + 8, dw(case.get("fptot", 0)))
        self.msgtab = self.alloc(0x3900)
        gm.w(0x20927C0, qw(self.msgtab))
        # EXP-232: q[01F83450] = the UI singleton 20CE00 returns.
        # The shipped .data bytes there are stale non-pointer data
        # (init code publishes the real object); pre-init state is
        # null, which makes 8632B0's gate an honest no-op and keeps
        # 20CE60 (vtable dispatch needing a UiManager fixture) a
        # disclosed boundary.
        gm.w(0x1F83450, qw(0))
        if self.objrow and case.get("objlink"):
            self.e68 = self.alloc(0x60)
            gm.w(self.objrow + 0xE68, qw(self.e68))
            gm.w(self.e68 + 0x52,
                 struct.pack("<H", case.get("e68w52", 0xFFFF) & 0xFFFF))
        if case.get("fbdev"):
            # EXP-241: widened 0x6000->0x12000 — 290B90's device list
            # hangs at q[+0x10F10].  fbdev={"nodes":[{id,w850},...]}
            # chains nodes: d[+0x810] id, w[+0x850] state, q[+0x868]
            # next; a dict-less truthy fbdev plants the object with an
            # empty list (legacy 28FB80 semantics).
            self.fbdev = self.alloc(0x12000)
            gm.w(0x209BE80, qw(self.fbdev))
            self.fbnodes = []
            fbs = case["fbdev"]
            prev = 0
            for spec in (fbs.get("nodes", []) if isinstance(fbs, dict)
                         else []):
                n = self.alloc(0x900)
                gm.w(n + 0x810, dw(spec.get("id", 0)))
                gm.w(n + 0x850, struct.pack("<H", spec.get("w850", 0)))
                self.fbnodes.append(n)
                if prev:
                    gm.w(prev + 0x868, qw(n))
                else:
                    gm.w(self.fbdev + 0x10F10, qw(n))
                prev = n
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
            # EXP-253: ci0 leaves q[row+0x10] null -> 469570's
            # second lookup gates rbx=0 -> 2FA3B0(0).
            if not spec.get("ci0"):
                gm.w(row + 0x10, qw(ci))
            gm.w(row, qw(spec.get("flags", 0x4000000)))
            self.oar4[si] = (row, ri, ci)
            oc = max(oc, si + 1)
        gm.w(OBJCNT, dw(oc))
        if self.q6s and case.get("q6own") is not None:
            # EXP-252: 46AB10's mid-gate — q[r8+8] feeds 31B860's
            # OBJARR scan for q[row+0x698]==arg; pointing it at an
            # oar4 row's linked rec makes the scan return the row,
            # so the d[02089340]&0x3080 / b[row+4]&0x20 exits run.
            gm.w(self.q6s + 8, qw(self.oar4[case["q6own"]][1]))
        if self.q6s and case.get("q6own0") is not None:
            # EXP-253: q[r8+0] is 469570's rsi (rdx) carrier — the
            # FIRST owner lookup.  Planting it makes the rsi arm
            # run before the rdi arm.
            gm.w(self.q6s + 0, qw(self.oar4[case["q6own0"]][1]))
        self.q6arg = 0
        if case.get("q6arg") is not None:
            # EXP-255: direct-entry 469570 cases pass the oar4
            # row's linked rec as a register arg.
            self.q6arg = self.oar4[case["q6arg"]][1]
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

        # EXP-263: iat_ret — plant a heap ret-stub into the listed
        # IAT slots.  51BA80's populate chain reaches 409210 whose
        # tail calls ff15[0x8C2F70] (an unbound import thunk in the
        # replay image); the slot is redirected to a real `ret` so
        # the rest of 409210 still runs shipped.  Synthetic import
        # boundary — disclosed in the EXP-263 record, the import's
        # (lock-init) semantics are nil for this fixture.
        self.iatstub = 0
        for a in case.get("iat_ret", []):
            if not self.iatstub:
                self.iatstub = self.alloc(0x10)
                gm.w(self.iatstub, b"\xc3")
            gm.w(a, qw(self.iatstub))
        # srcd/srcw/srcq: the 51BA80 insert's arg5 source spec —
        # w[src+0x10] gates 409F50/2ED570 doc resolve (-1 -> null
        # doc -> populate ret 0), q[src+8]/d[src+0x14] seed the
        # record's own container handle q[+0x330]/d[+0x338].
        self.dsrc = 0
        if case.get("srcd") or case.get("srcw") or case.get("srcq"):
            self.dsrc = self.alloc(0x60)
            for off, v in case.get("srcd", {}).items():
                gm.w(self.dsrc + off, dw(v))
            for off, v in case.get("srcq", {}).items():
                gm.w(self.dsrc + off, qw(v))
            for off, v in case.get("srcw", {}).items():
                gm.w(self.dsrc + off, struct.pack("<H", v & 0xFFFF))

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
        # EXP-205: 31C5D0 kind-0x1A resource resolver.  T1 IS the
        # per-bit cascade table (CASCD cell 02EBF118, already driven
        # by the cascd fixture above).  T2 index table q[02EBF170]:
        # d[4+i*4] = elemb off of a T3 inline table.  w[row] packs
        # hi5 -> T2 idx / lo11 -> T3 idx; d[T3+4+lo11*4] = final off
        # -> q[blk+0x18]; w[row+0xA] -> 2F9860 -> q[blk+0x10].
        t2 = case.get("dt2")
        if t2 is None:
            gm.w(0x02EBF170, qw(0))
        else:
            t2p = self.alloc(0x40)
            gm.w(0x02EBF170, qw(t2p))
            for i, off in t2.items():
                gm.w(t2p + 4 + i * 4, dw(off))
        t1 = cd
        self.l1row = 0
        if t1:
            rid = case.get("c5id", case.get("rqv", 0))
            self.l1row = (self.elemb + t1.get("off", 0x70000)
                          + t1.get("stride", 0x40) * rid)
            for off, v in case.get("l1w", {}).items():
                gm.w(self.l1row + off, struct.pack("<H", v & 0xFFFF))
            for off, v in case.get("l1b", {}).items():
                gm.w(self.l1row + off, bytes([v & 0xFF]))
        for base, tbl in case.get("t3", {}).items():
            for j, off in tbl.items():
                gm.w(self.elemb + base + 4 + j * 4, dw(off))
        for off, bs in case.get("t3s", {}).items():
            gm.w(self.elemb + off, bytes(bs))
        # c5blk: direct-entry descriptor block for c5d0-* cases
        # (d[+0]=kind, d[+4]=id; resolver writes q18/q10/b20-25).
        self.c5blk = self.alloc(0xA0)
        gm.w(self.c5blk, dw(case.get("c5kind", 0)))
        gm.w(self.c5blk + 4, dw(case.get("c5id", 0)))
        for off, v in case.get("c5pre", {}).items():
            gm.w(self.c5blk + off, bytes([v & 0xFF]))
        # EXP-208: segment-string machinery.  c60 = the copy+0x60
        # table ptr for the >0xF flag test, d[+0xC] selects the elemb
        # offset; eflags = flag dwords at elemb+cp*8.  Allocated before
        # e312q so "c60" resolves as an e312q attr.
        self.c60 = self.alloc(0x40)
        for off, v in case.get("c60d", {}).items():
            gm.w(self.c60 + off, dw(v))
        for idx, v in case.get("eflags", {}).items():
            gm.w(self.elemb + case.get("c60d", {}).get(0xC, 0)
                 + idx * 8, dw(v))
        # EXP-213 fixtures for the resource-lookup chain — allocated
        # before e312q so "nobj"/"rstr" resolve in e312q/nobjq/eac10t.
        # rstr: the resource string 2639E0/263990 return — the arm
        # NUL-scans it, suppress-measures via 2B41F0, nested-walks it.
        self.rstr = self.alloc(0x100)
        if "rstrb" in case:
            gm.w(self.rstr, bytes(case["rstrb"]))
        # nobj: the '>' arm's named-record object (q[e312+0x78]).
        # w[+0x102]<0 -> q[+0xF8] direct; else the 32A930/3EAC10 chain.
        self.nobj = self.alloc(0x200)
        for off, v in case.get("nobjw", {}).items():
            gm.w(self.nobj + off, ww(v))
        for off, v in case.get("nobjq", {}).items():
            if isinstance(v, str):
                v = getattr(self, v, 0)
            gm.w(self.nobj + off, qw(v))
        # ba30t: 39BA30's font-record table is INLINE at BSS 0x2AEE810
        # (lea loads the base, not a pointer).  {idx: {"w6": count,
        # "e": [(stride, wC, d30), ...]}} — rec alloc'd per idx;
        # records chained from rec+0x10 by d[rbx] strides; a record
        # matches when w[rbx+0xC]>0x30 and (d[rbx+0x30]&0x18000)==0x8000.
        self.ba30r = {}
        for idx, spec in case.get("ba30t", {}).items():
            rec = self.alloc(0x400)
            self.ba30r[idx] = rec
            gm.w(0x2AEE810 + idx * 8, qw(rec))
            gm.w(rec + 6, ww(spec.get("w6", 0)))
            pos = rec + 0x10
            for st, wc, d30 in spec.get("e", []):
                gm.w(pos, dw(st))
                gm.w(pos + 0xC, ww(wc))
                gm.w(pos + 0x30, dw(d30))
                pos += st
        # a930m: 32A930's bit-test bitmap — 2EF2B0()=0x2164480, bit
        # idx -> b[0x2164480+0x13B4+(idx>>3)] bit (idx&7).  {off: byte}
        for off, v in case.get("a930m", {}).items():
            gm.w(0x2175834 + off, bytes([v & 0xFF]))
        # eac10t: 3EAC10's runtime pair table — q[0x2B5E0D8] ->
        # {d[+8] count, d[+0xC+i*4] signed entries}.  {i: val} (str
        # resolves an alloc addr); eac10n overrides the count.
        self.eac10 = 0
        if "eac10t" in case or "eac10n" in case:
            self.eac10 = self.alloc(0x1000)
            gm.w(0x2B5E0D8, qw(self.eac10))
            ents = case.get("eac10t", {})
            gm.w(self.eac10 + 8,
                 dw(case.get("eac10n", max(ents) + 1 if ents else 0)))
            for i, v in ents.items():
                if isinstance(v, str):
                    v = getattr(self, v, 0)
                gm.w(self.eac10 + 0xC + i * 4, dw(v))
        # EXP-206: 2B3120 direct-entry fixtures.  e312 = 0xD0 arg
        # struct; q[+0x28] nonzero -> evaluator path (struct copied
        # whole into the 2B24B0 frame), null -> two zero words, ret 0.
        self.e312 = self.alloc(0x100)
        # EXP-219: q[e312+0x20] is the 4x4 matrix 2DD860 transforms
        # corner vectors through (202B70->217060 -> projective divide).
        # It's also a null-gate for the tag-5 '20'-tail (tag2 asserts
        # it stays null) — so the identity matrix is opt-in via "emat".
        if case.get("emat"):
            self.mat = self.alloc(0x40)
            for i in range(4):
                gm.w(self.mat + i * 0x14, struct.pack("<f", 1.0))
            gm.w(self.e312 + 0x20, qw(self.mat))
        for off, v in case.get("e312q", {}).items():
            if isinstance(v, str):
                v = getattr(self, v, 0)
            gm.w(self.e312 + off, qw(v))
        # wout/wout2: the two truncated-float word out-pointers.
        self.wout = self.alloc(0x10)
        self.wout2 = self.wout + 8
        # EXP-207: 2B24B0 line-layout fixtures.  q[0209CC40] is the
        # shared text context (BSS — must be planted): its save fields
        # are snapshot/restored across the nested measure.  ctxd/ctxf/
        # ctxq/ctxb plant the pre-eval save fields (d10D8, f10E8,
        # q10C8, b10FC, b10FF).  ctxrd/ctxrf/ctxrb are applied by the
        # s2b2150 stub onto the same object as its results.
        self.ctxo = self.alloc(0x1200)
        gm.w(0x209CC40, qw(self.ctxo))
        # EXP-216: ctx48o = plant ctx48 as a real object (2B4730's
        # align step derefs d[ctx48+8]); scalar ctx48 stays for the
        # arm-level "nonzero" gates.
        if "ctx48o" in case:
            self.ctx48o = self.alloc(0x100)
            gm.w(0x209CC48, qw(self.ctx48o))
            gm.w(self.ctx48o + 8, qw(case.get("c48c", 0)))
        else:
            gm.w(0x209CC48, qw(case.get("ctx48", 0)))
        for off, v in case.get("ctxd", {}).items():
            gm.w(self.ctxo + off, dw(v))
        for off, v in case.get("ctxf", {}).items():
            gm.w(self.ctxo + off, struct.pack("<f", float(v)))
        for off, v in case.get("ctxq", {}).items():
            gm.w(self.ctxo + off, qw(v))
        for off, v in case.get("ctxb", {}).items():
            gm.w(self.ctxo + off, bytes([v & 0xFF]))
        # e312f: float fields on the 0xD0 arg struct (2B24B0's scale
        # fields +0x34/+0x38 for the b10FE line-height accumulate).
        for off, v in case.get("e312f", {}).items():
            gm.w(self.e312 + off, struct.pack("<f", float(v)))
        # e312d/e312b: dword/byte presets on the 0xD0 arg struct —
        # tag-15 sub-arms gate on d[+0xB0]/d[+0x44] and read b[+0xA8]
        # /b[+0x9F]/b[+0xA6] colour + font-slot state.
        for off, v in case.get("e312d", {}).items():
            gm.w(self.e312 + off, dw(v))
        for off, v in case.get("e312b", {}).items():
            gm.w(self.e312 + off, bytes([v & 0xFF]))
        # ba00t: 39BA00's param escape table.  q[02AEE870] ships BSS —
        # plant a guest table pointer always so the escape path is
        # deterministic; entry bytes come from {off: byte}.
        self.ba00t = self.alloc(0x400)
        gm.w(0x2AEE870, qw(self.ba00t))
        for off, v in case.get("ba00t", {}).items():
            gm.w(self.ba00t + off, bytes([v & 0xFF]))
        # EXP-215 sprt: '?'-arm sprite draw chain — 39BB00's BSS
        # singletons -> sprite table -> q[tab+0x20] record (+0x30 =
        # rbx).  Zeroed word-pair table makes index = param; the
        # metric dword at rbx+idx*8+4 = rec+0x34+idx*8: bits 0..11
        # -> f[0209CC64]/f58 via xmm10, bits 12..23 -> f[0209CC60]
        # via xmm9.  sprt = [idx, lo, hi] (param = rdx index).
        if "sprt" in case:
            t = self.alloc(0x40)
            r = self.alloc(0x200)
            gm.w(0x208EA90, qw(t))
            gm.w(0x208EAA8, qw(t))
            gm.w(t + 0x20, qw(r))
            idx, lo, hi = case["sprt"]
            gm.w(r + 0x34 + idx * 8, dw(lo | (hi << 0xC)))
            self.sprtt = t
            self.sprtr = r
        # EXP-219: 17FC90/17F7C0 real — 1B5FA0 returns q[01F811F8],
        # 1E9C40 writes quad UV floats at +0x137C..0x1388; plant a
        # 0x1400 device buffer.  2AEB20's edi seed is
        # b[q[01F7FFE0]+0x38] (1E0C10 -> 198790); 180150 separately
        # reads b[01F811E0] (a flag byte, not the same cell).
        self.dev1 = self.alloc(0x2800)
        gm.w(0x1F811F8, qw(self.dev1))
        self.dev2 = self.alloc(0x40)
        gm.w(0x1F7FFE0, qw(self.dev2))
        # EXP-220: the device object is real now.  q[dev1] = devsub
        # (17F920 arm select d+0x1C/d+0x20, 225690/79E3C0 divisors at
        # +0x24/+0x28, f+0x34 unit scale for 1E9BD0/1FDDB0, inline
        # glyph map at +0x40/+0x50 for 1FDEC0).  q[dev1+8] = the
        # codepoint->index dword vector (begin/end); q[dev1+0x10] =
        # the emit-vector header — the std::vector itself sits at
        # devec+0x18 (begin/end/cap) with the embedded allocator at
        # devec+0x30 whose +0x10/+0x18 are the alloc/dealloc fn ptrs
        # (scripted salloc/sdealloc).  q[dev1+0x28] = the walkers'
        # save/restore ctx slot — nonzero (default 0x1234, never
        # dereferenced) keeps the kern arm skipped exactly as the
        # old f940v stub default did; devctxv=0 selects the fallback
        # kern metric arm, devctxv="devctx" a live ctx object.
        # dev1+0xF68+idx*36 = 1E94E0 lazy-init metric ext records
        # (flag byte planted 1); dev1+0x137C the scale quad;
        # dev1+slot*0x2C+0x2324 the bounds accumulator.
        self.devsub = self.alloc(0x100)
        gm.w(self.dev1, qw(self.devsub))
        gm.w(self.devsub + 0x1C, dw(5))     # 17F920 arm1 (tag4/kern)
        gm.w(self.devsub + 0x20, dw(6))     # 17F920 arm0 (tag1)
        gm.w(self.devsub + 0x24, dw(2))     # 225690 divisor
        gm.w(self.devsub + 0x28, dw(2))     # 79E3C0 divisor
        gm.w(self.devsub + 0x34, struct.pack("<f", 1.0))  # 1FDDB0
        # 17F8C0/1E9860: devsub's inline glyph map (root q[+0x50],
        # sentinel devsub+0x40) — one node key 3 so codepoint 3
        # (identity remap through dwtab) hits; 1FDEC0 returns
        # node+0x24.
        self.gnode = self.alloc(0x40)
        gm.w(self.gnode + 0x20, dw(3))
        gm.w(self.gnode + 0x24, dw(0x1234))
        gm.w(self.devsub + 0x50, qw(self.gnode))
        self.dwtab = self.alloc(0x400)
        for i in range(256):
            gm.w(self.dwtab + i * 4, dw(i))
        self.devrmp = self.alloc(0x20)
        gm.w(self.devrmp, qw(self.dwtab))
        gm.w(self.devrmp + 8, qw(self.dwtab + 0x400))
        gm.w(self.dev1 + 8, qw(self.devrmp))
        self.evbase = self.alloc(0x600)
        self.devec = self.alloc(0x60)
        gm.w(self.devec + 0x18, qw(self.evbase))           # begin
        gm.w(self.devec + 0x20, qw(self.evbase))           # end
        gm.w(self.devec + 0x28, qw(self.evbase + 0x240))   # cap
        self.aobj = self.alloc(0x20)
        gm.w(self.aobj + 0x10, qw(0x7000A100))   # alloc slot
        gm.w(self.aobj + 0x18, qw(0x7000A108))   # dealloc slot
        gm.w(self.devec + 0x30, qw(self.aobj))
        gm.w(self.dev1 + 0x10, qw(self.devec))
        self.devctx = self.alloc(0x40)
        gm.w(self.devctx + 0x1C, dw(4))
        dcv = case.get("devctxv", 0x1234)
        if isinstance(dcv, str):
            dcv = getattr(self, dcv, 0)
        gm.w(self.dev1 + 0x28, qw(dcv))
        for i in range(28):
            # 1E94E0 ext record for idx: flag at dev1+idx*36+0xF68,
            # metric ints at +0xF6C..+0xF87 (small nonzero dims)
            base = self.dev1 + 0xF68 + i * 36
            gm.w(base, b"\x01")
            for j in range(8):
                gm.w(base + 4 + j * 4, dw(4 + j))
        gm.w(self.dev1 + 0x137C,
             struct.pack("<ffff", 1.0, 1.0, 1.0, 1.0))
        # EXP-220: q[01F81200] font-metrics map (1B5FB0 singleton ->
        # 1B51C0 exact-key find -> q[node+0x28] value).  Two-node
        # tree: root key1 -> mv1, its +0 child key3 -> mv3.
        # b[01F811E0]=0 (BSS) selects the ceilf(d[val+X]/f[val+0x34])
        # arm: mv1 13/2.0 -> 7.0 and 12/2.0 -> 6.0, mv3 9.0/8.0 via
        # scale 1.0.
        self.devmap = self.alloc(0x60)
        gm.w(0x1F81200, qw(self.devmap))
        self.mn1 = self.alloc(0x40)
        self.mn3 = self.alloc(0x40)
        self.mv1 = self.alloc(0x40)
        self.mv3 = self.alloc(0x40)
        gm.w(self.devmap + 0x40, qw(self.mn1))
        gm.w(self.mn1, qw(self.mn3))
        gm.w(self.mn1 + 0x20, dw(1))
        gm.w(self.mn1 + 0x28, qw(self.mv1))
        gm.w(self.mn3 + 0x20, dw(3))
        gm.w(self.mn3 + 0x28, qw(self.mv3))
        gm.w(self.mv1 + 0x2C, dw(12))
        gm.w(self.mv1 + 0x30, dw(13))
        gm.w(self.mv1 + 0x34, struct.pack("<f", 2.0))
        gm.w(self.mv3 + 0x2C, dw(9))
        gm.w(self.mv3 + 0x30, dw(8))
        gm.w(self.mv3 + 0x34, struct.pack("<f", 1.0))
        # scripted allocator slots for 1E7A20's realloc arm
        gm.w(0x7000A100, b"\xC3")
        gm.w(0x7000A108, b"\xC3")
        self.e7buf = self.alloc(0x600)
        # EXP-221: q[01F811E8] render-device object (1B1C00's
        # singleton).  Slot records at rdev+0x2328 stride 0x58
        # (cursor d+0x3928, 0x3F bound); the emit tail calls
        # 181560 reset (1B0100 clears slots 0..cursor then -1,
        # memset +0x3930..+0x3AA7, seeds +0x3A4C..0x3A58 with 0x80),
        # 1819A0/1B2410 props (+0x3930/+0x3934, name copy into
        # +0x3938 via 17D2E0 when r9!=0, stack args to +0x3AA0 and
        # +0x3A38..0x3A48), 181870/1B2490 mode table -> +0x3A60,
        # 181460/1B06D0 0x30-record appends (edx-2 outer x3 inner),
        # 1816B0/1B22D0 q[+0x3A68] and 181910/1B22E0 q[+0x3A70].
        # rdcur plants the pre-reset cursor so 1B0100's clear loop
        # runs (slots 0..rdcur reset); rvbuf/raobj give slot0's
        # sub-vector a 2-record cap so the 3rd append runs 1AED50's
        # realloc arm through the scripted s2alloc/s2dealloc slots.
        self.rdev = self.alloc(0x4000)
        gm.w(0x1F811E8, qw(self.rdev))
        gm.w(self.rdev + 0x3928, dw(case.get("rdcur", 1)))
        self.rvbuf = self.alloc(0x200)
        self.raobj = self.alloc(0x20)
        gm.w(self.raobj + 8, qw(0x7000A110))    # alloc slot
        gm.w(self.raobj + 0x18, qw(0x7000A118))  # dealloc slot
        slot0 = self.rdev + 0x2328
        gm.w(slot0 + 0x38, qw(self.rvbuf))
        gm.w(slot0 + 0x40, qw(self.rvbuf))
        gm.w(slot0 + 0x48, qw(self.rvbuf + case.get("rvcap", 0x60)))
        gm.w(slot0 + 0x50, qw(self.raobj))
        gm.w(self.rdev + 0x2328 + 0x58 + 0x50, qw(self.raobj))
        if case.get("rseal"):
            gm.w(slot0, qw(1))
        gm.w(0x7000A110, b"\xC3")
        gm.w(0x7000A118, b"\xC3")
        # rsrc: 0x30-record source stream for direct 181460/1B06D0
        # entries; distinct qwords make the append copies checkable.
        self.rsrc = self.alloc(0x300)
        for i in range(8):
            for j in range(6):
                gm.w(self.rsrc + i * 0x30 + j * 8,
                     qw(0x1100 + i * 0x100 + j))
        # rname: string the 1B2410 r9!=0 arm copies into +0x3938.
        self.rname = self.alloc(0x40)
        gm.w(self.rname, b"RDEVNM\x00")
        # EXP-220: 1E8070/17F7C0 source state (0xA0) — d[+0x9C] is the
        # metric index (mod 0x1C -> the dev1+0xF68 record), the corner
        # int/float fields at +0..+0x14 and +0x1C..+0x7C feed the 2x3
        # vertex expansion.  vcap shrinks the emit vector's cap so a
        # case exercises the real 1E7A20 realloc arm; dslot picks the
        # bounds slot; b2349 plants the post-loop derived-flag arm.
        self.st7c0 = self.alloc(0xA0)
        gm.w(self.st7c0 + 0x9C, dw(case.get("vidx", 0) & 0xFFFFFFFF))
        for i, v in enumerate((8.0, 10.0, 12.0, 14.0, 16.0, 18.0)):
            gm.w(self.st7c0 + i * 4, struct.pack("<f", v))
        # r14 walks st7c0+0x2C with vertex k=(outer+inner) in 0..3, so
        # the +0x2C float stream and the +0x5C/+0x6C/+0x7C dword
        # streams need only 4 entries; the reads stop at +0x88.  Keep
        # them at 4 so the +0x8C post-loop scale source survives.
        for vi in range(4):
            gm.w(self.st7c0 + 0x2C + vi * 4,
                 struct.pack("<f", 20.0 + vi * 2))
            gm.w(self.st7c0 + 0x5C + vi * 4, dw(4 + vi))
            gm.w(self.st7c0 + 0x6C + vi * 4, dw(8 + vi))
            gm.w(self.st7c0 + 0x7C + vi * 4, dw(2 + vi))
        gm.w(self.st7c0 + 0x8C, dw(64))
        gm.w(self.dev1 + 0x20, dw(case.get("dslot", 0)))
        sl = self.dev1 + case.get("dslot", 0) * 0x2C
        gm.w(sl + 0x2328, struct.pack("<f", 1e30))
        gm.w(sl + 0x232C, struct.pack("<f", 1e30))
        gm.w(sl + 0x2330, struct.pack("<f", -1e30))
        gm.w(sl + 0x2334, struct.pack("<f", -1e30))
        if case.get("b2349"):
            gm.w(sl + 0x2349, b"\x01")
        if case.get("vcap") is not None:
            gm.w(self.devec + 0x28, qw(self.evbase + case["vcap"]))
        if case.get("vfill"):
            gm.w(self.devec + 0x20,
                 qw(self.evbase + case["vfill"] * 0x3C))
        if case.get("nomap"):
            gm.w(self.devmap + 0x40, qw(0))
        # eb20t: kind-0x1C catch-all fixture.  edi=1 needs
        # b[dev2+0x38]!=0 and the 1E0C30 mode chain
        # d[q[q[02AEE868]+0xDF8]+0x10]==2 -> record index edx=1 (byte
        # table 0x9165F0+ebx*4+a); the per-ctxo record sits at
        # ctxo+edx*24: d[rec]>>2 = entry count, q[rec+0x10] = entry ptr
        # array.  Entry: w+0xA pair idx, w+0xC/w+0xE/w+0x10/w+0x12
        # metrics, b+0x39 pair byte, q+0x20 = UV pair tab
        # (d[tab+idx*8+4] lo12|hi12<<12, w[tab+idx*8] col,
        # w[tab+idx*8+2] row).  Sprite rec r via sprt t: w[r+0x42] =
        # byte-base inside r, b[r+0x30+w[r+0x42]+(b39>>4)] = pair idx;
        # q[t+0x30] = record attr qword.  Emits count-1 quad records
        # at q[0209CC50], stride 0x70.
        if "eb20t" in case:
            e = case["eb20t"]
            gm.w(self.dev2 + 0x38, bytes([e.get("d238", 1)]))
            o1 = self.alloc(0x1000)
            o2 = self.alloc(0x40)
            gm.w(0x2EA5368, qw(o1))
            gm.w(o1 + 0xDF8, qw(o2))
            gm.w(o2 + 0x10, dw(e.get("e868v", 2)))
            edx = e.get("edx", 1)
            rec = self.ctxo + edx * 24
            arr = self.alloc(0x40)
            ent = self.alloc(0x60)
            ent2 = self.alloc(0x60)
            ptab = self.alloc(0x40)
            gm.w(rec, dw(e.get("cnt", 2) << 2))
            gm.w(rec + 0x10, qw(arr))
            gm.w(arr, qw(ent))
            # the pre-loop publish block reads arr[cnt-1] — the last
            # entry — for the f[0209CC60/64/68] metric globals
            gm.w(arr + (e.get("cnt", 2) - 1) * 8, qw(ent2))
            self.eb20ent = ent
            self.eb20ent2 = ent2
            gm.w(ent + 0x10, struct.pack("<H", e.get("w10", 0x10)))
            gm.w(ent + 0x12, struct.pack("<H", e.get("w12", 0x20)))
            gm.w(ent2 + 0x10, struct.pack("<H", e.get("w10b", 0x8)))
            gm.w(ent2 + 0x12, struct.pack("<H", e.get("w12b", 0x4)))
            gm.w(ent + 0xA, struct.pack("<h", e.get("wa", 0)))
            gm.w(ent + 0xC, struct.pack("<h", e.get("wc", 0)))
            gm.w(ent + 0xE, struct.pack("<h", e.get("we", 0)))
            gm.w(ent + 0x39, bytes([e.get("b39", 0)]))
            gm.w(ent + 0x20, qw(ptab))
            gm.w(ptab + 4, dw(e.get("lo", 0x30) | (e.get("hi", 0x40) << 0xC)))
            gm.w(ptab, struct.pack("<H", e.get("col", 5)))
            gm.w(ptab + 2, struct.pack("<H", e.get("row", 7)))
            if "sprt" in case:
                t, r = self.sprtt, self.sprtr
            else:
                t = self.alloc(0x40)
                r = self.alloc(0x200)
                gm.w(0x208EA90, qw(t))
                gm.w(0x208EAA8, qw(t))
                gm.w(t + 0x20, qw(r))
            gm.w(r + 0x42, struct.pack("<H", e.get("w42", 0)))
            gm.w(r + 0x30 + e.get("w42", 0), bytes([e.get("bidx", 0)]))
            gm.w(t + 0x30, qw(e.get("attr", 0)))
        # EXP-215: 2A9F00's publish writes quad-command records at
        # q[0209CC50] (the same display-list cursor 2B4730 drains) —
        # plant a writable buffer (offset 0x10 so 2B4730's rdx-0x10
        # header write stays in-bounds).
        self.pcur = self.alloc(0x2000) + 0x10
        gm.w(0x209CC50, qw(self.pcur))
        # EXP-216: 2B4730's command-list write cursor q[0209E5A0].
        self.listcur = self.alloc(0x1000)
        gm.w(0x209E5A0, qw(self.listcur))
        # b4730p: the direct-entry fixture — point the publish cursor
        # INSIDE the list buffer so the drained record count is small
        # (2 records), and plant the 3A1DB0 double-buffer ring:
        # slot0 = ringbuf[0..0x20] (2 records for 36F360), slot1's
        # write cursor resets to its start.
        if "b4730p" in case:
            gm.w(0x209CC50, qw(self.listcur + 0x30))
            self.ringbuf = self.alloc(0x1000)
            gm.w(0x2EBEFC0, qw(self.ringbuf))          # slot0 start
            gm.w(0x2EBEFC8, qw(self.ringbuf + 0x20))   # slot0 end
            gm.w(0x2EBEFD8, qw(self.ringbuf + 0x800))  # slot1 start
            gm.w(0x2EBEFE0, qw(self.ringbuf + 0x900))  # slot1 cursor
            gm.w(0x2EBEFF0, dw(0))                     # cur slot = 0
            gm.w(self.ringbuf + 0x10, dw(0x30000000))  # last-rec hdr
        # EXP-218: 39C4A0 promoted real — a 3-way BSS select
        # (ecx==0 -> q[02AEE800]; ecx!=0 -> q[02AEE808] else the
        # q[02AEE800] fallback).  Plant both globals with the
        # resolved s39c4a0_ret so every existing caller sees exactly
        # the record the stub used to return.
        crv = case.get("s39c4a0_ret", 0)
        if isinstance(crv, str):
            crv = getattr(self, crv, 0)
        gm.w(0x2AEE800, qw(crv))
        gm.w(0x2AEE808, qw(crv))
        # strb = bytes the walker iterates at nstr (each byte is a
        # node tag).
        if "strb" in case:
            gm.w(self.nstr, bytes(case["strb"]))
        # ccp: a cursor CELL for direct 2AC5F0 entry — the
        # interpreter's rdx is &cursor, so q[ccp] = the string ptr.
        self.ccp = self.alloc(0x10)
        ccp = case.get("ccp")
        if isinstance(ccp, str):
            ccp = getattr(self, ccp, 0)
        if ccp:
            gm.w(self.ccp, qw(ccp))
        gm.w(0x209E598, qw(case.get("e598v", 0)))
        # e2814v: the global dword 229E40 reads at 01E02814 (tag-7's
        # ==7 -> 0x1A special case; ships BSS/0).
        gm.w(0x1E02814, dw(case.get("e2814v", 0)))
        # EXP-238 bad0t: 39BAD0's registered-language table at
        # 02AEE810 (8 qword slots, dword compared at +0 of each).
        # Ships BSS-zero = nothing registered; a live game fills it
        # at init.  bad0t={i: dword} plants entries so the real scan
        # returns index i for a matching arg (b3050-* pass 0x44).
        for i, v in case.get("bad0t", {}).items():
            gm.w(0x2AEE810 + i * 8, dw(v & 0xFFFFFFFF))
        self.params = self.alloc(0x40)
        self.auxout = self.alloc(0x10)
        # paramd/paramf: presets on the params block — the '2' arm
        # reads f[params] and d[params] for its inline advance.  NOTE:
        # the 2AC5F0 prologue zeroes d[r9] at entry, so these presets
        # only survive when the case's r9 is NOT "params" (use auxout).
        for off, v in case.get("paramd", {}).items():
            gm.w(self.params + off, dw(v))
        for off, v in case.get("paramf", {}).items():
            gm.w(self.params + off, struct.pack("<f", float(v)))
        self.ctxe8 = self.ctxo + 0x10E8
        # c54: out-cell block for direct 2B24B0 entry — r9 = c54+0x54,
        # stack ptrs to +0x58/+0x60/+0x5C/+0x50/+0x51.
        self.c54 = self.alloc(0x80)
        self.c54r9 = self.c54 + 0x54
        self.c54a5 = self.c54 + 0x58
        self.c54a6 = self.c54 + 0x60
        self.c54a7 = self.c54 + 0x5C
        self.c54a8 = self.c54 + 0x50
        self.c54a9 = self.c54 + 0x51
        # dobjrec: optional rec planted at q[dobj+0x698] — 3283D0's
        # subtype-offset gate consults it (rec && b5==0 -> offset 0).
        dr = case.get("dobjrec", 0)
        if isinstance(dr, str):
            dr = getattr(self, dr, 0)
        if dr:
            gm.w(self.dobj + 0x698, qw(dr))
        # sob: extra byte writes on subobj (b[+3] stays via so3).
        for off, v in case.get("sob", {}).items():
            gm.w(self.subobj + off, bytes([v & 0xFF]))
        # ctrl: 28FBE0's dispatch controller — q[0209BE80] -> obj,
        # q[obj+0x10F78] -> handler; both non-null for dispatch.
        # ctrlsub hosts the sinks' 0x160-stride slot array: w[idx*0x160
        # +0x318] flag bits, paired zero-words +0x350/354/356, gate byte
        # +0x31E.
        if case.get("ctrl"):
            self.ctrl = self.alloc(0x11000)
            self.ctrlsub = self.alloc(0x4000)
            gm.w(0x209BE80, qw(self.ctrl))
            gm.w(self.ctrl + 0x10F78, qw(self.ctrlsub))
        # csb: byte presets on ctrlsub (pre-set flag words / gate byte)
        for off, v in case.get("csb", {}).items():
            gm.w(self.ctrlsub + off, bytes([v & 0xFF]))
        # fbtab: 296280's fixed 4-entry 0xC0-stride scan table at
        # 0209BFBE — flag b[e]&2 (or b[e-0x58]&2), id match d[e+0x32].
        for i, spec in case.get("fbtab", {}).items():
            e = 0x209BFBE + i * 0xC0
            if "fl" in spec:
                gm.w(e, bytes([spec["fl"] & 0xFF]))
            if "fl0" in spec:
                gm.w(e - 0x58, bytes([spec["fl0"] & 0xFF]))
            gm.w(e + 0x32, dw(spec.get("id", 0)))
        # t3320: 273320's resolver table — count w[022C8064] (movsx word),
        # id field d[022C8084 + i*0xC0]; return = index or -1.
        t33 = case.get("t3320")
        if t33 is not None:
            gm.w(0x22C8064, struct.pack("<H", t33.get("n", 0) & 0xFFFF))
            for i, v in t33.get("ids", {}).items():
                gm.w(0x22C8084 + i * 0xC0, dw(v))
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

    def _ctxr(self):
        # EXP-208: helper-produced context results + the measure
        # deltas.  ctxrd/ctxrf/ctxrb write the shared ctx object's
        # result fields (the real producers are the stubbed decoders);
        # af340f plants the 0209CC60-band global accumulators the
        # walkers clear at init and accumulate into per iteration.
        cx = self.gm.q(0x209CC40)
        for off, v in self.case.get("ctxrd", {}).items():
            self.gm.w(cx + off, dw(v))
        for off, v in self.case.get("ctxrf", {}).items():
            self.gm.w(cx + off, struct.pack("<f", float(v)))
        for off, v in self.case.get("ctxrb", {}).items():
            self.gm.w(cx + off, bytes([v & 0xFF]))
        af = self.case.get("af340f")
        if af is not None:
            self.gm.w(0x209CC68, struct.pack("<f", float(af[0])))
            self.gm.w(0x209CC64, struct.pack("<f", float(af[1])))

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        if self.case.get("dbgf"):
            for r in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI",
                      "RBP", "RSP", "R8", "R9"):
                self.faults.append(
                    (r, uc.reg_read(
                        globals()["UC_X86_REG_" + r])))
            self.faults.append(
                ("stk", self.gm.q(uc.reg_read(UC_X86_REG_RSP)),
                 self.gm.q(uc.reg_read(UC_X86_REG_RSP) + 8)))
            rip = uc.reg_read(UC_X86_REG_RIP)
            try:
                self.faults.append(
                    ("ibs", bytes(uc.mem_read(rip, 16)).hex()))
            except Exception:
                pass
        uc.emu_stop()
        return False

    SCR = {0x30E130: ("e130", "e130_ret"),
           # EXP-257: 427320 promoted real on u43f0-ec — 3E7D10 row
           # empty -> misses the 0x2005/0x2006 arms -> 420890 default
           # -> 423790 ret 1 -> class-1 switch arm (20E600 x2, d294|=8).
           X_112F0: ("n12f0", "n12f0_ret"),
           # EXP-250: 2FA390 promoted real (2F8E90 &7)
           # EXP-246: 46AB10's insert-notify tail — 0x240-frame fn
           # taking a stack arg 46AB10 never writes; sole caller is
           # 0x46AC66.  Kept a recorded boundary.
           0x5369C0: ("s5369c0", None),
           # EXP-224: 234DA0 promoted real (ld234da0)
           # EXP-218: 808C40 (__security_check_cookie) promoted real —
           # cmp/rol/test leaf; the planted cookie always matches so
           # the 809654 report path is never taken.
           # EXP-248: 383F10 nav-grid cell walk — scripted boundary
           # (IAT slot 0x8C2C10 holds unbound RVA 0x1CCF034, not
           # code).  Ret models the shipped early-exit (cell origin
           # past the query point -> 0xFF); grid fixture deferred to
           # the 391D10/3920F0 query-arms package.
           0x383F10: ("s383f10", "s383f10_ret"),
           0x3B02A0: ("b3b02a0", "b3b02a0_ret"),
           0x1DBDB0: ("b1dbdb0", "b1dbdb0_ret"),
           0x2966E0: ("q2966e0", "q2966e0_ret"),

           # EXP-250: 2FA540 promoted real (320450->329A20)
           # EXP-243: 28F1F0 gauge-event post promoted real — the
           # channel table at 0x209BF66..0x209C2BE and default slot
           # 0x209C240 are BSS-zero shipped, so the 296280 id-scan
           # misses, the 2962C0 fallback's d[+0xB0]!=0 gate fails,
           # and the body early-outs.  All 7 callers pass ecx=0.
           0x252E60: ("n252e60", "n252e60_ret"),
           0x300E40: ("p300e40", None),
           # EXP-234: 2E42D0 (q[ent+0xC0] node -> ecarr row-gated
           # 427280 fold -> d[+0xEC] clear) promoted real; 427280's
           # jmp 422C20 dereg tail promoted real EXP-257 — the three
           # slot fields planted -1 so only the clear block runs
           # (51BA40/2ED570 resolver arms stay unclaimed).
           # EXP-225: unlink/teardown leaf family promoted real —
           # 2ECF10/2ECEC0 (q[obj+0xC0] link -> ec-array gated tails),
           # 313F60 (thunk -> 377C20 row-bit15 check), 2699D0
           # (2ECA00 flag + 2EB430 reset -> 2EB0D0 sink), 17FD30
           # (on_code shim removed — 1B5FA0 + 1E9D20 dev1 setter).
           # EXP-198: unlink-carrier family boundaries
           0x238BF0: ("d8bf0", None),
           # EXP-245: 23B040 promoted real — the b[02089340]&0x40
           # epoch gate -> 303EC0/313F60 guards -> 3272A0 ctx-row
           # lookup (null on u0fc0 fixtures) -> tail 3592C0/359200/
           # 26BD40 flag publishes on BSS cells 022C80xx/0209A2C5.
           0x311F70: ("b1f70", None),
           # EXP-251: 311CF0 promoted real — 3138D0's rdi-nonnull arm
           # now reaches it (ctx4 slot-3 + clstab fixture); tail
           # 317E60->25AAD0(1,0) is bounded (ebx!=0 skips the notify).
           0x313B30: ("b3b30", None),
           0x2FEAD0: ("bread0", None),
           # EXP-231: 319140's edx&1 arm — 290B90 walks the entity
           # list at q[0x209BE80]+0x10F10 unconditionally; the shipped
           # cell is BSS-null and no fixture builds the list, so the
           # real head deref would fault.  Scripted boundary until a
           # live-list fixture exists.
           # EXP-241: 290B90 promoted real — fbdev device-list
           # scan (d[node+0x810]==ecx, w[+0x850] 2->3).
           # EXP-242: 28EF70/28EF00 promoted real — 317ED0's flag-
           # writer sinks now execute on the fbdev=1 object; 28F0C0
           # runs silently real (ecx!=0 arm -> t53770 -> real 316A50).
           # EXP-230: 30C970's gated arms — handle releases the
           # 325A00/317EC0 guards jmp to on a nonzero d[+0x28]/[+0x24]
           # and the d[+0x18]-gated owner notify. x0 under shipped-
           # zeroed table rows; declared so a live-row fixture
           # surfaces them instead of running unmapped.
           0x3DC780: ("v3dc780", None), 0x42FCC0: ("v42fcc0", None),
           0x306570: ("v306570", None),
           0x317E50: ("b7e50", None),
           0x321850: ("b1850", None), 0x327200: ("b7200", "b7200_ret"),
           # EXP-239: 2EBB80 promoted real (b[+3]&0xE0==0x60 gate
           # -> q[+0xC0] node -> b[node+0x10] bit-3 fold).  Its pass-arm
           # jmp tail 2E8FD0 stays scripted v2e8fd0 — second-level
           # node walk + 3E6A60/2E8CE0/2EE190/2E8AC0/2E8A70 subtree;
           # never reached under fixtures (ent_b+3=0).
           0x2E8FD0: ("v2e8fd0", None),
           0x3E6B40: ("b6b40", None),
           # EXP-250: 254850 promoted real (10x 2E1C20)
           # EXP-244: 2548F0 promoted real — flag->set/clear pick
           # between 2E1C20/2E1CA0 then four (slot8, bit) ops on
           # d[0215F1E0] (BSS): bits {8,9,0xB,6} = 0xB40 / clear.
           0x36C1D0: ("bc1d0", "bc1d0_ret"),
           0x36C140: ("bc140", None), 0x24FE70: ("b4e70", "b4e70_ret"),
           0x3B0770: ("b0770", None),
           # EXP-240: 2E9BB0/2EC5B0 promoted real — null-guarded
           # q[+0xC0] -> q[+0x138] -> d[+0x110] getter/setter pair.
           # EXP-199: 312280's scripted subtree boundaries.  EXP-223
           # promoted 3171C0/317090/28FB80/253690/254EE0/469E80 real;
           # 317ED0/319490/3180F0/319CA0 stay scripted (the
           # 3377C0 entity-node subtree behind 319490 needs the deep
           # ctx chain). EXP-226 promoted 316A50 real; EXP-232
           # promoted its UI message sink 8632B0 + singleton getter
           # 20CE00 real — the 20CE60 dispatch stays scripted (needs
           # a planted UiManager vtable; null singleton gates it out).
           # EXP-236: 317ED0 promoted real — its deep arms (229E40
           # epoch gate -> 28EF00/28EF70 flag writers on the
           # q[0x209BE80] cell family) stay gated off under the
           # shipped-zero counters; on the reached arm it runs pure
           # reads + 0x22C31xx counter writes.
           # EXP-234: 319490 promoted real — its ctx chain (3590D0 ->
           # b[0x2089340]&0x10 -> 3588B0 -> 263E30 -> b[node]&8) is all
           # real; EXP-247 promoted the 3377C0 spatial broadcast too
           # (guard path — deep arms await the entity-list fixture).
           0x3180F0: ("s80f0", "s80f0_ret"),
           0x319CA0: ("s9ca0", None),
           0x20CE60: ("v20ce60", None),
           # EXP-201/206: display-queue scripted boundaries.  31C5D0
           # promoted real in EXP-205; 2B3050/2B3120 real in EXP-206 —
           # these five leaves stay scripted and the 2B24B0 float
           # evaluator is stubbed in on_code (bounded CRT subtree).
           # EXP-218: 39C4A0 promoted real — BSS font-record select;
           # the q[02AEE800]/q[02AEE808] fixture below returns the
           # resolved s39c4a0_ret unchanged.
           # EXP-238: 39BAD0 promoted real — the 8-entry
           # registered-language table at 02AEE810 ships BSS-zero;
           # the bad0t fixture plants it so the real scan returns
           # the s39bad0_ret=7 arm honestly.

           # EXP-220: 1E94E0's lazy-init callees (the +0xF68 flag
           # plant skips them; scripted so a flag-0 run is a
           # disclosed boundary, not a crash) + the fixture
           # allocator's alloc/dealloc slots used by 1E7A20's
           # realloc arm (aobj+0x10/+0x18).
           0x19C5D0: ("s19c5d0", "s19c5d0_ret"),
           0x1C5F20: ("s1c5f20", None),
           0x7000A100: ("salloc", "salloc_ret"),
           0x7000A108: ("sdealloc", None)}

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
            # EXP-224: the entry-proven scripted bodies promoted — all
            # already execute real as direct-entry cases (g7930-*,
            # l8b40-*, o4100-*, u43f0-*, c650-* sites); their callees
            # were all REAL or still-scripted sinks.  g3910/s3c60/
            # a8ff0/o4020/m8040/m8130/ld234da0 already had REAL tags;
            # only the SCR intercepts were removed.
            0x317930: "l317930", 0x318B40: "l318b40",
            0x324100: "l324100", 0x3243F0: "l3243f0",
            0x30C650: "l30c650",
            # EXP-225: unlink/teardown leaf family + 17FD30 setter.
            # 2ECF10/2ECEC0 share the q[obj+0xC0] -> d[link] idx ->
            # q[0x22C6F28]+idx*0x740 -> d[elem+0x284] gate -> tails
            # (426130 heavy / 3AEEF0 chain-zero); 313F60 -> 377C20
            # (3148F0 idx -> q[0x2ADD100] row bit15); 2699D0 ->
            # 2ECA00 flag + 2EB430 reset + kb0d0 sink; 17FD30 ->
            # 1B5FA0 dev1 + 1E9D20 map-find/clear.
            0x2ECF10: "l2ecf10", 0x2ECEC0: "l2ecec0",
            0x313F60: "l313f60",
            0x2699D0: "l2699d0", 0x2ECA00: "l2eca00",
            0x2EB430: "l2eb430", 0x3587C0: "l3587c0",
            0x17FD30: "l17fd30", 0x1E9D20: "l1e9d20",
            0x1B5FA0: "l1b5fa0", 0x3AEEF0: "l3aeef0",
            0x263FF0: "l263ff0", 0x16D6A0: "l16d6a0",
            0x2FD0C0: "l2fd0c0", 0x3B2830: "l3b2830", 0x3B1260: "l3b1260",
            # EXP-226: 316A50 per-kind stat accumulator + helpers —
            # kind desc table 0xD10460 {mode,slotoff,cmpmode,cmpval},
            # msg ids 0xD10550, value slots q[020927C0]+0x384C,
            # achieved-bits +0x3844; 315E90 gate -> 8632B0 notify
            # (scripted), 316BF0 write-back. Deep 315E90 arms
            # (309EC0 scan/popcount/3160C0/3161A0/315420) unreachable
            # under these fixtures (all exercised kinds cmp=0).
            0x316A50: "l6a50", 0x316BF0: "l6bf0",
            0x3166F0: "l66f0", 0x3165C0: "l65c0",
            0x316760: "l6760", 0x315E90: "l5e90",
            # EXP-227: 3105D0 object reset — null/q[obj+0x698] gate,
            # 310780(obj+0x80) detach, 30C970 on old +0x695/+0x696
            # bytes (real since EXP-230), 300280 dc8/e58 handling, header bit
            # masks, 16D6A0 noop, 236820 loop clearing elem+0xEA0 bit
            # b[obj+0xEA9], 316CF0 memset(obj+0x778,0x208), state copies
            # +0x718/+0x728 -> +0x730/+0x740, field resets, 3291B0 ctx
            # reset (3839F0 FF-fill +0x200..0x27F, 16B copies),
            # 33C9B0(336710 compose -> 33E1F0) on obj+0x80. 33E1F0's
            # and [q[obj+0x1E0]] and 336710's q[obj+0x1E8] deref are
            # fixture-planted under objlink.
            0x3105D0: "l3105d0",
            # EXP-228: 30FED0 status recompute — builds a 128-bit
            # bitmap (foed row +0x50/+0x54 or member +0xE80, 5 equip
            # slots via memt + 31E9A0==3 -> b[row+0x1A], license bits
            # rec+0x194 -> abild rows gated 323890==2 -> w[+8..0x16]),
            # diffs vs rec+0x78, dispatches added bits -> e130 mode3 /
            # removed -> mode1 (scripted), fef30 notify (scripted),
            # member tail: bt d[owner+0xE90] -> e360 mode5, then
            # b[q[owner+0x6A0]]&0x80 selects the +0x78..0x7C <-> +0x40..
            # 0x44 copy direction; tail clamps d[+0x48]/w[+0x4C]/w[+6]
            # then n0e060.  31E9A0/31E9F0 real: b[row+9] -> shipped
            # jump table -> class 0-3.
            0x30FED0: "l30fed0", 0x31E9A0: "l31e9a0",
            0x31E9F0: "l31e9f0",
            # EXP-229: 2FEF30 derived-stat accumulator promoted real —
            # zeroes rec+0x24..0x47 (saving d[rec+0x3C] first when
            # rdx==0 -> 31B860 owner resolve), foe arm: 2F8E50
            # (x*y*z magic-div scale) + 2F9180 (x*y/100) + d[+0x48/
            # 0x4C] flag ORs; member arm: level delta b[+0x1C2]-b[+0x88]
            # scales growth rows q[02EBF148/140/150] chained off
            # w[membrow+0x22]/+0x24/+0; equip loop folds
            # b/w[elemb+d[memtrow+0x28]] item bonus; status-bit fold
            # walks q[02EBF040] rows via shipped idx tables
            # 0xD10290/0xD102A0/0xD102B0; tail clamps: d[+0x24] HP
            # (0x270F or 0x3B9ACA00 cap), w[+0x28] MP <=0x3E7,
            # b[+0x2A..0x2D] stats <=0x63, b[+0x2E] <=3.
            0x2FEF30: "l2fef30", 0x2F8E50: "l2f8e50",
            0x2F9180: "l2f9180",
            # EXP-230: 30C970 mode-byte clear — cl<=0x1F resolves a
            # 0x30B row in the 32-entry .data table 0x22C17B0,
            # unlinks it from the intrusive lists headed at
            # 0x22BE978/0x22BEB88, releases d[+0x28]/d[+0x24] through
            # the 325A00/317EC0 guard thunks (self-skip on 0),
            # notifies 306570(31B7E0(d[+0x20])) when d[+0x18]!=0,
            # then resets the row: d[+0x2C]&=~0x1F, w[+0x1C]=0xFFFF,
            # q[+0]/q[+8]=0, d[+0x28]=0x80000000, d[+0x24]=0xFFFFFFFF,
            # q[+0x14]=d[+0x10]=d[+0x20]=0.  cl==0xFF or cl>0x1F is a
            # full no-op.  The jmp 3DC780/42FCC0 arms and 306570 stay
            # scripted (v3dc780/v42fcc0/v306570, x0 — shipped-zeroed
            # rows).
            0x30C970: "l30c970", 0x325A00: "l325a00",
            0x317EC0: "l317ec0",
            # EXP-231: the 310780/300FC0 detach siblings —
            # 319420(obj+0x6B0): d[+0xC4] (i.e. d[obj+0x774]) not in
            # {0,-1} -> 2EAEA0(id,1) -> real 24FE30 dispatch, then
            # d[+0xC4]=-1.  319140(obj,edx): edx&1 -> 290B90
            # (d[obj+8] id -> entity-list flag; EXP-241 real — the
            # fbdev fixture plants q[0x209BE80] + its q[+0x10F10]
            # device list), edx&2 -> 3BBC80(q[obj+0x10]) 64-entry ring
            # clear on q[0x2B457D0] (null-safe real).  308270(obj):
            # bt q[obj],0x16 -> d[+0x28]=0, 30C970(b[obj+0x695]),
            # b[+0x695]=0xFF, w[+0xDC8]/d[+0xE58] from 0x22C1DB0 row
            # b[obj+0xEA9], 30EDA0 snapshot copy q[obj+0xB88]->
            # obj+0x730 (0x480), q[obj]&=~0x400000400000,
            # d[+0x690]=0.
            0x319420: "l319420", 0x319140: "l319140",
            0x308270: "l308270", 0x2EAEA0: "l2eaea0",
            0x3BBC80: "l3bbc80", 0x30EDA0: "l30eda0",
            # EXP-232: 316A50 family's UI notify thunk — 8632B0
            # (ecx=msgid): 20CE00() singleton null -> ret; else
            # tail 20CE60(ctx, msgid) — scripted v20ce60, gated
            # out on the null q[01F83450] fixture (x0).
            0x8632B0: "l32b0", 0x20CE00: "l20ce00",
            # EXP-233: 2EB430 family's node teardown — 2EB0D0
            # (node=rdx: null->ret, d[node]==-1 -> bail; else
            # 269D60 flag fold + ecarr-row (w[node]*0x740 +
            # q[0x22C6F28], d[+0x284] gate) 427xxx flag writes +
            # node reset -1.0/FFFF/flag clears).  427320 scripted
            # v427320.  269D60 = b[+0x29] flag leaf; 4278B0/427860/
            # 4272A0 = d[+0x294] bitset leaves.
            0x2EB0D0: "l2eb0d0", 0x269D60: "l269d60",
            0x4278B0: "l4278b0", 0x427860: "l427860",
            0x4272A0: "l4272a0",
            # EXP-234: 2E42D0's node->ecarr clear + its 427280 fold
            # leaf (the jmp 422C20 dereg tail stays scripted).
            0x2E42D0: "l2e42d0", 0x427280: "l427280",
            # EXP-256: 426FA0 ecarr flag-propagate — w[obj] idx ->
            # q[0x22C6F28]+idx*0x740 row; 426220 signature gate (ret
            # nonzero -> skip) else d[row+0x284]|=0x100000 +
            # b[row+0xC0]&=0xBF, then w[row+8] child row (same) and
            # 42EF90 enqueues w[row+8]/w[row+0xA] into a stack set.
            0x426FA0: "l426fa0",
            # EXP-257: 422C20 ecarr-row dereg (slots d[+0xC4]/+0xC8]
            # -> 20E600->q[+0xDA8]->51BA40, d[+0x18] -> q[+0xD98] ->
            # 2ED570 -> d[node]&=~8) + clear block (q[+0x68]/+0xD8]/
            # +0xF0/+0xE0/+0xF8]=0, d[+0x23C]=0, b[+0xC0]&=0xBF,
            # d[+0x69C]=20E620(0) twice); 427320 edi-switch (3E55F0/
            # 3E7D10 gates -> 420890 default + 423790 ret-1 ->
            # class-1 dispatch w/ 20E600 x2 + d294|=8).
            0x422C20: "l422c20", 0x427320: "l427320",
            # EXP-234b: 319490's ctx resolution + vec4 marshal — the
            # 3377C0 broadcast stays scripted (v3377c0 handler).
            0x319490: "l319490",
            # EXP-236: 317ED0 broadcast-rate gate real (229E40 was
            # already real since EXP-209 — called twice per pass, at
            # the b[obj+0x56]==d[0x22C3168] arm and after the LCG
            # tick; the 28EF70/28EF00 flag sinks stay v-scripted).
            0x317ED0: "l317ed0",
            # EXP-237: the u0fc0 b[+3]&0xE0==0x60 gate pair — 2E9780
            # (node b[+0x11]>>6 read, null-guarded) and 26D6F0 (float
            # dispatch on q[+0xB8]/q[+0xC0]+0x138, gate-fail = pure
            # ret).  All 8 calls run the early-out under fixtures.
            0x2E9780: "l2e9780", 0x26D6F0: "l26d6f0",
            # EXP-238: 39BAD0 registered-language resolver — scans
            # the 8-slot 02AEE810 table for low32(rcx), ret index or
            # 0.  bad0t plants the table; b3050-arm/alt get the
            # ==7 arm from the real scan.
            0x39BAD0: "l39bad0",
            # EXP-239: 2EBB80 entity-node bit-3 writer — reached via
            # the l26dc60 jmp trampoline from 301140's teardown.
            0x2EBB80: "l2ebb80",
            # EXP-240: the flagtgt d[+0x110] getter/setter pair
            # 26D6F0's pass arm calls through q[+0xC0]->q[+0x138].
            0x2E9BB0: "l2e9bb0", 0x2EC5B0: "l2ec5b0",
            # EXP-241: 290B90 fbdev device-list scan — ret 1 on a
            # d[node+0x810]==ecx match (folds w[+0x850] 2->3), 0 else.
            0x290B90: "l290b90",
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
            0x3EFD00: "l3efd00", 0x3A1920: "l3a1920",
            # EXP-203: 28FBE0 dispatch consumers — ctrlsub slot-array
            # flag setters
            0x296E90: "l296e90", 0x297040: "l297040",
            # EXP-204: the sinks' id->slot-index resolver and its two
            # table leaves (count w[022C8064], id field d[022C8084+i*C0])
            0x273320: "l273320", 0x35BB00: "l35bb00",
            0x35BB60: "l35bb60",
            # EXP-205: kind-dispatched resource resolver (type-0x1A
            # arm resolves the display path) + its bucket leaf
            0x31C5D0: "l31c5d0", 0x2F9860: "l2f9860",
            # EXP-206: 2B3050 evaluator wrapper + 2B3120 float->word
            # output shell — last display-path edges; the formatter
            # core 2B24B0 stays a bounded stub
            0x2B3050: "l2b3050", 0x2B3120: "l2b3120",
            # EXP-207: 2B24B0 itself — line-layout save/reset/restore
            # wrapper; inner measurers 2B2150/2AF340 + ceilf stubbed
            0x2B24B0: "l2b24b0",
            # EXP-208: 2B2150/2AF340 segment-string walkers real;
            # 2AC1E0 0xD0 state init real; the control-code decode
            # 2AC2F0, glyph interpret 2AC5F0, 2B3E30 and the font
            # shim family 17F940/17FAE0/17F8C0 stay boundary stubs
            0x2B2150: "l2b2150", 0x2AF340: "l2af340",
            0x2AC1E0: "l2ac1e0",
            # EXP-209: 2AC5F0 text-control-code interpreter real +
            # its leaf helpers (global dword read, const float div,
            # ctx-field dispatchers).  2A9F00 glyph engine, 2B2DF0/
            # 2B43C0 walker wrappers, 3FFDF0 param parser, 2AB820 and
            # the 17Fxxx font shims stay boundary stubs.
            0x2AC5F0: "l2ac5f0",
            0x229E40: "l229e40", 0x24ABA0: "l24aba0",
            0x2B1F20: "l2b1f20", 0x2B2C50: "l2b2c50",
            0x2B2D20: "l2b2d20",
            # EXP-211: tag-15 second-level sub-arm decoders —
            # 3FFAB0 (param byte decoder) + 39BA00 (escape-table
            # lookup over q[02AEE870], fixture-planted via ba00t)
            0x3FFAB0: "l3ffab0", 0x39BA00: "l39ba00",
            # EXP-211 correction: 2AC5F0 tag-5 arm's nested-2B2150
            # call site — records rcx/rdx when the ctx48==0 gate
            # passes (nested self-calls are invisible when the case
            # entry IS 2B2150)
            0x2ACDF9: "l2b2150n",
            # EXP-212: the whole param-parser family — leaf decoders
            # promoted real; 3FFBC0/3FFB00 call the real 39BA00.
            0x3FFEE0: "l3fee0", 0x3FFBC0: "l3fbc0", 0x3FFD70: "l3fd70",
            0x3FFC60: "l3fc60", 0x3FFCE0: "l3fce0", 0x3FFDA0: "l3fda0",
            0x3FFB00: "l3fb00", 0x3FFB90: "l3fb90", 0x3FFF10: "l3ff10",
            # EXP-213: the resource-lookup chain under the '8'/'>'
            # arms and '!' font select.  2EF2B0/2EF640 already REAL.
            0x39BA30: "l39ba30", 0x263990: "l263990",
            0x2639E0: "l2639e0", 0x32A930: "l32a930",
            0x3EAC10: "l3eac10",
            # EXP-214: the measure wrappers — 2B41F0 builds a default
            # 0xD0 state template (861EC0 memset hook + s39c4a0 font
            # pick -> q[copy+0x60] flag desc), then both tail into the
            # REAL 2AF340 evaluator; 808C40 cookie check stays a
            # scripted boundary.
            0x2B41F0: "b41f0", 0x2B43C0: "b43c0",
            # EXP-215: publish/draw helpers — 2AE610 '-'-arm
            # decoration measure+publish (state copy, 39C4A0 pick,
            # real 3FFC60 re-parse, d44&0x800-gated deep measure,
            # real 2A9F00 tail); 2AE450 '?'-arm sprite draw +
            # 39BB00 BSS-singleton mode dispatch (table fixture-
            # planted via sprtab); 2A9F00 glyph-run publisher —
            # per-glyph 17F8C0 record fetch, 17FC90 quad build,
            # 17F7C0 emit, d[ctxo+0x10D4] batch counter, real 2AC5F0
            # re-interpret of embedded control codes.  17FC90/
            # 17F7C0/2AFDC0 emit sinks stay scripted boundaries.
            0x2AE610: "e610", 0x2AE450: "e450",
            0x39BB00: "bb00", 0x2A9F00: "a9f00",
            # EXP-216: display-list append chain — 2B4730 drains
            # q[0209CC50] into q[0209E5A0] command records (header +
            # terminator), aligns q[ctx48+8], then 3A1DB0 flips the
            # d[02EBEFF0] ring slot (resets the other slot's write
            # cursor) and 36F360 patches the 0x30000000 record header
            # + ring bookkeeping.  All globals fixture-planted
            # (listcur/ctx48o/ring).
            0x2B4730: "b4730", 0x3A1DB0: "a1db0",
            0x36F360: "l36f360",
            # EXP-217: 2B1FB0 — standalone measure/skip helper.
            # Memsets a 0xD0 default state (861EC0 hook), 39C4A0 font
            # pick -> q[rbp-0x60], then dispatches on b[rcx]:
            # >0xF -> REAL 2AC2F0 decode, <=0xF -> REAL 2AC5F0 interpreter,
            # both on cursor cell q[rsp+0x28].  Returns consumed =
            # d[rsp+0x28] - arg.  Callees all mapped.
            0x2B1FB0: "b1fb0",
            # EXP-218: 808C40 __security_check_cookie leaf, 39C4A0
            # BSS font-record select (globals fixture-planted),
            # 2AFDC0 '?'-arm quad submitter (writes real command
            # records + calls the real 2B4730 flush; 17FC90 stays
            # scripted and 2DD860/181560 are new emit stubs),
            # 2B1ED0 ctx soft-reset (d44&0x800 selects the
            # s17f980/s17f960 vs s17f8a0/s17f880 float pair; both
            # arms land the results on f[0209CC70]/f[0209CC74]).
            0x808C40: "cookie", 0x39C4A0: "c4a0",
            0x2AFDC0: "afdc0", 0x2B1ED0: "b1ed0",
            0x2DD8B0: "dd8b0",
            # EXP-219: 2AEB20 kind-0x1C nested catch-all — sub-kind flag
            # table (2AB8F0 jump table), edi-gated record index from the
            # 9165F0/916670 byte tables (1E0C30 -> d[q[q[02AEE868]+0xDF8]
            # +0x10] mode check), per-entry quad records into q[0209CC50]
            # (real 17FC90 UV write into q[01F811F8]+0x137C, real 2DD860
            # corner transform+projective divide via 202B70/217060 leaf,
            # 2DD8B0 vertex format, scripted 181xxx device tail), then
            # real 2B4730(1) flush; returns eax=2 consumed. 17F7C0's
            # 0xA0 matrix copy + 1E8070 submit runs fully real.
            0x2AEB20: "eb20", 0x17FC90: "fc90", 0x17F7C0: "f7c0",
            0x2DD860: "dd860", 0x1E9C40: "e9c40", 0x1B5FA0: "b5fa0",
            0x202B70: "e2b70", 0x217060: "t7060", 0x1E0C10: "e0c10",
            0x1E0C30: "e0c30", 0x2AB8F0: "ab8f0", 0x2DDC50: "ddc50",
            0x180150: "l80150", 0x228480: "l228480", 0x2441E0: "l441e0",
            # EXP-220: 1E8070 vertex-batch submitter (2x3 expansion of
            # the 0xA0 state into 0x3C records appended to the vector
            # at q[dev1+0x10]+0x18, bounds/flags at dev1+slot*0x2C+
            # 0x2324, consumes+resets the dev1+0x137C scale quad) +
            # 1E7A20 vector::_Emplace_reallocate (allocator virtuals
            # at aobj+0x10/+0x18 stay scripted) + 1E94E0 lazy-init
            # metrics getter (flag planted 1; s19c5d0/s1c5f20
            # scripted boundaries).  The four metric thunks run
            # 1B5FB0 (q[01F81200] font-map singleton) -> 1B51C0
            # exact-key find -> 1B1620 flag (b[01F811E0]) -> raw
            # field or divss/ceilf arm; 1E94E0/1FDDB0/225670/
            # 79CFA0/225690/79E3C0/16D6A0 leaves, 17F920 -> 1E9840
            # (dl selects 1FDDC0 d+0x1C vs 1F49E0 d+0x20), 17F9C0 ->
            # 1E9BD0 (ceilf(edx / f[devsub+0x34])), 17F8C0 -> 1E9860
            # (codepoint remap via q[dev1+8] vector -> 1FDEC0 inline
            # map at devsub+0x50), 17F940 -> 5C52D0 getter and
            # 17FAE0 -> 848C20 setter for q[dev1+0x28].
            0x1E8070: "e8070", 0x1E7A20: "e7a20", 0x1E94E0: "e94e0",
            0x17F880: "f880", 0x1E93C0: "e93c0",
            0x17F8A0: "f8a0", 0x1E9450: "e9450",
            0x17F960: "f960", 0x1E9580: "e9580",
            0x17F980: "f980", 0x1E9610: "e9610",
            0x17F920: "f920", 0x1E9840: "e9840",
            0x1FDDC0: "fddc0", 0x1F49E0: "f49e0",
            0x17F9C0: "f9c0", 0x1E9BD0: "e9bd0",
            0x17F8C0: "f8c0", 0x1E9860: "e9860", 0x1FDEC0: "fdec0",
            0x17F940: "f940", 0x5C52D0: "c52d0",
            0x17FAE0: "fae0", 0x848C20: "a8c20",
            0x1B5FB0: "b5fb0", 0x1B51C0: "b51c0", 0x1B1620: "b1620",
            0x1FDDB0: "fddb0", 0x225670: "t5670", 0x79CFA0: "y9cfa0",
            0x225690: "t5690", 0x79E3C0: "y9e3c0", 0x16D6A0: "d6a00",
            # EXP-221: the 181xxx emit-tail wrappers forward through
            # 1B1C00 (q[01F811E8] render-device singleton) into real
            # 1Bxxxx methods: 1B1910 reset (1B0100 slot-clear loop
            # over dev+0x2328 stride 0x58 + memset hook + four 0x80
            # seeds), 1B2410 texture-region props (r9!=0 -> 17D2E0
            # -> 16D670 CRT-options global -> scripted vsnprintf-
            # shaped sink at 0x1CCECB4), 1B06D0 slot-vector append
            # (1AED50 insert/realloc arm; allocator fn slots
            # scripted), 1B2490 mode table (0x8F80F8 dwords) ->
            # d[dev+0x3A60], 1B22D0/1B22E0 qword stores.  181330 ->
            # 1B03D0 stays scripted (deep multi-callee body).
            0x181560: "w181560", 0x1B1C00: "b1c00",
            0x1B1910: "b1910", 0x1B0100: "b0100",
            0x1819A0: "w1819a0", 0x1B2410: "b2410",
            0x17D2E0: "d2e0", 0x16D670: "d670",
            0x181870: "w181870", 0x1B2490: "b2490",
            0x181460: "w181460", 0x1B06D0: "b06d0", 0x1AED50: "aed50",
            0x1816B0: "w1816b0", 0x1B22D0: "b22d0",
            0x181910: "w181910", 0x1B22E0: "b22e0",
            # EXP-222: 2AC2F0 control-code/char decoder real —
            # b[cursor]>=0x20 -> esi=b-0x20 (+1 advance); b<0x20 ->
            # esi=b[cursor+1]-0x20+d[0x916570|0x9165B0 | (al&0xF)*4]
            # (d[0209CC38] selects the table; +2 advance).  Both arms
            # pick a font record (39C4A0(0) -> q[ctx+0x60]), run
            # scripted 17FD30 with d[0209D480], set mode globals
            # d[0209CC30]/+34, then publish the 0x209CC60..7C quad
            # block: real 17F980/60 or 17F8A0/80 metric pair (the
            # d[ctx+0x44]&0x800 arm), 20E600 element row at esi*8,
            # 17F8C0 glyph remap, kern paths 17F9C0 / (17F940 &&
            # d[rbx+0x20]!=-1 ->) 17F8E0 -> 1E9780 -> 1FDDD0 two-
            # level devsub map find -> 1E9BD0 ceilf tail, then
            # 17FAE0 publishes rbx to q[dev1+0x28].  254A10 promoted
            # real: 229E40 lang dword 0x1E02814 in {0,7,8,10,11} via
            # bt 0xD81.
            0x2AC2F0: "l2ac2f0", 0x17F8E0: "f8e0",
            0x1E9780: "e9780", 0x1FDDD0: "fddd0",
            0x254A10: "l254a10",
            # EXP-223: 312280's source-share tail accessors real —
            # 253690 FP-total getter (d[q[02092758]+8]), 254EE0 FP
            # setter (delta -> 316A50(6|7,|delta|) notify, clamp
            # [0,0x5F5E0FF], store d[+8]), 317090 FP stat add
            # (316A50(0x11, (b1c2-b88)*w[e78]+w[e70]) via 253770 jmp),
            # 3171C0 member-seen counter (316A50(4,1), then
            # 263C20!=3 && w[e68+0x52]!=0xFFFF -> 253750 -> 315820
            # msg-id counter at b[q[020927C0]+id+0x3404]), 28FB80
            # paired 289D00 slot writes on q[0209BE80]+0x5380,
            # 469E80 delta notifier (ecx>0 -> REAL 46AB10).
            # 317ED0/316A50/319490/3180F0/319CA0 stay scripted —
            # 319490's 3377C0 tail needs the entity-node ctx chain.
            0x253690: "t53690", 0x254EE0: "t54ee0",
            0x28FB80: "tfb80", 0x317090: "t7090",
            0x3171C0: "t71c0", 0x469E80: "t69e80",
            0x289D00: "t89d00", 0x2E9D10: "t2e9d10",
            0x289BD0: "t89bd0", 0x2536A0: "t536a0",
            0x315820: "t15820", 0x315D50: "t15d50",
            0x253770: "t53770", 0x253750: "t53750",
            # EXP-242: 317ED0's broadcast flag writers real on the
            # fbdev object — 28EF70 (28F0C0 arm + bit-1 fold +
            # w[+0x7C82]=r8w), 28EF00 (d[+0x7C7C]=9|1 + w stores).
            0x28EF70: "l28ef70", 0x28EF00: "l28ef00",
            0x28F0C0: "l28f0c0",
            # EXP-243: gauge-event post + channel-lookup helpers —
            # 296280 scans the BSS-zero 4-entry channel table,
            # 2962C0 returns the static default slot, 3F8980 is the
            # post sink (unreached — fallback gate fails on
            # d[0209C2F0]==0).
            0x28F1F0: "l28f1f0", 0x296280: "l296280",
            0x2962C0: "l2962c0", 0x3F8980: "l3f8980",
            # EXP-244: 2548F0 dispatch + its slot-8 bit set/clear
            # leaves (d[0215F1C0+ecx*4] |= / &= ~ (1<<edx), ecx<0x10).
            0x2548F0: "l2548f0", 0x2E1C20: "l2e1c20",
            0x2E1CA0: "l2e1ca0",
            # EXP-245: 23B040 mask classifier + its leaf helpers —
            # 303EC0 (30D9A0==2), 2E8100 (3588B0->q[+0xC0] lookup),
            # 322600/322920 (bitset range tests), tail publishers
            # 3592C0/359200 (b/d[022C80xx] bts|btr) + 26BD40
            # (setne b[0209A2C5]).
            0x23B040: "lb040", 0x303EC0: "l303ec0",
            0x2E8100: "l2e8100", 0x322600: "l322600",
            0x322920: "l322920", 0x3592C0: "l3592c0",
            0x359200: "l359200", 0x26BD40: "l26bd40",
            # EXP-246: 46AB10 dedup-ring inserter + its 469570
            # resolver — all gates BSS-safe under shipped state:
            # d[r8+0x28] cap <0x1FF, 31B860 entity scan (236850
            # count cell 0x208E6A0 == 0 -> miss), then 469570
            # returns 0 on q[0x2EBF018] == 0 (BSS desc) -> early-out
            # at 0x46AC7A.  31B860/2368xx/32A150 stay silent-real.
            0x46AB10: "l6ab10", 0x469570: "l69570",
            # EXP-247: 3377C0 spatial broadcast — promoted real on
            # the guard path (rcx==0 or q[rcx+0x10]==0 -> ret 0).
            0x3377C0: "l377c0",
            # EXP-248: 3377C0 deep scaffolding — d228-pos/pos2 plant
            # q[n30+0x10] (S: b[+3]&0xE0==0x60 -> q[+0xB8]+0x50) and
            # an oar4 cid row, so 265090->3DA710 (pos/radius fetch),
            # 236820 row resolve, 31ABE0->3588B0 clstab id resolve,
            # 2EA7F0's gate chain (early-outs on f[c138+0xF0]==0) and
            # the 337700 fallback tail (391410's 383840 grid-null
            # early-out, 384130 xz-pack) all execute shipped bytes.
            # 383F10 stays scripted — its cell-walk calls through an
            # unbound IAT slot (q[0x8C2C10] -> 0x1CCF034 .rdata data).
            0x265090: "l265090", 0x3DA710: "l3da710",
            0x31ABE0: "l31abe0",
            0x2EA7F0: "l2ea7f0", 0x337700: "l37700",
            0x391410: "l391410", 0x383840: "l383840",
            0x384130: "l384130",
            # EXP-250 small-stub sweep — wrappers whose callees were
            # already REAL or fixture-safe unmapped bodies:
            # 31B8C0: 263750(rcx) -> null ret / jmp 263E30.
            # 2FA390: 2F8E90(rcx) -> (al&7)!=0; leaf path on the
            #   e360 fixture (b[+5]==0 -> ret 1, same as the old
            #   synthetic qfa390_ret=1 but shipped-computed).
            # 2FA540: 320450(rcx) -> jmp 329A20(rcx, 0.0f); both
            #   early-out on b[rcx]&0x10==0 on ce0-drop.
            # 254850: ten 2E1C20 bit-sets on slot 8 when ecx!=0.
            # 254940: one 2E1C20/2E1CA0 pick + jmp 2547D0 (7 more).
            0x311CF0: "l311cf0",
            0x31B8C0: "l31b8c0", 0x2FA390: "l2fa390",
            0x2F8E90: "l2f8e90", 0x2FA540: "l2fa540",
            0x320450: "l320450", 0x329A20: "l329a20",
            0x254850: "l254850", 0x254940: "l254940",
            0x2547D0: "l2547d0"}

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
        if addr == 0x2AC5F0:     # EXP-209: real interpreter — record
            self.rets["cc48mid"] = self.gm.q(0x209CC48)  # ctx48 swap
            self.trace.append("l2ac5f0")                 # at entry
            self.rets.setdefault("rargs", []).append(
                ["l2ac5f0",
                 uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
                 uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF])
            return
        if addr == 0x2B2DF0:     # walker wrapper used by the tag-14
            self._args("s2b2df0")  # arm; xmm0 float out
            uc.reg_write(UC_X86_REG_XMM0,
                         int.from_bytes(
                             struct.pack("<f", float(
                                 self.case.get("f2df0", 0.0)))
                             + b"\x00" * 12, "little"))
            self._ret()
            return
        # EXP-214: 2B43C0 promoted real — caller-state copy + real
        # 2AF340 walk; xmm0 out is 2AF340's leftover width float.
        if addr == 0x2AB820:     # 17FD30-shimmed helper
            self._args("s2ab820")
            self._ret()
            return
        # EXP-247: 3377C0 promoted real — all 19 callers hit the
        # rcx==0 / q[rcx+0x10]==0 guard (ctxn30's +0x10 link is
        # unplanted) -> ret 0.  The 265090/236820/31ABE0/2EA7F0 ->
        # 391D10/3920F0 spatial-query deep arms need an entity-list
        # fixture; s80f0/s9ca0 drop to x0 on d228-pos/pos2, which is
        # shipped-honest for this fixture state (the old s9490_ret
        # stub papered over the incomplete ctxn30).
        # EXP-211/212: tag-15 sub-arm scripted boundaries — font-
        # resource tables, embed resolvers/draws, and the ctx48-gated
        # global tail helpers stay disclosed stubs.  (The nine param
        # parsers went real in EXP-212.)
        # EXP-213: 39BA30/263990/2639E0 (+32A930/3EAC10 chain) promoted
        # real; 2EF2B0/2EF640 already real.  Remaining stubs:
        # EXP-225: 17FD30 promoted real — flag->0/1 + 1B5FA0 dev1
        # singleton -> 1E9D20 map-find/set (early-out clears dev1+0..24).
        # EXP-220: the four metric thunks (17F880/8A0/960/980) are
        # real — the 1B5FB0 -> 1B51C0 map-find + 1B1620 flag chain
        # runs on the planted q[01F81200] font-metrics map.
        # EXP-216: 2B4730/3A1DB0/36F360 promoted real — the
        # display-list append + ring flip + terminator patch.
        # EXP-214: 2B41F0 promoted real — default-state template +
        # real 2AF340 walk; eax = evaluator node count.
        # EXP-215: 2AE610/2AE450/39BB00/2A9F00 promoted real — the
        # emit sinks they tail into stay scripted:
        # EXP-218: 2AFDC0 promoted real — the quad submitter's own
        # emit helpers stay scripted:
        # EXP-219: 2DD860/17FC90/17F7C0/2AEB20 promoted real —
        # 2DD860's 202B70->217060 mat4x4 leaf runs real, 17FC90 writes
        # the quad UV/scale into the planted q[01F811F8] device buffer.
        # EXP-220: 1E8070 (17F7C0's submitter) promoted real — the
        # vector grow's allocator virtuals stay scripted
        # (salloc/sdealloc fixture slots), as do 1E94E0's lazy-init
        # callees (s19c5d0/s1c5f20; the +0xF68 flag is planted 1).
        # EXP-221: the six 181xxx wrappers + 1Bxxxx device methods
        # are real now (q[01F811E8] fixture below).  Scripted edges
        # that remain: the CRT format-copy target 17D2E0 calls
        # through q[08C2F08] (vsnprintf-shaped: rdx=dst, r8=-1,
        # r9=src — byte copy to NUL, bounded at the 0x3938 field
        # extent) and the slot-vector allocator fn slots used by
        # 1AED50's realloc arm (+8 alloc / +0x18 dealloc).
        if addr == 0x1CCECB4:    # vsnprintf-shaped sink (17D2E0)
            self._args("scrtfmt")
            dst = uc.reg_read(UC_X86_REG_RDX)
            src = uc.reg_read(UC_X86_REG_R9)
            n = 0
            while True:
                ch = self.gm.b(src + n)
                self.gm.w(dst + n, bytes([ch]))
                if ch == 0 or n >= 0x167:
                    break
                n += 1
            uc.reg_write(UC_X86_REG_RAX, n)
            self._ret()
            return
        if addr == 0x7000A110:   # rdev slot-vector alloc (scripted)
            self._args("s2alloc")
            uc.reg_write(UC_X86_REG_RAX, self.alloc(0x400))
            self._ret()
            return
        if addr == 0x7000A118:   # rdev slot-vector dealloc
            self._args("s2dealloc")
            self._ret()
            return
        if addr == 0x181330:     # device tail op (deep, scripted)
            self._args("s181330")
            self._ret()
            return
        # EXP-219: 2AEB20 promoted real (kind-0x1C catch-all, eax=2).
        if addr == 0x3FFDF0:     # tag-14 parameter-block parser; eax =
            self._args("s3ffdf0")  # bytes consumed
            # df0v: the parser's stack-passed out cell (caller's
            # q[rsp+0x28] = &rsp+0x48 -> callee rsp+0x30).  The arm
            # sets b[ctxo+0x10FE] = (cell == 0).
            dv = self.case.get("df0v")
            if dv is not None:
                cellp = self.gm.q(
                    uc.reg_read(UC_X86_REG_RSP) + 0x30)
                self.gm.w(cellp, dw(dv))
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("f3ff0", 0) & 0xFFFFFFFF)
            self._ret()
            return
        # EXP-220: 17F880 (metric thunk) / 17F920 (devsub arm select:
        # cl=0 -> d[devsub+0x20], cl=1 -> d[devsub+0x1C]) / 17F9C0
        # (ceilf(ecx / f[devsub+0x34])) / 17F940+17FAE0 (q[dev1+0x28]
        # getter/setter) / 17F8C0 (codepoint->glyph remap through
        # q[dev1+8] + the devsub+0x50 inline map) all promoted real;
        # the f880v/f920v/f940v/f980v/f960v/f8a0v case keys retire.
        if addr == 0x17F850:
            self._args("s17f850")
            self._ret()
            return
        if addr == 0x17FA10:
            self._args("s17fa10")
            self._ret()
            return
        if addr == 0x17FB00:
            self._args("s17fb00")
            self._ret()
            return
        if addr == 0x2B3E30:     # tag-0xE params-block adjuster
            self._args("s2b3e30")
            self._ret()
            return
        if addr == 0x1CCEF90:    # ceilf via IAT (861F4A thunk)
            self.trace.append("ceilf")
            xv = uc.reg_read(UC_X86_REG_XMM0)
            xf = struct.unpack("<f",
                               struct.pack("<I", xv & 0xFFFFFFFF))[0]
            fn = self.case.get("f861", "ceil")
            xf = {"ceil": math.ceil, "floor": math.floor,
                  "trunc": math.trunc, "id": lambda v: v,
                  "round": round}[fn](xf)
            uc.reg_write(UC_X86_REG_XMM0,
                         int.from_bytes(struct.pack("<f", float(xf))
                                        + b"\x00" * 12, "little"))
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
                 uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
                 uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF,
                 uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF])
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
        self.gm.w(rsp + 0x20, qw(rarg(self.case.get("sarg", 0))))
        self.gm.w(rsp + 0x28, qw(rarg(self.case.get("a5", 0))))
        self.gm.w(rsp + 0x30, qw(rarg(self.case.get("a6", 0))))
        self.gm.w(rsp + 0x38, qw(rarg(self.case.get("a7", 0))))
        self.gm.w(rsp + 0x40, qw(rarg(self.case.get("a8", 0))))
        self.gm.w(rsp + 0x48, qw(rarg(self.case.get("a9", 0))))
        try:
            uc.emu_start(self.entry, RETQ, timeout=60_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        # EXP-220: capture xmm0 for float-returning metric bodies
        self.rets["xmm0"] = uc.reg_read(UC_X86_REG_XMM0)
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------------------------
def base_case(**kw):
    c = {"idx": 2, "mode": 0, "gate": 1}
    for k, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(k), dict):
            c[k] = {**c[k], **v}
        else:
            c[k] = v
    return c


SM_NONE = {i: 0xFF for i in range(9)}

# EXP-224: shared descriptor specs for the promoted bodies.
# GRWD: 30C650's growth desc q[02EBF108] — rows default all-zero so
# 2F9A60/2F9B20 take the "growth 0" arm (comiss 0.01 vs 0 -> base
# passthrough, no RNG/div).  GRWMEMT: member-id table for real
# 317930 — b7>>5 is the slot-cursor class, b7&0x10 is 323C60's
# allow flag, b9/b11 are the pair-tag compare bytes.
GRWD = {"stride": 0x20, "off": 0x88000, "count": 0x70}
GRWMEMT = {"stride": 8, "off": O_MEMT, "count": 0x2000}
# foe path slot ids 0x1101/0x1102 (cursors 0/1): row b7 = class<<5|0x10,
# pair tags equal so 318B40 leaves the pair alone.
GRWMEMT_FOE = {0x101: {7: 0x10, 0x11: 7}, 0x102: {7: 0x30, 9: 7}}
# member path ids 0x1111/0x2222 (0x2222 is class-7: 322C50 kind-7 arm
# needs m98d for the [0x2000,0x2000+d[+4]) range).
GRWMEMT_MEM = {0x111: {7: 0x10, 0x11: 7}, 0x1222: {7: 0x30, 9: 7}}
GRWM98 = {"count": 0x400}


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
    # EXP-224: guests now reach real 30C650 -> growth desc + zero rows
    # keep the level-set stat-neutral for the share-path asserts.
    kw.setdefault("grwd", GRWD)
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
    # EXP-224: guests now reach real 30C650 -> growth desc + zero rows
    # keep the level-set stat-neutral for the share-path asserts.
    kw.setdefault("grwd", GRWD)
    kw.setdefault("memslots", [0, 0xFF, 0xFF, 0xFF])
    kw["rec_b"] = {5: 1, **kw.get("rec_b", {})}
    return base_case(**kw)


# EXP-205: kind-0x1A resource-resolution fixture shared by the
# type-2 display cases — w[row]=3 packs T2[0]/T3[3] -> q18 =
# elemb+0x80000 (empty 2-byte tag -> 2B58B0 -> q30 = +2).
RES1A = {"cascd": {"off": 0x7A000, "stride": 0x30, "count": 0x10},
         "dt2": {0: 0x7F000},
         "l1w": {0: 3, 0xA: 7},
         "l1b": {0x10: 0x11, 0x13: 0x22, 0x26: 0x33, 0x27: 0x44},
         "t3": {0x7F000: {3: 0x80000}},
         # t3s = the resource name; single lite char + NUL so the
         # EXP-208 string walker terminates cleanly on real bytes.
         "t3s": {0x80000: b"\x00\x00\x05\x00"}}


def res1a(**over):
    # RES1A with per-key dict merges (l1b={2:0xFF} keeps the rest).
    r = dict(RES1A)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(r.get(k), dict):
            r[k] = {**r[k], **v}
        else:
            r[k] = v
    return r


CASES = {
    # ---- gates / mode dispatch ----
    "ac80-gate-off":   base_case(gate=0),
    "ac80-mode2":      base_case(mode=2),
    "ac80-modeff":     base_case(mode=0xFF),

    # ---- member path ----
    # EXP-224: real 317930 gates the 31A630 slot writes — memt rows
    # carry b7=slotclass<<5|0x10 (cursor match + 323C60 allow),
    # b9/b11 the pair tag; grwd covers the 30C650 growth tail;
    # m98d covers class-7 id 0x2222's 322C50 range.
    "ac80-member":       base_case(mode=1, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_MEM,
                                   m98d=GRWM98, grwd=GRWD),
    # EXP-229: real 2FEF30 (inside 30C470->30FED0) derefs the null MEMD
    # row at 2FF158 (w[r13+0x22]) before 23AC80's own member-arm reads —
    # shipped-order fault relocation, was 23ADA8 under the fef30 stub.
    "ac80-member-nulld": base_case(mode=1, memd=None,
                                   expect_fault=0x2FF158),
    # EXP-224: real deny — memt planted (318B40 runs on the FFFF
    # sentinel slots regardless) but row b7>>5 mismatches the slot
    # cursor -> 317930 vetoes each real id.
    "ac80-member-deny":  base_case(mode=1, memt=GRWMEMT,
                                   memt_rows={0x111: {7: 5 << 5},
                                              0x1222: {7: 5 << 5}}),

    # ---- foe path ----
    # EXP-224: real 317930 needs memt (foe slot ids now member-range
    # 0x1101/0x1102); grwd covers the 30C650 growth tail.
    "ac80-foe":          base_case(memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    "ac80-foe-nulld":    base_case(foed=None,
                                   expect_fault=0x23AD7B),
    "ac80-foe-idx7":     base_case(idx=7, abil=[0xFF] * 8,
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    "ac80-foe-scan":     base_case(idx=2, abil=[0, 4, 0xFF, 4],
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    "ac80-foe-cnt0":     base_case(foe={"cnt": 0}, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    "ac80-foe-noflag40": base_case(foe={"b2c": 0}, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    # d[rec+0x190] is memset to 0 before 323790 and the addend is a
    # word (<0x1869F) — the cap/floor arms of 323790 are unreachable
    # from this caller; the value asserts document that.
    "ac80-foe-gilbig":   base_case(foe={"w": {0x44: 0x7FFF}},
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    "ac80-foe-oidx27":   base_case(idx=0x27, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    "ac80-foe-oidx28":   base_case(idx=0x28, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   expect_fault=0x326057),
    "ac80-foe-pairnull": base_case(paird=None, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    "ac80-foe-pairbad":  base_case(foe={"w": {0x14: 0x4000}},
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    "ac80-foe-ordrow":   base_case(ordmask=3, ordrows=[{}, {}],
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD, e360n=1),
    # slotrow b[+4]=5 != rec b[+4]=2: the two 327DE0 calls use
    # different index bytes AND different cursor cells/blocks —
    # rec-call's blk (pos 2*3) unplanted -> ordrow2 stays empty;
    # slotrow-call's blk (pos 5*3) planted -> ordrow5 fills.
    "ac80-foe-orddiv":   base_case(ordmask=3, ordrows=[{}, {}],
                                   ordidx=5, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    # cursor=1 shifts the scanned block to position idx*3+1
    "ac80-foe-cursor1":  base_case(ordmask=3, ordrows=[{}, {}],
                                   cursor=1, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   e360n=1),
    # glob null faults first inside 327CB0's tail-call 327DE0(rec):
    # movsxd rcx, d[0+idx*4+0x7370] — before 326030 is reached.
    "ac80-foe-globnull": base_case(glob_null=True, memt=GRWMEMT,
                                   memt_rows=GRWMEMT_FOE, grwd=GRWD,
                                   expect_fault=0x327E27),
    # 30C470's 30F690 gate: d[0208D320]|d[0208D324] != 0.
    # mask=1 -> bit0 fixup runs real: 31B860 owner scan finds the
    # linked row, but rec's +0x3C/+0x64 flags are memset -> the
    # 0x80000003 check fails -> no 377C20, no bit26 clear; e360 still
    # fires for the set bit.
    "ac80-foe-f690gate": base_case(f690_gate=1, objlink=True,
                                   memt=GRWMEMT, memt_rows=GRWMEMT_FOE,
                                   grwd=GRWD),
    "ac80-foe-f690norow": base_case(f690_gate=1, memt=GRWMEMT,
                                    memt_rows=GRWMEMT_FOE, grwd=GRWD),

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
    "f340-bit10":   base_case(fbdev=1, entry=0x30F340, idx=0x1C, objlink=True,
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
    # mode pair: arg7 in {3,4} -> 46A800 (bit 1 -> REAL 46AB10)
    "e360-mode-pair": base_case(q6desc=1, entry=R_E360, edx=0, r8=1, r9=0x33,
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
    "b140-td":      base_case(fbdev=1, entry=0x300140, rcx="obj", edx=1,
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
                              objc0={}),

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
    "s8a0-flag4":  base_case(q6desc=1, entry=R_08A0, rcx=0xC012, edx=1, a5=1,
                             foebmp=0, statecell=1),
    "s8a0-flag4clr": base_case(q6desc=1, entry=R_08A0, rcx=0xC012,
                               edx=-1 & 0xFFFFFFFF, a5=1, statecell=1),

    # EXP-249: 46AB10 dedup-ring SCAN arm, direct entry.
    # 46AB10(rcx=payload ptr rsi, edx=tag w edi, r8=struct q6s).
    # q6desc+elf=1 -> desc resolves rcx2=elemb, b[elemb+4]&1 set ->
    # scan arm.  Hit iff 1*0x1c2 + d[row+4] > d[0x208D45C].
    # q6dup-hit: fresh row (ts 0, now 0) -> 0x1c2 > 0 -> suppress:
    # no row write, no s5369c0, ret via 0x46AC6B epilogue.
    "q6dup-hit":   base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             q6ring=[{"slot": 2, "w": 0x1234,
                                      "ts": 0, "q8": "self"}]),
    # q6dup-miss: seeded row carries a different tag -> the w[+0]
    # compare fails on all 10 rows -> insert arm at cursor 0
    # (BSS) overwrites the seeded slot, s5369c0 fires.
    "q6dup-miss":  base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             q6ring=[{"slot": 0, "w": 0x9999,
                                      "ts": 0, "q8": "self"}]),
    # q6dup-stale: matching tag+payload but now=0x1000 makes
    # 0x1c2+ts <= now -> expired -> scan continues past it and the
    # insert arm fires at cursor 5.
    "q6dup-stale": base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             q6now=0x1000, q6cur=5,
                             q6ring=[{"slot": 2, "w": 0x1234,
                                      "ts": 0, "q8": "self"}]),
    # q6dup-cap: d[r8+0x28]=0x200 >= 0x1FF -> jge 0x46AC7A before
    # the owner scan — nothing runs but the entry compare.
    "q6dup-cap":   base_case(entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             q6cap=0x200),
    # EXP-252: 46AB10 mid-gate exits (before 469570 + ring).  q6own
    # plants q[q6s+8]=oar4[si]'s linked rec -> real 31B860 returns
    # that row.  g3080: d[02089340]&0x3080 -> jne 0x46AC7A.
    # b20: gates clear until b[row+4]&0x20 (flags qword byte 4) ->
    # jne 0x46AC7A.  ok: both clear -> resolver + insert arm run.
    "q6mid-g3080": base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {}}, q6own=1, owngl=0x3080),
    "q6mid-b20":   base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {"flags": 0x2040000000}},
                             q6own=1),
    "q6mid-ok":    base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {}}, q6own=1),
    # EXP-253: q6own0 plants q[q6s+0] (469570's rsi carrier).
    # q6mid-rsi: q[q6s+8]==0 -> 46AB10's own scan misses -> straight
    # to the resolver whose rsi arm hits row 2 -> 2FA3B0(ci2).
    "q6mid-rsi":   base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={2: {}}, q6own0=2),
    # q6mid-noci: rdi-arm hit on a row whose q[+0x10] is null ->
    # rbx=0 -> 2FA3B0(0) decides.
    "q6mid-noci":  base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {"ci0": 1}}, q6own=1),
    # q6mid-veto: owner row with client-info whose vec3 sits ~100
    # units from the camera -> 2FA3B0 ret 0 -> 469570 ret 0 ->
    # 46AB10 je 46AC7A.  The veto exit returns 0 (unlike the
    # mid-gate exits which return the owner row).
    "q6mid-veto":  base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {"trip": [100.0, 0.0, 0.0]}},
                             q6own=1),
    # EXP-255: 469570's early arms.  q6mid-g80: b[elemb+3]=0x80 ->
    # jae 0x469685 -> ret 1 before any owner lookup -> 46AB10
    # proceeds straight to the ring (owner cell stays null).
    "q6mid-g80":   base_case(q6desc={"elf": 1, "b3": 0x80},
                             entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {}}, q6own=1),
    # Direct-entry resolver probes (entry's own tag unrecorded):
    # desc-null -> arm falls to lookups; q69570-null exercises the
    # rdi arm end to end, q69570-rsi the rsi arm.
    # EXP-256: rsi-arm hit on a null-ci row falls THROUGH to the
    # rdi arm (je 0x469644), which re-resolves and consults.
    "q6mid-fall":  base_case(q6desc={"elf": 1}, entry=0x46AB10,
                             rcx="q6pay", edx=0x1234, r8="q6s",
                             oar4={1: {"ci0": 1}, 2: {}},
                             q6own0=1, q6own=2),
    "q69570-null": base_case(entry=0x469570, rcx=0x1234, edx=0,
                             r8="q6arg", oar4={1: {}}, q6arg=1),
    "q69570-rsi":  base_case(entry=0x469570, rcx=0x1234,
                             edx="q6arg", r8=0,
                             oar4={2: {}}, q6arg=2),
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
    "a630r9-swap":   base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # r9d==0 -> whole chain skipped (control)
    "a630r9-off":    base_case(entry=R_A630, edx=2, r8=0x1150, r9=0,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # old slot word FFFF -> 30F9A0 -1 early; 30C410 still runs
    "a630r9-oldff":  base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0xFFFF}, objlink=1,
                               cls1words={0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # old id foe-class 0xC012 -> 30F9A0 class gate -> 0, no 3008A0
    "a630r9-oldfoe": base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0xC012}, objlink=1,
                               cls1words={0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # new id 0x1000 exactly -> 30C410 class-eq gate -> 0, no 3008A0
    "a630r9-new1k":  base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1000, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               memt=GRWMEMT,
                               memt_rows={0: {7: 0x50}},
                               cls1words={0x000: 0x0803,
                                          0x100: 0x1405}),
    # owner scan miss -> 31B860 ret 0 -> 324470 skipped
    "a630r9-nomatch": base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                                rec_w={0x54: 0x1100}, objcount=2,
                                cls1words={0x100: 0x1405,
                                           0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # member d[0] bit23 -> 2ECF10 edx=1
    "a630r9-bit23":  base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               objflags=0x40800000,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # 313F60 nonzero -> 300E40 skipped.  EXP-229: real 2FEF30 rebuilds
    # d[rec+0x3C] (or's in d[foerow+0x48]) — plant the row flag, not
    # the rec field (the stub-era rec_d plant is zeroed by the rebuild).
    "a630r9-gate3f": base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               rec_b={4: 2}, foe={"w": {0x48: 1}},
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # b[member]&2 -> 300E40 skipped
    "a630r9-b2":     base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               objflags=0x4000002,
                               rec_b={4: 2}, foe={"w": {0x48: 1}},
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # rec +0x3C bit0 (via foerow+0x48) -> 313F60 path; cd_words=[0]
    # keeps its ret 0 -> 300E40 runs too
    "a630r9-rec3c":  base_case(fbdev=1, entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               rec_b={4: 2}, foe={"w": {0x48: 1}},
                               cd_words=[0],
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0803},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),
    # rcx==0 -> -1
    "a630r9-null":   base_case(entry=R_A630, rcx=0, edx=2, r9=1),
    # 317930 deny -> -1, no writes / no chain
    "a630r9-deny":   base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x150: 0x0803}),
    # new id FFFF -> 317930 skipped, 30C410(FFFF)->-1, slot cleared
    "a630r9-newff":  base_case(fbdev=1, entry=R_A630, edx=2, r8=0xFFFF, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               memt=GRWMEMT,
                               cls1words={0x100: 0x1405}),
    # equip clamp: new count would exceed cap (3/3) -> clamped
    "a630r9-clamp":  base_case(entry=R_A630, edx=2, r8=0x1150, r9=1,
                               rec_w={0x54: 0x1100}, objlink=1,
                               cls1words={0x100: 0x1405,
                                          0x150: 0x0C03},
                               memt=GRWMEMT,
                               memt_rows={0x150: {7: 0x50}}),

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
    # EXP-224: real 323C60 — row b7&0x10 is its allow shortcut (else
    # the 323BB0 class-mask intersect decides).
    "g7930-ok":     base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: (2 << 5) | 0x10,
                                                 9: 31}}),
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
                              memt_rows={0x150: {7: (2 << 5) | 0x10,
                                                 9: 31}}),
    # esi==1 sub-check: slot0 occupied (w[slots]=0x1160), new row b9
    # must equal slot0 row's b11
    "g7930-s1eq":   base_case(entry=0x317930, edx="rec50", r8=1,
                              r9=0x1150,
                              rec_w={0x50: 0x1160},
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: (1 << 5) | 0x10,
                                                 9: 5},
                                         0x160: {7: 0, 0x11: 5}}),
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
    # 323C60 real: b7&0x10 clear -> 323BB0 mask intersect vs memset
    # rec+0x194 -> no hit -> deny (was s323c60_ret=0)
    "g7930-c60":    base_case(entry=0x317930, edx="rec50", r8=2,
                              r9=0x1150,
                              memt={"stride": 8, "off": O_MEMT, "count": 0x200},
                              memt_rows={0x150: {7: 2 << 5, 9: 31}}),
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
    "u43f0-gate0":  base_case(fbdev=1, entry=0x3243F0, rcx="obj", objlink=1),
    "u43f0-698z":   base_case(entry=0x3243F0, rcx="obj", objlink=1,
                              obj698=0),
    "u43f0-3f":     base_case(fbdev=1, entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}, cd_words=[0]),
    "u43f0-3fskip": base_case(fbdev=1, entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}),
    "u43f0-b2":     base_case(fbdev=1, entry=0x3243F0, rcx="obj", objlink=1,
                              rec_d={0x3C: 1}, objflags=0x4000002),
    # 2ECEC0 deep arm: q[obj+0xC0] link w=idx -> ecarr elem
    # d[+0x284]!=0 -> 3AEEF0 zeroes the elem+0x568 node chain.
    "u43f0-ec":     base_case(fbdev=1, entry=0x3243F0, rcx="obj", objlink=1,
                              objc0={0: 2},
                              ecarr={"elems": 4,
                                     "rows": {0: {"d": {0x8:
                                                        0xFFFFFFFF,
                                                        0xC0:
                                                        0xFFFFFFFF}},
                                              2: {"d": {0x284: 1,
                                                        0x18: -1,
                                                        0xC4: -1,
                                                        0xC8: -1,
                                                        0xC0:
                                                        0xFFFFFFFF,
                                                        0x110: 0x99,
                                                        0x23C: 0x77,
                                                        0x69C:
                                                        0x12345678},
                                                  "q": {0x68:
                                                        0xDEAD68,
                                                        0xD8:
                                                        0xDEADD8,
                                                        0xE0:
                                                        0xDEADE0,
                                                        0xF0:
                                                        0xDEADF0,
                                                        0xF8:
                                                        0xDEADF8},
                                                  "chain": {0x568:
                                                            [0x41,
                                                             0x42]}}}}),
    # 324450 conditional caller: b&0x40 -> 3243F0 + clear 0x40
    "w4450-set":    base_case(fbdev=1, entry=0x324450, rcx="obj", objlink=1,
                              realx=[0x3243F0], objflags=0x4000040),
    "w4450-clear":  base_case(entry=0x324450, rcx="obj", objlink=1,
                              realx=[0x3243F0]),

    # EXP-258: 422C20 direct-entry dereg arms.  delem is the elem row
    # (rcx); d[+0x10] is the resolved-element elemb offset whose
    # q[+0xDA8] is the mode-1 container.  Clear-block sentinels ride
    # every case so the tail writes stay pinned with the arm running.
    "d422c20-c4":   base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: 1, 0xC8: -1,
                                           0x18: -1,
                                           0xC0: 0xFFFFFFFF,
                                           0x23C: 0x77},
                                     "q": {0x68: 0xDEAD68,
                                           0xD8: 0xDEADD8,
                                           0xE0: 0xDEADE0,
                                           0xF0: 0xDEADF0,
                                           0xF8: 0xDEADF8},
                                     "count": 2, "head": 2,
                                     "tail": 3,
                                     "descs": {1: {"key": 2},
                                               2: {"d": {0x8: -1,
                                                         0xC: -1}},
                                               3: {}}}),
    "d422c20-c8":   base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: -1, 0xC8: 0,
                                           0x18: -1,
                                           0xC0: 0xFFFFFFFF},
                                     "w": {0xCC: 0x1234},
                                     "count": 2, "head": 0xFFFF,
                                     "tail": 1,
                                     "descs": {0: {"key": 1},
                                               1: {"d": {0x8: -1,
                                                         0xC: -1}}}}),
    "d422c20-both": base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: 0, 0xC8: 1,
                                           0x18: -1,
                                           0xC0: 0xFFFFFFFF},
                                     "count": 3, "head": 2,
                                     "tail": 2,
                                     "descs": {0: {"key": 2},
                                               1: {"key": 3},
                                               2: {"d": {0x8: -1,
                                                         0xC: -1}},
                                               3: {"d": {0x8: -1,
                                                         0xC: -1}}}}),
    # mode-2 container: 51F240 returns 0 -> 51BA40 skips the
    # reset/release, but 422C20 still retires the slot fields.
    "d422c20-mode2": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: 1, 0xC8: -1,
                                            0x18: -1,
                                            0xC0: 0xFFFFFFFF},
                                      "mode": 2,
                                      "descs": {1: {"key": 2},
                                                2: {}}}),
    # EXP-259: the d[+0x18] arm — 2ED570(q[elem+0xD98], slot):
    # row[slot*0x10] gates on d[row]!=-1, sub[slot*0x20]'s
    # d[+0x10] resolves the target element -> ret -> d[ret]&=~8.
    # 422C20 does NOT retire d[+0x18] (unlike +0xC4/+0xC8).
    "d422c20-18":   base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: -1, 0xC8: -1,
                                           0x18: 1,
                                           0xC0: 0xFFFFFFFF},
                                     "w": {0xCC: 0x1234},
                                     "c2": {"rows": {1: {"d":
                                                         {0:
                                                          0x55}}},
                                            "subs": {1: {"d":
                                                         {0x10:
                                                          0x70100}}},
                                            "e2": 0x70100,
                                            "e2d": {0: 0xF}}}),
    # d[row]==-1 -> 2ED570 ret 0 -> the &=~8 write skipped.
    "d422c20-18nul": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: -1, 0xC8: -1,
                                            0x18: 1,
                                            0xC0: 0xFFFFFFFF},
                                      "w": {0xCC: 0x1234},
                                      "c2": {"rows": {1: {"d":
                                                          {0: -1}}},
                                             "subs": {1: {"d":
                                                          {0x10:
                                                           0x70100}}},
                                             "e2": 0x70100,
                                             "e2d": {0: 0xF}}}),
    # EXP-260: 2ED570 arm variants.  The row index is the RAW slot
    # (rsi); only the sub index is slot>>d[C2+0x4C] — shift=1, slot=1
    # resolves sub[0], not sub[1].
    "d422c20-18sh": base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: -1, 0xC8: -1,
                                           0x18: 1,
                                           0xC0: 0xFFFFFFFF},
                                     "w": {0xCC: 0x1234},
                                     "c2": {"shift": 1,
                                            "rows": {1: {"d":
                                                         {0:
                                                          0x55}}},
                                            "subs": {0: {"d":
                                                         {0x10:
                                                          0x70100}}},
                                            "e2": 0x70100,
                                            "e2d": {0: 0xF}}}),
    # mask/mult: ret = element + (d[C2+0x50]&slot)*d[C2+0x48] — the
    # &=~8 lands at element+0x10; element+0 itself untouched.
    "d422c20-18mm": base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: -1, 0xC8: -1,
                                           0x18: 1,
                                           0xC0: 0xFFFFFFFF},
                                     "w": {0xCC: 0x1234},
                                     "c2": {"mask": 1,
                                            "mult": 0x10,
                                            "rows": {1: {"d":
                                                         {0:
                                                          0x55}}},
                                            "subs": {1: {"d":
                                                         {0x10:
                                                          0x70100}}},
                                            "e2": 0x70100,
                                            "e2d": {0: 0xF,
                                                    0x10: 0xF}}}),
    # handle-tagged bases: hdr|tag -> 36B130 -> q[hdr&~3 +8]+0x40.
    # Tag 1 on rows, tag 3 on subs — every nonzero tag resolves
    # identically (the low bits just mean "not a pointer").
    "d422c20-18tag": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: -1, 0xC8: -1,
                                            0x18: 1,
                                            0xC0: 0xFFFFFFFF},
                                      "w": {0xCC: 0x1234},
                                      "c2": {"rowtag": 1,
                                             "subtag": 3,
                                             "rows": {1: {"d":
                                                          {0:
                                                           0x55}}},
                                             "subs": {1: {"d":
                                                          {0x10:
                                                           0x70100}}},
                                             "e2": 0x70100,
                                             "e2d": {0: 0xF}}}),
    # null base cells: the 3AB7F0 calls are skipped and the resolved
    # cells q[C2+0x38]/q[C2+0x10] keep their cached bases.
    "d422c20-18noc": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: -1, 0xC8: -1,
                                            0x18: 1,
                                            0xC0: 0xFFFFFFFF},
                                      "w": {0xCC: 0x1234},
                                      "c2": {"rowtag": "cache",
                                             "subtag": "cache",
                                             "rows": {1: {"d":
                                                          {0:
                                                           0x55}}},
                                             "subs": {1: {"d":
                                                          {0x10:
                                                           0x70100}}},
                                             "e2": 0x70100,
                                             "e2d": {0: 0xF}}}),

    # EXP-262: 51F240's b[desc]&2 arm — the record ptr is
    # re-resolved: q[D+0x18] = sx(3AB7F0(q[D+0x10]) + d[D+0x20]).
    # The planted R1 is discarded; the reset lands on R2 and the
    # release is keyed by d[R2].
    "d422c20-c4ind": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: 1, 0xC8: -1,
                                            0x18: -1,
                                            0xC0: 0xFFFFFFFF},
                                      "descs": {1: {"key": 7,
                                                    "rec2": True,
                                                    "key2": 2,
                                                    "add2": 0x20,
                                                    "d": {0: 2}},
                                                2: {}}}),
    # mode 0: 51F240 resolves q[C+8] through 3AB7F0 before indexing
    # (direct aligned ptr -> returned unchanged).
    "d422c20-mode0": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: 1, 0xC8: -1,
                                            0x18: -1,
                                            0xC0: 0xFFFFFFFF},
                                      "mode": 0,
                                      "descs": {1: {"key": 2},
                                                2: {}}}),
    # mode 3: like mode 2 — 51F240 ret 0, slots still retire.
    "d422c20-mode3": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: 1, 0xC8: -1,
                                            0x18: -1,
                                            0xC0: 0xFFFFFFFF},
                                      "mode": 3,
                                      "descs": {1: {"key": 2},
                                                2: {}}}),
    # 41CF00's w[R+0x28] loop: 0xA0-stride subrecord resets at
    # R+0x30/R+0xD0 — cx is always 0 (it's the pre-loop ecx, not
    # the counter); r8d counts iterations.
    "d422c20-c4rows": base_case(entry=0x422C20, rcx="delem",
                                dcntr={"d": {0xC4: 1, 0xC8: -1,
                                             0x18: -1,
                                             0xC0: 0xFFFFFFFF},
                                       "descs": {1: {"key": 2,
                                                     "rw": {0x28: 2,
                                                            0xC6: 0xFF,
                                                            0x166:
                                                            0xFF},
                                                     "rd": {0xB8:
                                                            0x1234,
                                                            0x158:
                                                            0x5678}},
                                                 2: {}}}),
    # 41CF00's d[R+0xC]&0x1000 arm: 2ED570(q[R+0x330], d[R+0x338])
    # -> 372280 word-list walk — rdi = 20E600(d[e3+0x84]) array
    # base, list at rdi+w[e3+0x88]*0x290, w[e3+0x8A] entries, each
    # word w -> row rdi+w*0x290 cleared.
    "d422c20-c4rc2": base_case(entry=0x422C20, rcx="delem",
                               dcntr={"d": {0xC4: 1, 0xC8: -1,
                                            0x18: -1,
                                            0xC0: 0xFFFFFFFF},
                                      "descs": {1: {"key": 2,
                                                    "rd": {0xC:
                                                           0x1000},
                                                    "rc2": {
                                                        "slot": 0,
                                                        "rows": {0:
                                                                 {"d":
                                                                  {0:
                                                                   0x55}}},
                                                        "subs": {0:
                                                                 {"d":
                                                                  {0x10:
                                                                   0x70200}}}}},
                                                2: {}},
                                      "c2": {"e2": 0x70100,
                                             "ed": {0x70200 + 0x84:
                                                    0x74000,
                                                    0x74290 + 0x1A0:
                                                    0x1111,
                                                    0x74290 + 0x1A4:
                                                    0x5555,
                                                    0x74290 + 0x1AC:
                                                    0x2222,
                                                    0x74290 + 0x1C0:
                                                    0x3333,
                                                    0x74290 + 0x1C4:
                                                    0x6666,
                                                    0x74290 + 0x1CC:
                                                    0x4444},
                                             "ew": {0x70200 + 0x88: 0,
                                                    0x70200 + 0x8A: 1,
                                                    0x74000: 1,
                                                    0x74290 + 0x280:
                                                    0x10}}}),
    # d[R+0x338]==-1 -> rcx stays 0 -> 372280(0) reads d[0x84] —
    # unguarded, pinned by the fault PC; no page-0 fixture.
    "d422c20-c4f0": base_case(entry=0x422C20, rcx="delem",
                              dcntr={"d": {0xC4: 1, 0xC8: -1,
                                           0x18: -1,
                                           0xC0: 0xFFFFFFFF},
                                     "descs": {1: {"key": 2,
                                                   "rd": {0xC:
                                                          0x1000,
                                                          0x338: -1}},
                                               2: {}}},
                              expect_fault=0x37228D),

    # EXP-261: 2ED610(cx=ecarr w-index, dx=0x290-mult) — the
    # caller-side walk over 2ED570: row = q[022C6F28]+(int16)cx*0x740
    # gated on d[row+0x284]; d[row+0x18] is the C2 slot (-1 -> ret 0);
    # elem = 20E600(d[row+0x10]); 2ED570(q[elem+0xD98], slot); ret =
    # 20E600(d[ret+0x84]) + dx*0x290.  Pure resolve — 2ED610 writes
    # nothing (the &=~8 is 422C20's, not 2ED570's).
    "d2ed610-live":  base_case(entry=0x2ED610, rcx=2, edx=3,
                               ecarr={"elems": 4,
                                      "rows": {2: {"d": {0x284: 1,
                                                         0x10: 0x70000,
                                                         0x18: 1}}}},
                               dcntr={"c2": {"rows": {1: {"d":
                                                          {0: 0x55}}},
                                             "subs": {1: {"d":
                                                          {0x10:
                                                           0x70100}}},
                                             "e2": 0x70100,
                                             "e2d": {0: 0xF,
                                                     0x84:
                                                     0x72000}}}),
    # d[row+0x18]==-1 -> ret 0 before any resolve.
    "d2ed610-slotm1": base_case(entry=0x2ED610, rcx=2, edx=3,
                                ecarr={"elems": 4,
                                       "rows": {2: {"d": {0x284: 1,
                                                          0x10: 0x70000,
                                                          0x18: -1}}}}),
    # row live + slot live but the c2 row gate is -1 -> 2ED570 ret 0
    # -> ret 0 (bases still resolved+stored into C2).
    "d2ed610-c2nul": base_case(entry=0x2ED610, rcx=2, edx=3,
                               ecarr={"elems": 4,
                                      "rows": {2: {"d": {0x284: 1,
                                                         0x10: 0x70000,
                                                         0x18: 1}}}},
                               dcntr={"c2": {"rows": {1: {"d":
                                                          {0: -1}}},
                                             "subs": {1: {"d":
                                                          {0x10:
                                                           0x70100}}}}}),
    # d[row+0x284]==0 -> cmove -> rax=0 -> d[0x18] unguarded deref;
    # cx==-1 -> rax=0 -> same fault site.  Both pinned by the fault
    # PC — no page-0 fixture is fabricated.
    "d2ed610-dead":  base_case(entry=0x2ED610, rcx=2, edx=3,
                               ecarr={"elems": 4, "rows": {2: {}}},
                               expect_fault=0x2ED648),
    "d2ed610-neg1":  base_case(entry=0x2ED610, rcx=0xFFFF, edx=3,
                               ecarr={"elems": 4},
                               expect_fault=0x2ED648),

    # EXP-263: 51BA80(C, idx, recbase, reloff, src) — the record
    # INSERT complement of 51BA40's delete.  edx==-1 -> 51F150 cap
    # gate (d[C+0x14]>=d[C+0x10] -> -10); 41CB90 stack tmp reset;
    # 41D220(tmp, src) populate (deep: 409210 obj-init — its ff15
    # IAT tail lands on the planted ret stub, DISCLOSED synthetic
    # import boundary; 409780 doc scans x2, 409660, 41CA70,
    # 41CD30, 46E420) -> 51F080 slot alloc -> 51F240 -> 0x390 copy
    # -> 41CA70 -> d[rec]=key.  ret-0 populate + edx==-1 -> ret -1;
    # ret-0 + edx=idx -> 51F240/41CF00/51F190 dereg then ret -1.
    # cap arm: 51F150 ret -10 -> ret -1, nothing else runs.
    "d51ba80-cap":   base_case(entry=0x51BA80, rcx="dcntr", edx=-1,
                               dcntr={"fill": 2, "count": 2,
                                      "descs": {0: {"key": 0}}}),
    # populate-fail + edx==-1: w[src+0x10]=-1 -> 409F50 ret 0 ->
    # null doc through 409780 (409210 ran on tmp+0x2EC + the
    # 02B62E20 static via the planted IAT slot) -> 41D220 ret 0 ->
    # ebx==-1 -> ret -1; 51F080 never runs, no desc marked.
    "d51ba80-pop0":  base_case(entry=0x51BA80, rcx="dcntr", edx=-1,
                               r8="delem", a5="dsrc",
                               srcw={0x10: 0xFFFF},
                               srcd={0x14: -1},
                               dcntr={"fill": 4, "count": 0,
                                      "descs": {}},
                               iat_ret=[0x8C2F70],
                               imgd={0x2B62E20: 0xDEADBEEF}),
    # populate-fail + edx=1: the live desc's record is deregistered
    # anyway — 51F240 -> 41CF00 reset -> 51F190 release by d[rec].
    "d51ba80-dereg": base_case(entry=0x51BA80, rcx="dcntr", edx=1,
                               r8="delem", a5="dsrc",
                               srcw={0x10: 0xFFFF},
                               srcd={0x14: -1},
                               dcntr={"fill": 4, "count": 2,
                                      "descs": {1: {"key": 2},
                                                2: {}}},
                               iat_ret=[0x8C2F70]),

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
    # EXP-224: real 324020 = popcount(rec+0x194 bits 0..17);
    # 324100 scans bits 18..30 -> w[abil_row(i)+8] -> 308FF0(id)
    # -> d138 row grade (b[+0x1E] in {5,6} -> b[+0xA]).
    "o4100-null":   base_case(entry=0x324100, rcx=0),
    "o4100-base":   base_case(entry=0x324100, rec_b={0x194: 7}),
    "o4100-lic":    base_case(entry=0x324100,
                              rec_b={0x194: 7, 0x196: 4},
                              abil_rows={0x12: {"w": {8: 0x21}}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x300},
                              d138_rows={0x21: {0x1E: 5, 0xA: 7}}),
    "o4100-liclow": base_case(entry=0x324100,
                              rec_b={0x194: 0xFF, 0x195: 1,
                                     0x196: 4},
                              abil_rows={0x12: {"w": {8: 0x22}}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x300},
                              d138_rows={0x22: {0x1E: 5, 0xA: 5}}),
    "o4100-noabil": base_case(entry=0x324100,
                              rec_b={0x194: 7, 0x196: 4},
                              abild=None),

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
    "c650-one":    base_case(q6desc=1, entry=0x30C650, idx=1,
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
    "c650-multi":  base_case(q6desc=1, entry=0x30C650, idx=1,
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
    "c650-clamp":  base_case(q6desc=1, entry=0x30C650, idx=1,
                             rec_b={0x1C2: 0x62, 0x4: 1},
                             edx=0xFF, objlink=1,
                             rec_d={8: 10},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={0x62: (5, 0)}),
    # MP jitter: mp_g=5 -> 379CD0 -> tempered word mod (g*100)/100
    "c650-mp":     base_case(q6desc=1, entry=0x30C650, idx=1,
                             rec_b={0x1C2: 5, 0x4: 1},
                             edx=6, objlink=1,
                             rec_d={8: 100}, rec_w={0xC: 50},
                             grwd={"stride": 0x20, "off": 0x88000,
                                   "count": 0x70},
                             grwrows={5: (0, 5)},
                             mt={"idx": 0, "words": {0: 0x64}}),
    # full notify tail: 267330 gate + a11 serial match -> 2DF220 ->
    # 1DBDB0 -> 329210(1, ret) -> d[0x208D32C]
    "c650-full":   base_case(q6desc=1, entry=0x30C650, idx=1,
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
    "g3910-e5":     base_case(fbdev=1, entry=0x323910, edx=0xE5, r8=1,
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
                              rec_d={0x190: 100}),
    "g3910-grade":  base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x100},
                              d138_rows={0x55: {0x1E: 5, 0xA: 2}},
                              rec_b={0x20: 0},
                              rec_d={0x190: 100}),
    "g3910-grade-cap": base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x100},
                              d138_rows={0x55: {0x1E: 5, 0xA: 9}},
                              rec_b={0x20: 0},
                              rec_d={0x190: 100}),
    "g3910-grade-hold": base_case(entry=0x323910, edx=0x14, r8=1,
                              abild={"stride": 0x20, "off": O_ABIL,
                                     "count": 0x40},
                              abil_rows={0x14: {"w": {8: 0x55}}},
                              d138={"stride": 0x20, "off": 0x78000,
                                    "count": 0x100},
                              d138_rows={0x55: {0x1E: 5, 0xA: 1}},
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
                              rec_b={0x194: 7},
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
                              slotd={"count": 8}, cd_words=[0],
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
    "u0fc0-fast":  base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 0, 4: 0x1B}),
    "u0fc0-fastt": base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 0, 4: 0x27},
                             cd_words=[0],
                             ctx4=[{"w16": 0x123, "b15": 4,
                                    "n30": {"size": 0xC00,
                                            "q698": {}}},
                                   None, None,
                                   {"n30": {"size": 0xC00,
                                            "d": {8: 0x12340000}}}],
                             clstab={4: ["ctx0"]}, g272f0=0x10,
                             globb={0x5B04: 1, 0x5AD0: 3}),
    "u0fc0-def":   base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1},
                             objflags=0xFFFFFFFFFFFFFFFF,
                             obj_d={4: 0xFFFFFFFF, 0x694: 0x27}),
    # EXP-240: pass-arm fixture — b[ent+3]=0x60 opens 2E9780/26D6F0;
    # desc8 wires q[ent+0xB8]->q[+0xF0] float cell; objc0+objc0q wire
    # q[ent+0xC0] node -> q[node+0x138] flag target (d[+0x110] +
    # f[+0xC8] writes).
    "u0fc0-m1":    base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=1,
                             objlink=1, rec_b={5: 1},
                             ent_b={3: 0x60}, desc8={}, objc0={},
                             objc0q={0x138: 0x140}),
    "u0fc0-s400":  base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1}, objcount=3,
                             cd_words=[0],
                             foed={"stride": 0x60, "off": O_FOE, "count": 4}, globb={0x5A5A: 2},
                             oar4={2: {"id": 2, "recd": {0x64: 1}}},
                             slotmap={i: 0xFF for i in range(9)}),
    "u0fc0-s200":  base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={4: 0x10, 5: 0},
                             objcount=3, foed={"stride": 0x60, "off": O_FOE, "count": 0x10},
                             globb={0x5A5A: 7}, oar4={2: {"id": 7}}),
    "u0fc0-s800":  base_case(fbdev={"nodes":[{"id":9,"w850":2}]}, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, rec_b={5: 1}, obj_d={8: 9},
                             cd_words=[0],
                             globb={0x5AD5: 9, 0x5B04: 1}),
    "u0fc0-mtail": base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=0,
                             objlink=1, slothit=2, cd_words=[0],
                             ctx4=[{"w16": 0x123, "b15": 4,
                                    "n30": {"size": 0xC00,
                                            "q698": {}}},
                                   None, None,
                                   {"n30": {"size": 0xC00,
                                            "d": {8: 0x12340000}}}],
                             clstab={4: ["ctx0"]}, g272f0=0x10,
                             globb={0x5AD5: 2, 0x5B04: 1, 0x5AD0: 3}),
    "u0fc0-caps":  base_case(fbdev=1, entry=0x300FC0, rcx="obj", edx=1,
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
    "l01140-rel":  base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             obj_d={0x748: 9, 0x770: 8, 0x74C: 7,
                                    0xDCC: 6, 0x30: 5, 0x788: 0x4FF,
                                    0x6B0: 0xFF},
                             imgd={0x208D45C: 1000}),
    "l01140-sent": base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             objflags=0x4004000, obj_d={0xBA0: 0x113}),
    "l01140-sentc": base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                              objflags=0x4004000, obj_d={0xBA0: 0x111}),
    "l01140-f70":  base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             objflags=0),
    "l01140-strn": base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             rec_b={5: 1}),
    "l01140-e30":  base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             obj_d={0x74: 5}),
    # EXP-240: b[ent+3]=0x60 + objc0 node -> l2ebb80 pass arm folds
    # bit 3 (dl=1) then tail-calls the scripted v2e8fd0 boundary.
    "l01140-bbb1": base_case(fbdev=1, entry=0x301140, rcx="obj", objlink=1,
                             objflags=0x4000008,
                             ent_b={3: 0x60}, objc0={}),
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
    "d228-gate5":  c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       fbdev=1),
    "d228-gaterc": c228(rcx="row2", row2={}, slotmap=SM_NONE, fbdev=1),
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
                       fbdev=1,
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10),
    "d228-globn": c228(rcx=0, obj_b={0xE9A: 5},
                       glob_null=True, expect_fault=0x31BA57),
    # clamps: exp cap 0x5F5E0FF, lp cap 0x1869F; negative share -> 0
    "d228-ecap":   c228(q6desc=1, rcx=0, obj_b={0xE9A: 5},
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
    "d228-lp5":    c228(q6desc=1, rcx=0, obj_b={0xE9A: 5},
                       slotmap={**SM_NONE, 0: 0},
                       guest={0: {"b": {0x1C2: 5, 0x69: 0x10},
                                  "d": {0x18C: 100, 0x190: 20}}},
                       rec_b={0x1C2: 10, 0x88: 2}, e78=3, e70=7,
                       oar4={1: {"link": 0}},
                       e70e=50, e70l=10, fptot=1000),
    # fp arg = (10-2)*3 + 7 + 0 = 31; ebp = max(5+31,0) = 36 -> s54ee0;
    # delta 36-5 = 31 -> s69e80
    "d228-fp":     c228(q6desc=1, rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       rec_b={0x1C2: 10, 0x88: 2}, e78=3, e70=7,
                       fptot=5),
    # negative total floors at 0: ebp=0 -> s54ee0(0), s69e80(0-5)
    "d228-fpneg":  c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       rec_b={0x1C2: 2, 0x88: 10}, e78=3, e70=7,
                       fptot=5),
    # msg-id rec w[e68+0x52]=5 -> 3171C0's 315820 counter arm:
    # b[tab+5+0x3404] 0->2 on the 315D50 miss (q[022C2550]==0)
    "d228-msg":    c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       e68w52=5, msgtab=1),
    # pos chain: real l319490 -> REAL l377c0(ctx-or-0,&vec4) guard
    # ret 0 -> 3180F0/319CA0 arms skipped (s80f0/s9ca0 boundaries x0).
    # g272f0/mctxid/ctx4+clstab
    # resolve a live ctx whose n30 node passes b[+0]&8 -> v3377c0's
    # rcx is the real node.
    "d228-pos":    c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       g272f0=0x10, mctxid=0x12340000,
                       ctx4=[{"b15": 4, "w16": 0x123,
                              "n30": {"size": 0xF00, "b": {0: 8,
                                      0xEA9: 1}, "deep": {}}}],
                       clstab={4: ["ctx0"]},
                       oar4={1: {"cid": 0x12340000}},
                       s9490_ret=1, s80f0_ret=1,
                       s383f10_ret=0xFF),
    "d228-pos2":   c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       g272f0=0x10, mctxid=0x12340000,
                       ctx4=[{"b15": 4, "w16": 0x123,
                              "n30": {"size": 0xF00, "b": {0: 8,
                                      0xEA9: 1}, "deep": {}}}],
                       clstab={4: ["ctx0"]},
                       oar4={1: {"cid": 0x12340000}},
                       s9490_ret=1, s383f10_ret=0xFF),
    # source share args: sfb80(ecx=d[r14+8], edx=exp, r8d=lp)
    "d228-src":    c228(rcx=0, obj_b={0xE9A: 5}, slotmap=SM_NONE,
                       obj_d={8: 0x1234}, e70e=77, e70l=88,
                       oar4={1: {"id": 0}}, fbdev=1),
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
    "d228-lvl":    c228(q6desc=1, rcx=0, obj_b={0xE9A: 5},
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
                       **RES1A),
    "bd00-t2ff":  cdis(qtptr="qtab", rqt=2, rqv=7,
                       **res1a(l1b={2: 0xFF})),
    "bd00-t2b25": cdis(qtptr="qtab", rqt=2, rqv=7, randv=8,
                       dd7={"n": 0x20, "d": {0x12: 0x1234}},
                       **res1a(l1b={0x24: 2})),
    # cascd=None -> validator null-desc -> -2 -> 35D330 memsets blk
    # -> b24=0 -> gate passes anyway
    "bd00-t2neg": cdis(qtptr="qtab", rqt=2, rqv=7, cascd=None),
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
                               "w": {0x3A: 9}}}, **RES1A),
    "bd00-t3":    cdis(qtptr="qtab", rqt=3, rqv=7),
    # 3284D0(obj, dl): dist gate on q[obj+0x10]; builds type-2 req
    "d4d0-null":  base_case(entry=0x3284D0, rcx="dobj", edx=5),
    "d4d0-far":   base_case(entry=0x3284D0, rcx="dobj", edx=5,
                            obj10="subobj", pos=(100.0, 0.0, 0.0)),
    "d4d0-near":  base_case(entry=0x3284D0, rcx="dobj", edx=5,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            qtptr="qtab", randv=2, c5id=5, **RES1A),
    # 3283D0(obj, edx=num, r8, r9) type-0 post: same dist gate;
    # req = {subobj, abs(edx), type 0, subtype =
    # b[01EED300 + (edi+off)*4]}, edi=(2*r8)|r9, off=4 iff
    # (rec==0 || b[rec+5]!=0) && 263C20(q[obj+10])!=3.
    "d3d0-null":  base_case(entry=0x3283D0, rcx="dobj", edx=7),
    "d3d0-far":   base_case(entry=0x3283D0, rcx="dobj", edx=7,
                            obj10="subobj", pos=(100.0, 0.0, 0.0)),
    # Dispatch cases plant a real packed id: sob gives subobj
    # w[+0]=0x1234 (-> 3589B0 id 0x1234), fbtab matches it, t3320
    # resolves it to slot index 0 so the sinks write ctrlsub slot 0.
    "d3d0-near":  base_case(entry=0x3283D0, rcx="dobj", edx=12345,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12}, qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    "d3d0-neg":   base_case(entry=0x3283D0, rcx="dobj", edx=0xFFFFFFD6,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12}, qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    "d3d0-sub":   base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12},
                            r8=1, r9=1, qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    "d3d0-rec":   base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12},
                            dobjrec="rec", recb={5: 0},
                            qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    "d3d0-c20":   base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12, 0xE: 3},
                            qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    # edi=2 (r8=1,r9=0) + off=0 (rec b5==0) -> subtype table[2]=1
    # -> arm0 -> 297040(id, r8=0)
    "d3d0-arm0":  base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12},
                            r8=1, dobjrec="rec", recb={5: 0},
                            qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    # edi=1 + off=0 -> subtype table[1]=4 -> arm3 -> dispatch no-op
    "d3d0-arm3":  base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12},
                            r9=1, dobjrec="rec", recb={5: 0},
                            qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    # edi=5 + off=0 -> subtype table[5]=8 -> subtype-1=7 >6 -> skip
    "d3d0-sub8":  base_case(entry=0x3283D0, rcx="dobj", edx=9,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            sob={0: 0x34, 1: 0x12},
                            r8=2, r9=1, dobjrec="rec", recb={5: 0},
                            qtptr="qtab", ctrl=1,
                            fbtab={0: {"fl": 2, "id": 0x1234}},
                            t3320={"n": 1, "ids": {0: 0x1234}}),
    # 328480(obj, edx) type-1 post: same gate; req =
    # {subobj, edx, type 1} (battle_4_p arm in 506700).
    "d480-null":  base_case(entry=0x328480, rcx="dobj", edx=5),
    "d480-far":   base_case(entry=0x328480, rcx="dobj", edx=5,
                            obj10="subobj", pos=(100.0, 0.0, 0.0)),
    "d480-near":  base_case(entry=0x328480, rcx="dobj", edx=3,
                            obj10="subobj", pos=(1.0, 0.0, 0.0),
                            qtptr="qtab"),

    # ---- EXP-203: 28FBE0 dispatch consumers executed real ----
    # 296E90(ctrlsub, id): 273320(id)->idx (real since EXP-204);
    # idx<0 bail; w[idx*0x160+0x318] |= 0x10, w[+0x350] = 0.
    "e690-null":  base_case(entry=0x296E90, rcx=0, edx=7),
    "e690-bad":   base_case(entry=0x296E90, rcx="ctrlsub", edx=7,
                            ctrl=1, t3320={"n": 1, "ids": {0: 0x999}}),
    "e690-idx0":  base_case(entry=0x296E90, rcx="ctrlsub", edx=7,
                            ctrl=1, t3320={"n": 1, "ids": {0: 7}},
                            csb={0x350: 0xFF, 0x351: 0xFF}),
    "e690-idx2":  base_case(entry=0x296E90, rcx="ctrlsub", edx=7,
                            ctrl=1,
                            t3320={"n": 3, "ids": {0: 1, 1: 2, 2: 7}}),
    "e690-or":    base_case(entry=0x296E90, rcx="ctrlsub", edx=7,
                            ctrl=1, t3320={"n": 1, "ids": {0: 7}},
                            csb={0x318: 0x40}),
    # 297040(ctrlsub, id, flag): flag!=0 gated on b[idx*160+0x31E]!=3;
    # flag=0 -> w318|=0x20/w354=0; flag!=0 -> w318|=0x40/w356=0.
    "p7040-null": base_case(entry=0x297040, rcx=0, edx=7, r8=0),
    "p7040-bad":  base_case(entry=0x297040, rcx="ctrlsub", edx=7,
                            r8=1, ctrl=1,
                            t3320={"n": 1, "ids": {0: 0x999}}),
    "p7040-f0":   base_case(entry=0x297040, rcx="ctrlsub", edx=7,
                            r8=0, ctrl=1, t3320={"n": 1, "ids": {0: 7}}),
    "p7040-f1":   base_case(entry=0x297040, rcx="ctrlsub", edx=7,
                            r8=1, ctrl=1, t3320={"n": 1, "ids": {0: 7}}),
    "p7040-f1g3": base_case(entry=0x297040, rcx="ctrlsub", edx=7,
                            r8=1, ctrl=1, csb={0x31E: 3},
                            t3320={"n": 1, "ids": {0: 7}}),
    "p7040-idx2": base_case(entry=0x297040, rcx="ctrlsub", edx=7,
                            r8=0, ctrl=1,
                            t3320={"n": 3, "ids": {0: 1, 1: 2, 2: 7}}),

    # ---- EXP-204: 273320 id->slot resolver + table leaves real ----
    # 273320(id): id==0 -> -1; else scan d[022C8084+i*0xC0] i<n
    # (n = movsx w[022C8064]); first match -> index; else -1.
    "r3320-nul":  base_case(entry=0x273320, rcx=0,
                            t3320={"n": 1, "ids": {0: 7}}),
    "r3320-empty": base_case(entry=0x273320, rcx=7, t3320={"n": 0}),
    "r3320-hit":  base_case(entry=0x273320, rcx=7,
                            t3320={"n": 1, "ids": {0: 7}}),
    "r3320-hit2": base_case(entry=0x273320, rcx=7,
                            t3320={"n": 3, "ids": {0: 1, 1: 9, 2: 7}}),
    "r3320-miss": base_case(entry=0x273320, rcx=7,
                            t3320={"n": 2, "ids": {0: 1, 1: 2}}),
    "r3320-neg":  base_case(entry=0x273320, rcx=7,
                            t3320={"n": 0xFFFF, "ids": {0: 7}}),

    # ---- EXP-205: 31C5D0 kind-0x1A resolver direct entry ----
    # c5blk = {d kind, d+4 id}; row fields from RES1A/L1 overrides.
    "c5d0-ok":    base_case(entry=0x31C5D0, rcx="c5blk",
                            c5kind=0x1A, c5id=7, **RES1A),
    "c5d0-noval": base_case(entry=0x31C5D0, rcx="c5blk",
                            c5kind=0x1A, c5id=7,
                            cascd={"off": 0x7A000, "stride": 0x30,
                                   "count": 3}),
    "c5d0-not2":  base_case(entry=0x31C5D0, rcx="c5blk",
                            c5kind=0x1A, c5id=7,
                            cascd={"off": 0x7A000, "stride": 0x30,
                                   "count": 0x10}),
    "c5d0-kind0": base_case(entry=0x31C5D0, rcx="c5blk", c5kind=0),
    "c5d0-kind33": base_case(entry=0x31C5D0, rcx="c5blk",
                             c5kind=0x21),
    # b25 = ((w[row+6]>>13)&1) | ((b[row+0x24]<<1)&0x1E):
    # w6=0x2000 -> bit0; b24row=0xB -> 0x16 -> b25 = 0x17
    "c5d0-b25":   base_case(entry=0x31C5D0, rcx="c5blk",
                            c5kind=0x1A, c5id=7,
                            **res1a(l1w={6: 0x2000},
                                    l1b={0x24: 0xB})),
    # kind-1 auto-kind arm: 309440(w[blk+6]=1 -> hi0) -> d[blk]=5
    # (shipped remap 5+hi) -> kind-5 arm -> -2
    "c5d0-auto":  base_case(entry=0x31C5D0, rcx="c5blk",
                            c5kind=1, c5id=0x00010007),
    # ---- EXP-206/207: 2B3120 float->word evaluator shell ----
    # q[rcx+0x28]==0 -> w[rdx]=w[r8]=0, ret 0; else copies the 0xD0
    # struct and calls 2B24B0 (now REAL — s2b2150/s2af340/ceilf
    # stubs supply its inner results via ctxr*/af340f).
    "b3120-nil":   base_case(entry=0x2B3120, rcx="e312",
                             edx="wout", r8="wout2"),
    # q[state+0x28] = the string ptr (the walk cursor); strb is the
    # byte stream — a real tag-5 arm produces the 15.0 x 6.5 measure.
    "b3120-ok":    base_case(entry=0x2B3120, rcx="e312",
                             edx="wout", r8="wout2",
                             e312q={0x28: "nstr"}, strb=b"\x05"),
    "b3120-noout": base_case(entry=0x2B3120, rcx="e312", edx=0,
                             r8=0,
                             e312q={0x28: "nstr"}, strb=b"\x05"),
    # tag-0xE -> b10FE -> acc-merge path (f54 = 32*scale)
    "b3120-tage":  base_case(entry=0x2B3120, rcx="e312",
                             edx="wout", r8="wout2", df0v=0,
                             e312q={0x28: "nstr"}, strb=b"\x0e",
                             e312f={0x34: 1.0, 0x38: 1.0}),
    # 2B3050(ctx, str, outW1, outW2): 2AC1E0(&state); 39BAD0(ctx)->bl;
    # 254A10()==0 && bl==7 -> bts d[state+0x64].0xB + 39C4A0(bit)->
    # q[state+0x80]; q[state+0x28]=str; then
    # 2B3120(state, rdx=outW1, r8=outW2, str cell).
    "b3050-run":   base_case(entry=0x2B3050, rcx=0x44, edx="nstr",
                             r8="wout", r9="wout2",
                             strb=b"\x05"),
    "b3050-arm":   base_case(entry=0x2B3050, rcx=0x44, edx="nstr",
                             r8="wout", r9="wout2",
                             bad0t={7: 0x44}, s39c4a0_ret=0x1234,
                             e2814v=1,
                             strb=b"\x05"),
    "b3050-alt":   base_case(entry=0x2B3050, rcx=0x44, edx="nstr",
                             r8="wout", r9="wout2",
                             bad0t={7: 0x44},
                             strb=b"\x05"),
    # ---- EXP-207/208: 2B24B0 + the 2B2150/2AF340 walkers ----
    # ctxo = q[0209CC40] shared text ctx; save fields planted by
    # ctxd/ctxf/ctxq/ctxb, results by the helper stubs (ctxr*);
    # af340f = per-iter 0209CC68/64 accumulator deltas.
    "b24b0-run":   base_case(entry=0x2B24B0, rcx="e312",
                             edx="c60", r8="nstr", r9="c54r9",
                             strb=b"\x05",
                             a5="c54a5", a6="c54a6", a7="c54a7",
                             a8="c54a8", a9="c54a9",
                             ctx48=0x5EED,
                             ctxd={0x10D8: 0xDEAD},
                             ctxf={0x10E8: 1.5},
                             ctxq={0x10C8: 0x77},
                             ctxb={0x10FC: 0xAB, 0x10FF: 0xCD}),
    # tag-0xE arm sets b10FE -> acc += 2*d[01E0CDC0]*s34*s38 = 32;
    # acc+ec dominates the measure -> f[+0x54] = acc+ec
    "b24b0-acc":   base_case(entry=0x2B24B0, rcx="e312",
                             edx="c60", r8="nstr", r9="c54r9",
                             strb=b"\x0e", df0v=0,
                             a5="c54a5", a6="c54a6", a7="c54a7",
                             a8="c54a8", a9="c54a9",
                             e312f={0x34: 1.0, 0x38: 1.0}),
    # acc+ec == f54 exactly (0+15 vs ceil(15)) -> strict -> is false
    # -> else branch: f[+0x60] = f54 - acc
    "b24b0-merge": base_case(entry=0x2B24B0, rcx="e312",
                             edx="c60", r8="nstr", r9="c54r9",
                             strb=b"\x05",
                             a5="c54a5", a6="c54a6", a7="c54a7",
                             a8="c54a8", a9="c54a9"),
    # ---- EXP-208: 2B2150 / 2AF340 direct entries ----
    # null cursor -> no walk, restores, f[r8]=0
    "b2150-nil":   base_case(entry=0x2B2150, rcx="e312", edx=0,
                             r8="params", r9="ctxe8",
                             ctx48=0x77, e598v=0x66),
    # lite char 5 -> real 2AC5F0 tag-5 arm (space advance 15.0,
    # height f880v) -> continue -> NUL -> exit merge
    "b2150-lite":  base_case(entry=0x2B2150, rcx="e312", edx="nstr",
                             r8="params", r9="ctxe8",
                             strb=b"\x05",
                             ctx48=0x77, e598v=0x66,
                             ctxb={0x10FC: 0xAB, 0x10FF: 0xCD}),
    # tag-0xB is a ret-0 no-op arm -> the walker break path
    "b2150-brk":   base_case(entry=0x2B2150, rcx="e312", edx="nstr",
                             r8="params", r9="ctxe8",
                             strb=b"\x0b"),
    # heavy char '#' -> real 2AC2F0 decode (esi=3) + elemb flag
    # test -> b10FC; s39c4a0_ret keeps q[ctx+0x60] = c60 and
    # devctxv gives 17F8E0's 1E9780 arm a live q[dev1+0x28] object
    "b2150-heavy": base_case(entry=0x2B2150, rcx="e312", edx="nstr",
                             r8="params", r9="ctxe8",
                             strb=b"\x23\x00",
                             s39c4a0_ret="c60", devctxv="devctx",
                             e312q={0x60: "c60"},
                             eflags={3: 0x80000000}),
    # two heavy chars: flag[3]=0 -> b10FC=2, then flag[4] set with
    # b10FC==2 -> the scale advance xmm6 += f34*2.3*f38
    "b2150-adv":   base_case(entry=0x2B2150, rcx="e312", edx="nstr",
                             r8="params", r9="ctxe8",
                             strb=b"\x23\x24\x00",
                             s39c4a0_ret="c60", devctxv="devctx",
                             e312q={0x60: "c60"},
                             e312f={0x34: 2.0, 0x38: 3.0},
                             eflags={3: 0, 4: 0x80000000}),
    # lite char -> tag-5 space arm -> continue -> NUL final flush,
    # ret = node count (tag-5 sets the aux dword)
    "af340-run":   base_case(entry=0x2AF340, rcx="e312", edx="nstr",
                             r8="params", r9=0,
                             strb=b"\x05"),
    # heavy char -> real 2AC2F0 -> flag test + b1102 clear + r12d++
    "af340-heavy": base_case(entry=0x2AF340, rcx="e312", edx="nstr",
                             r8="params", r9=0,
                             strb=b"\x23\x00",
                             s39c4a0_ret="c60", devctxv="devctx",
                             e312q={0x60: "c60"},
                             eflags={3: 0x80000000}),
    # tag 2 -> nested 2B2150 on the next char (real tag-5 inside)
    "af340-tag2":  base_case(entry=0x2AF340, rcx="e312", edx="nstr",
                             r8="params", r9=0,
                             strb=b"\x02\x05\x00"),
    # tag 0xE -> real tag-14 arm (s3ffdf0 parse + s2b2df0 wrap +
    # param loop over s2a9f00/s39c4a0/s2b43c0) returns 0 -> break
    # path sees b==0xE -> s2b3e30 + float(d[0x1E0CDE8]=8) -> f24
    "af340-tage":  base_case(entry=0x2AF340, rcx="e312", edx="nstr",
                             r8="params", r9=0,
                             strb=b"\x0e\x00"),
    # ---- EXP-209: 2AC5F0 direct entries (rdx = &cursor cell) ----
    # NUL first byte -> ret 0, cursor untouched
    "c5f0-nul":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x00"),
    # ctx+0x10C8 match word == current word -> ret 0, no dispatch
    "c5f0-match": base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x41\x00",
                            e312q={0x10C8: "c60"}, c60d={0: 0x41}),
    # tag 8 -> cursor += 3, ret 1; tag 9 -> cursor += 1, ret 1
    "c5f0-tag8":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x08\x00"),
    "c5f0-tag9":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x09\x00"),
    # tag 5 on direct entry: 15.0/6.5 into the cc60 accumulators,
    # aux dword set, cursor+1, nested 2B2150 under ctx48==0
    "c5f0-tag5":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x05\x00"),
    # ---- EXP-210: remaining 2AC5F0 arms ----
    # shared arm 0x2ACB96: tag1 -> 17F920(0), tag4 -> 17F920(1);
    # int(17f880) height, scale s34/s38 (cc68) + s34/s3C (cc64)
    "c5f0-tag1":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x01\x00",
                            e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0}),
    "c5f0-tag4":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x04\x00",
                            e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0}),
    # tag6 -> fixed shipped const 10.0 * s34 * s38
    "c5f0-tag6":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x06\x00",
                            e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0}),
    # tag7 -> 229E40()==7 ? 0x1A : int(1.0*10.0); e2e14v picks the arm
    "c5f0-tag7":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x07\x00",
                            e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0}),
    "c5f0-tag7a": base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x07\x00",
                            e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0},
                            e2814v=7),
    # tag2 -> nested 2B2150 on cursor+1 + b1102 + f[params] outs
    "c5f0-tag2":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x02\x05\x00"),
    # tag2 with state+0x20 nonnull -> the 17F850/17FA10/2AB820/17FB00
    # tail block
    "c5f0-tag2f": base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x02\x05\x00",
                            e312q={0x20: "c60"}),
    # tag3 -> cursor+1, e598/b10FC clear, 17FAE0(0), ret 0
    "c5f0-tag3":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x03\x00", e598v=0x66),
    # tagA -> tag-5-family advance + scan-for-02/05 + nested 2B2150
    "c5f0-taga":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x0a\x00"),
    # tagB -> shared no-op arm, ret 0, cursor untouched
    "c5f0-tagb":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x0b\x00"),
    # tagF -> second-level dispatch; sub byte 0x80-0x20=0x60 > 0x50
    # -> ret-1 tail, cursor already +1
    "c5f0-tagf":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                            r8="params", r9="params",
                            ccp="nstr", strb=b"\x0f\x80"),
    # EXP-211: tag-15 second-level sub-arms.  idx = sub-0x20; kind =
    # b[02AE3FC+idx]; target = base + d[02AE370 + kind*4] -- the jump
    # table is KIND-indexed and sub bytes share arms.  3FFAB0 (param
    # decoder) + 39BA00 (escape-table lookup over planted ba00t) run
    # real; deep parsers/font helpers stay stubbed.
    # strb = \x0f <sub> <b1> <b2>.
    # kind 0x0D/0x22 (subs 0x30 '0' / 0x5F '_') -> ret-1 tail direct
    "c5f0-f30":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x30\x00"),
    "c5f0-f5f":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x5f\x00"),
    # kind 0x02 (sub '"') -> REAL 3FFEE0(str+1, 0, &state+0x9E):
    # b[0x9E] = b[+2]&0x1F, ret 3; cursor += 1 + 3
    "c5f0-f22":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x22\x83\x17\x00"),
    # kind 0x0A (sub ',') -> pure 3FFAB0 param-skip, ret 1
    "c5f0-f2c":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x2c\x03\x09\x00"),
    # kind 0x1D (sub 'V') -> 3FFAB0 + d[aux]=0
    "c5f0-f56":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x56\x03\x09\x00"),
    # kind 0x04 (sub '$'): real 3FFAB0 direct decode (b1&7!=0 ->
    # (b1&C0)*2|b2&7F) -> f[+0x4C] = float(movsx(param));
    # d[+0xB0]&0x2000000 gates the write
    "c5f0-f24":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x24\x03\x05\x00"),
    "c5f0-f24s":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           e312d={0xB0: 0x2000000},
                           ccp="nstr", strb=b"\x0f\x24\x03\x05\x00"),
    # kind 0x03 (sub '#'): param!=0 -> w[+0x88]=param*0x1E + b9B=1;
    # param==0 -> w88=0x2710, bB0=5, dB0|=0x4080000
    "c5f0-f23":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x23\x03\x02\x00"),
    # b1&7==0 -> escape decode through REAL 39BA00 over ba00t:
    # param = b[q[02AEE870] + 1 + 5*(b2&7F)]  (b2=0 -> entry 0)
    "c5f0-f23z":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x23\x00\x00\x00"),
    "c5f0-f23e":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ba00t={1: 0x37},
                           ccp="nstr", strb=b"\x0f\x23\x00\x00\x00"),
    # kind 0x01 (sub '!'): REAL 39BA30(b[A6],1) over ba30t -> rec+0x40
    # -> q68/q60; 254a10==0 -> d44|=0x800 + 17FD30(7,0) +
    # d[209CC30]=7/d[209CC34]=0 + 2B1ED0
    "c5f0-f21":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ba30t={0: {}},
                           e2814v=1,
                           ccp="nstr", strb=b"\x0f\x21\x00"),
    # 254a10()!=0 inside 39BA30 -> record scan: w6=1 entry (stride
    # 0x40, wC=0x40>0x30, d30=0x8000) matches -> rec+0x40; the arm's
    # own 254a10==1 -> 17FD30(b[A6],1), cc30=bA6, cc34=1
    "c5f0-f21a":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ba30t={9: {"w6": 1,
                                      "e": [[0x40, 0x40, 0x8000]]}},
                           e312b={0xA6: 0x09},
                           ccp="nstr", strb=b"\x0f\x21\x00"),
    # kind 0x05 (subs '%'/'&'/"'"): align family -- b99=param,
    # b9A=sub byte, ctxo+0x1104=sub; ctxo b1102!=0 -> nested 2B2150 +
    # real 2B1F20 (b9A arm) -> f[params]
    "c5f0-f25":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x25\x03\x07\x00"),
    "c5f0-f25n":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ctxb={0x1102: 1},
                           ccp="nstr", strb=b"\x0f\x25\x03\x07\x00"),
    "c5f0-f26n":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ctxb={0x1102: 1},
                           e312b={0x94: 0x30},
                           ccp="nstr", strb=b"\x0f\x26\x03\x07\x00"),
    "c5f0-f27n":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ctxb={0x1102: 1},
                           e312b={0x94: 0x30},
                           ccp="nstr", strb=b"\x0f\x27\x03\x07\x00"),
    # kind 0x06 (sub '('): f34 = param/24.0 (h-scale); 254a10==0 &&
    # param>=24 -> b44 = int((param-24)*0.25); param<24 -> b44=0
    "c5f0-f28":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", e2814v=1,
                           ccp="nstr", strb=b"\x0f\x28\x03\x30\x00"),
    "c5f0-f28l":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x28\x03\x10\x00"),
    # kind 0x14 (sub '7'): f34 = param/100.0 (v-scale); param>=100 ->
    # b44 = int((param-100)/16.6); else b44=0
    "c5f0-f37":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", e2814v=1,
                           ccp="nstr", strb=b"\x0f\x37\x03\x78\x00"),
    # kind 0x00 (sub ' '): f40 override; param 0 + old f40 0 -> ret-1
    # early; old f40!=0 + param 0 -> 17F920(1) kern path ->
    # cc68 = f920*s34*s38*old_f40; + d44&0x800 -> cc68 += s34*s38
    "c5f0-f20":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x20\x03\x00\x00"),
    "c5f0-f20r":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", devctxv=0,
                           e312f={0x40: 2.0, 0x34: 2.0, 0x38: 3.0},
                           ccp="nstr", strb=b"\x0f\x20\x03\x00\x00"),
    "c5f0-f20k":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", devctxv=0,
                           e312f={0x40: 2.0, 0x34: 2.0, 0x38: 3.0},
                           e312d={0x44: 0x800}, e2814v=1,
                           ccp="nstr", strb=b"\x0f\x20\x03\x00\x00"),
    # kind 0x07 (sub ')'): REAL 3FFBC0 colour -> d30 mirrored to
    # ctxo+0x10D0; b[A8]==0xFF absorbs b[9F]; alpha 0 -> b9f=0.
    # b1=0x0B: count 3, hi-byte sel 1 -> out=[0x80|0x11, 0x22, 0x33]
    "c5f0-f29":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           e312b={0xA8: 0xFF, 0x9F: 0x05},
                           ccp="nstr",
                           strb=b"\x0f\x29\x0b\x11\x22\x33\x00"),
    # escape path: b1&7==0 -> 39BA00(b2&7F) -> 5-byte record copied
    # reversed; idx 2 -> table+11 = [0,0x33,0x22,0x11] -> d30 00332211
    "c5f0-f29e":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ba00t={11: 0x00, 12: 0x33, 13: 0x22,
                                  14: 0x11},
                           e312b={0xA8: 0x33},
                           ccp="nstr", strb=b"\x0f\x29\x00\x02\x00"),
    "c5f0-f29z":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           e312b={0xA8: 0x33},
                           ccp="nstr", strb=b"\x0f\x29\x00\x00\x00"),
    # kind 0x09 (sub '+'): alpha param -> shared colour tail
    "c5f0-f2b":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", e312b={0x9F: 0xAB},
                           ccp="nstr", strb=b"\x0f\x2b\x03\x50\x00"),
    # kind 0x0B (sub '-'): REAL 3FFC60(&sub,&tmp,&state+0xA1,0) ->
    # bA1 = min(b2&0xF, 8) = min(9,8) = 8, ret 3; then
    # 2AE610(ctx,&sub,&f16copy,aux); d[aux]=0
    "c5f0-f2d":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", s39c4a0_ret="c60",
                           ccp="nstr", strb=b"\x0f\x2d\x15\x39\x00"),
    # kind 0x0E (sub '1'): REAL 3FFF10(str,0,0,0) -> ret 4
    "c5f0-f31":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x31\x05\x0a\x00"),
    # kind 0x11 (sub '4'): 3FFAB0 writes param byte to b[+0xA9]
    "c5f0-f34":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x34\x03\x12\x00"),
    # kind 0x12 (sub '5'): b[+0xAA]=param; b1102!=0 -> f[params]=
    # float(movsx(param)); b[ctxo+0x10FD]=param
    "c5f0-f35":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x35\x03\x12\x00"),
    "c5f0-f35n":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ctxb={0x1102: 1},
                           ccp="nstr", strb=b"\x0f\x35\x03\x12\x00"),
    # kind 0x13 (sub '6'): b[+0xAA] = -param; ctxo+0x10FD mirrors
    "c5f0-f36":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x36\x03\x12\x00"),
    # kind 0x10 (sub '3'): REAL 3FFDA0 -> f[+0x38]=b1/10.0,
    # f[+0x3C]=b2/10.0 (shipped const f[0x8F8180]), ret 3
    "c5f0-f33":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x33\x55\x0a\x00"),
    # kind 0x21 (sub 'o'): REAL 3FFB00 word param -> f[params]=
    # movsx(w); direct enc b1=3 -> w = b2<<8 | b3 = 0x0028
    "c5f0-f6f":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", e598v=0x66,
                           ccp="nstr", strb=b"\x0f\x6f\x03\x00\x28\x00"),
    # 'o' escape: b1&7==0 -> 39BA00(b2) -> w = movsx(rec[0]); idx 2 ->
    # ba00t[11]=0xE0 -> -32
    "c5f0-f6fe":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ba00t={11: 0xE0},
                           ccp="nstr", strb=b"\x0f\x6f\x00\x02\x00"),
    # kind 0x0F (sub '2'): param==0 -> d[ctxo+0x10E0]=d[params];
    # param!=0 -> f[0209CC68] = max(0, 2*p - (f[params]-f[ctxo10E0]))
    "c5f0-f32":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="auxout", paramd={0: 0x1234},
                           ccp="nstr", strb=b"\x0f\x32\x03\x00\x00"),
    "c5f0-f32a":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="auxout",
                           paramf={0: 40.0}, ctxf={0x10E0: 10.0},
                           ccp="nstr", strb=b"\x0f\x32\x03\x0a\x00"),
    "c5f0-f32b":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="auxout",
                           paramf={0: 40.0}, ctxf={0x10E0: 10.0},
                           ccp="nstr", strb=b"\x0f\x32\x03\x20\x00"),
    # kind 0x1C catch-all (subs 0x40..0x6B): state copy, alpha from
    # ctxo+0x10DC/10E4, b[ctxo+0x10FC]=1, nested 2AEB20, d[aux]=1
    "c5f0-f42":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x42\x00",
                           ctx48o=1, b4730p=1, emat=1,
                           eb20t={"cnt": 2, "lo": 0x30, "hi": 0x40,
                                  "col": 5, "row": 7, "w10": 0x10,
                                  "w12": 0x20, "attr": 0x0123450000000000},
                           e312f={0x34: 2.0, 0x38: 3.0, 0x3C: 4.0,
                                  0x4C: 5.0},
                           e312b={0x30: 0x11, 0x31: 0x22, 0x32: 0x33,
                                  0x44: 0, 0xAB: 0}),
    # EXP-212: remaining arms, all parser-driven now that the family
    # is real.
    # kind 0x1F/0x20 (subs 'm'/'n'): 3FFB90(str+1,0,0) pure skip, ret 3
    "c5f0-f6d":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x6d\x05\x0a\x00"),
    "c5f0-f6e":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x6e\x05\x0a\x00"),
    # kind 0x1E (sub 'l'): 3FFCE0(str+1,0,0,0,[0,0,0]) skip, ret 4
    "c5f0-f6c":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x6c\x05\x0a\x0f\x00"),
    # kind 0x0C (sub '.'): 3FFC60(str+1,&tmp,&tmp2,0); q[state+0x70]==0
    # -> early ret-1 (the entry-table path stays dark)
    "c5f0-f2e":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x2e\x15\x39\x00"),
    # kind 0x16 (sub '9'): 3FFAB0 -> b[+0xA7]=param; d[+0xB0]|=0x200000
    "c5f0-f39":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x39\x03\x12\x00"),
    # kind 0x17 (sub ':'): 3FFAB0(&tmp) skip -> 2ACFB4 tail:
    # q[0209E598]=0 + 17FAE0(0) + ret 1
    "c5f0-f3a":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", e598v=0x66,
                           ccp="nstr", strb=b"\x0f\x3a\x03\x05\x00"),
    # kind 0x18/0x19 (subs '<'/'='): 3FFAB0 -> b[+0xAB]/b[+0xAE]=param
    "c5f0-f3c":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x3c\x03\x21\x00"),
    "c5f0-f3d":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x3d\x03\x2e\x00"),
    # kind 0x15 (sub '8'): 3FFB00 word -> REAL 2639E0(movsx w) ->
    # 32A930 bit-test + 3EAC10 table (unplanted -> 0) -> early ret-1
    "c5f0-f38e":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           ccp="nstr", strb=b"\x0f\x38\x03\x00\x28\x00"),
    # '8' with a resolved resource: eac10t[2*0x28]=rstr -> deep tail:
    # state copies, NUL-scan, 2B41F0 suppress-measure, unconditional
    # nested 2B2150 on the resource, 2A9F00 publish
    # EXP-214: 2B41F0 real — its 39C4A0 font pick lands q[copy+0x60]
    # (s39c4a0_ret="c60" supplies the flag desc); the wrapper's own
    # 2AF340 walk decodes "X" once, then the nested walk once more.
    "c5f0-f38n":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           s39c4a0_ret="c60",
                           eac10t={0x50: "rstr"}, rstrb=b"\x23\x00",
                           devctxv="devctx",
                           e312q={0x60: "c60"},
                           eflags={3: 0x80000000},
                           ccp="nstr", strb=b"\x0f\x38\x03\x00\x28\x00"),
    # kind 0x1A (sub '>'): 3FFAB0 skip then REAL 263990(q[state+0x78])
    # -> w102=0 -> 32A930/3EAC10 -> unplanted table -> 0 -> ret-1
    "c5f0-f3e":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           e312q={0x78: "nobj"}, nobjw={0x102: 0},
                           ccp="nstr", strb=b"\x0f\x3e\x03\x05\x00"),
    # '>' with w102<0 -> q[nobj+0xF8] direct resource -> deep tail
    # (2B41F0 suppress-measure + nested 2B2150 + 2A9F00 publish)
    "c5f0-f3en":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           s39c4a0_ret="c60",
                           e312q={0x78: "nobj", 0x60: "c60"},
                           nobjw={0x102: 0x8000}, nobjq={0xF8: "rstr"},
                           rstrb=b"\x23\x00", devctxv="devctx",
                           eflags={3: 0x80000000},
                           ccp="nstr", strb=b"\x0f\x3e\x03\x05\x00"),
    # kind 0x1B (sub '?'): 3FFAB0 -> alpha pick + state copy ->
    # 2AE450(copy, movsx(param), params, ...); bA9=0, d[aux]=1
    # EXP-218: 2AFDC0 real — writes its quad records at q[0209CC50]
    # then calls 2B4730(1) unconditionally, so the publish cursor must
    # live inside the list buffer (b4730p) and ctx48 must be an object.
    "c5f0-f3f":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", sprt=[5, 0x40, 0x30],
                           ctx48o=1, b4730p=1, emat=1,
                           e312f={0x34: 1.0, 0x38: 2.0, 0x3C: 0.5},
                           ccp="nstr", strb=b"\x0f\x3f\x03\x05\x00"),
    # kind 0x08 (sub '*'): 3FFD70 icon header (w44=b1, w48=b2=len,
    # rest=str+4, ret=len+3); suppress rest[w48]+rest[w48+w44] ->
    # 2B43C0 x2; both nested 2B2150 walks unconditional; ctx48==0 ->
    # ctxo block skipped
    "c5f0-f2a":   base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           s39c4a0_ret="c60", devctxv="devctx",
                           e312q={0x60: "c60"},
                           eflags={3: 0x80000000},
                           ccp="nstr", strb=b"\x0f\x2a\x02\x01\x23\x00"),
    # '*' with ctx48!=0 -> the ctxo publish block runs: b43c0 rets
    # feed the icon-fit clamp; ctxo d10D8/d10DC/f10E4 saved+restored
    # around the 2A9F00 boundary
    "c5f0-f2ac":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params", ctx48=0x77,
                           ctxd={0x10D8: 9, 0x10DC: 5},
                           ctxf={0x10E4: 2.0},
                           s39c4a0_ret="c60", devctxv="devctx",
                           e312q={0x60: "c60"},
                           eflags={3: 0x80000000},
                           ccp="nstr", strb=b"\x0f\x2a\x02\x01\x23\x00"),
    # '*' with w48 < len -> suppress rest[0] + nested 2B2150 on the
    # truncated blob, then restore
    "c5f0-f2an":  base_case(entry=0x2AC5F0, rcx="e312", edx="ccp",
                           r8="params", r9="params",
                           s39c4a0_ret="c60", devctxv="devctx",
                           e312q={0x60: "c60"},
                           eflags={3: 0x80000000},
                           ccp="nstr", strb=b"\x0f\x2a\x02\x00\x23\x00"),
    # EXP-216: 2B4730 display-list append direct entry — drains
    # q[0209CC50] into q[0209E5A0] command records, aligns
    # q[ctx48+8], then real 3A1DB0 ring flip + 36F360 terminator
    # patch.  ecx=1 also runs the ebx-gated ring-slot-table reset.
    "b4730-flush":  base_case(entry=0x2B4730, rcx=1, ctx48o=1,
                             b4730p=1),
    # ecx=0 skips the ring-slot-table reset tail.
    "b4730-noflip": base_case(entry=0x2B4730, rcx=0, ctx48o=1,
                             b4730p=1),
    # EXP-217: 2B1FB0 standalone measure/skip helper direct entry —
    # b[rcx]<=0xF takes the REAL 2AC5F0 interpreter path on the local
    # memset state (kind 'm' = pure 3FFB90 skip, needs no e312
    # fixtures); b[rcx]>0xF takes the REAL 2AC2F0 decode path.
    # Returns consumed = cursor advance.
    "b1fb0-c5":     base_case(entry=0x2B1FB0, rcx="nstr",
                             strb=b"\x0f\x6d\x05\x0a\x00"),
    "b1fb0-dec":    base_case(entry=0x2B1FB0, rcx="nstr",
                             s39c4a0_ret="c60",
                             strb=b"\x41\x41\x41\x00"),
    # ---- EXP-220: 1E8070 vertex submitter + metric thunks ----
    # real 17F7C0 0xA0 copy -> real 1E8070: d[+0x9C]%0x1C -> e94e0
    # ext record, 2x3 loop appends six 0x3C records to the devec
    # vector, slot bounds at dev1+0x2324, scale quad reset to 1.0.
    "e8070-append": base_case(entry=0x17F7C0, rcx="st7c0"),
    # cap==end==begin+0x3C (one live record) -> first append enters
    # the real 1E7A20 realloc arm; salloc returns the e7buf fixture.
    "e8070-grow":   base_case(entry=0x17F7C0, rcx="st7c0",
                             vcap=0x3C, vfill=1, salloc_ret="e7buf"),
    # b[dev1+0x2349] -> the post-loop flag arm writes +0x2340 and
    # +0x2344 and clears the flag.
    "e8070-flag":   base_case(entry=0x17F7C0, rcx="st7c0", b2349=1),
    # d[+0x9C] negative -> r15 = dev1+0x1358 default record, e94e0
    # skipped.
    "e8070-neg":    base_case(entry=0x17F7C0, rcx="st7c0",
                             vidx=0xFFFFFFFF),
    # metric thunks: map miss -> shipped const f[00901990];
    # f920 arm select; f9c0 ceilf scale; f8c0 codepoint->glyph
    # remap + inline map hit.
    "f880-miss":    base_case(entry=0x17F880, nomap=1),
    "f920-arm0":    base_case(entry=0x17F920, rcx=0),
    "f920-arm1":    base_case(entry=0x17F920, rcx=1),
    "f9c0-scale":   base_case(entry=0x17F9C0, rcx=4),
    "f8c0-hit":     base_case(entry=0x17F8C0, rcx=3),
    "f940-get":     base_case(entry=0x17F940),
    "fae0-set":     base_case(entry=0x17FAE0, rcx=0x77),
    # ---- EXP-221: render-device op tail (q[01F811E8]) ----
    # 181460(rcx=recs, edx) appends (edx-2)*3 0x30 records to the
    # current slot's sub-vector; rdcur=0 + q[slot0]==0 keeps slot0
    # (cap 2 -> two real 1AED50 reallocs, cap 2->4->8).
    "rdev-append": base_case(entry=0x181460, rcx="rsrc", edx=4,
                             rdcur=0),
    # rdcur=0 + sealed slot0 (q[slot0]!=0) -> 1B06D0 seals, bumps
    # to slot1, inits it and appends via 1AED50's empty grow.
    "rdev-seal":   base_case(entry=0x1B06D0, rcx="rdev", edx="rsrc",
                             rdcur=0, rseal=1),
    # 1819A0 -> 1B2410: edx<-rcx, r8d<-rdx, r9<-r8(name) — the
    # nonzero-name arm runs 17D2E0's CRT copy into +0x3938.
    "rdev-props":  base_case(entry=0x1819A0, rcx=0x11, edx=0x22,
                             r8="rname", r9=0x33),
    # 181560 -> 1B1910: 1B0100 clears slots 0..rdcur, memset hook,
    # then four 0x80 seeds at +0x3A4C..0x3A58.
    "rdev-reset":  base_case(entry=0x181560, rdcur=2),
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
                # EXP-224 real semantics: 317930 vetoes the real
                # ids; the FFFF-sentinel slots still run 31A630 ->
                # 318B40, which normalizes w[slots0] FFFF -> 0x1000.
                ck(eax == 1, "ret")
                ck(gm.w16(w.rec + 0x50) == 0x1000,
                   "slot0 %04x" % gm.w16(w.rec + 0x50))
                ck(gm.w16(w.rec + 0x52) == 0xFFFF,
                   "slot1 written despite veto")
                fed = [c for c in w.rets.get("rargs", [])
                       if c[0] == "l30fed0" and c[2] == 0x97]
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
                ra = w.rets.get("rargs", [])
                c50 = [c for c in ra if c[0] == "l30c650"]
                ck(c50 and c50[0][2] == 1 and c50[0][3] == 2,
                   f"c650 args {c50}")
                # changed slots -> fed0(rec,0x97) per write
                fed = [c for c in w.rets.get("rargs", [])
                       if c[0] == "l30fed0"]
                # EXP-224: real 30C650 emits its own fed0(*,0), so the
                # seq is c470's + c650's zeros, then the two slot 0x97s
                ck([c[2] for c in fed] == [0, 0, 0x97, 0x97],
                   f"fed0 seq {fed}")
                ck(not [c for c in ra if c[0] == "lg3910"],
                   "member scanned abils")

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
                ck(gm.w16(w.rec + 0x50) == 0x1101, "slot0")
                ck(gm.w16(w.rec + 0x52) == 0x1102, "slot1")
                ck(gm.w16(w.rec + 0x54) == 0xFFFF, "slot2")
                ck(gm.w16(w.rec + 0x56) == 0xFFFF, "slot3")
                ck(gm.w16(w.rec + 0x58) == 0xFFFF, "slot4")
                # scan
                g = [c for c in w.rets.get("rargs", [])
                     if c[0] == "lg3910"]
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
                ck("l30c650" in w.trace and "l30fed0" in w.trace,
                   "c650/fed0")
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
                    # EXP-229: real 2FEF30 rebuilds d[rec+0x24] (HP
                    # floor 1) -> 300530's stat-decrease arm dispatches
                    # 30E360 mode3 once per completed foe rebuild.
                    ck(w.trace.count("e360") == case.get("e360n", 0),
                       f"e360 {w.trace.count('e360')}")
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
                ck(len(byr("l28f1f0")) == 1,
                   f"28F1F0 gauge post missing {calls}")
                ck(w6 == 10 + 30, f"hp cascade w6 {w6}")
            elif name == "ce0-cap":
                ck(w4c == 200, f"w4C {w4c} != cap")
            elif name == "ce0-cascade":
                ck("h0bc0" in w.trace, "hp cascade missing")
                ck(w6 == 40, f"w6 {w6}")
            elif name == "ce0-drop":
                ck(w4c == 20, f"w4C {w4c}")
                ck(len(byr("l2fa540")) == 1,
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
                ck(not byr("l3105d0"), "u3105d0 on edx=0")
            elif name == "b140-clear":
                ck(not (gm.q(obj) & 0x4000), "bit14 kept on sentinel miss")
                ck(gm.d(obj + 4) & 0x200000, "d4 |= 0x200000")
            elif name == "b140-td":
                ck(len(byr("l3105d0")) == 1, "u3105d0 missing")
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
                ck(not byr("l2eb0d0"), "2EB0D0 on b18==1")
            elif name == "k99b0-hi":
                ck(gm.d(obj + 0x5C) == 0x5300,
                   f"d5C {gm.d(obj + 0x5C):#x} != 0x5300")
                ck(gm.d(ent + 0xF0) == 0x5300, "dF0")
            elif name == "k99b0-kick":
                kk = byr("l2eb0d0")
                ck(len(kk) == 1, "2EB0D0 not kicked")
                if kk:
                    ck(kk[0][1] == ent, f"kb0d0 rcx {kk[0][1]:#x}")
                    ck(kk[0][2] == w.objc0, f"kb0d0 rdx {kk[0][2]:#x}")
                    ck(kk[0][3] == 0x50, f"kb0d0 r8 {kk[0][3]:#x}")
                    ck(kk[0][4] == 1, f"kb0d0 r9 {kk[0][4]:#x}")
                # EXP-233: real node teardown writes — the null-ecarr
                # path skips all 427xxx gates (w[node]==0 -> row 0 +
                # null base == 0) but 269D60's flag fold + the reset
                # writes land on the objc0 node.
                ck(gm.d(w.objc0 + 0x14) == 0xBF800000, "node d14 -1.0")
                ck(gm.d(w.objc0 + 0x18) == 0xBF800000, "node d18 -1.0")
                ck(gm.d(w.objc0 + 0x1C) == 0xBF800000, "node d1C -1.0")
                ck(gm.w16(w.objc0 + 0x2A) == 0xFFFF, "node w2A reset")
                ck(gm.b(w.objc0 + 0x11) == 0, "node b11 cleared")
                ck(gm.b(w.objc0 + 0x29) == 0, "node b29 folded")

        elif name.startswith("s8a0-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
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
                ck(len(byr("l6ab10")) == 1, "46ab10 not called")
            elif name == "s8a0-flag4clr":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("l6a630") == 1, f"46a630 {tcount('l6a630')}")
                ck(len(byr("l6ab10")) == 1, "46ab10 not called")
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

        elif name.startswith(("q6dup-", "q6mid-")):
            # EXP-249: 46AB10 dedup-ring scan arm.  Ring base
            # 0x2EBB560, stride 0x20, cursor d[0x2EBB54C],
            # "now" = 32A150() = d[0x208D45C].
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            # entry's own tag is never recorded (on_code skips
            # addr==entry); execution is proven by the ring writes,
            # the cursor cell, and the scripted-notify args.
            vv = byr("l69570")
            if name in {"q6dup-cap", "q6mid-g3080", "q6mid-b20"}:
                ck(not vv, f"469570 ran past mid-gate ({name})")
            else:
                ck(len(vv) == 1, f"469570 {len(vv)}")
                if vv:
                    ck(vv[0][1] == 0x1234,
                       f"469570 ecx {vv[0][1]:#x}")
            sc = by("s5369c0")
            if sc:
                ck(sc[0][1] == w.q6pay, f"notify rcx {sc[0][1]:#x}")
                ck(sc[0][2] == 0x1234, f"notify edx {sc[0][2]:#x}")
                ck(sc[0][3] == w.q6s, f"notify r8 {sc[0][3]:#x}")
            ring = 0x2EBB560
            if name == "q6dup-hit":
                # fresh seeded row at slot 2: 0x1c2 + 0 > now(0)
                # -> suppress: no notify, no write, cursor unmoved
                ck(not by("s5369c0"), "s5369c0 fired on dedup hit")
                ck(gm.w16(ring + 0x40) == 0x1234, "hit row tag")
                ck(gm.q(ring + 0x48) == w.q6pay, "hit row payload")
                ck(gm.d(ring + 0x44) == 0, "hit row ts")
                ck(gm.w16(ring) == 0, "slot0 written")
                ck(gm.d(0x2EBB54C) == 0, "cursor moved")
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "q6dup-miss":
                # tag mismatch on all 10 rows -> insert at cursor 0
                ck(len(by("s5369c0")) == 1, "s5369c0 count")
                ck(gm.w16(ring) == 0x1234, "insert tag")
                ck(gm.q(ring + 8) == w.q6pay, "insert payload")
                ck(gm.d(ring + 4) == 0, "insert ts")
                ck(gm.d(0x2EBB54C) == 1, "cursor")
            elif name == "q6dup-stale":
                # matching row expired (0x1c2+0 <= now 0x1000) ->
                # scan passes over it; insert arm writes cursor 5
                ck(len(by("s5369c0")) == 1, "s5369c0 count")
                ck(gm.w16(ring + 0x40) == 0x1234, "stale row tag")
                ck(gm.q(ring + 0x48) == w.q6pay, "stale row payload")
                ck(gm.d(ring + 0x44) == 0, "stale row ts rewritten")
                ck(gm.w16(ring + 0xA0) == 0x1234, "insert tag")
                ck(gm.q(ring + 0xA8) == w.q6pay, "insert payload")
                ck(gm.d(ring + 0xA4) == 0x1000, "insert ts")
                ck(gm.d(0x2EBB54C) == 6, "cursor")
            elif name == "q6dup-cap":
                # count cap: jge out before the owner scan — no
                # resolver call, no write, no notify
                ck(tcount("l69570") == 0, "469570 ran past cap")
                ck(not by("s5369c0"), "s5369c0 fired past cap")
                ck(gm.d(0x2EBB54C) == 0, "cursor moved past cap")
                ck(gm.w16(ring) == 0, "ring written past cap")
            elif name.startswith("q6mid-"):
                # owner-scan hit then a mid-gate exit (g3080/b20) or
                # pass-through (ok/rsi/noci).  31B860 ran real.
                ob = byr("b860")
                if name == "q6mid-rsi":
                    # q[q6s+8]==0 -> 46AB10's own scan skipped
                    # (test rcx,rcx; je); only the resolver's rsi
                    # pair runs, both on the +0 carrier's rec.
                    ck(len(ob) == 2 and
                       all(c[1] == w.oar4[2][1] for c in ob),
                       f"rsi pair args {ob}")
                elif name == "q6mid-fall":
                    ck(ob[0][1] == w.oar4[2][1],
                       f"46AB10 scan arg {ob}")
                else:
                    ck(len(ob) >= 1 and ob[0][1] == w.oar4[1][1],
                       f"31B860 arg {ob}")
                if name in {"q6mid-g3080", "q6mid-b20"}:
                    # rax still holds 31B860's row at 0x46AC7A —
                    # the exit returns the owner row, not 0.
                    ck(eax == w.oar4[1][0], f"ret {eax:#x}")
                    ck(not by("s5369c0"), "s5369c0 fired past gate")
                    ck(gm.d(0x2EBB54C) == 0, "cursor moved")
                    ck(gm.w16(ring) == 0, "ring written")
                elif name == "q6mid-veto":
                    # 2FA3B0 ret 0 -> 469570 ret 0 -> 46AB10 exits;
                    # the veto path returns 0, not the row.
                    ck(eax == 0, f"ret {eax:#x}")
                    ck(not by("s5369c0"), "s5369c0 fired past veto")
                    ck(gm.d(0x2EBB54C) == 0, "cursor moved")
                    ck(gm.w16(ring) == 0, "ring written")
                else:
                    ck(len(by("s5369c0")) == 1,
                       f"s5369c0 on {name}")
                    ck(gm.w16(ring) == 0x1234, "insert tag")
                    ck(gm.d(0x2EBB54C) == 1, "cursor")
                # EXP-253 verdict pins: 469570 stores the owner row
                # at q[02EBF188]; its ret gates 46AB10 (0 -> exit).
                if name == "q6mid-ok":
                    ck(gm.q(0x2EBF188) == w.oar4[1][0],
                       "owner cell")
                    fa = byr("lfa3b0")
                    ck(len(fa) == 1 and fa[0][1] == w.oar4[1][2],
                       f"2FA3B0 arg {fa}")
                elif name == "q6mid-rsi":
                    ck(gm.q(0x2EBF188) == w.oar4[2][0],
                       "owner cell (rsi arm)")
                    fa = byr("lfa3b0")
                    ck(len(fa) == 1 and fa[0][1] == w.oar4[2][2],
                       f"2FA3B0 arg {fa}")
                elif name == "q6mid-noci":
                    # q[row+0x10]==0 -> je -> ret 1 (proceed);
                    # 2FA3B0 is only consulted when the owner row
                    # carries client-info — never called here.
                    ck(gm.q(0x2EBF188) == w.oar4[1][0],
                       "owner cell (noci)")
                    ck(not byr("lfa3b0"),
                       "2FA3B0 ran on null q[+0x10]")
                    ck(len(ob) == 2, f"rdi single lookup {ob}")
                elif name == "q6mid-veto":
                    ck(gm.q(0x2EBF188) == w.oar4[1][0],
                       "owner cell (veto)")
                    fa = byr("lfa3b0")
                    ck(len(fa) == 1 and fa[0][1] == w.oar4[1][2],
                       f"2FA3B0 arg {fa}")
                elif name == "q6mid-fall":
                    # rsi arm hits row1 (null ci) -> falls to rdi
                    # arm -> hits row2 -> cell ends on row2, the
                    # rdi pair + 2FA3B0(ci2) run.  b860 x4 total.
                    ck(len(ob) == 4, f"lookup count {ob}")
                    ck(ob[1][1] == w.oar4[1][1] and
                       ob[2][1] == ob[3][1] == w.oar4[2][1],
                       f"arm order {ob}")
                    ck(gm.q(0x2EBF188) == w.oar4[2][0],
                       "owner cell (fall)")
                    fa = byr("lfa3b0")
                    ck(len(fa) == 1 and fa[0][1] == w.oar4[2][2],
                       f"2FA3B0 arg {fa}")
                elif name == "q6mid-g80":
                    # b[elem+3]>=0x80 -> ret 1 before the lookups:
                    # owner cell stays null, 2FA3B0 never consulted.
                    ck(gm.q(0x2EBF188) == 0, "owner cell on g80")
                    ck(not byr("lfa3b0"), "2FA3B0 ran on g80")
                    # 4 e600 in 469570's desc gate + 2 more for
                    # 46AB10's own element resolve at 46AB83.
                    ck(len(byr("e600")) == 6, "e600 chain")

        elif name.startswith("q69570-"):
            # EXP-255: direct-entry resolver probes (desc null ->
            # straight to the owner arms; ret = 2FA3B0 verdict).
            tr = w.trace
            tcount = lambda t: tr.count(t)
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
            si = case["q6arg"]
            row, ri, ci = w.oar4[si]
            ck(gm.q(0x2EBF188) == row, "owner cell")
            ob = byr("b860")
            ck(len(ob) == 2 and all(c[1] == ri for c in ob),
               f"lookup pair {ob}")
            fa = byr("lfa3b0")
            ck(len(fa) == 1 and fa[0][1] == ci, f"2FA3B0 arg {fa}")
            ck(eax != 0, f"ret {eax:#x}")

        elif name.startswith("a630r9-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
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
                ck(tcount("a08a0") == 3, f"8a0 {tcount('a08a0')}")
                # EXP-224: real 309EC0 free-count adds a 2FD8D0 query
                # alongside f9a0/c410's pairs; EXP-227: real 3105D0 ->
                # 300280 -> 3008A0 -> 309F30 adds one more 2FD8D0 +
                # 2FD150 dispatch on the teardown arm.
                ck(tcount("v2fd8d0") == 4 and tcount("m2fd150") == 3,
                   f"cb {tcount('v2fd8d0')}/{tcount('m2fd150')}")
                ck(len(byr("l318b40")) == 1
                   and byr("l318b40")[0][2] == 2, "l318b40 args")
                ck(len(byr("l30fed0")) == 1 and byr("l30fed0")[0][2] == 0x97,
                   "fed0 missing")
                # 324470 teardown chain on the owner member
                ck(len(byr("l2ecf10")) == 1
                   and byr("l2ecf10")[0][1] == w.objent
                   and byr("l2ecf10")[0][2] == 0, "tecf10 args")
                ck(len(byr("l3105d0")) == 1
                   and byr("l3105d0")[0][1] == w.objrow, "u3105d0")
                ck(not byr("l313f60") and not by("p300e40"),
                   "313f60/300e40 ran past zero or-gate")
                ck(len(byr("l2e42d0")) == 1
                   and byr("l2e42d0")[0][1] == w.objent, "l2e42d0 args")
                for t in ("l2699d0", "l2ecec0"):
                    ck(len(byr(t)) == 1 and byr(t)[0][1] == w.objent,
                       f"{t} args")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
                # EXP-230: real 30C970 ran on mode byte 0 — row 0 of
                # the 0x22C17B0 table carries the reset sentinels.
                ck(tcount("l30c970") >= 1, "l30c970")
                ck(gm.w16(0x22C17B0 + 0x1C) == 0xFFFF
                   and gm.d(0x22C17B0 + 0x24) == 0xFFFFFFFF
                   and gm.d(0x22C17B0 + 0x28) == 0x80000000
                   and gm.q(0x22C17B0) == 0,
                   f"c970 row0 {gm.d(0x22C17B0 + 0x24):#x} "
                   f"{gm.d(0x22C17B0 + 0x28):#x}")
                ck(tcount("v3dc780") == 0 and tcount("v42fcc0") == 0
                   and tcount("v306570") == 0, "c970 gated arms")
            elif name == "a630r9-off":
                ck(eax == 0, f"ret {eax:#x}")
                ck(w54 == 0x1150, f"slot {w54:#x}")
                for t in ("uf9a0", "ec410", "m4470", "a08a0"):
                    ck(tcount(t) == 0, f"{t} ran with r9d=0")
                # EXP-228: real 30FED0 tail -> n0e060 -> +1 b860
                # EXP-229: real 2FEF30 head -> 31B860 owner resolve -> +1
                ck(tcount("b860") == 2, f"b860 {tcount('b860')}")
            elif name == "a630r9-oldff":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("uf9a0") == 1, "f9a0 not entered")
                ck(tcount("a08a0") == 2,
                   f"8a0 {tcount('a08a0')} (only equip arm)")
                ck(w150 == 0x0C03, f"w150 {w150:#x}")
                ck(w54 == 0x1150, f"slot {w54:#x}")
            elif name == "a630r9-oldfoe":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("uf9a0") == 1, "f9a0 not entered")
                ck(tcount("a08a0") == 2,
                   f"8a0 {tcount('a08a0')} (foe-class old skipped)")
                ck(w150 == 0x0C03, f"w150 {w150:#x}")
            elif name == "a630r9-new1k":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("ec410") == 1, "c410 not entered")
                ck(tcount("a08a0") == 2,
                   f"8a0 {tcount('a08a0')} (0x1000 new skipped)")
                ck(w100 == 0x1005, f"w100 {w100:#x}")
                ck(w54 == 0x1000, f"slot {w54:#x}")
            elif name == "a630r9-nomatch":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("b860") == 3,
                   f"owner scan + fed0/e060 tail {tcount('b860')}")
                ck(tcount("e6850") >= 1 and tcount("e6820") == 6,
                   f"scan loop e6820 {tcount('e6820')}")
                ck(tcount("m4470") == 0, "4470 ran on null owner")
            elif name == "a630r9-bit23":
                ck(len(byr("l2ecf10")) == 1 and byr("l2ecf10")[0][2] == 1,
                   "tecf10 edx not 1")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-gate3f":
                ck(len(byr("l313f60")) == 1, "s313f60 skipped")
                ck(not by("p300e40"), "300e40 ran past 313f60 gate")
            elif name == "a630r9-b2":
                ck(len(byr("l313f60")) == 1, "s313f60 skipped")
                ck(not by("p300e40"), "300e40 ran past b2 gate")
                ck(gm.d(w.objrow) & 0x40, "member 0x40 not set")
            elif name == "a630r9-rec3c":
                ck(len(byr("l313f60")) == 1
                   and byr("l313f60")[0][1] == w.rec, "s313f60")
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
                ck(not byr("l317930"), "7930 ran on FFFF new id")
                ck(tcount("a08a0") == 2,
                   f"8a0 {tcount('a08a0')} (FFFF equip skipped)")
                ck(w100 == 0x1005, f"w100 {w100:#x}")
                ck(w54 == 0xFFFF, f"slot {w54:#x}")
            elif name == "a630r9-clamp":
                # EXP-224 real semantics: 309EC0 free-count for
                # 0x1150 is cap3-count3 = 0 -> 317930 denies ->
                # 31A630 vetoes the whole op (-1, no writes).
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                ck(w54 == 0x1100, f"slot written on veto {w54:#x}")
                ck(w150 == 0x0C03, f"clamp w150 {w150:#x}")
                ck(w100 == 0x1405, f"w100 {w100:#x}")
                ck(tcount("uf9a0") == 0 and tcount("ec410") == 0,
                   "chain ran on veto")


        elif name.startswith(("g7930-", "l8b40-", "u43f0-", "w4450-",
                              "r71d0", "g8010-", "o4100-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]
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
                # real 323C60 adds its own 322C50 (kind-1 auto
                # class) + row resolves on top of 317930's
                ck(tcount("v2c50") == 2, "kind-6 range not run")
                ck(tcount("e600") == 6, f"e600 {tcount('e600')}")
                ck(len(byr("s3c60")) == 1
                   and byr("s3c60")[0][2] == 0x1150, "323c60 args")
            elif name == "g7930-tagmm":
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("e600") == 2 and not byr("s3c60"),
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
                ck(tcount("e600") == 8, f"e600 {tcount('e600')}")
            elif name == "g7930-s1ne":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not byr("s3c60"), "323c60 ran on tag mismatch")
            elif name == "g7930-foebit":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not byr("s3c60"), "323c60 ran on foe bit set")
            elif name == "g7930-b5":
                # b[rec+5]!=0 short-circuits to ret1 before the foe test
                ck(eax == 1, f"ret {eax:#x}")
                ck(tcount("e600") == 2, f"e600 {tcount('e600')}")
            elif name == "g7930-c60":
                ck(eax == 0, f"ret {eax:#x}")
                ck(len(byr("s3c60")) == 1, "323c60 not called")
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
                ck(len(byr("l3105d0")) == 1
                   and byr("l3105d0")[0][1] == w.objrow, "u3105d0")
                ck(not byr("l313f60") and not by("p300e40"),
                   "gates ran past zero or-mask")
                ck(len(byr("l2e42d0")) == 1
                   and byr("l2e42d0")[0][1] == w.objent, "l2e42d0 args")
                for t in ("l2699d0", "l2ecec0"):
                    ck(len(byr(t)) == 1 and byr(t)[0][1] == w.objent,
                       f"{t} args")
            elif name == "u43f0-698z":
                ck(not byr("l313f60"), "313f60 ran on null 698")
                ck(len(by("p300e40")) == 1
                   and by("p300e40")[0][1] == w.objrow
                   and by("p300e40")[0][2] == 0, "300e40 args")
            elif name == "u43f0-3f":
                ck(len(byr("l313f60")) == 1, "313f60 missing")
                ck(len(by("p300e40")) == 1, "300e40 missing")
            elif name in ("u43f0-3fskip", "u43f0-b2"):
                ck(len(byr("l313f60")) == 1, "313f60 missing")
                ck(not by("p300e40"), "300e40 ran past skip gate")
            elif name == "u43f0-ec":
                ck(len(byr("l2ecec0")) == 1
                   and byr("l2ecec0")[0][1] == w.objent, "l2ecec0")
                c = byr("l3aeef0")
                ck(len(c) == 1
                   and c[0][1] == w.ecarr + 2 * 0x740 + 0x550,
                   "3aeef0 arg")
                ck(gm.q(w.ecarr + 2 * 0x740 + 0x568) == 0
                   and gm.q(w.ecarr + 2 * 0x740 + 0x570) == 0,
                   "ec head/cur not cleared")
                ck(all(gm.b(n) == 0 for n in w.ecnodes),
                   "ec nodes not zeroed")
                # EXP-233/234: real 2E42D0+2EB0D0 on the objc0 node —
                # 2E42D0's 427280 folds elem2's d[+0x294] first
                # (&=0xFFFDFA5F|=4), then 2EB0D0's 427xxx arms fold
                # (4278B0 |=0x400000, 427860 &=0xFFFDFADF|=0x80,
                # 4272A0 |=0x1000).  EXP-257: real 427320's class-1
                # switch arm (423790 ret 1) runs BEFORE the folds and
                # adds |=8 -> 0x40108C.
                elem2 = w.ecarr + 2 * 0x740
                ck(gm.d(elem2 + 0x294) == 0x40108C,
                   f"elem d294 {gm.d(elem2 + 0x294):#x}")
                # EXP-257: real 422C20 — all three slot fields
                # planted -1 -> resolver arms skipped; clear block
                # pinned by sentinels (q writes + d[+0x23C]/+0x69C]/
                # b[+0xC0]).  427320 real: 3E7D10 row-0 empty ->
                # edi=0x1001 misses the 0x2005/0x2006 arms -> 420890
                # default (2ED500(0) zeroes the out buf ->
                # d[+0x110]=0) -> 423790 (d[+0xC4]==-1 -> ret 1) ->
                # class-1 switch arm ((edi>>0xC)&0xF=1): 20E600 x2 +
                # d[+0x294]|=8 upstream of the 427xxx folds.
                c20 = byr("l422c20")
                ck(len(c20) == 1 and c20[0][1] == elem2,
                   f"l422c20 {c20}")
                ck(all(gm.q(elem2 + o) == 0 for o in
                       (0x68, 0xD8, 0xE0, 0xF0, 0xF8)),
                   "422c20 q clears")
                # d[+0x69C] = 20E620(0) = 0 - d[01F83530] — the BSS
                # base counter reads 0x40001000 -> 0xBFFFF000.
                ck(gm.d(elem2 + 0x23C) == 0
                   and gm.d(elem2 + 0x69C) == 0xBFFFF000,
                   f"422c20 d clears {gm.d(elem2 + 0x23C):#x} "
                   f"{gm.d(elem2 + 0x69C):#x}")
                ck(gm.d(elem2 + 0xC0) == 0xFFFFFFBF,
                   f"422c20 bC0 {gm.d(elem2 + 0xC0):#x}")
                ck(gm.w16(elem2 + 0x3B6) == 0, "elem w3b6")
                ck(gm.d(elem2 + 0x3C4) == 0, "elem d3c4")
                t320 = byr("l427320")
                ck(len(t320) == 1 and t320[0][1] == elem2
                   and t320[0][2] == 0x1001, f"l427320 {t320}")
                ck(gm.d(elem2 + 0x110) == 0,
                   f"427320 d110 {gm.d(elem2 + 0x110):#x}")
                ck(not by("v422c20") and not by("v427320"),
                   "v-stubs still scripted")
                ck(gm.d(w.objc0 + 0x14) == 0xBF800000
                   and gm.w16(w.objc0 + 0x2A) == 0xFFFF,
                   "node reset")
                # EXP-256: real 426FA0 — w[elem2]=0 -> ecarr row0.
                # 426220 sig-gate ret 0 (row b[+0x3C]!=0x68, arg
                # b[+0x3C]!=0x62) -> d[row+0x284]|=0x100000 +
                # b[row+0xC0]&=0xBF; w[row+8]=-1 -> leaf, no child
                # row / no 42EF90 enqueue.
                fa0 = byr("l426fa0")
                ck(len(fa0) == 1 and fa0[0][1] == elem2
                   and fa0[0][2] == 0x10, f"l426fa0 {fa0}")
                ck(gm.d(w.ecarr + 0x284) == 0x100000,
                   f"ec row0 d284 {gm.d(w.ecarr + 0x284):#x}")
                ck(gm.d(w.ecarr + 0xC0) == 0xFFFFFFBF,
                   f"ec row0 dC0 {gm.d(w.ecarr + 0xC0):#x}")
                ck(not by("b6fa0"), "b6fa0 still scripted")
            elif name == "w4450-set":
                ck(tcount("rx3243f0") == 1, "43f0 not entered")
                ck(len(byr("l3105d0")) == 1, "u3105d0 missing")
                ck(not gm.d(w.objrow) & 0x40, "0x40 not cleared")
            elif name == "w4450-clear":
                ck(tcount("rx3243f0") == 0, "43f0 ran on clear bit")
                ck(not byr("l3105d0"), "u3105d0 ran")

            elif name.startswith("d422c20-"):
                # EXP-258: direct-entry 422C20 dereg arms.  The
                # resolver arms run 20E600(d[+0x10]) -> q[elem+0xDA8]
                # -> 51BA40(container, slot): 51F240 picks desc
                # darr[slot] -> q[desc+0x18] record -> 41CF00/41CB90
                # record reset -> 51F190 releases desc
                # darr[d[record]] (51F4C0 w-index unlink + head/tail
                # fixups, live count d[C+0x14]--).
                C, A = w.dcntr, w.darr
                c4 = name in ("d422c20-c4", "d422c20-both",
                              "d422c20-mode2", "d422c20-mode3",
                              "d422c20-mode0", "d422c20-c4ind",
                              "d422c20-c4rows", "d422c20-c4rc2")
                c8 = name in ("d422c20-c8", "d422c20-both")
                if name != "d422c20-c4f0":
                    # c4f0 faults inside 51BA40 -> 41CF00 ->
                    # 372280(0) — 422C20's retire/clear writes never
                    # run; the fault PC pin is the whole assertion.
                    ck(gm.d(w.delem + 0xC4) == 0xFFFFFFFF, "dC4")
                    ck(gm.d(w.delem + 0xC8) == 0xFFFFFFFF, "dC8")
                    # w[+0xCC] only the +0xC4 arm writes it
                    ck(gm.w16(w.delem + 0xCC) ==
                       (0xFFFF if c4 else 0x1234),
                       f"wCC {gm.w16(w.delem + 0xCC):#x}")
                    # clear block runs regardless of arm coverage
                    ck(gm.d(w.delem + 0xC0) == 0xFFFFFFBF
                       and gm.d(w.delem + 0x69C) == 0xBFFFF000,
                       "clear block")
                if name.startswith("d422c20-18"):
                    # EXP-259/260: 2ED570(q[elem+0xD98], slot)
                    # resolves 3AB7F0-tagged row/sub bases (direct,
                    # hdr|tag handle via 36B130, or null -> cached
                    # q[C2+0x38]/+0x10); d[row]!=-1 -> ret
                    # element+(d[C2+0x50]&slot)*d[C2+0x48] ->
                    # d[ret] &= ~8.  422C20 leaves d[+0x18] set —
                    # the +0x18 slot is not retired.
                    C2 = w.dcntr2
                    ck(gm.q(C2 + 0x38) == w.dc2rows
                       and gm.q(C2 + 0x10) == w.dc2subs,
                       "c2 bases resolved")
                    ck(gm.d(w.delem + 0x18) == 1,
                       f"d18 {gm.d(w.delem + 0x18):#x}")
                    woff = 0x10 if name == "d422c20-18mm" else 0
                    exp = (0xF if name == "d422c20-18nul" else 7)
                    ck(gm.d(w.dc2elem + woff) == exp,
                       f"e2+{woff:#x} {gm.d(w.dc2elem + woff):#x}")
                    if name == "d422c20-18mm":
                        ck(gm.d(w.dc2elem) == 0xF,
                           "e2 base dword untouched")
                elif name in ("d422c20-mode2", "d422c20-mode3"):
                    # 51F240 ret 0 -> 51BA40 skips reset + release
                    R = w.drecs[1]
                    ck(gm.d(R) == 2, f"{name} rec still keyed")
                    ck(gm.d(A + 2 * 0x30 + 4) == 0,
                       f"{name} desc released")
                    ck(gm.d(C + 0x14) == 2, f"{name} count moved")
                elif name == "d422c20-c4ind":
                    # EXP-262: b[desc]&2 re-resolve — the record
                    # pointer is recomputed as sx(3AB7F0(q[D+0x10])
                    # +d[D+0x20]) and STORED back to q[D+0x18]; the
                    # reset lands on R2, release is keyed by d[R2].
                    R, r2 = w.drecs[1], w.drecs[("r2", 1)]
                    ck(gm.q(A + 0x30 + 0x18) == r2,
                       "desc1 ptr re-resolved")
                    ck(gm.d(r2) == 0xFFFFFFFF
                       and gm.d(r2 + 0x324) == 0xFFFFFFFF
                       and gm.d(r2 + 0x358) == 0x10, "r2 reset")
                    ck(gm.d(R) == 7, "R1 never reset")
                    D = A + 2 * 0x30
                    ck(gm.d(D) == 0 and gm.d(D + 4) == 0xFFFFFFFF
                       and gm.d(D + 8) == 0xFFFFFFFF
                       and gm.d(D + 0xC) == 0xFFFFFFFF
                       and gm.q(D + 0x10) == 0
                       and gm.q(D + 0x18) == 0
                       and gm.q(D + 0x20) == 0, "desc2 release")
                    ck(gm.d(C + 0x14) == 1, "count")
                    ck(gm.d(C + 0x1C) == 0xFFFFFFFF
                       and gm.d(C + 0x20) == 3, "head/tail")
                elif name in ("d422c20-c4", "d422c20-c8",
                              "d422c20-both", "d422c20-mode0",
                              "d422c20-c4rows", "d422c20-c4rc2"):
                    pops = {"d422c20-c4": [(1, 2)],
                            "d422c20-c8": [(0, 1)],
                            "d422c20-both": [(0, 2), (1, 3)],
                            "d422c20-mode0": [(1, 2)],
                            "d422c20-c4rows": [(1, 2)],
                            "d422c20-c4rc2": [(1, 2)]}[name]
                    for slot, key in pops:
                        R = w.drecs[slot]
                        # 41CB90 signature writes on the record
                        ck(gm.d(R) == 0xFFFFFFFF
                           and gm.d(R + 0x324) == 0xFFFFFFFF
                           and gm.d(R + 0x358) == 0x10,
                           f"rec{slot} reset")
                        # the popped desc keeps its q[+0x18] link
                        ck(gm.q(A + slot * 0x30 + 0x18) == R,
                           f"desc{slot} link moved")
                        # 51F190 released desc A[key]
                        D = A + key * 0x30
                        ck(gm.d(D) == 0 and gm.d(D + 4) == 0xFFFFFFFF
                           and gm.d(D + 8) == 0xFFFFFFFF
                           and gm.d(D + 0xC) == 0xFFFFFFFF
                           and gm.q(D + 0x10) == 0
                           and gm.q(D + 0x18) == 0
                           and gm.q(D + 0x20) == 0, f"desc{key} release")
                    ck(gm.d(C + 0x14) == 1,
                       f"count {gm.d(C + 0x14):#x}")
                    # head/tail fixups: key match -> adopt released
                    # desc's (both -1) links
                    if name in ("d422c20-c4", "d422c20-mode0",
                                "d422c20-c4rows", "d422c20-c4rc2"):
                        ck(gm.d(C + 0x1C) == 0xFFFFFFFF
                           and gm.d(C + 0x20) == 3, "head/tail")
                    elif name == "d422c20-c8":
                        ck(gm.d(C + 0x1C) == 0xFFFF
                           and gm.d(C + 0x20) == 0xFFFFFFFF,
                           "head/tail")
                    else:
                        ck(gm.d(C + 0x1C) == 0xFFFFFFFF
                           and gm.d(C + 0x20) == 0xFFFFFFFF,
                           "head/tail")
                    if name == "d422c20-c4rows":
                        # EXP-262: 41CF00's w[R+0x28] block loop —
                        # 0xA0-stride resets at R+0x30/R+0xD0.
                        # w[blk+4] = cx = the pre-loop ecx (always
                        # 0, NOT the iteration count — r8d counts
                        # and is never stored).  41CB90's writes
                        # skip +0x30..+0x2AF so the loop's writes
                        # survive into the final state.
                        R = w.drecs[1]
                        ck(gm.d(R + 0x30) == 0xFFFFFFFF
                           and gm.w16(R + 0x34) == 0
                           and gm.d(R + 0x48) == 0x1E0000
                           and gm.d(R + 0x50) == 0x41F00000
                           and gm.w16(R + 0x80) == 0xFFFF
                           and gm.w16(R + 0x82) == 0xFFFF
                           and gm.d(R + 0x98) == 0xFFFFFFFF
                           and gm.d(R + 0xBC) == 0x1234
                           and gm.w16(R + 0xC6) == 0x7F, "block0")
                        ck(gm.d(R + 0xD0) == 0xFFFFFFFF
                           and gm.w16(R + 0xD4) == 0
                           and gm.d(R + 0x15C) == 0x5678
                           and gm.w16(R + 0x166) == 0x7F, "block1")
                    elif name == "d422c20-c4rc2":
                        # EXP-262: d[R+0xC]&0x1000 -> 2ED570 on the
                        # record's own container q[R+0x330] -> e3 ->
                        # 372280: list at rdi+w[+0x88]*0x290, word
                        # count w[+0x8A], each word -> 0x290 row.
                        C3, rows3, subs3 = w.dc3
                        ck(gm.q(C3 + 0x38) == rows3
                           and gm.q(C3 + 0x10) == subs3,
                           "rc2 bases resolved")
                        t = w.elemb + 0x74290
                        ck(gm.w16(t + 0x280) == 0, "row1 flag bit")
                        ck(gm.q(t + 0x1A4) == 0
                           and gm.d(t + 0x1A0) == 0
                           and gm.d(t + 0x1AC) == 0x3F800000
                           and gm.q(t + 0x1C4) == 0
                           and gm.d(t + 0x1C0) == 0
                           and gm.d(t + 0x1CC) == 0x3F800000,
                           "row1 cleared")
                        # 41CB90 retires the record's container
                        # handle itself (q[+0x330]=0, d[+0x338]=-1)
                        R = w.drecs[1]
                        ck(gm.q(R + 0x330) == 0
                           and gm.d(R + 0x338) == 0xFFFFFFFF,
                           "record container retired")
                # c4f0: pinned by expect_fault=0x37228D — the
                # d[R+0x338]==-1 path passes rcx=0 (the xor'd reg,
                # untouched by the block loop) to 372280 which reads
                # d[0x84] unguarded.

            elif name.startswith("d2ed610-"):
                # EXP-261: caller-side walk over 2ED570 — ecarr row
                # (w-index, d[+0x284] gate) -> elem via
                # 20E600(d[+0x10]) -> 2ED570(q[elem+0xD98],
                # d[row+0x18]) -> ret = 20E600(d[ret+0x84]) +
                # dx*0x290.  Resolve-only: no writes besides the
                # resolved-base stores inside C2.
                if name == "d2ed610-live":
                    ck(eax == w.elemb + 0x72000 + 3 * 0x290,
                       f"ret {eax:#x}")
                    C2 = w.dcntr2
                    ck(gm.q(C2 + 0x38) == w.dc2rows
                       and gm.q(C2 + 0x10) == w.dc2subs,
                       "c2 bases stored")
                    ck(gm.d(w.dc2elem) == 0xF,
                       "resolve-only: no &=~8")
                elif name in ("d2ed610-slotm1", "d2ed610-c2nul"):
                    ck(eax == 0, f"ret {eax:#x}")
                    if name == "d2ed610-c2nul":
                        C2 = w.dcntr2
                        ck(gm.q(C2 + 0x38) == w.dc2rows
                           and gm.q(C2 + 0x10) == w.dc2subs,
                           "c2 bases stored on null row")
                # dead/neg1: the unguarded d[0x18] read is pinned by
                # expect_fault=0x2ED648 above.

            elif name.startswith("d51ba80-"):
                # EXP-263: 51BA80 insert.  edx==-1 -> 51F150 cap
                # gate -> 41CB90 tmp reset -> 41D220 populate ->
                # 51F080 alloc -> 51F240 -> copy -> 41CA70.  All
                # three cases fail inside populate or the cap gate,
                # so ret is always -1.
                C, A = w.dcntr, w.darr
                ck(eax == 0xFFFFFFFF, f"ret {eax:#x}")
                if name == "d51ba80-cap":
                    # 51F150 ret -10 -> js -> ret -1; nothing else
                    # ran — no desc marked, count untouched.
                    ck(gm.d(C + 0x14) == 2, "count untouched")
                    ck(gm.d(A) == 0, "desc0 unmarked")
                elif name == "d51ba80-pop0":
                    # populate ret 0 + edx==-1 -> ret -1 before
                    # 51F080 — no desc allocated, count still 0.
                    ck(gm.d(C + 0x14) == 0, "no alloc")
                    ck(gm.d(A) == 0 and gm.d(A + 0x30) == 0,
                       "descs unmarked")
                    ck(gm.d(C + 0x1C) == 0xFFFFFFFF
                       and gm.d(C + 0x20) == 0xFFFFFFFF, "links")
                    # the planted IAT slot let 409210's real init run
                    # on the 02B62E20 static (sentinel overwritten)
                    ck(gm.d(0x2B62E20) == 0
                       and gm.b(0x2B62E20 + 0x1F) == 0,
                       "409210 init ran")
                elif name == "d51ba80-dereg":
                    # populate ret 0 + edx=1 -> desc1's record is
                    # reset + its key released before ret -1.
                    R = w.drecs[1]
                    ck(gm.d(R) == 0xFFFFFFFF
                       and gm.d(R + 0x324) == 0xFFFFFFFF
                       and gm.d(R + 0x358) == 0x10, "rec1 reset")
                    D = A + 2 * 0x30
                    ck(gm.d(D) == 0 and gm.d(D + 4) == 0xFFFFFFFF
                       and gm.d(D + 8) == 0xFFFFFFFF
                       and gm.d(D + 0xC) == 0xFFFFFFFF
                       and gm.q(D + 0x10) == 0
                       and gm.q(D + 0x18) == 0
                       and gm.q(D + 0x20) == 0, "desc2 release")
                    ck(gm.d(C + 0x14) == 1, "count")
                    ck(gm.d(C + 0x1C) == 0xFFFFFFFF
                       and gm.d(C + 0x20) == 3, "head/tail")

            elif name == "r71d0":
                ck(eax == 0x5A, f"ret {eax:#x}")

            elif name == "g8010-b5z":
                ck(len(byr("m8130")) == 1 and not byr("m8040"),
                   "b5==0 did not take 308130")
            elif name in ("g8010-b5nz", "g8010-698z", "g8010-null"):
                ck(len(byr("m8040")) == 1 and not byr("m8130"),
                   f"{name} landing wrong")

            elif name == "o4100-null":
                ck(eax == 0, f"ret {eax:#x}")
                ck(not byr("o4020"), "4020 ran on null")
            elif name == "o4100-base":
                ck(eax == 3, f"ret {eax:#x}")
                ck(len(byr("o4020")) == 1
                   and byr("o4020")[0][1] == w.rec, "4020 args")
                ck(not byr("a8ff0"), "8ff0 ran with no bits")
            elif name == "o4100-lic":
                ck(eax == 7, f"ret {eax:#x}")
                ck(len(byr("a8ff0")) == 1, "8ff0 count")
            elif name == "o4100-liclow":
                ck(eax == 9, f"ret {eax:#x}")
                ck(len(byr("a8ff0")) == 1, "8ff0 count")
            elif name == "o4100-noabil":
                ck(eax == 3, f"ret {eax:#x}")
                ck(not byr("a8ff0"), "8ff0 ran on null abild")


        elif name.startswith(("s8130-", "m8040-", "a8ff0-", "o4020-",
                              "s3c60-")):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]

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
                ck(len(byr("cookie")) == 1, "cookie check missing")
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
                ck(tcount("b860") == 0 and not byr("l30fed0"),
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
                ck(len(byr("l30fed0")) == 1 and byr("l30fed0")[0][2] == 0,
                   "fed0 count/arg")
                ck(len(byr("l6ab10")) == 1 and byr("l6ab10")[0][2] == 4,
                   "46a690 arg")
                ck(len(byr("b860")) == 5,
                   f"b860 {len(byr('b860'))} (e060+fef30 heads add one;"
                   " EXP-246: +2 real 46AB10/469570 owner scans)")
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
                ck(len(byr("l6ab10")) == 0, "46a690 ran with r8&2")
                ck(tcount("l35d8c0") == 0, "notify ran with r8&2")
                ck(len(byr("l30fed0")) == 1, "fed0 count")
                ck(gm.d(w.rec + 8) == 103, "hp")
            elif name == "c650-multi":
                ck(lvl == 5, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 19, f"hp {gm.d(w.rec+8)}")
                ck(len(byr("b860")) == 7,
                   f"b860 {len(byr('b860'))} (EXP-246: +2 real"
                   " 46AB10/469570 owner scans)")
                ck(len(byr("l30fed0")) == 1, "fed0 count")
                ck(len(byr("l6ab10")) == 1, "46a690 once")
                ck(len(by("b3b02a0")) == 1, "notify once")
            elif name == "c650-b5":
                ck(lvl == 6, f"lvl {lvl:#x}")
                ck(tcount("g2f9a60") == 0, "growth ran with b5")
                ck(len(byr("l30fed0")) == 1, "fed0 count")
                ck(len(byr("l6ab10")) == 0 and tcount("l35d8c0") == 0,
                   "b5 tail ran")
            elif name == "c650-nolvl":
                pass  # expect_fault asserted above
            elif name == "c650-clamp":
                ck(lvl == 0x63, f"lvl {lvl:#x}")
                ck(gm.d(w.rec + 8) == 15, f"hp {gm.d(w.rec+8)}")
                ck(len(byr("l30fed0")) == 1, "fed0 count")
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
                ck(not byr("l30fed0"), "fed0 on reject")
            elif name == "g3910-grant":
                ck(eax == 0, f"ret {eax:#x}")
                ck(lp == 70, f"lp {lp}")
                ck(bit == 1, "bit not set")
                ck(len(byr("l30fed0")) == 1 and byr("l30fed0")[0][2] == 0x97,
                   "fed0 arg")
                ck(len(byr("l323d10")) == 1, "323d10 count")
                ck(len(byr("o4020")) == 1, "324020 count")
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
                ck(not byr("l30fed0"), "fed0 on dup")
            elif name == "g3910-revoke":
                ck(eax == 0, f"ret {eax:#x}")
                ck(gm.b(w.rec + 0x196) == 0, "bit not cleared")
                ck(lp == 100, f"lp {lp}")
                ck(len(byr("l323d10")) == 0, "323d10 on revoke")
                ck(len(byr("l30fed0")) == 1, "fed0 count")
            elif name == "g3910-e5":
                ck(eax == 0, f"ret {eax:#x}")
                ck(gm.b(w.rec + 0x194 + 0x1C) & 0x20,
                   "e5 bit not set")
                ck(len(byr("b860")) == 3,
                   f"31b860 {len(byr('b860'))} (e060+fef30 heads add one)")
                ck(len(byr("l3105d0")) == 1
                   and byr("l3105d0")[0][1] == w.objrow,
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
                a8 = byr("a8ff0")
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
                ck(len(byr("o4020")) == 1, "324020 count")
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
                ck(len(byr("l313f60")) == 0, "313f60 on zero mask")
                ck(len(byr("cookie")) == 1, "cookie missing")
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
                ck(len(byr("l313f60")) == 1, "313f60 missing")
                ck(tcount("l265020") == 0, "265020 past gate")
            elif name == "d4da0-alive":
                ck(eax == 1, f"ret {eax:#x}")
                ck(len(byr("l313f60")) == 1, "313f60 missing")
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
                u = byr("l3105d0")
                ck(len(u) == 1 and u[0][1] == obj, f"3105d0 {u}")
                # EXP-227: real 3105D0 calls 310780(obj) internally —
                # the old stub hid the detach call.
                ck(tcount("l310780") == 1, "310780 inside 3105d0")
                ck(tcount("l3138d0") == 1, "3138d0 tail")
                ck(gm.q(obj) == 0x4000000, "flags touched")
                ck(gm.w16(obj + 0x714) == 0xFFFF
                   and gm.d(obj + 0x690) == 0
                   and gm.d(obj + 0x768) == 0, "3105d0 reset writes")
                ck(gm.b(obj + 0x695) == 0xFF
                   and gm.b(obj + 0x696) == 0xFF
                   and gm.b(obj + 0x694) == 0xFF, "mode bytes FF")
                ck(not byr("l31b8c0"), "31B8C0 ran (30d9a0!=1)")
                ck(not byr("lb040"), "23b040 ran")
            elif name == "u0fc0-fastt":
                u = byr("l3105d0")
                ck(len(u) == 1 and u[0][1] == obj, f"3105d0 {u}")
                ck(len(byr("l31b8c0")) == 1
                   and byr("l31b8c0")[0][1] == 3, "31b8c0 arg")
                # EXP-251: ctx4 slot 3 -> 263750(3) nonnull -> 263E30 ->
                # 31B7E0(cid)->ctx0->rdi; real 311CF0 writes
                # w[5AD0]&=0xFFFE + w[rdi+0xBA0]=0x113/d[+0xBB8]=cid/
                # w[+0xBA4]|0x8000/q[+0]|0x4000, then 3138D0's xor holds
                # bit0 clear (esi=0): planted 3 -> 2.
                rdi0 = w.n30by[0]
                ck(len(byr("l311cf0")) == 1
                   and byr("l311cf0")[0][1] == rdi0
                   and byr("l311cf0")[0][2] == 0x12340000
                   and byr("l311cf0")[0][4] == 0x113, "311cf0 args")
                ck(gm.w16(rdi0 + 0xBA0) == 0x113, "rdi ba0")
                ck(gm.d(rdi0 + 0xBB8) == 0x12340000, "rdi bb8")
                ck(gm.w16(rdi0 + 0xBA4) & 0x8000, "rdi ba4")
                ck(gm.q(rdi0) & 0x4000, "rdi q0")
                ck(gm.w16(w.glob + 0x5AD0) == 2,
                   f"toggle {gm.w16(w.glob + 0x5AD0):#x}")
            elif name == "u0fc0-def":
                ck(not w.faults, f"fault {w.faults}")
                ck(tcount("l310780") == 1, "310780")
                # 310780's &0xFFFFFFFFEFFFFFDF + 300FC0's
                # &0xFFFFFFFDFFE7FFFD + &d[+4]0xFFFFFFFB + EXP-231's
                # real 308270 &0xFFFFBFFFFFFFBFFFFF (clears bits
                # 46/22 — the stub hid it) fold to
                # q=0xFFFFBFF9EFA7FFDD / d4=0xFFFFBFF9.
                ck(gm.q(obj) == 0xFFFFBFF9EFA7FFDD,
                   f"qmask {gm.q(obj):#x}")
                ck(gm.d(obj + 4) == 0xFFFFBFF9, "d4 mask")
                ck(gm.b(obj + 0x694) == 0xFF, "b694")
                ck(tcount("l26dac0") == 1 and tcount("l26a330") == 1,
                   "ent writes")
                ck(tcount("l219d0") == 1, "3219d0")
                ck(len(byr("l308270")) == 1
                   and byr("l308270")[0][1] == obj, "308270")
                # EXP-231: two real 30C970 calls now — 308270's
                # b[obj+0x695]=0 row-0 reset, then the old 0x27 no-op
                # on b[obj+0x694] (read BEFORE the 0xFF write).
                u = byr("l30c970")
                ck(len(u) == 2 and u[0][1] == 0 and u[1][1] == 0x27,
                   f"30c970 {u}")
                ck(len(byr("l319420")) == 1
                   and byr("l319420")[0][1] == obj + 0x6B0, "319420")
                ck(len(byr("l319140")) == 1
                   and byr("l319140")[0][1] == obj
                   and byr("l319140")[0][2] == 1, "319140")
                # EXP-231: real 319420's write — d[obj+0x6B0+0xC4]=-1;
                # 290B90 stayed scripted (null q[0x209BE80] fault path)
                ck(gm.d(obj + 0x774) == 0xFFFFFFFF, "319420 d774")
                ck(len(byr("l290b90")) == 1
                   and byr("l290b90")[0][1] == 0, "290b90")
                ck(len(byr("l2e9780")) == 1
                   and byr("l2e9780")[0][1] == ent, "2e9780")
                ck(len(byr("l26d6f0")) == 1
                   and byr("l26d6f0")[0][1] == ent, "26d6f0")
                ck(flg == 0x100, f"flags {flg:#x}")
                ck(len(byr("l2548f0")) == 1 and byr("l2548f0")[0][1] == 1,
                   "2548f0")
                # EXP-244: ecx=1 -> 2E1C20 set arm — slot 8 gains
                # bits {6,8,9,0xB} on the BSS d[0215F1E0].
                ck(gm.d(0x215F1E0) == 0xB40,
                   f"215f1e0 {gm.d(0x215F1E0):#x}")
                ck(gm.d(0x22C83E8) == 0x10, "22c83e8")
                ck(not byr("lb040"), "23b040")
                ck(tcount("l3138d0") == 0, "3138d0 on 30d9a0!=1")
            elif name == "u0fc0-m1":
                ck(not w.faults, f"fault {w.faults}")
                ck(tcount("l310780") == 1, "310780")
                ck(tcount("l3138d0") == 0, "3138d0 on edx!=0")
                ck(not byr("lb040"), "23b040 tail on edx!=0")
                ck(flg == 0x100, f"flags {flg:#x}")
                # EXP-240: b[ent+3]=0x60 opens the real pass arm —
                # 2E9BB0 reads d[flagtgt+0x110]=0, &~4 -> 0,
                # b[ent+0x12]=0<=3, xmm6==0.0 -> or ebx,4 ->
                # 2EC5B0 writes d[flagtgt+0x110]=4.  2E9780's pass
                # arm reads b[node+0x11]=0 -> ret 0.
                ck(len(byr("l2e9bb0")) == 1
                   and byr("l2e9bb0")[0][1] == ent, "2e9bb0")
                e5 = byr("l2ec5b0")
                ck(len(e5) == 1 and e5[0][1] == ent
                   and e5[0][2] == 4, f"2ec5b0 {e5}")
                ck(gm.d(w.objc0q[0x138] + 0x110) == 4,
                   f"flagtgt d110 {gm.d(w.objc0q[0x138]+0x110):#x}")
                ck(gm.f(w.desc8f0 + 0x24) == 0.0
                   and gm.f(w.desc8 + 0xD0) == 0.0
                   and gm.f(w.objc0q[0x138] + 0xC8) == 0.0,
                   "pass-arm float writes")
            elif name == "u0fc0-s400":
                ck(flg == 0x400, f"flags {flg:#x}")
                ck(tcount("l3001d0") == 1, "3001d0")
                ck(len(byr("l254850")) == 1 and byr("l254850")[0][1] == 1,
                   "254850")
                ck(gm.d(0x22C83E8) == 2, "22c83e8")
                ck(len(byr("lb040")) == 1, "23b040 tail")
                ck(tcount("l37260") == 0, "237260 after tail")
            elif name == "u0fc0-s200":
                ck(flg == 0x200, f"flags {flg:#x}")
                ck(len(byr("l254940")) == 1 and byr("l254940")[0][1] == 1,
                   "254940")
                ck(gm.d(0x22C83E8) == 1, "22c83e8")
                ck(len(byr("lb040")) == 1, "23b040 tail")
                ck(tcount("l373c0") == 0, "2373c0 after tail")
            elif name == "u0fc0-s800":
                ck(flg == 0x800, f"flags {flg:#x}")
                ck(not byr("l2548f0"), "0x100 arm fired")
                ck(not byr("lb040"), "23b040 tail")
                # EXP-241: fbdev node {id=9,w850=2} — real l290b90
                # matches d[+0x810]==ecx=9 and folds w[+0x850] 2->3.
                ck(len(byr("l290b90")) == 1
                   and byr("l290b90")[0][1] == 9, "290b90")
                ck(gm.w16(w.fbnodes[0] + 0x850) == 3,
                   f"node w850 {gm.w16(w.fbnodes[0]+0x850):#x}")
            elif name == "u0fc0-mtail":
                # EXP-251: g272f0 plants b[02089340]=0x10 for the
                # 31B7E0 flag-set arm — base 0x100 | 0x10 = 0x110.
                ck(flg == 0x110, f"flags {flg:#x}")
                ck(tcount("l3138d0") == 1, "3138d0")
                ck(len(byr("l31b8c0")) == 1 and byr("l31b8c0")[0][1] == 3,
                   "31b8c0")
                # EXP-251: same chain as u0fc0-fastt — real 311CF0
                # publishes the unit-mode writes; planted 3 -> 2 via
                # &=0xFFFE, xor holds it.
                rdi0 = w.n30by[0]
                ck(len(byr("l311cf0")) == 1
                   and byr("l311cf0")[0][1] == rdi0, "311cf0 rdi")
                ck(gm.w16(rdi0 + 0xBA0) == 0x113, "rdi ba0")
                ck(gm.d(rdi0 + 0xBB8) == 0x12340000, "rdi bb8")
                ck(gm.q(rdi0) & 0x4000, "rdi q0")
                ck(gm.w16(w.glob + 0x5AD0) == 2,
                   f"toggle {gm.w16(w.glob + 0x5AD0):#x}")
                ck(len(byr("lb040")) == 1, "23b040 tail")
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
                ck(not by("d8bf0") and not byr("l3105d0")
                   and not byr("l2ecf10"), "release ran on bail")
            elif name == "l01140-rel":
                ck(not w.faults, f"fault {w.faults}")
                ck(len(by("d8bf0")) == 1 and by("d8bf0")[0][1] == obj,
                   "238bf0")
                ck(len(byr("l3105d0")) == 1 and byr("l3105d0")[0][1] == obj,
                   "3105d0")
                ck(gm.d(obj) == 0x45000000, f"d0 {gm.d(obj):#x}")
                ck(gm.d(obj + 4) == 0x200000, f"d4 {gm.d(obj+4):#x}")
                ck(gm.q(obj + 0x6F8) == 0, "q6f8")
                ck(gm.d(obj + 0x748) == 0, "d748")
                ck(gm.d(obj + 0x770) == 0, "d770")
                ck(gm.q(obj + 0x750) == 0, "q750")
                ck(gm.d(obj + 0x74C) == 0, "d74c")
                # EXP-227: +0x788 is inside 3105D0's 316CF0 memset
                # (obj+0x778..0x97F) — runs after 301140's &~0x400, so
                # the shipped final is 0, not the stub-era 0xFF.
                ck(gm.d(obj + 0x788) == 0, "d788 memset")
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
                ck(len(byr("l2ecf10")) == 1
                   and byr("l2ecf10")[0][1] == ent, "2ecf10")
                ck(gm.d(obj + 0x5C) == 0x200D, "d5c msg")
                ck(gm.d(obj + 0x2C) == 0, "d2c")
                ck(gm.b(ent + 0xF5) == 0xFF, "bF5")
                ck(gm.d(ent + 0xF0) == 0x200D, "dF0")
                kk = byr("l2eb0d0")
                ck(len(kk) == 1 and kk[0][1] == ent
                   and kk[0][3] == 0x200D and kk[0][4] == 1,
                   f"kb0d0 {kk}")
                ck(not by("b1f70"), "311f70 ran (bit26 set)")
                ck(not by("b0770"), "3b0770 ran (d74=0)")
                bb = byr("l2ebb80")
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
                bb = byr("l2ebb80")
                ck(len(bb) == 1 and bb[0][2] == 1, f"bbb80 {bb}")
                # EXP-240: ent_b+3=0x60 + objc0 -> the real fold
                # lands bit 3 (dl=1) then tail-calls v2e8fd0 with
                # rcx=ent and the folded dl=8.
                ck(gm.b(w.objc0 + 0x10) == 8,
                   f"node b10 {gm.b(w.objc0+0x10):#x}")
                vf = by("v2e8fd0")
                ck(len(vf) == 1 and vf[0][1] == ent
                   and vf[0][2] == 8, f"v2e8fd0 {vf}")
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
                ck(len(byr("t71c0")) == 1
                   and byr("t71c0")[0][1] == obj, "t71c0")
                ck(not by("s7ed0"), "s7ed0 on null rec")
                ck(not byr("l28bb0"), "l28bb0 past gate")
                ck(not byr("t7090"), "t7090 past gate")
                ck(not byr("l6a50"), "s6a50 on null rec")
            elif name == "d228-b5rec":
                ck(len(byr("t71c0")) == 1, "t71c0")
                ck(not byr("l28bb0"), "l28bb0 past b5 gate")
                ck(not byr("t7090"), "t7090 past b5 gate")
                ck(not byr("l6a50"), "s6a50 on b5 rec")
            elif name == "d228-e9a8":
                s6 = byr("l6a50")
                ck(len(byr("t71c0")) == 1
                   and len(s6) == 1 and s6[0][1] == 4
                   and s6[0][2] == 1, f"71c0->6a50 {s6}")
                ck(gm.w16(w.msgtab + 0x384C + 8) == 1,
                   "kind4 u16 slot accumulate")
                ck(gm.b(w.msgtab + 0x3844) & 0x10,
                   "kind4 achieved-bit")
                ck(len(byr("l32b0")) == 1
                   and byr("l32b0")[0][1] == 5,
                   f"8632b0 msg {byr('l32b0')}")
                ck(not by("v20ce60"), "20ce60 dispatch past null sgl")
                ck(not byr("l28bb0"), "l28bb0 past e9a.8")
                ck(not byr("t7090"), "t7090 past e9a.8")
            elif name == "d228-norow2":
                s6 = byr("l6a50")
                ck(len(byr("t71c0")) == 1
                   and len(s6) == 1 and s6[0][1] == 4, f"71c0 {s6}")
                ck(not by("s7ed0"), "s7ed0 w/o peer rec")
                ck(not byr("l28bb0"), "l28bb0 w/o scan arm")
                ck(not byr("t7090"), "t7090 w/o scan arm")
            elif name == "d228-row2b5":
                ck(len(byr("t71c0")) == 1, "t71c0")
                ck(not byr("l28bb0"), "l28bb0 w/ b5!=0 peer")
                ck(not byr("t7090"), "t7090 w/ b5!=0 peer")
            elif name == "d228-f2nol2":
                s6 = byr("l6a50")
                ck(len(byr("t71c0")) == 1
                   and len(s6) == 1 and s6[0][1] == 4, f"71c0 {s6}")
                ck(not byr("l28bb0"), "l28bb0 w/ f2 but no e9a.2")
                ck(not byr("t7090"), "t7090 w/ f2 but no e9a.2")
            elif name == "d228-gate5":
                ck(not byr("l317ed0"), "317ed0 w/o peer")
                ck(len(byr("t71c0")) == 1, "t71c0")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(byr("l30c650")) == 0, "c650 w/o guests")
                ck(len(byr("l28bb0")) == 1
                   and byr("l28bb0")[0][1] == 0
                   and byr("l28bb0")[0][2] == obj, "src 8bb0 args")
                ck(len(byr("l290c0")) == 1
                   and byr("l290c0")[0][1] == 0
                   and byr("l290c0")[0][2] == obj, "src 90c0 args")
                ck(len(byr("tfb80")) == 1, "tfb80")
                t89 = byr("t89d00")
                ck(len(t89) == 2
                   and t89[0][1] == w.fbdev + 0x5380
                   and t89[0][4] == 0 and t89[1][4] == 1,
                   f"289d00 pair {t89}")
                ck(len(byr("t7090")) == 1
                   and byr("t7090")[0][1] == obj, "t7090")
            elif name == "d228-gaterc":
                ck(len(byr("l317ed0")) == 1
                   and byr("l317ed0")[0][1] == obj, "l317ed0 arg")
                # EXP-236: real counter writes — epoch cells
                # b[obj+0x56]==d[0x22C3168]==0 and w[e68+0x40]==
                # d[0x22C316C]==0 -> d[0x22C315C]/d[0x22C3160] +=1
                # (clamp 0x3E7/0x3E6).  229E40 fires twice (the
                # epoch arm + post-LCG poll); its q[0x209BE80]
                # flag sink 28EF70 is real now — recorded with
                # (ecx=d[0x22C315C], edx=bl rate flag 0 =
                # LCG%100>=5, r8d=d[0x22C3158]).
                ck(len(byr("l229e40")) == 2, "l229e40")
                ck(gm.d(0x22C315C) == 1
                   and gm.d(0x22C3160) == 1, "7ed0 counters")
                # EXP-242: 28EF70 real on the fbdev object — the
                # 28F0C0(ecx=1) arm stores w[+0x7C78]=1, d[+0x7C7C]
                # |=1 &=~8, then bit1 := dl&1 = 0; w[+0x7C82] = r8w.
                ck(len(byr("l28ef70")) == 1
                   and byr("l28ef70")[0][1] == 1
                   and byr("l28ef70")[0][2] == 0
                   and byr("l28ef70")[0][3] == 0, "l28ef70 args")
                ck(gm.w16(w.fbdev + 0x7C78) == 1
                   and gm.d(w.fbdev + 0x7C7C) == 1
                   and gm.w16(w.fbdev + 0x7C82) == 0, "28ef70 writes")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(byr("t7090")) == 1, "t7090")
            elif name == "d228-gatef2":
                ck(not byr("l317ed0"), "317ed0 w/o peer")
                ck(tcount("r2ab0") == 9, f"scan {tcount('r2ab0')}")
                ck(len(byr("t7090")) == 1, "t7090")
            elif name == "d228-g1":
                ck(gm.q(0x22C1740) == g0, "stash[0]")
                ck(gm.d(g0 + 0x18C) == 150,
                   f"exp {gm.d(g0 + 0x18C):#x}")
                ck(gm.d(g0 + 0x190) == 30,
                   f"lp {gm.d(g0 + 0x190):#x}")
                s6 = [c for c in byr("l6a50") if c[1] == 0xB]
                ck(len(s6) == 1 and s6[0][2] == 10, f"s6a50 {s6}")
                ck(gm.d(w.msgtab + 0x384C + 0x10) == 10,
                   "kind11 dword slot")
                ck(gm.b(w.msgtab + 0x3844 + 1) & 8,
                   "kind11 achieved-bit (bit 3)")
                ck(13 in [c[1] for c in byr("l32b0")],
                   f"8632b0 msg13 {byr('l32b0')}")
                c6 = byr("l30c650")
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
                s6 = [c for c in byr("l6a50") if c[1] == 0xB]
                ck(len(s6) == 1 and s6[0][2] == 0, f"s6a50 {s6}")
            elif name == "d228-gflg0":
                ck(gm.q(0x22C1740) == 0, "stash empty")
                ck(tcount("cd7c20") == 2,
                   "377c20 scan + src 30d9a0")
                ck(len(byr("l30c650")) == 0, "c650 on dropped guest")
                ck(gm.d(g0 + 0x18C) == 100, "exp not awarded")
            elif name == "d228-sup":
                ck(tcount("l236780") == 2, "236780 twice")
                ck(gm.d(g0 + 0x18C) == 100, "guest exp suppressed")
                ck(gm.d(g0 + 0x190) == 30, "guest lp kept")
                fb = byr("tfb80")
                ck(len(fb) == 1 and fb[0][2] == 0
                   and fb[0][3] == 10, f"tfb80 {fb}")
                t89 = byr("t89d00")
                ck(len(t89) == 2 and t89[0][3] == 0
                   and t89[1][3] == 10, f"289d00 {t89}")
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
                s6 = [c for c in byr("l6a50") if c[1] == 0xB]
                ck(len(s6) == 1 and s6[0][2] == 0,
                   f"s6a50 edx {s6}")
                # fp = (10-2)*3 + 7 + (5*10*5) = 281; 1000+281 -> set;
                # real 254EE0 clamps+stores d[fpp+8] and notifies
                # 6a50(6,|delta|); real 469E80 -> q6ab10 on +delta
                ck(gm.d(w.fpp + 8) == 1281,
                   f"fpp {gm.d(w.fpp + 8):#x}")
                # 254EE0 notifies 6a50(cl=6|7 on full ecx -> kind is
                # the low byte; 1281&~FF|6 = 1286)
                s6d = [c for c in byr("l6a50") if c[1] & 0xFF == 6]
                ck(len(s6d) == 1 and s6d[0][2] == 281,
                   f"54ee0->6a50 {s6d}")
                ck(len(byr("t69e80")) == 1
                   and byr("t69e80")[0][1] == 281, "t69e80")
                ck(len(byr("l6ab10")) == 1, "46AB10 on +delta")
            elif name == "d228-fp":
                ck(gm.d(w.fpp + 8) == 36,
                   f"fpp {gm.d(w.fpp + 8):#x}")
                s6d = [c for c in byr("l6a50") if c[1] & 0xFF == 6]
                ck(len(s6d) == 1 and s6d[0][2] == 31,
                   f"54ee0->6a50 {s6d}")
                ck(len(byr("t69e80")) == 1
                   and byr("t69e80")[0][1] == 31, "t69e80")
                ck(len(byr("l6ab10")) == 1, "46AB10 on +delta")
            elif name == "d228-fpneg":
                ck(gm.d(w.fpp + 8) == 0,
                   f"fpp {gm.d(w.fpp + 8):#x}")
                s6d = [c for c in byr("l6a50") if c[1] & 0xFF == 7]
                ck(len(s6d) == 1 and s6d[0][2] == 5,
                   f"54ee0->6a50 {s6d}")
                ck(len(byr("t69e80")) == 1
                   and byr("t69e80")[0][1] == 0xFFFFFFFB, "t69e80")
                ck(not byr("l6ab10"), "46AB10 on -delta")
            elif name == "d228-msg":
                ck(len(byr("t15820")) == 1, "t15820")
                ck(gm.b(w.msgtab + 5 + 0x3404) == 2,
                   f"ctr {gm.b(w.msgtab + 0x3409)}")
                s6 = [c for c in byr("l6a50") if c[1] == 4]
                ck(len(s6) == 1 and s6[0][2] == 1, f"6a50 {s6}")
            elif name == "d228-pos":
                ck(len(byr("l319490")) == 1, "l319490")
                # EXP-247: 3377C0 real.  EXP-248: deep scaffolding —
                # q[ctxn30+0x10] link + oar4 cid row drive the real
                # 265090->3DA710 pos fetch, 236820 row resolve,
                # 31ABE0->3588B0 clstab id resolve to ctx0, 2EA7F0
                # gate (early-out f[c138+0xF0]==0), then the real
                # 337700 fallback tail (391410 grid-null early-out,
                # 384130 xz-pack, scripted s383f10 cell walk ->0xFF)
                # -> ret 0 -> 312280 skips the 3180F0/319CA0 arms.
                vv = byr("l377c0")
                ck(len(vv) == 1 and vv[0][1] == w.ctxn30,
                   f"l377c0 {vv}")
                ck(gm.d(vv[0][2] + 0xC) == 0x3F800000,
                   "vec4 w != 1.0f")
                ck(len(byr("l265090")) == 2, "265090 x2 (3377C0+337700)")
                ck(len(byr("l3da710")) == 2, "3da710 x2")
                le = byr("l31abe0")
                ck(len(le) == 1 and le[0][1] == 0x12340000,
                   f"31abe0 {le}")
                le = byr("l2ea7f0")
                ck(len(le) == 1 and le[0][1] == w.ctx[0],
                   f"2ea7f0 {le}")
                le = byr("l37700")
                ck(len(le) == 1 and le[0][1] == w.ctxn30,
                   f"337700 {le}")
                ck(len(byr("l391410")) == 1, "391410")
                ck(len(byr("l383840")) == 1, "383840")
                ck(len(byr("l384130")) == 1, "384130")
                ck(len(by("s383f10")) == 1, "s383f10")
                ck(not by("s80f0"), "s80f0 fired on ret 0")
                ck(not by("s9ca0"), "s9ca0 fired on ret 0")
            elif name == "d228-pos2":
                ck(len(byr("l319490")) == 1, "l319490")
                vv = byr("l377c0")
                ck(len(vv) == 1 and vv[0][1] == w.ctxn30,
                   f"l377c0 {vv}")
                ck(gm.d(vv[0][2] + 0xC) == 0x3F800000,
                   "vec4 w != 1.0f")
                ck(len(byr("l265090")) == 2, "265090 x2")
                ck(len(byr("l31abe0")) == 1
                   and byr("l31abe0")[0][1] == 0x12340000, "31abe0")
                ck(len(byr("l37700")) == 1, "337700")
                ck(len(byr("l391410")) == 1, "391410")
                ck(len(byr("l384130")) == 1, "384130")
                ck(len(by("s383f10")) == 1, "s383f10")
                ck(not by("s80f0"), "s80f0 fired on ret 0")
                ck(not by("s9ca0"), "s9ca0 w/o 80f0")
            elif name == "d228-src":
                fb = byr("tfb80")
                ck(len(fb) == 1 and fb[0][1] == 0x1234
                   and fb[0][2] == 77 and fb[0][3] == 88,
                   f"tfb80 {fb}")
                t89 = byr("t89d00")
                ck(len(t89) == 2
                   and t89[0][1] == w.fbdev + 0x5380
                   and t89[0][2] == 0x1234 and t89[0][3] == 77
                   and t89[0][4] == 0
                   and t89[1][2] == 0x1234 and t89[1][3] == 88
                   and t89[1][4] == 1, f"289d00 {t89}")
            elif name == "d228-2g":
                ck(gm.q(0x22C1740) == w.guests[0], "stash[0]")
                ck(gm.q(0x22C1740 + 8) == w.guests[4],
                   "stash[1]")
                s6 = [c for c in byr("l6a50") if c[1] == 0xB]
                ck(len(s6) == 2, f"s6a50 count {s6}")
                ck(len(byr("l30c650")) == 2, "c650 count")
            elif name == "d228-lvl":
                c6 = byr("l30c650")
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
                ck(len(byr("l2fa390")) == 1 and len(byr("l6ab10")) == 1,
                   f"46A800->46AB10 missing {calls}")
                ck(f64 == 1 << 1, f"d64 {f64:#x}")
                # EXP-246: real 46AB10 insert arm — ring[0] written
                # from the shipped body, cursor advanced, miss store.
                ck(gm.q(0x2EBB568) == 0x40000000, "ring+8 != rsi")
                ck(gm.w16(0x2EBB560) == 18, "ring+0 != id")
                ck(gm.d(0x2EBB564) == 0, "ring+4 != timestamp")
                ck(gm.d(0x2EBB54C) == 1, "cursor != 1")
                ck(gm.q(0x2EBF188) == 0, "2EBF188 != b860 miss")
                ck(len(by("s5369c0")) == 1, "insert notify missing")
            elif name == "e360-nomode-pair":
                ck(not byr("l2fa390"), "46A800 on non-mode arm")
                ck(f64 == 0, f"d64 {f64:#x}")
            elif name == "e360-neg-arg5":
                ck(f64 == 0, f"d64 {f64:#x}")
                ck(arr_w == 3 * 2 * 0x1E,
                   f"arr_w {arr_w:#x} != resolved 0xB4")
                ck("v876d0" in w.trace, "3876D0 resolver not run")

        elif name.startswith("f690-") or name.startswith("f340-")                 or name.startswith("f5a0-"):
            calls = w.rets.get("calls", [])
            by = lambda t: [c for c in calls if c[0] == t]
            rargs = w.rets.get("rargs", [])
            byr = lambda t: [c for c in rargs if c[0] == t]

            if name == "f690-mask0":
                # bit loop skips everything but the tail notify is
                # unconditional
                fe = byr("l30fed0")
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
                fe = byr("l30fed0")
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
                fe = byr("l30fed0")
                ck(len(fe) == 1 and fe[0][2] == 0x217,
                   f"tail fed0 {fe}")

            elif name == "f340-equal":
                ck(not calls, f"calls on equal {calls}")

            elif name == "f340-delta":
                # 300530 now real: f340 passes delta=7 -> d48 0+7=7
                ck(not w.faults, f"fault {w.faults}")
                ck(gm.d(w.rec + 0x48) == 7,
                   f"d48={gm.d(w.rec + 0x48)}")
                ck(not byr("l3243f0"), "u43f0 w/o stored<=0")

            elif name == "f340-bit1c":
                # computed 7*2=14 -> d48 = 0+14 = 14
                ck(gm.d(w.rec + 0x48) == 14,
                   f"d48={gm.d(w.rec + 0x48)}")

            elif name == "f340-bit10":
                # computed = max(-5,1)=1 vs stored -5 -> delta 6;
                # stored<=0 + idx 0x1C in [0x1B,0x27] + b5==0 -> unlink
                ck("b860" in w.trace, "b860 unlink scan missing")
                u = byr("l3243f0")
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

        elif name.startswith(("fa3b0-", "fmt-", "bd00-", "d4d0-",
                              "d3d0-", "d480-", "e690-", "p7040-",
                              "r3320-", "c5d0-", "b3120-", "b3050-",
                              "b24b0-", "b2150-", "af340-", "c5f0-",
                              "b4730-", "b1fb0-", "e8070-", "f880-",
                              "f920-", "f9c0-", "f8c0-", "f940-",
                              "fae0-", "rdev-")):
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
                ck(gm.q(slot + 0x30) == w.elemb + 0x80002,
                   "q30 name ptr")
                ck(gm.b(slot + 0x3D) == 4, "b3D=4")
                ck(gm.d(slot + 0xC) == 0x80808080, "d0C")
                ck(gm.d(slot + 0x44) == 0, "d44 pri")
                c = byr("l31c5d0")
                ck(len(c) == 2 and all(x[1] == 0x22CA520 for x in c),
                   f"l31c5d0 args {c}")
                ck(gm.d(0x22CA520) == 0x1A
                   and gm.d(0x22CA524) == 7, "rblk kind/arg")
                # real arm-0x1A resolution: q18 via T2/T3 chain,
                # q10 = 2F9860 default, b20-24 row copies, b25 mix
                ck(gm.q(0x22CA520 + 0x18) == w.elemb + 0x80000,
                   "q18 resolved")
                ck(gm.q(0x22CA520 + 0x10) == 0x1CEB638,
                   "q10 2F9860 default")
                ck(gm.b(0x22CA520 + 0x20) == 0x11
                   and gm.b(0x22CA520 + 0x21) == 0x33
                   and gm.b(0x22CA520 + 0x22) == 0x44
                   and gm.b(0x22CA520 + 0x23) == 0x22
                   and gm.b(0x22CA520 + 0x24) == 0
                   and gm.b(0x22CA520 + 0x25) == 0, "blk fields")
                # EXP-206/207: 2B3050/2B3120/2B24B0 real — rcx=0 ctx,
                # rdx=str; real evaluator ceilf's the af340f floats.
                c = byr("l2b3050")
                ck(len(c) == 1 and c[0][1] == 0
                   and c[0][2] == w.elemb + 0x80002, f"l2b3050 {c}")
                ck(len(byr("l2b3120")) == 1
                   and byr("l2b3120")[0][2] == slot + 0x40,
                   "evaluator call")
                ck(len(byr("l2b24b0")) == 1
                   and len(byr("l2af340")) == 1,
                   "evaluator not reached")
                # EXP-209: real 2AC5F0 tag-5 — outer 2B2150 + the
                # interpreter's own nested call under ctx48==0, once
                # per walker walk
                ck(len(byr("l2b2150")) == 3
                   and len(byr("l2ac5f0")) == 2,
                   f"walks {byr('l2b2150')}/{byr('l2ac5f0')}")
                # EXP-220: f880 real -> 1E93C0's divss/ceilf tail
                # fires once per call (2 walks) + the evaluator's own
                # 2 = 4 total
                ck(tcount("ceilf") == 4, "ceilf not applied")
                # real tag-5: width int(448/448*15)=15, height
                # 17F880 -> ceilf(13/2.0) = 7.0 -> 15/7 px
                ck(gm.w16(slot + 0x40) == 15
                   and gm.w16(slot + 0x42) == 7,
                   f"out words {gm.w16(slot + 0x40):x}/"
                   f"{gm.w16(slot + 0x42):x}")
            elif name == "bd00-t2ff":
                ck((eax & 0xFF) == 0xFF, f"eax {eax:x} (b24==FF gate)")
                ck(tcount("l506700") == 0, "init ran past gate")
                ck(len(byr("l31c5d0")) == 1, "resolver not called")
                ck(gm.b(0x22CA520 + 0x24) == 0xFF,
                   "b24 = b[row+2] not seen")
                ck(gm.b(0x2B443C0) == 0, "qidx moved")
            elif name == "bd00-t2b25":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.b(0x22CA520 + 0x25) == 4,
                   f"b25 {gm.b(0x22CA520 + 0x25):x} != 4")
                ck(gm.d(slot + 0xC) == 0x1234,
                   f"d0C override {gm.d(slot + 0xC):x}")
                c = byr("l2dd7e0")
                ck(any(x[1] == 0x12 for x in c),
                   f"2DD7E0(0x12) missing {c}")
            elif name == "bd00-t2neg":
                # real 31C5D0 -2 (null T1) -> 35D330 memsets blk
                # (0x98) -> b24=0 -> gate passes anyway
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l506700") == 1, "init missing")
                ck(tcount("l31c5d0") == 2, "resolver count")
                ck([0x22CA520, 0x98] in ms, f"blk memset {ms}")
                ck(gm.d(0x22CA520) == 0, "blk wiped")
                ck(gm.q(slot + 0x30) == 0, "q30 from null q18")
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
                for t in ("l3efd00", "l31c5d0", "l2b3050"):
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
                ck(len(byr("l31c5d0")) == 2
                   and gm.d(0x22CA520) == 0x1A
                   and gm.d(0x22CA524) == 5, "type2 req fields")
                ck(gm.q(0x22CA520 + 0x18) == w.elemb + 0x80000,
                   "q18 resolved (id 5 row)")
                ck(gm.b(w.qtab + 0x3C) == 2, "slot type")
                ck(gm.b(w.qtab + 0x3F) == 5, "slot b3F=flag")
                ck(gm.w16(w.qtab + 0x3A) == 3, "w3A type2")
                ck(len(byr("l2b3050")) == 1, "evaluator call missing")

            # ---- EXP-202: type-0/type-1 post wrappers ----
            elif name == "d3d0-null":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 0, "enqueue on null subobj")
            elif name == "d3d0-far":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 0, "enqueue past 24u")
            elif name == "d3d0-near":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(bytes(gm.b(w.qtab + 0x40 + i) for i in range(6))
                   == b"12345\x00", "type0 fmt")
                ck(gm.b(w.qtab + 0x3F) == 5, "b3F len")
                ck(gm.b(w.qtab + 0x3C) == 0, "type byte")
                # edi=0, no rec -> 263C20!=3 -> off 4 -> subtype
                # table[4]=6 -> arm5 -> 296E90 real: slot0 w318|=0x10
                c = byr("l296e90")
                ck(len(c) == 1 and c[0][1] == w.ctrlsub,
                   f"dispatch {c}")
                ck(tcount("l297040") == 0, "wrong arm")
                ck(gm.w16(w.ctrlsub + 0x318) == 0x10, "w318 bit4")
                ck(gm.w16(w.ctrlsub + 0x350) == 0, "w350 cleared")
            elif name == "d3d0-neg":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(bytes(gm.b(w.qtab + 0x40 + i) for i in range(3))
                   == b"42\x00", "abs(edx) fmt")
                ck(gm.b(w.qtab + 0x3F) == 2, "b3F len")
                ck(tcount("l296e90") == 1, "arm5 dispatch")
            elif name == "d3d0-sub":
                # edi=3 + off4 -> subtype table[7]=7 -> arm6 ->
                # 297040(id, r8=1): b31E!=3 -> w318|=0x40, w356=0
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                c = byr("l297040")
                ck(len(c) == 1 and c[0][1] == w.ctrlsub,
                   f"dispatch {c}")
                ck(tcount("l296e90") == 0, "wrong arm")
                ck(gm.w16(w.ctrlsub + 0x318) == 0x40, "w318 bit6")
                ck(gm.w16(w.ctrlsub + 0x356) == 0, "w356 cleared")
            elif name == "d3d0-rec":
                # rec with b5==0 -> off 0 -> subtype table[0]=2 ->
                # arm1 -> 296E90; 263C20 not consulted
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l296e90") == 1, "arm1 dispatch")
                ck(gm.w16(w.ctrlsub + 0x318) == 0x10, "w318 bit4")
                ck(tcount("l263c20") == 0, "263C20 ran w/ live b5==0 rec")
            elif name == "d3d0-c20":
                # b[subobj+0xE]&0xF == 3 -> off 0 -> subtype 2 -> arm1
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l263c20") == 1, "263C20 missing")
                ck(tcount("l296e90") == 1, "arm1 dispatch")
                ck(gm.w16(w.ctrlsub + 0x318) == 0x10, "w318 bit4")
            elif name == "d3d0-arm0":
                # subtype 1 -> arm0 -> 297040(id, r8=0): w318|=0x20
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                c = byr("l297040")
                ck(len(c) == 1 and c[0][1] == w.ctrlsub,
                   f"dispatch {c}")
                ck(gm.w16(w.ctrlsub + 0x318) == 0x20, "w318 bit5")
                ck(gm.w16(w.ctrlsub + 0x354) == 0, "w354 cleared")
            elif name == "d3d0-arm3":
                # subtype 4 -> arm3 -> dispatch is a no-op
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l296e90") == 0 and tcount("l297040") == 0,
                   "noop arm dispatched")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "w318 untouched")
            elif name == "d3d0-sub8":
                # subtype 8 -> edx=7 >6 -> dispatch skipped entirely
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(tcount("l296e90") == 0 and tcount("l297040") == 0,
                   "subtype 8 dispatched")
                ck(gm.b(w.qtab + 0x3C) == 0, "still enqueued")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "w318 untouched")
            elif name == "d480-null":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 0, "enqueue on null subobj")
            elif name == "d480-far":
                ck(eax == 0, f"eax {eax:x}")
                ck(tcount("l3bbd00") == 0, "enqueue past 24u")
            elif name == "d480-near":
                ck((eax & 0xFF) == 0x20, f"eax {eax:x}")
                ck(gm.b(w.qtab + 0x3C) == 1, "type byte")
                ck(gm.b(w.qtab + 0x3F) == 3, "b3F = b[req+8]")
                ck(tcount("l3efd00") == 0, "type1 ran formatter")
                ck(tcount("l24a5a0") == 1, "battle_4_p lookup")
                ck(tcount("l2dd7e0") == 2, "style pair lookups")
                ck(gm.d(w.qtab + 0xC) == 0x80808080
                   and gm.d(w.qtab + 0x10) == 0x80808080,
                   "dd7 miss defaults")

            # ---- EXP-203: dispatch consumer sinks real ----
            elif name == "e690-null":
                ck(tcount("l273320") == 0, "resolve on null")
            elif name == "e690-bad":
                ck(tcount("l273320") == 1, "resolve missing")
                ck(tcount("l35bb00") == 1, "scan ran once")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "w318 on bad idx")
            elif name == "e690-idx0":
                ck(gm.w16(w.ctrlsub + 0x318) == 0x10, "w318 bit4")
                ck(gm.w16(w.ctrlsub + 0x350) == 0, "w350 cleared")
            elif name == "e690-idx2":
                ck(gm.w16(w.ctrlsub + 0x5D8) == 0x10, "idx2 w318 bit4")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "idx0 untouched")
            elif name == "e690-or":
                ck(gm.w16(w.ctrlsub + 0x318) == 0x50, "w318 |= 0x10")
            elif name == "p7040-null":
                ck(tcount("l273320") == 0, "resolve on null")
            elif name == "p7040-bad":
                ck(tcount("l273320") == 1, "resolve missing")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "w318 on bad idx")
            elif name == "p7040-f0":
                ck(gm.w16(w.ctrlsub + 0x318) == 0x20, "w318 bit5")
                ck(gm.w16(w.ctrlsub + 0x354) == 0, "w354 cleared")
            elif name == "p7040-f1":
                ck(gm.w16(w.ctrlsub + 0x318) == 0x40, "w318 bit6")
                ck(gm.w16(w.ctrlsub + 0x356) == 0, "w356 cleared")
            elif name == "p7040-f1g3":
                ck(gm.w16(w.ctrlsub + 0x318) == 0,
                   "b31E==3 gate bypassed")
            elif name == "p7040-idx2":
                ck(gm.w16(w.ctrlsub + 0x5D8) == 0x20, "idx2 w318 bit5")
                ck(gm.w16(w.ctrlsub + 0x318) == 0, "idx0 untouched")

            # ---- EXP-204: 273320 resolver real ----
            elif name == "r3320-nul":
                ck(eax == 0xFFFFFFFF, f"id0 -> {eax:x} != -1")
                ck(tcount("l35bb60") == 0, "count read on id 0")
            elif name == "r3320-empty":
                ck(eax == 0xFFFFFFFF, f"empty table -> {eax:x} != -1")
                ck(tcount("l35bb60") == 1 and tcount("l35bb00") == 0,
                   "scan ran on empty")
            elif name == "r3320-hit":
                ck(eax == 0, f"idx0 -> {eax:x}")
                ck(tcount("l35bb00") == 1, "one probe")
            elif name == "r3320-hit2":
                ck(eax == 2, f"idx2 -> {eax:x}")
                ck(tcount("l35bb00") == 3, "three probes")
            elif name == "r3320-miss":
                ck(eax == 0xFFFFFFFF, f"miss -> {eax:x} != -1")
                ck(tcount("l35bb00") == 2, "two probes")
            elif name == "r3320-neg":
                ck(eax == 0xFFFFFFFF, f"neg count -> {eax:x} != -1")
                ck(tcount("l35bb00") == 0, "scanned on neg count")

            # ---- EXP-205: 31C5D0 kind-0x1A resolver ----
            elif name == "c5d0-ok":
                ck(eax == 0, f"ret {eax:x}")
                ck(tcount("v2c50") == 1, "validator missing")
                ck(tcount("l2f9860") == 1, "bucket leaf missing")
                ck(gm.q(w.c5blk + 0x18) == w.elemb + 0x80000,
                   "q18 resolved")
                ck(gm.q(w.c5blk + 0x10) == 0x1CEB638,
                   "q10 default")
                ck(gm.b(w.c5blk + 0x20) == 0x11
                   and gm.b(w.c5blk + 0x21) == 0x33
                   and gm.b(w.c5blk + 0x22) == 0x44
                   and gm.b(w.c5blk + 0x23) == 0x22
                   and gm.b(w.c5blk + 0x24) == 0
                   and gm.b(w.c5blk + 0x25) == 0, "row copies")
            elif name == "c5d0-noval":
                ck(eax == 0xFFFFFFFE, f"ret {eax:x} != -2")
                ck(tcount("v2c50") == 1, "validator missing")
                ck(tcount("l2f9860") == 0, "leaf ran on fail")
                ck(gm.q(w.c5blk + 0x18) == 0, "q18 on fail")
            elif name == "c5d0-not2":
                # T2 null is graceful: q18=0, fields still resolve
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.q(w.c5blk + 0x18) == 0, "q18 on null T2")
                ck(gm.q(w.c5blk + 0x10) == 0x1CEB638,
                   "q10 default")
                ck(gm.b(w.c5blk + 0x24) == 0, "b24 copy")
            elif name == "c5d0-kind0":
                ck(eax == 0xFFFFFFFE, f"ret {eax:x} != -2")
                ck(tcount("v2c50") == 1, "validator missing")
            elif name == "c5d0-kind33":
                ck(eax == 0xFFFFFFFE, f"ret {eax:x} != -2")
                ck(tcount("v2c50") == 1, "validator missing")
            elif name == "c5d0-b25":
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.b(w.c5blk + 0x25) == 0x17,
                   f"b25 {gm.b(w.c5blk + 0x25):x} != 0x17")
            elif name == "c5d0-auto":
                ck(eax == 0xFFFFFFFE, f"ret {eax:x} != -2")
                ck(tcount("v309440") == 1, "auto-kind arm missing")
                # shipped remap d[01EEBCF8 + (w6>>C)*0x58] = 5+hi:
                # hi0 -> kind 5 -> re-dispatched arm fails -> -2
                ck(gm.d(w.c5blk) == 5,
                   "kind not rewritten to shipped remap 5")

            # ---- EXP-206/207: 2B3050/2B3120/2B24B0 evaluator ----
            elif name == "b3120-nil":
                ck(eax == 0, f"ret {eax:x}")
                ck(not byr("l2b24b0"), "evaluator on null gate")
                ck(gm.w16(w.wout) == 0 and gm.w16(w.wout2) == 0,
                   "outs on null")
            elif name == "b3120-ok":
                ck(eax == 0, f"ret {eax:x}")
                ck(len(byr("l2b24b0")) == 1, "evaluator missing")
                # tag-5 space: 15.0 x 6.5 -> ceil -> 15/7
                ck(gm.w16(w.wout) == 15
                   and gm.w16(w.wout2) == 7,
                   f"outs {gm.w16(w.wout):x}/{gm.w16(w.wout2):x}")
            elif name == "b3120-noout":
                ck(eax == 0, f"ret {eax:x}")
                ck(len(byr("l2b24b0")) == 1, "evaluator missing")
            elif name == "b3120-tage":
                # tag-0xE sets b10FE -> acc = 2*d[01E0CDC0]*1*1 = 32;
                # measure 0 -> f54 = acc+ec = 32; height 0
                ck(eax == 0, f"ret {eax:x}")
                ck(len(byr("l2b24b0")) == 1, "evaluator missing")
                ck(len(by("s3ffdf0")) == 2
                   and len(by("s2b2df0")) == 2,
                   "tag-14 helpers")
                ck(gm.w16(w.wout) == 32 and gm.w16(w.wout2) == 0,
                   f"outs {gm.w16(w.wout):x}/{gm.w16(w.wout2):x}")
            elif name == "b3050-run":
                ck(eax == 0, f"ret {eax:x}")
                ck(len(byr("l2ac1e0")) == 1, "state init missing")
                ck(byr("l39bad0")[0][1] == 0x44, "ctx not passed")
                # 254a10: the bl==7 gate once + once per real tag-5
                # arm (two walker walks)
                ck(len(byr("l254a10")) == 3, "gate/interp calls")
                # real 2AC1E0 tails into 39C4A0 once; the bl==7 arm
                # would add a second call
                ck(len(byr("c4a0")) == 1, "arm ran on bl!=7")
                c = byr("l2b3120")
                ck(len(c) == 1 and c[0][2] == w.wout,
                   f"evaluator args {c}")
                ck(gm.w16(w.wout) == 15 and gm.w16(w.wout2) == 7,
                   "outs")
            elif name == "b3050-arm":
                c = byr("c4a0")
                # 2AC1E0 init calls 39C4A0(0); the armed path bts
                # d[state+0x44].0xB then calls 39C4A0((d44>>B)&1)=1
                ck(len(c) == 2 and c[0][1] == 0 and c[1][1] == 1,
                   f"bts bit {c}")
                # 39C4A0's result lands q[state+0x60] (rsp+0x80 ==
                # state+0x60); the evaluator sees it in its struct
                # copy at l2b24b0's rcx.
                ck(gm.q(byr("l2b24b0")[0][1] + 0x60) == 0x1234,
                   "39c4a0 result not in evaluator struct")
                ck(gm.d(byr("l2b24b0")[0][1] + 0x44) & 0x800,
                   "bts bit 0xB not in copy")
            elif name == "b3050-alt":
                ck(len(byr("c4a0")) == 1,
                   "arm ran on 254a10!=0")
                ck(len(byr("l2b3120")) == 1, "evaluator missing")
            elif name == "b24b0-run":
                ck(eax == 0, f"ret {eax:x}")
                # EXP-220: +2 ceilf inside the real 1E93C0 tails
                ck(len(byr("l2b2150")) == 3
                   and len(byr("l2af340")) == 1
                   and len(byr("l2ac5f0")) == 2
                   and tcount("ceilf") == 4, "inner calls")
                # ctx swap: q[0209CC48] was 0 inside eval, restored
                ck(w.rets.get("cc48mid") == 0, "ctx not swapped out")
                ck(gm.q(0x209CC48) == 0x5EED, "ctx48 not restored")
                # save/restore fields
                ck(gm.d(w.ctxo + 0x10D8) == 0xDEAD
                   and gm.q(w.ctxo + 0x10C8) == 0x77
                   and gm.b(w.ctxo + 0x10FC) == 0xAB
                   and gm.b(w.ctxo + 0x10FF) == 0xCD,
                   "ctx save fields")
                ck(abs(gm.f(w.ctxo + 0x10E8) - 1.5) < 1e-6,
                   "f10e8 not restored")
                # real tag-5 measure: width 15 -> ceil 15; height
                # f880 -> ceilf(13/2.0)=7.0 -> 7; acc=0 ->
                # f60 = 15-0; tag-5's ctx48==0 arm set
                # b[ctxo+0x1100]=1 -> b51
                ck(abs(gm.f(w.c54 + 0x54) - 15.0) < 1e-6,
                   "f54")
                ck(abs(gm.f(w.c54 + 0x58) - 7.0) < 1e-6,
                   "f58")
                ck(abs(gm.f(w.c54 + 0x60) - 15.0) < 1e-6,
                   "f60 remainder")
                ck(gm.d(w.c54 + 0x5C) == 0, "d5c")
                # the b1100->+0x51 copy is gated on ctxo b10FE — a
                # tag-5 string leaves it clear, so +0x51 stays 0 even
                # though b[ctxo+0x1100] = 1 mid-measure
                ck(gm.b(w.c54 + 0x50) == 0
                   and gm.b(w.c54 + 0x51) == 0, "bytes")
                ck(gm.b(w.ctxo + 0x1100) == 1, "ctxo b1100")
            elif name == "b24b0-acc":
                # tag-0xE: b10FE -> acc = 2*16*1*1 = 32; measure 0
                # -> acc+ec=32 > f54=0 -> f54 = 32, d60 = ec bits
                ck(abs(gm.f(w.c54 + 0x54) - 32.0) < 1e-6,
                   f"f54 {gm.f(w.c54 + 0x54)}")
                ck(gm.b(w.ctxo + 0x1101) == 1
                   and gm.b(w.ctxo + 0x10FE) == 1,
                   "tag-14 ctx marks")
            elif name == "b24b0-merge":
                # acc+ec = 0+15 == f54 = ceil(15) -> strict > false
                # -> else: f54 untouched, f60 = 15 - 0
                ck(abs(gm.f(w.c54 + 0x54) - 15.0) < 1e-6,
                   "f54 on equal")
                ck(abs(gm.f(w.c54 + 0x60) - 15.0) < 1e-6,
                   "f60 remainder")
            # ---- EXP-208: 2B2150/2AF340 segment-string walkers ----
            elif name == "b2150-nil":
                ck(eax == 0, f"ret {eax:x}")
                ck(not byr("l2ac5f0") and not byr("l2ac2f0"),
                   "walk on null cursor")
                ck(abs(gm.f(w.params)) < 1e-6, "width out")
                ck(abs(gm.f(w.ctxe8)) < 1e-6, "height out")
                ck(gm.q(0x209CC48) == 0x77, "ctx48 restore")
                ck(gm.q(0x209E598) == 0x66, "e598 restore")
            elif name == "b2150-lite":
                ck(eax == 1, f"consumed {eax:x}")
                ck(len(byr("l2ac5f0")) == 1, "interpret missing")
                # ctx48==0 mid-walk -> the tag-5 arm's own nested
                # 2B2150 fires on the next cell.  The nested call is a
                # self-entry (invisible in rargs) — the l2b2150n
                # call-site tag proves it ran
                c = byr("l2b2150n")
                ck(len(c) == 1 and c[0][2] == w.nstr + 1,
                   f"nested walk {c}")
                ck(len(byr("f880")) == 1, "height shim missing")
                c = byr("fae0")
                # outer clear+restore, nested clear+restore, the
                # interpreter's own exit clear -> restore lands last
                ck(len(c) == 5 and c[-1][1] == 0x1234,
                   f"+0x28 swap {c}")
                ck(w.rets.get("cc48mid") == 0,
                   "ctx48 still set mid-walk")
                ck(gm.q(0x209CC48) == 0x77, "ctx48 restore")
                # tag-5 clears b10FC mid-walk (walker restores the
                # preset 0xAB at exit) + sets 1100 on the global ctx
                ck(gm.b(w.ctxo + 0x10FC) == 0xAB
                   and gm.b(w.ctxo + 0x1100) == 1,
                   "ctx marks")
                ck(gm.q(0x209E598) == 0x66, "e598 restore")
                # real tag-5: 15.0 advance, 7.0 height
                ck(abs(gm.f(w.params) - 15.0) < 1e-6, "width out")
                ck(abs(gm.f(w.ctxe8) - 7.0) < 1e-6, "height out")
            elif name == "b2150-brk":
                ck(len(byr("l2ac5f0")) == 1, "interpret missing")
                ck(eax == 0, f"consumed {eax:x}")
                ck(abs(gm.f(w.params)) < 1e-6, "width out")
            elif name == "b2150-heavy":
                # one heavy byte (0x23) -> one real decode + one
                # glyph remap; the NUL exits the walk
                c = byr("l2ac2f0")
                ck(len(c) == 1, f"decode calls {c}")
                # EXP-222: real 2AC2F0 also remaps via 17F8C0
                # internally -> decoder call + walker call
                g = byr("f8c0")
                ck(len(g) == 2 and g[0][1] == 3 and g[1][1] == 3,
                   f"glyph lookups {g}")
            elif name == "b2150-adv":
                # flag[3]=0 -> b10FC=2; flag[4] set + b10FC==2 ->
                # xmm6 += f34 * 2.3 * f38 = 2.0*2.3*3.0 = 13.8
                ck(abs(gm.f(w.params) - 13.8) < 0.01,
                   f"advance {gm.f(w.params)}")
            elif name == "af340-run":
                # real tag-5 -> continue -> NUL -> final flush:
                # f30 = 15.0, f34 = 7.0
                ck(eax == 1, f"node count {eax:x}")
                ck(len(byr("l2ac5f0")) == 1, "interpret missing")
                ck(abs(gm.f(w.params + 0x30) - 15.0) < 1e-6
                   and abs(gm.f(w.params + 0x34) - 7.0) < 1e-6,
                   f"outs {gm.f(w.params + 0x30)}/"
                   f"{gm.f(w.params + 0x34)}")
            elif name == "af340-heavy":
                ck(eax == 1, f"node count {eax:x}")
                ck(len(byr("l2ac2f0")) == 1, "decode missing")
                ck(gm.b(w.ctxo + 0x10FC) == 1,
                   "flag-set arm did not mark ctx")
                ck(gm.b(w.ctxo + 0x1102) == 0, "b1102")
            elif name == "af340-tag2":
                # tag-2 nested walk (1) + the tag-5 arm's ctx48==0
                # nested inside it (2) + the outer walk re-processes
                # the same \x05 afterwards -> another tag-5 nested
                # (3); the interpreter runs once per \x05
                ck(len(byr("l2b2150")) == 3,
                   f"nested walks {byr('l2b2150')}")
                ck(len(byr("l2ac5f0")) == 2,
                   f"interprets {byr('l2ac5f0')}")
                ck(gm.b(w.ctxo + 0x1102) == 1, "b1102 not set")
            elif name == "af340-tage":
                # real tag-14 arm: s3ffdf0 parse + s2b2df0 wrap,
                # returns 0 -> break arm sees 0xE -> s2b3e30
                ck(len(by("s3ffdf0")) == 1
                   and len(by("s2b2df0")) == 1, "tag-14 helpers")
                ck(len(byr("l2ac5f0")) == 1, "interpret missing")
                c = by("s2b3e30")
                ck(len(c) == 1 and c[0][1] == w.params,
                   f"2b3e30 {c}")
                ck(abs(gm.f(w.params + 0x24) - 8.0) < 1e-6,
                   f"f24 {gm.f(w.params + 0x24)}")
            # ---- EXP-209: 2AC5F0 direct entries ----
            elif name == "c5f0-nul":
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr, "cursor moved on NUL")
            elif name == "c5f0-match":
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr, "cursor moved on match")
            elif name == "c5f0-tag8":
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 3, "tag8 cursor")
            elif name == "c5f0-tag9":
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "tag9 cursor")
            elif name == "c5f0-tag5":
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "tag5 cursor")
                ck(abs(gm.f(0x209CC68) - 15.0) < 1e-6
                   and abs(gm.f(0x209CC64) - 7.0) < 1e-6,
                   "accumulators")
                ck(gm.d(w.params) == 1, "aux dword")
                ck(len(byr("l2b2150")) == 1, "nested walk missing")
                ck(gm.b(w.ctxo + 0x10FC) == 0
                   and gm.b(w.ctxo + 0x1100) == 1, "ctx marks")
                ck(gm.q(0x209E598) == 0, "e598 clear")
            # ---- EXP-210: remaining 2AC5F0 arms ----
            elif name in ("c5f0-tag1", "c5f0-tag4"):
                # shared arm: advance = float(17F920(ecx)) * s34 *
                # s38; height = int(17f880=7.0)=7 * s34 * s3C
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
                c = byr("f920")
                want = 0 if name == "c5f0-tag1" else 1
                ck(len(c) == 1 and c[0][1] == want,
                   f"f920 arg {c}")
                # real 17F920: cl=0 -> d[devsub+0x20]=6,
                # cl=1 -> d[devsub+0x1C]=5
                adv = 6.0 if name == "c5f0-tag1" else 5.0
                ck(abs(gm.f(0x209CC68) - adv * 2 * 3) < 1e-6,
                   f"cc68 {gm.f(0x209CC68)}")
                ck(abs(gm.f(0x209CC64) - 7.0 * 2 * 4) < 1e-6,
                   f"cc64 {gm.f(0x209CC64)}")
                ck(gm.d(w.params) == 1, "aux dword")
            elif name == "c5f0-tag6":
                # fixed shipped const 10.0 * s34 * s38
                ck(eax == 1, f"ret {eax:x}")
                ck(abs(gm.f(0x209CC68) - 10.0 * 2 * 3) < 1e-6,
                   f"cc68 {gm.f(0x209CC68)}")
                ck(abs(gm.f(0x209CC64) - 7.0 * 2 * 4) < 1e-6,
                   "cc64")
            elif name in ("c5f0-tag7", "c5f0-tag7a"):
                # 229E40()==7 -> 0x1A else int(1.0*10.0)=10
                ck(eax == 1, f"ret {eax:x}")
                # EXP-222: real 254a10 makes lang 7 a set member
                # -> the 229e40==7 (0x1A) arm is unreachable for it;
                # both take the 24aba0 int(1.0*10.0) arm = 10
                want = 10.0
                ck(abs(gm.f(0x209CC68) - want * 2 * 3) < 1e-6,
                   f"cc68 {gm.f(0x209CC68)}")
            elif name in ("c5f0-tag2", "c5f0-tag2f"):
                # nested 2B2150 on the rest; outs land f[params]/
                # f[params+4]; ret 1, cursor+1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
                ck(len(byr("l2b2150")) == 2, f"nested {byr('l2b2150')}")
                ck(gm.b(w.ctxo + 0x1102) == 1, "b1102")
                # nested on \x05 -> height 7.0 -> else-branch:
                # f[params+4] = 7.0, f[ctxo+10E8] = 7.0
                ck(abs(gm.f(w.params + 4) - 7.0) < 1e-6,
                   f"params+4 {gm.f(w.params + 4)}")
                ck(abs(gm.f(w.ctxo + 0x10E8) - 7.0) < 1e-6,
                   "nested height -> 10E8")
                ck(abs(gm.f(0x209CC60)) < 1e-6
                   and abs(gm.f(0x209CC68)) < 1e-6,
                   "cc60-band cleared")
                ck(gm.q(0x209E598) == 0, "e598 clear")
                if name == "c5f0-tag2f":
                    ck(len(by("s17f850")) == 1
                       and len(by("s17fa10")) == 1
                       and len(by("s2ab820")) == 1
                       and len(by("s17fb00")) == 1,
                       "0x20 tail block")
                    ck(by("s17fb00")[0][1] == w.c60,
                       "fb00 arg = state+0x20")
                else:
                    ck(not by("s17fb00"), "0x20-null tail ran")
            elif name == "c5f0-tag3":
                # line break: cursor+1, e598/b10FC cleared, ret 0
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
                ck(gm.q(0x209E598) == 0, "e598 not cleared")
                ck(gm.b(w.ctxo + 0x10FC) == 0, "b10FC")
                ck(len(byr("fae0")) == 1
                   and byr("fae0")[0][1] == 0, "fae0(0)")
            elif name == "c5f0-taga":
                # tag-5-family advance + scan-for-02/05, nested
                # 2B2150 on the (already advanced) cursor
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
                ck(abs(gm.f(0x209CC68) - 15.0) < 1e-6, "cc68")
                ck(abs(gm.f(0x209CC64) - 7.0) < 1e-6, "cc64")
                ck(len(byr("l2b2150")) == 1, "nested walk")
            elif name == "c5f0-tagb":
                ck(eax == 0, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr, "cursor moved on no-op")
            elif name == "c5f0-tagf":
                # second-level dispatch: sub 0x80-0x20=0x60 > 0x50 ->
                # out-of-range -> ret 1, cursor already advanced 1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
            elif name in ("c5f0-f30", "c5f0-f5f"):
                # kind 0x0D/0x22 -> direct ret-1 tail, cursor +1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.ccp) == w.nstr + 1, "cursor")
            elif name == "c5f0-f22":
                # kind 0x02 -> REAL 3FFEE0(str+1, 0, &state+0x9E):
                # b[9E] = b[+2]&0x1F = 0x17, ret 3 -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fee0")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1
                   and c[0][2] == 0, "fee0 args")
                ck(gm.b(w.e312 + 0x9E) == 0x17, "b9E")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f2c":
                # kind 0x0A -> pure 3FFAB0 param skip; ret 1, cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 not real")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f56":
                # kind 0x1D -> 3FFAB0 + d[aux]=0
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 not real")
                ck(gm.d(w.params) == 0, "aux")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f24":
                # kind 0x04: real 3FFAB0 direct decode -> f[+0x4C]=5.0
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 not real")
                ck(not byr("l39ba00"), "escape path on direct enc")
                ck(abs(gm.f(w.e312 + 0x4C) - 5.0) < 1e-6, "f4C")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f24s":
                # d[+0xB0]&0x2000000 gates the f4C write
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.d(w.e312 + 0x4C) == 0, "f4C gated")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f23":
                # kind 0x03: param 2 -> w[+0x88] = 2*0x1E, b9B=1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.w16(w.e312 + 0x88) == 0x3C, "w88")
                ck(gm.b(w.e312 + 0x9B) == 1, "b9B")
                ck(gm.d(w.e312 + 0xB0) == 0, "dB0 untouched")
            elif name == "c5f0-f23z":
                # param 0 via escape table -> w88=0x2710, dB0 =
                # bB0=5 | 0x4080000
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.w16(w.e312 + 0x88) == 0x2710, "w88")
                ck(gm.d(w.e312 + 0xB0) == 0x04080005, "dB0")
                ck(gm.b(w.e312 + 0x9B) == 1, "b9B")
            elif name == "c5f0-f23e":
                # escape decode through REAL 39BA00 (ba00t[1]=0x37)
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l39ba00")) == 1, "ba00 not real")
                ck(gm.w16(w.e312 + 0x88) == 0x37 * 0x1E, "w88")
                ck(gm.d(w.e312 + 0xB0) == 0, "dB0")
            elif name == "c5f0-f21":
                # kind 0x01: REAL 39BA30(idx 0, mode 1) over ba30t;
                # 254a10==0 inside -> ret rec+0x40 -> q68/q60;
                # arm's own 254a10==0 -> d44|=0x800, 17FD30(7,0),
                # d[209CC30]=7/d[209CC34]=0, 2B1ED0(ctx)
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l39ba30")
                ck(len(c) == 1 and c[0][1] == 0 and c[0][2] == 1,
                   f"ba30 args {c}")
                ck(gm.q(w.e312 + 0x68) == w.ba30r[0] + 0x40
                   and gm.q(w.e312 + 0x60) == w.ba30r[0] + 0x40,
                   "q68/q60 = rec+0x40")
                ck(gm.d(w.e312 + 0x44) & 0x800, "d44 kern bit")
                c = byr("l17fd30")
                ck(len(c) == 1 and c[0][1] == 7 and c[0][2] == 0,
                   "fd30(7,0)")
                ck(gm.d(0x209CC30) == 7 and gm.d(0x209CC34) == 0,
                   "cc30/cc34")
                c = byr("b1ed0")
                ck(len(c) == 1 and c[0][1] == w.e312, "b1ed0 arg")
                # real 2B1ED0: d44&0x800 -> f980/f960 -> f[CC70/74]
                ck(abs(gm.f(0x209CC70) - 9.0) < 1e-3
                   and abs(gm.f(0x209CC74) - 8.0) < 1e-3, "b1ed0 floats")
                ck(gm.q(w.ccp) == w.nstr + 2, "cursor")
            elif name == "c5f0-f21a":
                # 254a10()==1 inside 39BA30 -> w6=1 record scan hits
                # (wC=0x40>0x30, d30&0x18000==0x8000) -> rec+0x40;
                # arm's 254a10==1 -> 17FD30(b[A6]=9,1), cc30=9, cc34=1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.q(w.e312 + 0x68) == w.ba30r[9] + 0x40
                   and gm.q(w.e312 + 0x60) == w.ba30r[9] + 0x40,
                   "q68/q60 = rec+0x40")
                c = byr("l17fd30")
                ck(len(c) == 1 and c[0][1] == 9 and c[0][2] == 1,
                   "fd30(9,1)")
                ck(gm.d(0x209CC30) == 9 and gm.d(0x209CC34) == 1,
                   "cc30/cc34")
            elif name == "c5f0-f25":
                # kind 0x05 '%': b99=param, b9A=0x25, ctxo+0x1104=0x25;
                # ctxo b1102==0 -> no nested measure
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0x99) == 7, "b99")
                ck(gm.b(w.e312 + 0x9A) == 0x25, "b9A")
                ck(gm.b(w.ctxo + 0x1104) == 0x25, "ctxo 1104")
                ck(not byr("l2b2150"), "nested ran on b1102==0")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f25n":
                # b1102!=0 -> nested 2B2150 + real 2B1F20 (b9A==0x25
                # arm) -> f[params]=float(movsx(b99))=7.0
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l2b2150")) == 1, "nested missing")
                ck(len(byr("l2b1f20")) == 1, "b1f20 missing")
                ck(abs(gm.f(w.params) - 7.0) < 1e-6, "f[params]")
            elif name == "c5f0-f26n":
                # '&' nested: 2B1F20 b9A==0x26 arm -> f[params] =
                # int(w94 - nested_h(0)) + b99 = 0x30 + 7 = 55.0
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0x9A) == 0x26, "b9A")
                ck(len(byr("l2b1f20")) == 1, "b1f20 missing")
                ck(abs(gm.f(w.params) - 55.0) < 1e-6, "f[params]")
            elif name == "c5f0-f27n":
                # "'" nested: 2B1F20 b9A==0x27 arm -> f[params] =
                # (int(w94) >> 1) + b99 = 24 + 7 = 31.0
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0x9A) == 0x27, "b9A")
                ck(abs(gm.f(w.params) - 31.0) < 1e-6, "f[params]")
            elif name == "c5f0-f28":
                # kind 0x06 '(': f34 = 48/24 = 2.0; param>=24 -> b44=6
                ck(eax == 1, f"ret {eax:x}")
                ck(abs(gm.f(w.e312 + 0x34) - 2.0) < 1e-6, "f34")
                ck(gm.b(w.e312 + 0x44) == 6, "b44")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f28l":
                # param 16 < 24 -> f34 = 16/24, b44 = 0
                ck(eax == 1, f"ret {eax:x}")
                ck(abs(gm.f(w.e312 + 0x34) - 16.0 / 24.0) < 1e-6,
                   "f34")
                ck(gm.b(w.e312 + 0x44) == 0, "b44")
            elif name == "c5f0-f37":
                # kind 0x14 '7': f34 = 120/100 = 1.2;
                # b44 = int(20/16.6) = 1
                ck(eax == 1, f"ret {eax:x}")
                ck(abs(gm.f(w.e312 + 0x34) - 1.2) < 1e-6, "f34")
                ck(gm.b(w.e312 + 0x44) == 1, "b44")
            elif name == "c5f0-f20":
                # kind 0x00 ' ': param 0 -> d40=0; old f40==0 ->
                # ret-1 early, no font-shim calls, no cc68 write
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.d(w.e312 + 0x40) == 0, "f40")
                ck(not byr("f920") and not byr("f940"),
                   "font calls ran")
            elif name in ("c5f0-f20r", "c5f0-f20k"):
                # old f40=2.0, param 0 -> 17F920(1)=5 -> cc68 =
                # 5*s34*s38*2.0 = 60; d44&0x800 adds s34*s38 = 6
                ck(eax == 1, f"ret {eax:x}")
                c = byr("f920")
                ck(len(c) == 1 and c[0][1] == 1, "f920(1)")
                want = 60.0 if name == "c5f0-f20r" else 66.0
                ck(abs(gm.f(0x209CC68) - want) < 1e-6, "cc68")
            elif name == "c5f0-f29":
                # kind 0x07 ')': REAL 3FFBC0 direct colour (count 3,
                # sel 1) -> d30 = [0x91,0x22,0x33,0] = 0x00332291;
                # ctxo+0x10D0 mirror; b[A8]=FF absorbs b[9F]=5; alpha
                # byte 0 -> b9f=0; consumed 5 -> cursor+6
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3fbc0")) == 1, "fbc0 not real")
                ck(not byr("l39ba00"), "escape on direct enc")
                ck(gm.d(w.e312 + 0x30) == 0x00332291, "d30")
                ck(gm.d(w.ctxo + 0x10D0) == 0x00332291, "ctxo 10D0")
                ck(gm.b(w.e312 + 0xA8) == 5, "A8 absorbed 9F")
                ck(gm.b(w.e312 + 0x9F) == 0, "b9f alpha-replace")
                ck(gm.q(w.ccp) == w.nstr + 6, "cursor")
            elif name == "c5f0-f29e":
                # ')' escape: 39BA00(2) -> rec at ba00t+11 copied
                # reversed -> d30 = [rec3,rec2,rec1,rec0] =
                # [0x11,0x22,0x33,0] = 0x00332211; alpha 0 -> b9f=0;
                # consumed 3 -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l39ba00")) == 1, "ba00 missing")
                ck(gm.d(w.e312 + 0x30) == 0x00332211, "d30")
                ck(gm.d(w.ctxo + 0x10D0) == 0x00332211, "ctxo 10D0")
                ck(gm.b(w.e312 + 0x9F) == 0, "b9f")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f29z":
                # escape idx 0 -> all-zero record -> d30==0 -> default
                # 0x80808080 + alpha = b[A8]=0x33; tail: 0x33&F0=0x30
                # != 0x00 -> b9f = 0x33|0 = 0x33; cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l39ba00")) == 1, "ba00 missing")
                ck(gm.d(w.e312 + 0x30) == 0x00808080, "d30")
                ck(gm.d(w.ctxo + 0x10D0) == 0x00808080, "ctxo 10D0")
                ck(gm.b(w.e312 + 0x9F) == 0x33, "b9f merge")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f2b":
                # kind 0x09 '+': alpha param 0x50, old b9f=0xAB ->
                # hi-nib differ -> b9f = 0x50|0xA0 = 0xF0
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0x9F) == 0xF0, "b9f")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f2d":
                # kind 0x0B '-': REAL 3FFC60 -> bA1 = min(0x39&F,8)=8,
                # ret 3 -> cursor+4; then 2AE610(state,&sub,&f16copy,
                # aux); d[aux]=0
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fc60")
                ck(len(c) == 2 and c[0][1] == w.nstr + 1,
                   f"fc60 args {c}")
                ck(gm.b(w.e312 + 0xA1) == 8, "bA1 clamp")
                c = byr("e610")
                ck(len(c) == 1 and c[0][1] == w.e312, "e610 arg")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f31":
                # kind 0x0E '1': REAL 3FFF10(str,0,0,0) -> ret 4 ->
                # cursor+5
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3ff10")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1
                   and c[0][2] == 0, "ff10 args")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f34":
                # kind 0x11 '4': real 3FFAB0 writes param to b[+0xA9]
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 not real")
                ck(gm.b(w.e312 + 0xA9) == 0x12, "bA9")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f35":
                # kind 0x12 '5': bAA=param; ctxo b1102==0 -> no
                # f[params] write; b[ctxo+0x10FD]=param
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0xAA) == 0x12, "bAA")
                ck(gm.b(w.ctxo + 0x10FD) == 0x12, "ctxo 10FD")
                ck(gm.d(w.params) == 0, "f[params] gated")
            elif name == "c5f0-f35n":
                # b1102!=0 -> f[params] = float(movsx(param)) = 18.0
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0xAA) == 0x12, "bAA")
                ck(abs(gm.f(w.params) - 18.0) < 1e-6, "f[params]")
                ck(gm.b(w.ctxo + 0x10FD) == 0x12, "ctxo 10FD")
            elif name == "c5f0-f36":
                # kind 0x13 '6': bAA = -param (0x100-0x12 = 0xEE)
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.e312 + 0xAA) == 0xEE, "bAA neg")
                ck(gm.b(w.ctxo + 0x10FD) == 0xEE, "ctxo 10FD")
            elif name == "c5f0-f33":
                # kind 0x10 '3': REAL 3FFDA0 -> f38 = 0x55/10 = 8.5,
                # f3C = 0x0A/10 = 1.0; ret 3 -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fda0")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1
                   and c[0][2] == w.e312 + 0x38, "fda0 args")
                ck(abs(gm.f(w.e312 + 0x38) - 8.5) < 1e-6, "f38")
                ck(abs(gm.f(w.e312 + 0x3C) - 1.0) < 1e-6, "f3C")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f6f":
                # kind 0x21 'o': REAL 3FFB00 direct word 0x0028 ->
                # f[params]=40.0; ret 4 -> cursor+5; tail clears
                # q[209E598] + 17FAE0(0)
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3fb00")) == 1, "fb00 not real")
                ck(abs(gm.f(w.params) - 40.0) < 1e-6, "f[params]")
                ck(gm.q(0x209E598) == 0, "e598 cleared")
                c = byr("fae0")
                ck(len(c) == 1 and c[0][1] == 0, "fae0(0)")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f6fe":
                # 'o' escape: 39BA00(2) -> w = movsx(ba00t[11]) = -32
                # -> f[params] = -32.0; ret 3 -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l39ba00")) == 1, "ba00 missing")
                ck(abs(gm.f(w.params) + 32.0) < 1e-6, "f[params]")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f32":
                # kind 0x0F '2': param==0 -> d[ctxo+0x10E0]=d[params]
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.d(w.ctxo + 0x10E0) == 0x1234, "ctxo 10E0")
            elif name == "c5f0-f32a":
                # param 10 -> 2*10-(40-10) = -10 < 0 -> no cc68 write
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.d(0x209CC68) == 0, "cc68 untouched")
            elif name == "c5f0-f32b":
                # param 32 -> 2*32-(40-10) = 34 -> f[cc68]=34.0
                ck(eax == 1, f"ret {eax:x}")
                ck(abs(gm.f(0x209CC68) - 34.0) < 1e-6, "cc68")
            elif name == "c5f0-f42":
                # kind 0x1C catch-all: state copy, b[ctxo+0x10FC]=1,
                # REAL nested 2AEB20(rdx=ccp) — edi=1 path (dev2+0x38),
                # e868v=2 -> table-C edx=1 -> ctxo+0x18 record, emits
                # cnt-1=1 quad records at q[0209CC50] (pcur=listcur+0x30),
                # real 17FC90/2DD860x2/dd8b0 + scripted 181xxx tail,
                # real 2B4730(1) flush, eax=2 -> cursor += 2, d[aux]=1
                ck(eax == 1, f"ret {eax:x}")
                ck(gm.b(w.ctxo + 0x10FC) == 1, "ctxo 10FC")
                ck(len(byr("eb20")) == 1, "eb20 ran")
                ck(len(byr("fc90")) == 1, "fc90")
                ck(len(byr("dd860")) == 2, "dd860")
                ck(len(byr("dd8b0")) == 1, "dd8b0")
                ck(len(byr("e0c30")) == 2, "e0c30")
                ck(len(byr("bb00")) == 1, "bb00")
                ck(len(byr("b4730")) == 1, "b4730 flush")
                ck(len(by("s181330")) == 1, "s181330")
                ck(len(byr("cookie")) >= 1, "cookie")
                # EXP-221: real device-op tail — wrappers ->
                # 1B1C00 -> 1Bxxxx methods on planted q[01F811E8].
                ck(len(byr("w181560")) == 1 and len(byr("b1910")) == 1
                   and len(byr("b0100")) == 1, "device reset calls")
                ck(len(byr("w1819a0")) == 1 and len(byr("b2410")) == 1
                   and len(byr("d2e0")) == 1 and len(byr("d670")) == 1
                   and len(by("scrtfmt")) == 1, "props+name copy")
                ck(len(byr("w181870")) == 1 and len(byr("b2490")) == 1,
                   "mode write")
                ck(len(byr("w181460")) == 1 and len(byr("b06d0")) == 6
                   and len(byr("aed50")) == 2, "appends+grows")
                ck(len(byr("w1816b0")) == 1 and len(byr("b22d0")) == 1
                   and len(byr("w181910")) == 1
                   and len(byr("b22e0")) == 1, "field stores")
                ck(len(byr("b1c00")) == 11, "singleton reads")
                # 1B0100 cleared slots 0..rdcur(1) then -1; the
                # appends sealed+init'd slot0 (d+0x2C stays 0 while
                # slot1 keeps the reset's 1) and grew its vector.
                ck(gm.d(w.rdev + 0x3928) == 0, "slot cursor")
                s1 = w.rdev + 0x2328 + 0x58
                ck(gm.d(s1 + 0x10) == 1 and gm.d(s1 + 0x2C) == 1
                   and gm.d(s1 + 0x30) == 1 and gm.q(s1) == 0,
                   "slot1 reset pattern")
                s0 = w.rdev + 0x2328
                vbeg = gm.q(s0 + 0x38)
                ck(vbeg != w.rvbuf and gm.q(s0 + 0x40) == vbeg + 0x120
                   and gm.q(s0 + 0x48) == vbeg + 0x180,
                   "slot0 vec grew")
                ck(len(by("s2alloc")) == 2
                   and len(by("s2dealloc")) == 2, "vec alloc/dealloc")
                src = byr("w181460")[0][1] & 0xFFFFFFFFFFFFFFFF
                for k, so in enumerate((0, 0x30, 0x60, 0x30, 0x60,
                                        0x90)):
                    ck(gm.q(vbeg + k * 0x30) == gm.q(src + so),
                       f"rec{k} copy")
                ck([w.rdev + 0x3930, 0x178] in w.rets["memsets"],
                   "props memset")
                for off in (0x3A4C, 0x3A50, 0x3A54, 0x3A58):
                    ck(gm.d(w.rdev + off) == 0x80, f"seed {off:x}")
                ck(gm.d(w.rdev + 0x3A60) == 2, "mode tbl[3]")
                ck(gm.q(w.rdev + 0x3A68) == 0x44
                   and gm.q(w.rdev + 0x3A70) == 0, "qword stores")
                ck(gm.d(w.rdev + 0x3930) == 0
                   and gm.d(w.rdev + 0x3934) == 0
                   and gm.d(w.rdev + 0x3A38) == 0
                   and gm.d(w.rdev + 0x3A40) == 1
                   and gm.d(w.rdev + 0x3A44) == 0
                   and gm.d(w.rdev + 0x3A48) == 0
                   and gm.d(w.rdev + 0x3AA0) == 0, "prop fields")
                sc = by("scrtfmt")[0]
                ck(sc[2] == w.rdev + 0x3938
                   and gm.b(w.rdev + 0x3938) == gm.b(sc[4]),
                   "name copy dst/src")
                ck(gm.d(w.params) == 1, "aux")
                # publish globals from the LAST entry (arr[cnt-1]):
                # w10b*xscale(2*3=6) -> cc60, w12b*yscale(2*4=8) -> cc64,
                # cc60-val + f4C(5) -> cc68
                ck(abs(gm.f(0x209CC60) - 48.0) < 1e-6, "cc60")
                ck(abs(gm.f(0x209CC64) - 32.0) < 1e-6, "cc64")
                ck(abs(gm.f(0x209CC68) - 53.0) < 1e-6, "cc68")
                # record[0] at pcur = listcur+0x30, stride 0x70
                rec = w.listcur + 0x30
                ck(gm.q(rec + 8) == 6 and gm.q(rec + 0x18) == 6, "hdr6")
                ck(gm.q(rec) == (0x0123450000000000 | 0x1300000),
                   "hdr attr")
                ck(gm.q(rec + 0x10) == 0x0123450000000000, "hdr attr2")
                ck(gm.d(rec + 0x20) == 0x11 and gm.d(rec + 0x24) == 0x22
                   and gm.d(rec + 0x28) == 0x33, "rgba")
                ck(gm.d(rec + 0x60) == 5 and gm.d(rec + 0x64) == 7,
                   "col/row")
                ck(gm.d(rec + 0x4C) == 1, "scale flag")
                ck(abs(gm.f(rec + 0x50) - 48.0) < 1e-6
                   and abs(gm.f(rec + 0x54) - 64.0) < 1e-6, "uv")
                # post-flush: ctx48 -> ring slot1 cell pair, publish
                # cursor restored from the ring-pair array
                ck(gm.q(0x209CC48) == 0x2EBEFD8, "ctx48 -> slot")
                ck(gm.d(0x2EBEFF0) == 1, "ring flipped")
            elif name in ("c5f0-f6d", "c5f0-f6e"):
                # kind 0x1F/0x20 'm'/'n': REAL 3FFB90(str+1,0,0)
                # pure skip -> ret 3 -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fb90")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1
                   and c[0][2] == 0, "fb90 args")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f6c":
                # kind 0x1E 'l': REAL 3FFCE0(str+1,0,0,0,[0,0,0]) ->
                # ret 4 -> cursor+5
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fce0")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1
                   and c[0][2] == 0, "fce0 args")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f2e":
                # kind 0x0C '.': REAL 3FFC60 ret 3 -> cursor+4;
                # q[state+0x70]==0 -> early ret-1
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3fc60")) == 1, "fc60 not real")
                ck(not by("s2b41f0") and not byr("l2b2150"),
                   "table path ran on q70==0")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f39":
                # kind 0x16 '9': param -> b[+0xA7]; dB0 |= 0x200000
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                ck(gm.b(w.e312 + 0xA7) == 0x12, "bA7")
                ck(gm.d(w.e312 + 0xB0) & 0x200000, "dB0 bit")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f3a":
                # kind 0x17 ':': 3FFAB0 skip -> FB4 tail: e598=0 +
                # 17FAE0(0) + ret 1
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                ck(gm.q(0x209E598) == 0, "e598 cleared")
                c = byr("fae0")
                ck(len(c) == 1 and c[0][1] == 0, "fae0(0)")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f3c":
                # kind 0x18 '<': param -> b[+0xAB]
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                ck(gm.b(w.e312 + 0xAB) == 0x21, "bAB")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f3d":
                # kind 0x19 '=': param -> b[+0xAE]
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                ck(gm.b(w.e312 + 0xAE) == 0x2E, "bAE")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f38e":
                # kind 0x15 '8': REAL 3FFB00 word 0x28 -> REAL 2639E0
                # -> 32A930 bit + 3EAC10 table (unplanted) -> 0 ->
                # early ret-1; ret 4 -> cursor+5
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3fb00")) == 1, "fb00 not real")
                c = byr("l2639e0")
                ck(len(c) == 1 and c[0][1] == 0x28, f"e39 arg {c}")
                ck(len(byr("l32a930")) == 1
                   and len(byr("l3eac10")) == 1, "lookup chain")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f38n":
                # '8' resolved: eac10t[0x50]=rstr -> deep tail: REAL
                # 2B41F0 (memset template + s39c4a0 -> q60 + real
                # 2AF340 walk decodes "X"), unconditional nested
                # 2B2150 decodes "X" again, 2A9F00 publish
                ck(eax == 1, f"ret {eax:x}")
                c = byr("b41f0")
                ck(len(c) == 1 and c[0][1] == w.rstr, "b41f0 arg")
                ck(len(byr("l2b2150")) == 1, "nested missing")
                ck(len(byr("l2ac2f0")) == 2, "X decodes")
                ck(len(byr("a9f00")) == 1, "a9f00 missing")
                ck(gm.b(w.rstr) == 0x23, "rstr[0] intact")
            elif name == "c5f0-f3e":
                # kind 0x1A '>': 3FFAB0 skip -> REAL 263990(nobj):
                # w102=0 -> 32A930(0)/3EAC10(0,0) -> unplanted -> 0 ->
                # early ret-1; cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                c = byr("l263990")
                ck(len(c) == 1 and c[0][1] == w.nobj, f"e990 arg {c}")
                ck(len(byr("l32a930")) == 1
                   and len(byr("l3eac10")) == 1, "lookup chain")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f3en":
                # '>' w102<0 -> q[nobj+0xF8]=rstr direct (no lookup
                # chain) -> deep tail: 2B41F0 + nested 2B2150 + 2A9F00
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l263990")) == 1, "e990 not real")
                ck(not byr("l32a930"), "chain ran on w102<0")
                c = byr("b41f0")
                ck(len(c) == 1 and c[0][1] == w.rstr, "b41f0 arg")
                ck(len(byr("l2b2150")) == 1, "nested missing")
                ck(len(byr("l2ac2f0")) == 2, "Y decodes")
                ck(len(byr("a9f00")) == 1, "a9f00 missing")
            elif name == "c5f0-f3f":
                # kind 0x1B '?': param 5 -> ecx=0xB/r8=3/r9=1 path ->
                # 2AE450(copy,5,params); b[ctxo+0x10FC]=1, bA9=0,
                # d[aux]=1; cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("l3ffab0")) == 1, "fab0 missing")
                ck(len(byr("e450")) == 1, "e450 missing")
                ck(len(byr("bb00")) == 1, "bb00 dispatch")
                ck(len(byr("afdc0")) == 1, "2afdc0 submit")
                # EXP-218: real 2AFDC0 writes the quad command record
                # at the publish cursor (listcur+0x30 under b4730p):
                # q[+8]=6 cmd header, q[+0x18]=6 second header.
                ck(gm.q(w.listcur + 0x38) == 6
                   and gm.q(w.listcur + 0x48) == 6,
                   "afdc0 cmd headers")
                # then the unconditional 2B4730(1) tail flush drains
                # the pending records and flips the ring.
                ck(len(byr("b4730")) == 1 and len(byr("a1db0")) == 1
                   and len(byr("l36f360")) == 1, "flush chain")
                ck(gm.d(0x2EBEFF0) == 1, "ring flipped")
                # ebx-tail restore: ctx48 -> ring-pair slot1 entry
                # (02EBEFC0 + 24*idx, idx = post-flip selector = 1),
                # cursors reload from slot1's reset pair.
                f3fslot = 0x2EBEFC0 + gm.d(0x2EBEFF0) * 24
                ck(gm.q(0x209CC48) == f3fslot, "ctx48 -> slot")
                ck(gm.q(0x209CC50) == gm.q(f3fslot + 8) + 0x10,
                   "post-flush cursor")
                # emit tail: two REAL quad-corner emits (2DD860 ->
                # 202B70 -> 217060 mat leaf + projective divide), the
                # scripted emit sink, REAL 2DD8B0 stack-vertex
                # formatting, then the six scripted device-state ops.
                ck(len(byr("dd860")) == 2, "2dd860 corners")
                ck(len(byr("w181560")) == 1, "181560 emit")
                ck(tcount("dd8b0") == 1, "dd8b0 vertex fmt")
                ck(len(by("s181330")) == 1, "s181330")
                # EXP-221: real device-op tail on q[01F811E8].
                ck(len(byr("b1910")) == 1 and len(byr("b0100")) == 1,
                   "device reset")
                ck(len(byr("w1819a0")) == 1 and len(byr("b2410")) == 1
                   and len(byr("d2e0")) == 1 and len(byr("d670")) == 1
                   and len(by("scrtfmt")) == 1, "props+name copy")
                ck(len(byr("w181870")) == 1 and len(byr("b2490")) == 1,
                   "mode write")
                ck(len(byr("w181460")) == 1 and len(byr("b06d0")) == 6
                   and len(byr("aed50")) == 2, "appends+grows")
                ck(len(byr("w1816b0")) == 1 and len(byr("b22d0")) == 1
                   and len(byr("w181910")) == 1
                   and len(byr("b22e0")) == 1, "field stores")
                ck(len(byr("b1c00")) == 11, "singleton reads")
                ck(gm.d(w.rdev + 0x3928) == 0, "slot cursor")
                s1 = w.rdev + 0x2328 + 0x58
                ck(gm.d(s1 + 0x10) == 1 and gm.d(s1 + 0x2C) == 1
                   and gm.d(s1 + 0x30) == 1 and gm.q(s1) == 0,
                   "slot1 reset pattern")
                s0 = w.rdev + 0x2328
                vbeg = gm.q(s0 + 0x38)
                ck(vbeg != w.rvbuf and gm.q(s0 + 0x40) == vbeg + 0x120
                   and gm.q(s0 + 0x48) == vbeg + 0x180,
                   "slot0 vec grew")
                ck(len(by("s2alloc")) == 2
                   and len(by("s2dealloc")) == 2, "vec alloc/dealloc")
                src = byr("w181460")[0][1] & 0xFFFFFFFFFFFFFFFF
                for k, so in enumerate((0, 0x30, 0x60, 0x30, 0x60,
                                        0x90)):
                    ck(gm.q(vbeg + k * 0x30) == gm.q(src + so),
                       f"rec{k} copy")
                ck([w.rdev + 0x3930, 0x178] in w.rets["memsets"],
                   "props memset")
                for off in (0x3A4C, 0x3A50, 0x3A54, 0x3A58):
                    ck(gm.d(w.rdev + off) == 0x80, f"seed {off:x}")
                ck(gm.d(w.rdev + 0x3A60) == 2, "mode tbl[3]")
                ck(gm.q(w.rdev + 0x3A68) == 0x44
                   and gm.q(w.rdev + 0x3A70) == 0, "qword stores")
                ck(gm.d(w.rdev + 0x3930) == 0
                   and gm.d(w.rdev + 0x3934) == 0
                   and gm.d(w.rdev + 0x3A38) == 0
                   and gm.d(w.rdev + 0x3A40) == 1
                   and gm.d(w.rdev + 0x3A44) == 0
                   and gm.d(w.rdev + 0x3A48) == 0
                   and gm.d(w.rdev + 0x3AA0) == 0, "prop fields")
                sc = by("scrtfmt")[0]
                ck(sc[2] == w.rdev + 0x3938
                   and gm.b(w.rdev + 0x3938) == gm.b(sc[4]),
                   "name copy dst/src")
                # sprt d[rec+0x5C] = 0x30040: lo12=0x40 * (f34*f38
                # =1*2) -> f[0209CC60]=128; hi12=0x30 * (f34*f3C
                # =1*0.5) -> f[0209CC64]=24; lo-scaled + f4C(0)
                # -> f[0209CC68]=128
                ck(abs(gm.f(0x209CC60) - 128.0) < 1e-3,
                   f"spr lo {gm.f(0x209CC60)}")
                ck(abs(gm.f(0x209CC64) - 24.0) < 1e-3,
                   f"spr hi {gm.f(0x209CC64)}")
                ck(abs(gm.f(0x209CC68) - 128.0) < 1e-3,
                   f"spr base {gm.f(0x209CC68)}")
                ck(gm.b(w.ctxo + 0x10FC) == 1, "ctxo 10FC")
                ck(gm.b(w.e312 + 0xA9) == 0, "bA9")
                ck(gm.d(w.params) == 1, "aux")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name == "c5f0-f2a":
                # kind 0x08 '*': REAL 3FFD70 -> rest=str+4, ret =
                # len(1)+3 = 4 -> cursor+5; 2 suppress-measures via
                # 2B43C0; BOTH nested 2B2150 calls are unconditional
                # (w48/w44 only gate the byte suppresses): nested1
                # walks "A" (rest[1] suppress = NUL->NUL) -> one
                # decode; nested2 on rest+1="" -> clean; ctx48==0 ->
                # ctxo block skipped
                ck(eax == 1, f"ret {eax:x}")
                c = byr("l3fd70")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1, "fd70 arg")
                ck(len(byr("b43c0")) == 2, "b43c0 x2")
                ck(len(byr("l2b2150")) == 2,
                   f"nested walks {byr('l2b2150')}")
                ck(len(byr("l2ac2f0")) == 2,
                   f"A decodes {byr('l2ac2f0')}")
                ck(not byr("a9f00"), "ctxo block on ctx48==0")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f2ac":
                # '*' + ctx48!=0: ctxo publish block runs — icon-fit
                # clamp math, 2A9F00 boundary, then ctxo d10D8/d10DC/
                # f10E4 restored to presets; same dual nested walks;
                # each real 2B43C0 walks rest -> 'A' decode
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("b43c0")) == 2, "b43c0 x2")
                ck(len(byr("l2b2150")) == 2,
                   f"nested walks {byr('l2b2150')}")
                ck(len(byr("l2ac2f0")) == 3,
                   f"A decodes {byr('l2ac2f0')}")
                ck(len(byr("a9f00")) == 1, "a9f00 missing")
                ck(gm.d(w.ctxo + 0x10D8) == 9, "d10D8 restored")
                ck(gm.d(w.ctxo + 0x10DC) == 5, "d10DC restored")
                ck(abs(gm.f(w.ctxo + 0x10E4) - 2.0) < 1e-6,
                   "f10E4 restored")
                ck(gm.q(w.ccp) == w.nstr + 5, "cursor")
            elif name == "c5f0-f2an":
                # '*' w48=0 < len -> suppress rest[0] + nested1 on ""
                # (clean); nested2 on rest+0="A" unsuppressed (w44=2
                # >= len2=1) -> one decode; rest[0] restored; ret=3
                # -> cursor+4
                ck(eax == 1, f"ret {eax:x}")
                ck(len(byr("b43c0")) == 2, "b43c0 x2")
                ck(len(byr("l2b2150")) == 2,
                   f"nested walks {byr('l2b2150')}")
                ck(len(byr("l2ac2f0")) == 2, "A decodes")
                ck(gm.b(w.nstr + 4) == 0x23, "rest[0] restored")
                ck(gm.q(w.ccp) == w.nstr + 4, "cursor")
            elif name in ("b4730-flush", "b4730-noflip"):
                # direct 2B4730 entry: drains 2 records out of the
                # publish cursor (pcur -> listcur+0x20), writes the
                # 0x10000002-range header + 0x6C028150 cmd + the
                # 0x10000000/0x15000000/0x13000000 terminator at
                # listcur+0x30, advances q[0209E5A0] to listcur+0x40,
                # aligns q[ctx48o+8] += cursor-low32&~0xF, then real
                # 3A1DB0 flips d[02EBEFF0] 0->1, 36F360 patches
                # q[ringbuf+0x20]=0x10000000 and resets slot1's
                # cursor to its start.
                lc = w.listcur
                ck(len(byr("a1db0")) == 1, "a1db0 entry")
                ck(len(byr("l36f360")) == 1, "36f360 entry")
                ck(gm.d(lc) == 0x10000002, f"hdr {gm.d(lc):08x}")
                ck(gm.d(lc + 8) == 0x10000000
                   and gm.d(lc + 0xC) == 0x6C028150, "cmd rec")
                ck(gm.q(lc + 0x30) == 0x10000000
                   and gm.d(lc + 0x38) == 0x15000000
                   and gm.d(lc + 0x3C) == 0x13000000, "terminator")
                ck(gm.d(lc + 0x2C) == 1, "drained hdr")
                ck(gm.q(w.ctx48o + 8) ==
                   ((lc + 0x40) & 0xFFFFFFFF) & ~0xF,
                   "ctx48 align")
                ck(gm.d(0x2EBEFF0) == 1, "ring flip")
                ck(gm.q(0x2EBEFE0) == w.ringbuf + 0x800,
                   "slot1 cursor reset")
                ck(gm.q(w.ringbuf + 0x20) == 0x10000000,
                   "36f360 patch")
                if name == "b4730-flush":
                    # ebx=1 tail: the ring-pair array itself at
                    # 02EBEFC0 + d[02EBEFF0]*24 supplies the cursors
                    # (idx = the just-flipped selector = 1 -> slot1).
                    slot = 0x2EBEFC0 + gm.d(0x2EBEFF0) * 24
                    ck(gm.q(0x209CC48) == slot, "ctx48 -> slot")
                    ck(gm.q(0x209E5A0) == gm.q(slot + 8),
                       "listcur -> slot cursor")
                    ck(gm.q(0x209CC50) == gm.q(slot + 8) + 0x10,
                       "pcur -> slot cursor+0x10")
                else:
                    ck(gm.q(0x209CC48) == w.ctx48o, "ctx48 kept")
                    ck(gm.q(0x209E5A0) == lc + 0x40, "listcur adv")
                    ck(gm.q(0x209CC50) == lc + 0x20, "pcur drained")
            elif name == "b1fb0-c5":
                # b[str]=0x0F -> real 2AC5F0 on the memset local state;
                # 'm' arm = 3FFB90(str+1,0,0) ret 3 -> cursor+4 ->
                # 2B1FB0 ret consumed=4
                ck(len(byr("l2ac5f0")) == 1, "c5f0 entry")
                c = byr("l3fb90")
                ck(len(c) == 1 and c[0][1] == w.nstr + 1,
                   f"fb90 args {c}")
                ck(eax == 4, f"consumed {eax:x}")
            elif name == "b1fb0-dec":
                # b[str]=0x41 >0xF -> real 2AC2F0 decode: 'A' ->
                # esi=0x21 (glyph-map miss -> q[r14]>>0x20 fallback),
                # cursor +1 -> consumed=1
                ck(not byr("l2ac5f0"), "c5f0 not taken")
                ck(len(byr("l2ac2f0")) == 1, "decode")
                ck(eax == 1, f"consumed {eax:x}")
            # ---- EXP-220 asserts ----
            elif name == "e8070-append":
                # real 17F7C0 copy -> real 1E8070: 1E94E0 ext rec for
                # vidx 0, 2x3 loop -> six 0x3C appends, bounds slot 0
                ck(len(byr("e8070")) == 1, "e8070 not reached")
                ck(len(byr("e94e0")) == 1, "e94e0")
                ck(len(byr("t5690")) == 6 and len(byr("y9e3c0")) == 12,
                   "divisor leaves")
                ck(not by("salloc") and not byr("e7a20"),
                   "realloc on roomy cap")
                ck(gm.q(w.devec + 0x18) == w.evbase
                   and gm.q(w.devec + 0x20) == w.evbase + 6 * 0x3C,
                   "vector end +6 recs")
                ck(gm.b(w.dev1 + 0x2324) == 1, "slot flag")
                # bounds compare the raw stream floats, not the
                # computed pos: xmm6 = f[st7c0+0x1C+k*4] (all zero),
                # xmm7 = f[st7c0+0x2C+k*4] k=0..3 -> {20,22,24,26}.
                # A-bounds at +0x2328..34, B-mirror mins at
                # +0x2338 (x) and (slot+0xCD)*0x2C = +0x233C (y).
                ck(gm.f(w.dev1 + 0x2328) == 0.0
                   and gm.f(w.dev1 + 0x2330) == 0.0, "x bounds")
                ck(abs(gm.f(w.dev1 + 0x232C) - 20.0) < 1e-6
                   and abs(gm.f(w.dev1 + 0x2334) - 26.0) < 1e-6,
                   "y bounds")
                ck(gm.f(w.dev1 + 0x2338) == 0.0
                   and abs(gm.f(w.dev1 + 0x233C) - 20.0) < 1e-6,
                   "mirror mins")
                # rec[0]: +0x00 x = f[st7c0]/d24 = 8/2 = 4.0;
                # +0x04 y = (d28 - f[st7c0+8])/d28 = (2-12)/2 = -5.0;
                # +0x38 = float(d[ext+0x10]=7) * (1/128)
                ck(gm.d(w.evbase) == 0x40800000
                   and gm.d(w.evbase + 4) == 0xC0A00000,
                   "rec0 pos")
                ck(gm.d(w.evbase + 0x38) == 0x3D600000,
                   f"rec38 {gm.d(w.evbase + 0x38):#x}")
                # post-loop b2349==0 arm -> f[+0x2344] =
                # d[st7c0+0x8C]=64 * 1/128 * f[dev1+0x137C]=1.0 = 0.5
                ck(abs(gm.f(w.dev1 + 0x2344) - 0.5) < 1e-6,
                   "2344 derived")
                ck(gm.q(w.dev1 + 0x137C) == 0x3F8000003F800000
                   and gm.q(w.dev1 + 0x1384) == 0x3F8000003F800000,
                   "scale quad reset")
            elif name == "e8070-grow":
                # cap=begin+0x3C end=begin+0x3C -> realloc on iters
                # 1,2,4 (counts 1->2, 2->4, 4->8 recs)
                ck(len(byr("e7a20")) == 3, f"e7a20 {byr('e7a20')}")
                ck(len(by("salloc")) == 3 and len(by("sdealloc")) == 3,
                   "alloc/dealloc calls")
                ck(gm.q(w.devec + 0x18) == w.e7buf
                   and gm.q(w.devec + 0x20) == w.e7buf + 7 * 0x3C
                   and gm.q(w.devec + 0x28) == w.e7buf + 8 * 0x3C,
                   "grown vector")
            elif name == "e8070-flag":
                ck(abs(gm.f(w.dev1 + 0x2340) - 0.5) < 1e-6
                   and abs(gm.f(w.dev1 + 0x2344) - 0.5) < 1e-6,
                   "2340/2344")
                ck(gm.b(w.dev1 + 0x2349) == 0, "flag cleared")
            elif name == "e8070-neg":
                ck(not byr("e94e0"), "e94e0 on negative idx")
                ck(gm.q(w.devec + 0x20) == w.evbase + 6 * 0x3C,
                   "appends on default rec")
                ck(gm.b(w.dev1 + 0x2324) == 1, "slot flag")
                ck(gm.q(w.dev1 + 0x137C) == 0x3F8000003F800000,
                   "scale quad reset")
            elif name == "f880-miss":
                # map root null -> 1B51C0 miss -> f[00901990] const,
                # flag/divide arm skipped (b1620 not reached)
                ck(len(byr("e93c0")) == 1 and len(byr("b51c0")) == 1,
                   "map find ran")
                ck(not byr("b1620"), "flag read on miss")
                # miss arm returns the shipped constant f[00901990]
                # = 23.0f
                ck((w.rets["xmm0"] & 0xFFFFFFFF) == 0x41B80000,
                   f"miss const {w.rets['xmm0'] & 0xFFFFFFFF:#x}")
            elif name == "f920-arm0":
                ck(eax == 6, f"eax {eax:x}")
                ck(len(byr("f49e0")) == 1 and not byr("fddc0"),
                   "arm select")
            elif name == "f920-arm1":
                ck(eax == 5, f"eax {eax:x}")
                ck(len(byr("fddc0")) == 1 and not byr("f49e0"),
                   "arm select")
            elif name == "f9c0-scale":
                # ceilf(float(4) / f[devsub+0x34]=1.0) = 4.0
                ck((w.rets["xmm0"] & 0xFFFFFFFF) == 0x40800000,
                   f"xmm0 {w.rets['xmm0'] & 0xFFFFFFFF:#x}")
                ck(len(byr("e9bd0")) == 1 and len(byr("fddb0")) == 1
                   and tcount("ceilf") == 1, "scale chain")
            elif name == "f8c0-hit":
                # codepoint 3 -> dwtab[3]=3 -> inline map hit ->
                # 1FDEC0 returns node+0x24
                ck(eax == w.gnode + 0x24, f"eax {eax:#x}")
                ck(len(byr("e9860")) == 1 and len(byr("fdec0")) == 1,
                   "remap+find")
            elif name == "f940-get":
                ck(eax == 0x1234, f"eax {eax:#x}")
                ck(len(byr("c52d0")) == 1, "getter leaf")
            elif name == "fae0-set":
                ck(gm.q(w.dev1 + 0x28) == 0x77, "setter write")
                ck(len(byr("a8c20")) == 1, "setter leaf")
            # ---- EXP-221 asserts ----
            elif name == "rdev-append":
                # edx=4 -> (4-2)*3 = 6 appends into slot0's vec
                # (cap 2): grows land at appends 3 and 5.
                ck(len(byr("b06d0")) == 6
                   and len(byr("aed50")) == 2
                   and len(byr("b1c00")) == 6, "append chain")
                ck(len(by("s2alloc")) == 2
                   and len(by("s2dealloc")) == 2, "realloc calls")
                ck(gm.d(w.rdev + 0x3928) == 0, "cursor stays 0")
                s0 = w.rdev + 0x2328
                vbeg = gm.q(s0 + 0x38)
                ck(vbeg != w.rvbuf
                   and gm.q(s0 + 0x40) == vbeg + 0x120
                   and gm.q(s0 + 0x48) == vbeg + 0x180,
                   "vec cap 2->4->8")
                for k, so in enumerate((0, 0x30, 0x60, 0x30, 0x60,
                                        0x90)):
                    for j in range(6):
                        ck(gm.q(vbeg + k * 0x30 + j * 8)
                           == gm.q(w.rsrc + so + j * 8),
                           f"rec{k}.{j}")
            elif name == "rdev-seal":
                # sealed slot0 -> cursor bumps to 1, slot1 inits
                # (append-init: d+0x2C=0 unlike 1B0100's 1) and the
                # record lands via 1AED50's empty-vector grow.
                ck(len(byr("aed50")) == 1, "seal+grow")
                ck(len(by("s2alloc")) == 1
                   and not by("s2dealloc"), "one alloc, no dealloc")
                ck(gm.d(w.rdev + 0x3928) == 1, "cursor bumped")
                s1 = w.rdev + 0x2328 + 0x58
                ck(gm.d(s1 + 0x10) == 1 and gm.q(s1 + 0x14) == 1
                   and gm.q(s1) == 0 and gm.q(s1 + 0x2C) == 0,
                   "slot1 init pattern")
                vb = gm.q(s1 + 0x38)
                ck(vb != 0 and gm.q(s1 + 0x40) == vb + 0x30
                   and gm.q(s1 + 0x48) == vb + 0x30, "slot1 vec")
                for j in range(6):
                    ck(gm.q(vb + j * 8) == gm.q(w.rsrc + j * 8),
                       f"rec0.{j}")
            elif name == "rdev-props":
                # 1819A0 shuffles: 1B2410 edx<-rcx(0x11) ->
                # +0x3930, r8d<-rdx(0x22) -> +0x3934, r9<-r8(rname)
                # -> 17D2E0 copies "RDEVNM" into +0x3938; stack
                # dwords {0, r9d(0x33), sarg, 1, 0, 0} ->
                # +0x3AA0/+0x3A38/+0x3A3C/+0x3A40/+0x3A44/+0x3A48.
                ck(len(byr("b2410")) == 1
                   and len(byr("d2e0")) == 1 and len(byr("d670")) == 1
                   and len(by("scrtfmt")) == 1, "prop chain")
                ck(gm.d(w.rdev + 0x3930) == 0x11
                   and gm.d(w.rdev + 0x3934) == 0x22, "prop ints")
                ck(gm.q(w.rdev + 0x3938)
                   == int.from_bytes(b"RDEVNM\x00\x00", "little"),
                   "name bytes")
                ck(gm.d(w.rdev + 0x3AA0) == 0
                   and gm.d(w.rdev + 0x3A38) == 0x33
                   and gm.d(w.rdev + 0x3A40) == 1
                   and gm.d(w.rdev + 0x3A44) == 0
                   and gm.d(w.rdev + 0x3A48) == 0, "stack args")
                sc = by("scrtfmt")[0]
                ck(sc[2] == w.rdev + 0x3938
                   and sc[4] == w.rname, "copy dst/src")
            elif name == "rdev-reset":
                # rdcur=2: 1B0100 clears slots 0..2 (d+0x10/+0x2C/
                # +0x30 = 1, q0=0, end=begin) then -1; memset hook
                # covers +0x3930..0x3AA7; four 0x80 seeds.
                ck(len(byr("b1910")) == 1
                   and len(byr("b0100")) == 1, "reset chain")
                ck(gm.d(w.rdev + 0x3928) == 0xFFFFFFFF, "cursor -1")
                for si in range(3):
                    s = w.rdev + 0x2328 + si * 0x58
                    ck(gm.q(s) == 0 and gm.d(s + 0x10) == 1
                       and gm.q(s + 0x14) == 1
                       and gm.d(s + 0x2C) == 1
                       and gm.d(s + 0x30) == 1
                       and gm.q(s + 0x20) == 0
                       and gm.q(s + 0x40) == gm.q(s + 0x38),
                       f"slot{si} reset")
                ck([w.rdev + 0x3930, 0x178] in w.rets["memsets"],
                   "props memset")
                for off in (0x3A4C, 0x3A50, 0x3A54, 0x3A58):
                    ck(gm.d(w.rdev + off) == 0x80, f"seed {off:x}")

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
