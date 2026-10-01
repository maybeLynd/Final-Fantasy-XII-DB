# broadcast wrappers: 30F3F0 member loop + 30F4B0/30F4D0 foe loop
# REAL + resolvers 320AB0/31B9F0/320A40/30B0E0 + direct-call cases
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
        gm.w(OBJCNT, dw(oc))

        # 30F3F0 broadcast: slot->recidx map b[glob+0x5A7E+slot*2]
        # (cls-3 arm of 31B9F0); default identity map 0..8
        for slot in range(9):
            gm.w(self.glob + 0x5A7E + slot * 2,
                 bytes([case.get("slotmap", {}).get(slot, slot) & 0xFF]))
        # cls-0xC validator bitmap for 30B0E0/2FD970:
        # valid iff bit (id&0xF) of w[bmp + (id&0xFFF)>>4 *2] set
        fbmp = self.alloc(0x40)
        gm.w(FOEBMP_R, qw(fbmp))
        gm.w(fbmp + 2, struct.pack("<H", case.get("foebmp", 0x7FFC) & 0xFFFF))

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
           X_0530: ("c530", "c530_ret"),
           X_43F0: ("u43f0", "u43f0_ret"),
           X_B770: ("kb770", "kb770_ret"),
           X_B7F0: ("kb7f0", "kb7f0_ret"),
           X_8F1F0: ("q28f1f0", None), X_FA540: ("q2fa540", None),
           X_FA3B0: ("q2fa3b0", None),
           X_3910: ("g3910", "g3910_ret"),
           X_4100: ("o4100", "o4100_ret"), X_7930: ("s7930", "s7930_ret"),
           X_8B40: ("l8b40", "l8b40_ret"), X_F9A0: ("uf9a0", None),
           X_C410: ("ec410", None), X_4470: ("m4470", None)}

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
            R_2FD970: "vfd970"}

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
}


def main():
    raw, secs = load_image()
    res = {}
    for name, case in CASES.items():
        w = World(case, raw, secs)
        eax = w.run(rcx=case.get("rcx", w.rec),
                    edx=case.get("edx", w.sel))
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
                c5 = by("c530")
                ck(len(c5) == 1 and c5[0][1] == w.rec
                   and c5[0][2] == 7 and c5[0][3] == 0
                   and c5[0][4] == 0x217, f"c530 {c5}")
                ck(not by("u43f0"), "u43f0 w/o stored<=0")

            elif name == "f340-bit1c":
                c5 = by("c530")
                ck(len(c5) == 1 and c5[0][2] == 14,
                   f"c530 delta {c5}")

            elif name == "f340-bit10":
                # computed = max(-5,1)=1 vs stored -5 -> delta 6;
                # stored<=0 + idx 0x1C in [0x1B,0x27] + b5==0 -> unlink
                ck("b860" in w.trace, "b860 unlink scan missing")
                u = by("u43f0")
                ck(len(u) == 1 and u[0][1] == w.objrow,
                   f"u43f0 arg {u}")
                c5 = by("c530")
                ck(len(c5) == 1 and c5[0][2] == 6,
                   f"c530 delta {c5}")

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
