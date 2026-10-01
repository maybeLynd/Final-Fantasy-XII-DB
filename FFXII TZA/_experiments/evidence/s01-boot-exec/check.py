# S-01 boot-exec — isolated original-code runs answering three FABLE
# requests (FABLE-REQ-ORACLE-S01-TIMING-BOOTSTRAP-BOTH-BRANCHES,
# FABLE-REQ-ORACLE-S01-GENERATOR-SEEDING-WITH-AN-EXTERNAL-GROUND-TRUTH,
# FABLE-REQ-ORACLE-S01-MEMORY-BUDGET-ELEVEN-ALLOCATIONS). Shipped bytes
# execute under Unicorn; the only scripted boundaries are PE-import
# calls (WINMM timeGetDevCaps/timeBeginPeriod/timeEndPeriod, CRT
# malloc, CRT thunk 00861F5C) which the image cannot resolve, plus the
# pre-battery span of 0022A0B0 which is outside the requested scope.
#
#   TIMING 001EDDC0 (165 B): ecx!=0 -> float[1DFE0B8]=2.0f,
#            float[1DFE0BC]=0.5f, d[1F82E38]=1, d[1DFE0B4]=2, call
#            LUT battery 0033F020, IF b[1F82E3C]: ecx=d[1F82E40],
#            b[1F82E3C]=0, timeEndPeriod. ecx==0 -> timeGetDevCaps(
#            rsp+0x38, 8); eax==0 -> d[1F82E40]=wPeriodMin (low dword
#            of caps), timeBeginPeriod(period), b[1F82E3C]=1. Both:
#            calls 0032AE70, 003333D0, 00337A00; tail-jmp 002BDA90.
#   SEED   00863D30 (69 B): if !b[2EB4234]: local q[+38]=vtable
#            01CCFAC8, call 00866D60(&local, 0x1571); b[2EB4234]=1;
#            call 00866D60(&local, ecx). 00866D60 (67 B): textbook
#            mt19937 init: state[0]=edx at 02EB3870, state[i]=
#            0x6C078965*(state[i-1]^(state[i-1]>>30))+i for i<0x270,
#            d[02EB4230]=0x270. First arg never dereferenced.
#   MEM    0022A0B0 span 0022A1DC..0022A399: eleven mov ecx,imm +
#            call 0036D240 (= movsxd rcx,ecx; r8=-1; edx=0; jmp
#            0085E730 -> IAT malloc), each rax -> a q[] global, then
#            nine 00369D30(ptr, base_size, tail, idx) registrations
#            for the nine tailed sizes; 0x80000 and 0x100000 are
#            unregistered. 00369D30 ledger[ecx] (0xA8 rec at
#            02D989A0+idx*0xA8) zeroes the block head q[0..0x38] and
#            writes bookkeeping stores confined to the block HEAD
#            (observed offsets 0..~0x783C, proportional to size);
#            the +0x10/+0x100/+0x400 tail bytes are headroom for
#            that head-resident ledger — the END of the allocation
#            is never written (executed finding; corrects the
#            earlier static reading that placed slot records in
#            the tail).

import ctypes
import hashlib
import json
import os
import struct
import sys

from unicorn import *
from unicorn.x86_const import *

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x30A0000
HEAP = 0x40000000
POOLSPACE = 0x44000000          # bump-allocator region for malloc stub
STACK = 0x61000000
RETQ = 0x62000000

TIMING = 0x1EDDC0
SEED = 0x863D30
MTINIT = 0x866D60
MEMBAT = 0x22A1DC               # first mov ecx of the battery
MEMEND = 0x22A399               # insn after last 0x369D30 call
ALLOC = 0x36D240                # malloc thunk (runs native)
REG = 0x369D30                  # pool registrar

# timing observables
CELL_B4 = 0x1DFE0B4             # dword frame-base code
CELL_B8 = 0x1DFE0B8             # float scalar
CELL_BC = 0x1DFE0BC             # float scalar
CELL_E38 = 0x1F82E38            # dword gate (fed to 32AE70/1EDE70)
CELL_E3C = 0x1F82E3C            # byte timer flag
CELL_E40 = 0x1F82E40            # dword period
CELLS = [CELL_B4, CELL_B8, CELL_BC, CELL_E38, CELL_E3C, CELL_E40]

# seed observables
MT_ARR = 0x2EB3870              # 624 dwords
MT_IDX = 0x2EB4230
MT_FLAG = 0x2EB4234

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def fw(f): return struct.pack("<f", f)


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


def import_map(raw, secs):
    """IAT cell VA -> 'dll!name'. The cells in the shipped image hold
    loader hints, not callable addresses — every `jmp qword[IAT]`
    thunk must be stubbed."""
    pe = struct.unpack_from("<I", raw, 0x3C)[0]
    optsz = struct.unpack_from("<H", raw, pe + 20)[0]
    magic = struct.unpack_from("<H", raw, pe + 24)[0]
    dd = pe + 24 + (0x70 if magic == 0x20B else 0x60)
    imp_rva = struct.unpack_from("<I", raw, dd + 8)[0]

    def r2o(rva):
        for sva, vs, ra, rs in secs:
            if sva <= rva < sva + max(vs, rs):
                return ra + (rva - sva)
        return None

    out, i = {}, r2o(imp_rva)
    while True:
        oft, ts, fwd, name, ft = struct.unpack_from("<IIIII", raw, i)
        if not (oft or name or ft):
            break
        dll = raw[r2o(name):].split(b"\0")[0].decode("latin1")
        thunk, a = r2o(oft or ft), ft + IMG_LO
        while True:
            val = struct.unpack_from("<Q", raw, thunk)[0]
            if not val:
                break
            if val >> 63:
                nm = "ord%d" % (val & 0xFFFF)
            else:
                hn = r2o(val & 0x7FFFFFFF)
                nm = raw[hn + 2:].split(b"\0")[0].decode("latin1")
            out[a] = "%s!%s" % (dll, nm)
            thunk += 8
            a += 8
        i += 20
    return out


class GuestMem:
    def __init__(self, uc):
        self.uc, self.bufs, self.regions = uc, [], []
    def map(self, addr, size, init=b"", buffered=True):
        if buffered:
            buf = ctypes.create_string_buffer(size)
            if init:
                ctypes.memmove(buf, init, min(len(init), size))
            self.bufs.append(buf)
            self.uc.mem_map_ptr(addr, size, UC_PROT_ALL,
                                ctypes.addressof(buf))
            self.regions.append((addr, size, ctypes.addressof(buf)))
        else:
            self.uc.mem_map(addr, size, UC_PROT_ALL)
    def _ptr(self, addr, n):
        for base, size, ptr in self.regions:
            if base <= addr and addr + n <= base + size:
                return ptr + (addr - base)
        return None
    def w(self, addr, data):
        p = self._ptr(addr, len(data))
        if p is not None:
            ctypes.memmove(p, bytes(data), len(data))
        else:
            self.uc.mem_write(addr, bytes(data))
    def r(self, addr, n):
        p = self._ptr(addr, n)
        if p is not None:
            return ctypes.string_at(p, n)
        return bytes(self.uc.mem_read(addr, n))
    def qw(self, addr): return struct.unpack("<Q", self.r(addr, 8))[0]
    def dw(self, addr): return struct.unpack("<I", self.r(addr, 4))[0]


class World:
    """Native execution with scripted import/boundary stubs only."""
    def __init__(self, case, raw, secs, imports):
        self.case, self.raw, self.secs = case, raw, secs
        self.imports = imports
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        # bump-allocator region: mem_map (lazy zero pages) — 257 MiB of
        # requested pools never get a real ctypes buffer; spot reads go
        # through uc.mem_read. Head/tail scratch windows are pre-dirtied
        # with 0xAA by the stub where needed.
        gm.map(POOLSPACE, 0x12000000, buffered=False)
        for addr, dat in case.get("plant", []):
            gm.w(addr, dat)
        self.calls = []           # ordered (tag, args) at stub/callee entries
        self.writes = []          # (addr,size,pc) inside watched ranges
        self.stub_writes = []     # (addr,size,tag) emulated by CRT stubs
        self.faults = []
        self.rets = []
        self.bump = POOLSPACE + 0x100000
        self.blocks = []          # (ptr,size) returned by malloc stub
        self.depth_tag = ["<top>"]
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self.on_write)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    # --- return-flow helper for stubs --------------------------------
    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def _label(self, rip):
        if REG <= rip < 0x36A000:
            return "reg369d30"
        if 0x36A490 <= rip < 0x36A580:
            return "tailhdr36a490"
        if 0x17D2E0 <= rip < 0x17D3C0:
            return "setup17d2e0"
        if 0x1EDDC0 <= rip < 0x1EDE70:
            return "timing"
        if 0x22A0B0 <= rip < 0x22A400:
            return "battery"
        return hex(rip)

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, hex(addr),
                          uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    def on_write(self, uc, access, addr, size, value, _):
        for lo, hi in self.case.get("watch", []):
            if lo <= addr < hi:
                self.writes.append((hex(addr), size,
                                    self._label(uc.reg_read(
                                        UC_X86_REG_RIP))))
                return
        for ptr, sz in self.blocks:
            if ptr <= addr < ptr + sz:
                self.writes.append((hex(addr), size,
                                    self._label(uc.reg_read(
                                        UC_X86_REG_RIP))))
                return

    def _iat_stub(self, uc, addr):
        """`ff 15/ff 25 <disp32>` call/jmp through the IAT -> named
        scripted stub. The shipped IAT cells hold loader hints, not
        callable addresses; every import executes here instead."""
        insn = self.gm.r(addr, 8)
        off = 1 if insn[0] in (0x48, 0x4C) else 0
        op = insn[off:off + 2]
        if op not in (b"\xff\x25", b"\xff\x15"):
            return False
        cell = addr + off + 6 + struct.unpack(
            "<i", insn[off + 2:off + 6])[0]
        name = self.imports.get(cell)
        if name is None:
            return False
        short = name.split("!")[1]
        rcx = uc.reg_read(UC_X86_REG_RCX)
        rdx = uc.reg_read(UC_X86_REG_RDX)
        r8 = uc.reg_read(UC_X86_REG_R8)
        if short in ("memcpy", "memmove", "memset"):
            if short == "memset":
                self.gm.w(rcx, bytes([rdx & 0xFF]) * r8)
            else:
                self.gm.w(rcx, self.gm.r(rdx, r8))
            uc.reg_write(UC_X86_REG_RAX, rcx)
            self.calls.append(("iat:" + name, hex(rcx), hex(rdx),
                               hex(r8)))
            # stub-side copies bypass UC_HOOK_MEM_WRITE; log them
            # separately so per-block write accounting stays honest
            self.stub_writes.append((rcx, r8, "iat:" + short))
        elif short == "malloc":
            ptr = self.bump
            self.bump = (self.bump + rcx + 0xFFF) & ~0xFFF
            self.blocks.append((ptr, rcx))
            # pre-dirty head + tail windows so writes stand out
            self.gm.w(ptr, b"\xaa" * min(0x40, rcx))
            self.gm.w(ptr + max(0, rcx - 0x40),
                      b"\xaa" * min(0x40, rcx))
            self.calls.append(("malloc", hex(rcx), hex(ptr)))
            uc.reg_write(UC_X86_REG_RAX, ptr)
        elif short == "timeGetDevCaps":
            caps = self.case.get("caps", (0xBEEF, 0xCAFE))
            self.gm.w(rcx, dw(caps[0]) + dw(caps[1]))
            self.calls.append(("timeGetDevCaps", hex(rcx), rdx))
            uc.reg_write(UC_X86_REG_EAX,
                         self.case.get("caps_ret", 0))
        elif short in ("timeBeginPeriod", "timeEndPeriod"):
            self.calls.append((short, uc.reg_read(UC_X86_REG_ECX)))
            uc.reg_write(UC_X86_REG_EAX, 0)
        else:
            uc.reg_write(UC_X86_REG_RAX, 0)
            self.calls.append(("iat:" + name, hex(rcx), hex(rdx),
                               hex(r8)))
        if op == b"\xff\x25":        # jmp-thunk: caller's ret is on top
            self._ret(uc)
        else:                        # call site: consume the insn
            uc.reg_write(UC_X86_REG_RIP, addr + off + 6)
        return True

    def on_code(self, uc, addr, size, _):
        c = self.case
        # --- generic IAT import boundary -----------------------------
        b0 = self.gm.r(addr, 3)
        if b0[:2] in (b"\xff\x25", b"\xff\x15") or \
                b0[1:3] in (b"\xff\x25", b"\xff\x15"):
            if self._iat_stub(uc, addr):
                return
        # --- call instrumentation ------------------------------------
        if addr in (0x33F020, 0x32AE70, 0x3333D0, 0x337A00, 0x2BDA90,
                    0x369D30, 0x17D2E0, 0x36A490, 0x16D670, 0x20E620,
                    0x16D6A0):
            self.calls.append(("enter%x" % addr,
                               hex(uc.reg_read(UC_X86_REG_RCX)),
                               hex(uc.reg_read(UC_X86_REG_RDX)),
                               hex(uc.reg_read(UC_X86_REG_R8)),
                               hex(uc.reg_read(UC_X86_REG_R9))))
        if addr == MTINIT:
            self.calls.append(("mtinit",
                               uc.reg_read(UC_X86_REG_EDX),
                               hex(uc.reg_read(UC_X86_REG_RCX))))
        if addr == self.case.get("stopat", -1):
            self.rets.append(("stopat", hex(addr)))
            uc.emu_stop()

    def run(self, entry, ecx=0, stop=None):
        self.uc.reg_write(UC_X86_REG_RSP, STACK + 0x80000)
        self.uc.reg_write(UC_X86_REG_RIP, entry)
        self.uc.reg_write(UC_X86_REG_ECX, ecx)
        # return trampoline: function ret lands at RETQ -> emu ends
        self.gm.w(STACK + 0x80000, qw(RETQ))
        self.uc.emu_start(entry, RETQ)


def mt19937(seed):
    """Standard reference — computed from the standard's recurrence,
    not from the image."""
    st = [0] * 624
    st[0] = seed & 0xFFFFFFFF
    for i in range(1, 624):
        st[i] = (0x6C078965 * (st[i - 1] ^ (st[i - 1] >> 30)) + i) \
            & 0xFFFFFFFF
    return st


def read_float(gm, a):
    return struct.unpack("<f", gm.r(a, 4))[0]


def cells_of(w):
    gm = w.gm
    return {
        "b4": gm.dw(CELL_B4), "b8": read_float(gm, CELL_B8),
        "bc": read_float(gm, CELL_BC), "e38": gm.dw(CELL_E38),
        "e3c": gm.r(CELL_E3C, 1)[0], "e40": gm.dw(CELL_E40),
    }


def run_case(case, raw, secs, imports):
    w = World(case, raw, secs, imports)
    kind = case["kind"]
    out = {"faults": w.faults, "writes": w.writes, "calls": w.calls}
    if kind == "timing":
        before = cells_of(w)
        case["stopat"] = 0x1EDE60   # the tail-jmp insn itself; 2BDA90
                                    # is beyond the 165-byte scope
        w.run(TIMING, ecx=case.get("ecx", 1))
        out["before"], out["after"] = before, cells_of(w)
        out["rets"] = w.rets
        return w, out
    if kind == "seed":
        if case.get("flag"):
            w.gm.w(MT_FLAG, b"\x01")
        for s in case["seeds"]:
            w.run(SEED, ecx=s)
        arr = struct.unpack("<624I", w.gm.r(MT_ARR, 624 * 4))
        out["index"], out["flag"] = w.gm.dw(MT_IDX), w.gm.r(MT_FLAG, 1)[0]
        out["match"] = arr == tuple(mt19937(case["seeds"][-1]))
        out["arr"] = [hex(x) for x in arr]
        return w, out
    if kind == "mtinit-direct":
        w.uc.reg_write(UC_X86_REG_EDX, case["seed"])
        w.run(MTINIT, ecx=case.get("rcx", 0xDEAD))
        arr = struct.unpack("<624I", w.gm.r(MT_ARR, 624 * 4))
        out["match"] = arr == tuple(mt19937(case["seed"]))
        out["index"] = w.gm.dw(MT_IDX)
        out["arr"] = [hex(x) for x in arr]
        return w, out
    if kind == "mem":
        case.setdefault("watch", []).append((0x1DAA900, 0x1DAAA40))
        case["stopat"] = MEMEND
        w.run(MEMBAT)
        out["blocks"] = [(hex(p), hex(s)) for p, s in w.blocks]
        out["rets"] = w.rets
        # per-block: which offsets were written (emulated + stub-side),
        # head/tail bytes
        per = []
        for ptr, sz in w.blocks:
            ws = [(int(a, 16) - ptr, s, l) for a, s, l in w.writes
                  if ptr <= int(a, 16) < ptr + sz]
            sw = [(a - ptr, s, l) for a, s, l in w.stub_writes
                  if ptr <= a < ptr + sz]
            head = w.gm.r(ptr, 0x40)
            tail = w.gm.r(ptr + sz - 0x40, 0x40)
            per.append({"ptr": hex(ptr), "size": hex(sz),
                        "writes": [(hex(o), s, l) for o, s, l in
                                   sorted(ws)],
                        "stub_writes": [(hex(o), s, l) for o, s, l in
                                        sorted(sw)],
                        "head40": head.hex(), "tail40": tail.hex()})
        out["perblock"] = per
        return w, out
    raise ValueError(kind)


CASES = {
    # ---- timing ----------------------------------------------------
    "t-ecx1-flag0": {"kind": "timing", "ecx": 1,
                     "watch": [tuple(c) for c in
                               [(CELL_B4, CELL_B4 + 4), (CELL_B8, CELL_B8 + 4),
                                (CELL_BC, CELL_BC + 4), (CELL_E38, CELL_E38 + 4),
                                (CELL_E3C, CELL_E3C + 1), (CELL_E40, CELL_E40 + 4)]]},
    "t-ecx1-flag1": {"kind": "timing", "ecx": 1,
                     "plant": [(CELL_E3C, b"\x01"), (CELL_E40, dw(0x1234))],
                     "watch": [tuple(c) for c in
                               [(CELL_B4, CELL_B4 + 4), (CELL_B8, CELL_B8 + 4),
                                (CELL_BC, CELL_BC + 4), (CELL_E38, CELL_E38 + 4),
                                (CELL_E3C, CELL_E3C + 1), (CELL_E40, CELL_E40 + 4)]]},
    "t-ecx0-ok": {"kind": "timing", "ecx": 0, "caps": (0xBEEF, 0xCAFE),
                  "watch": [tuple(c) for c in
                               [(CELL_B4, CELL_B4 + 4), (CELL_B8, CELL_B8 + 4),
                                (CELL_BC, CELL_BC + 4), (CELL_E38, CELL_E38 + 4),
                                (CELL_E3C, CELL_E3C + 1), (CELL_E40, CELL_E40 + 4)]]},
    "t-ecx0-fail": {"kind": "timing", "ecx": 0, "caps_ret": 1,
                    "watch": [tuple(c) for c in
                               [(CELL_B4, CELL_B4 + 4), (CELL_B8, CELL_B8 + 4),
                                (CELL_BC, CELL_BC + 4), (CELL_E38, CELL_E38 + 4),
                                (CELL_E3C, CELL_E3C + 1), (CELL_E40, CELL_E40 + 4)]]},
    # ---- seeding ----------------------------------------------------
    "s-first-4537": {"kind": "seed", "seeds": [4537]},
    "s-twice-4537": {"kind": "seed", "seeds": [4537, 4537]},
    "s-boot-seq": {"kind": "seed", "seeds": [5489, 4537]},
    "s-flag-preset": {"kind": "seed", "seeds": [4537], "flag": True},
    "s-mtinit-badptr": {"kind": "mtinit-direct", "rcx": 0xDEAD,
                        "seed": 42},
    # ---- memory battery ---------------------------------------------
    "m-battery": {"kind": "mem"},
}

EXPECT_SIZES = [0x1DC0010, 0xD20100, 0x100010, 0x1C0100, 0x6C00400,
                0x3000100, 0x2000100, 0x1200010, 0x400100, 0x80000,
                0x100000]


def check():
    raw, secs = load_image()
    imports = import_map(raw, secs)
    results, fails = {}, []
    for name, case in CASES.items():
        w, out = run_case(case, raw, secs, imports)
        results[name] = out
        if out["faults"]:
            fails.append((name, "faults", out["faults"]))
    # ---- assertions -------------------------------------------------
    t0 = results["t-ecx1-flag0"]
    if t0["after"]["b4"] != 2 or abs(t0["after"]["b8"] - 2.0) > 1e-6 \
            or abs(t0["after"]["bc"] - 0.5) > 1e-6 or t0["after"]["e38"] != 1:
        fails.append(("t-ecx1-flag0", "cells", t0["after"]))
    if t0["after"]["e3c"] != 0:
        fails.append(("t-ecx1-flag0", "flag", t0["after"]["e3c"]))
    order = [c[0] for c in t0["calls"]]
    want = ["enter33f020", "enter32ae70", "enter3333d0", "enter337a00"]
    if [c for c in order if c.startswith("enter")] != want:
        fails.append(("t-ecx1-flag0", "call-order", order))
    if any(c[0].startswith("time") for c in t0["calls"]):
        fails.append(("t-ecx1-flag0", "winmm-called", t0["calls"]))

    t1 = results["t-ecx1-flag1"]
    if t1["after"]["e3c"] != 0 or t1["after"]["e40"] != 0x1234:
        fails.append(("t-ecx1-flag1", "cells", t1["after"]))
    if ("timeEndPeriod", 0x1234) not in t1["calls"]:
        fails.append(("t-ecx1-flag1", "endPeriod", t1["calls"]))
    o = [c[0] for c in t1["calls"]]
    if o.index("timeEndPeriod") < o.index("enter33f020"):
        fails.append(("t-ecx1-flag1", "order", o))

    t2 = results["t-ecx0-ok"]
    if t2["after"]["e40"] != 0xBEEF or t2["after"]["e3c"] != 1:
        fails.append(("t-ecx0-ok", "cells", t2["after"]))
    o = [c[0] for c in t2["calls"]]
    if o[:2] != ["timeGetDevCaps", "timeBeginPeriod"]:
        fails.append(("t-ecx0-ok", "order", o))
    # I3 prediction: ecx==0 writes NONE of the four 60-branch cells
    for k in ("b4", "b8", "bc", "e38"):
        if t2["before"][k] != t2["after"][k]:
            fails.append(("t-ecx0-ok", "i3-violation", k,
                          t2["before"][k], t2["after"][k]))

    t3 = results["t-ecx0-fail"]
    o = [c[0] for c in t3["calls"]]
    if "timeBeginPeriod" in o or t3["after"]["e3c"] != 0:
        fails.append(("t-ecx0-fail", "fail-arm", o, t3["after"]))
    for k in ("b4", "b8", "bc", "e38", "e40"):
        if t3["before"][k] != t3["after"][k]:
            fails.append(("t-ecx0-fail", "cells", k))

    for nm in ("s-first-4537", "s-twice-4537", "s-boot-seq",
               "s-flag-preset", "s-mtinit-badptr"):
        if not results[nm]["match"]:
            fails.append((nm, "mt-mismatch",
                          results[nm].get("arr_head"),
                          results[nm].get("arr_tail")))
    if results["s-first-4537"]["index"] != 0x270 \
            or results["s-first-4537"]["flag"] != 1:
        fails.append(("s-first-4537", "idx/flag",
                      results["s-first-4537"]["index"],
                      results["s-first-4537"]["flag"]))
    mt_calls = [c for c in results["s-twice-4537"]["calls"]
                if c[0] == "mtinit"]
    if [c[1] for c in mt_calls] != [0x1571, 4537, 4537]:
        fails.append(("s-twice-4537", "mtinit-args", mt_calls))
    mt_calls = [c for c in results["s-boot-seq"]["calls"]
                if c[0] == "mtinit"]
    if [c[1] for c in mt_calls] != [0x1571, 5489, 4537]:
        fails.append(("s-boot-seq", "mtinit-args", mt_calls))
    mt_calls = [c for c in results["s-flag-preset"]["calls"]
                if c[0] == "mtinit"]
    if [c[1] for c in mt_calls] != [4537]:
        fails.append(("s-flag-preset", "mtinit-args", mt_calls))

    mb = results["m-battery"]
    mcs = [c for c in mb["calls"] if c[0] == "malloc"]
    if [int(c[1], 16) for c in mcs] != EXPECT_SIZES:
        fails.append(("m-battery", "sizes",
                      [c[1] for c in mcs]))
    regs = [c for c in mb["calls"] if c[0] == "enter369d30"]
    if len(regs) != 9:
        fails.append(("m-battery", "reg-count", len(regs)))
    # every registered call carries (idx, base, tail) = (ecx,r8,r9)
    reg_args = [(int(c[1], 16), int(c[3], 16), int(c[4], 16))
                for c in regs]
    if reg_args != [(2, 0x1DC0000, 0x10), (3, 0xD20000, 0x100),
                    (4, 0x100000, 0x10), (5, 0x1C0000, 0x100),
                    (6, 0x6C00000, 0x400), (7, 0x3000000, 0x100),
                    (8, 0x2000000, 0x100), (9, 0x1200000, 0x10),
                    (0xB, 0x400000, 0x100)]:
        fails.append(("m-battery", "reg-args", reg_args))

    summary = {"cases": len(CASES), "failures": fails,
               "pass": len(CASES) - len({f[0] for f in fails})}
    with open(RESULT, "w") as f:
        json.dump({"summary": summary, "results":
                   {k: {kk: vv for kk, vv in v.items()
                        if kk != "perblock"} for k, v in
                    results.items()},
                   "perblock": results["m-battery"]["perblock"]},
                  f, indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))
    return fails


if __name__ == "__main__":
    sys.exit(1 if check() else 0)
