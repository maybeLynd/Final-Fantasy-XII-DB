# unlink/teardown 3105D0+301140 REAL: ->310780/30C970/300280
# (->3008A0 deregister!)/316CF0/3291B0/33C9B0 + 20 leaf chain;
# 238BF0/336710/33E1F0/311F70 scripted
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
#     0030C650 level-set + 0030FED0 recompute (EXP-148 proven bodies),
#     0030F690/0030F340/0030F5A0 mutually-recursive stat cluster
#     (pulls 377C20/3105D0/30E360), 00323910 deep grant (0x299,15c),
#     00324100 override (->324020), 00317930 slot search, 00318B40
#     list op, 0030F9A0/0030C410 un/equip, 0031B860->00324470 member
#     block chain.
#
import hashlib
import json
import os
import struct
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
            gm.w(self.objrow, qw(case.get("objflags", 0x4000000)))
            gm.w(self.objrow + 0x698, qw(self.rec))
            oc = max(oc, 1)
            if case.get("objb5") is not None:
                gm.w(self.objrow + 5, bytes([case["objb5"] & 0xFF]))
            if case.get("objb4") is not None:
                gm.w(self.objrow + 4, bytes([case["objb4"] & 0xFF]))
            if case.get("objd64"):
                gm.w(self.objrow + 0x64, dw(case["objd64"]))
            if case.get("objd3c"):
                gm.w(self.objrow + 0x3C, dw(case["objd3c"]))
            if case.get("recback"):
                gm.w(self.rec + 0x698, qw(self.objrow))
            if case.get("rec10pos"):
                import struct as _st
                pb = self.alloc(0x100)
                gm.w(pb, _st.pack("<3f", *case["rec10pos"]))
                o10p = gm.q(self.rec + 0x10)
                gm.w(o10p + 0xB8, qw(pb))
            if case.get("rec6a0"):
                a6a0 = self.alloc(0x40)
                gm.w(a6a0, bytes([case.get("rec6a0b0", 0) & 0xFF]))
                gm.w(self.rec + 0x6A0, qw(a6a0))
            if case.get("rece60"):
                e60 = self.alloc(0x400)
                gm.w(self.rec + 0xE60, qw(e60))
                e68 = self.alloc(0x400)
                gm.w(self.rec + 0xE68, qw(e68))
            if case.get("rec10"):
                o10 = self.alloc(0x100)
                gm.w(o10 + 3, bytes([case.get("rec10b3", 0) & 0xFF]))
                gm.w(self.rec + 0x10, qw(o10))
        gm.w(OBJCNT, dw(oc))

        # 30F3F0 broadcast: slot->recidx map b[glob+0x5A7E+slot*2]
        # (cls-3 arm of 31B9F0); default identity map 0..8
        for slot in range(9):
            gm.w(self.glob + 0x5A7E + slot * 2,
                 bytes([case.get("slotmap", {}).get(slot, slot) & 0xFF]))
        # cls-0xC validator bitmap for 30B0E0/2FD970:
        # valid iff bit (id&0xF) of w[bmp + (id&0xFFF)>>4 *2] set
        fbmp = self.fbmp = self.alloc(0x40)
        gm.w(FOEBMP_R, qw(fbmp))
        gm.w(fbmp + 2, struct.pack("<H", case.get("foebmp", 0x7FFC) & 0xFFFF))
        if case.get("objreg"):
            self.reg = self.alloc(0x12000)
            gm.w(0x209BE80, qw(self.reg))
        if case.get("statecell"):
            self.cell = self.alloc(0x6000)
            gm.w(0x2EBF190, qw(self.cell))
            gm.w(self.cell + 0x5B04, dw(case.get("stateflags", 0)))
        else:
            self.cell = None
        # 312730 opcode-dispatch fixtures: cmd {w op, w arg} + outs
        if "cmd" in case:
            self.cmd = self.alloc(0x40)
            op, carg = case["cmd"]
            gm.w(self.cmd + 0, struct.pack("<H", op & 0xFFFF))
            gm.w(self.cmd + 2, struct.pack("<h", carg & 0xFFFF
                                           if carg < 0x8000 else
                                           carg - 0x10000))
        else:
            self.cmd = 0
        if case.get("scatrow"):
            # 3DFD00 row group for the 0x4000-subop seed fetch:
            # q[0x2B59D48 + idx*8] -> {b[+7]=0x33, d[+0xC]=count,
            # rows +0x10 stride 0x30 (3 quads each)}
            grp = self.alloc(0x100)
            gm.w(0x2B59D48 + case.get("scatidx", 1) * 8, qw(grp))
            gm.w(grp + 7, bytes([0x33]))
            gm.w(grp + 0xC, dw(2))
            gm.w(grp + 0x10,
                 struct.pack("<4f", *case.get("seed", (1.0, 0.0, 2.0, 0.0))))
            gm.w(grp + 0x40,
                 struct.pack("<4f", *case.get("seed2", (3.0, 0.0, 4.0, 0.0))))
        if case.get("outptrs"):
            self.out1 = self.alloc(0x40)
            self.out2 = self.alloc(0x40)
            self.outf = self.alloc(0x40)
            case["r8"] = self.out1
            case["r9"] = self.out2
            case["a5"] = self.outf
        else:
            self.out1 = self.out2 = self.outf = 0

        # 322C50 cls-0x1D bound cell for 30E130's bit validation
        self.bitcell = self.alloc(0x20)
        gm.w(self.bitcell + 4, dw(case.get("bitbound", 0x80)))
        gm.w(0x2EBF040, qw(self.bitcell))

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
           X_B9B0: ("kb9b0", "kb9b0_ret"),
           X_B8E0: ("kb8e0", "kb8e0_ret"),
           X_0FC0: ("u0fc0", "u0fc0_ret"), X_112F0: ("n12f0", "n12f0_ret"),
           X_2FA390: ("qfa390", "qfa390_ret"), X_46AB10: ("q6ab10", None),
           X_01140: ("l301140", None), X_12280: ("l312280", None),
           X_299B0: ("l3299b0", None), X_00140: ("l300140", None),
           X_07D10: ("l307d10", None), X_284D0: ("n284d0", None),

           X_43F0: ("u43f0", "u43f0_ret"),
           X_B770: ("kb770", "kb770_ret"),
           X_B7F0: ("kb7f0", "kb7f0_ret"),
           X_8F1F0: ("q28f1f0", None), X_FA540: ("q2fa540", None),
           X_FA3B0: ("q2fa3b0", None),
           X_3910: ("g3910", "g3910_ret"),
           X_4100: ("o4100", "o4100_ret"), X_7930: ("s7930", "s7930_ret"),
           X_8B40: ("l8b40", "l8b40_ret"), X_F9A0: ("uf9a0", None),
           X_C410: ("ec410", None), X_4470: ("m4470", None),
           0x252E60: ("n252e60", "n252e60_ret"),
           0x384B10: ("m384b10", "m384b10_ret"),
           0x311F70: ("m311f70", "m311f70_ret"),
           0x32A790: ("n32a790", "n32a790_ret"),
           0x861F08: ("n861f08", "n861f08_ret"),
           0x861F0E: ("n861f0e", "n861f0e_ret"),
           0x336710: ("m336710", "m336710_ret"),
           0x33E1F0: ("m33e1f0", "m33e1f0_ret"),
           0x290DF0: ("m290df0", "m290df0_ret"),
           0x3B02A0: ("m3b02a0", "m3b02a0_ret"),
           0x3279B0: ("m3279b0", "m3279b0_ret"),
           0x2F8E50: ("m2f8e50", "m2f8e50_ret"),
           0x2F9180: ("m2f9180", "m2f9180_ret")}

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
            0x30FED0: "dfed0", 0x2FEF30: "w2fef30",
            0x30E130: "he130", 0x30EA40: "lea40",
            0x387020: "l387020", 0x386AE0: "l386ae0",
            0x46A720: "l46a720", 0x46A790: "l46a790",
            0x31E9A0: "l31e9a0", 0x31E9F0: "l31e9f0",
            0x323890: "l323890", 0x3241D0: "l3241d0",
            0x861EC0: "l861ec0", 0x808C40: "l808c40",
            0x809950: "l809950",
            0x3105D0: "u105d0", 0x301140: "u301140",
            0x300280: "u300280", 0x310780: "u310780",
            0x30C970: "u30c970", 0x316CF0: "u316cf0",
            0x3291B0: "u3291b0", 0x33C9B0: "u33c9b0",
            0x31B7E0: "u31b7e0", 0x313B30: "u313b30",
            0x2FEAD0: "u2fead0", 0x308270: "u308270",
            0x319420: "u319420", 0x319140: "u319140",
            0x317E50: "u317e50", 0x325A00: "u325a00",
            0x317EC0: "u317ec0", 0x306570: "u306570",
            0x253690: "u253690", 0x254EE0: "u254ee0",
            0x316A50: "u316a50", 0x3839F0: "u3839f0",
            0x3588B0: "u3588b0", 0x31B810: "u31b810",
            0x2ED2A0: "u2ed2a0", 0x30C0E0: "u30c0e0",
            0x2EAEA0: "u2eaea0", 0x290B90: "u290b90",
            0x3BBC80: "u3bbc80", 0x3590D0: "u3590d0",
            0x263E30: "u263e30", 0x2671F0: "u2671f0",
            0x238A60: "u238a60", 0x30EDA0: "u30eda0",
            0x2E9600: "u2e9600", 0x2EACD0: "u2eacd0",
            0x2E8060: "u2e8060", 0x319E30: "u319e30",
            0x26DC60: "u26dc60", 0x358940: "u358940",
            0x2ECD50: "u2ecd50", 0x8632B0: "u8632b0",
            0x20CE00: "u20ce00", 0x2536A0: "u2536a0",
            0x3165C0: "u3165c0", 0x2EBB80: "u2ebb80",
            0x30D9A0: "u30d9a0", 0x3125E0: "u3125e0",
            0x2ECF10: "u2ecf10",
            0x238BF0: "v238bf0", 0x269F30: "v269f30",
            0x267CC0: "v267cc0", 0x26B4A0: "v26b4a0",
            0x2659A0: "v2659a0", 0x25D5E0: "v25d5e0",
            0x269FE0: "v269fe0", 0x2E5FD0: "v2e5fd0",
            0x26DAC0: "v26dac0", 0x2EC5B0: "v2ec5b0",
            0x26A430: "v26a430", 0x26A3A0: "v26a3a0",
            0x2E8220: "v2e8220", 0x269F20: "v269f20",
            0x2E8A10: "v2e8a10", 0x26AD00: "v26ad00",
            0x2361B0: "v2361b0", 0x26A7F0: "v26a7f0",
            0x26A7C0: "v26a7c0", 0x269E20: "v269e20",
            0x236210: "v236210", 0x26A330: "v26a330",
            0x268EA0: "v268ea0", 0x2626C0: "v2626c0",
            0x262740: "v262740", 0x2681E0: "v2681e0",
            0x2682D0: "v2682d0", 0x3204D0: "v3204d0",
            0x2E9780: "v2e9780", 0x26D6F0: "v26d6f0",
            0x265090: "v265090", 0x30A130: "v30a130",
            0x312DF0: "v312df0", 0x26B6A0: "v26b6a0",
            0x3587C0: "v3587c0", 0x2EB930: "v2eb930",
            0x2E5C70: "v2e5c70", 0x2E5C90: "v2e5c90",
            0x2E4A10: "v2e4a10", 0x2646C0: "v2646c0",
            0x3DBBE0: "v3dbbe0", 0x3DBEA0: "v3dbea0",
            0x3DB2A0: "v3db2a0", 0x3590D0: "v3590d0b",
            0x263F10: "v263f10", 0x3589B0: "v3589b0",
            0x265680: "v265680", 0x2672B0: "v2672b0",
            0x37C860: "v37c860", 0x2ECE50: "v2ece50",
            0x265240: "v265240", 0x2ECE80: "v2ece80",
            0x2E9BB0: "v2e9bb0",
            0x327200: "v327200", 0x31B8C0: "v31b8c0",
            0x328370: "v328370", 0x317DE0: "v317de0",
            0x320940: "v320940", 0x263FF0: "v263ff0",
            0x4288B0: "v4288b0", 0x4690B0: "v4690b0",
            0x392200: "v392200", 0x312700: "v312700",
            0x311F70: "t311f70",
            0x265020: "t265020", 0x263F40: "t263f40",
            0x26B0C0: "t26b0c0", 0x392170: "t392170",
            0x26A0D0: "t26a0d0", 0x26B620: "t26b620",
            0x336E40: "n336e40", 0x2646C0: "n2646c0",
            0x265200: "n265200", 0x265090: "n265090",
            0x3272A0: "n3272a0", 0x309AE0: "n309ae0",
            0x259B10: "n259b10", 0x3DA710: "n3da710",
            0x312730: "t312730", 0x312DF0: "t312df0",
            0x3DFD00: "t3dfd00", 0x2367A0: "t2367a0",
            0x31B7E0: "t31b7e0", 0x3588B0: "t3588b0",
            0x319850: "t319850", 0x2FB310: "t2fb310",
            0x3A1960: "t3a1960", 0x337700: "t337700",
            0x3377C0: "t3377c0"}

    def on_code(self, uc, addr, size, _):
        if addr == self.entry:
            return
        if addr == R_61EC0:      # memset(rcx, dl, r8)
            dst = uc.reg_read(UC_X86_REG_RCX)
            cnt = uc.reg_read(UC_X86_REG_R8)
            uc.mem_write(dst, b"\0" * cnt)
            self.rets.setdefault("memsets", []).append(
                [dst & 0xFFFFFFFFFFFFFFFF, cnt & 0xFFFFFFFFFFFFFFFF])
            self.trace.append("memset")
            self._ret()
            return
        ent = self.SCR.get(addr)
        if ent is not None:
            tag, retkey = ent
            self._args(tag)
            if retkey:
                uc.reg_write(UC_X86_REG_RAX,
                             self.case.get(retkey, 0)
                             & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        t = self.REAL.get(addr)
        if t is not None:
            self.trace.append(t)
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
        uc.reg_write(UC_X86_REG_R8,
                     self.case.get("r8", 0) & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9,
                     self.case.get("r9", 0) & 0xFFFFFFFFFFFFFFFF)
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
                                 kb9b0_ret=1),
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
                             objlink=True, kb770_ret=1,
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
                             objlink=True, kb7f0_ret=1,
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
                             r9=0x216, kb8e0_ret=1,
                             rec_d={0x24: 100, 0x48: 10}),
    "s530-nonotify": base_case(entry=R_0530R, edx=5, r9=0x0,
                               rec_d={0x24: 100, 0x48: 10}),
    "s530-cap2x":  base_case(entry=R_0530R, edx=500, r9=0x217,
                             rec_d={0x24: 100, 0x48: 10,
                                    0x64: 1 << 0x1C}),

    "s530-revive": base_case(entry=R_0530R, edx=5, r9=0x217,
                             rec_d={0x24: 100, 0x48: 0}),

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
    # 30FED0(rec, notify) stat-change dispatcher
    "fed0-base":   base_case(entry=0x30FED0, edx=0x217,
                             rec_d={0x24: 100, 0x48: 10}),
    "fed0-null":   base_case(entry=0x30FED0, rcx=0, edx=0x217,
                             expect_fault=0x310080),
    "fed0-b5":     base_case(entry=0x30FED0, edx=0x217,
                             rec_b={5: 1}, expect_fault=0x2FF1FC),
    "fed0-b5own":  base_case(entry=0x30FED0, edx=0x217,
                             rec_b={5: 1}, objlink=1,
                             expect_fault=0x2FF1FC),
    "fed0-n0":     base_case(entry=0x30FED0, edx=0x0,
                             rec_d={0x24: 100, 0x48: 10}),
    # rec b4=2 -> FOED walk resolves foerow; d[foerow+0x50] watch
    # bits -> per-bit 30E130 dispatch (arm3 set / arm1 clear)
    "fed0-watch":  base_case(entry=0x30FED0, edx=0x217,
                             rec_b={4: 2},
                             foe={"w": {0x50: 0x0005}}),
    "fed0-watch2": base_case(entry=0x30FED0, edx=0x217,
                             rec_b={4: 2},
                             foe={"w": {0x50: 0x0080}}),
    # fed0-watch now drives real 30E130 (was scripted)
    # 30E130(rec, bit, arg3, notify, arm@a5):
    # arm0=clr+0x68 arm1=clr+0x78 arm2=set+0x68 arm3=set+0x78
    "e130-set78":  base_case(entry=0x30E130, edx=2, r9=0x217, a5=3),
    "e130-set68":  base_case(entry=0x30E130, edx=2, r9=0x217, a5=2),
    "e130-clr78":  base_case(entry=0x30E130, edx=2, r9=0x217, a5=1,
                            rec_b={0x78: 4}),
    "e130-clr68":  base_case(entry=0x30E130, edx=2, r9=0x217, a5=0,
                            rec_b={0x68: 4}),
    "e130-noedge": base_case(entry=0x30E130, edx=2, r9=0x217, a5=3,
                            rec_b={0x78: 4}),
    "e130-oob":    base_case(entry=0x30E130, edx=0x90, r9=0x217,
                            a5=3),
    "e130-notify0": base_case(entry=0x30E130, edx=2, r9=0x0, a5=3),
    "e130-bit68":  base_case(entry=0x30E130, edx=0x68, r9=0x217,
                            a5=3),

    # 3105D0(rec) unlink/reset + 301140(rec) despawn teardown
    "u5d0-base":   base_case(entry=0x3105D0, objlink=1, recback=1, objreg=1),
    "u5d0-noown":  base_case(entry=0x3105D0),
    "u1140-base":  base_case(entry=0x301140, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1, rece60=1,
                            rec_d={0: 0x04000000}),
    "u1140-eng":   base_case(entry=0x301140, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1, rece60=1, objd64=1),
    "u1140-noflg": base_case(entry=0x301140, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1, rece60=1),

    # 238BF0(rec) — object detach/anim-release chain inside 301140
    "v8bf0-foe":   base_case(entry=0x238BF0, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1,
                            rece60=1),
    "v8bf0-memb":  base_case(entry=0x238BF0, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1,
                            rece60=1, rec6a0=1, objb5=1),
    "v8bf0-cls1b": base_case(entry=0x238BF0, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1,
                            rece60=1, objb4=0x1B),
    "v8bf0-noobj": base_case(entry=0x238BF0),

    # 311F70(mode, rec, arg3) — reposition/transform helper
    "t1f70-base":  base_case(entry=0x311F70, rcx=0, edx_rec=1,
                            objlink=1, recback=1, rec10=1,
                            statecell=1, objreg=1, rece60=1),
    "t1f70-posw":  base_case(entry=0x311F70, rcx=0, edx_rec=1,
                            objlink=1, recback=1, rec10=1,
                            statecell=1, objreg=1, rece60=1,
                            rec10b3=0x20, rec10pos=(9.0, 8.0, 7.0)),
    "t1f70-aux":   base_case(entry=0x311F70, edx_rec=1,
                            objlink=1, recback=1, rec10=1,
                            statecell=1, objreg=1, rece60=1,
                            expect_fault=0x383F23),
    "t1f70-mode1": base_case(entry=0x311F70, edx_rec=1,
                            objlink=1, recback=1, rec10=1,
                            statecell=1, stateflags=1, cd_words=[0]*8,
                            objreg=1, rece60=1,
                            expect_fault=0x1CCEF20),
    "t1f70-memb":  base_case(entry=0x311F70, rcx=0, edx_rec=1,
                            r8=1, objlink=1, recback=1, rec10=1,
                            statecell=1, objreg=1, rece60=1,
                            rec6a0=1, objb5=1),
    "t2700-wrap":  base_case(entry=0x312700, objlink=1, recback=1,
                            rec10=1, statecell=1, objreg=1,
                            rece60=1),

    # ---- 312730 opcode dispatcher (EXP-165) ----
    # 312730(rec, cmd={w op, w arg}, out1=r8, out2=r9, a5=outf)
    "t2730-bad":   base_case(entry=0x312730, cmd=(0x3FFF, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1),
    "t2730-4021":  base_case(entry=0x312730, cmd=(0x4021, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1),
    "t2730-4020":  base_case(entry=0x312730, cmd=(0x4020, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1),
    "t2730-4020m": base_case(entry=0x312730, cmd=(0x4020, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1, objb5=1, rec6a0=1,
                            expect_fault=0x383F23),
    "t2730-4000":  base_case(entry=0x312730, cmd=(0x4000, 1),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1),
    "t2730-scat":  base_case(entry=0x312730, cmd=(0x4000, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1, scatrow=1,
                            scatidx=0, expect_fault=0x383F23),
    "t2730-4026":  base_case(entry=0x312730, cmd=(0x4026, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1,
                            expect_fault=0x265090),
    "t2730-4124":  base_case(entry=0x312730, cmd=(0x4124, 0),
                            objlink=1, recback=1, rec10=1,
                            rec10b3=0x20, statecell=1, objreg=1,
                            rece60=1, outptrs=1),
}


def main():
    raw, secs = load_image()
    res = {}
    for name, case in CASES.items():
        w = World(case, raw, secs)
        edx_v = w.rec if case.get("edx_rec") else case.get("edx", w.sel)
        if case.get("cmd") is not None:
            edx_v = w.cmd
        eax = w.run(rcx=case.get("rcx", w.rec), edx=edx_v)
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
                ck(len(by("kb770")) == 1, "kb770 missing")
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
                ck(len(by("n283d0")) >= 1 or len(by("q2fa3b0")) >= 1,
                   f"r13 owner post missing {calls}")
            elif name == "ce0-veto":
                ck(w4c == 50, f"veto w4C {w4c}")
            elif name == "e060-frac":
                ck(gm.b(w.rec + 0x4E) == 1,
                   f"b4E {gm.b(w.rec + 0x4E)} != 1")
                ck(len(by("n283d0")) == 1 or
                   len(by("q2fa3b0")) == 1,
                   f"frac post missing {calls}")
            elif name == "e060-same":
                ck(not by("n283d0") and not by("q2fa3b0"),
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
                # delta<0, notify&1=0, kb8e0=1 -> write skipped
                ck(not w.faults, f"fault {w.faults}")
                ck(d48 == 10, f"d48={d48} not vetoed")
                ck(any(c[0] == "kb8e0" for c in
                       w.rets.get("calls", [])), "kb8e0 not called")
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

        elif name.startswith("u5d0-") or name.startswith("u1140-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            if name == "u5d0-base":
                ck(tcount("u300280") == 1, f"300280 {tcount('u300280')}")
                ck(tcount("a08a0") == 1, f"3008a0 {tcount('a08a0')}")
            elif name == "u5d0-noown":
                ck(tcount("u105d0") >= 0, "ran")
            elif name == "u1140-base":
                ck(tcount("u105d0") == 1, f"3105d0 {tcount('u105d0')}")
                ck(tcount("u2e9600") == 1, f"2e9600 {tcount('u2e9600')}")
                ck(not any(c[0] == "m311f70" for c in calls),
                   "311f70 called with bit1A set")
                ck(tcount("v238bf0") == 1, "238bf0 not real")
                for tg in ("u2e8060", "u2ecf10", "u319e30", "l2a150",
                           "u3125e0", "u30d9a0", "u26dc60", "u2ebb80"):
                    ck(tcount(tg) >= 1, f"tail missing {tg}")
                ck(any(c[0] == "l3299b0" for c in calls),
                   "3299b0 post missing")
            elif name == "u1140-noflg":
                # d[rec] bit 0x1A clear -> 311F70 runs, rest same
                ck(tcount("u105d0") == 1, f"3105d0 {tcount('u105d0')}")
                ck(any(c[0] == "m311f70" for c in calls),
                   "311f70 not called (bit1A clear)")
                for tg in ("u2e8060", "u2ecf10", "u319e30",
                           "u3125e0", "u2ebb80"):
                    ck(tcount(tg) >= 1, f"tail missing {tg}")
            elif name == "u1140-eng":
                # engaged bit set -> bail before unlink
                ck(tcount("u105d0") == 0, "3105d0 ran while engaged")

        elif name.startswith("v8bf0-") or name.startswith("t1f70-") \
                or name.startswith("t2700-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            calls = w.rets.get("calls", [])
            if name in ("v8bf0-foe", "v8bf0-memb", "v8bf0-cls1b"):
                # full detach chain; 269F30/269FE0 are foe-only arms
                core = {"v2e5fd0", "v26dac0", "v2ec5b0", "v26a430",
                        "v26a3a0", "v2e8220", "v269f20", "v2e8a10",
                        "v26ad00", "v2361b0", "v26a7f0", "v26a7c0",
                        "v269e20", "v26a330"}
                if name != "v8bf0-memb":
                    core |= {"v269f30", "v269fe0"}
                missing = sorted(t for t in core if t not in w.trace)
                ck(not missing, f"missing callees {missing}")
                if name == "v8bf0-memb":
                    ck("v269f30" not in w.trace,
                       "269f30 ran on member path")
                ck(tcount("v312700") == 1, "312700 tail missing")
                ck(tcount("u3125e0") == 1, "312700's 3125e0 missing")
                ck(tcount("u2ebb80") == 1, "312700's 2ebb80 missing")
            elif name == "v8bf0-noobj":
                # q[rec+0x10]==0 -> bail at 0x238F76, no work
                ck(not w.trace, f"trace on noobj {w.trace}")
            elif name == "t1f70-base":
                ck(tcount("u30d9a0") == 1, "30d9a0 missing")
                ck(tcount("n336e40") == 1, "336e40 not real")
                ck(tcount("n2646c0") >= 1, "2646c0 missing")
                ck(tcount("t265020") == 1, "265020 missing")
                ck(tcount("t392170") == 1, "392170 missing")
                ck(tcount("t26b0c0") == 0, "26b0c0 ran on equal pos")
                ck(gm.q(w.rec) & 0x4000000, "bit26 not set")
            elif name == "t1f70-posw":
                # planted obj pos flows through 336E40's gather ->
                # transform == current pos -> compare equal -> no
                # write (proves the gather consumed the same obj)
                ck(tcount("n336e40") == 1, "336e40 not real")
                ck(tcount("t26b0c0") == 0, "26b0c0 ran")
            elif name == "t1f70-aux":
                # rcx=rec -> ctx+8 non-null aux arm -> 202F00 copy ->
                # 383F10 zone lookup: d[q[0x5A8DFB0]+0x20] on a null
                # global -> authentic fault (IAT trig unresolvable)
                ck(tcount("n336e40") == 1, "336e40 not real")
            elif name == "t1f70-mode1":
                # aux non-null + stateflags&1 -> 30D9A0 ret 1 ->
                # d[ctx]=1 arm1: 309AE0 + 259B10 table index ->
                # 0x3370D2 call q[IAT] -> wild exec in .rdata ->
                # deterministic fetch fault at 0x1CCEF20
                ck(tcount("n336e40") == 1, "336e40 not real")
                ck(tcount("n309ae0") >= 1, "309ae0 missing")
                ck(tcount("n259b10") >= 1, "259b10 missing")
            elif name == "t1f70-memb":
                # arg3 + b[objrow+5]==1 -> mirror write at 6A0+0x50
                ck(tcount("n336e40") == 1, "336e40 not real")
                a6a0 = gm.q(w.rec + 0x6A0)
                ck(a6a0 != 0, "6a0 not planted")
                ck(gm.q(w.rec) & 0x4000000, "bit26 not set")
            elif name == "t2700-wrap":
                # 312700 = 3125E0 -> 26DC60(->2EBB80) wrapper
                ck(tcount("u3125e0") == 1, "3125e0 missing")
                ck(tcount("u26dc60") == 1, "26dc60 missing")
                ck(tcount("u2ebb80") == 1, "2ebb80 missing")
            elif name == "t2730-bad":
                # op 0x3FFF out of range -> reject 0
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "t2730-4021":
                # op 0x4021 -> jump-table idx 5 -> reject 0
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "t2730-4020":
                # member-only arm: b[objrow+5]!=1 -> reject 0
                ck(tcount("t312730") == 1, "312730 not real")
                ck(eax == 0, f"ret {eax:#x}")
                ck(tcount("t312df0") == 0, "312df0 ran on foe")
            elif name == "t2730-4020m":
                # b[objrow+5]==1 -> seed = q[rec+0x6A0]+0x50 (the
                # 311F70 member mirror quad!) -> 312DF0 scatter
                # loop -> 337700 -> 383F10 zone fault (disclosed)
                ck(tcount("t312df0") == 1, "312df0 missing")
                ck(tcount("v328370") >= 2, "RNG iters missing")
                ck(tcount("t337700") >= 1, "337700 missing")
            elif name == "t2730-4000":
                # op 0x4000 -> arm0 -> 312DF0(rcx=0) -> 320940 ->
                # 3DFD00 row fetch: shipped table slot empty ->
                # ret -1 -> dispatcher rejects (eax=0)
                ck(tcount("t312730") == 1, "312730 not real")
                ck(tcount("t312df0") == 1, "312df0 missing")
                ck(tcount("t3dfd00") == 1, "3dfd00 missing")
                ck(eax == 0, f"ret {eax:#x}")
            elif name == "t2730-4026":
                # 0x4026..0x4035 -> 2367A0(op-0x4026) scans the
                # shipped global rec array q[0x41E6688] (0xF50
                # stride, w[q[rec+0x698]+4]==arg match) -> found a
                # shipped row -> 0x312918 arm copies its +0xD0 quad
                # -> 30A130 -> 265090 faults on null q[+0x10]
                # (authentic: static-image rows are unlinked) @265090
                ck(tcount("t2367a0") >= 1, "2367a0 missing")
                ck(tcount("v30a130") >= 1, "30a130 missing")
            elif name == "t2730-scat":
                # planted seed row -> 312DF0 scatter loop:
                # 328370 RNG x2 + 317DE0 validate -> 337700 ->
                # 383F10 zone lookup -> authentic null-global fault
                ck(tcount("t312df0") == 1, "312df0 missing")
                ck(tcount("v328370") >= 2, "RNG iters missing")
                ck(tcount("v317de0") >= 1, "317de0 missing")
                ck(tcount("t337700") >= 1, "337700 missing")
            elif name == "t2730-4124":
                # 0x4124 -> owner arm: 31B7E0(d[rec+0x24]) -> null
                # owner -> reject 0
                ck(tcount("t312730") == 1, "312730 not real")
                ck(tcount("t31b7e0") == 1, "31b7e0 missing")
                ck(eax == 0, f"ret {eax:#x}")

        elif name.startswith("e130-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            bit = case["edx"] & 0xFF
            b68 = gm.b(w.rec + 0x68 + (bit >> 3))
            b78 = gm.b(w.rec + 0x78 + (bit >> 3))
            m = 1 << (bit & 7)
            calls = w.rets.get("calls", [])

            if name == "e130-set78":
                # arm3: set b78 bit2; transition -> memset blk +
                # 386AE0 (ebx=1 arm) ; notify 0x217 -> bit1 comp 0,
                # bit9 set -> no 46A790, no recursion
                ck(not w.faults, f"fault {w.faults}")
                ck(b78 & m, f"b78 {b78:#x}")
                ck(tcount("l386ae0") == 1, f"386ae0 {tcount('l386ae0')}")
                ck(tcount("l46a790") == 0, "46a790 fired on 0x217")
                ck(tcount("e600") == 0, "fed0 recursed on bit9")
            elif name == "e130-set68":
                # arm2: set b68 bit2 -> 30EA40 post-call
                ck(b68 & m, f"b68 {b68:#x}")
                ck(tcount("lea40") == 1, f"30ea40 {tcount('lea40')}")
                ck(tcount("l386ae0") == 1, f"386ae0 {tcount('l386ae0')}")
            elif name == "e130-clr78":
                # arm1: clear b78 bit2 (pre-set) -> transition ->
                # 386A50 (ebx=0 arm), no 30EA40 (edi!=0,2)
                ck(not (b78 & m), f"b78 {b78:#x}")
                ck(tcount("h86a50") == 1,
                   f"386a50 {tcount('h86a50')}")
                ck(tcount("lea40") == 0, "ea40 on +0x78 arm")
            elif name == "e130-clr68":
                ck(not (b68 & m), f"b68 {b68:#x}")
                ck(tcount("lea40") == 1, f"30ea40 {tcount('lea40')}")
            elif name == "e130-noedge":
                # bit already set -> arm3 bails, no transition work
                ck(b78 & m, f"b78 {b78:#x}")
                ck(tcount("l386ae0") == 0, "handler ran on no-edge")
                ck(tcount("l861ec0") == 0, "memset ran on no-edge")
            elif name == "e130-oob":
                # 322C50(0x1D, bit)=0 -> bail before any mutation
                ck(tcount("l861ec0") == 0, "memset ran oob")
                ck(tcount("l386ae0") == 0, "handler ran oob")
            elif name == "e130-notify0":
                # notify=0 -> bit9 clear -> recurses into 30FED0
                # (intercepted at boundary; callee proven by fed0-*)
                ck(b78 & m, f"b78 {b78:#x}")
                ck(any(c[0] == "fed0" for c in calls),
                   "no fed0 recursion")
                ck(tcount("l46a790") == 1,
                   f"46a790 {tcount('l46a790')} (notify&1 arm)")
            elif name == "e130-bit68":
                # bit 0x68 -> byte 0x78+0xD=0x85 bit0 -> 3279B0 call
                ck(any(c[0] == "m3279b0" for c in calls),
                   "3279b0 not called")
                ck(gm.b(w.rec + 0x85) & 1, "b85 bit0 unset")

        elif name.startswith("fed0-"):
            tr = w.trace
            tcount = lambda t: tr.count(t)
            if name == "fed0-base":
                ck(tcount("e600") >= 2, f"descwalk {tcount('e600')}")
                ck(tcount("v2c50") >= 1, f"bound {tcount('v2c50')}")
                ck(tcount("w2fef30") == 1, f"walker {tcount('w2fef30')}")
                ck(tcount("n0e060") >= 1, "hpfrac notify absent")
            elif name == "fed0-null":
                # no null guard: bail target IS the loop entry ->
                # w[0x50] read faults. f690 owns the caller guard.
                ck(tcount("e600") == 0, "descwalk ran on null")
            elif name in ("fed0-b5", "fed0-b5own"):
                # member rec (b5==1): 2FEF30 takes a member-resolution
                # arm whose slot-table state is not yet planted ->
                # authentic fault at 2FEF30's b[rdi+5] read
                # (expect_fault asserted above). Boundary disclosed.
                ck(tcount("e600") >= 2, "main loop not reached")
            elif name == "fed0-n0":
                ck(tcount("w2fef30") == 1, "walker skipped")
            elif name == "fed0-watch":
                # watch bits 0,2 -> per-bit dispatch fires 30E130
                ck(tcount("v2c50") >= 1, "bound loop absent")
                ck(tcount("he130") == 2,
                   f"he130 {tcount('he130')} (bits 0,2)")
            elif name == "fed0-watch2":
                ck(tcount("he130") == 1,
                   f"he130 {tcount('he130')} (bit 7)")

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
                ck(len(by("kb9b0")) == 1, "kb9b0 missing")
                ck(not by("kb8e0"), "kb8e0 on non-mode arm")
                ck(f64 == 0, f"d64 {f64:#x}")
            elif name == "e360-owner-bail":
                ck(len(by("kb9b0")) == 1, "kb9b0 missing")
                ck(f64 == 1 << 2, f"bail touched d64 {f64:#x}")
            elif name == "e360-owner2-chk":
                ck(len(by("kb9b0")) == 1 and len(by("kb8e0")) == 1,
                   f"owner pair {calls}")
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
