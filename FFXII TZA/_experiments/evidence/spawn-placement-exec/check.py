# spawn-placement runtime validation — CONTRACT-spawn-placement.md
# section 13 carried UNLINKED / nothing-executed. This harness runs
# Spawn_TrySelectCandidatePosition (00234AF0), the return-window pair
# (00235330/00235340), the fetch wrapper (003209C0 -> 003DFD00) and the
# shared four-slot probe (00234DA0) on shipped bytes under Unicorn.
#
#   signature   00234AF0(ecx=candidateIndex, rdx=outPos(f32 x3),
#                        xmm2=minR, xmm3=maxR,
#                        [rsp+0x28]=scoreOut-or-0 -> probe r9/rbp,
#                        [rsp+0x30]=allSlots flag -> probe r12d)
#
#   planted cells (all runtime BSS / descriptor state, disclosed;
#   every rip-relative target resolved with capstone, not by hand):
#     d[0x2089358]   arc degrees (r15d)                e.g. 90
#     q[0x1F44830]   stack cookie — left 0, self-consistent
#     b[0x2089340]   leader-exists gate, needs bit 0x10
#     d[0x22C7FE0]   party-leader id (003590D0)        0x100000
#     q[0x2B59D48]   format-class-0 record-set ptr     (003DFD00)
#     0x2098E10      id-descriptor block (00263FF0 idx 0)
#     q[0x2EBF190]   member-index table (0031B810, +0x5A5A bytes)
#     q[0x208E688]   unit array base (002367A0, stride 0xF50)
#     d[0x208E6A0]   unit array count
#     q[0x2ADD100]   spawn-flag table (00377C20, stride 3, bit15)
#     d[0x21754C4]   flag-table index (003148F0 ignores rcx!)
#     d[0x208936C]   g_nSpawnKeepReturnWindow (00235330/40)
#     d[0x22C256C]   shared LCG state (00328370, 3 ANSI-C rounds/draw)
#
#   leader chain:  003590D0 -> d[0x22C7FE0] id; 003588B0 decodes
#     id = (gen<<20)|(tblIdx<<16)|slot -> desc 0x2098E10+tblIdx*0x288
#     -> q[desc+8] array -> q[arr+8+slot*8] = obj -> w[obj+0x16]==gen
#     -> 00263E30: q[obj+0x30]=rec, b[rec]&8 -> q[rec+0x10]=sub
#   sub convention (00265020/00265200): b[sub+3]>>5 in {1,2};
#     class1 -> q[sub+0xb8]=pos blk, pos f{x,y,z} + f[+0x38]=heading
#
#   scripted boundaries: 0x861F02 is a tail-jmp through cell 0x8C2BD0
#   (not a named import — encoded CRT pointer, file holds 0x1CCED38).
#   Its semantics per CONTRACT I8 are atan2f(dx,dz); emulated and
#   returned to the caller's return address. Everything else —
#   validator 00322C50, both LCG draws, sine table 01F004E0, region
#   transform 00325EA0, probe 00234DA0, cookie checks — executes as
#   shipped bytes.

import ctypes
import hashlib
import json
import math
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

ARC_DEG = 0x2089358            # d, mov r15d at 00234B27
LEADER_GATE = 0x2089340        # b&0x10, test at 003272A9
LEADER_ID_CELL = 0x22C7FE0     # d, 003590D0
FMT0_TAB = 0x2B59D48           # q[cls*8] table base, 003DFD03
ID_DESC0 = 0x2098E10           # lea at 00263FF3, stride 0x288
MEMBER_TAB = 0x2EBF190         # q, 0031B83A (+0x5A5A bytes)
UNIT_BASE = 0x208E688          # q, 002367AA (stride 0xF50)
UNIT_COUNT = 0x208E6A0         # d, 002367C5
FLAG_TAB = 0x2ADD100           # q, 00377C29 (stride 3, bit15)
FLAG_IDX = 0x21754C4           # d at ctx0 0x2164280+0x200+0x1044
VALID2_DESC = 0x2EBF130        # cls-2 validator descriptor cell (EXP-143)
WINDOW_CELL = 0x208936C        # d, 00235330 getter / 00235340 setter
LCG_STATE = 0x22C256C
COOKIE = 0x1F44830             # all three bodies share this cell

LCG_PLANT = 0x11111111
LEADER_ID = (1 << 20)          # gen=1, tblIdx=0, slot=0

RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")


def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def f32(v): return struct.pack("<f", v)
def xf(v):  # float -> xmm reg int128
    return int.from_bytes(struct.pack("<f", v) + b"\0" * 12, "little")
def fx(i):  # xmm reg int128 -> float
    return struct.unpack("<f", i.to_bytes(16, "little")[:4])[0]


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
    def f(self, addr): return struct.unpack("<f", self.r(addr, 4))[0]


CALLS = (0x3DFD00, 0x3209C0, 0x3272A0, 0x265020, 0x265200, 0x31AC90,
         0x31A930, 0x234DA0, 0x328370, 0x316DA0, 0x319390, 0x2374E0,
         0x31B810, 0x322C50, 0x2367A0, 0x313F60, 0x377C20, 0x3148F0,
         0x3273B0, 0x31E620, 0x3A1960, 0x263FF0, 0x3588B0, 0x263E30,
         0x2EF640, 0x2EF2B0, 0x325EA0, 0x235330, 0x235340, 0x808C40)


class World:
    def __init__(self, case, raw, secs, imports):
        self.case, self.imports = case, imports
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x400000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        self.hbuf = HEAP + 0x1000
        self.calls = []
        self.lcg_accesses = []
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

    def on_read(self, uc, access, addr, size, value, _):
        if LCG_STATE <= addr < LCG_STATE + 4:
            self.lcg_accesses.append(("r", hex(uc.reg_read(
                UC_X86_REG_RIP))))

    def on_write(self, uc, access, addr, size, value, _):
        if LCG_STATE <= addr < LCG_STATE + 4:
            self.lcg_accesses.append(("w", hex(uc.reg_read(
                UC_X86_REG_RIP)), hex(value)))

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
        self.calls.append(("iat:" + name, ))
        if op == b"\xff\x25":
            self._ret(uc)
        else:
            uc.reg_write(UC_X86_REG_RIP, addr + off + 6)
        return True

    def on_code(self, uc, addr, size, _):
        # 0x861F02: encoded-CRT tail thunk — atan2f(dx, dz) per I8.
        if addr == 0x861F02:
            y = fx(uc.reg_read(UC_X86_REG_XMM0))
            x = fx(uc.reg_read(UC_X86_REG_XMM1))
            self.calls.append(("stub:atan2f", y, x))
            uc.reg_write(UC_X86_REG_XMM0,
                         xf(math.atan2(y, x)))
            self._ret(uc)
            return
        b0 = self.gm.r(addr, 3)
        if b0[:2] in (b"\xff\x25", b"\xff\x15") or \
                b0[1:3] in (b"\xff\x25", b"\xff\x15"):
            if self._iat_stub(uc, addr):
                return
        if addr in CALLS:
            self.calls.append(("enter%x" % addr,
                               hex(uc.reg_read(UC_X86_REG_RCX))))
        if addr == self.case.get("stopat", -1):
            self.faults.append(("stopat", hex(addr)))
            uc.emu_stop()

    def run(self, entry, regs=None, xmm=None, stack_args=()):
        # sentinel-fill the frame region — an uninitialised local must
        # show 0xCD provenance (I7: the polar construction never writes
        # its out+4, yet the caller still copies it into out.y).
        self.gm.w(STACK + 0x70000, b"\xcd" * 0x10000)
        self.uc.reg_write(UC_X86_REG_RSP, STACK + 0x80000)
        self.uc.reg_write(UC_X86_REG_RIP, entry)
        self.gm.w(STACK + 0x80000, qw(RETQ))
        for i, v in enumerate(stack_args):
            self.gm.w(STACK + 0x80000 + 0x28 + i * 8, qw(v))
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
        return self.uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


# --- fixture builders -------------------------------------------------

def plant_leader(w, pos=(0.0, 0.0, 0.0), heading=0.0):
    """The whole 003272A0 chain -> a live leader at `pos`."""
    w.gm.w(LEADER_GATE, bytes([w.gm.r(LEADER_GATE, 1)[0] | 0x10]))
    w.gm.w(LEADER_ID_CELL, dw(LEADER_ID))
    arr = w.alloc(0x20)
    w.gm.w(arr, dw(1))                 # d[arr] count > slot 0
    obj = w.alloc(0x100)
    w.gm.w(arr + 8, qw(obj))
    w.gm.w(obj + 0x16, b"\x01\x00")    # w[obj+0x16] == gen 1
    # desc0 in image .data
    w.gm.w(ID_DESC0, qw(1))
    w.gm.w(ID_DESC0 + 8, qw(arr))
    w.gm.w(ID_DESC0 + 0x10,
           bytes([w.gm.r(ID_DESC0 + 0x10, 1)[0] | 1]))
    w.gm.w(ID_DESC0 + 0x20, dw(1))
    rec = w.alloc(0x100)
    w.gm.w(obj + 0x30, qw(rec))
    w.gm.w(rec, bytes([w.gm.r(rec, 1)[0] | 8]))
    sub = w.alloc(0x200)
    w.gm.w(rec + 0x10, qw(sub))
    w.gm.w(sub + 3, b"\x20")           # class 1
    posblk = w.alloc(0x100)
    w.gm.w(sub + 0xB8, qw(posblk))
    w.gm.w(posblk + 0, f32(pos[0]))
    w.gm.w(posblk + 4, f32(pos[1]))
    w.gm.w(posblk + 8, f32(pos[2]))
    w.gm.w(posblk + 0x38, f32(heading))
    return obj


def plant_units(w, specs):
    """specs: list of dicts {byte, uid, pos} — unit fixtures for the
    00234DA0 probe. byte = member-table index byte, uid = d[unit+8]."""
    mtab = w.alloc(0x8000)
    units = w.alloc(0xF50 * 8)
    w.gm.w(MEMBER_TAB, qw(mtab))
    w.gm.w(UNIT_BASE, qw(units))
    w.gm.w(UNIT_COUNT, dw(8))
    # cls-2 validator inside 002367A0 is descriptor-backed (BSS) —
    # plant a 64-entry descriptor so member bytes 0..63 validate.
    vdesc = w.alloc(0x20)
    w.gm.w(VALID2_DESC, qw(vdesc))
    w.gm.w(vdesc + 4, dw(64))
    for i, s in enumerate(specs):
        w.gm.w(mtab + 0x5A5A + i * 2, bytes([s["byte"]]))
        u = units + i * 0xF50
        sub = w.alloc(0x200)
        w.gm.w(u + 0x698, qw(sub))
        w.gm.w(sub + 4, struct.pack("<H", s["byte"]))
        # gate flags zero -> 00313F60 not consulted
        w.gm.w(u + 8, dw(s.get("uid", 0)))
        sp = w.alloc(0x200)
        w.gm.w(u + 0x10, qw(sp))
        w.gm.w(sp + 3, b"\x20")
        pb = w.alloc(0x100)
        w.gm.w(sp + 0xB8, qw(pb))
        x, y, z = s.get("pos", (0.0, 0.0, 0.0))
        w.gm.w(pb + 0, f32(x)); w.gm.w(pb + 4, f32(y))
        w.gm.w(pb + 8, f32(z))


def plant_fmt0(w, records, version=0x33):
    """records: list of dicts {mode,hx,hz,x,y,z,ang} for v>=0x33
    (0x30-byte records at tbl+0x10) or {x,y,z,e} for old format
    (0x10-byte records at tbl+0x10+(idx+1)*0x10)."""
    n = len(records)
    if version >= 0x33:
        tbl = w.alloc(0x10 + n * 0x30)
        for i, r in enumerate(records):
            b = tbl + 0x10 + i * 0x30
            w.gm.w(b + 0, bytes([r.get("mode", 0)]))
            w.gm.w(b + 4, f32(r.get("hx", 0.0)))
            w.gm.w(b + 8, f32(r.get("hz", 0.0)))
            w.gm.w(b + 0x10, f32(r.get("x", 0.0)))
            w.gm.w(b + 0x14, f32(r.get("y", 0.0)))
            w.gm.w(b + 0x18, f32(r.get("z", 0.0)))
            w.gm.w(b + 0x1C, f32(r.get("ang", 0.0)))
    else:
        tbl = w.alloc(0x10 + n * 0x10)
        for i, r in enumerate(records):
            # code reads r9 + (idx+1)*0x10 = tbl + 0x10 + idx*0x10
            b = tbl + 0x10 + i * 0x10
            w.gm.w(b + 0, f32(r.get("x", 0.0)))
            w.gm.w(b + 4, f32(r.get("y", 0.0)))
            w.gm.w(b + 8, f32(r.get("z", 0.0)))
            w.gm.w(b + 0xC, f32(r.get("e", 0.0)))
    w.gm.w(tbl + 7, bytes([version]))
    w.gm.w(tbl + 0xC, dw(n))
    w.gm.w(FMT0_TAB, qw(tbl))
    return tbl


def lcg3(s):
    for _ in range(3):
        s = (s * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    return s


def run_case(name, case, raw, secs, imports):
    w = World(case, raw, secs, imports)
    w.gm.w(LCG_STATE, dw(case.get("lcg", LCG_PLANT)))
    out = w.alloc(0x40, fill=0xAA)
    score = w.alloc(0x10, fill=0xAA)
    recbuf = w.alloc(0x40, fill=0xAA)

    entry = case["entry"]

    if name.startswith("win-"):
        w.gm.w(WINDOW_CELL, dw(0x55555555))
        ret = w.run(0x235340,
                    regs={UC_X86_REG_ECX: case["set"] & 0xFFFFFFFF})
        cell = w.gm.dw(WINDOW_CELL)
        ret2 = w.run(0x235330)
        return {"ret_set": ret, "cell": cell, "ret_get": ret2,
                "calls": w.calls, "faults": w.faults,
                "lcg": hex(w.gm.dw(LCG_STATE))}

    if name == "fetch-direct":
        plant_fmt0(w, [{"x": 1.0, "y": 2.0, "z": 3.0}])
        ret_ok = w.run(0x3209C0,
                       regs={UC_X86_REG_ECX: 0,
                             UC_X86_REG_RDX: recbuf})
        rec = [w.gm.f(recbuf + o) for o in (0x10, 0x14, 0x18)]
        ret_bad = w.run(0x3209C0,
                        regs={UC_X86_REG_ECX: 5,
                              UC_X86_REG_RDX: recbuf})
        return {"ret_ok": ret_ok, "rec": rec, "ret_bad": ret_bad,
                "calls": w.calls, "faults": w.faults}

    # --- 00234AF0 cases ---------------------------------------------
    w.gm.w(ARC_DEG, dw(case.get("arc", 90)))
    if case.get("fmt0") == "null":
        pass                                  # cell stays shipped 0
    elif case.get("fmt0") == "old":
        plant_fmt0(w, case["records"], version=0x20)
    else:
        plant_fmt0(w, case["records"])
    if not case.get("noleader"):
        plant_leader(w, pos=case.get("leader_pos", (0.0, 0.0, 0.0)),
                     heading=case.get("yaw", 0.0))
    plant_units(w, case.get("units", []))
    if case.get("flagtab"):
        ft = w.alloc(0x40)
        w.gm.w(FLAG_TAB, qw(ft))
        w.gm.w(ft + 4, dw(1))
        w.gm.w(ft + 8 + 1, b"\x80")           # entry0 word bit15
        w.gm.w(FLAG_IDX, dw(0))

    lcg0 = w.gm.dw(LCG_STATE)
    ret = w.run(entry,
                regs={UC_X86_REG_ECX: case.get("idx", 0),
                      UC_X86_REG_RDX: out},
                xmm={UC_X86_REG_XMM2: xf(case.get("minr", 5.0)),
                     UC_X86_REG_XMM3: xf(case.get("maxr", 15.0))},
                stack_args=(score if case.get("scoreout") else 0,
                            case.get("allslots", 0)))
    lcg1 = w.gm.dw(LCG_STATE)

    return {
        "ret": ret,
        "out": [w.gm.f(out + o) for o in (0, 4, 8)],
        "out_raw": w.gm.r(out, 12).hex(),
        "score": (None if w.gm.r(score, 4) == b"\xaa" * 4
                  else w.gm.f(score)),
        "lcg": [hex(lcg0), hex(lcg1)],
        "lcg_calls": sum(1 for c in w.calls
                         if c[0] == "enter328370"),
        "lcg_accesses": w.lcg_accesses,
        "calls": [c[0] for c in w.calls],
        "faults": w.faults,
    }


# leader at origin, heading 0 (forward = +Z). candidate (0,0,8):
# heading-to = atan2(0,8) = 0 -> inside 90-deg arc; dist^2 = 64 in
# [25,225] -> probe pass when the leader slot is the only live unit.
LEAD = [{"byte": 0, "uid": LEADER_ID, "pos": (0.0, 0.0, 0.0)}]

CASES = {
    "win-neg":      {"entry": 0x235340, "set": -5},
    "win-zero":     {"entry": 0x235340, "set": 0},
    "win-pos":      {"entry": 0x235340, "set": 7},
    "empty-band":   {"entry": 0x234AF0,
                     "records": [{"mode": 0, "x": 0, "y": 0, "z": 8}],
                     "minr": 5.0, "maxr": 5.0, "units": LEAD},
    "fetch-null":   {"entry": 0x234AF0, "fmt0": "null", "units": LEAD},
    "fetch-oob":    {"entry": 0x234AF0, "records": [], "units": LEAD},
    "fetch-direct": {"entry": 0x3209C0},
    "null-leader":  {"entry": 0x234AF0, "noleader": True,
                     "records": [{"mode": 0, "x": 0, "y": 0, "z": 8}],
                     "units": LEAD},
    "point-hit":    {"entry": 0x234AF0,
                     "records": [{"mode": 0, "x": 0, "y": 0, "z": 8}],
                     "units": LEAD, "scoreout": 1},
    "point-arc-miss": {"entry": 0x234AF0,
                       "records": [{"mode": 0, "x": 8, "y": 0,
                                    "z": -8}],
                       "units": LEAD},
    "point-band-far": {"entry": 0x234AF0,
                       "records": [{"mode": 0, "x": 0, "y": 0,
                                    "z": 20}],
                       "units": LEAD},
    "point-band-near": {"entry": 0x234AF0,
                        "records": [{"mode": 0, "x": 0, "y": 0,
                                     "z": 2}],
                        "units": LEAD},
    "point-coincident": {"entry": 0x234AF0,
                         "records": [{"mode": 0, "x": 0, "y": 0,
                                      "z": 0}],
                         "units": LEAD},
    "point-no-slots": {"entry": 0x234AF0,
                       "records": [{"mode": 0, "x": 0, "y": 0,
                                    "z": 8}],
                       "units": []},
    "probe-allslots-fail": {"entry": 0x234AF0,
                            "records": [{"mode": 0, "x": 0, "y": 0,
                                         "z": 8}],
                            "allslots": 1,
                            "units": LEAD + [
                                {"byte": 1, "uid": 0x222222,
                                 "pos": (900.0, 0.0, 900.0)}]},
    "area-box-hit": {"entry": 0x234AF0,
                     "records": [{"mode": 1, "hx": 1e6, "hz": 1e6,
                                  "x": 0, "y": 7.5, "z": 0}],
                     "units": LEAD},
    "area-box-miss": {"entry": 0x234AF0,
                      "records": [{"mode": 1, "hx": 1.0, "hz": 1.0,
                                   "x": 1e6, "y": 0, "z": 1e6}],
                      "units": LEAD},
    "area-ellipse-hit": {"entry": 0x234AF0,
                         "records": [{"mode": 2, "hx": 1e6,
                                      "hz": 1e6,
                                      "x": 0, "y": 0, "z": 0}],
                         "units": LEAD},
    "area-shape3": {"entry": 0x234AF0,
                    "records": [{"mode": 3, "hx": 1e6, "hz": 1e6,
                                 "x": 0, "y": 0, "z": 0}],
                    "units": LEAD},
    "oldfmt-point": {"entry": 0x234AF0, "fmt0": "old",
                     "records": [{"x": 0, "y": 0, "z": 8}],
                     "units": LEAD},
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
        expect(name, not r["faults"], "faults %s" % (r["faults"],))

    # I1 — return window
    expect("win-neg", results["win-neg"]["cell"] == 300,
           "negative -> %r, want 300" % (results["win-neg"]["cell"],))
    expect("win-neg", results["win-neg"]["ret_get"] == 300,
           "getter -> %r" % (results["win-neg"]["ret_get"],))
    expect("win-zero", results["win-zero"]["cell"] == 0,
           "zero -> %r (cmovs is sign-only)" % (results["win-zero"],))
    expect("win-pos", results["win-pos"]["cell"] == 7,
           "positive -> %r" % (results["win-pos"]["cell"],))

    # I5 — empty band refuses before fetch
    r = results["empty-band"]
    expect("empty-band", r["ret"] == 0, "ret %r" % (r["ret"],))
    expect("empty-band", "enter3209c0" not in r["calls"] and
           "enter3dfd00" not in r["calls"],
           "fetch ran on empty band: %s" % (r["calls"],))

    # I2 — fetch: 0 = success, negative = failure
    r = results["fetch-direct"]
    expect("fetch-direct", r["ret_ok"] == 0,
           "in-range idx -> %r, want 0" % (r["ret_ok"],))
    expect("fetch-direct", r["rec"] == [1.0, 2.0, 3.0],
           "record -> %r" % (r["rec"],))
    expect("fetch-direct", r["ret_bad"] == 0xFFFFFFFF,
           "oob idx -> %#x, want -1" % (r["ret_bad"],))
    expect("fetch-null", results["fetch-null"]["ret"] == 0,
           "null table -> %r" % (results["fetch-null"]["ret"],))
    expect("fetch-oob", results["fetch-oob"]["ret"] == 0,
           "oob -> %r" % (results["fetch-oob"]["ret"],))
    for nm in ("fetch-null", "fetch-oob"):
        expect(nm, "enter3dfd00" in results[nm]["calls"],
               "fetch body never reached: %s" % (results[nm]["calls"],))

    # I4 — null leader returns 0 AFTER the authored pos is copied out
    r = results["null-leader"]
    expect("null-leader", r["ret"] == 0, "ret %r" % (r["ret"],))
    expect("null-leader", r["out"] == [0.0, 0.0, 8.0],
           "out not authored pos: %r" % (r["out"],))
    expect("null-leader", "enter3272a0" in r["calls"],
           "leader getter never ran")

    # point mode — arc then band
    r = results["point-hit"]
    expect("point-hit", r["ret"] == 1, "ret %r" % (r["ret"],))
    expect("point-hit", r["out"] == [0.0, 0.0, 8.0],
           "out %r" % (r["out"],))
    expect("point-hit", r["score"] == 64.0,
           "score-out %r want 64.0 (dist^2)" % (r["score"],))
    expect("point-hit", "enter31ac90" in r["calls"] and
           "enter234da0" in r["calls"], "calls %s" % (r["calls"],))
    expect("point-hit", r["lcg_calls"] == 0,
           "point mode drew RNG %d times" % (r["lcg_calls"],))

    r = results["point-arc-miss"]
    expect("point-arc-miss", r["ret"] == 0, "ret %r" % (r["ret"],))
    expect("point-arc-miss", "enter234da0" not in r["calls"],
           "probe ran after arc miss: %s" % (r["calls"],))

    for nm in ("point-band-far", "point-band-near",
               "point-coincident"):
        r = results[nm]
        expect(nm, r["ret"] == 0, "ret %r" % (r["ret"],))
        expect(nm, "enter234da0" in r["calls"],
               "probe not reached: %s" % (r["calls"],))

    r = results["point-no-slots"]
    expect("point-no-slots", r["ret"] == 0,
           "no live slots -> ret %r (probe ORs, 0 when all dead)"
           % (r["ret"],))

    r = results["probe-allslots-fail"]
    expect("probe-allslots-fail", r["ret"] == 0,
           "arg6=1: out-of-band live slot must early-fail even with "
           "leader in-band: ret %r" % (r["ret"],))

    # area mode — two draws, region is the only filter
    lcg_twice = lcg3(lcg3(LCG_PLANT))
    for nm in ("area-box-hit", "area-box-miss", "area-ellipse-hit",
               "area-shape3"):
        r = results[nm]
        expect(nm, r["lcg_calls"] == 2,
               "draws %d, want exactly 2" % (r["lcg_calls"],))
        expect(nm, int(r["lcg"][1], 16) == lcg_twice,
               "LCG end %s != two-draw state %s"
               % (r["lcg"][1], hex(lcg_twice)))
    r = results["area-box-hit"]
    expect("area-box-hit", r["ret"] == 1, "ret %r" % (r["ret"],))
    expect("area-box-hit", "enter319390" in r["calls"] and
           "enter2374e0" in r["calls"], "calls %s" % (r["calls"],))
    # I7: authored Y was 7.5 but out.y must show the stack sentinel —
    # 00319390 writes out+0/+8 only; the caller copies the untouched
    # +4 slot into the result.
    expect("area-box-hit", r["out_raw"][8:16] == "cdcdcdcd",
           "out.y %r — expected uninit-stack sentinel 0xCDCDCDCD "
           "(authored y was 7.5)" % (r["out_raw"],))
    expect("area-box-miss", results["area-box-miss"]["ret"] == 0,
           "ret %r" % (results["area-box-miss"]["ret"],))
    expect("area-ellipse-hit",
           results["area-ellipse-hit"]["ret"] == 1,
           "ret %r" % (results["area-ellipse-hit"]["ret"],))
    expect("area-shape3", results["area-shape3"]["ret"] == 0,
           "shape 3 -> ret %r (region test rejects)" % (
               results["area-shape3"]["ret"],))

    # old record format forces point mode (fetch writes rec[0]=0)
    r = results["oldfmt-point"]
    expect("oldfmt-point", r["ret"] == 1, "ret %r" % (r["ret"],))
    expect("oldfmt-point", "enter328370" not in r["calls"],
           "old format drew RNG: %s" % (r["calls"],))

    out = {"cases": len(results), "results": results,
           "failures": fails}
    with open(RESULT, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"cases": len(results), "failures": fails},
                     indent=1))


if __name__ == "__main__":
    check()
