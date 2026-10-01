# EXP-120 exp108-tail-resolvers-exec — native replay harness.
#
# Executes EXP-108's two remaining scripted boundaries — both carried
# a stale "deep subtree" estimate; both are thin:
#
#   F56 003E56A0 24B — rdx = q[rcx+0x400]; null -> 0;
#        else ret = sx32( zx16(w[rdx+2]) + edx )
#        NOTE: mov rdx clobbers the ARGUMENT — edx is now the table
#        pointer's low dword, so the second parameter is dead and the
#        body is effectively tab + w[tab+2] sign-extended.
#   F60 00370F60 61B — rbx = sx32(edx); (idx&0xFFFF)==0xFFFF -> 0;
#        else ret = BASE(d[p+0x84]) + sx32(idx)*0x290 + 0x80
#        (0x290-stride record lookup; the ==0xFFFF test is on low16,
#        so idx=0xFFFF0000 proceeds with sx32 = -65536)
#   BASE 0020E600 10B — arena codec base (real, rerun in-tree)
#
# ZERO scripted boundaries — every call target executes real.
# Native and model must agree on rets/faults.

import ctypes
import hashlib
import json
import struct
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, \
    UC_HOOK_MEM_UNMAPPED, UC_PROT_ALL, UcError
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_RSP

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

IMG_LO = 0x120000
IMG_HI = 0x30A0000
HEAP   = 0x40000000
HIMEM  = 0x7FF00000          # extra region for sign-extension cases
STACK  = 0x61000000
RETQ   = 0x62000000

F56  = 0x003E56A0
F60  = 0x00370F60
BASE = 0x0020E600

CODEC = 0x01F83530   # q: arena codec base (shipped global)

# planted fixture addresses
REC    = HEAP + 0x100000          # F56's rec arg (q[+0x400] table)
TAB    = HEAP + 0x200000          # F56 table (w[+2] inline offset)
F60P   = HEAP + 0x300000          # F60's pointer arg (d[+0x84] off)
HITAB  = HIMEM + 0xF9000          # 0x7FFF9000 — sign-edge table
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


def build_fixture(case):
    """bytes/plants shared by native World and python model."""
    W = []
    # --- F56: rec -> q[+0x400] = tab; tab -> w[+2] inline offset ---
    W.append((REC + 0x400, qw(case.get("tab", TAB))))
    tab = case.get("tab", TAB)
    if tab == TAB:
        W.append((TAB + 2, ww(case.get("w2", 0x180))))
        W.append((TAB + 4, ww(case.get("w4", 0x2222))))
    elif tab == HITAB:
        W.append((HITAB + 2, ww(case.get("w2", 0x8000))))
    # --- F60: p -> d[+0x84] codec offset ---
    W.append((F60P + 0x84, dw(case.get("off84", 0x100) & 0xFFFFFFFF)))
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
        gm.map(HIMEM, 0x120000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        for addr, dat in build_fixture(case):
            gm.w(addr, dat)
        for addr, dat in case.get("patch_bytes", []):
            gm.w(addr, dat)
        self.faults, self.rets = [], []
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)

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
        return {"faults": self.faults, "rets": self.rets}


# ---------------- python model ----------------
# the model interprets the same planted fixture bytes — md/mw/mq/mb
# read the shared image so there is no parallel param copy.

def sx32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v


VALID = ((HEAP, HEAP + 0x1000000), (HIMEM, HIMEM + 0x120000),
         (IMG_LO, IMG_HI))


class Model:
    def __init__(self, case):
        self.case = case
        self.mem = {}
        for addr, dat in build_fixture(case):
            for i, b in enumerate(dat):
                self.mem[addr + i] = b
        self.faults, self.rets = [], []

    def mb(self, a): return self.mem.get(a & 0xFFFFFFFFFFFFFFFF, 0)
    def mw(self, a): return self.mb(a) | (self.mb(a + 1) << 8)
    def md(self, a):
        return self.mb(a) | (self.mb(a + 1) << 8) | \
            (self.mb(a + 2) << 16) | (self.mb(a + 3) << 24)
    def mq(self, a): return self.md(a) | (self.md(a + 4) << 32)

    def mapped(self, a):
        return any(lo <= a < hi for lo, hi in VALID)

    def base(self, arg):
        """0020E600 — ARENA + u32(arg)."""
        return (self.mq(CODEC) + (arg & 0xFFFFFFFF)) & \
            0xFFFFFFFFFFFFFFFF

    def f56(self, rec):
        """003E56A0 — edx arg is DEAD (clobbered by mov rdx);
        ret = sx32( zx16(w[tab+2]) + low32(tab) )."""
        tab = self.mq(rec + 0x400)
        if tab == 0:
            return 0
        if not self.mapped(tab + 2):
            self.faults.append(tab + 2)
            return None
        return sx32(self.mw(tab + 2) + (tab & 0xFFFFFFFF)) & \
            0xFFFFFFFFFFFFFFFF

    def f60(self, p, idx):
        """00370F60 — (idx&0xFFFF)==0xFFFF -> 0; else
        BASE(d[p+0x84]) + sx32(idx)*0x290 + 0x80."""
        if idx & 0xFFFF == 0xFFFF:
            return 0
        if not self.mapped(p + 0x84):
            self.faults.append(p + 0x84)
            return None
        return (self.base(self.md(p + 0x84)) +
                sx32(idx) * 0x290 + 0x80) & 0xFFFFFFFFFFFFFFFF


def run_model(case):
    m = Model(case)
    for entry, rcx, rdx in case.get("steps", []):
        if entry == F56:
            m.rets.append(m.f56(rcx))
        elif entry == F60:
            m.rets.append(m.f60(rcx, rdx & 0xFFFFFFFF))
        elif entry == BASE:
            m.rets.append(m.base(rcx))
    return {"faults": m.faults, "rets": m.rets}


# ---------------- cases ----------------

def f56c(**kw):
    c = {"steps": [(F56, REC, 0x99)]}
    c.update(kw)
    return c


def f60c(**kw):
    c = {"off84": 0x100, "steps": [(F60, F60P, 3)]}
    c.update(kw)
    return c


def build_cases():
    C = {}
    # ---- F56: tab -> w[tab+2] + low32(tab) ----
    C["f56-basic"] = f56c()
    # the edx argument is dead: two calls, different args, same ret
    C["f56-deadarg"] = f56c(steps=[(F56, REC, 0),
                                  (F56, REC, 0xDEADBEEF)])
    C["f56-null"] = f56c(tab=0)
    C["f56-word0"] = f56c(w2=0)
    C["f56-negword"] = f56c(w2=0xFFFF)          # zx16, not sx16
    # sum bit31 set -> cdqe sign-extends the pointer-shaped result
    C["f56-sign"] = f56c(tab=HITAB, w2=0x8000)
    # table pointer outside every mapped region -> real fault
    C["f56-badptr"] = f56c(tab=0xFFFFFFF0)
    # ---- F60: BASE + sx32(idx)*0x290 + 0x80 ----
    C["f60-basic"] = f60c()
    C["f60-neg1"] = f60c(steps=[(F60, F60P, 0xFFFFFFFF)])
    # low16 mask: 0x0001FFFF caught, 0xFFFF0000 proceeds (sx32<0)
    C["f60-low16"] = f60c(steps=[(F60, F60P, 0x0001FFFF)])
    C["f60-hineg"] = f60c(steps=[(F60, F60P, 0xFFFF0000)])
    C["f60-neg2"] = f60c(steps=[(F60, F60P, 0xFFFFFFFE)])
    C["f60-zero"] = f60c(steps=[(F60, F60P, 0)])
    C["f60-off0"] = f60c(off84=0)
    return C


# ---------------- mutations (verified byte-precise) ----------------

def B(x): return bytes([x])

MUTS = [
    # F56: table disp +0x400 -> +0x408 (reads zero -> ret 0)
    ("m-f56-tab",   0x3E56A3, B(0x00), B(0x08), "f56-basic"),
    # F56: test rdx,rdx -> test rcx,rcx (rcx=REC nonzero: null case
    # falls into the movzx and faults at 0x2)
    ("m-f56-test",  0x3E56A9, B(0xD2), B(0xC9), "f56-null"),
    # F56: jne -> je (nonnull table returns 0)
    ("m-f56-jne",   0x3E56AA, B(0x75), B(0x74), "f56-basic"),
    # F56: movzx word -> byte (w=0x180 reads as 0x80)
    ("m-f56-movzx", 0x3E56B0, B(0xB7), B(0xB6), "f56-basic"),
    # F56: word disp +2 -> +4 (reads the adjacent field)
    ("m-f56-wdisp", 0x3E56B2, B(0x02), B(0x04), "f56-basic"),
    # F56: add eax,edx -> sub eax,edx
    ("m-f56-add",   0x3E56B3, B(0x03), B(0x2B), "f56-basic"),
    # F56: cdqe (48 98) -> REX nop (sum bit31: rax upper stays 0)
    ("m-f56-cdqe",  0x3E56B6, B(0x98), B(0x90), "f56-sign"),
    # F60: movsxd rbx,edx -> movsxd rbx,eax (rbx=0 -> product 0)
    ("m-f60-sx",    0x370F68, B(0xDA), B(0xD8), "f60-basic"),
    # F60: cmp value 0xffff -> 0xfffe (idx=-1 proceeds)
    ("m-f60-ffff",  0x370F6A, B(0xFF), B(0xFE), "f60-neg1"),
    # F60: je -> jne (valid idx returns 0)
    ("m-f60-je",    0x370F71, B(0x74), B(0x75), "f60-basic"),
    # F60: offset disp +0x84 -> +0x88
    ("m-f60-disp",  0x370F75, B(0x84), B(0x88), "f60-basic"),
    # F60: stride 0x290 -> 0x280
    ("m-f60-st290", 0x370F84, B(0x90), B(0x80), "f60-basic"),
    # F60: sub rax,-0x80 -> add rax,-0x80
    ("m-f60-add80", 0x370F8A, B(0xE8), B(0xC0), "f60-basic"),
    # F60: add rax,r8 -> sub rax,r8
    ("m-f60-addr8", 0x370F8D, B(0x03), B(0x2B), "f60-basic"),
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
    keys = ("rets", "faults")
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
