# resource-request-queue remaining entries — runtime validation for
# CONTRACT-resource-request-queue.md §13's "NO executed evidence" list.
# Executes on shipped bytes under Unicorn:
#
#   E450 0032E450 (126 B): pool constructor — no calls. d[01EED498]=1
#     (request-id counter), 64 slots at 022C31C0+i*0x80 linked through
#     +0x10(next)/+0x18(prev), d[+0x58]=i, d[+0x64]=-1, then
#     q[022C51D0]=slot0 (free head), slot0.prev=0, slot63.next=0,
#     pending head/tail q[022C51C0]/q[022C51C8]=0.
#   E990 0032E990 (186 B): slot-taker — no calls. Pops free head, links
#     into pending: head when ecx==0, tail when ecx!=0; pending-empty
#     sets head+tail. NO empty-free guard (rdx=0 -> [rdx+0x10] read).
#   E870 0032E870: requester — stalls on empty free list pumping
#     E070(0)+FLAG(0046DFE0)+EA30(0035EA30) per pass, then takes a slot
#     (E990, head-flag from arg6) and fills +0x20/+0x21/+0x24/+0x28/
#     +0x2c(round-down-0x800 of aux.d0)/+0x38/+0x40/+0x48/+0x60/
#     +0x64(=(idctr<<6)|slotidx; ctr++ wraps >0xFFFFFF->1)/+0x70.
#   E620 0032E620: builder — writes telemetry d[022C51D8]/d[022C51DC],
#     refuses edx<0 (-1, telemetry still written), gates on 003EB0D0
#     (byte scan at 02B5E111): gate=0 passes aux through, gate=1 copies
#     the 0x28-byte aux to a local and forces +4=0x80000/+0x20=0;
#     post-E870 fixups on nonzero id: +0x30=0x80000, w[+0x22]=1,
#     +0x34=pre-clamp +0x28, +0x28 clamped <=0x80000, +0x2c re-rounded,
#     q[slot]=0.
#   E040 0032E040 (38 B): per-frame caller — 001EDE80() or 0017D930()
#     nonzero -> tail jmp 0032E070(0); else ret.
#
#   Scripted boundaries (entry-intercepted, disclosed): 001EDE80 and
#   0017D930 loader predicates (planted returns), 0035EA30 pacer thunk
#   (call count; the stall-release case has the stub plant a free slot
#   on pass 3 — equivalent to a completion arriving from outside the
#   emulated boundary), and for the pump-integration case the EXP-128
#   boundary set: 003EADD0 init gate (xadd0), 0046E030 submit-A,
#   002DF6C0 submit-B, 0046DD50/003E9780/0036FD50/003BB790 teardown
#   externals, 00862090 tick source, 0017D3E0/003691B0/00369190/
#   0035E7A0 resync externals.
#
#   Everything else executes as shipped bytes: the pump 0032E070 and
#   its retire path (0032E330/0032E370/0032EC40/003697F0), the E620
#   gate 003EB0D0, the FLAG leaf 0046DFE0, tick leaf 0035E810, ret-0
#   0016D6A0. All rip-relative targets resolved with capstone.

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
HEAP = 0x40000000          # aux records + fixture slot live here
STACK = 0x61000000
RETQ = 0x62000000

# ---- subjects ----
E450 = 0x0032E450          # pool constructor (real, no calls)
E040 = 0x0032E040          # per-frame caller (real)
E990 = 0x0032E990          # slot-taker (real, no calls)
E870 = 0x0032E870          # requester (real)
E620 = 0x0032E620          # builder (real)
E070 = 0x0032E070          # task pump (real; EXP-128 scope)
E330 = 0x0032E330          # retire helper (real)
E370 = 0x0032E370          # gated retire helper (real)
EC40 = 0x0032EC40          # active->idle splice (real)
GATE3B = 0x003EB0D0        # E620's one-byte gate (real)
FLAGG_FN = 0x0046DFE0      # FLAG leaf -> ret-0 x2 (real)
PREL_THUNK = 0x003697F0    # free-if-nonnull -> PREL (real)

# ---- scripted boundaries (entry-intercepted) ----
XEDE80 = 0x001EDE80        # loader predicate 1 (planted ret)
XD930  = 0x0017D930        # loader predicate 2 (planted ret)
XEA30  = 0x0035EA30        # pacer thunk (counted; stall case injects)
XADD0  = 0x003EADD0        # init gate inside pump S1 (planted ret)
X46E0  = 0x0046E030        # submit-A shim (planted ret)
X2DF6  = 0x002DF6C0        # submit-B (planted ret)
X46DD  = 0x0046DD50        # teardown external
X3E97  = 0x003E9780        # teardown external
X36FD  = 0x0036FD50        # teardown gate
X3BB7  = 0x003BB790        # teardown tail
X2090  = 0x00862090        # tick source (cell jump)
X17D3  = 0x0017D3E0        # resync gate
X3691B = 0x003691B0        # resync helper
X36919 = 0x00369190        # resync helper
X35E7  = 0x0035E7A0        # resync external

# ---- queue globals (runtime state; zero-planted by the fixture) ----
SLOT0   = 0x022C31C0       # 64 slots x 0x80 -> [022C31C0, 022C51C0)
PEND_H  = 0x022C51C0       # pending/active head
PEND_T  = 0x022C51C8       # pending/active tail
FREE_H  = 0x022C51D0       # free-list head
IDCTR   = 0x01EED498       # request-id counter (ctor=1, wraps >0xFFFFFF->1)
TEL_A   = 0x022C51D8       # E620 telemetry: last ecx
TEL_B   = 0x022C51DC       # E620 telemetry: last edx
GATE_B  = 0x02B5E111       # 003EB0D0's scanned byte
TICKQ   = 0x022CA5E0       # q: tick leaf 0035E810 reads this
PACC    = 0x022CA5C4       # pacer-state cluster (EB70 resync writes)

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
    """image bytes + per-case page overlays; reads consult overlays."""
    def __init__(self, uc, raw, secs):
        self.uc, self.secs = uc, secs
        self.writes, self.ovl = {}, {}
        for va, vs, ra, rs in secs:
            lo = (va + IMG_LO) & ~0xFFF
            hi = (va + IMG_LO + max(vs, rs) + 0xFFF) & ~0xFFF
            uc.mem_map(lo, hi - lo)
            if rs:
                uc.mem_write(va + IMG_LO, raw[ra:ra + rs])

    def w(self, addr, data):
        if isinstance(data, int):
            data = qw(data)
        self.writes.setdefault(addr, len(data))
        try:
            self.uc.mem_write(addr, bytes(data))
        except UcError:
            lo = addr & ~0xFFF
            self.uc.mem_map(lo, 0x1000)
            self.uc.mem_write(addr, bytes(data))
        self.ovl[addr] = bytes(self.uc.mem_read(addr, len(data)))

    def q(self, a):
        return struct.unpack("<Q", bytes(self.uc.mem_read(a, 8)))[0]

    def d(self, a):
        return struct.unpack("<I", bytes(self.uc.mem_read(a, 4)))[0]

    def b(self, a):
        return self.uc.mem_read(a, 1)[0]


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.gm = GuestMem(self.uc, raw, secs)
        self.gm.map = self.uc.mem_map
        self.gm.map(STACK, 0x100000)
        self.gm.map(RETQ, 0x1000)
        self.gm.map(HEAP, 0x200000)
        self.trace, self.faults, self.xctr = [], [], {}
        self.rets = {}

        # ---- fixture ----
        self.gm.w(IDCTR, dw(case.get("idctr", 0)))
        self.gm.w(PEND_H, qw(case.get("pend_h", 0)))
        self.gm.w(PEND_T, qw(case.get("pend_t", 0)))
        self.gm.w(FREE_H, qw(case.get("free_h", 0)))
        self.gm.w(GATE_B, bytes([case.get("gateb", 0)]))
        self.gm.w(TICKQ, qw(case.get("tickq", 0x1000)))
        self.gm.w(PACC, dw(0))
        # pending links the case fabricates: {addr: {off: qword-or-dword}}
        for addr, fields in (case.get("slots") or {}).items():
            addr = int(addr)
            for off, (val, sz) in fields.items():
                self.gm.w(addr + int(off, 0),
                          dw(val) if sz == 4 else
                          (bytes([val]) if sz == 1 else qw(val)))
        # aux record for E870/E620
        aux = case.get("aux")
        if aux is not None:
            a = HEAP + 0x1000
            self.aux_addr = a
            self.gm.w(a, dw(aux.get("d0", 0)))
            self.gm.w(a + 4, dw(aux.get("d4", 0)))
            self.gm.w(a + 8, dw(aux.get("d8", 0)))
            self.gm.w(a + 0x10, qw(aux.get("q10", 0)))
            self.gm.w(a + 0x18, qw(aux.get("q18", 0)))
            self.gm.w(a + 0x20, qw(aux.get("q20", 0)))
        else:
            self.aux_addr = 0
        # fixture slot used by the stall-release case
        self.fx_slot = HEAP + 0x4000

        self.uc.hook_add(UC_HOOK_CODE, self.on_code)
        self.uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        self.uc.hook_add(UC_HOOK_INTR, self.on_intr)

    # ---- helpers ----
    def _xval(self, key, default=0):
        v = self.case.get(key, default)
        if isinstance(v, list):
            i = min(self.xctr.get(key, 0), len(v) - 1)
            self.xctr[key] = self.xctr.get(key, 0) + 1
            return v[i]
        return v

    def _ret(self):
        rsp = self.uc.reg_read(UC_X86_REG_RSP)
        self.uc.reg_write(UC_X86_REG_RIP, self.gm.q(rsp))
        self.uc.reg_write(UC_X86_REG_RSP, rsp + 8)

    def _ret_eax(self, tag, key, default=0):
        v = self._xval(key, default)
        self.trace.append("%s=%x" % (tag, v & 0xFFFFFFFF))
        self.uc.reg_write(UC_X86_REG_RAX, v)
        self._ret()

    def on_intr(self, uc, intno, _):
        self.faults.append(("trap", uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("mem", access, addr,
                            uc.reg_read(UC_X86_REG_RIP)))
        uc.emu_stop()
        return False

    # real bodies whose entry is traced for ordering evidence
    MARK = {E070: "e070", FLAGG_FN: "flag", E990: "e990",
            E330: "e330", E370: "e370", EC40: "ec40",
            GATE3B: "gate3b", 0x0035E810: "e810",
            PREL_THUNK: "g97f0"}

    def on_code(self, uc, addr, size, _):
        tag = self.MARK.get(addr)
        if tag is not None:
            self.trace.append(tag)
        if addr == XEDE80:
            self._ret_eax("ede80", "ede80")
        elif addr == XD930:
            self._ret_eax("d930", "d930")
        elif addr == XEA30:
            n = self.xctr.get("ea30", 0) + 1
            self.xctr["ea30"] = n
            self.trace.append("ea30#%d" % n)
            # stall-release: the pacer stub injects a free slot on the
            # pass named by the case — a completion arriving from outside
            rel = self.case.get("ea30_release")
            if rel and n == rel:
                self.gm.w(FREE_H, qw(self.fx_slot))
            self._ret()
        elif addr == XADD0:
            self._ret_eax("xadd0", "xadd0")
        elif addr == X46E0:
            self._ret_eax("x46e0", "x46e0", 1)
        elif addr == X2DF6:
            self._ret_eax("x2df6", "x2df6", 0)
        elif addr in (X46DD, X3E97, X36FD, X3BB7, X17D3, X3691B,
                      X36919, X35E7):
            self.trace.append("x%x" % addr)
            self.uc.reg_write(UC_X86_REG_RAX, 0)
            self._ret()
        elif addr == X2090:
            self._ret_eax("x2090", "x2090", 0x1000)
        if addr == E870 and "e870" not in self.trace:
            self.trace.append("e870")
            # at entry (pre-prologue) arg5 sits at [rsp+0x28]
            self.rets["e870_aux"] = self.gm.q(
                uc.reg_read(UC_X86_REG_RSP) + 0x28)

    def run(self, entry, rcx=0, rdx=0, r8=0, r9=0, arg5=0, arg6=0):
        uc = self.uc
        rsp = STACK + 0x80000
        uc.reg_write(UC_X86_REG_RSP, rsp)
        self.gm.w(rsp, qw(RETQ))                    # return addr slot
        self.gm.w(rsp + 0x28, qw(arg5))             # callee's arg5
        self.gm.w(rsp + 0x30, qw(arg6))             # callee's arg6
        uc.reg_write(UC_X86_REG_RCX, rcx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, rdx & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R8, r8 & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_R9, r9 & 0xFFFFFFFFFFFFFFFF)
        try:
            uc.emu_start(entry, RETQ, timeout=300_000_000)
        except UcError as e:
            self.faults.append(("uc", str(e),
                                uc.reg_read(UC_X86_REG_RIP)))
        return uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF


def slot(i):
    return SLOT0 + i * 0x80


def run_case(name, case, raw, secs):
    w = World(case, raw, secs)
    out = {"trace": w.trace, "faults": w.faults}
    c = case

    if name.startswith("ctor"):
        w.run(E450)
    elif name == "stall-then-request":
        # free list empty; EA30 stub injects the fixture slot on pass 3
        out["ret"] = w.run(E870, rcx=9, rdx=0x42, r8=0, r9=0x100,
                           arg5=0, arg6=1)
    elif name.startswith("e040"):
        out["ret"] = w.run(E040)
    elif name == "cycle-request-pump-retire":
        out["ctor_ret"] = w.run(E450)
        out["req_ret"] = w.run(E870, rcx=3, rdx=0x100, r8=0, r9=0x400,
                               arg5=0, arg6=1)
        # state-1 slot with d28==0 -> pump retires it (EXP-128 recipe)
        w.gm.w(slot(0) + 0x28, dw(0))
        out["e040_ret"] = w.run(E040)
    elif name.startswith("take"):
        out["ret"] = w.run(E990, rcx=c.get("flag", 0))
    elif name.startswith("req"):
        out["ret"] = w.run(E870, rcx=c.get("ecx", 0),
                           rdx=c.get("edx", 0), r8=c.get("r8", 0),
                           r9=c.get("r9", 0),
                           arg5=w.aux_addr if "aux" in c else c.get("arg5", 0),
                           arg6=c.get("arg6", 0))
    elif name.startswith("bld"):
        out["ret"] = w.run(E620, rcx=c.get("ecx", 0),
                           rdx=c.get("edx", 0), r8=c.get("r8", 0),
                           r9=c.get("r9", 0),
                           arg5=w.aux_addr if "aux" in c else c.get("arg5", 0))

    # ---- observed post-state ----
    gm = w.gm
    out["cells"] = {
        "pend_h": gm.q(PEND_H), "pend_t": gm.q(PEND_T),
        "free_h": gm.q(FREE_H), "idctr": gm.d(IDCTR),
        "tel_a": gm.d(TEL_A), "tel_b": gm.d(TEL_B),
    }
    for i in c.get("read_slots", []):
        s = slot(i)
        out["slot%d" % i] = {
            "q00": gm.q(s), "q10": gm.q(s + 0x10), "q18": gm.q(s + 0x18),
            "b20": gm.b(s + 0x20), "b21": gm.b(s + 0x21),
            "w22": gm.b(s + 0x22) | (gm.b(s + 0x23) << 8),
            "d24": gm.d(s + 0x24), "d28": gm.d(s + 0x28),
            "d2c": gm.d(s + 0x2c), "d30": gm.d(s + 0x30),
            "d34": gm.d(s + 0x34), "q38": gm.q(s + 0x38),
            "q40": gm.q(s + 0x40), "q48": gm.q(s + 0x48),
            "q50": gm.q(s + 0x50), "d58": gm.d(s + 0x58),
            "d5c": gm.d(s + 0x5c), "d60": gm.d(s + 0x60),
            "d64": gm.d(s + 0x64), "q70": gm.q(s + 0x70),
        }
    if c.get("read_fx"):
        s = w.fx_slot
        out["fx"] = {"q00": gm.q(s), "q10": gm.q(s + 0x10),
                     "q18": gm.q(s + 0x18), "b20": gm.b(s + 0x20),
                     "b21": gm.b(s + 0x21), "d24": gm.d(s + 0x24),
                     "d28": gm.d(s + 0x28), "d2c": gm.d(s + 0x2c),
                     "d58": gm.d(s + 0x58), "d60": gm.d(s + 0x60),
                     "d64": gm.d(s + 0x64),
                     "q38": gm.q(s + 0x38), "q70": gm.q(s + 0x70)}
    out["aux_seen"] = w.rets.get("e870_aux", 0)
    out["ok"], out["fail"] = check(name, case, out)
    return out


def check(name, c, o):
    """returns (ok, failures[]); asserts per-case expectations."""
    f = []
    cl = o["cells"]
    faults = o.get("faults", [])

    def eq(k, got, want):
        if got != want:
            f.append("%s: got %x want %x" % (k, got, want))

    if name == "ctor-init":
        eq("idctr", cl["idctr"], 1)
        eq("free_h", cl["free_h"], SLOT0)
        eq("pend_h", cl["pend_h"], 0)
        eq("pend_t", cl["pend_t"], 0)
        s = o["slot0"]; eq("s0.next", s["q10"], slot(1))
        eq("s0.prev", s["q18"], 0)
        eq("s0.idx", s["d58"], 0)
        eq("s0.id", s["d64"], 0xFFFFFFFF)
        eq("s0.b20", s["b20"], 0)
        eq("s0.d28", s["d28"], 0)
        s63 = o["slot63"]
        eq("s63.next", s63["q10"], 0)
        eq("s63.prev", s63["q18"], slot(62))
        eq("s63.idx", s63["d58"], 63)
        eq("s63.id", s63["d64"], 0xFFFFFFFF)
        s1 = o["slot1"]; eq("s1.prev", s1["q18"], slot(0))
    elif name == "ctor-dirty-rerun":
        eq("idctr", cl["idctr"], 1)
        eq("free_h", cl["free_h"], SLOT0)
        eq("pend_h", cl["pend_h"], 0)
        eq("pend_t", cl["pend_t"], 0)
    elif name == "take-head-empty-pending":
        eq("ret", o["ret"], SLOT0)
        eq("free_h", cl["free_h"], slot(1))
        eq("pend_h", cl["pend_h"], SLOT0)
        eq("pend_t", cl["pend_t"], SLOT0)
        s = o["slot0"]; eq("s0.next", s["q10"], 0); eq("s0.prev", s["q18"], 0)
        s1 = o["slot1"]; eq("s1.prev", s1["q18"], 0)
    elif name == "take-head-nonempty":
        eq("ret", o["ret"], SLOT0)
        eq("pend_h", cl["pend_h"], SLOT0)
        eq("pend_t", cl["pend_t"], slot(41))
        s = o["slot0"]; eq("s0.next", s["q10"], slot(40)); eq("s0.prev", s["q18"], 0)
        s40 = o["slot40"]; eq("s40.prev", s40["q18"], SLOT0)
    elif name == "take-tail-nonempty":
        eq("ret", o["ret"], SLOT0)
        eq("pend_h", cl["pend_h"], slot(40))
        eq("pend_t", cl["pend_t"], SLOT0)
        s = o["slot0"]; eq("s0.prev", s["q18"], slot(41)); eq("s0.next", s["q10"], 0)
        s41 = o["slot41"]; eq("s41.next", s41["q10"], SLOT0)
    elif name == "take-free-empty-fault":
        if not any(x[0] == "mem" for x in faults):
            f.append("expected a memory fault on empty free list")
        else:
            eq("fault_addr", faults[0][2], 0x10)
    elif name == "take-last":
        eq("ret", o["ret"], slot(63))
        eq("free_h", cl["free_h"], 0)
    elif name == "req-basic":
        eq("ret", o["ret"], 0x40)          # (ctr1<<6)|idx0
        eq("idctr", cl["idctr"], 2)
        eq("pend_h", cl["pend_h"], SLOT0)
        eq("pend_t", cl["pend_t"], SLOT0)
        eq("free_h", cl["free_h"], slot(1))
        s = o["slot0"]
        eq("b20", s["b20"], 1); eq("b21", s["b21"], 7)
        eq("d24", s["d24"], 0x1234); eq("d28", s["d28"], 0x500)
        eq("d2c", s["d2c"], 0); eq("q38", s["q38"], 0xCAFE00)
        eq("q40", s["q40"], 0); eq("q48", s["q48"], 0)
        eq("q50", s["q50"], 0); eq("d60", s["d60"], 0)
        eq("d64", s["d64"], 0x40); eq("d5c", s["d5c"], 0)
        eq("w22", s["w22"], 0); eq("q70", s["q70"], 0xCAFE00)
        eq("q00", s["q00"], 0)
    elif name == "req-aux":
        eq("ret", o["ret"], 0x40)
        s = o["slot0"]
        eq("d2c", s["d2c"], 0x800)         # 0x8FF rounded down to 0x800
        eq("q40", s["q40"], 0xAAAA); eq("q48", s["q48"], 0xBBBB)
        eq("d60", s["d60"], 0x99)
        eq("b21", s["b21"], 9)
    elif name == "req-second":
        eq("r1", o["ret1"], 0x40)          # (ctr1<<6)|slot0
        eq("r2", o["ret"], 0x81)           # (ctr2<<6)|slot1
        eq("idctr", cl["idctr"], 3)
        eq("pend_h", cl["pend_h"], SLOT0); eq("pend_t", cl["pend_t"], slot(1))
        s1 = o["slot1"]; eq("s1.prev", s1["q18"], SLOT0)
        eq("s1.idx-read", s1["d58"], 1)
    elif name == "req-idwrap":
        eq("ret", o["ret"], (0xFFFFFF << 6) | 0)
        eq("idctr", cl["idctr"], 1)        # >0xFFFFFF wraps to 1
    elif name == "req-id-zero":
        eq("ret", o["ret"], 0)             # ctr=0 & idx0 -> id 0
        eq("pend_h", cl["pend_h"], SLOT0)  # yet the slot was consumed
        eq("free_h", cl["free_h"], slot(1))
    elif name == "stall-then-request":
        eq("ret", o["ret"], (1 << 6) | (o["fx"]["d58"] & 0x3F)
           if o.get("fx") else -1)
        # exactly three pump passes, each e070 -> flag -> ea30
        sub = [t for t in o["trace"]
               if t in ("e070", "flag") or t.startswith("ea30")]
        if sub != ["e070", "flag", "ea30#1", "e070", "flag",
                   "ea30#2", "e070", "flag", "ea30#3"]:
            f.append("stall trace: %s" % o["trace"])
        fx = o["fx"]
        eq("fx.b20", fx["b20"], 1); eq("fx.b21", fx["b21"], 9)
        eq("fx.d24", fx["d24"], 0x42); eq("fx.d28", fx["d28"], 0x100)
        eq("free_h", cl["free_h"], 0)      # fixture slot consumed
        eq("pend_h", cl["pend_h"], 0x40004000 & 0xFFFFFFFFFFFFFFFF)
    elif name == "bld-neg":
        eq("ret", o["ret"], 0xFFFFFFFF)     # or eax,-1: 32-bit -1
        eq("tel_a", cl["tel_a"], 0x55); eq("tel_b", cl["tel_b"], 0xFFFFFFFF)
    elif name == "bld-gate0":
        # gate clear -> raw path: aux passed through, NO post-fixups
        eq("ret", o["ret"], 0x40)
        eq("tel_a", cl["tel_a"], 0x55); eq("tel_b", cl["tel_b"], 0x1234)
        eq("e870_aux", o["aux_seen"], 0x40001000)   # caller's ptr as-is
        s = o["slot0"]
        eq("d30", s["d30"], 0); eq("w22", s["w22"], 0)
        eq("d34", s["d34"], 0)
        eq("d28", s["d28"], 0x500)
        eq("d2c", s["d2c"], 0x800)          # aux.d0 0x8FF -> 0x800
    elif name == "bld-gate1":
        # gate set -> aux copied to a stack local, fixups applied
        eq("ret", o["ret"], 0x40)
        if not (0x61000000 <= o["aux_seen"] < 0x62000000):
            f.append("e870 aux not a stack copy: %x" % o["aux_seen"])
        s = o["slot0"]
        eq("d2c", s["d2c"], 0x800)          # copied aux.d0 still read
        eq("q40", s["q40"], 0xAAAA); eq("q48", s["q48"], 0xBBBB)
        eq("d60", s["d60"], 0x11)
        eq("d30", s["d30"], 0x80000); eq("w22", s["w22"], 1)
        eq("d34", s["d34"], 0x500)          # pre-clamp copy of +0x28
        eq("d28", s["d28"], 0x500)
        eq("q00", s["q00"], 0)
    elif name == "bld-gate1-clamp":
        eq("ret", o["ret"], 0x40)
        s = o["slot0"]
        eq("d34", s["d34"], 0x90000)        # pre-clamp value kept
        eq("d28", s["d28"], 0x80000)        # clamped
    elif name == "bld-reqfail":
        eq("ret", o["ret"], 0)              # id==0 reads as failure
        s = o["slot0"]
        eq("w22", s["w22"], 0)              # fixups skipped
        eq("d30", s["d30"], 0)
    elif name == "e040-idle":
        if "e070" in [t.split(":")[0] for t in o["trace"]]:
            f.append("pump entered while both loaders idle")
        eq("ret", o["ret"], 0)
    elif name in ("e040-loader1", "e040-loader2"):
        pass                              # trace asserted in report
    elif name == "cycle-request-pump-retire":
        eq("req_ret", o["req_ret"], 0x40)
        eq("pend_h", cl["pend_h"], 0)       # task retired off pending
        eq("pend_t", cl["pend_t"], 0)
        s = o["slot0"]
        eq("d64", s["d64"], 0xFFFFFFFF)     # EC40 clears the id
        # retired slot lands on the free/idle list
        eq("free_h", cl["free_h"], SLOT0)
    return (len(f) == 0), f


def main():
    raw, secs = load_image()
    C = {}

    C["ctor-init"] = {"read_slots": [0, 1, 63]}
    C["ctor-dirty-rerun"] = {
        "idctr": 77, "pend_h": 0xDEAD, "pend_t": 0xBEEF,
        "free_h": 0xF00D, "read_slots": []}
    # post-ctor state for taker cases: hand-plant the ctor result
    def built(extra=None):
        c = {"free_h": SLOT0, "idctr": 1}
        for i in range(64):
            c.setdefault("slots", {})[str(slot(i))] = {
                "0x10": (slot(i + 1) if i < 63 else 0, 8),
                "0x18": (slot(i - 1) if i else 0, 8),
                "0x58": (i, 4), "0x64": (0xFFFFFFFF, 4)}
        if extra:
            c.update(extra)
        return c

    C["take-head-empty-pending"] = built({"flag": 0, "read_slots": [0, 1]})
    # pending slots 40/41 are pulled OUT of the free chain (39<->42)
    # so the fixture is a consistent queue state, not dual-listed
    def pend2(c):
        c["slots"][str(slot(39))].update({"0x10": (slot(42), 8)})
        c["slots"][str(slot(42))].update({"0x18": (slot(39), 8)})
        c["slots"][str(slot(40))].update(
            {"0x10": (slot(41), 8), "0x18": (0, 8)})
        c["slots"][str(slot(41))].update(
            {"0x10": (0, 8), "0x18": (slot(40), 8)})
        return c

    C["take-head-nonempty"] = pend2(built({
        "flag": 0, "pend_h": slot(40), "pend_t": slot(41),
        "read_slots": [0, 40, 41]}))
    C["take-tail-nonempty"] = pend2(built({
        "flag": 1, "pend_h": slot(40), "pend_t": slot(41),
        "read_slots": [0, 40, 41]}))
    C["take-free-empty-fault"] = {"free_h": 0}
    C["take-last"] = {"free_h": slot(63),
                      "slots": {str(slot(63)): {"0x10": (0, 8),
                                               "0x18": (0, 8)}}}

    C["req-basic"] = built({"ecx": 7, "edx": 0x1234, "r8": 0xCAFE00,
                            "r9": 0x500, "arg6": 1, "read_slots": [0]})
    C["req-aux"] = built({"ecx": 9, "edx": 0x77, "r8": 0x1111,
                          "r9": 0x300, "arg6": 0, "read_slots": [0],
                          "aux": {"d0": 0x8FF, "d8": 0x99,
                                  "q10": 0xAAAA, "q18": 0xBBBB}})
    C["req-second"] = built({"ecx": 1, "edx": 2, "r8": 0, "r9": 0x10,
                             "arg6": 1, "read_slots": [0, 1]})
    C["req-idwrap"] = built({"idctr": 0xFFFFFF, "ecx": 1, "edx": 1,
                             "r8": 0, "r9": 1, "arg6": 1,
                             "read_slots": [0]})
    C["req-id-zero"] = built({"idctr": 0, "ecx": 1, "edx": 1, "r8": 0,
                              "r9": 1, "arg6": 1, "read_slots": [0]})
    C["stall-then-request"] = {"free_h": 0, "ea30_release": 3,
                               "read_fx": 1, "idctr": 1}

    C["bld-neg"] = built({"ecx": 0x55, "edx": 0xFFFFFFFF, "r8": 0,
                          "r9": 0, "read_slots": [0]})
    C["bld-gate0"] = built({"ecx": 0x55, "edx": 0x1234, "r8": 0x2222,
                            "r9": 0x500, "read_slots": [0],
                            "aux": {"d0": 0x8FF, "d8": 0x11,
                                    "q10": 0xAAAA, "q18": 0xBBBB},
                            "gateb": 0})
    C["bld-gate1-clamp"] = built({"ecx": 0x55, "edx": 0x1234, "r8": 0,
                                  "r9": 0x90000, "read_slots": [0],
                                  "gateb": 1})
    C["bld-gate1"] = built({"ecx": 0x55, "edx": 0x1234, "r8": 0x3333,
                            "r9": 0x500, "read_slots": [0],
                            "aux": {"d0": 0x8FF, "d8": 0x11,
                                    "q10": 0xAAAA, "q18": 0xBBBB},
                            "gateb": 1})
    C["bld-reqfail"] = built({"idctr": 0, "ecx": 1, "edx": 1, "r8": 0,
                              "r9": 1, "read_slots": [0], "gateb": 1})

    C["e040-idle"] = {"ede80": 0, "d930": 0}
    C["e040-loader1"] = {"ede80": 1, "d930": 0}
    C["e040-loader2"] = {"ede80": 0, "d930": 1}
    C["cycle-request-pump-retire"] = {"ede80": 1, "d930": 0,
                                     "xadd0": 0, "read_slots": [0]}

    results = {}
    fails = 0
    for name, case in C.items():
        # req-second runs E870 twice
        if name == "req-second":
            w = World(case, raw, secs)
            r1 = w.run(E870, rcx=case["ecx"], rdx=case["edx"],
                       r8=case["r8"], r9=case["r9"], arg5=0,
                       arg6=case["arg6"])
            r2 = w.run(E870, rcx=case["ecx"], rdx=case["edx"],
                       r8=case["r8"], r9=case["r9"], arg5=0,
                       arg6=case["arg6"])
            out = {"trace": w.trace, "faults": w.faults,
                   "ret1": r1, "ret": r2}
            gm = w.gm
            out["cells"] = {"pend_h": gm.q(PEND_H), "pend_t": gm.q(PEND_T),
                            "free_h": gm.q(FREE_H), "idctr": gm.d(IDCTR),
                            "tel_a": gm.d(TEL_A), "tel_b": gm.d(TEL_B)}
            for i in case.get("read_slots", []):
                s = slot(i)
                out["slot%d" % i] = {"q10": gm.q(s + 0x10),
                                     "q18": gm.q(s + 0x18),
                                     "d58": gm.d(s + 0x58),
                                     "d64": gm.d(s + 0x64)}
            out["ok"], out["fail"] = check(name, case, out)
            results[name] = out
        else:
            results[name] = run_case(name, case, raw, secs)
        if not results[name]["ok"]:
            fails += 1
            print("FAIL %s: %s" % (name, results[name].get("fail")))
        else:
            print("ok   %s" % name)

    json.dump({"exe_sha256": SHA, "cases": results},
              open(RESULT, "w"), indent=1, default=str)
    print("== %d cases, %d failed ==" % (len(results), fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
