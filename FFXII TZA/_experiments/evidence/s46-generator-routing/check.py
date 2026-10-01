# S-46 generator routing — which consumer advances which generator
# state, executed on shipped bytes under Unicorn. One representative
# consumer per claimed route; all four generator states are planted
# distinguishably; every case snapshots all four states before/after
# and records reads/writes against them.
#
#   states      gameplay MT19937  02EB3870[624], idx 02EB4230, flag 02EB4234
#               graphics MT19937  01F79C00[624] (pinned by 0015BCF0's
#                                 lea rcx,[rip+state] — I5's "may not
#                                 exist" is resolved: the address is
#                                 fixed, only the TWIST takes it as an
#                                 argument)
#               shared LCG        022C256C (ANSI-C, *0x41C64E6D+0x3039 x3)
#               presentation PRNG 01EF93E8 (bit-feedback, S-10 law)
#
#   consumers   lcg-loot-inliner  003185D0 Loot_RollNormalSlotChance —
#                                 inlines the recurrence on 022C256C
#               lcg-yaw           00239210 — calls 00328370 (the one
#                                 non-inlined draw), then % 360
#               mt-weather-2/-1   0025ABA0(slot) — draws at 0025ABB8 in
#                                 the current==2 arm only
#               mt-roll-20000     0038DB10 — leaf roll, % 20000
#               mt-roll-100       00389670 — leaf percent-gate roll
#               prng-render       004005E0 — guarded inline draw on
#                                 01EF93E8, float result
#               gfxmt-seed        0015BCF0 — _time64/_clock stubs ->
#                                 0018D680 mix -> 0018D740 -> 0018EE20
#               gfxmt-draw        0018D740(state, 0x5555AAAA) direct
#
#   scripted boundaries: the two CRT imports inside 0015BCF0
#   (_time64, and the second time source) plus the generic IAT
#   boundary (unresolvable in isolation). Everything else executes
#   shipped bytes, including every generator body.

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
STACK = 0x61000000
RETQ = 0x62000000

# --- generator state cells ------------------------------------------
MT_STATE = 0x2EB3870            # 624 dwords
MT_IDX = 0x2EB4230
MT_FLAG = 0x2EB4234
MT_SEEDER = 0x863D30            # wrapper (flag -> implicit 5489 -> seed)
LCG_STATE = 0x22C256C
PRNG_STATE = 0x1EF93E8
GFX_STATE = 0x1F7F600           # pinned by 0015BCF0's lea rcx,[rip+..]
GFX_CURSOR = 0x1F7FFC0          # q: consumer's walking state pointer
GFX_COUNT = 0x1F7FFC8           # d: consumer's remaining-count
RESOLVER_BASE = 0x1F83530       # q: encoded-table base (0020E600)
PRNG_GUARD = 0x22D9138          # d: draw-enable flag for 004005E0

PLANT_LCG = 0x11111111
PLANT_PRNG = 0x22222222
PLANT_GFX = 0x33333333
MT_SEED = 0xACE1                # planted via the REAL seeder body

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


def import_map(raw, secs):
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


WATCHES = [
    ("mt", MT_STATE, MT_STATE + 0x9C4),       # state array + index
    ("mt-flag", MT_FLAG, MT_FLAG + 4),
    ("lcg", LCG_STATE, LCG_STATE + 4),
    ("prng", PRNG_STATE, PRNG_STATE + 4),
    ("gfx", GFX_STATE, GFX_STATE + 0x9C4),
    ("gfx-book", GFX_CURSOR, GFX_COUNT + 4),
]


class World:
    def __init__(self, case, raw, secs, imports):
        self.case, self.imports = case, imports
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x100000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        self.hbuf = HEAP + 0x1000     # fixture bump cursor
        self.calls = []
        self.accesses = []            # (watch-name, 'r'/'w', addr, size)
        self.faults = []
        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_MEM_READ, self.on_read)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self.on_write)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    def alloc(self, n, fill=0):
        a = self.hbuf
        self.hbuf = (a + n + 0xF) & ~0xF
        if fill:
            self.gm.w(a, bytes([fill]) * n)
        return a

    def _tag(self, addr):
        for name, lo, hi in WATCHES:
            if lo <= addr < hi:
                return name
        return None

    def on_read(self, uc, access, addr, size, value, _):
        t = self._tag(addr)
        if t:
            self.accesses.append((t, "r", hex(addr), size))

    def on_write(self, uc, access, addr, size, value, _):
        t = self._tag(addr)
        if t:
            self.accesses.append((t, "w", hex(addr), size,
                                  hex(value & ((1 << (size * 8)) - 1))))

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", hex(uc.reg_read(UC_X86_REG_RIP))))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        kind = "memr" if access in (16, 19) else \
               "memf" if access in (18, 21) else "memw"
        self.faults.append((kind, hex(addr),
                            hex(uc.reg_read(UC_X86_REG_RIP))))
        uc.emu_stop()
        return False

    def _ret(self, uc):
        uc.reg_write(UC_X86_REG_RIP,
                     self.gm.qw(uc.reg_read(UC_X86_REG_RSP)))
        uc.reg_write(UC_X86_REG_RSP,
                     uc.reg_read(UC_X86_REG_RSP) + 8)

    def _iat_stub(self, uc, addr):
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
        self.calls.append(("iat:" + name, hex(rcx)))
        if short == "_time64":
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("time64", 0x1BADD00D))
        else:
            uc.reg_write(UC_X86_REG_RAX,
                         self.case.get("clockv", 0x0C0FFEE))
        if op == b"\xff\x25":
            self._ret(uc)
        else:
            uc.reg_write(UC_X86_REG_RIP, addr + off + 6)
        return True

    def on_code(self, uc, addr, size, _):
        b0 = self.gm.r(addr, 3)
        if b0[:2] in (b"\xff\x25", b"\xff\x15") or \
                b0[1:3] in (b"\xff\x25", b"\xff\x15"):
            if self._iat_stub(uc, addr):
                return
        if addr in (0x328370, 0x379CD0, 0x863BF0, 0x18D740, 0x18EE20,
                    0x18D680, 0x2658B0, 0x20E600, 0x31B760, 0x316DA0):
            self.calls.append(("enter%x" % addr,
                               hex(uc.reg_read(UC_X86_REG_RCX)),
                               hex(uc.reg_read(UC_X86_REG_RDX))))
        if addr == self.case.get("stopat", -1):
            self.faults.append(("stopat", hex(addr)))
            uc.emu_stop()

    def run(self, entry, regs=None, xmm=None):
        self.uc.reg_write(UC_X86_REG_RSP, STACK + 0x80000)
        self.uc.reg_write(UC_X86_REG_RIP, entry)
        self.gm.w(STACK + 0x80000, qw(RETQ))
        for r, v in (regs or {}).items():
            self.uc.reg_write(r, v)
        for r, v in (xmm or {}).items():
            self.uc.reg_write(r, v)
        try:
            self.uc.emu_start(entry, RETQ)
        except UcError as e:
            if not self.faults:
                self.faults.append(("ucerr", str(e),
                                    hex(self.uc.reg_read(
                                        UC_X86_REG_RIP))))

    # --- four-state snapshots ----------------------------------------
    def snapshot(self):
        gm = self.gm
        st = struct.unpack("<624I", gm.r(MT_STATE, 624 * 4))
        g = struct.unpack("<624I", gm.r(GFX_STATE, 624 * 4))
        return {
            "mt_idx": gm.dw(MT_IDX),
            "mt_flag": gm.r(MT_FLAG, 1)[0],
            "mt_hash": hashlib.sha1(gm.r(MT_STATE, 0x9C0)).hexdigest()[:12],
            "mt_head": [hex(x) for x in st[:3]],
            "lcg": hex(gm.dw(LCG_STATE)),
            "prng": hex(gm.dw(PRNG_STATE)),
            "gfx_hash": hashlib.sha1(gm.r(GFX_STATE, 0x9C0)).hexdigest()[:12],
            "gfx_head": [hex(x) for x in g[:3]],
            "gfx_cursor": hex(gm.qw(GFX_CURSOR)),
            "gfx_count": hex(gm.dw(GFX_COUNT)),
        }

    def plant_states(self):
        """Distinguishable contents in all four generators. The
        gameplay MT is seeded by its REAL seeder body (flag pre-set so
        the implicit-5489 pass is skipped)."""
        self.gm.w(MT_FLAG, b"\x01")
        self.uc.reg_write(UC_X86_REG_RSP, STACK + 0x80000)
        self.gm.w(STACK + 0x80000, qw(RETQ))
        self.uc.reg_write(UC_X86_REG_ECX, MT_SEED)
        try:
            self.uc.emu_start(MT_SEEDER, RETQ)
        except UcError as e:
            self.faults.append(("seed-ucerr", str(e),
                                hex(self.uc.reg_read(UC_X86_REG_RIP))))
        self.gm.w(LCG_STATE, dw(PLANT_LCG))
        self.gm.w(PRNG_STATE, dw(PLANT_PRNG))
        pat = b"".join(dw(PLANT_GFX + i) for i in range(624))
        self.gm.w(GFX_STATE, pat)
        self.gm.w(GFX_CURSOR, qw(GFX_STATE))
        self.gm.w(GFX_COUNT, dw(624))


def lcg3(s):
    """Three ANSI-C rounds — the recurrence inside 00328370."""
    for _ in range(3):
        s = (s * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return s


def diff(before, after):
    out = {}
    for k in before:
        if before[k] != after[k]:
            out[k] = [before[k], after[k]]
    return out


def run_case(name, case, raw, secs, imports):
    w = World(case, raw, secs, imports)
    entry = case["entry"]

    # --- fixtures -----------------------------------------------------
    if name == "lcg-loot-inliner":
        # descriptor at q[0x2EBF0C0]: {d+4 count, w+8 stride, d+C row}
        desc = w.alloc(0x40)
        w.gm.w(0x2EBF0C0, qw(desc))
        w.gm.w(desc + 4, dw(case.get("count", 4)))
        w.gm.w(desc + 8, b"\x04\x00")          # stride 4
        w.gm.w(desc + 0xC, dw(0))              # resolver index 0
        table = w.alloc(0x40)
        w.gm.w(table, bytes(case.get(
            "probs", [60, 10, 90, 30, 55, 45, 80, 20,
                      5, 95, 40, 70, 15, 85, 25, 65])))
        w.gm.w(RESOLVER_BASE, qw(table))         # encoded-table base
    elif name == "lcg-yaw":
        buf = w.alloc(0x200)
        sub = w.alloc(0x800)
        obj = w.alloc(0x800)
        w.gm.w(sub + 0x6A0, qw(buf))
        w.gm.w(obj + 0x30, qw(sub))
        case.setdefault("regs", {})[UC_X86_REG_RCX] = obj
        case.setdefault("xmm", {})[UC_X86_REG_XMM1] = int.from_bytes(
            struct.pack("<f", case.get("yaw_in", -1.0)) + b"\0" * 12,
            "little")
    elif name == "prng-render":
        w.gm.w(PRNG_GUARD, dw(1))               # guard: draw enabled
    elif name == "gfxmt-draw":
        case.setdefault("regs", {})[UC_X86_REG_RCX] = GFX_STATE
        case.setdefault("regs", {})[UC_X86_REG_EDX] = 0x5555AAAA

    w.plant_states()
    before = w.snapshot()
    w.accesses.clear()
    w.run(entry, regs=case.get("regs"), xmm=case.get("xmm"))
    after = w.snapshot()

    return {
        "before": before, "after": after,
        "delta": diff(before, after),
        "accesses": w.accesses,
        "calls": w.calls,
        "faults": w.faults,
        "lcg_expect": hex(lcg3(PLANT_LCG)),
    }


CASES = {
    "lcg-loot-inliner": {"entry": 0x3185D0,
                         "regs": {UC_X86_REG_ECX: 1, UC_X86_REG_EDX: 2}},
    "lcg-yaw": {"entry": 0x239210},
    "mt-weather-2": {"entry": 0x25ABA0,
                     "regs": {UC_X86_REG_ECX: 2}},
    "mt-weather-1": {"entry": 0x25ABA0,
                     "regs": {UC_X86_REG_ECX: 1}},
    "mt-roll-20000": {"entry": 0x38DB10},
    "mt-roll-100": {"entry": 0x389670},
    "prng-render": {"entry": 0x4005E0},
    "gfxmt-seed": {"entry": 0x15BCF0},
    "gfxmt-draw": {"entry": 0x18D740},
}


def check():
    raw, secs = load_image()
    imports = import_map(raw, secs)
    results, fails = {}, []

    def expect(name, cond, msg):
        if not cond:
            fails.append("%s: %s" % (name, msg))

    for name, case in CASES.items():
        r = run_case(name, case, raw, secs, imports)
        results[name] = r
        d = r["delta"]
        acc_names = {a[0] for a in r["accesses"]}
        expect(name, not r["faults"],
               "faults %s" % (r["faults"],))
        # every case must touch exactly its claimed generator
        if name.startswith("lcg-"):
            expect(name, "lcg" in acc_names,
                   "no LCG access: %s" % (acc_names,))
            expect(name, "lcg" in d,
                   "LCG unchanged: %s" % (d,))
            expect(name, not any(k.startswith(t) for k in d
                   for t in ("mt", "prng", "gfx")),
                   "unexpected generator touched: %s" % (d,))
        elif name.startswith("mt-weather-1") or name == "mt-weather-1":
            pass
        elif name.startswith("mt-"):
            expect(name, any(k.startswith("mt") for k in d),
                   "MT unchanged: %s" % (d,))
            expect(name, not any(k.startswith(t) for k in d
                   for t in ("lcg", "prng", "gfx")),
                   "unexpected generator touched: %s" % (d,))
        elif name.startswith("prng-"):
            expect(name, "prng" in d,
                   "PRNG unchanged: %s" % (d,))
            expect(name, not any(k.startswith(t) for k in d
                   for t in ("lcg", "mt", "gfx")),
                   "unexpected generator touched: %s" % (d,))
        elif name.startswith("gfxmt-"):
            expect(name, any(k.startswith("gfx") for k in d),
                   "gfx state unchanged: %s" % (d,))
            expect(name, not any(k.startswith(t) for k in d
                   for t in ("lcg", "mt", "prng")),
                   "unexpected generator touched: %s" % (d,))

    # case-specific
    if "mt-weather-1" in results:
        expect("mt-weather-1", results["mt-weather-1"]["delta"] == {},
               "slot-1 arm should touch NO generator: %s"
               % (results["mt-weather-1"]["delta"],))
    if "lcg-loot-inliner" in results:
        r = results["lcg-loot-inliner"]
        expect("lcg-loot-inliner",
               r["after"]["lcg"] == r["lcg_expect"],
               "LCG end state %s != three-round %s"
               % (r["after"]["lcg"], r["lcg_expect"]))
    if "lcg-yaw" in results:
        r = results["lcg-yaw"]
        expect("lcg-yaw", r["after"]["lcg"] == r["lcg_expect"],
               "LCG end state %s != three-round %s"
               % (r["after"]["lcg"], r["lcg_expect"]))

    out = {"cases": len(results), "results": results,
           "failures": fails}
    with open(RESULT, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"cases": len(results), "failures": fails},
                     indent=1))


if __name__ == "__main__":
    check()
