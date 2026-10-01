# spawn-init: 0023AC80 with the REAL callee layer — runtime validation
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

# ---- scripted boundaries ----
X_C650 = 0x0030C650        # level-set (EXP-148 proven)
X_FED0 = 0x0030FED0        # recompute (EXP-148 proven)
X_F690 = 0x0030F690        # stat cluster
X_F340 = 0x0030F340
X_F5A0 = 0x0030F5A0
X_3910 = 0x00323910        # deep grant
X_4100 = 0x00324100        # b[+0x20] override (->324020)
X_7930 = 0x00317930        # slot search
X_8B40 = 0x00318B40        # list op
X_F9A0 = 0x0030F9A0        # unequip (r9d path, never from ac80)
X_C410 = 0x0030C410        # equip   (r9d path)
X_B860 = 0x0031B860        # member block (r9d path)
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
F693B   = 0x0208D324       # gate dword B

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
        gm.w(F693B, dw(0))

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
           X_F690: ("f690", "f690_ret"), X_F340: ("f340", "f340_ret"),
           X_F5A0: ("f5a0", "f5a0_ret"), X_3910: ("g3910", "g3910_ret"),
           X_4100: ("o4100", "o4100_ret"), X_7930: ("s7930", "s7930_ret"),
           X_8B40: ("l8b40", "l8b40_ret"), X_F9A0: ("uf9a0", None),
           X_C410: ("ec410", None), X_B860: ("mb860", "b860_ret"),
           X_4470: ("m4470", None)}

    REAL = {F_AC80: "ac80", R_E600: "e600", R_C470: "c470",
            R_A630: "a630", R_3790: "g3790", R_7CB0: "p7cb0",
            R_6030: "c6030", R_7DE0: "o7de0", R_2C50: "v2c50",
            R_8F20: "f8f20"}

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
        self.entry = F_AC80
        rsp = STACK + 0x80000
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, edx & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(F_AC80, RETQ, timeout=60_000_000)
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
    # 30C470's 30F690 gate: d[0208D320]|d[0208D324] != 0
    "ac80-foe-f690gate": base_case(f690_gate=1),
}


def main():
    raw, secs = load_image()
    res = {}
    for name, case in CASES.items():
        w = World(case, raw, secs)
        eax = w.run(rcx=w.rec, edx=w.sel)
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
                # scripted call sequence spot checks
                seq = [c[0] for c in w.rets.get("calls", [])]
                ck("c650" in seq and "fed0" in seq, "c650/fed0")
                ck("f340" in seq and "f5a0" in seq, "f340/f5a0")
                if case.get("f690_gate"):
                    ck("f690" in seq, "f690 gate")
                else:
                    ck("f690" not in seq, "f690 ran w/o gate")

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
