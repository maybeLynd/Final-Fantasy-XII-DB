# EXP-119 t51-tail-resolvers-exec — native replay harness.
#
# Executes the two tails that stayed scripted through EXP-109/117/118
# on a stale "deep ~85 insns" estimate — both are thin resolvers:
#
#   T51T 0051B9E0   6B — jmp 0051F240 thunk
#   T51  0051F240 138B — resolve_element(ctx=rcx, idx=edx):
#        mode = sx2(d[ctx+4]): 0 -> table = RES(q[ctx+8]);
#        1 -> table = q[ctx+8] direct; 2/3 -> 0.
#        elem = table + (idx & 0xFFFF)*48; elem == 0 -> 0.
#        b[elem] & 2 -> q[elem+0x18] = sx32(RES(q[elem+0x10])
#                       + d[elem+0x20])   (lazy write-back)
#        return q[elem+0x18]
#   E20  00370E20  11B — mov ecx,[rcx+0x94]; jmp BASE
#        -> return ARENA + u32(d[rcx+0x94])
#   RES  003AB7F0  99B — two-way dispatch + <=0x40 result bound
#   BASE 0020E600  10B — arena codec base
#
# Scripted boundary (planted return, arg traced):
#   HRES 0036B130 — RES's nonzero-mode resolver (real in EXP-084)
#
# Native and model must agree on trace/rets/faults/write-backs.

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
    UC_X86_REG_RDX, UC_X86_REG_RSP, UC_X86_REG_RIP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

T51T = 0x0051B9E0
T51  = 0x0051F240
E20  = 0x00370E20
RES  = 0x003AB7F0
BASE = 0x0020E600
HRES = 0x0036B130    # RES mode arm — scripted boundary

CODEC = 0x01F83530   # q: arena codec base (shipped global)

# planted fixture addresses
CTX    = HEAP + 0x100000          # the ctx arg (mode/table)
TABLE  = HEAP + 0x200000          # resolved element table base
ELEMH  = HEAP + 0x300000          # spare resolved-handle target
E20P   = HEAP + 0x400000          # E20's pointer arg
ARENA  = HEAP + 0x600000          # arena base (codec value)


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


ENT_ST = 48          # T51 element stride


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # --- ctx: d[+4] mode source, q[+8] table handle/ptr ---
    ctx = case.get("ctx", CTX)
    W.append((ctx + 4, dw(case.get("mode_d", 0))))
    W.append((ctx + 8, qw(case.get("htab", TABLE))))
    # --- element table: 48B rows {b flag, q+0x10 hdl, q+0x18 cached,
    #     d+0x20 addend} at the RESOLVED base ---
    tab = case.get("htab", TABLE)
    if tab & 3 == 0:
        base = tab                       # direct pointer (low2==0)
    else:
        base = case.get("hres_map", {}).get(tab, 0)
    if base < HEAP:
        base = 0                         # unreachable rows — skip
    for i, e in case.get("elems", {}).items() if base else ():
        el = base + i * ENT_ST
        W.append((el + 0, bytes([e.get("flag", 0) & 0xFF])))
        W.append((el + 0x10, qw(e.get("hdl", 0))))
        W.append((el + 0x18, qw(e.get("old18", 0))))
        W.append((el + 0x20, dw(e.get("add", 0) & 0xFFFFFFFF)))
    # --- E20 pointer arg: d[+0x94] codec offset ---
    p = case.get("e20p", E20P)
    W.append((p + 0x94, dw(case.get("e94", 0) & 0xFFFFFFFF)))
    W.append((CODEC, qw(ARENA)))
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
        self.trace, self.faults, self.rets = [], [], []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

    def on_code(self, uc, addr, size, _):
        if addr == HRES:
            # scripted boundary: record arg, plant return, pop call
            self.trace.append("hres:%x" % uc.reg_read(UC_X86_REG_RCX))
            ret = self.case.get("hres_map", {}).get(
                uc.reg_read(UC_X86_REG_RCX), 0)
            uc.reg_write(UC_X86_REG_RAX, ret)
            uc.reg_write(UC_X86_REG_RIP, self.gm.qw(
                uc.reg_read(UC_X86_REG_RSP)))
            uc.reg_write(UC_X86_REG_RSP,
                         uc.reg_read(UC_X86_REG_RSP) + 8)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.emu_stop()
        return True

    def run_one(self, entry, rcx, rdx=0):
        uc = self.uc
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, rcx)
        uc.reg_write(UC_X86_REG_RDX, rdx)
        try:
            uc.emu_start(entry, RETQ, count=60000)
        except UcError as e:
            if not self.faults:
                self.faults.append(("emuerr", str(e)))
        self.rets.append(uc.reg_read(UC_X86_REG_RAX))

    def run(self):
        for entry, rcx, rdx in self.case.get("steps", []):
            self.run_one(entry, rcx, rdx)

    def obs(self):
        # resolved table base for write-back observation
        tab = self.case.get("htab", TABLE)
        if tab & 3 == 0:
            base = tab
        else:
            base = self.case.get("hres_map", {}).get(tab, 0)
        elems = {}
        if base >= HEAP:
            for i in self.case.get("elems", {}):
                el = base + i * ENT_ST
                elems[i] = {"v18": self.gm.qw(el + 0x18),
                            "v20": self.gm.dw(el + 0x20)}
        return {"trace": self.trace, "faults": self.faults,
                "rets": self.rets, "elems": elems}


# ---------------- python model ----------------
# the model interprets the same planted fixture bytes — md/mw/mq/mb
# read the shared image so there is no parallel param copy.

def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


class Model:
    def __init__(self, case):
        self.case = case
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.trace, self.faults, self.rets = [], [], []
        self.wb = {}

    def mb(self, a): return self.mem.get(a & 0xFFFFFFFFFFFFFFFF, 0)
    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)

    def w64(self, a, v):
        for i in range(8):
            self.mem[a + i] = (v >> (i * 8)) & 0xFF

    def res(self, h):
        """RES dispatch: null->0, low2==0->identity, else hres;
        resolved sx32 <= 0x40 zeroed (EXP-117)."""
        if h == 0:
            return 0
        if h & 3 == 0:
            return h
        self.trace.append("hres:%x" % h)
        r = self.case.get("hres_map", {}).get(h, 0)
        if sx32(r) & 0xFFFFFFFFFFFFFFFF <= 0x40:
            return 0
        return r

    def t51(self, ctx, idx):
        """0051F240 — resolve_element. Returns rax; records
        write-backs into self.wb."""
        v = self.md(ctx + 4)
        # shl 0x1e / sar 0x1e = sx2(v&3)
        mode = v & 3
        mode = mode - 4 if mode & 2 else mode
        edi = idx & 0xFFFF
        if mode == 0:
            base = self.res(self.mq(ctx + 8))
            elem = (base + edi * ENT_ST) & 0xFFFFFFFFFFFFFFFF
        elif mode == 1:
            elem = (self.mq(ctx + 8) + edi * ENT_ST) & \
                0xFFFFFFFFFFFFFFFF
        else:
            return 0
        if elem == 0:
            return 0
        if elem < HEAP:
            # element pointer below the fixture region — real fault
            self.faults.append(elem)
            return None
        if self.mb(elem) & 2:
            val = (self.res(self.mq(elem + 0x10)) +
                   self.md(elem + 0x20)) & 0xFFFFFFFF
            sv = sx32(val) & 0xFFFFFFFFFFFFFFFF
            self.w64(elem + 0x18, sv)
            self.wb[elem + 0x18] = sv
        return self.mq(elem + 0x18)

    def e20(self, p):
        """00370E20 — BASE(d[p+0x94]); ecx zero-extends -> u32 add."""
        return (self.md(p + 0x94) + ARENA) & 0xFFFFFFFFFFFFFFFF


def run_model(case):
    m = Model(case)
    for entry, rcx, rdx in case.get("steps", []):
        if entry in (T51, T51T):
            m.rets.append(m.t51(rcx, rdx & 0xFFFFFFFF))
        elif entry == E20:
            m.rets.append(m.e20(rcx))
        elif entry == RES:
            m.rets.append(m.res(rcx))
    # write-back observables for every planted element
    tab = case.get("htab", TABLE)
    if tab & 3 == 0:
        base = tab
    else:
        base = case.get("hres_map", {}).get(tab, 0)
    elems = {}
    if base >= HEAP:
        for i, e in case.get("elems", {}).items():
            el = base + i * ENT_ST
            v18 = m.wb.get(el + 0x18, e.get("old18", 0))
            elems[i] = {"v18": v18, "v20": m.md(el + 0x20)}
    return {"trace": m.trace, "faults": m.faults, "rets": m.rets,
            "elems": elems}


# ---------------- cases ----------------

LAZY = {"flag": 2, "hdl": 0x12345, "add": 0x20}
CACHED = {"flag": 0, "old18": 0x777}
HMAP = {0x12345: 0x4ABC0000}


def t51c(**kw):
    c = {"mode_d": 0, "htab": TABLE,
         "elems": {0: CACHED, 1: LAZY, 2: CACHED},
         "hres_map": dict(HMAP),
         "steps": [(T51, CTX, 1)]}
    c.update(kw)
    return c


def build_cases():
    C = {}
    # ---- mode 0: table resolved through RES ----
    C["t51-mode0-lazy"] = t51c()
    # cached element: flag&2==0 -> no second RES, old q[+0x18] kept
    C["t51-mode0-cached"] = t51c(steps=[(T51, CTX, 0)])
    # ---- mode 1: q[ctx+8] used directly, no table RES ----
    C["t51-mode1"] = t51c(mode_d=1)
    C["t51-mode1-idx2"] = t51c(mode_d=1,
                               elems={0: CACHED, 1: LAZY,
                                      2: {"flag": 2, "hdl": 0x12345,
                                          "add": 0x99}},
                               steps=[(T51, CTX, 2)])
    # modes 2/3: sx2 gives -2/-1 -> ret 0 before any read
    C["t51-mode2"] = t51c(mode_d=2)
    C["t51-mode3"] = t51c(mode_d=3)
    # mode 0, table resolves to 0: idx==0 -> elem==0 -> ret 0;
    # idx!=0 -> elem=idx*48 lands at 0x30 -> real fault
    C["t51-nulltab-i0"] = t51c(htab=0x12345,
                             hres_map={0x12345: 0},
                             steps=[(T51, CTX, 0)])
    C["t51-nulltab-i1"] = t51c(htab=0x12345,
                             hres_map={0x12345: 0},
                             steps=[(T51, CTX, 1)])
    # element index masking: idx&0xFFFF
    C["t51-idx2"] = t51c(elems={0: CACHED, 1: LAZY,
                                2: {"flag": 2, "hdl": 0x12345,
                                    "add": 0x99}},
                         steps=[(T51, CTX, 2)])
    C["t51-idx-wrap"] = t51c(steps=[(T51, CTX, 0x10001)])
    # RES bound on the ELEMENT handle: hres->0x30 -> RES->0 but the
    # addend still applies -> ret = sx32(0+0x20) = 0x20
    C["t51-hres-low"] = t51c(elems={0: CACHED,
                                   1: {"flag": 2, "hdl": 0x99999,
                                       "add": 0x20},
                                   2: CACHED},
                             hres_map={0x12345: 0x4ABC0000,
                                       0x99999: 0x30})
    # negative addend: sx32 sign-extends the sum
    C["t51-neg-add"] = t51c(elems={0: CACHED,
                                  1: {"flag": 2, "hdl": 0x12345,
                                      "add": 0xFFFFFFF0},
                                  2: CACHED})
    # element handle with low2==0 passes through RES verbatim
    C["t51-elem-ptr"] = t51c(elems={0: CACHED,
                                   1: {"flag": 2, "hdl": ELEMH,
                                       "add": 0x20},
                                   2: CACHED})
    # ---- thunk entry: 0051B9E0 jmp -> 0051F240 ----
    C["t51t-thunk"] = t51c(steps=[(T51T, CTX, 1)])
    # ---- E20 ----
    C["e20-basic"] = {"e94": 0x1200, "steps": [(E20, E20P, 0)]}
    # u32 add — d=0xFFFFFFF0 zero-extends into rcx
    C["e20-big"] = {"e94": 0xFFFFFFF0, "steps": [(E20, E20P, 0)]}
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])
def W(x): return struct.pack("<i", x)

MUTS = [
    # T51: shl r8d,0x1e -> 0x1f (mode becomes sign bit only: mode2->0)
    ("m-t51-shl",    0x51F254, B(0x1E), B(0x1F), "t51-mode2"),
    # T51: cmp r8d,1 -> cmp r8d,2 (mode-1 arm unreachable)
    ("m-t51-mode",   0x51F263, B(0x01), B(0x02), "t51-mode1"),
    # T51: mode-1 lea SIB scale 2->4 (elem stride 80)
    ("m-t51-elem",   0x51F26C, B(0x49), B(0x89), "t51-mode1-idx2"),
    # T51: mode-1 shl 4 -> 3 (elem stride 24)
    ("m-t51-st48",   0x51F270, B(0x04), B(0x03), "t51-mode1-idx2"),
    # T51: mode-0 lea SIB scale 2->4 (elem stride 80)
    ("m-t51-elem0",  0x51F289, B(0x49), B(0x89), "t51-idx2"),
    # T51: mode-0 shl 4 -> 3 (elem stride 24)
    ("m-t51-st48b",  0x51F28D, B(0x04), B(0x03), "t51-idx2"),
    # T51: mode-1 table disp +8 -> +0x10
    ("m-t51-table",  0x51F274, B(0x08), B(0x10), "t51-mode1"),
    # T51: mode-0 table disp +8 -> +0x10 (RES arg = 0)
    ("m-t51-m0tab",  0x51F27A, B(0x08), B(0x10), "t51-mode0-lazy"),
    # T51: flag test bit 2 -> 4 (lazy write-back skipped)
    ("m-t51-flag",   0x51F2A5, B(0x02), B(0x04), "t51-mode0-lazy"),
    # T51: elem handle disp +0x10 -> +0x18 (resolves the old cache)
    ("m-t51-hdl",    0x51F2AB, B(0x10), B(0x18), "t51-mode0-lazy"),
    # T51: addend disp +0x20 -> +0x24
    ("m-t51-add",    0x51F2B3, B(0x20), B(0x24), "t51-mode0-lazy"),
    # T51: write-back disp +0x18 -> +0x20 (clobbers the addend)
    ("m-t51-wb",     0x51F2BA, B(0x18), B(0x20), "t51-mode0-lazy"),
    # T51: return disp +0x18 -> +0x20 (returns the addend)
    ("m-t51-ret",    0x51F2BE, B(0x18), B(0x20), "t51-mode0-lazy"),
    # T51T: jmp E9 -> call E8 (returns into int3 -> fault)
    ("m-t51t-jmp",   0x51B9E0, B(0xE9), B(0xE8), "t51t-thunk"),
    # E20: offset disp +0x94 -> +0x98
    ("m-e20-disp",   0x370E22, B(0x94), B(0x98), "e20-basic"),
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
    keys = ("trace", "rets", "elems", "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case, raw, secs)
        mod = run_model(case)
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
        mod = run_model(case)
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
