# EXP-121 exp109-queue-tails-exec — native replay harness.
#
# Executes the EXP-109 thin "subsystem boundary" stubs — a coherent
# item-queue transfer pipeline plus four resolver/clear tails, all
# over SHIPPED globals (image addresses, planted per case):
#
#   C140 0036C140  83B — pop: spin while d[QCOUNT]<=0; count--;
#        stage entry {w+0,b+2,b+3,q+8} into 4 globals; ret=b3.
#   C1D0 0036C1D0  21B — r9=q[rsp+4]-5 (caller-stack trick), r8d=0,
#        jmp C1F0 (lane-0 push).
#   C1F0 0036C1F0 150B — push: spin while lane count>=0x1F; entry =
#        QBASE+(lane*32+cnt)*16 gets STAGED {w,b2,q8,b3}; count++;
#        staging <- {zx(b[QBYTE+ecx]), edx, r9}; ret=tag byte.
#   E070/35EA30   — scripted (deep poll-loop callees)
#   E400 0032E400  79B — idx==0xFF->-1; ptr=q[PTAB+sx32(idx)*8];
#        null or rdx>=0x400 -> DE70->2DF960 2D fallback;
#        else d[ptr+rdx*4]; eax>0 rounds UP to 64.
#   DE70 0046DE70   6B — jmp 2DF960
#   T2D 002DF960   11B — d[T2DB + (sx32(ecx)*0x1388 + sx32(edx))*4]
#   CLR  00512EF0  50B — 3 flag bytes=0; 32x {b[t+i*0x10]&=0xF0;
#        b[t-3+i*0x10]=i} over shipped table
#   E520 0032E520 107B — ecx!=0: ret=(FLAG()!=0)|(q[POLLQ]!=0);
#        ecx==0: poll loop {E070(0); if POLLQ!=0 -> 35EA30; else
#        FLAG(); ==0 -> ret 0; else 35EA30} — converges when the
#        scripted callee settles the shipped globals
#   FLAG 0046DFE0  18B — d[FLAGG]==-1 -> 2 else 0
#
# Scripted boundaries (planted returns, args traced):
#   E070 0032E070, EA30 0035EA30 — poll-loop callees; the scripted
#   side may settle POLLQ/FLAGG after N calls (disclosed injection).

import ctypes
import hashlib
import json
import struct
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, \
    UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9, \
    UC_X86_REG_RSP, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

C140 = 0x0036C140
C1D0 = 0x0036C1D0
C1F0 = 0x0036C1F0
E400 = 0x0032E400
DE70 = 0x0046DE70
T2D  = 0x002DF960
CLR  = 0x00512EF0
E520 = 0x0032E520
FLAG = 0x0046DFE0
E070 = 0x0032E070   # scripted boundary
EA30 = 0x0035EA30   # scripted boundary

SPIN_POP  = 0x36C150   # C140 empty-queue spin site
SPIN_PUSH = 0x36C211   # C1F0 full-lane spin site

# shipped globals (image addresses)
QCOUNT = 0x22D89C0     # d: queue count (pop source, push lane 0)
QBASE  = 0x22D89D0     # 16B-stride entries {w+0,b+2,b+3,q+8}
QBYTE  = 0x22D89A8     # b[+ecx] push tag byte
ST_W   = 0x22D89BC     # d: staged word
ST_B2  = 0x22D8E18     # d: staged byte2
ST_Q   = 0x22D8E20     # q: staged qword
ST_B3  = 0x22D8E28     # d: staged byte3
FLAGG  = 0x215EFF4     # d: state flag (-1 -> FLAG()=2)
POLLQ  = 0x22C51C0     # q: poll-gate global
PTAB   = 0x22C51F0     # q[8]-stride pointer table (E400)
T2DB   = 0x2EC3EE0     # 2D fallback dword table (row 0x1388)
CLRT   = 0x2CA81FF     # CLR and-lane base (0x10 stride, 32 iters)
CLRF1  = 0x2CA83F0     # CLR flag byte 1
CLRF2  = 0x2EBA481     # CLR flag byte 2
CLRF3  = 0x2EBA480     # CLR flag byte 3

# planted fixture addresses
PDW    = HEAP + 0x200000          # E400 ptr-target dwords
ARENA  = HEAP + 0x600000


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def ww(v): return struct.pack("<H", v & 0xFFFF)


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


def img_byte(raw, secs, va):
    try:
        return img_rd(raw, secs, va, 1)[0]
    except KeyError:
        return 0      # .bss / outside raw data reads as zero


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b""):
        buf = ctypes.create_string_buffer(size)
        if init:
            ctypes.memmove(buf, init, min(len(init), size))
        self.bufs.append(buf)
        self.uc.mem_map_ptr(addr, size, UC_PROT_ALL, ctypes.addressof(buf))
        self.regions.append((addr, size, ctypes.addressof(buf)))
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        raise KeyError("fixture access to unmapped guest addr %x" % addr)
    def w(self, addr, data):
        ctypes.memmove(self._ptr(addr, len(data)), bytes(data), len(data))
    def r(self, addr, n):
        return ctypes.string_at(self._ptr(addr, n), n)
    def qw(self, addr):
        return struct.unpack("<Q", self.r(addr, 8))[0]
    def dw(self, addr):
        return struct.unpack("<I", self.r(addr, 4))[0]


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # queue: count, 16B entries, staging, tag bytes
    W.append((QCOUNT, dw(case.get("qcount", 0) & 0xFFFFFFFF)))
    for l, c in case.get("qlane", {}).items():
        W.append((QCOUNT + l * 4, dw(c & 0xFFFFFFFF)))
    for i, e in case.get("qent", {}).items():
        el = QBASE + i * 16
        W.append((el + 0, ww(e.get("w", 0))))
        W.append((el + 2, bytes([e.get("b2", 0) & 0xFF])))
        W.append((el + 3, bytes([e.get("b3", 0) & 0xFF])))
        W.append((el + 8, qw(e.get("q8", 0))))
    stg = case.get("stg")
    if stg is not None:
        W.append((ST_W, dw(stg.get("w", 0) & 0xFFFFFFFF)))
        W.append((ST_B2, dw(stg.get("b2", 0) & 0xFFFFFFFF)))
        W.append((ST_Q, qw(stg.get("q8", 0))))
        W.append((ST_B3, dw(stg.get("b3", 0) & 0xFFFFFFFF)))
    for i, b in case.get("qbyte", {}).items():
        W.append((QBYTE + i, bytes([b & 0xFF])))
    # flag / poll globals
    W.append((FLAGG, dw(case.get("flag", 0) & 0xFFFFFFFF)))
    W.append((POLLQ, qw(case.get("pollq", 0))))
    # E400: pointer table + planted target dwords + 2D table
    for i, p in case.get("ptab", {}).items():
        W.append((PTAB + i * 8, qw(p)))
    for k, v in case.get("pdw", {}).items():
        W.append((PDW + k * 4, dw(v & 0xFFFFFFFF)))
    for k, v in case.get("t2d", {}).items():
        W.append((T2DB + k * 4, dw(v & 0xFFFFFFFF)))
    # CLR touch region: and-lane + (-3)-lane + 3 flags
    clr = case.get("clr")
    if clr:
        for i, v in clr.get("and", {}).items():
            W.append((CLRT + i * 0x10, bytes([v & 0xFF])))
        for i, v in clr.get("m3", {}).items():
            W.append((CLRT - 3 + i * 0x10, bytes([v & 0xFF])))
        W.append((CLRF1, bytes([clr.get("f1", 0) & 0xFF])))
        W.append((CLRF2, bytes([clr.get("f2", 0) & 0xFF])))
        W.append((CLRF3, bytes([clr.get("f3", 0) & 0xFF])))
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
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.ea30_calls = 0
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr in (E070, EA30):
            name = "e070" if addr == E070 else "35ea"
            self.trace.append("%s:%x" %
                              (name, uc.reg_read(UC_X86_REG_RCX)))
            if addr == EA30:
                self.ea30_calls += 1
                st = self.case.get("settle")
                if st and self.ea30_calls >= st["after"]:
                    for a, d in st["writes"]:
                        self.gm.w(a, d)
            uc.reg_write(UC_X86_REG_RAX, 0)
            uc.reg_write(UC_X86_REG_RIP,
                         self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.emu_stop()
        return True

    def run_one(self, entry, rcx, rdx=0, r8=0, r9=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        self.gm.w(rsp + 8, dw(self.case.get("stack8", 0)))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        uc.reg_write(UC_X86_REG_R8, r8)
        uc.reg_write(UC_X86_REG_R9, r9)
        try:
            uc.emu_start(entry, RETQ, count=20000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))
        self.ends.append(uc.reg_read(UC_X86_REG_RIP))

    def run(self):
        for step in self.case.get("steps", []):
            self.run_one(*step)

    def obs(self):
        mem = {}
        for a, n in self.case.get("watch", []):
            mem["%x" % a] = self.gm.r(a, n).hex()
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "ends": self.ends, "mem": mem}


# ---------------- python model ----------------
# the model interprets the same planted fixture bytes; reads not
# planted fall back to shipped image bytes (mirroring the mapped
# image), then to zero.

def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


class Model:
    def __init__(self, case, raw, secs):
        self.case, self.raw, self.secs = case, raw, secs
        self.mem, self.written = {}, set()
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
                self.written.add(addr + i)
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.ea30_calls = 0

    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            return img_byte(self.raw, self.secs, a)
        return 0

    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)

    def stb(self, a, v):
        self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def stw(self, a, v):
        self.stb(a, v); self.stb(a + 1, v >> 8)
    def std(self, a, v):
        for i in range(4): self.stb(a + i, v >> (i * 8))
    def stq(self, a, v):
        for i in range(8): self.stb(a + i, v >> (i * 8))

    # ---- bodies ----
    def flag(self):
        return 2 if sx32(self.md(FLAGG)) == -1 else 0

    def pop(self):
        """0036C140 — ret = staged b3; spins on empty."""
        cnt = sx32(self.md(QCOUNT))
        if cnt <= 0:
            return ("spin", SPIN_POP)
        cnt -= 1
        self.std(QCOUNT, cnt)
        el = QBASE + cnt * 16
        self.std(ST_W, self.mw(el))
        self.std(ST_B2, self.mb(el + 2))
        self.stq(ST_Q, self.mq(el + 8))
        self.std(ST_B3, self.mb(el + 3))
        return ("ret", self.mb(el + 3))

    def push(self, ecx, edx, lane, r9):
        """0036C1F0 — ret = tag byte; spins on lane full."""
        lane = sx32(lane)
        cnt = sx32(self.md(QCOUNT + lane * 4))
        if cnt >= 0x1F:
            return ("spin", SPIN_PUSH)
        el = QBASE + (lane * 32 + cnt) * 16
        self.stw(el, self.mw(ST_W))
        self.stb(el + 2, self.mb(ST_B2))
        self.stq(el + 8, self.mq(ST_Q))
        self.stb(el + 3, self.mb(ST_B3))
        self.std(QCOUNT + lane * 4, cnt + 1)
        self.std(ST_B2, edx & 0xFFFFFFFF)
        self.stq(ST_Q, r9)
        tag = self.mb((QBYTE + sx32(ecx)) & 0xFFFFFFFFFFFFFFFF)
        self.std(ST_W, tag)
        return ("ret", tag)

    def push_c1d0(self, ecx, edx, stack8):
        """0036C1D0 — r9 = q[rsp+4]-5 = (stack8<<32)-5; lane 0."""
        r9 = ((stack8 & 0xFFFFFFFF) << 32) - 5
        return self.push(ecx, edx, 0, r9 & 0xFFFFFFFFFFFFFFFF)

    def r400(self, ecx, rdx):
        """0032E400 — the PRIMARY path returns raw eax at 0x32E430;
        only the DE70 fallback and 0xFF arm reach the round-to-64.
        All arms return eax -> rax is zero-extended."""
        if (ecx & 0xFFFFFFFF) == 0xFF:
            return 0xFFFFFFFF
        ptr = self.mq((PTAB + sx32(ecx) * 8) & 0xFFFFFFFFFFFFFFFF)
        if ptr != 0 and rdx < 0x400:
            return self.md((ptr + rdx * 4) & 0xFFFFFFFFFFFFFFFF) \
                & 0xFFFFFFFF
        # DE70 -> T2D: d[T2DB + (sx32(ecx)*0x1388 + sx32(edx))*4]
        k = sx32(ecx) * 0x1388 + sx32(rdx)
        eax = sx32(self.md((T2DB + k * 4) & 0xFFFFFFFFFFFFFFFF))
        if eax > 0:
            # add 0x3F; cdq; and edx,0x3F (sign adjust); add; mask
            v = (eax + 0x3F) & 0xFFFFFFFF
            adj = 0x3F if v & 0x80000000 else 0
            eax = (v + adj) & 0xFFFFFFC0
        return eax & 0xFFFFFFFF

    def clr(self):
        """00512EF0 — writes only."""
        self.stb(CLRF1, 0); self.stb(CLRF2, 0); self.stb(CLRF3, 0)
        for i in range(0x20):
            a = CLRT + i * 0x10
            self.stb(a, self.mb(a) & 0xF0)
            self.stb(a - 3, i)
        return ("ret", CLRT + 0x200)   # rax = lea result past the loop

    def e520(self, ecx):
        """0032E520 — nonzero arm OR poll loop (scripted callees)."""
        if ecx != 0:
            ebx = 1 if self.mq(POLLQ) != 0 else 0
            dil = 1 if self.flag() != 0 else 0
            return ("ret", ebx | dil)
        for _ in range(64):                 # poll loop cap
            self.trace.append("e070:0")
            if self.mq(POLLQ) != 0:
                self.trace.append("35ea:0")
                self._settle()
                continue
            if self.flag() == 0:
                return ("ret", 0)
            self.trace.append("35ea:0")
            self._settle()
        return ("ret", 0)                   # unreachable w/ settle

    def _settle(self):
        self.ea30_calls += 1
        st = self.case.get("settle")
        if st and self.ea30_calls >= st["after"]:
            for a, d in st["writes"]:
                for i, b in enumerate(d):
                    self.stb(a + i, b)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry = step[0]
        rcx = step[1] & 0xFFFFFFFFFFFFFFFF
        rdx = step[2] & 0xFFFFFFFFFFFFFFFF if len(step) > 2 else 0
        r8 = step[3] & 0xFFFFFFFFFFFFFFFF if len(step) > 3 else 0
        r9 = step[4] & 0xFFFFFFFFFFFFFFFF if len(step) > 4 else 0
        if entry == C140:
            kind, v = m.pop()
            m.rets.append(v if kind == "ret" else None)
            m.ends.append(RETQ if kind == "ret" else v)
        elif entry == C1F0:
            kind, v = m.push(rcx, rdx, r8, r9)
            m.rets.append(v if kind == "ret" else None)
            m.ends.append(RETQ if kind == "ret" else v)
        elif entry == C1D0:
            kind, v = m.push_c1d0(rcx, rdx, case.get("stack8", 0))
            m.rets.append(v if kind == "ret" else None)
            m.ends.append(RETQ if kind == "ret" else v)
        elif entry == FLAG:
            m.rets.append(m.flag()); m.ends.append(RETQ)
        elif entry == E400:
            m.rets.append(m.r400(rcx, rdx)); m.ends.append(RETQ)
        elif entry == T2D:
            k = sx32(rcx) * 0x1388 + sx32(rdx)
            m.rets.append(sx32(m.md(T2DB + k * 4)) &
                          0xFFFFFFFFFFFFFFFF)
            m.ends.append(RETQ)
        elif entry == CLR:
            kind, v = m.clr()
            m.rets.append(v); m.ends.append(RETQ)
        elif entry == E520:
            kind, v = m.e520(rcx)
            m.rets.append(v); m.ends.append(RETQ)
    mem = {}
    for a, n in case.get("watch", []):
        mem["%x" % a] = "".join("%02x" % m.mb(a + i) for i in range(n))
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "ends": m.ends, "mem": mem}


# ---------------- cases ----------------

WATCH_STG = [(ST_W, 4), (ST_B2, 4), (ST_Q, 8), (ST_B3, 4),
             (QCOUNT, 4)]
ENT1 = {"w": 0x1234, "b2": 0x56, "b3": 0x78, "q8": 0x9ABCDEF0}
ENT0 = {"w": 0xAAAA, "b2": 0x11, "b3": 0x22, "q8": 0x7777}


def build_cases():
    C = {}
    # ---- pop ----
    C["pop-basic"] = {"qcount": 2, "qent": {0: ENT0, 1: ENT1},
                      "watch": WATCH_STG, "steps": [(C140, 0, 0)]}
    C["pop-last"] = {"qcount": 1, "qent": {0: ENT1},
                     "watch": WATCH_STG, "steps": [(C140, 0, 0)]}
    C["pop-empty"] = {"qcount": 0, "steps": [(C140, 0, 0)]}
    C["pop-neg"] = {"qcount": 0xFFFFFFFF, "steps": [(C140, 0, 0)]}
    # ---- push via C1D0 (lane 0, caller-stack r9) ----
    C["push-basic"] = {"qcount": 3,
                       "qent": {3: {"w": 0, "b2": 0, "b3": 0, "q8": 0}},
                       "stg": dict(ENT1), "qbyte": {5: 0x77},
                       "stack8": 0x41414141,
                       "watch": WATCH_STG + [(QBASE + 3 * 16, 16)],
                       "steps": [(C1D0, 5, 0xBEEF, 0, 0)]}
    # ---- push via C1F0 (direct lane) ----
    C["push-lane2"] = {"qlane": {2: 1},
                       "qent": {65: {"w": 0, "b2": 0, "b3": 0, "q8": 0}},
                       "stg": dict(ENT1), "qbyte": {0: 0x33},
                       "watch": WATCH_STG +
                                [(QBASE + 65 * 16, 16),
                                 (QCOUNT + 8, 4)],
                       "steps": [(C1F0, 0, 0x22, 2, 0x99)]}
    C["push-full"] = {"qcount": 0x1F, "steps": [(C1D0, 0, 0, 0, 0)]}
    # ---- the pipeline: pop stages, push re-queues ----
    C["pop-push"] = {"qcount": 2, "qent": {0: ENT0, 1: ENT1},
                     "stg": {"w": 0xDEAD, "b2": 0x99, "b3": 0x88,
                             "q8": 0x5555},
                     "qbyte": {0: 0x42},
                     "watch": WATCH_STG + [(QBASE + 16, 16),
                                           (QBASE + 32, 16)],
                     "steps": [(C140, 0, 0), (C1D0, 0, 0x55, 0, 0)]}
    # ---- flag leaf ----
    C["flag-set"] = {"flag": 0xFFFFFFFF, "steps": [(FLAG, 0, 0)]}
    C["flag-clear"] = {"flag": 0, "steps": [(FLAG, 0, 0)]}
    # ---- E400 resolver ----
    C["r400-basic"] = {"ptab": {0: PDW}, "pdw": {5: 0x21},
                       "steps": [(E400, 0, 5)]}      # 0x21 -> 0x40
    C["r400-exact"] = {"ptab": {0: PDW}, "pdw": {5: 0x80},
                       "steps": [(E400, 0, 5)]}      # already 64x
    C["r400-neg"] = {"ptab": {0: PDW}, "pdw": {5: 0xFFFFFFE0},
                     "steps": [(E400, 0, 5)]}        # <=0 verbatim
    C["r400-null"] = {"ptab": {1: 0}, "t2d": {0x1388 + 7: 0x30},
                      "steps": [(E400, 1, 7)]}       # ptr 0 -> 2D
    C["r400-big"] = {"ptab": {0: PDW}, "pdw": {0x400: 0x99},
                     "t2d": {0x400: 0x55},
                     "steps": [(E400, 0, 0x400)]}    # rdx>=0x400
    C["r400-ff"] = {"steps": [(E400, 0xFF, 0)]}      # -> -1
    C["r400-idx1"] = {"ptab": {0: PDW, 1: PDW + 0x100},
                      "pdw": {0x40: 0x10, 0x50: 0x99},
                      "steps": [(E400, 1, 0x10)]}    # lane select
    C["r400-mid"] = {"ptab": {0: PDW}, "pdw": {0x300: 0x10},
                     "t2d": {0x300: 0x77},
                     "steps": [(E400, 0, 0x300)]}    # <0x400 primary
    # ---- CLR ----
    C["clr-planted"] = {"clr": {"and": {0: 0xFF, 1: 0x3C, 31: 0x7F},
                               "m3": {0: 0xAA, 31: 0xBB},
                               "f1": 0x77, "f2": 0x66, "f3": 0x55},
                        "watch": [(CLRT, 4), (CLRT - 3, 4),
                                  (CLRT + 31 * 0x10, 1),
                                  (CLRT + 31 * 0x10 - 3, 1),
                                  (CLRF1, 1), (CLRF2, 1), (CLRF3, 1)],
                        "steps": [(CLR, 0, 0)]}
    C["clr-shipped"] = {"watch": [(CLRT, 4), (CLRT - 3, 4),
                                  (CLRF1, 1), (CLRF2, 1), (CLRF3, 1)],
                        "steps": [(CLR, 0, 0)]}
    # ---- E520 nonzero arm ----
    C["e520-nz-both"] = {"pollq": PDW, "flag": 0,
                         "steps": [(E520, 1, 0)]}   # ebx|dil = 1|1
    C["e520-nz-q0f2"] = {"pollq": 0, "flag": 0,
                         "steps": [(E520, 1, 0)]}   # 0|1 = 1
    C["e520-nz-q1f0"] = {"pollq": PDW, "flag": 0xFFFFFFFF,
                         "steps": [(E520, 1, 0)]}   # 1|0 = 1
    C["e520-nz-none"] = {"pollq": 0, "flag": 0xFFFFFFFF,
                         "steps": [(E520, 1, 0)]}   # 0|0 = 0
    # ---- E520 poll arm (scripted settle disclosed) ----
    # exits when POLLQ==0 AND FLAG()==0 (d[FLAGG]!=-1)
    C["e520-poll-imm"] = {"pollq": 0, "flag": 0,
                          "steps": [(E520, 0, 0)]}
    C["e520-poll-q1"] = {"pollq": PDW, "flag": 0,
                         "settle": {"after": 1,
                                    "writes": [(POLLQ, qw(0)),
                                               (FLAGG, dw(0))]},
                         "steps": [(E520, 0, 0)]}
    C["e520-poll-f2"] = {"pollq": 0, "flag": 0xFFFFFFFF,
                         "settle": {"after": 1,
                                    "writes": [(FLAGG, dw(0))]},
                         "steps": [(E520, 0, 0)]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])

MUTS = [
    # C140: count global disp -> +4 (reads adjacent dword: spins)
    ("m-pop-count", 0x36C142, B(0x7A), B(0x7E), "pop-basic"),
    # C140: jg -> jl (count>0 falls into the spin)
    ("m-pop-jg",    0x36C148, B(0x7F), B(0x7C), "pop-basic"),
    # C140: dec eax -> inc eax (pops entry[count], not count-1)
    ("m-pop-dec",   0x36C153, B(0xC8), B(0xC0), "pop-basic"),
    # C140: staged-b2 disp +2 -> +4
    ("m-pop-b2",    0x36C175, B(0x02), B(0x04), "pop-basic"),
    # C140: staged-q8 disp +8 -> +0x10
    ("m-pop-q8",    0x36C180, B(0x08), B(0x10), "pop-basic"),
    # C1F0: jl -> jge (non-full lane spins)
    ("m-push-jl",   0x36C20F, B(0x7C), B(0x7D), "push-basic"),
    # C1F0: shl r10,5 -> shl r10,4 (lane*16 not *32)
    ("m-push-lane", 0x36C21D, B(0x05), B(0x04), "push-lane2"),
    # C1F0: staged-b2 write disp -> +4 (wrong staging field)
    ("m-push-st2",  0x36C267, B(0xAD), B(0xB1), "push-basic"),
    # C1F0: count+1 -> count+2
    ("m-push-inc",  0x36C25D, B(0x01), B(0x02), "push-basic"),
    # C1F0: tag byte table disp A8 -> A0
    ("m-push-tag",  0x36C276, B(0xA8), B(0xA0), "push-basic"),
    # C1D0: sub r9,5 -> sub r9,4 (caller-stack value off by 1)
    ("m-c1d0-sub5", 0x36C1DE, B(0x05), B(0x04), "push-basic"),
    # C1D0: [r9+4] -> [r9+8] (reads past the stack trick)
    ("m-c1d0-rsp4", 0x36C1DA, B(0x04), B(0x08), "push-basic"),
    # E400: idx==0xFF -> 0xFE (sentinel misses)
    ("m-r400-ff",   0x32E406, B(0xFF), B(0xFE), "r400-ff"),
    # E400: ptab stride *8 -> *4 (misaligned lane read)
    ("m-r400-str8", 0x32E419, B(0xC0), B(0x80), "r400-idx1"),
    # E400: bound 0x400 -> 0x200 (0x300 falls to 2D path)
    ("m-r400-bnd",  0x32E423, B(0x04), B(0x02), "r400-mid"),
    # E400: table dword stride *4 -> *8
    ("m-r400-str4", 0x32E42B, B(0x90), B(0xD0), "r400-basic"),
    # E400: jle -> jmp (rounding skipped entirely)
    ("m-r400-jle",  0x32E43D, B(0x7E), B(0xEB), "r400-null"),
    # E400: round mask ~0x3F -> ~0x7F
    ("m-r400-mask", 0x32E44A, B(0xC0), B(0x80), "r400-null"),
    # T2D: row stride 0x1388 -> 0x1390
    ("m-2d-row",    0x2DF966, B(0x88), B(0x90), "r400-null"),
    # FLAG: cmove -> cmovne (-1 yields 0)
    ("m-flag-cmv",  0x46DFEF, B(0x44), B(0x45), "flag-set"),
    # E520: setne -> sete (nonzero POLLQ reads as zero; needs
    # the ebx=1,dil=0 case to discriminate)
    ("m-e520-sne",  0x32E53E, B(0x95), B(0x94), "e520-nz-both"),
    # E520: xor edi,1 -> xor edi,0 (dil stays raw)
    ("m-e520-xor",  0x32E54D, B(0x01), B(0x00), "e520-nz-q0f2"),
]


def run_native(case, raw, secs):
    w = World(case, raw, secs)
    w.run()
    return w.obs()


def differs(k, nv, mv):
    if k == "rets":
        if len(nv) != len(mv):
            return True
        return any(m is not None and n != m for n, m in zip(nv, mv))
    if k == "faults":
        naddrs = sorted(t[1] if isinstance(t[1], int) else -1
                        for t in nv)
        return naddrs != sorted(mv)
    return nv != mv


def main():
    raw, secs = load_image()
    cases = build_cases()
    keys = ("trace", "rets", "ends", "mem", "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case, raw, secs)
        mod = run_model(case, raw, secs)
        d = [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:180])
                print("  mod:", str(mod.get(k))[:180])
    print("functional: %d/%d" % (len(cases) - fails, len(cases)))

    for mid, va, orig, mut, cname in MUTS:
        got = img_rd(raw, secs, va, len(orig))
        if got != orig:
            results["bad_sites"].append((mid, hex(va), got.hex()))
            print("BAD SITE", mid, hex(va), "want", orig.hex(),
                  "got", got.hex())
    if results["bad_sites"]:
        print("aborting mutant run — fix sites first")
        json.dump(results, open(RESULT, "w"), indent=1)
        return

    alive = 0
    for mid, va, orig, mut, cname in MUTS:
        case = dict(cases[cname])
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + \
            [(va, mut)]
        try:
            nat = run_native(case, raw, secs)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case, raw, secs)
        if [k for k in keys if k in nat and differs(k, nat[k], mod.get(k))]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
