# EXP-140 license-check-exec — isolated original-code run (ASTRA-TRANSFER-
# ORACLE-S31-LICENCE; original request OPUS-REQ-ASTRA-S31-LICENCE-CHECK-
# ISOLATED-RUN). Executes the licence-check bodies real under Unicorn,
# Python model mirrors site-for-site.
#
#   MAIN   00323EC0 — BattleStats_HasRequiredLicenseForAction
#            (rcx=statsRecord, edx=actionId). I1 exits in order:
#            validator(0x14,id)==0 -> 0; rec==0 -> 1; b[rec+5]!=0 -> 1;
#            b[rec+4]>6 (unsigned) -> 1. Then action-row escape:
#            desc=q[0x2EBF138], row=decode(d[desc+0xC])+w[desc+8]*id,
#            w[row+0x2C]&0x2000 -> 1. Then id-0xD0<=0x11 -> I5:
#            prow=decode(desc2=0x2EBF130)+w[desc2+8]*b[rec+4];
#            idx=ROWSRCH(prow,id16); n=POPCNT(rec); ret idx<n (setl,
#            signed). Else tail-jmp PREREQ(rec,1,id).
#   PREREQ 00323BB0 — zeroes 0x2E stack mask (5 q + d + w), calls
#            BUILDER(ecx=1, dx=id16, r8=&mask), then byte-wise AND vs
#            rec+0x194 returning 1 on first nonzero byte, else 0.
#            Cookie-checked (real CHKCK).
#   POPCNT 00324020 — 3 passes x 6 bits = popcount of bits 0..17 of
#            rec+0x194 (r11 walks 2,8,14; per pass tests indices
#            r11-2..r11+3 via (idx>>3) byte + rol'd dl mask).
#   ROWSRCH 0030A330 — for i in 0..2: cx = row? b[row+4+i] : 0xFFFF;
#            cx==dx -> ret i; else 3.
#   VALID  00322C50 — BattleEncodedId_IsValidForClass: class 1..32,
#            jtab d[0x323054+(cls-1)*4]+0x120000; class-0x14 arm
#            0x322F72 reads desc q[0x2EBF138] — the SAME action-table
#            descriptor as MAIN I3 — count=d[desc+4];
#            tail 0x32302C: 0<=id<count -> 1 else 0.
#   DECODE 0020E600 — rax = ecx + q[0x1F83530] (BASE pool decode).
#   BUILDER 002F8FA0 — (ecx=kind, dx=reqId16, r8=out): n=d[descN+4]
#            where descN=q[0x2EBF038]; memset(out,0,(n+7)>>3) via real
#            TMS thunk -> host memset; loop i<n: row = descN? decode(
#            d[descN+0xC]) + w[descN+8]*i : 0; if CLS1(b[row+5])==kind:
#            scan w[row+8+2k] k=0..7 for reqId16 -> bts out[i>>3],i&7,
#            ebp++. Returns match count.
#   CLS1   00323890 — CLS2(b)-0x15, >9 -> -1; else jtab 0x3238E4:
#            {0,1,2,3}->0, {4,5,8}->1, {6,7}->2, {9}->3.
#   CLS2   003241D0 — kind byte: k-1>0x1D -> 0; else remap
#            b[0x324260+k-1] -> jtab 0x324234 -> ret 0x15+slot
#            (slot10 -> 0).
#   CHKCK  00808C40 — __security_check_cookie (real; shipped cookie
#            q[0x1F44830]).
#
# Scripted boundary (disclosed, single):
#   MSET  memset — via real thunk 00861EC0 jmp q[IAT 0x8C2A60] ->
#        planted host trampoline; host memsets guest mem and records
#        "memset:<dst>:<val>:<n>" in trace.
#
# Fixture (planted, disclosed): all descriptor globals are BSS
# (ship 0) — q[0x2EBF138] (action table, also the class-0x14
# validator source), q[0x2EBF130] (party rows), q[0x2EBF038]
# (node table) point at planted descriptors in the BASE pool;
# q[0x1F83530]=BASEP.
# Stats record REC on the heap: b[+4]=slot, b[+5]=kind, mask at
# +0x194 (46B). Everything fixture-planted is MODEL-PROVEN, not
# replay authority.
#
# Native and model must agree on trace/rets/faults/watched memory.

import ctypes
import hashlib
import json
import struct
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_HOOK_INTR, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RBX

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000
MSET   = 0x630A0000          # planted trampoline: memset import

MAIN    = 0x00323EC0         # BattleStats_HasRequiredLicenseForAction
PREREQ  = 0x00323BB0         # HasLicensePrerequisiteForRequirement
POPCNT  = 0x00324020         # CountLicenseBits00To17
ROWSRCH = 0x0030A330         # slot-row 3-byte search
VALID   = 0x00322C50         # BattleEncodedId_IsValidForClass
DECODE  = 0x0020E600         # ecx + q[0x1F83530]
BUILDER = 0x002F8FA0         # BuildPrerequisiteNodeMaskForRequirement
CLS1    = 0x00323890         # kind byte -> class {0,1,2,3,-1}
CLS2    = 0x003241D0         # kind byte -> 0x15+remap or 0
TMS     = 0x00861EC0         # real IAT thunk -> memset
CHKCK   = 0x00808C40         # __security_check_cookie (real)

BASECELL = 0x1F83530         # q: BASE pool base (BSS, ships 0)
DESCA_A  = 0x2EBF138         # q: action-row descriptor (also the
                             #    class-0x14 validator's count source)
DESCP_A  = 0x2EBF130         # q: party-row descriptor
DESCN_A  = 0x2EBF038         # q: license-node-table descriptor
MSETIAT  = 0x8C2A60          # q: IAT memset (import-dir proven)

BASEP  = HEAP + 0x30000      # BASE pool base -> decode(i)=BASEP+i
REC    = HEAP + 0x40000      # statsRecord fixture (needs +0x1C0)
DESCA  = HEAP + 0x42000      # action-row descriptor (d+4 = count
                             #    bound for validator, w+8 = stride,
                             #    d+0xC = enc)
DESCP  = HEAP + 0x43000      # party-row descriptor
DESCN  = HEAP + 0x44000      # node-table descriptor


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)
def bb(v): return struct.pack("<B", v & 0xFF)


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


def img_rd(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + (rva - sva): ra + (rva - sva) + n]
    raise KeyError("image read outside shipped bytes: %x" % va)


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL,
                            ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x"
                       % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data),
                       len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    W.append((MSETIAT, qw(MSET)))
    W.append((BASECELL, qw(case.get("basep", BASEP))))
    # descriptor fixtures (BSS globals -> planted descriptors)
    W.append((DESCA_A, qw(case.get("desca", DESCA))))
    W.append((DESCP_A, qw(case.get("descp", DESCP))))
    W.append((DESCN_A, qw(case.get("descn", DESCN))))
    # DESCA: action-row descriptor — d[+4]=count (validator bound),
    # w[+8]=stride, d[+0xC]=enc
    da = bytearray(0x20)
    da[4:8] = dw(case.get("vcount", 0x220))
    da[8:0xA] = ww(case.get("astride", 0x40))
    da[0xC:0x10] = dw(case.get("enca", 0x0400))
    W.append((DESCA, bytes(da)))
    # DESCP: party-row descriptor — indexed by rec[4]
    dp = bytearray(0x20)
    dp[8:0xA] = ww(case.get("pstride", 0x20))
    dp[0xC:0x10] = dw(case.get("encp", 0x1000))
    W.append((DESCP, bytes(dp)))
    # DESCN: node-table descriptor — d[+4]=rows, w[+8]=stride,
    # d[+0xC]=enc
    dn = bytearray(0x20)
    dn[4:8] = dw(case.get("nrows", 8))
    dn[8:0xA] = ww(case.get("nstride", 0x20))
    dn[0xC:0x10] = dw(case.get("encn", 0x2000))
    W.append((DESCN, bytes(dn)))
    # BASE pool image: action rows @0x400, party rows @0x1000,
    # node rows @0x2000
    pool = bytearray(0x8000)
    # action rows: w[row+0x2C] flag word (bit 0x2000 = no licence)
    arows = case.get("arows", {})          # {actionId: flagword}
    astride = case.get("astride", 0x40)
    for aid, flag in arows.items():
        r = 0x0400 + astride * aid
        pool[r + 0x2C:r + 0x2E] = ww(flag)
    # party rows: three action-id bytes at row+4/+5/+6
    prows = case.get("prows", {})          # {slot: (b4,b5,b6)}
    pstride = case.get("pstride", 0x20)
    for slot, ids in prows.items():
        r = 0x1000 + pstride * slot
        pool[r + 4:r + 7] = bytes(ids)
    # node rows: b[+5]=kind byte, w[+8+2k]=requirement ids
    nrows = case.get("nrecs", [])          # [(kind, [ids...]), ...]
    nstride = case.get("nstride", 0x20)
    for i, (kind, ids) in enumerate(nrows):
        r = 0x2000 + nstride * i
        pool[r + 5] = kind & 0xFF
        for k, rid in enumerate(ids[:8]):
            pool[r + 8 + k * 2:r + 0xA + k * 2] = ww(rid)
    W.append((BASEP, bytes(pool)))
    # stats record: b[+4]=slot, b[+5]=kind, mask at +0x194 (46B)
    rec = bytearray(0x200)
    rec[4] = case.get("rec_slot", 0) & 0xFF
    rec[5] = case.get("rec_kind", 0) & 0xFF
    mask = case.get("mask", bytes(46))
    rec[0x194:0x194 + 46] = bytes(mask[:46])
    W.append((REC, bytes(rec)))
    return W


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.map(MSET, 0x1000, b"\xc3" * 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, addr, size))
        uc.emu_stop()
        return True

    def on_code(self, uc, addr, size, _):
        if addr == MSET:
            dst = uc.reg_read(UC_X86_REG_RCX)
            val = uc.reg_read(UC_X86_REG_RDX) & 0xFF
            n = uc.reg_read(UC_X86_REG_R8)
            self.gm.w(dst, bytes([val]) * n)
            uc.reg_write(UC_X86_REG_RAX, dst)
            self.trace.append("memset:%x:%x:%x" % (dst, val, n))
            self._ret(uc)

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        try:
            uc.emu_start(entry, RETQ, count=300000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for step in self.case.get("steps", []):
            entry, rcx = step[0], step[1]
            rdx = step[2] if len(step) > 2 else 0
            r8 = step[3] if len(step) > 3 else 0
            r9 = step[4] if len(step) > 4 else 0
            self.run_one(entry, rcx, rdx, r8, r9)

    def obs(self):
        mem = {}
        for addr, n in self.case.get("watch", []):
            try:
                mem["%x" % addr] = self.gm.r(addr, n).hex()
            except KeyError:
                mem["%x" % addr] = None
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------

RANGES = ((HEAP, HEAP + 0x100000), (IMG_LO, IMG_HI),
          (STACK, STACK + 0x100000))


class Model:
    def __init__(self, case, raw, secs):
        self.case = case
        self.raw, self.secs = raw, secs
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.fault_end = RETQ
        self._rax = 0
        self._fault_rax = 0

    # memory
    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            try:
                return img_rd(self.raw, self.secs, a, 1)[0]
            except KeyError:
                return 0
        return 0
    def mw(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a):
        return self.md(a) | (self.md(a + 4) << 32)
    def sb(self, a, v):
        self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def sd(self, a, v):
        for i in range(4):
            self.sb(a + i, (v >> (8 * i)) & 0xFF)

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in RANGES)

    def _rd(self, a, n, site, raxv=0):
        """ordered read: records ('memr', a, n) + fault_end on
        unmapped and returns None. raxv = the value native RAX
        holds at the faulting instruction."""
        if not self.mapped(a):
            self.faults.append(("memr", a & 0xFFFFFFFFFFFFFFFF, n))
            self.fault_end = site
            self._fault_rax = raxv
            return None
        if n == 1:
            return self.mb(a)
        if n == 2:
            return self.mw(a)
        if n == 4:
            return self.md(a)
        return self.mq(a)

    # ---------- scripted boundary ----------
    def memset(self, dst, val, n):
        for i in range(n):
            self.sb(dst + i, val)
        self.trace.append("memset:%x:%x:%x" % (dst, val & 0xFF, n))
        return dst

    # ---------- bodies ----------
    def decode(self, i):
        """0020E600 — rax = ecx + q[0x1F83530]."""
        return (i + self.mq(BASECELL)) & 0xFFFFFFFFFFFFFFFF

    def cls2(self, k):
        """003241D0 — kind byte k: k-1>0x1D -> 0; else
        remap=btab[0x324260+k-1]; jtab slot -> 0x15+slot or 0
        (slot 10 -> 0)."""
        k = (k - 1) & 0xFFFFFFFF
        if k > 0x1D:
            return 0
        slot = self.mb(0x324260 + k)
        if slot > 10:
            self.faults.append(("unmodeled-cls2-slot", slot, 0))
            return None
        return 0 if slot == 10 else (0x15 + slot)

    def cls1(self, k):
        """00323890 — r = cls2(k)-0x15; r>9 -> -1; else jtab
        0x3238E4: {0,1,2,3}->0, {4,5,8}->1, {6,7}->2, {9}->3."""
        c2 = self.cls2(k)
        if c2 is None:
            return None
        r = (c2 - 0x15) & 0xFFFFFFFF
        if r > 9:
            return -1 & 0xFFFFFFFF
        return (0, 0, 0, 0, 1, 1, 2, 2, 1, 3)[r]

    def valid(self, cls, idv):
        """00322C50 — cls 1..32 -> jtab[cls-1] -> arm. Only the
        class-0x14 arm (0x322F72) is modeled; other dispatches are
        flagged 'unmodeled-arm' (never taken: callers fix 0x14)."""
        a = (cls - 1) & 0xFFFFFFFF
        if a > 0x1F:
            return 0
        tgt = (self.md(0x323054 + a * 4) + 0x120000) & 0xFFFFFFFF
        if tgt != 0x322F72:
            self.faults.append(("unmodeled-arm", tgt, 0))
            return None
        desc = self._rd(DESCA_A, 8, 0x322F72)
        if desc is None:
            return None
        if desc == 0:
            return 0
        cnt = self._rd(desc + 4, 4, 0x322F84)
        if cnt is None:
            return None
        # tail 0x32302C: edx=eax(0); id<0 ->0; id>cnt-1 ->0; else 1
        if idv & 0x80000000:
            return 0
        if idv > (cnt - 1) & 0xFFFFFFFF:
            return 0
        return 1

    def rowsrch(self, row, id16):
        """0030A330 — for i in 0..2: cx = row? b[row+4+i] : 0xFFFF;
        cx==dx -> ret i; else 3."""
        for i in range(3):
            if row == 0:
                cx = 0xFFFF
            else:
                cx = self._rd(row + 4 + i, 1, 0x30A34B)
                if cx is None:
                    return None
            if cx == (id16 & 0xFFFF):
                return i
        return 3

    def popcnt(self, rec):
        """00324020 — popcount of rec+0x194 bits 0..17: 3 passes,
        r11 = 2+6p; per pass test indices r11-2..r11+3, dl rol'd
        once per test starting at 1."""
        n = 0
        dl = 1
        r11 = 2
        for p in range(3):
            for k in range(6):
                idx = r11 - 2 + k
                b = self._rd(rec + 0x194 + (idx >> 3), 1, 0x32404F)
                if b is None:
                    return None
                if b & dl:
                    n += 1
                dl = ((dl << 1) | (dl >> 7)) & 0xFF
            r11 += 6
        return n

    def builder(self, kind, req, out):
        """002F8FA0 — n=d[descN+4]; memset(out,0,(n+7)>>3); per row:
        row=descN? decode(d[+0xC])+w[+8]*i : 0; if cls1(b[row+5])==
        kind: scan w[row+8+2k] k<8 for req -> bts out[i>>3],i&7.
        Returns match count ebp."""
        descn = self._rd(DESCN_A, 8, 0x2F8FB9)
        if descn is None:
            return None
        n = self._rd(descn + 4, 4, 0x2F8FD0) if descn else 0
        if n is None:
            return None
        self.memset(out, 0, ((n + 7) & 0xFFFFFFFF) >> 3)
        cnt = 0
        for i in range(n if n < 0x80000000 else 0):
            descn = self.mq(DESCN_A)
            if descn and self.decode(self.md(descn + 0xC)):
                # ebx = (decode(enc) + stride*i) truncated to 32 bits
                row = ((self.decode(self.md(descn + 0xC)) & 0xFFFFFFFF)
                       + self.mw(descn + 8) * i) & 0xFFFFFFFF
            else:
                row = 0
            kb = self._rd(row + 5, 1, 0x2F9045)
            if kb is None:
                return None
            c = self.cls1(kb)
            if c is None:
                return None
            if c != (kind & 0xFFFFFFFF):
                continue
            for k in range(8):
                w = self._rd(row + 8 + k * 2, 2, 0x2F9060)
                if w is None:
                    return None
                if w == (req & 0xFFFF):
                    byte = self._rd(out + (i >> 3), 1, 0x2F907D)
                    if byte is None:
                        return None
                    self.sb(out + (i >> 3), byte | (1 << (i & 7)))
                    cnt += 1
                    break
        return cnt

    def prereq(self, rec, kind, idv, vsp):
        """00323BB0 — zero 0x2E mask on frame, BUILDER(1? ecx=kind,
        id16, &mask), byte-wise AND vs rec+0x194 first-nonzero -> 1
        else 0. vsp = entry rsp; frame rsp = vsp-0x68 so the mask
        sits at vsp-0x48."""
        mask = vsp - 0x48
        for i in range(5):
            for j in range(8):
                self.sb(mask + i * 8 + j, 0)
        self.sd(mask + 0x28, 0)
        self.sb(mask + 0x2C, 0)
        self.sb(mask + 0x2D, 0)
        r = self.builder(kind, idv & 0xFFFF, mask)
        if r is None:
            return None
        for i in range(0x2E):
            b = self._rd(rec + 0x194 + i, 1, 0x323C18)
            if b is None:
                return None
            m = self._rd(mask + i, 1, 0x323C20)
            if m is None:
                return None
            if m & b:
                return 1
        return 0

    def main(self, rec, idv, vsp):
        """00323EC0 — full I1..I5 chain."""
        r = self.valid(0x14, idv)
        if r is None:
            return None
        if r == 0:
            return 0
        if rec == 0:
            return 1
        k = self._rd(rec + 5, 1, 0x323EF3)
        if k is None:
            return None
        if k != 0:
            return 1
        s = self._rd(rec + 4, 1, 0x323EFF)
        if s is None:
            return None
        if s > 6:
            return 1
        # action-row escape hatch
        desca = self._rd(DESCA_A, 8, 0x323F09)
        if desca is None:
            return None
        if desca:
            enc = self._rd(desca + 0xC, 4, 0x323F1C)
            if enc is None:
                return None
            dp = self.decode(enc)
            if dp:
                enc2 = self._rd(self.mq(DESCA_A) + 0xC, 4, 0x323F30)
                if enc2 is None:
                    return None
                base = self.decode(enc2) & 0xFFFFFFFF
                stride = self.mw(self.mq(DESCA_A) + 8)
                row = (base + stride * idv) & 0xFFFFFFFF
            else:
                row = 0
        else:
            row = 0
        flag = self._rd(row + 0x2C, 2, 0x323F52, raxv=0x2000)
        if flag is None:
            return None
        if flag & 0x2000:
            return 1
        # Quickening range?
        if (idv - 0xD0) & 0xFFFFFFFF <= 0x11:
            descp = self._rd(DESCP_A, 8, 0x323F78)
            if descp is None:
                return None
            if descp:
                encp = self._rd(descp + 0xC, 4, 0x323F84)
                if encp is None:
                    return None
                dpp = self.decode(encp)
                if dpp:
                    encp2 = self._rd(self.mq(DESCP_A) + 0xC, 4,
                                     0x323F98)
                    if encp2 is None:
                        return None
                    basep2 = self.decode(encp2) & 0xFFFFFFFF
                    pstr = self.mw(self.mq(DESCP_A) + 8)
                    slot = self._rd(rec + 4, 1, 0x323FAB)
                    if slot is None:
                        return None
                    prow = (basep2 + pstr * slot) & 0xFFFFFFFF
                else:
                    prow = 0
            else:
                prow = 0
            idx = self.rowsrch(prow, idv & 0xFFFF)
            if idx is None:
                return None
            n = self.popcnt(rec)
            if n is None:
                return None
            # setl: signed compare idx < n (both fit easily)
            si = idx - 0x100000000 if idx & 0x80000000 else idx
            sn = n - 0x100000000 if n & 0x80000000 else n
            return 1 if si < sn else 0
        # ordinary: tail-jmp PREREQ(rec, 1, idv)
        return self.prereq(rec, 1, idv, vsp)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry, rcx = step[0], step[1]
        rdx = step[2] if len(step) > 2 else 0
        r8 = step[3] if len(step) > 3 else 0
        vsp = STACK + 0x80000
        if entry == MAIN:
            m._rax = m.main(rcx, rdx, vsp)
        elif entry == PREREQ:
            m._rax = m.prereq(rcx, rdx, r8, vsp)
        elif entry == POPCNT:
            m._rax = m.popcnt(rcx)
        elif entry == ROWSRCH:
            m._rax = m.rowsrch(rcx, rdx)
        elif entry == VALID:
            m._rax = m.valid(rcx, rdx)
        elif entry == DECODE:
            m._rax = m.decode(rcx)
        elif entry == BUILDER:
            m._rax = m.builder(rcx, rdx, r8)
        elif entry == CLS1:
            m._rax = m.cls1(rcx)
        elif entry == CLS2:
            m._rax = m.cls2(rcx)
        else:
            raise KeyError("no model entry %x" % entry)
        if m._rax is not None:
            m.rets.append(m._rax & 0xFFFFFFFFFFFFFFFF)
        else:
            m.rets.append(m._fault_rax & 0xFFFFFFFFFFFFFFFF)
        m.ends.append(m.fault_end)
    mem = {}
    for addr, n in case.get("watch", []):
        try:
            mem["%x" % addr] = bytes(
                m.mem.get(addr + i, 0) for i in range(n)).hex()
        except KeyError:
            mem["%x" % addr] = None
    return {"trace": m.trace, "faults": m.faults,
            "rets": m.rets, "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

def cases():
    cs = {}
    # node 3 kind=9 (cls1==1) carrying id 0x10 -> mask bit 3;
    # node 5 kind=14 (cls1==1) also carries 0x10 -> bit 5;
    # node 2 kind=1 (cls1==0) carrying 0x10 -> ignored
    base_nodes = dict(nrows=8, nrecs=[
        (0, []), (0, []), (1, [0x10]), (9, [0x10]), (0, []),
        (14, [0x10, 0x22]), (0, []), (0, [])])
    # ---- MAIN I1 exits ----
    cs["m-badid"] = dict(steps=[(MAIN, REC, 0x9999)],
                         vcount=0x100)
    cs["m-nullrec"] = dict(steps=[(MAIN, 0, 0x10)])
    cs["m-kind"] = dict(steps=[(MAIN, REC, 0x10)], rec_kind=1)
    cs["m-slot7"] = dict(steps=[(MAIN, REC, 0x10)], rec_slot=7)
    cs["m-slot255"] = dict(steps=[(MAIN, REC, 0x10)], rec_slot=0xFF)
    # ---- I3 escape hatch ----
    cs["m-esc"] = dict(steps=[(MAIN, REC, 0x10)],
                       arows={0x10: 0x2000})
    cs["m-escneg"] = dict(steps=[(MAIN, REC, 0x10)],
                          arows={0x10: 0x1000}, **base_nodes)
    # ---- I4 ordinary path (PREREQ) ----
    # own bit 3 -> licensed
    cs["m-own3"] = dict(steps=[(MAIN, REC, 0x10)],
                        mask=bytes([8]) + bytes(45), **base_nodes)
    # own bit 5 -> licensed (OR across nodes)
    cs["m-own5"] = dict(steps=[(MAIN, REC, 0x10)],
                        mask=bytes(5) + bytes([0x20]) + bytes(40),
                        **base_nodes)
    # own neither -> 0
    cs["m-own0"] = dict(steps=[(MAIN, REC, 0x10)],
                        mask=bytes(46), **base_nodes)
    # own an unrelated node -> 0
    cs["m-ownx"] = dict(steps=[(MAIN, REC, 0x10)],
                        mask=bytes([1]) + bytes(45), **base_nodes)
    # kind-filtered node carrying the id still yields bit 3/5 only
    cs["m-kindflt"] = dict(steps=[(MAIN, REC, 0x10)],
                           mask=bytes([4]) + bytes(45), **base_nodes)
    # ---- I5 Quickening ----
    prows = {0: (0xD0, 0xD1, 0xD2), 1: (0xD3, 0xD4, 0xD5)}
    cs["m-q0"] = dict(steps=[(MAIN, REC, 0xD0)], prows=prows,
                      rec_slot=0, mask=bytes(46))
    cs["m-q1"] = dict(steps=[(MAIN, REC, 0xD0)], prows=prows,
                      rec_slot=0, mask=bytes([1]) + bytes(45))
    cs["m-q2"] = dict(steps=[(MAIN, REC, 0xD1)], prows=prows,
                      rec_slot=0, mask=bytes([3]) + bytes(45))
    cs["m-q2lo"] = dict(steps=[(MAIN, REC, 0xD1)], prows=prows,
                        rec_slot=0, mask=bytes([1]) + bytes(45))
    cs["m-qabsent9"] = dict(steps=[(MAIN, REC, 0xD9)], prows=prows,
                            rec_slot=0,
                            mask=bytes([0x3F]) + bytes([7]) +
                            bytes(44))   # 6+3 bits -> n=9
    # over-permission edge: absent id, count=4 -> idx3 < 4 -> 1
    cs["m-qabsent4"] = dict(steps=[(MAIN, REC, 0xD9)], prows=prows,
                            rec_slot=0,
                            mask=bytes([0x0F]) + bytes(45))
    # absent id, count=3 -> idx3 < 3 -> 0
    cs["m-qabsent3x"] = dict(steps=[(MAIN, REC, 0xD9)], prows=prows,
                             rec_slot=0,
                             mask=bytes([0x07]) + bytes(45))
    cs["m-qslot1"] = dict(steps=[(MAIN, REC, 0xD4)], prows=prows,
                          rec_slot=1, mask=bytes([7]) + bytes(45))
    # bits past 17 do NOT count (popcount pins 0..17)
    cs["m-qhi"] = dict(steps=[(MAIN, REC, 0xD0)], prows=prows,
                       rec_slot=0,
                       mask=bytes(3) + bytes([0xFF]) + bytes(42))
    # boundary ids 0xD0 / 0xE1 / 0xE2-not-quickening
    cs["m-qe1"] = dict(steps=[(MAIN, REC, 0xE1)], prows=prows,
                       rec_slot=0, mask=bytes([7]) + bytes(45))
    cs["m-e2-ord"] = dict(steps=[(MAIN, REC, 0xE2)], prows=prows,
                          rec_slot=0, mask=bytes(46), **base_nodes)
    # I5-beats-I4 flank: id 0xE1 IS licensed via I4 (node owns it)
    # but the Quickening path runs first and idx3>=n -> 0
    cs["m-qflank"] = dict(steps=[(MAIN, REC, 0xE1)], prows=prows,
                          rec_slot=0, mask=bytes([1]) + bytes(45),
                          nrows=1, nrecs=[(9, [0xE1])])
    # ---- null-table paths ----
    # null action DESC is unreachable past the validator — VALID
    # reads the same 0x2EBF138 cell and rejects first -> ret 0.
    cs["m-nulla"] = dict(steps=[(MAIN, REC, 0x10)], desca=0)
    # null ROW: enc = -BASEP -> decode gives rax=2^32 (nonzero) but
    # low32 row base = 0; id=0 -> row=0 -> test w[0x2C] faults.
    cs["m-nullrow"] = dict(steps=[(MAIN, REC, 0)],
                           enca=(-BASEP) & 0xFFFFFFFF)
    # null party desc -> prow=0 -> rowsrch treats row 0 as absent ->3
    cs["m-nullp"] = dict(steps=[(MAIN, REC, 0xD0)], descp=0)
    # ---- direct bodies ----
    cs["d-pop0"] = dict(steps=[(POPCNT, REC)], mask=bytes(46))
    cs["d-pop1"] = dict(steps=[(POPCNT, REC)],
                        mask=bytes([1]) + bytes(45))
    cs["d-pop18"] = dict(steps=[(POPCNT, REC)],
                         mask=bytes([7]) + bytes([0xFF]) +
                         bytes([3]) + bytes(43))
    cs["d-popover"] = dict(steps=[(POPCNT, REC)],
                           mask=bytes(3) + bytes([0xFF] * 10) +
                           bytes(33))
    cs["d-rows0"] = dict(steps=[(ROWSRCH, BASEP + 0x1000, 0xD0)],
                         prows={0: (0xD0, 0xD1, 0xD2)})
    cs["d-rows2"] = dict(steps=[(ROWSRCH, BASEP + 0x1000, 0xD2)],
                         prows={0: (0xD0, 0xD1, 0xD2)})
    cs["d-rows3"] = dict(steps=[(ROWSRCH, BASEP + 0x1000, 0xEE)],
                         prows={0: (0xD0, 0xD1, 0xD2)})
    cs["d-rowsnull"] = dict(steps=[(ROWSRCH, 0, 0xFFFE)])
    cs["d-valid-ok"] = dict(steps=[(VALID, 0x14, 0x21F)],
                            vcount=0x220)
    cs["d-valid-edge"] = dict(steps=[(VALID, 0x14, 0x21F)],
                              vcount=0x220)
    cs["d-valid-hi"] = dict(steps=[(VALID, 0x14, 0x220)],
                            vcount=0x220)
    cs["d-valid-cls0"] = dict(steps=[(VALID, 0, 1)])
    cs["d-valid-cls33"] = dict(steps=[(VALID, 33, 1)])
    cs["d-valid-nulld"] = dict(steps=[(VALID, 0x14, 5)], desca=0)
    cs["d-valid-a0"] = dict(steps=[(VALID, 0x14, 0x21F)],
                            vcount=0x220, astride=0)
    cs["d-decode"] = dict(steps=[(DECODE, 0x1234)])
    cs["d-build"] = dict(steps=[(BUILDER, 1, 0x10, REC + 0x300)],
                         watch=[(REC + 0x300, 8)], **base_nodes)
    cs["d-build-none"] = dict(steps=[(BUILDER, 1, 0x77,
                                     REC + 0x300)],
                              watch=[(REC + 0x300, 8)], **base_nodes)
    cs["d-build-k2"] = dict(steps=[(BUILDER, 2, 0x10, REC + 0x300)],
                            watch=[(REC + 0x300, 8)],
                            nrows=8, nrecs=[
                                (0, []), (0, []), (1, [0x10]),
                                (15, [0x10]), (0, []), (16, [0x10]),
                                (0, []), (0, [])])
    cs["d-cls1-9"] = dict(steps=[(CLS1, 9)])
    cs["d-cls1-1"] = dict(steps=[(CLS1, 1)])
    cs["d-cls1-14"] = dict(steps=[(CLS1, 14)])
    cs["d-cls1-15"] = dict(steps=[(CLS1, 15)])
    cs["d-cls1-30"] = dict(steps=[(CLS1, 30)])
    cs["d-cls1-0"] = dict(steps=[(CLS1, 0)])
    cs["d-cls1-40"] = dict(steps=[(CLS1, 40)])
    cs["d-prereq"] = dict(steps=[(PREREQ, REC, 1, 0x10)],
                          mask=bytes([8]) + bytes(45), **base_nodes)
    # byte-45-only overlap: the AND loop must scan all 46 bytes
    cs["d-prereq46"] = dict(
        steps=[(PREREQ, REC, 1, 0x10)],
        mask=bytes(45) + bytes([1]),
        nrows=361, nrecs=[(0, [])] * 360 + [(9, [0x10])])
    # requirement id in scan-slot 7 only
    cs["d-build-s7"] = dict(
        steps=[(BUILDER, 1, 0x10, REC + 0x300)],
        watch=[(REC + 0x300, 8)],
        nrows=1, nrecs=[(9, [0, 0, 0, 0, 0, 0, 0, 0x10])])
    # two-step: builder writes mask then prereq reads it — but
    # prereq builds its OWN mask; keep steps independent
    cs["d-two"] = dict(steps=[(POPCNT, REC),
                              (ROWSRCH, BASEP + 0x1000, 0xD1)],
                       prows={0: (0xD0, 0xD1, 0xD2)},
                       mask=bytes([0x1F]) + bytes(45))
    return cs


# ---------------- mutations (verified byte-precise) ----------------
# (name, case, addr, orig_byte, mut_byte) — orig asserted vs image
MUTS = [
    # MAIN exits
    ("m-valid-jne",   "m-own0",    0x323EDD, 0x75, 0x74),   # jne->je
    ("m-kind-jne",    "m-kind",    0x323EFA, 0x85, 0x84),   # 0F85 jne->0F84 je
    ("m-slot-ja",     "m-slot7",   0x323F04, 0x87, 0x86),   # 0F87 ja->0F86 jbe
    ("m-slot6",       "m-slot7",   0x323F02, 0x06, 0x07),   # cmp 6->7
    ("m-esc-je",      "m-esc",     0x323F56, 0x74, 0x75),   # je->jne
    ("m-esc-bit",     "m-esc",     0x323F4F, 0x20, 0x40),   # imm 0x2000->0x4000
    ("m-q-lo",        "m-qflank",  0x323F6F, 0x30, 0x31),   # lea -0xD0->-0xCF
    ("m-q-hi",        "m-qflank",  0x323F75, 0x11, 0x10),   # cmp 0x11->0x10
    ("m-q-ja",        "m-qflank",  0x323F76, 0x77, 0x76),   # ja->jbe
    ("m-q-setl",      "m-qabsent4", 0x323FCF, 0x9C, 0x9D),  # setl->setge
    ("m-q-slotb",     "m-qslot1",  0x323FAE, 0x04, 0x05),   # rec+4 -> +5
    # PREREQ
    ("m-p-and46",     "d-prereq46", 0x323C2A, 0x2E, 0x2D),  # cmp 0x2E
    ("m-p-jne",       "m-own0",    0x323C22, 0x75, 0x74),   # jne->je
    ("m-p-jl",        "d-prereq46", 0x323C2B, 0x7C, 0x7D),  # jl->jge
    ("m-p-kind1",     "d-prereq",  0x323BD2, 0x8B, 0x89),   # mov eax,edx->edx,eax
    # ROWSRCH
    ("m-r-3",         "d-rows3",   0x30A366, 0x03, 0x02),   # cmp 3->2
    ("m-r-ffff",      "d-rowsnull", 0x30A354, 0xFF, 0xFE),  # imm 0xFFFF->0xFFFE
    ("m-r-off4",      "d-rows2",   0x30A350, 0x04, 0x05),   # row+4 -> +5
    ("m-r-je",        "d-rows0",   0x30A35B, 0x74, 0x75),   # je->jne
    # POPCNT
    ("m-c-passes",    "d-pop18",   0x32403B, 0x03, 0x02),   # lea edi,[r9+3]
    ("m-c-add6",      "d-pop1",    0x3240C8, 0x06, 0x05),   # r11+=6 -> +5
    ("m-c-off",       "d-pop1",    0x324053, 0x94, 0x95),   # +0x194 ->+0x195
    # BUILDER
    ("m-b-setb",      "d-build",   0x2F907C, 0x07, 0x06),   # and eax,7 -> &6
    ("m-b-scan8",     "d-build-s7", 0x2F906D, 0x08, 0x07),  # cmp ecx,8->7
    ("m-b-kindjne",   "d-build",   0x2F9051, 0x75, 0x74),   # jne->je
    ("m-b-rowoff5",   "d-build",   0x2F9048, 0x05, 0x06),   # b[row+5]->+6
    ("m-b-reqoff",    "d-build",   0x2F9058, 0x08, 0x09),   # row+8 -> +9
    # VALID
    ("m-v-lea1",      "d-valid-ok", 0x322C5C, 0xFF, 0xFE),  # lea ecx-1->-2
    ("m-v-tail-jl",   "d-valid-ok", 0x323031, 0x8C, 0x8D),  # 0F8C jl->0F8D jge
    ("m-v-tail-jg",   "d-valid-hi", 0x32303C, 0x8F, 0x8E),  # 0F8F jg->0F8E jle
    ("m-v-off4",      "d-valid-a0", 0x322F86, 0x04, 0x05),  # d[desc+4]->+5
    # CLS chain
    ("m-c2-bound",    "d-cls1-30",  0x3241D4, 0x1D, 0x1C),  # cmp 0x1D
    ("m-c1-sub15",    "d-cls1-14",  0x32389B, 0xEB, 0xEC),  # add -0x15->-0x14
    ("m-c1-bound9",   "d-cls1-30",  0x32389E, 0x09, 0x08),  # cmp 9->8
    # DECODE
    ("m-dec-add",     "d-decode",   0x20E602, 0x48, 0x4C),  # REX 48->4C (add r8)
]


def differs(a, b):
    for k in ("trace", "rets", "ends", "faults", "mem"):
        if a[k] != b[k]:
            return "%s: %s != %s" % (k, a[k], b[k])
    return None


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    native = w.obs()
    model = run_model(case, raw, secs)
    return native, model, differs(native, model)


def main():
    raw, secs = load_image()
    cs = cases()
    fails = {}
    for name in sorted(cs):
        native, model, diff = run_case(name, cs[name], raw, secs)
        if diff:
            fails[name] = diff
    print("functional: %d/%d" % (len(cs) - len(fails), len(cs)))
    for name, diff in sorted(fails.items()):
        print("  FAIL %s: %s" % (name, diff))
    mkilled, msurv = [], []
    for mname, cname, addr, orig, mut in MUTS:
        base = dict(cs[cname])
        ob = img_rd(raw, secs, addr, 1)[0]
        assert ob == orig, \
            "%s: byte %x is %02x not %02x" % (mname, addr, ob, orig)
        base["patch_bytes"] = [(addr, bytes([mut]))]
        native, model, diff = run_case(mname, base, raw, secs)
        if diff:
            mkilled.append(mname)
        else:
            msurv.append(mname)
    print("mutants: %d/%d killed" % (len(mkilled), len(MUTS)))
    for mname in msurv:
        print("  SURVIVED %s" % mname)
    res = {"functional_total": len(cs),
           "functional_pass": len(cs) - len(fails),
           "functional_fail": sorted(fails),
           "mutants_total": len(MUTS),
           "mutants_killed": len(mkilled),
           "mutants_survived": msurv}
    with open(RESULT, "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)
    sys.exit(1 if (fails or msurv) else 0)


if __name__ == "__main__":
    main()
