# apply-result-to-target: five undecoded callees — runtime validation for
# CONTRACT-apply-result-to-target.md. Executes on shipped bytes under
# Unicorn:
#
#   00316A50 (0x19A): field writer. cl=field index (<0x1E), edx=delta.
#     Per-field descriptor at 00D10460+f*8: b[+0] path-select,
#     b[+2] mode, d[+4] bound/expect. flag==0 path: mode 0 -> gate =
#     003165C0(f) if nonzero else d[+4]; delta < gate -> exit; else bts
#     into bitfield at 002536A0()+0x3844+f>>3 bit f&7, then
#     008632B0(d[00D20550+f*4]). mode 1 -> require delta==d[+4].
#     flag!=0 path: ebx=003166F0(f) (real: 2536A0 base + desc-driven
#     read); mode 0 -> dispatch on b[+0]: 2 clamps to 0x7FFF, 4 clamps
#     to 0x7FFFFFFF, else plain add; mode 3 -> bts ebx,delta-0xE2;
#     mode 8 -> exit; other -> write back unchanged. Write-back pair
#     00315E90(f) then 00316BF0(f, ebx) (both scripted boundaries).
#   0030C650 (0x239): level-set/growth. rcx=unit, edx=target level
#     (clamped 0x63), r8d=flags (bit1 suppresses the last-iter sync
#     flag). Loops level=b[unit+0x1C2] -> target: 0031B860(unit)->rec
#     (scripted); if b[unit+5]==0: double-hop q[02EBF130] descriptor ->
#     0020E600 element base, w[desc+8]*b[unit+4] stride -> growth rec;
#     002F9A60/002F9B20 (real, via q[02EBF108] desc) rewrite d[unit+8]
#     /w[unit+0xC]; four 002F9BD0 (real) adds fold growth bytes
#     b[growth+0x1F/0x22/0x25/0x28] into f[unit+0x10..0x1C].
#     b[unit+0x1C2]=min(cur+1,99). Last iter: 0030FED0(unit,0)
#     (scripted); then if sync-flag && b[unit+5]==0 -> 0046A690; then
#     if sync-flag && rec && b[q[rec+0x698]+5]==0 -> license-notify
#     chain 0035D8C0/002EACD0/003A1180/002DF220/00329210 (scripted).
#   003008A0 (0x2DD): item write. cx=item id. Rejects: 0xFFFF, 0x1000,
#     (id&0xF000)>0xE000 -> ret -1. Category desc at
#     01EEBCC0+(id>>12)*0x58; (id&0xFFF) > d[desc+0x3C]-1 -> -1.
#     00309F30(id, r9d) -> ebp (scripted); q[desc+0x48] callback
#     overrides (scripted). If r9d==1 && ebp<=0 && esi>0: category
#     switch: cat3 -> or d[q[02EBF190]+4],1 then record chain via
#     q[02EBF0F0] (rec = base + stride*(id-0x3000)) -> q[02EBF138] ->
#     b[rec+2]-indexed second record -> w[rec2+0x2C]&7 indexes flag
#     table 01EECF98 -> or d[q[02EBF190]+4],mask; cat4 -> or 0x40;
#     cat 0xC: id<=0xC011 -> or 0x80; 0xC012..0xC01E -> or 0x100.
#     Returns esi (callback/resolved value).
#   0030E130 (0x228): status-bit modifier. rcx=target, dl=bit (0..0x1D
#     validated by 00322C50 cls-0x1D, real), r8d, r9d=flags,
#     [rsp+0x28]=mode. Modes: 0 -> clear bit in b[tgt+bit>>3+0x68]
#     (require set); 1 -> clear +0x78 (require set); 2 -> set +0x68
#     (require clear); 3 -> set +0x78 (require clear). On change:
#     memset 0x148 struct (00861EC0 scripted -> real memset in hook),
#     notify thunk 00386A50/00386AE0 selected by (mode-2<=1),
#     if b[struct+0x2C]&1 -> 003112F0; if d[struct-0x10]!=0 ->
#     0046A720/0046A790; bit-idx in 0x68..0x71 -> 003279B0(tgt,
#     sel*2-1); r9d bit9 -> 0030FED0(tgt, r9d) (scripted).
#   0030FED0 (0x6FA): recompute. rcx=unit, edx=flags|0x202. b[unit+5]==0
#     -> double-hop q[02EBF130] -> rec; build 16B stack bitmap from
#     d[rec+0x50] (bits 0-31) and d[rec+0x54] (bits 32-63).
#     b[unit+5]==1 -> 0031B860 -> OR member b[rec+bit>>3+0xE80] bits
#     0..0x7F. Then 5 words at unit+0x50 each cls-6 validated
#     (00322C50 real, q[02EBF0F8] desc, range [0x1000,0x1000+count)):
#     rec -> 0031E9A0(rec)==3 && b[rec+0x1A]!=0xFF -> bts bitmap; plus
#     w[rec+0xA..0x16] !=0xFFFF -> bts bitmap (via q[02EBF038] desc
#     loop with 00323890==2 gate). Per-bit dispatch loop calls
#     0030E130 (scripted) set/clear. Tail: b[unit+0x40..0x44] copied to
#     q[r8+0x6A0]+0x78..; gated updates of d[unit+0x48], w[unit+0x4C],
#     w[unit+6]; 0030E060(unit, flags) (scripted).
#
#   Scripted boundaries (entry-intercepted, args recorded, disclosed):
#   0031B860, 003165C0, 00315E90, 00316BF0, 008632B0, 00309F30,
#   0030EA40, 003112F0, 003279B0, 00808C40 (canary check),
#   00386A50, 00386AE0, 0046A720, 0046A790, 0046A690, 0035D8C0,
#   002EACD0, 003A1180, 002DF220, 00329210, 0031E9A0, 00323890,
#   002FEF30, 0030E060, the q[desc+0x48] callback, and the cross-calls
#   0030FED0/0030E130/0030E360 when reached from another subject.
#   Real under emulation: 002536A0, 0020E600, 002F9A60, 002F9B20,
#   002F9BD0, 003166F0, 00322C50 (+cls arms), 00861EC0 (memset,
#   implemented in the hook).
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

# ---- subjects (all executed as shipped bytes) ----
F_16A50 = 0x00316A50       # field writer
F_C650  = 0x0030C650       # level-set / growth
F_08A0  = 0x003008A0       # item write
F_E130  = 0x0030E130       # status-bit modifier
F_FED0  = 0x0030FED0       # recompute
V_C50   = 0x00322C50       # class validator (real)

# ---- real helpers ----
S_36A0  = 0x002536A0       # -> q[020927C0]
S_E600  = 0x0020E600       # -> ecx + q[01FE3530]
S_9A60  = 0x002F9A60       # stat setter (HP-ish)
S_9B20  = 0x002F9B20       # stat setter (MP-ish)
S_9BD0  = 0x002F9BD0       # float growth add
S_166F0 = 0x003166F0       # field getter

# ---- scripted boundaries ----
X_B860  = 0x0031B860       # unit -> record
X_165C0 = 0x003165C0       # chain-walker getter
X_15E90 = 0x00315E90       # write-back pre
X_16BF0 = 0x00316BF0       # write-back
X_632B0 = 0x008632B0       # field notify
X_9F30  = 0x00309F30       # item resolver
X_EA40  = 0x0030EA40       # E130 notify helper
X_112F0 = 0x003112F0       # E130 second notify
X_279B0 = 0x003279B0       # E130 element notify
X_8C40  = 0x00808C40       # canary check
X_6A50  = 0x00386A50       # E130 notify thunk A
X_6AE0  = 0x00386AE0       # E130 notify thunk B
X_A720  = 0x0046A720       # E130 notify C
X_A790  = 0x0046A790       # E130 notify D
X_A690  = 0x0046A690       # C650 post-sync
X_5D8C0 = 0x0035D8C0       # license chain
X_EACD0 = 0x002EACD0
X_A1180 = 0x003A1180
X_DF220 = 0x002DF220
X_29210 = 0x00329210
X_1E9A0 = 0x0031E9A0       # item-record predicate
X_23890 = 0x00323890       # bit-record predicate
X_FEF30 = 0x002FEF30       # member gate
X_E060  = 0x0030E060       # final tail
X_E360  = 0x0030E360       # status apply/remove (contract entry)
X_1EC0  = 0x00861EC0       # memset (implemented in hook)

# ---- globals / fixture cells ----
CANARY  = 0x01F44830
UNITB   = 0x020927C0       # 2536A0's cell
ELEMB   = 0x01F83530       # 20E600's cell
FDESC   = 0x00D10460       # field descriptors (f*8: b0 path, b2 mode, d4 bound)
FTAB2   = 0x00D10550       # 632B0 arg table (f*4)
CATTAB  = 0x01EEBCC0       # item category descs (cat*0x58)
FLAGTBL = 0x01EECF98       # item-kind flag masks (idx*4)
D_040   = 0x02EBF040       # cls-0x1D status desc cell
D_038   = 0x02EBF038       # FED0 bit-record desc
D_0F0   = 0x02EBF0F0       # 08A0 chain desc A
D_0F8   = 0x02EBF0F8       # cls-6 item desc
D_108   = 0x02EBF108       # 2F9A60/2F9B20 stat-curve desc
D_130   = 0x02EBF130       # cls-2 / unit-record desc
D_138   = 0x02EBF138       # 08A0 chain desc B
D_190   = 0x02EBF190       # flag-record pointer cell

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
        self.uc.mem_map(HEAP, 0x400000)
        self.trace, self.faults, self.rets = [], [], {}
        self.hb = HEAP            # bump allocator

        self.gm.w(CANARY, qw(0x1122334455667788))
        self.gm.w(ELEMB, qw(self.alloc(0x40000)))   # element array base
        self.elemb = self.gm.q(ELEMB)
        self.gm.w(UNITB, qw(case.get("unitb", 0)))

        # descriptor plumbing: q[cell] -> desc{d+4=count, w+8=stride,
        # d+0xC=elem offset into ELEMB}
        for name, cell in (("d040", D_040), ("d038", D_038),
                           ("d0f0", D_0F0), ("d0f8", D_0F8),
                           ("d108", D_108), ("d130", D_130),
                           ("d138", D_138)):
            d = case.get(name)
            if d is not None:
                desc = self.alloc(0x20)
                self.gm.w(cell, qw(desc))
                self.gm.w(desc + 4, dw(d.get("count", 0)))
                self.gm.w(desc + 8, bytes(struct.pack("<H",
                                          d.get("stride", 0))))
                self.gm.w(desc + 0xC, dw(d.get("off", 0)))

        # flag-record object for 003008A0's or-writes
        self.flagobj = self.alloc(0x20)
        self.gm.w(D_190, qw(case.get("flagobj", self.flagobj)))

        # unit record
        self.unit = self.alloc(0x800)
        u = case.get("unit", {})
        self.gm.w(self.unit + 4, bytes([u.get("b4", 0) & 0xFF]))
        self.gm.w(self.unit + 5, bytes([u.get("b5", 0) & 0xFF]))
        self.gm.w(self.unit + 8, dw(u.get("d8", 0)))
        self.gm.w(self.unit + 0xC, struct.pack("<H", u.get("wc", 0)))
        self.gm.w(self.unit + 6, struct.pack("<h", u.get("w6", 0)))
        for i, v in enumerate(u.get("f10", [])):
            self.gm.w(self.unit + 0x10 + i * 4, struct.pack("<f", v))
        self.gm.w(self.unit + 0x24, dw(u.get("d24", 0)))
        self.gm.w(self.unit + 0x37, bytes([u.get("b37", 0) & 0xFF]))
        self.gm.w(self.unit + 0x48, dw(u.get("d48", 0)))
        self.gm.w(self.unit + 0x4C, struct.pack("<h", u.get("w4c", 0)))
        self.gm.w(self.unit + 0x3C, dw(u.get("d3c", 0)))
        self.gm.w(self.unit + 0x64, dw(u.get("d64", 0)))
        self.gm.w(self.unit + 0x6C, bytes([u.get("b6c", 0) & 0xFF]))
        self.gm.w(self.unit + 0x7C, bytes([u.get("b7c", 0) & 0xFF]))
        self.gm.w(self.unit + 0x28, struct.pack("<h", u.get("w28", 0)))
        self.gm.w(self.unit + 0x1C2, bytes([u.get("level", 0) & 0xFF]))
        for i, v in enumerate(u.get("equip", [])):
            self.gm.w(self.unit + 0x50 + i * 2, struct.pack("<H", v))
        for a, v in u.get("bmap68", {}).items():   # {byteoff: val}
            self.gm.w(self.unit + 0x68 + a, bytes([v & 0xFF]))
        for a, v in u.get("bmap78", {}).items():
            self.gm.w(self.unit + 0x78 + a, bytes([v & 0xFF]))
        # member block behind q[unit? no — q[r8+0x6A0] is read off the
        # FED0 path's r8; supply via member cell on the unit
        self.member = self.alloc(0x1000)
        self.gm.w(self.unit + 0x6A0, qw(self.member))
        self.mflag = self.alloc(0x100)
        self.gm.w(self.member + 0x6A0, qw(self.mflag))
        self.gm.w(self.mflag, bytes([u.get("mf_b0", 0) & 0xFF]))
        self.gm.w(self.member + 0xE90, dw(u.get("memb_e90", 0)))
        for i, v in enumerate(u.get("u40", [])):
            self.gm.w(self.unit + 0x40 + i, bytes([v & 0xFF]))
        for i, v in enumerate(u.get("m78", [])):
            self.gm.w(self.member + 0x78 + i, bytes([v & 0xFF]))
        for a, v in u.get("memb_e80", {}).items():
            self.gm.w(self.member + 0xE80 + a, bytes([v & 0xFF]))

        # field descriptor table (image .data — writable)
        for f, d in case.get("fdesc", {}).items():
            base = FDESC + f * 8
            self.gm.w(base, bytes([d.get("b0", 0) & 0xFF]))
            self.gm.w(base + 1, bytes([d.get("b1", 0) & 0xFF]))
            self.gm.w(base + 2, bytes([d.get("b2", 0) & 0xFF]))
            self.gm.w(base + 4, dw(d.get("d4", 0)))
        for f, v in case.get("ftab2", {}).items():
            self.gm.w(FTAB2 + f * 4, dw(v))

        # item category descriptors
        for cat, d in case.get("cat", {}).items():
            base = CATTAB + cat * 0x58
            self.gm.w(base + 0x3C, dw(d.get("count", 0)))
            self.gm.w(base + 0x48, qw(d.get("cb", 0)))

        # generic named heap blocks written verbatim
        for name, blob in case.get("blobs", {}).items():
            a = self.alloc(len(blob) + 0x10)
            self.gm.w(a, bytes(blob))
            self.rets["blob_" + name] = a

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
             self.gm.d(rsp + 0x28)])
        self.trace.append(tag)

    # scripted boundary table: tag -> case key for return value
    SCR = {X_B860: ("b860", "b860_ret"), X_165C0: ("165c0", "165c0_ret"),
           X_15E90: ("15e90", None), X_16BF0: ("16bf0", None),
           X_632B0: ("632b0", None), X_9F30: ("9f30", "9f30_ret"),
           X_EA40: ("ea40", None), X_112F0: ("112f0", None),
           X_279B0: ("279b0", None), X_8C40: ("8c40", None),
           X_6A50: ("6a50", None), X_6AE0: ("6ae0", None),
           X_A720: ("a720", None), X_A790: ("a790", None),
           X_A690: ("a690", None), X_5D8C0: ("5d8c0", None),
           X_EACD0: ("eacd0", None), X_A1180: ("a1180", "a1180_ret"),
           X_DF220: ("df220", "df220_ret"), X_29210: ("29210", None),
           X_1E9A0: ("1e9a0", "1e9a0_ret"), X_23890: ("23890", "23890_ret"),
           X_FEF30: ("fef30", "fef30_ret"), X_E060: ("e060", None),
           X_E360: ("e360", None), F_E130: ("e130", None),
           F_FED0: ("fed0", None)}

    def on_code(self, uc, addr, size, _):
        ent = self.SCR.get(addr)
        if ent is not None:
            tag, retkey = ent
            # nested-subject calls only count when not the entry point
            if addr in (F_E130, F_FED0) and addr == self.entry:
                return
            self._args(tag)
            if retkey:
                uc.reg_write(UC_X86_REG_RAX,
                             self.case.get(retkey, 0) & 0xFFFFFFFFFFFFFFFF)
            self._ret()
            return
        if addr == X_1EC0:      # memset(rcx, dl, r8)
            dst = uc.reg_read(UC_X86_REG_RCX)
            cnt = uc.reg_read(UC_X86_REG_R8)
            uc.mem_write(dst, b"\0" * cnt)
            self.trace.append("memset")
            self._ret()
            return
        if addr == self.case.get("cb_addr"):   # planted 08A0 callback
            self._args("itemcb")
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("cb_ret", 0) & 0xFFFFFFFF)
            self._ret()
            return
        if addr == S_36A0: self.trace.append("s36a0")
        elif addr == S_E600: self.trace.append("e600")
        elif addr == S_9A60: self.trace.append("9a60")
        elif addr == S_9B20: self.trace.append("9b20")
        elif addr == S_9BD0: self.trace.append("9bd0")
        elif addr == S_166F0: self.trace.append("166f0")
        elif addr == V_C50:
            self.rets.setdefault("v_calls", []).append(
                [uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                 uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF])

    def run(self, entry, rcx=0, rdx=0, r8=0, r9=0, arg5=0, arg6=0):
        uc = self.uc
        self.entry = entry
        rsp = STACK + 0x80000
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))
        self.gm.w(rsp + 0x28, qw(arg5))
        self.gm.w(rsp + 0x30, qw(arg6))
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
CASES = {
    # ---- 00316A50: field writer ----
    "fld-oob":      {"f": 0x1E, "delta": 5},
    "fld-p0-m0-set":  {"f": 3, "delta": 0x200,
                       "fdesc": {3: {"b0": 0, "b2": 0, "d4": 0x100}},
                       "ftab2": {3: 0xAAAA},
                       "unitb": True, "165c0_ret": 0},
    "fld-p0-m0-below": {"f": 3, "delta": 0x50,
                        "fdesc": {3: {"b0": 0, "b2": 0, "d4": 0x100}},
                        "unitb": True, "165c0_ret": 0},
    "fld-p0-m0-getter": {"f": 3, "delta": 0x200,
                         "fdesc": {3: {"b0": 0, "b2": 0, "d4": 0x100}},
                         "unitb": True, "165c0_ret": 0x300},
    "fld-p0-m1-eq":   {"f": 3, "delta": 0x77,
                       "fdesc": {3: {"b0": 0, "b2": 1, "d4": 0x77}},
                       "unitb": True},
    "fld-p0-m1-ne":   {"f": 3, "delta": 0x78,
                       "fdesc": {3: {"b0": 0, "b2": 1, "d4": 0x77}},
                       "unitb": True},
    "fld-p1-clamp16": {"f": 3, "delta": 0x40, "store": 0x7FF0,
                       "fdesc": {3: {"b0": 2, "b1": 0, "b2": 0}},
                       "unitb": True},
    "fld-p1-neg":     {"f": 3, "delta": -5 & 0xFFFFFFFF, "store": 0,
                       "fdesc": {3: {"b0": 2, "b1": 0, "b2": 0}},
                       "unitb": True},
    "fld-p1-clamp32": {"f": 3, "delta": 0x40, "store": 0x7FFFFFF0,
                       "fdesc": {3: {"b0": 4, "b1": 0, "b2": 0}},
                       "unitb": True},
    "fld-p1-m3-bts":  {"f": 3, "delta": 0xE5, "store": 0,
                       "fdesc": {3: {"b0": 2, "b1": 0, "b2": 3}},
                       "unitb": True},
    "fld-p1-m8":      {"f": 3, "delta": 0xE5, "store": 0,
                       "fdesc": {3: {"b0": 2, "b1": 0, "b2": 8}},
                       "unitb": True},
    "fld-p1-m5":      {"f": 3, "delta": 0xE5, "store": 0x1234,
                       "fdesc": {3: {"b0": 2, "b1": 0, "b2": 5}},
                       "unitb": True},
    "fld-p1-add":     {"f": 3, "delta": 0x10,
                       "fdesc": {3: {"b0": 1, "b1": 0, "b2": 0}},
                       "unitb": True},

    # ---- 0030C650: level-set / growth ----
    "lvl-at-target": {"unit": {"level": 10}, "target": 10},
    "lvl-one":       {"unit": {"level": 5, "b4": 2, "d8": 0x111,
                               "wc": 0x222, "f10": [1.0, 2.0, 3.0, 4.0]},
                      "target": 6, "flags": 0, "b860_rec": 1,
                      "d130": {"count": 8, "stride": 0x30, "off": 0x100},
                      "d108": {"count": 8, "stride": 2, "off": 0x300}},
    "lvl-multi":     {"unit": {"level": 5, "b4": 2, "d8": 0x111,
                               "wc": 0x222, "f10": [1.0, 2.0, 3.0, 4.0]},
                      "target": 8, "flags": 0,
                      "d130": {"count": 8, "stride": 0x30, "off": 0x100},
                      "d108": {"count": 8, "stride": 2, "off": 0x300}},
    "lvl-flag5":     {"unit": {"level": 5, "b4": 2, "b5": 1},
                      "target": 6, "flags": 0, "b860_rec": 1,
                      "d130": {"count": 8, "stride": 0x30, "off": 0x100},
                      "d108": {"count": 8, "stride": 2, "off": 0x300}},
    "lvl-nosync":    {"unit": {"level": 5, "b4": 2, "d8": 0x111,
                               "wc": 0x222, "f10": [1.0, 2.0, 3.0, 4.0]},
                      "target": 6, "flags": 2,
                      "d130": {"count": 8, "stride": 0x30, "off": 0x100},
                      "d108": {"count": 8, "stride": 2, "off": 0x300}},
    "lvl-cap99":     {"unit": {"level": 98, "b4": 2, "d8": 0x111,
                               "wc": 0x222, "f10": [1.0, 2.0, 3.0, 4.0]},
                      "target": 200, "flags": 0, "b860_rec": 1,
                      "d130": {"count": 8, "stride": 0x30, "off": 0x100},
                      "d108": {"count": 8, "stride": 2, "off": 0x300}},

    # ---- 003008A0: item write ----
    "itm-ffff":   {"id": 0xFFFF},
    "itm-1000":   {"id": 0x1000},
    "itm-f000":   {"id": 0xF000},
    "itm-bound":  {"id": 0x3005,
                   "cat": {3: {"count": 4}}},
    "itm-plain":  {"id": 0x4002, "r9": 0, "9f30_ret": 7,
                   "cat": {4: {"count": 8}}},
    "itm-cb":     {"id": 0x4002, "r9": 0, "use_cb": 1,
                   "cb_ret": 0x55, "cat": {4: {"count": 8}}},
    "itm-add-c3": {"id": 0x3003, "r9": 1, "9f30_ret": -1,
                   "use_cb": 1, "cb_ret": 1,
                   "cat": {3: {"count": 8}},
                   "d0f0": {"count": 8, "stride": 0x10, "off": 0x200},
                   "d138": {"count": 8, "stride": 0x20, "off": 0x400},
                   "chain": 1},
    "itm-add-c4": {"id": 0x4003, "r9": 1, "9f30_ret": -1,
                   "use_cb": 1, "cb_ret": 1,
                   "cat": {4: {"count": 8}}},
    "itm-add-cC": {"id": 0xC005, "r9": 1, "9f30_ret": -1,
                   "use_cb": 1, "cb_ret": 1,
                   "cat": {0xC: {"count": 8}}},
    "itm-add-cC2": {"id": 0xC015, "r9": 1, "9f30_ret": -1,
                    "use_cb": 1, "cb_ret": 1,
                    "cat": {0xC: {"count": 0x20}}},

    # ---- 0030E130: status-bit modifier ----
    "st-oob":     {"bit": 0x30, "mode": 2,
                   "d040": {"count": 0x20}},
    "st-m2-set":  {"bit": 5, "mode": 2, "d040": {"count": 0x80}},
    "st-m2-already": {"bit": 5, "mode": 2,
                      "unit": {"bmap68": {0: 0x20}},
                      "d040": {"count": 0x80}},
    "st-m0-clear": {"bit": 5, "mode": 0,
                    "unit": {"bmap68": {0: 0x20}},
                    "d040": {"count": 0x80}},
    "st-m0-absent": {"bit": 5, "mode": 0, "d040": {"count": 0x80}},
    "st-m3-set78": {"bit": 9, "mode": 3, "d040": {"count": 0x80}},
    "st-m1-clear78": {"bit": 9, "mode": 1,
                      "unit": {"bmap78": {1: 0x02}},
                      "d040": {"count": 0x80}},
    "st-mode4":   {"bit": 5, "mode": 4, "d040": {"count": 0x80}},
    "st-sync":    {"bit": 0x69, "mode": 2, "flags": 0,
                   "d040": {"count": 0x80}},
    "st-nosync":  {"bit": 0x69, "mode": 2, "flags": 0x200,
                   "d040": {"count": 0x80}},

    # ---- 0030FED0: recompute ----
    "rc-null":    {"unitptr": 0},
    "rc-b5-2":    {"unit": {"b5": 2, "level": 1}},
    "rc-base":    {"unit": {"b5": 0, "b4": 2, "level": 1,
                            "equip": [0x1000, 0xFFFF, 0xFFFF, 0xFFFF,
                                      0xFFFF]},
                   "m50": 0x00000025, "m54": 0,
                   "equip_b1a": 0x40, "1e9a0_ret": 3,
                   "d130": {"count": 8, "stride": 0x60, "off": 0x100},
                   "d0f8": {"count": 8, "stride": 0x20, "off": 0x800},
                   "d038": {"count": 0x200, "stride": 0x10,
                            "off": 0xC00}},
    "rc-member":  {"unit": {"b5": 1, "b4": 2, "level": 1,
                            "memb_e80": {0: 0x03}, "memb_e90": 0x05,
                            "u40": [0x11, 0x22, 0x33, 0x44, 0x55],
                            "equip": [0xFFFF] * 5},
                   "b5member": 1,
                   "d130": {"count": 8, "stride": 0x60, "off": 0x100},
                   "d0f8": {"count": 8, "stride": 0x20, "off": 0x800},
                   "d038": {"count": 0x200, "stride": 0x10,
                            "off": 0xC00}},
}


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    if name.startswith("fld"):
        # unitb: q[UNITB] -> heap block whose +0x3844 is the bitfield
        if case.get("unitb"):
            ub = w.alloc(0x4000)
            w.gm.w(UNITB, qw(ub))
            w.ubase = ub
            st = case.get("store")
            if st is not None:
                w.gm.w(ub + 0x384C, dw(st))
        out["ret"] = w.run(F_16A50, rcx=case.get("f", 0),
                           rdx=case.get("delta", 0))
        if case.get("unitb"):
            f = case["f"]
            out["bit"] = (w.gm.b(w.ubase + 0x3844 + (f >> 3))
                          >> (f & 7)) & 1
    elif name.startswith("lvl"):
        if case.get("b860_rec"):
            rec = w.alloc(0x800)
            memb2 = w.alloc(0x100)
            w.gm.w(rec + 0x698, qw(memb2))
            w.gm.w(memb2 + 5, bytes([case.get("m2b5", 0) & 0xFF]))
            w.case["b860_ret"] = rec
        out["ret"] = w.run(F_C650, rcx=w.unit,
                           rdx=case.get("target", 0),
                           r8=case.get("flags", 0))
        gm = w.gm
        out["unit"] = {"level": gm.b(w.unit + 0x1C2),
                       "d8": gm.d(w.unit + 8),
                       "wc": struct.unpack("<H", bytes(
                           gm.uc.mem_read(w.unit + 0xC, 2)))[0],
                       "f10": [gm.f(w.unit + 0x10 + i * 4)
                               for i in range(4)]}
    elif name.startswith("itm"):
        if case.get("use_cb"):
            cba = w.alloc(0x10)
            w.case["cb_addr"] = cba
            w.gm.w(CATTAB + (case["id"] >> 12) * 0x58 + 0x48, qw(cba))
        if case.get("chain"):
            recA = w.elemb + 0x200 + (case["id"] & 0xFFF) * 0x10
            w.gm.w(recA + 2, bytes([case.get("reca_b2", 0) & 0xFF]))
            recB = w.elemb + 0x400 + case.get("reca_b2", 0) * 0x20
            w.gm.w(recB + 0x2C, struct.pack("<H",
                                            case.get("recb_w2c", 0)))
            idx = case.get("recb_w2c", 0) & 7
            out["flagmask"] = w.gm.d(FLAGTBL + idx * 4)
        out["ret"] = w.run(F_08A0, rcx=case.get("id", 0),
                           rdx=case.get("rdx", 0),
                           r8=case.get("r8", 0),
                           r9=case.get("r9", 0),
                           arg5=case.get("arg5", 0))
        out["flags"] = w.gm.d(w.flagobj + 4)
    elif name.startswith("st-"):
        out["ret"] = w.run(F_E130, rcx=w.unit,
                           rdx=case.get("bit", 0),
                           r8=case.get("r8", 0),
                           r9=case.get("flags", 0),
                           arg5=case.get("mode", 0))
        f = case.get("bit", 0)
        out["b68"] = w.gm.b(w.unit + 0x68 + (f >> 3))
        out["b78"] = w.gm.b(w.unit + 0x78 + (f >> 3))
    elif name.startswith("rc-"):
        # unit record via the d130 double-hop: rec = elemb + off +
        # stride * b[unit+4]
        d130 = case.get("d130")
        if d130:
            rec = w.elemb + d130["off"] + d130["stride"] *                 case.get("unit", {}).get("b4", 0)
            w.gm.w(rec + 0x50, dw(case.get("m50", 0)))
            w.gm.w(rec + 0x54, dw(case.get("m54", 0)))
        # member bitmap path uses scripted 31B860 -> member block
        if case.get("b5member"):
            w.case["b860_ret"] = w.member
        # equipped item record via d0f8: recI = elemb + off +
        # stride * (id - 0x1000); 31E9A0(ret)==3 -> b[recI+0x1A] bit
        d0f8 = case.get("d0f8")
        if d0f8 and case.get("equip_b1a") is not None:
            w.gm.w(w.elemb + d0f8["off"] + 0x1A,
                   bytes([case["equip_b1a"] & 0xFF]))
        uptr = case.get("unitptr", w.unit)
        out["ret"] = w.run(F_FED0, rcx=uptr,
                           rdx=case.get("flags", 0))
        out["u6"] = struct.unpack("<h", bytes(
            w.gm.uc.mem_read(w.unit + 6, 2)))[0]
        out["u48"] = w.gm.d(w.unit + 0x48)
        out["u4c"] = struct.unpack("<h", bytes(
            w.gm.uc.mem_read(w.unit + 0x4C, 2)))[0]
        out["m78"] = [w.gm.b(w.mflag + 0x78 + i) for i in range(5)]
        out["u40"] = [w.gm.b(w.unit + 0x40 + i) for i in range(5)]
    out.update(w.rets)
    out["ok"], out["fail"] = check(name, case, out)
    return out


def check(name, c, o):
    f = []
    tr = o["trace"]
    calls = o.get("calls", [])

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %s want %s" % (k, hex(got), hex(want)))

    def called(tag):
        return [x for x in calls if x[0] == tag]

    def no_faults():
        if o["faults"]:
            f.append("faults: %s" % o["faults"])

    if name != "rc-null":
        no_faults()

    if name.startswith("fld"):
        fno = c.get("f", 0)
        d = c.get("fdesc", {}).get(fno, {})
        if name == "fld-oob":
            if calls:
                f.append("oob made calls: %s" % calls)
        elif name == "fld-p0-m0-set":
            eq("bit", o["bit"], 1)
            c6 = called("632b0")
            if len(c6) != 1:
                f.append("632b0 calls: %s" % c6)
            else:
                eq("632b0.ecx", c6[0][1], 0xAAAA)
        elif name in ("fld-p0-m0-below", "fld-p0-m0-getter",
                      "fld-p0-m1-ne", "fld-p1-m8"):
            eq("bit", o["bit"], 0)
            if called("632b0"):
                f.append("unexpected 632b0")
            if called("16bf0"):
                f.append("unexpected writeback")
        elif name == "fld-p0-m1-eq":
            eq("bit", o["bit"], 1)
            if not called("632b0"):
                f.append("no 632b0")
        elif name == "fld-p1-clamp16":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.f", cb[0][1], fno)
                eq("16bf0.val", cb[0][2], 0x7FFF)
            if not called("15e90"):
                f.append("no 15e90")
        elif name == "fld-p1-neg":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.val", cb[0][2], 0)
        elif name == "fld-p1-clamp32":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.val", cb[0][2], 0x7FFFFFFF)
        elif name == "fld-p1-m3-bts":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.val", cb[0][2], 8)
        elif name == "fld-p1-add":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.val", cb[0][2],
                   (0xFFFFFFFF + c.get("delta", 0)) & 0xFFFFFFFF)
        elif name == "fld-p1-m5":
            cb = called("16bf0")
            if len(cb) != 1:
                f.append("16bf0 calls: %s" % cb)
            else:
                eq("16bf0.val", cb[0][2], c.get("store", 0))

    elif name.startswith("lvl"):
        u = c.get("unit", {})
        start = u.get("level", 0)
        tgt = min(c.get("target", 0), 0x63)
        if name == "lvl-at-target":
            eq("level", o["unit"]["level"], start)
            if calls:
                f.append("calls at-target: %s" % calls)
        else:
            eq("level", o["unit"]["level"], tgt)
            niter = tgt - start
            if u.get("b5", 0) == 0:
                if tr.count("9a60") != niter:
                    f.append("9a60 count %d want %d"
                             % (tr.count("9a60"), niter))
                if tr.count("9bd0") != 4 * niter:
                    f.append("9bd0 count %d want %d"
                             % (tr.count("9bd0"), 4 * niter))
            else:
                if tr.count("9a60"):
                    f.append("9a60 ran despite b5")
            fe = called("fed0")
            want_fe = 1 if tgt > start else 0
            if len(fe) != want_fe:
                f.append("fed0 calls %d want %d" % (len(fe), want_fe))
            elif fe:
                eq("fed0.edx", fe[0][2], 0)
            if c.get("flags", 0) & 2 or u.get("b5", 0) != 0:
                if called("a690"):
                    f.append("a690 despite suppress")
            elif tgt > start:
                if not called("a690"):
                    f.append("no a690")

    elif name.startswith("itm"):
        if name in ("itm-ffff", "itm-1000", "itm-f000", "itm-bound"):
            eq("ret", o["ret"] & 0xFFFFFFFF, 0xFFFFFFFF)
        elif name == "itm-plain":
            eq("ret", o["ret"], 7)
            eq("flags", o["flags"], 0)
        elif name == "itm-cb":
            eq("ret", o["ret"], 0x55)
            cb = called("itemcb")
            if len(cb) != 1:
                f.append("cb calls: %s" % cb)
            else:
                eq("cb.id", cb[0][1] & 0xFFFF, c["id"])
        elif name == "itm-add-c3":
            mask = struct.unpack("<I", open(EXE, "rb").read()
                                 [0:0])[0] if False else None
            want = 1 | o.get("flagmask", 0)
            eq("flags", o["flags"], want)
        elif name == "itm-add-c4":
            eq("flags", o["flags"], 0x40)
        elif name == "itm-add-cC":
            eq("flags", o["flags"], 0x80)
        elif name == "itm-add-cC2":
            eq("flags", o["flags"], 0x100)

    elif name.startswith("st-"):
        bit = c.get("bit", 0)
        mask = 1 << (bit & 7)
        mode = c.get("mode", 0)
        if name == "st-oob":
            bad = [t for t in tr if t != "8c40"]
            if bad:
                f.append("oob ran: %s" % bad)
        elif name == "st-mode4":
            eq("b68", o["b68"], 0)
            bad = [t for t in tr if t != "8c40"]
            if bad:
                f.append("mode4 ran: %s" % bad)
        else:
            set68 = mode == 2
            clr68 = mode == 0
            set78 = mode == 3
            clr78 = mode == 1
            pre68 = c.get("unit", {}).get("bmap68", {}).get(bit >> 3, 0)
            pre78 = c.get("unit", {}).get("bmap78", {}).get(bit >> 3, 0)
            if set68:
                eq("b68", o["b68"], (pre68 | mask) & 0xFF)
            elif clr68:
                eq("b68", o["b68"], pre68 & ~mask & 0xFF)
            if set78:
                eq("b78", o["b78"], (pre78 | mask) & 0xFF)
            elif clr78:
                eq("b78", o["b78"], pre78 & ~mask & 0xFF)
            changed = (set68 and not (pre68 & mask)) or \
                      (clr68 and (pre68 & mask)) or \
                      (set78 and not (pre78 & mask)) or \
                      (clr78 and (pre78 & mask))
            if changed:
                if "memset" not in tr:
                    f.append("no memset on change")
                th = called("6a50") + called("6ae0")
                if len(th) != 1:
                    f.append("notify thunks: %s" % th)
                else:
                    want = "6ae0" if mode >= 2 else "6a50"
                    if th[0][0] != want:
                        f.append("thunk %s want %s" % (th[0][0], want))
                if not (c.get("flags", 0) & 2):
                    th2 = called("a720") + called("a790")
                    if len(th2) != 1:
                        f.append("notify2: %s" % th2)
                    else:
                        want2 = "a790" if mode >= 2 else "a720"
                        if th2[0][0] != want2:
                            f.append("notify2 %s want %s"
                                     % (th2[0][0], want2))
            else:
                if "memset" in tr:
                    f.append("memset without change")
                if called("6a50") or called("6ae0") or called("a720")                         or called("a790"):
                    f.append("notify without change: %s" % calls)
            if 0x68 <= bit <= 0x71:
                p = called("279b0")
                want_d = (1 if mode >= 2 else 0) * 2 - 1
                if len(p) != 1:
                    f.append("279b0 calls: %s" % p)
                elif changed:
                    eq("279b0.edx", p[0][2], want_d & 0xFFFFFFFF)
            if name == "st-sync":
                fe = called("fed0")
                if len(fe) != 1:
                    f.append("fed0 calls: %s" % fe)
                else:
                    eq("fed0.edx", fe[0][2], c.get("flags", 0))
            if name == "st-nosync":
                if called("fed0"):
                    f.append("fed0 despite flag bit9")

    elif name.startswith("rc-"):
        if name == "rc-null":
            if not o["faults"]:
                f.append("null unit did not fault")
            elif o["faults"][0][2] != 0x50:
                f.append("fault addr %s want 0x50"
                         % hex(o["faults"][0][2]))
        elif name == "rc-b5-2":
            if called("e130") or called("e360"):
                f.append("b5=2 dispatched: %s" % calls)
        else:
            e1 = called("e130")
            o["e130_n"] = len(e1)
            want_bits = []
            if name == "rc-base":
                want_bits = [i for i in range(32)
                             if c.get("m50", 0) >> i & 1]
                if c.get("equip_b1a") is not None and \
                        c.get("1e9a0_ret") == 3:
                    want_bits.append(c["equip_b1a"])
            elif name == "rc-member":
                for a, v in c.get("unit", {}).get(
                        "memb_e80", {}).items():
                    want_bits += [a * 8 + i for i in range(8)
                                  if v >> i & 1]
            want_bits = sorted(set(want_bits))
            got_bits = sorted(x[2] for x in e1)
            if got_bits != want_bits:
                f.append("e130 bits %s want %s" % (got_bits,
                                                   want_bits))
            for x in e1:
                if x[4] != (c.get("flags", 0) | 0x202):
                    f.append("e130 r9 %x want flags|0x202" % x[4])
                if x[5] != 3:
                    f.append("e130 mode %x want 3" % x[5])
            e3 = called("e360")
            o["e360_n"] = len(e3)
            want_e3 = sorted(i for i in range(32)
                             if c.get("unit", {}).get(
                                 "memb_e90", 0) >> i & 1) \
                if name == "rc-member" else []
            got_e3 = sorted(x[3] for x in e3)
            if got_e3 != want_e3:
                f.append("e360 bits %s want %s" % (got_e3, want_e3))
            # copy direction: mf bit7 clear -> unit+0x40.. to member+0x78..
            if name == "rc-member":
                src = c.get("unit", {}).get("u40", [])
                if not (c.get("unit", {}).get("mf_b0", 0) & 0x80):
                    for i in range(min(len(src), 5)):
                        eq("m78[%d]" % i, o["m78"][i], src[i])
            fe = called("e060")
            if len(fe) != 1:
                f.append("e060 calls: %s" % fe)

    return (len(f) == 0), f


def main():
    raw, secs = load_image()
    out = {"cases": len(CASES), "pass": 0, "fail": 0, "results": {}}
    for name, case in CASES.items():
        try:
            r = run_case(name, case, raw, secs)
        except Exception as e:
            r = {"ok": False, "fail": ["exception: %r" % e],
                 "trace": [], "faults": []}
        out["results"][name] = r
        if r["ok"]:
            out["pass"] += 1
        else:
            out["fail"] += 1
            print("%-18s FAIL %s" % (name, r["fail"]))
            if r["faults"]:
                print("   faults:", r["faults"][:3])
            print("   trace:", r["trace"][:40])
            print("   calls:", r.get("calls", [])[:20])
    out["ok"] = out["fail"] == 0
    with open(RESULT, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("%d/%d pass" % (out["pass"], out["cases"]))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
