# EXP-122 — alloc-dispatch-exec
# Executes the staged-kind allocator dispatch end to end:
#   A100 0036A100 front door: BC60(ecx=d[0x22D89BC]=ST_W, edx=arg)
#     then BFE0(ecx=d[0x22D89BD] - the OVERLAPPING dword) on null;
#     on success writes b[obj-0x3E]=b[ST_B2], d[obj-0x10]=C620(0),
#     w[obj-2]=0.
#   BFE0 0036BFE0 create-with-retry: mask bt(d[0x22D89B8],ecx_arg)
#     hard jmp$ spin; desc = 0x22D8FD0 + sx32(ST_W)*0xA8 (kind>0xE
#     -> desc=0 -> q[0xA0] fault); call rax q[desc+0xA0] per-kind
#     ctor; AAD0/ABE0 live-pool check writes b[desc+2]=b[desc+0x62]=1;
#     BC60 alloc; retry jmp 0x36C013 re-reads ST_W.
#   C620 0020E620 BASE-inverse leaf: ecx - low32(q[0x1F83530]).
#
# Scripted boundaries (entry-intercepted, planted returns — NOT
# executed): BC60 0036BC60 (887B alloc core), AAD0 0036AAD0,
# ABE0 0036ABE0. The indirect `call rax` is NOT stubbed — the fixture
# plants q[desc+0xA0] = FLAG 0046DFE0, so the dispatch executes a real
# shipped leaf through the real indirect call.
#
# Fixture disclosure: all BSS globals (mask/ST_W/QCOUNT/ST_B2/desc
# table/codec cell) are planted; object pointer OBJ is a heap fixture;
# model reads fall back to shipped image bytes where unplanted.

import ctypes, hashlib, json, struct
from unicorn import Uc
from unicorn.x86_const import (
    UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
    UC_X86_REG_RAX, UC_X86_REG_RIP, UC_X86_REG_RSP)
from unicorn import (UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE,
                     UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL, UcError)

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

A100 = 0x0036A100
BFE0 = 0x0036BFE0
C620 = 0x0020E620
BC60 = 0x0036BC60     # scripted boundary (alloc core)
AAD0 = 0x0036AAD0     # scripted boundary (pool count)
ABE0 = 0x0036ABE0     # scripted boundary (pool flag)
FLAG = 0x0046DFE0     # real leaf - planted callback target

SPIN_BFE0 = 0x36C000  # BFE0 mask-gate jmp$ site
RETRY_BFE0 = 0x36C013 # BFE0 retry target (ST_W re-read)

MASKG  = 0x22D89B8    # d: kind mask (bt eax, ecx gates)
ST_W   = 0x22D89BC    # d: staged word/tag = kind (both calls read it)
QCOUNT = 0x22D89C0    # d: queue count (adjacent global)
ST_B2  = 0x22D8E18    # d: staged byte2 -> b[obj-0x3E]
CODEC  = 0x1F83530    # q: arena codec base cell
DTAB   = 0x22D7FD0    # kind descriptor table, stride 0xA8, kinds 0..14
FLAGG  = 0x215EFF4    # d: flag (-1 -> FLAG()=2)

ARENA  = HEAP + 0x20000      # planted codec base
OBJ    = HEAP + 0x40000      # planted alloc result
DESCK  = 2                    # default kind for cases


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


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # globals: mask, staged word, queue count, staged b2, flag, codec
    W.append((MASKG, dw(case.get("mask", 0) & 0xFFFFFFFF)))
    W.append((ST_W, dw(case.get("stw", 0) & 0xFFFFFFFF)))
    W.append((QCOUNT, dw(case.get("qcount", 0) & 0xFFFFFFFF)))
    W.append((ST_B2, dw(case.get("stb2", 0) & 0xFFFFFFFF)))
    W.append((FLAGG, dw(case.get("flag", 0) & 0xFFFFFFFF)))
    W.append((CODEC, qw(case.get("codec", ARENA))))
    # kind descriptor: +0x50 pool ptr, +0xA0 ctor callback, +2/+0x62 flags
    for k, d in case.get("desc", {}).items():
        b = DTAB + k * 0xA8
        if "q50" in d: W.append((b + 0x50, qw(d["q50"])))
        if "qA0" in d: W.append((b + 0xA0, qw(d["qA0"])))
        if "b2" in d:  W.append((b + 2, bytes([d["b2"] & 0xFF])))
        if "b62" in d: W.append((b + 0x62, bytes([d["b62"] & 0xFF])))
    # object header fill (makes zero-writes observable)
    if "hdrfill" in case:
        W.append((OBJ - 0x40, bytes([case["hdrfill"] & 0xFF]) * 0x40))
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
        self.bc60_n = 0
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr in (BC60, AAD0, ABE0):
            if addr == BC60:
                name = "bc60"
                seq = self.case.get("bc60_rets",
                                    [self.case.get("bc60_ret", 0)])
                ret = seq[min(self.bc60_n, len(seq) - 1)]
                self.bc60_n += 1
            elif addr == AAD0:
                name = "aad0"
                ret = self.case.get("aad0_ret", 0)
            else:
                name = "abe0"
                ret = self.case.get("abe0_ret", 0)
            self.trace.append("%s:%x:%x" % (
                name, uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF,
                uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, ret & 0xFFFFFFFFFFFFFFFF)
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
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        for addr, dat in case.get("patch_bytes", []):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets, self.ends = [], [], [], []
        self.bc60_n = 0

    def mb(self, a):
        a &= 0xFFFFFFFFFFFFFFFF
        if a in self.mem:
            return self.mem[a]
        if IMG_LO <= a < IMG_HI:
            return img_byte(self.raw, self.secs, a)
        return None                    # unmapped -> fault

    def mw(self, a):
        v0, v1 = self.mb(a), self.mb(a + 1)
        if v0 is None or v1 is None: return None
        return v0 | (v1 << 8)
    def md(self, a):
        r = 0
        for i in range(4):
            v = self.mb(a + i)
            if v is None: return None
            r |= v << (i * 8)
        return r
    def mq(self, a):
        lo, hi = self.md(a), self.md(a + 4)
        if lo is None or hi is None: return None
        return lo | (hi << 32)

    def stb(self, a, v):
        self.mem[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFF
    def stw(self, a, v):
        self.stb(a, v); self.stb(a + 1, v >> 8)
    def std(self, a, v):
        for i in range(4): self.stb(a + i, v >> (i * 8))

    # ---- scripted calls (planted returns; tokens recorded) ----
    def bc60_call(self, ecx, edx):
        self.trace.append("bc60:%x:%x" % (ecx & 0xFFFFFFFF,
                                          edx & 0xFFFFFFFF))
        seq = self.case.get("bc60_rets",
                            [self.case.get("bc60_ret", 0)])
        ret = seq[min(self.bc60_n, len(seq) - 1)]
        self.bc60_n += 1
        return ret & 0xFFFFFFFFFFFFFFFF

    def aad0_call(self, rcx):
        self.trace.append("aad0:%x:0" % (rcx & 0xFFFFFFFF))
        return self.case.get("aad0_ret", 0) & 0xFFFFFFFFFFFFFFFF

    def abe0_call(self, rcx):
        self.trace.append("abe0:%x:0" % (rcx & 0xFFFFFFFF))
        return self.case.get("abe0_ret", 0) & 0xFFFFFFFFFFFFFFFF

    # ---- real bodies ----
    def flag(self):
        return 2 if sx32(self.md(FLAGG) or 0) == -1 else 0

    def c620(self, ecx):
        return (ecx - (self.md(CODEC) or 0)) & 0xFFFFFFFF

    def bfe0(self, ecx, edx):
        """0036BFE0 — create-with-retry dispatcher."""
        ebp = edx & 0xFFFFFFFF
        for _pass in range(8):
            mask = self.md(MASKG) or 0
            if not (mask >> (ecx & 0x1F)) & 1:
                # jmp$ spin: rax still holds the mask dword
                return ("spin", SPIN_BFE0, mask)
            kind = sx32(self.md(ST_W) or 0)
            desc = DTAB + kind * 0xA8 if 0 <= kind <= 0xE else 0
            cb = self.mq(desc + 0xA0)          # desc=0 -> q[0xA0] fault
            if cb is None:
                return ("fault", desc + 0xA0, 0x36C02D, mask)
            if cb == FLAG:
                # real leaf executes through the indirect call —
                # no token on either side; esi = flag() is the effect
                esi = self.flag()
            elif cb == 0:
                esi = 0
            else:
                return ("fault", cb, 0x36C03B, mask)
            # pool check: mask bit(ST_W) && q[desc+0x50]
            mask = self.md(MASKG) or 0
            kind_d = self.md(ST_W) or 0
            edi = 0
            if (mask >> (kind_d & 0x1F)) & 1:
                rbx = desc                     # same kind -> same desc
                q50 = self.mq(rbx + 0x50)
                if q50 is None:
                    return ("fault", rbx + 0x50, 0x36C06A, mask)
                if q50 != 0:
                    edi = self.aad0_call(rbx)
                    if self.abe0_call(rbx) != 0:
                        edi = (edi + 1) & 0xFFFFFFFFFFFFFFFF
                    if edi != 0:
                        self.stb(rbx + 2, 1)
                        self.stb(rbx + 0x62, 1)
            rax = self.bc60_call(kind_d, ebp)
            if edi != 0:
                if rax == 0:
                    continue                   # retry: re-read ST_W
                return ("ret", rax)
            if rax != 0:
                return ("ret", rax)
            if esi != 0:
                continue                       # retry
            return ("ret", 0)
        return ("spin", RETRY_BFE0, mask)

    def a100(self, ecx):
        """0036A100 — front door: BC60 then BFE0 fallback."""
        edi = ecx & 0xFFFFFFFF
        rax = self.bc60_call(self.md(ST_W) or 0, edi)
        if rax == 0:
            # BFE0's ecx is also d[0x22D89BC] — same staged kind
            r = self.bfe0(self.md(ST_W) or 0, edi)
            if r[0] != "ret":
                return r
            rbx = r[1]
        else:
            rbx = rax
        if rbx == 0:
            return ("ret", 0)
        self.stb(rbx - 0x3E, self.mb(ST_B2) or 0)
        self.std(rbx - 0x10, self.c620(0))
        self.stw(rbx - 2, 0)
        return ("ret", rbx)


def run_model(case, raw, secs):
    m = Model(case, raw, secs)
    for step in case.get("steps", []):
        entry = step[0]
        if entry == A100:
            r = m.a100(step[1])
        elif entry == BFE0:
            r = m.bfe0(step[1], step[2])
        elif entry == C620:
            r = ("ret", m.c620(step[1]))
        else:
            raise ValueError("bad entry %x" % entry)
        if r[0] == "ret":
            m.rets.append(r[1]); m.ends.append(RETQ)
        elif r[0] == "spin":
            m.rets.append(r[2]); m.ends.append(r[1])
        elif r[0] == "fault":
            m.faults.append(("exp", r[1])); m.rets.append(r[3])
            m.ends.append(r[2])
            break
    mem = {}
    for a, n in case.get("watch", []):
        mem["%x" % a] = bytes(
            m.mem.get(a + i, img_byte(raw, secs, a + i)
                      if IMG_LO <= a + i < IMG_HI else 0)
            for i in range(n)).hex()
    return {"trace": m.trace, "faults": m.faults,
            "rets": m.rets, "ends": m.ends, "mem": mem}


def differs(nat, mod):
    d = []
    for a, b in (("trace", nat["trace"] == mod["trace"]),
                 ("rets", nat["rets"] == mod["rets"]),
                 ("ends", nat["ends"] == mod["ends"]),
                 ("mem", nat["mem"] == mod["mem"])):
        if not b:
            d.append(a)
    # faults: model emits ("exp", addr); native carries tuples
    nf, mf = nat["faults"], mod["faults"]
    if bool(nf) != bool(mf):
        d.append("faults")
    elif nf and mf:
        naddr = nf[0][1] if isinstance(nf[0][1], int) else None
        if naddr != mf[0][1]:
            d.append("faults")
    return d


# ---------------- cases ----------------

WATCH_HDR = [(OBJ - 0x40, 0x40)]           # object header window
WATCH_DSC = [(DTAB + DESCK * 0xA8, 0xA8)]  # descriptor kind 2

def cases():
    C = {}
    d2 = {"q50": 0x12345678, "qA0": FLAG}   # pool ptr + real-leaf cb
    # ---- A100 front door ----
    C["a100-direct"] = {
        "stw": DESCK, "stb2": 0xAB, "bc60_rets": [OBJ],
        "hdrfill": 0xAA,
        "watch": WATCH_HDR, "steps": [(A100, 0x77)]}
    C["a100-fallback"] = {
        "stw": DESCK, "qcount": 0, "stb2": 0x5C,
        "mask": (1 << 0) | (1 << DESCK),     # bit0 (karg) + bit2 (stw)
        "flag": -1,                          # FLAG()->2 -> esi=2
        "desc": {DESCK: dict(d2)},
        "aad0_ret": 2, "abe0_ret": 1,
        "bc60_rets": [0, OBJ],
        "watch": WATCH_HDR + WATCH_DSC, "steps": [(A100, 0x10)]}
    C["a100-null"] = {
        "stw": DESCK, "mask": 1 << DESCK,    # gate bit = stw bit
        "flag": 0,                           # FLAG()->0 -> esi=0
        "desc": {DESCK: dict(d2)},
        "bc60_rets": [0, 0],
        "watch": WATCH_HDR, "steps": [(A100, 0x10)]}
    C["a100-retry"] = {
        "stw": DESCK, "mask": 1 << DESCK, "flag": -1,
        "desc": {DESCK: dict(d2)},
        "bc60_rets": [0, 0, OBJ],            # A100, BFE0 p1, p2
        "watch": WATCH_HDR, "steps": [(A100, 0x10)]}
    # ---- BFE0 direct ----
    C["bfe0-spin"] = {
        "stw": DESCK, "mask": 0,
        "steps": [(BFE0, 0, 0x40)]}          # ecx bit0, mask 0 -> spin
    C["bfe0-karg-bit3"] = {
        "stw": 0x300, "qcount": 0, "mask": 0,
        "steps": [(BFE0, 3, 0x40)]}          # bit3, mask 0 -> spin
    C["bfe0-karg-bit3-ok"] = {
        "stw": DESCK, "mask": (1 << 3), "flag": 0,
        "desc": {DESCK: dict(d2)},
        "bc60_rets": [OBJ],
        "steps": [(BFE0, 3, 0x40)]}          # bit3 passes
    C["bfe0-desc-hi"] = {
        "stw": 0xF, "mask": 1 << 0,          # gate ok; kind 0xF -> desc=0
        "steps": [(BFE0, 0, 0x40)]}          # fault at q[0xA0]
    C["bfe0-nocb"] = {
        "stw": DESCK, "mask": 1 << 0, "flag": 0,
        "desc": {DESCK: {"q50": 0, "qA0": 0}},
        "bc60_rets": [OBJ],
        "steps": [(BFE0, 0, 0x40)]}
    C["bfe0-retry"] = {
        "stw": DESCK, "mask": 1 << 0, "flag": -1,
        "desc": {DESCK: dict(d2)},
        "bc60_rets": [0, OBJ],
        "steps": [(BFE0, 0, 0x40)]}
    C["bfe0-fail"] = {
        "stw": DESCK, "mask": 1 << 0, "flag": 0,
        "desc": {DESCK: dict(d2)},
        "bc60_rets": [0],
        "steps": [(BFE0, 0, 0x40)]}
    C["bfe0-poolflags"] = {
        "stw": DESCK, "mask": (1 << 0) | (1 << DESCK), "flag": 0,
        "desc": {DESCK: dict(d2)},
        "aad0_ret": 2, "abe0_ret": 0,
        "bc60_rets": [OBJ],
        "watch": WATCH_DSC, "steps": [(BFE0, 0, 0x40)]}
    C["bfe0-q50-null"] = {
        "stw": DESCK, "mask": (1 << 0) | (1 << DESCK), "flag": 0,
        "desc": {DESCK: {"q50": 0, "qA0": FLAG}},
        "bc60_rets": [0],
        "steps": [(BFE0, 0, 0x40)]}
    # ---- C620 leaf ----
    C["c620-basic"] = {"steps": [(C620, 0x100)]}
    C["c620-neg"] = {"steps": [(C620, 0)]}
    return C


# ---------------- mutants ----------------
# (name, va, expected_byte, mutant_byte, case)
def B(v): return bytes([v])

MUTS = [
    # A100: kind arg disp ST_W -> QCOUNT (BC60 gets count not tag)
    ("m-a100-kind",  0x36A115, B(0xA3), B(0xA7), "a100-fallback"),
    # A100: fallback gate je -> jne (BFE0 success skips writes)
    ("m-a100-je",    0x36A154, B(0x74), B(0x75), "a100-fallback"),
    # A100: BFE0 kind disp -1 (reads d[0x22D89BB] not ST_W);
    # karg becomes (stw<<8)|mask3 -> bit0, mask=4 fails -> spin
    ("m-a100-karg",  0x36A130, B(0x88), B(0x87), "a100-null"),
    # A100: staged b2 cell disp -1 (reads 0x22D8E17)
    ("m-a100-stb2",  0x36A159, B(0xBB), B(0xBA), "a100-direct"),
    # A100: header dword disp -0x10 -> -0x14
    ("m-a100-off10", 0x36A169, B(0xF0), B(0xEC), "a100-direct"),
    # A100: header word disp -2 -> -4
    ("m-a100-w2",    0x36A170, B(0xFE), B(0xFC), "a100-direct"),
    # BFE0: mask gate jb -> jae (bit clear proceeds, bit set spins)
    ("m-bfe0-gate",  0x36BFFB, B(0x72), B(0x73), "bfe0-spin"),
    # BFE0: desc index bound 0xE -> 0xD (kind 0xE loses desc)
    ("m-bfe0-kind",  0x36C01C, B(0x0E), B(0x0D), "bfe0-kind-e"),
    # BFE0: desc stride 0xA8 -> 0xA0 (callback cell misreads;
    # retry case: wrong cell reads 0 -> esi=0 -> ret 0 vs OBJ)
    ("m-bfe0-str",   0x36C022, B(0xA8), B(0xA0), "bfe0-retry"),
    # BFE0: pool qword disp +0x50 -> +0x58
    ("m-bfe0-q50",   0x36C06D, B(0x50), B(0x58), "bfe0-poolflags"),
    # BFE0: desc flag byte +2 -> +3
    ("m-bfe0-flag2", 0x36C097, B(0x02), B(0x03), "bfe0-poolflags"),
    # BFE0: pool-gate jae -> jb (mask bit set skips the pool check)
    ("m-bfe0-bt2",   0x36C052, B(0x73), B(0x72), "bfe0-poolflags"),
    # BFE0: esi-path retry jne -> je (near-jcc; no retry on null)
    ("m-bfe0-rty",   0x36C0BA, B(0x85), B(0x84), "bfe0-retry"),
    # C620: sub -> add (returns base + ecx)
    ("m-c620-sub",   0x20E620, B(0x2B), B(0x03), "c620-basic"),
]


def main():
    raw, secs = load_image()
    cs = cases()
    # extra case the mutants need (kind 0xE boundary)
    cs["bfe0-kind-e"] = {
        "stw": 0xE, "mask": 1 << 0xE, "flag": 0,
        "desc": {0xE: {"q50": 0, "qA0": 0}},
        "bc60_rets": [OBJ],
        "steps": [(BFE0, 0xE, 0x40)]}
    res = {"cases": {}, "mutants": {}, "bad_sites": []}
    nok = 0
    for name, case in cs.items():
        w = World(case, raw, secs); w.run()
        nat, mod = w.obs(), run_model(case, raw, secs)
        d = differs(nat, mod)
        res["cases"][name] = "ok" if not d else d
        if d:
            print("CASE %s DIFF %s" % (name, d))
            print("  nat:", {k: nat[k] for k in d})
            print("  mod:", {k: mod[k] for k in d})
        else:
            nok += 1
    print("functional: %d/%d" % (nok, len(cs)))
    # verify mutation sites against shipped bytes first
    bad = []
    for name, va, want, patch, cn in MUTS:
        got = img_rd(raw, secs, va, 1)
        if got != want:
            bad.append((name, va, want.hex(), got.hex()))
            print("BAD SITE %s 0x%x want %s got %s"
                  % (name, va, want.hex(), got.hex()))
    res["bad_sites"] = bad
    if bad:
        print("aborting mutant run — fix sites first")
        json.dump(res, open("result.json", "w"), indent=1)
        return
    kill = 0
    for name, va, want, patch, cn in MUTS:
        case = dict(cs[cn])
        case["patch_bytes"] = [(va, patch)]
        w = World(case, raw, secs); w.run()
        nat, mod = w.obs(), run_model(case, raw, secs)
        d = differs(nat, mod)
        if d:
            kill += 1
            res["mutants"][name] = "killed"
        else:
            res["mutants"][name] = "ALIVE"
            print("MUTANT ALIVE %s (case %s)" % (name, cn))
    print("mutants: %d/%d killed" % (kill, len(MUTS)))
    json.dump(res, open("result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
