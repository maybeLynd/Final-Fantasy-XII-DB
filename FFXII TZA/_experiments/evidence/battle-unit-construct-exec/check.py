# battle-unit-construction: installer 0023A570 with the REAL callee
# layer — runtime validation for CONTRACT-battle-unit-construction.md.
# EXP-075 ran the installer with nine no-op stubs (reset/rekey/resolver/
# spawn/text/tracked/engaged/hp) and manually initialized the unit; this
# harness executes the shipped bytes for every callee whose surface is
# closed under the fixture.
#
#   0023A570 (0x710): rcx=unit, edx=selector — dl=def index (r12d),
#     dh=mode (esi): 0=foe path, 1=member path, >=2 clears bit42 and
#     returns 0. Entry: ebx = b[unit]&4 ? w[q[unit+0x698]+4] : 0xFFFF
#     (old member kind, read BEFORE reset clears +0x698).
#     Flow: 236A60 reset; d[02089300] master gate; 303EC0/30D9A0 select
#     (mode byte d[q[02EBF190]+0x5B04]); 304630/3271D0 old-class
#     compare; rekey gate is b[rsp+0x89] = spilled arg2 byte1 == esi,
#     so esi!=0 ALWAYS rekeys; esi==0 rekeys iff old kind differs.
#     member path requires bt q[unit],0x1A; def row rsi = 20E600(d[
#     defdesc+0xC]) + w[defdesc+8]*idx; guards: w[def] <= member count-1,
#     w[def+0x50] <= w[orderdesc]-1 (SIGNED jg — null order desc
#     rejects), w[def+0x22]/+0x24 <= count-1 (unsigned ja — null reward
#     descs pass and store 0). Text chain: w[def+8] = poolidx<<11|idx,
#     two-level d[+4+4i] arrays -> 20E600 -> 2B58B0(blob,0). Spawn:
#     236100(movsx b[unit+0x57], q[unit+0x40]) -> spawnbase+id*0x250;
#     b[spawn]&5==0 -> 23AC80 init (scripted); w[def+0x32/34/36]!=0xFFFF
#     -> b[spawn+0x14] bits0-2; b[def+2]!=0xFF -> tracked counter
#     w[02089340+((b[0208D454]<<6)+slot)*2+0x4014] wrap-increment vs
#     254A40()==0x34, old count -> b[spawn+0x12]. Tail: f[+0x64]=
#     b[memb+0x22]*6.2832/360, f[+0x6C]=b[memb+0x27]*1.5, f[+0x68]=
#     float(b[memb+0x23]), b[+0x55]=b[memb+4], b[+0x56]=b[memb+5],
#     w[+0x52]=w[memb+6], b[+0x54]=0xFF, d[+0x48]=0, q[+0xE60]=def,
#     q[+0xE68]=memb, q[+0x698]=spawn+0x80, q[+0x6A0]=spawn,
#     q[+0x18]=text, q[+0xE70]/+0xE78 reward rows; 328FF0 tracked-kind
#     (writes only when edx kind != 0 or r8d < 0);
#     b[def+3]&3 || b[def+0x15]&4 -> bit43; 237040 engaged (308010 ->
#     REAL arms 2FED60 sets bit23 / 2FEDC0 clears bit23 + d4 mask, both
#     d[+0xDCC]=0, q[+0x6E8] = 0x1EEC3C0/0x1EEC410 by b[q[+0x698]+5],
#     tail 2ECF10); 2FEAB0 real; KO check reads
#     spawn+0x80 (+0x64|+0x3C & 0x80000003) -> 313F60 (real) -> 77C20
#     (scripted) -> on can-die==0: q[0] &= ~bit42, |=2; always |=4.
#     foe path (esi==0): 322C50(2,idx,1) = 0<=idx<=d[q[02EBF130]+4]-1;
#     def via 02EBF130; r15 = q[02EBF190]+8+idx*0x1C8; text ref w[def+
#     0x30]; q[+0x6E0]=02089378+idx*0x170; q[+0x6F0]=0x1E09350;
#     q[+0x698]=r15, q[+0x6A0]=0 (no spawn), b[+0x55]=b[+0x56]=0xFF,
#     w[+0x52]=0xFFFF, f[+0x64]=6.2832 const, f[+0x6C]=b[def+0x2B]*1.5,
#     f[+0x68]=float(b[def+0x2B]); no tracked/spawn work.
#
#   00236A60 reset (0x1C0, executed for real): conditional 3105D0 on
#     b[unit]&0x10; clears/masks: w[+0x695]=0xFFFF, b[+0x694]=0xFF,
#     d[+4]&=0xFFEFFFBB, q[0]&=0xFFFF7FFDFFE7FFFD then d[0]&=0xFFFFB0E3,
#     q[+0x698/+0xE60/+0xE68/+0x6A0/+0x2C/+0x24]=0, b[+0xEA8]=0,
#     d[+0xEA4/+0xE54/+0xDD0]=0, d[+0x74]=-1, q[+0x5C]=0, w[+0xDC8]=0xFFFF,
#     316D30(+0xBC0): memset 0x208 preserving bit0, w[+0xBC1]=0;
#     320450: d[+0x70]=0 (KO gate unreachable — +0x698 already cleared);
#     d[+0xE90]=0, q[+0xE80/+0xE88]=0, w[+0x55]=0xFFFF, w[+0x52]=0,
#     b[+0x54]=0xFF, q[+0x64]=0, d[+0x6C]=0, q[+0x708]=0, d[+0x710]=0,
#     w[+0x714]=0xFFFF, xmm[+0x700]->+0x730/+0x718, sd[+0x710]->+0x740/
#     +0x728, q[+0x76C/+0x764]=0, d[+0x760]=0, b[+0x6B0/+0x6B5]=0,
#     d[+0x6D0]=0, q[+0x6F8/+0x6F0/+0x6E8/+0x6E0]=0, q[+0x750/+0x748]=0,
#     w[+0x758]=0xFFFF, d[+0xB90]=0, d[+0x774]=-1, memset(+0x80,0,0x610),
#     3839C0(+0x200): w[+0x20C/+0x20E]=0xFFFF, 3839F0(+0x200):
#     b[+0x210..0x28F]=0xFF, 3176C0: rep-stosd 0x80B at +0xDD4.
#
#   00322050 rekey (0x2C, real): d[+0xEA4]=0, b[+0xEA8]=0,
#     d[+8] = 3220E0(q[+0x10]) — inner resolver scripted.
#
#   REAL (shipped bytes): 0023A570, 00236A60, 00316D30, 00320450,
#     003839F0, 003839C0, 003176C0, 00303EC0, 0030D9A0, 00304630,
#     00322050, 0020E600, 00236100, 002B58B0, 00328FF0, 00237040,
#     002FED60, 002FEDC0, 002ECF10, 002FEAB0, 00254A40, 00313F60,
#     00322C50 (+cls-2 arm), 00861EC0 (memset hook).
#
#   Scripted boundaries (entry-intercepted, args recorded, disclosed):
#     00377C20 can-die (called from inside real 00313F60; the
#       d[q[02EBF190]+0x5B04] mode byte exercises the real 30D9A0
#       ordering around it), 003271D0 class getter,
#     00308010 engaged predicate, 003220E0 rekey inner, 003105D0
#     reset's bit4 helper, 0023AC80 spawn-record init (249-ins —
#     separate package-sized surface).
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

# ---- subjects ----
F_INST  = 0x0023A570       # the installer
F_RESET = 0x00236A60       # the reset
F_REKEY = 0x00322050
S_16D30 = 0x00316D30
S_20450 = 0x00320450
S_839F0 = 0x003839F0
S_839C0 = 0x003839C0
S_176C0 = 0x003176C0
S_03EC0 = 0x00303EC0
S_0D9A0 = 0x0030D9A0
S_04630 = 0x00304630
S_0E600 = 0x0020E600
S_36100 = 0x00236100
S_B58B0 = 0x002B58B0
S_28FF0 = 0x00328FF0
S_37040 = 0x00237040
S_FEAB0 = 0x002FEAB0
S_54A40 = 0x00254A40
S_13F60 = 0x00313F60
S_22C50 = 0x00322C50
S_61EC0 = 0x00861EC0       # memset

# ---- scripted boundaries ----
X_77C20 = 0x00377C20       # can-die
X_71D0  = 0x003271D0       # class getter (304630's callee)
X_08010 = 0x00308010       # engaged predicate
X_ED60  = 0x002FED60       # engaged arm (308010 != 0): sets bit23
X_EDC0  = 0x002FEDC0       # not-engaged arm (== 0): clears bit23
X_CF10  = 0x002ECF10       # engaged tail (early-ret on null chain)
X_220E0 = 0x003220E0       # rekey inner resolver
X_105D0 = 0x003105D0       # reset's bit4 helper
X_3AC80 = 0x0023AC80       # spawn-record init

# ---- globals / fixture cells ----
ENABLE  = 0x02089300       # master enable dword
CTX     = 0x02EBF190       # shared context object cell
DEFD    = 0x02EBF120       # member-def descriptor
MEMD    = 0x02EBF150       # member-record descriptor
ORDD    = 0x02EBF168       # order descriptor (w[+0]=count, d[+4+4i])
BASED   = 0x02EBF148       # base-reward descriptor
LEVELD  = 0x02EBF140       # level-reward descriptor
POOLD   = 0x02EBF170       # text-pool descriptor
FOED    = 0x02EBF130       # foe-def descriptor (esi==0 + cls-2 bound)
ELEMB   = 0x01F83530       # 20E600's element-base cell
SPAWNB  = 0x0208E690       # 236100's spawn-table base cell
TRACKT  = 0x02089340       # tracked-count table (+0x4014 words)
TRACKC  = 0x0208D454       # tracked class byte (<<6 row select)
FOEORD  = 0x02089378       # foe order table (+idx*0x170)
FOEVTAB = 0x01E09350       # foe vtable constant
BIT42   = 1 << 42
BIT43   = 1 << 43

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


# elemb sub-block offsets — desc "off"/d-array values index into elemb
O_DEF   = 0x00000          # member-def rows, stride 0x60
O_MEMB  = 0x10000          # member records, stride 0x60
O_ORDER = 0x20000          # order target rows
O_BASE  = 0x30000          # base-reward rows, stride 0x38
O_LEVEL = 0x40000          # level-reward rows, stride 0x38
O_POOL  = 0x50000          # pool base: d[+4+4i] = blob offsets
O_BLOB  = 0x60000          # text blob (b[0]!=0 -> 2B58B0 returns blob)
O_FOE   = 0x80000          # foe-def rows, stride 0x60


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.uc.mem_map(STACK, 0x100000)
        self.uc.mem_map(RETQ, 0x1000)
        self.uc.mem_map(HEAP, 0x400000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP
        self.entry = 0
        gm = self.gm

        self.gm.w(ELEMB, qw(self.alloc(0x90000)))
        self.elemb = self.gm.q(ELEMB)
        self.ctx = self.alloc(0x8000)
        self.gm.w(CTX, qw(self.ctx))
        self.gm.w(self.ctx + 0x5B04, dw(case.get("mode", 0)))

        def mkdesc(cell, spec, count16=False):
            if spec is None:
                self.gm.w(cell, qw(0))
                return 0
            desc = self.alloc(0x60)
            self.gm.w(cell, qw(desc))
            if count16:
                self.gm.w(desc, struct.pack("<H", spec.get("count", 0)))
            else:
                self.gm.w(desc + 4, dw(spec.get("count", 0)))
            self.gm.w(desc + 8, struct.pack("<H",
                                            spec.get("stride", 0) & 0xFFFF))
            self.gm.w(desc + 0xC, dw(spec.get("off", 0)))
            for i, e in enumerate(spec.get("elems", [])):
                self.gm.w(desc + 4 + i * 4, dw(e))
            return desc

        self.defdesc = mkdesc(DEFD, case.get("defd",
            {"count": 8, "stride": 0x60, "off": O_DEF}))
        self.memdesc = mkdesc(MEMD, case.get("memd",
            {"count": 8, "stride": 0x60, "off": O_MEMB}))
        self.orddesc = mkdesc(ORDD, case.get("ordd",
            {"count": 4, "elems": [O_ORDER, O_ORDER + 0x20,
                                   O_ORDER + 0x40, O_ORDER + 0x60]}),
                              count16=True)
        self.based = mkdesc(BASED, case.get("based",
            {"count": 3, "stride": 0x38, "off": O_BASE}))
        self.leveld = mkdesc(LEVELD, case.get("leveld",
            {"count": 3, "stride": 0x38, "off": O_LEVEL}))
        self.poold = mkdesc(POOLD, case.get("poold",
            {"stride": 0, "elems": [O_POOL]}))
        self.foed = mkdesc(FOED, case.get("foed",
            {"count": 8, "stride": 0x60, "off": O_FOE}))
        # pool base d-array -> blob offsets; poold.elems[0] = O_POOL
        self.gm.w(self.elemb + O_POOL + 4, dw(O_BLOB))
        self.gm.w(self.elemb + O_POOL + 8, dw(O_BLOB + 0x40))
        for off, s in ((O_BLOB, b"leader\x00"),
                       (O_BLOB + 0x40, b"foe-name\x00")):
            self.gm.w(self.elemb + off, s)

        self.gm.w(ENABLE, dw(case.get("enable", 1)))
        self.spawnbase = self.alloc(0x8000)
        self.gm.w(SPAWNB, qw(self.spawnbase))
        self.gm.w(TRACKC, bytes([case.get("track_cls", 0) & 0xFF]))
        self.gm.w(TRACKT + 0x4014 +
                  ((case.get("track_cls", 0) << 6) +
                   case.get("track_slot", 0)) * 2,
                  struct.pack("<H", case.get("track_old", 0) & 0xFFFF))

        self.unit = self.alloc(0x1000)
        self.oldmemb = self.alloc(0x100)
        self.wrapper = self.alloc(0x100)
        self.spawnlist = self.alloc(0x100)
        self.spawn = self.spawnbase + case.get("spawn_id", 1) * 0x250

        u = case.get("unit", {})
        if case.get("sentinel_unit"):
            self.gm.w(self.unit, b"\xA5" * 0x1000)
        self.gm.w(self.unit, qw(u.get("q0", 0)))
        self.gm.w(self.unit + 4, dw(u.get("d4", 0)))
        self.gm.w(self.unit + 0x10, qw(u.get("q10", self.wrapper)))
        self.gm.w(self.unit + 0x40, qw(u.get("q40", self.spawnlist)))
        self.gm.w(self.unit + 0x57, bytes([u.get("b57", 0) & 0xFF]))
        self.gm.w(self.unit + 0xEA9, bytes([u.get("ea9", 0x27) & 0xFF]))
        if u.get("oldmemb"):
            self.gm.w(self.unit + 0x698, qw(self.oldmemb))
        self.gm.w(self.oldmemb + 4,
                  struct.pack("<H", case.get("old_kind", 0xFFFF) & 0xFFFF))
        sl = case.get("spawnlist", [1, case.get("spawn_id", 1)])
        for i, v in enumerate(sl):
            self.gm.w(self.spawnlist + i, bytes([v & 0xFF]))
        self.gm.w(self.spawn, bytes([case.get("spawn_b0", 1) & 0xFF]))
        for a, v in case.get("spawnv", {}).items():
            self.gm.w(self.spawn + a, bytes([v & 0xFF]))

        self.defrow = self.elemb + O_DEF + case.get("idx", 0) * 0x60
        self.plant_row(self.defrow, case.get("def", {}))
        self.memb = self.elemb + O_MEMB + \
            case.get("def", {}).get("w", {}).get(0, 0) * 0x60
        self.plant_row(self.memb, case.get("memb", {}))
        self.foerow = self.elemb + O_FOE + case.get("idx", 0) * 0x60
        self.plant_row(self.foerow, case.get("foe", {}))
        self.foem = self.ctx + 8 + case.get("idx", 0) * 0x1C8
        self.plant_row(self.foem, case.get("foem", {}))

        for a, blob in case.get("patch", {}).items():
            self.gm.w(a, bytes(blob))

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def plant_row(self, base, r):
        gm = self.gm
        for off, v in r.get("b", {}).items():
            gm.w(base + off, bytes([v & 0xFF]))
        for off, v in r.get("w", {}).items():
            gm.w(base + off, struct.pack("<H", v & 0xFFFF))
        for off, v in r.get("d", {}).items():
            gm.w(base + off, dw(v))
        for off, v in r.get("q", {}).items():
            gm.w(base + off, qw(v))

    def alloc(self, n):
        a = self.hb
        self.hb += (n + 0xFFF) & ~0xFFF
        return a

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    def _args(self, tag):
        uc = self.uc
        rsp = uc.reg_read(UC_X86_REG_RSP)
        self.rets.setdefault("calls", []).append(
            [tag, uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFFFFFFFFFF,
             uc.reg_read(UC_X86_REG_R9) & 0xFFFFFFFFFFFFFFFF,
             self.gm.d(rsp + 0x28), self.gm.d(rsp + 0x30)])
        self.trace.append(tag)

    SCR = {X_77C20: ("77c20", "77c20_ret"),
           X_71D0: ("71d0", "71d0_ret"),
           X_08010: ("08010", "08010_ret"),
           X_220E0: ("220e0", "220e0_ret"),
           X_105D0: ("105d0", None),
           X_3AC80: ("3ac80", None)}

    # installer callsites into real subjects — args recorded at the call
    CALLSITES = {0x23A5B0: "reset", 0x23A5CD: "select",
                 0x23A5D6: "class_a", 0x23A5E2: "class_b",
                 0x23A60A: "rekey", 0x23A776: "getspawn",
                 0x23A7A9: "spawninit", 0x23A814: "cap54a40",
                 0x23A8E1: "text", 0x23AB5A: "text_foe",
                 0x23AA04: "tracked", 0x23AA59: "validate",
                 0x23AC1C: "engaged", 0x23AC24: "hp",
                 0x23AC42: "ko_gate"}

    REAL = {S_0E600: "e600", S_B58B0: "b58b0", S_36100: "gspawn",
            S_28FF0: "trk28ff0", S_37040: "eng37040", S_FEAB0: "hp_feab0",
            S_54A40: "cap_real", S_13F60: "ko313f60", S_22C50: "val22c50",
            S_03EC0: "sel303ec0", S_0D9A0: "sel30d9a0",
            S_04630: "cls304630", F_REKEY: "rekey_real",
            S_16D30: "h16d30", S_20450: "h20450", S_839F0: "h3839f0",
            S_839C0: "h3839c0", S_176C0: "h3176c0",
            X_ED60: "eng_hi", X_EDC0: "eng_lo", X_CF10: "eng_tail"}

    def on_code(self, uc, addr, size, _):
        if addr == self.entry:
            return
        cs = self.CALLSITES.get(addr)
        if cs is not None and self.entry == F_INST:
            self._args(cs)
            return
        if addr == S_61EC0:      # memset(rcx, dl, r8)
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
                             self.case.get(retkey, 0) & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        t = self.REAL.get(addr)
        if t is not None:
            self.trace.append(t)
            if addr == S_0E600:
                self.rets.setdefault("e600_args", []).append(
                    uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF)
            elif addr == S_22C50:
                self.rets.setdefault("v_calls", []).append(
                    [uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                     uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF,
                     uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF])
            return
        if addr == F_RESET and self.entry != F_RESET:
            self.trace.append("reset_real")

    def run(self, entry, rcx=0, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.entry = entry
        rsp = STACK + 0x80000
        self.gm.w(rsp - 0x800, b"\xCD" * 0x800)
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R8, r8 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9, r9 & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, timeout=120_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


# ------------------------------------------------------------------
def member_case(**kw):
    c = {"idx": 0, "sel": 0x100,
         "unit": {"q0": (1 << 26), "b57": 0, "ea9": 0x27},
         "def": {"w": {0: 0, 0x22: 1, 0x24: 2, 0x50: 0,
                       0x32: 0xFFFF, 0x34: 0xFFFF, 0x36: 0xFFFF},
                 "b": {2: 0xFF, 3: 0, 0x15: 0}},
         "memb": {"b": {4: 2, 5: 1, 0x22: 90, 0x23: 7, 0x27: 30},
                  "w": {6: 0x1234}},
         "220e0_ret": 0x1234}
    for k, v in kw.items():
        if k in ("unit", "def", "memb", "foe", "foem", "spawnv"):
            c.setdefault(k, {})
            for kk, vv in v.items():
                c[k].setdefault(kk, {}).update(vv) \
                    if isinstance(vv, dict) else c[k].update({kk: vv})
        else:
            c[k] = v
    return c


CASES = {
    # ---- direct reset cases (entry = 236A60) ----
    "rs-plain": {"entry": "reset", "sentinel_unit": 1,
                 "unit": {"q0": (1 << 26) | 0xA5, "d4": 0xA5A5A5A5,
                          "ea9": 0xA5}},
    "rs-b10":   {"entry": "reset", "sentinel_unit": 1,
                 "unit": {"q0": (1 << 26) | 0xA5 | 0x10,
                          "d4": 0xA5A5A5A5, "ea9": 0xA5}},
    "rs-mask":  {"entry": "reset", "sentinel_unit": 1,
                 "unit": {"q0": 0xFFFFFFFFFFFFFFFF, "d4": 0xFFFFFFFF,
                          "ea9": 0xA5}},

    # ---- installer: member path (esi=1) ----
    "in-member": member_case(),
    # EXP-075's guard matrix under real callees
    "in-base-eq":  member_case(**{
        "def": {"w": {0x22: 2}},
        "based": {"count": 2, "stride": 0x38, "off": O_BASE}}),
    "in-level-eq": member_case(**{
        "def": {"w": {0x24: 3}},
        "leveld": {"count": 3, "stride": 0x38, "off": O_LEVEL}}),
    "in-both-bad": member_case(**{
        "def": {"w": {0x22: 2, 0x24: 3}},
        "based": {"count": 2, "stride": 0x38, "off": O_BASE},
        "leveld": {"count": 3, "stride": 0x38, "off": O_LEVEL}}),
    "in-base-ffff-bad": member_case(**{
        "def": {"w": {0x22: 0xFFFF}},
        "based": {"count": 0xFFFF, "stride": 0x38, "off": O_BASE}}),
    "in-base-ffff-ok": member_case(**{
        "def": {"w": {0x22: 0xFFFF}},
        "based": {"count": 0x10000, "stride": 0x38, "off": O_BASE}}),
    "in-level-ffff-bad": member_case(**{
        "def": {"w": {0x24: 0xFFFF}},
        "leveld": {"count": 0xFFFF, "stride": 0x38, "off": O_LEVEL}}),
    "in-level-ffff-ok": member_case(**{
        "def": {"w": {0x24: 0xFFFF}},
        "leveld": {"count": 0x10000, "stride": 0x38, "off": O_LEVEL}}),
    # count==0 -> count-1 wraps to 0xFFFFFFFF -> ja never fires; the
    # guard accepts every index (underflow semantics, real execution)
    "in-base-zero": member_case(**{
        "ret": 1,
        "def": {"w": {0x22: 0xFFFF}},
        "based": {"count": 0, "stride": 0x38, "off": O_BASE}}),
    "in-level-zero": member_case(**{
        "ret": 1,
        "def": {"w": {0x24: 0xFFFF}},
        "leveld": {"count": 0, "stride": 0x38, "off": O_LEVEL}}),
    # null reward descs: unsigned count-1 underflow -> guard PASSES,
    # row pointer stores 0 (EXP-075's null-table semantics, now real)
    "in-base-null": member_case(**{
        "def": {"w": {0x22: 0xFFFF}}, "based": None}),
    "in-level-null": member_case(**{
        "def": {"w": {0x24: 0xFFFF}}, "leveld": None}),
    # order guard is SIGNED jg on w[desc+0] count: null order desc ->
    # count16 read fails -> ecx=0 -> dec -> -1 -> w50(0) > -1 -> reject
    "in-order-null": member_case(**{"ordd": None}),
    "in-order-oob": member_case(**{
        "def": {"w": {0x50: 7}},
        "ordd": {"count": 4, "elems": [O_ORDER] * 4}}),
    "in-def-oob": member_case(**{
        "idx": 7, "sel": 0x107,
        "defd": {"count": 4, "stride": 0x60, "off": O_DEF}}),
    "in-mem-oob": member_case(**{
        "def": {"w": {0: 9}},
        "memd": {"count": 8, "stride": 0x60, "off": O_MEMB}}),
    "in-enable-off": member_case(**{"enable": 0}),
    "in-nobit26": member_case(**{"unit": {"q0": 0}}),
    "in-mode2": member_case(**{"sel": 0x200}),
    "in-spawn-bad": member_case(**{"unit": {"b57": 0xFE}}),
    "in-spawn-init": member_case(**{"spawn_b0": 0}),
    # the spawn-flag/tracked block sits inside the fresh-spawn arm
    # (b[spawn]&5 == 0); already-initialized spawns skip it entirely
    "in-tracked": member_case(**{
        "spawn_b0": 0,
        "def": {"b": {2: 5}},
        "track_slot": 5, "track_old": 0x10}),
    "in-tracked-cap": member_case(**{
        "spawn_b0": 0,
        "def": {"b": {2: 5}},
        "track_slot": 5, "track_old": 0x34}),
    "in-bit43": member_case(**{"def": {"b": {3: 1}}}),
    "in-bit43b": member_case(**{"def": {"b": {0x15: 4}}}),
    "in-ko": member_case(**{"spawnv": {0xE4: 0x01}, "77c20_ret": 0}),
    "in-ko-cantdie": member_case(**{"spawnv": {0xE4: 0x01},
                                    "77c20_ret": 1}),
    "in-engaged": member_case(**{"08010_ret": 1}),
    # rekey fires unconditionally on esi==1 (b[rsp+0x89] = arg byte1);
    # esi==0 with matching old kind skips it — needs bit2 + oldmemb
    "in-foe": {"idx": 0, "sel": 0,
               "unit": {"q0": 0, "b57": 0},
               "foe": {"w": {0x30: (0 << 11) | 1},
                       "b": {3: 0, 0x15: 0, 0x2B: 45}},
               "foem": {},
               "foed": {"count": 8, "stride": 0x60, "off": O_FOE}},
    "in-foe-badcls": {"idx": 9, "sel": 9,
                      "unit": {"q0": 0},
                      "foed": {"count": 8, "stride": 0x60,
                               "off": O_FOE}},
    "in-foe-rekey": {"idx": 0, "sel": 0,
                     "unit": {"q0": (1 << 2), "b57": 0, "oldmemb": 1},
                     "old_kind": 0x77,
                     "foe": {"w": {0x30: 1}, "b": {0x2B: 45}},
                     "foed": {"count": 8, "stride": 0x60,
                              "off": O_FOE},
                     "220e0_ret": 0x555},
    # select()==1 (mode byte = 2) + class equal + arg==0xFFFF -> skip
    "in-select-eq": {"idx": 0xFF, "sel": 0xFFFF, "mode": 2,
                     "unit": {"q0": (1 << 2), "b57": 0, "oldmemb": 1},
                     "old_kind": 0x77, "71d0_ret": 0x77,
                     "defd": {"count": 0x200, "stride": 0x60,
                              "off": O_DEF}},
    # spawn flag words != 0xFFFF set bits in b[spawn+0x14]; the whole
    # block only runs on a fresh spawn (b[spawn]&5 == 0)
    "in-spawnflags": member_case(**{
        "spawn_b0": 0, "ret": 1,
        "def": {"w": {0x32: 1, 0x34: 0xFFFF, 0x36: 7}}}),
    # ---- mutants (private per-World image patch) ----
    "mu-base-ja-jb": member_case(**{
        "ret": 1,
        "def": {"w": {0x22: 3}},   # count-1 boundary: JA rejects, JB
        "based": {"count": 3, "stride": 0x38, "off": O_BASE},
        "patch": {0x23A747: b"\x0f\x82"}}),
    "mu-level-ja-jb": member_case(**{
        "ret": 1,
        "def": {"w": {0x24: 3}},
        "leveld": {"count": 3, "stride": 0x38, "off": O_LEVEL},
        "patch": {0x23A768: b"\x0f\x82"}}),
    "mu-order-jg-jle": member_case(**{
        "ret": 1,
        "def": {"w": {0x50: 4}},
        "ordd": {"count": 4, "elems": [O_ORDER] * 4},
        "patch": {0x23A726: b"\x0f\x8e"}}),
}


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    gm = w.gm
    if case.get("entry") == "reset":
        out["ret"] = w.run(F_RESET, rcx=w.unit)
    else:
        out["ret"] = w.run(F_INST, rcx=w.unit, rdx=case.get("sel", 0))
    u = w.unit
    out["unit"] = {
        "q0": gm.q(u), "d4": gm.d(u + 4), "d8": gm.d(u + 8),
        "q10": gm.q(u + 0x10), "q18": gm.q(u + 0x18), "q24": gm.q(u + 0x24),
        "q2c": gm.q(u + 0x2C), "d38": gm.d(u + 0x38), "d3c": gm.d(u + 0x3C),
        "w52": gm.w16(u + 0x52), "b54": gm.b(u + 0x54),
        "w55": gm.w16(u + 0x55), "b55": gm.b(u + 0x55),
        "b56": gm.b(u + 0x56), "q5c": gm.q(u + 0x5C),
        "f64": gm.f(u + 0x64), "f68": gm.f(u + 0x68), "f6c": gm.f(u + 0x6C),
        "d6c": gm.d(u + 0x6C), "d70": gm.d(u + 0x70), "d74": gm.d(u + 0x74),
        "q698": gm.q(u + 0x698), "b694": gm.b(u + 0x694),
        "w695": gm.w16(u + 0x695), "q6a0": gm.q(u + 0x6A0),
        "d48": gm.d(u + 0x48), "ddcc": gm.d(u + 0xDCC),
        "q6e8": gm.q(u + 0x6E8),
        "q6e0": gm.q(u + 0x6E0), "q6f0": gm.q(u + 0x6F0),
        "d710": gm.d(u + 0x710), "w714": gm.w16(u + 0x714),
        "w758": gm.w16(u + 0x758), "d760": gm.d(u + 0x760),
        "d774": gm.d(u + 0x774), "db90": gm.d(u + 0xB90),
        "wdc8": gm.w16(u + 0xDC8), "dd54": gm.d(u + 0xDD4),
        "de4f": gm.d(u + 0xE50), "de60": gm.q(u + 0xE60),
        "de68": gm.q(u + 0xE68), "de70": gm.q(u + 0xE70),
        "de78": gm.q(u + 0xE78), "de80": gm.q(u + 0xE80),
        "de90": gm.d(u + 0xE90), "dea4": gm.d(u + 0xEA4),
        "bea8": gm.b(u + 0xEA8), "qeac": gm.q(u + 0xEAC),
        "b210": gm.b(u + 0x210), "b28f": gm.b(u + 0x28F),
        "w20c": gm.w16(u + 0x20C), "w20e": gm.w16(u + 0x20E),
        "d100": gm.d(u + 0x100), "d680": gm.d(u + 0x680),
        "bc0": gm.b(u + 0xBC0), "bc1": gm.w16(u + 0xBC1),
        "bc2": gm.b(u + 0xBC2),
    }
    out["spawn"] = {"b12": gm.b(w.spawn + 0x12),
                    "b14": gm.b(w.spawn + 0x14),
                    "ko_d64": gm.d(w.spawn + 0x80 + 0x64),
                    "ko_d3c": gm.d(w.spawn + 0x80 + 0x3C)}
    out["track"] = gm.w16(TRACKT + 0x4014 +
                          ((case.get("track_cls", 0) << 6) +
                           case.get("track_slot", 0)) * 2)
    out["trktab"] = {"d0": gm.d(0x02E81380), "d4": gm.d(0x02E81384)}
    out.update(w.rets)
    out["ok"], out["fail"] = check(name, case, w, out)
    return out


def check(name, c, w, o):
    f = []
    tr = o["trace"]
    calls = o.get("calls", [])

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %s want %s" % (k, hex(got) if
                     isinstance(got, int) else got,
                     hex(want) if isinstance(want, int) else want))

    def eqf(k, got, want):
        if abs(got - want) > 1e-5:
            f.append("%s: got %r want %r" % (k, got, want))

    def called(tag):
        return [x for x in calls if x[0] == tag]

    def nreal(t):
        return tr.count(t)

    allow_fault = c.get("expect_fault")
    if o["faults"] and not allow_fault:
        f.append("faults: %s" % (o["faults"][:3],))
    if allow_fault and not o["faults"]:
        f.append("expected fault, none")

    u = o["unit"]
    # ---- reset direct cases ----
    if name.startswith("rs-"):
        # field clears
        for k, want in (("w695", 0xFFFF), ("b694", 0xFF), ("q698", 0),
                        ("de60", 0), ("de68", 0), ("q6a0", 0),
                        ("q2c", 0), ("q24", 0), ("bea8", 0),
                        ("dea4", 0), ("d74", 0xFFFFFFFF),
                        ("q5c", 0), ("wdc8", 0xFFFF), ("de90", 0),
                        ("de80", 0), ("w55", 0xFFFF), ("w52", 0),
                        ("b54", 0xFF), ("d710", 0), ("w714", 0xFFFF),
                        ("d760", 0), ("w758", 0xFFFF), ("db90", 0),
                        ("d774", 0xFFFFFFFF), ("dd54", 0),
                        ("de4f", 0), ("d70", 0), ("d6c", 0),
                        ("b210", 0xFF), ("b28f", 0xFF),
                        ("w20c", 0xFFFF), ("w20e", 0xFFFF),
                        ("d100", 0), ("d680", 0)):
            eq(k, u[k], want)
        # helper trace
        for t in ("h16d30", "h20450", "h3839f0", "h3839c0", "h3176c0"):
            if not nreal(t):
                f.append("missing %s" % t)
        ms = [m for m in o.get("memsets", [])]
        if not any(m[0] == w.unit + 0x80 and m[1] == 0x610 for m in ms):
            f.append("memsets: %s" % ms)
        if not any(m[0] == w.unit + 0xBC0 and m[1] == 0x208 for m in ms):
            f.append("bc0 memset: %s" % ms)
        # masks — observed combined mask on all-ones input (the reset's
        # exact bit-clear pattern, more extensive than the static read)
        if name == "rs-mask":
            eq("q0", u["q0"], 0xFFEF7FB9FFE7B0E1)
            eq("d4", u["d4"], 0xFFEF7FB9)
        # 3105D0 fires iff b[unit]&0x10 — rs-b10 sets it, rs-mask's
        # all-ones input does too; rs-plain must not call it
        want_105d0 = bool(c["unit"].get("q0", 0) & 0x10)
        if called("105d0") and not want_105d0:
            f.append("105d0 called without bit4")
        if want_105d0 and not called("105d0"):
            f.append("bit4 set but 3105D0 not called")
        # 316D30 preserves bit0 of b[unit+0xBC0]: sentinel 0xA5 bit0=1
        eq("bc0 bit0", u["bc0"] & 1, 1)
        eq("bc1", u["bc1"], 0)
        eq("bc2", u["bc2"], 0)
        return len(f) == 0, f

    # ---- installer cases ----
    expect_ret = c.get("ret", None)
    if expect_ret is None:
        # success expected for the positive paths
        expect_ret = 1 if name in (
            "in-member", "in-base-ffff-ok", "in-level-ffff-ok",
            "in-base-null", "in-level-null", "in-spawn-init",
            "in-tracked", "in-tracked-cap", "in-bit43", "in-bit43b",
            "in-ko", "in-ko-cantdie", "in-engaged", "in-foe",
            "in-foe-rekey", "mu-order-jg-jle") else 0
    eq("ret", o["ret"], expect_ret)

    # reset always ran first
    if not nreal("reset_real"):
        f.append("reset did not run")

    if name == "in-enable-off":
        # master gate aborts after reset — the reset callsite itself is
        # the only recorded call
        bad = [x for x in calls if x[0] != "reset"]
        if bad:
            f.append("enable-off still called: %s" % bad)
        return len(f) == 0, f

    if name == "in-member":
        sp = w.spawn
        eq("e60", u["de60"], w.defrow)
        eq("e68", u["de68"], w.memb)
        eq("q698", u["q698"], sp + 0x80)
        eq("q6a0", u["q6a0"], sp)
        eq("q18", u["q18"], w.elemb + O_BLOB)
        eq("q6e0", u["q6e0"], w.elemb + O_ORDER)
        eq("e70", u["de70"], w.elemb + O_BASE + 1 * 0x38)
        eq("e78", u["de78"], w.elemb + O_LEVEL + 2 * 0x38)
        eq("b55", u["b55"], 2)
        eq("b56", u["b56"], 1)
        eq("w52", u["w52"], 0x1234)
        eq("b54", u["b54"], 0xFF)
        eq("d48", u["d48"], 0)
        eq("qeac", u["qeac"], 0)
        eqf("f64", u["f64"], 90 * 6.2831855 / 360.0)
        eqf("f6c", u["f6c"], 30.0)      # member path: float(b27), no
        eqf("f68", u["f68"], 7.0)      #  x1.5 (that scale is foe-only)
        # exact 20E600 token sequence observed: def-base, member desc
        # gate+recompute x2, def-base x2 (text gate + resolve), pool
        # elem, def-base, string elem, order elem, base desc x2,
        # level desc x2
        eq("e600 seq", o.get("e600_args"),
           [0, 0, O_MEMB, O_MEMB, 0, 0, O_POOL, 0, O_BLOB, O_ORDER,
            O_BASE, O_BASE, O_LEVEL, O_LEVEL])
        # bit43 cleared (def b3=0, b15=0); bit2 set; bit26 kept
        eq("q0", u["q0"] & (BIT43 | BIT42 | (1 << 26) | 7),
           (1 << 26) | 4)
        # rekey ran (esi!=0): d[8] = 220e0_ret
        if not called("220e0"):
            f.append("no 220e0 inner call")
        eq("d8", u["d8"], 0x1234)
        eq("dea4", u["dea4"], 0)
        eq("bea8", u["bea8"], 0)
        # call order spot checks
        for tag in ("reset", "select", "rekey", "getspawn", "text",
                    "tracked", "engaged", "hp"):
            if not called(tag):
                f.append("no %s callsite" % tag)
        # tracked write: 328FF0(0, b[def+3]&3=0, r8d=b[u+0xEA9]=0x27)
        # 328FF0 only writes when kind(edx)!=0 or r8d<0; member b3=0
        # and ea9=0x27 -> the call runs real but stores nothing
        eq("trk d0", o["trktab"]["d0"], 0)
        eq("trk d4", o["trktab"]["d4"], 0)
        # engaged arms run REAL: 08010=0 -> 2FEDC0 clears bit23, zeroes
        # d[+0xDCC], selects vtable 0x1EEC3C0 (spawn+0x85 == 0)
        if not nreal("eng_lo"):
            f.append("no eng_lo arm")
        if nreal("eng_hi"):
            f.append("unexpected eng_hi")
        eq("ddcc", u["ddcc"], 0)
        eq("q6e8", u["q6e8"], 0x1EEC3C0)
        # spawn flag bytes: all w32/34/36=0xFFFF -> b14 stays 0
        eq("spawn b14", o["spawn"]["b14"], 0)
        eq("spawn b12", o["spawn"]["b12"], 0)
        # real-callee trace
        for t in ("e600", "b58b0", "gspawn", "trk28ff0", "eng37040",
                  "hp_feab0", "rekey_real", "sel303ec0"):
            if not nreal(t):
                f.append("missing real %s" % t)
        if nreal("val22c50"):
            f.append("member path hit cls validator")
        if nreal("cap_real"):
            f.append("b[def+2]==0xFF but 254A40 ran")
    elif name.startswith("in-base") or name.startswith("in-level") or \
            name == "in-both-bad" or name == "in-order-null" or \
            name == "in-order-oob" or name == "in-def-oob" or \
            name == "in-mem-oob":
        # guard semantics — reward row pointers iff success
        if name == "in-base-ffff-ok":
            eq("e70", u["de70"], w.elemb + O_BASE + 0xFFFF * 0x38)
        if name == "in-level-ffff-ok":
            eq("e78", u["de78"], w.elemb + O_LEVEL + 0xFFFF * 0x38)
        if name == "in-base-null":
            eq("e70", u["de70"], 0)
        if name == "in-level-null":
            eq("e78", u["de78"], 0)
    elif name == "in-nobit26" or name == "in-mode2":
        eq("q0 bit42", u["q0"] & BIT42, 0)
        if name == "in-mode2" and not called("rekey"):
            f.append("esi=2 should still rekey (arg byte1 != 0)")
    elif name == "in-spawn-bad":
        if not nreal("gspawn"):
            f.append("236100 not reached")
    elif name == "in-spawnflags":
        eq("spawn b14", o["spawn"]["b14"], 0x05)  # bits 0,2
    elif name == "in-spawn-init":
        sc = called("3ac80")
        if len(sc) != 1:
            f.append("3ac80 calls: %s" % sc)
        else:
            eq("3ac80.rcx", sc[0][1], w.spawn + 0x80)
            eq("3ac80.edx", sc[0][2], 0x100)
    elif name == "in-tracked" or name == "in-tracked-cap":
        old = c["track_old"]
        want = old + 1 if old < 0x34 else 1
        eq("track", o["track"], want)
        eq("spawn b12", o["spawn"]["b12"], old & 0xFF)
        if not nreal("cap_real"):
            f.append("254A40 not reached")
    elif name == "in-bit43" or name == "in-bit43b":
        eq("q0 bit43", u["q0"] & BIT43, BIT43)
    elif name == "in-ko" or name == "in-ko-cantdie":
        # KO bits planted at spawn+0x80+0x64 — the installer reads
        # q[unit+0x698]=spawn+0x80's +0x64|+0x3C
        if not called("ko_gate"):
            f.append("no 313F60 KO gate call")
        if not called("77c20"):
            f.append("77C20 not consulted")
        if name == "in-ko":
            eq("q0 bit1", u["q0"] & 2, 2)
            eq("q0 bit42", u["q0"] & BIT42, 0)
        else:
            eq("q0 bit1", u["q0"] & 2, 0)
        eq("q0 bit2", u["q0"] & 4, 4)
    elif name == "in-engaged":
        # 08010=1 -> real 2FED60 arm: sets d[unit] bit23, tail 2ECF10
        if not nreal("eng_hi"):
            f.append("08010=1 should take eng_hi")
        if nreal("eng_lo"):
            f.append("unexpected eng_lo")
        eq("q0 bit23", u["q0"] & 0x800000, 0x800000)
        eq("ddcc", u["ddcc"], 0)
    elif name == "in-foe":
        eq("e60", u["de60"], w.foerow)
        eq("q698", u["q698"], w.foem)
        eq("q6a0", u["q6a0"], 0)
        eq("q6e0", u["q6e0"], FOEORD + 0 * 0x170)
        eq("q6f0", u["q6f0"], FOEVTAB)
        eq("q18", u["q18"], w.elemb + O_BLOB + 0x40)
        eq("de68", u["de68"], 0)
        eq("b55", u["b55"], 0xFF)
        eq("b56", u["b56"], 0xFF)
        eq("w52", u["w52"], 0xFFFF)
        eqf("f64", u["f64"], 6.2831855)
        eqf("f6c", u["f6c"], 45 * 1.5)
        eqf("f68", u["f68"], 45.0)
        vc = o.get("v_calls", [])
        if vc != [[2, 0, 1]]:
            f.append("v_calls: %s" % vc)
        if nreal("gspawn"):
            f.append("foe path called getspawn")
        if nreal("trk28ff0"):
            f.append("foe path hit tracked write")
        # foe path: rekey decided by old-kind gate (ebx=0xFFFF -> skip)
        if called("rekey"):
            f.append("foe path rekeyed with ebx=0xFFFF")
    elif name == "in-foe-badcls":
        vc = o.get("v_calls", [])
        if vc != [[2, 9, 1]]:
            f.append("v_calls: %s" % vc)
    elif name == "in-foe-rekey":
        # esi==0, old kind 0x77 != arg 0 -> rekey fires
        if not called("rekey"):
            f.append("no rekey callsite")
        if not called("220e0"):
            f.append("no 220e0")
        eq("d8", u["d8"], 0x555)
    elif name == "in-select-eq":
        # select==1 (mode=2), 71d0==old kind, arg==0xFFFF -> gate skipped
        if not called("class_a"):
            f.append("no class compare")
        if called("rekey"):
            f.append("rekey should be skipped")
    elif name.startswith("mu-"):
        # mutants FLIP the guard outcome: boundary index that JA/JG
        # rejects must pass under JB/JLE
        eq("ret(mutant)", o["ret"], 1)

    return len(f) == 0, f


def main():
    raw, secs = load_image()
    out = {"cases": len(CASES), "pass": 0, "fail": 0, "results": {}}
    for name, case in CASES.items():
        try:
            r = run_case(name, case, raw, secs)
        except Exception as e:
            import traceback
            r = {"ok": False, "fail": ["exception: %r" % e],
                 "trace": [], "faults": [],
                 "tb": traceback.format_exc()}
        out["results"][name] = r
        if r["ok"]:
            out["pass"] += 1
        else:
            out["fail"] += 1
            print("%-20s FAIL %s" % (name, r["fail"]))
            if r["faults"]:
                print("   faults:", r["faults"][:3])
            print("   trace:", r["trace"][:60])
            print("   calls:", r.get("calls", [])[:20])
    out["ok"] = out["fail"] == 0
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("%d/%d pass" % (out["pass"], out["cases"]))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
