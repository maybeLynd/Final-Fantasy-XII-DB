# EXP-114 shadow-lod-compute-exec
#
# Executes the SHIPPED bytes of the computed shadow-LOD family named as
# "003B5980's bone-height fade" (CONTRACT-authored-command-ramp-channels
# section 13; scripted boundary in EXP-113). The span 003B5980..003B6020
# holds SIX sibling functions, all generation-checking the same 0xE0
# shadow-slot pool at q[0x2B40528] (slot = u8(ecx)*0xE0 + base;
# d[slot+0x10] must equal ecx):
#
#   003B5980  LODC   computed LOD (344 B + shared epilogue).
#                    bad gen / w04==-1 / d[rec+0x284]==0 / RES2 null /
#                    GATE null -> ret f[0x1CEBBA8] (shipped default).
#                    rdi = 00421FF0(rec, zx(w[slot+0x3C]))  (bone obj)
#                    rax = 003E6F70(rec)                   (gate obj)
#                    scratch block:
#                      vec[0x22D91B0] = const vec4 (0x2AEDF20, BSS-planted)
#                      vec[0x22D91C0] = [rdi+0x30..0x3F] - const vec4
#                      vec[0x22D91D0] = [g.x, g.y, STK, g.f+0x2C]
#                        (element 2 = UNINITIALISED stack — planted)
#                    LEAF resets vec4[0x1EF93F0] = shipped const 0x8C5FD0;
#                      xmm6 = el3, xmm3 = el0.
#                    sum = xmm6*(dy^2+dz^2+dw^2) (element0 NOT summed);
#                    |sum| via cvtps2pd/andps[0x1CEBD80]/cvtpd2ps;
#                    dist = sqrtf(sum) -> f[0x22D9198];
#                    partial xmm6*(dy2+dw2) -> f[0x22D91AC];
#                    xmm1 = max(xmm3 + dist, g.x);
#                    xmm2 = (min(g.y, xmm1) - g.x) * g.w;
#                    xmm4 = clamp(xmm6+xmm3 - xmm2, xmm3, xmm6)
#                         -> f[0x22D91F0], vec[0x22D91C0][0];
#                    vec[0x22D8FB0] = vec[0x22D91C0]; ret xmm4.
#   003B5C00  ACC    requires b[+0x40]&1. Five countdown channels:
#                    b[0]  -> f50 += f60, f54 += f64
#                    b[2]  -> f58 += f68, f5C += f6C
#                    b[1]  -> f70 += f74
#                    b[3]  -> f78 += f7C
#                    b[43] -> f98 += f9C      (each decs its count)
#   003B5CE0  CPY    d[+0x48]->d[+0x30], d[+0x4C]->d[+0x34],
#                    w[+0x38]->w[+0x3A]; f[+0x48]=xmm2, f[+0x4C]=xmm3;
#                    w[+0x38] = edx==0 ? w[+0x3C] : w[+0x3E].
#   003B5D40  INIT   copy d[+0xC0..+0xD4] -> d[+0x80..+0x94] (6 dwords);
#                    b[+0x43]=dl; d[+0x98]=0;
#                    d[0x22D914C]=1.0f; d[0x22D9148]=edx;
#                    q = 1.0 / bits2f(edx); q[0x22D8F90]=0x3F800000;
#                    f[+0x9C]=q; if dl: b43=dl-1, f[+0x98]=q.
#   003B5E20  FSYNC  r10=rdx arg struct. On old-b40 flag bits:
#                    bit1: fA0/A4 -> f50/54 and -> f80/84; b[0]=0
#                    bit2: fB0 -> f70 and -> f90;          b[3]=0
#                    bit3: fA8/AC -> f58/5C and -> f88/8C; b[2]=0
#                    bit4: dB4->d48, dB8->d4C
#                    if w[r10+0x32]!=0: copy r10+4C/50 -> slot+A0/A4;
#                      slot+B0 = f(w32 sar 6) * shipped f[0xD115B0];
#                      r10+58/5C -> +B4/B8; r10+10/14 -> +A8/AC.
#                    flag rebuild: w32 bits {0,1,3,2,4,5} -> b40 {1..6}
#                      (xor-mask merge; bit0 + bit7 preserved);
#                    d[r9]=0 clears countdown bytes b[0..3].
#   003B6000  CLRE   b[+0x40] &= 0xFE.
#
#   0036DD80  LEAF   vec4[0x1EF93F0] = vec4[0x8C5FD0] (shipped const).
#
# Real callees re-executed from EXP-108's proven layer:
#   00421FF0  res2   ebx=d[rcx+0x18]; -1 -> 0;
#                    rax=0020E600(d[rcx+0x10]) = q[0x1F83530]+ecx;
#                    rcx=q[rax+0xD98]; rax=002ED570(rcx,ebx) stub;
#                    rax==0 -> 0 else tail 00370F60(rax, edi) stub.
#   003E6F70  gate   q[rec+0x400]==0 -> 0 else tail 003E56A0 (stub).
#   0020E600  base   rax = ecx + q[0x1F83530].
#
# Scripted boundaries (disclosed):
#   003E56A0  E56    rec -> planted GATE object (arg captured)
#   002ED570  MIDS   (rcx,ebx) -> planted MID
#   00370F60  OUTR   (mid,edi) -> planted BONE object
#   00861F14  SQRTF  CRT thunk jmp [0x8C2BB8] -> api-ms-win-crt-math
#                    sqrtf; stub computes xmm0 = sqrtf(xmm0).
#
# Trace tokens: R<rcx>:<edx> res2, e<ecx> base, m<mid>:<ebx> mids-stub,
# o<mid>:<edi> outr-stub, g<rcx> gate, s<rcx> e56-stub, L leaf,
# q<xmm0bits> sqrtf-stub.

import ctypes, hashlib, json, math, os, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDI, UC_X86_REG_RDX, UC_X86_REG_RIP, UC_X86_REG_RSP, \
    UC_X86_REG_XMM0, UC_X86_REG_XMM2, UC_X86_REG_XMM3

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000
RESULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "result.json")

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

LODC   = 0x003B5980
ACC    = 0x003B5C00
CPY    = 0x003B5CE0
INIT   = 0x003B5D40
FSYNC  = 0x003B5E20
CLRE   = 0x003B6000
LEAF   = 0x0036DD80
GATE   = 0x003E6F70
RES2   = 0x00421FF0
BASE   = 0x0020E600
E56    = 0x003E56A0        # STUB
MIDS   = 0x002ED570        # STUB
OUTR   = 0x00370F60        # STUB
SQRTF  = 0x00861F14        # STUB (CRT thunk)

# BSS globals (runtime-populated — planted by fixture)
G_SLOTS  = 0x02B40528      # qword: slot table base (stride 0xE0)
G_RECS   = 0x022C6F28      # qword: actor-rec table base (stride 0x740)
G_BASE   = 0x01F83530      # qword: 0020E600 resolver base
C_VEC    = 0x02AEDF20      # vec4 const LODC subtracts (BSS — planted)
LEAF_G   = 0x01EF93F0      # vec4 the LEAF resets (BSS — planted init)
LEAF_C   = 0x008C5FD0      # shipped const vec4 the LEAF copies
DEF_F    = 0x01CEBBA8      # shipped default-return float
FS_MUL   = 0x00D115B0      # shipped float fn5 multiplies by
OBS_LO   = 0x022D8F80      # observed scratch/globals window
OBS_HI   = 0x022D9200

# heap layout
SLOTS  = HEAP + 0x000000   # 16 x 0xE0
RECS   = HEAP + 0x100000   # 0x740-stride actor records
OBJB   = HEAP + 0x300000   # 0020E600 base — object array
BONE   = HEAP + 0x500000   # OUTR stub return — bone object (+0x30 vec4)
GOBJ   = HEAP + 0x510000   # E56 stub return — gate object (+0x20/24/2C)
MID_A  = HEAP + 0x530000   # MIDS stub return
ARG5   = HEAP + 0x540000   # fn5 r10 arg struct

NSLOT = 16


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def sx16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v
def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]
def fbits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]
def bits2f(b):
    return struct.unpack("<f", struct.pack("<I", b & 0xFFFFFFFF))[0]
def fm(a, b): return f32(f32(a) * f32(b))
def fa(a, b): return f32(f32(a) + f32(b))
def fs(a, b): return f32(f32(a) - f32(b))
def fd(a, b):
    a, b = f32(a), f32(b)
    if b == 0.0:
        if a == 0.0 or a != a: return f32(float("nan"))
        return f32(math.copysign(float("inf"), a))
    r = a / b
    if r != r: return f32(float("nan"))
    if abs(r) > 3.4028235e38:
        return f32(math.copysign(float("inf"), r))
    return f32(r)


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


def img_dw(raw, secs, va):
    return struct.unpack("<I", img_rd(raw, secs, va, 4))[0]


def img_f(raw, secs, va):
    return bits2f(img_dw(raw, secs, va))


def img_rd_or_zero(raw, secs, va, n):
    try:
        return img_rd(raw, secs, va, n)
    except KeyError:
        return b"\0" * n


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


# ---------------- fixture shapes ----------------

def default_slot(i):
    """A valid, enabled slot with distinct per-field values."""
    return {
        "i10": i, "w04": i, "w38": 0, "w3a": 1, "w3c": 2, "w3e": 3,
        "b40": 0x01, "b00": 2, "b01": 3, "b02": 4, "b03": 5, "b43": 6,
        "f08": 0.125, "f0c": 0.25, "f14": 0.5, "f18": 0.75,
        "f2c": 1.0, "f30": 1.25, "f34": 1.5,
        "f44": 2.0, "f48": 2.25, "f4c": 2.5,
        "f50": 3.0, "f54": 3.25, "f58": 3.5, "f5c": 3.75,
        "f60": 4.0, "f64": 4.25, "f68": 4.5, "f6c": 4.75,
        "f70": 5.0, "f74": 5.25, "f78": 5.5, "f7c": 5.75,
        "f80": 6.0, "f84": 6.25, "f88": 6.5, "f8c": 6.75,
        "f90": 7.0, "f94": 7.25, "f98": 7.5, "f9c": 7.75,
        "fa0": 8.0, "fa4": 8.25, "fa8": 8.5, "fac": 8.75,
        "fb0": 9.0, "fb4": 9.25, "fb8": 9.5, "fbc": 9.75,
        "fc0": 10.0, "fc4": 10.25, "fc8": 10.5, "fcc": 10.75,
        "fd0": 11.0, "fd4": 11.25,
    }


def default_rec(i):
    return {"d284": 1, "q400": GOBJ, "d10": i * 0x2000, "d18": 0}


def default_arg5():
    """fn5's rdx struct: w32 bitfield + payload fields."""
    return {"w32": 0x0020, "d10": fbits(20.0), "d54": fbits(20.5),
            "d4c": fbits(21.0), "d50": fbits(21.5),
            "d58": fbits(22.0), "d5c": fbits(22.5)}


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

        # ---- globals ----
        gm.w(G_SLOTS, qw(SLOTS))
        gm.w(G_RECS, qw(RECS))
        gm.w(G_BASE, qw(OBJB))
        cvec = case.get("cvec", [1.0, 2.0, 3.0, 4.0])
        for k, fv in enumerate(cvec):
            gm.w(C_VEC + k * 4, struct.pack("<f", fv))
        leaf_init = case.get("leaf_init", [9.0, 8.0, 7.0, 6.0])
        for k, fv in enumerate(leaf_init):
            gm.w(LEAF_G + k * 4, struct.pack("<f", fv))
        gm.w(0x22D9140, struct.pack("<f", case.get("g140", 2.0)))
        gm.w(0x22D9144, dw(case.get("g144", 0x11223344)))
        gm.w(0x22D9148, struct.pack("<f", case.get("g148", 4.0)))

        # ---- slots ----
        slots = [default_slot(i) for i in range(NSLOT)]
        for i, kw in case.get("slots", {}).items():
            slots[i].update(kw)
        for i, s in enumerate(slots):
            b = SLOTS + i * 0xE0
            gm.w(b + 0x10, dw(s.get("i10", i)))
            for name, off in (("w04", 4), ("w38", 0x38), ("w3a", 0x3A),
                              ("w3c", 0x3C), ("w3e", 0x3E)):
                gm.w(b + off, hw(s.get(name, 0)))
            for name, off in (("b00", 0), ("b01", 1), ("b02", 2),
                              ("b03", 3), ("b40", 0x40), ("b43", 0x43)):
                gm.w(b + off, bytes([s.get(name, 0) & 0xFF]))
            for name, off in (("f08", 8), ("f0c", 0xC), ("f14", 0x14),
                              ("f18", 0x18), ("f2c", 0x2C),
                              ("f30", 0x30), ("f34", 0x34),
                              ("f44", 0x44), ("f48", 0x48),
                              ("f4c", 0x4C), ("f50", 0x50),
                              ("f54", 0x54), ("f58", 0x58),
                              ("f5c", 0x5C), ("f60", 0x60),
                              ("f64", 0x64), ("f68", 0x68),
                              ("f6c", 0x6C), ("f70", 0x70),
                              ("f74", 0x74), ("f78", 0x78),
                              ("f7c", 0x7C), ("f80", 0x80),
                              ("f84", 0x84), ("f88", 0x88),
                              ("f8c", 0x8C), ("f90", 0x90),
                              ("f94", 0x94), ("f98", 0x98),
                              ("f9c", 0x9C), ("fa0", 0xA0),
                              ("fa4", 0xA4), ("fa8", 0xA8),
                              ("fac", 0xAC), ("fb0", 0xB0),
                              ("fb4", 0xB4), ("fb8", 0xB8),
                              ("fbc", 0xBC), ("fc0", 0xC0),
                              ("fc4", 0xC4), ("fc8", 0xC8),
                              ("fcc", 0xCC), ("fd0", 0xD0),
                              ("fd4", 0xD4)):
                gm.w(b + off, struct.pack("<f", s.get(name, 0.0)))

        # ---- actor records ----
        recs = [default_rec(i) for i in range(NSLOT)]
        for i, kw in case.get("recs", {}).items():
            recs[i].update(kw)
        for i, r in enumerate(recs):
            b = RECS + i * 0x740
            gm.w(b + 0x284, dw(r.get("d284", 1)))
            gm.w(b + 0x400, qw(r.get("q400", GOBJ)))
            gm.w(b + 0x10, dw(r.get("d10", 0)))
            gm.w(b + 0x18, dw(r.get("d18", 0)))

        # ---- resolver object array (0020E600 base) ----
        for i, r in enumerate(recs):
            gm.w(OBJB + r.get("d10", 0) + 0xD98, qw(MID_A + i * 0x100))

        # ---- stub-returned objects ----
        bone = case.get("bone", {"v": [10.0, 11.0, 12.0, 13.0]})
        for k, fv in enumerate(bone.get("v", [10.0, 11.0, 12.0, 13.0])):
            gm.w(BONE + 0x30 + k * 4, struct.pack("<f", fv))
        gate = case.get("gate", {"x": 30.0, "y": 31.0, "w": 33.0})
        gm.w(GOBJ + 0x20, struct.pack("<f", gate.get("x", 30.0)))
        gm.w(GOBJ + 0x24, struct.pack("<f", gate.get("y", 31.0)))
        gm.w(GOBJ + 0x2C, struct.pack("<f", gate.get("w", 33.0)))

        # ---- fn5 arg struct ----
        a5 = case.get("arg5", default_arg5())
        gm.w(ARG5 + 0x32, hw(a5.get("w32", 0)))
        for name, off in (("d10", 0x10), ("d54", 0x54), ("d4c", 0x4C),
                          ("d50", 0x50), ("d58", 0x58), ("d5c", 0x5C)):
            gm.w(ARG5 + off, dw(a5.get(name, 0)))

        self.trace, self.faults, self.fired = [], [], set()
        self.e56_ret = case.get("e56_ret", GOBJ)
        self.mid_ret = case.get("mid_ret", MID_A)
        self.outr_ret = case.get("outr_ret", BONE)
        self.sqrt_ret = case.get("sqrt_ret", "compute")
        self.stk28 = case.get("stk28", 0xDEADBEEF)
        for va, data in case.get("plants", []):
            gm.w(va, data)
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (E56, MIDS, OUTR, SQRTF):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in (RES2, GATE, BASE, LEAF):
            uc.hook_add(UC_HOOK_CODE, self.on_watch, begin=va, end=va)

    # ---- hooks ----
    def on_watch(self, uc, addr, size, _):
        """observe a real callee's entry args — the body runs on."""
        if addr == RES2:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("R%x:%x" % (rcx & 0xFFFFFFFF, edx))
        elif addr == GATE:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            self.trace.append("g%x" % (rcx & 0xFFFFFFFF))
        elif addr == BASE:
            ecx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self.trace.append("e%x" % ecx)
        elif addr == LEAF:
            self.trace.append("L")

    def on_call(self, uc, addr, size, _):
        """scripted boundary — record args, plant return, emulate ret."""
        rsp = uc.reg_read(UC_X86_REG_RSP)
        ret = struct.unpack("<Q", self.gm.r(rsp, 8))[0]
        if addr == E56:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            self.trace.append("s%x" % (rcx & 0xFFFFFFFF))
            uc.reg_write(UC_X86_REG_RAX, self.e56_ret)
        elif addr == MIDS:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("m%x:%x" % (rcx & 0xFFFFFFFF, edx))
            uc.reg_write(UC_X86_REG_RAX, self.mid_ret)
        elif addr == OUTR:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("o%x:%x" % (rcx & 0xFFFFFFFF, edx))
            uc.reg_write(UC_X86_REG_RAX, self.outr_ret)
        elif addr == SQRTF:
            x0 = uc.reg_read(UC_X86_REG_XMM0)
            xb = struct.pack("<Q", x0 & 0xFFFFFFFFFFFFFFFF)[:4]
            xv = struct.unpack("<f", xb)[0]
            self.trace.append("q%x" % fbits(xv))
            if self.sqrt_ret == "compute":
                rv = f32(math.sqrt(abs(xv))) if xv == xv else \
                    bits2f(0x7FC00000)
            else:
                rv = bits2f(self.sqrt_ret)
            uc.reg_write(UC_X86_REG_XMM0,
                int.from_bytes(struct.pack("<f", rv) + b"\0" * 12, "little"))
        uc.reg_write(UC_X86_REG_RSP, rsp + 8)
        uc.reg_write(UC_X86_REG_RIP, ret)

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append((access, addr, size))
        uc.reg_write(UC_X86_REG_RIP, RETQ)
        return True

    # ---- run ----
    def run(self, case):
        uc = self.uc
        entry = case["entry"]
        self.gm.w(RETQ, b"\xc3" * 0x100)
        rsp = STACK + 0x80000
        self.gm.w(rsp, qw(RETQ))
        # LODC's uninitialised [rsp+0x28] (= entry_rsp-0x20) — plant canary
        self.gm.w(rsp - 0x20, dw(self.stk28))
        # entry+0xC..0xF canary — read by the movups mutant at the tail
        self.gm.w(rsp + 0xC, dw(case.get("stk0c", 0xAABBCCDD)))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, case.get("ecx", 0))
        uc.reg_write(UC_X86_REG_RDX, case.get("edx", 0))
        uc.reg_write(UC_X86_REG_RDI, case.get("rdi", 0x1122334455667788))
        for reg, key in ((UC_X86_REG_XMM2, "xmm2"), (UC_X86_REG_XMM3, "xmm3")):
            fv = case.get(key, 0.0)
            uc.reg_write(reg,
                int.from_bytes(struct.pack("<f", fv) + b"\0" * 12, "little"))
        uc.emu_start(entry, RETQ, count=4000)
        xmm0 = uc.reg_read(UC_X86_REG_XMM0)
        self.ret_f = struct.unpack("<f", struct.pack("<Q",
            xmm0 & 0xFFFFFFFFFFFFFFFF)[:4])[0]
        self.ret_v = struct.pack("<QQ", xmm0 & 0xFFFFFFFFFFFFFFFF,
                                 (xmm0 >> 64) & 0xFFFFFFFFFFFFFFFF)

    # ---- observation ----
    def obs(self):
        gm = self.gm
        h = self.case.get("ecx", 0) & 0xFF
        s = SLOTS + h * 0xE0
        o = {
            "trace": self.trace,
            "faults": self.faults,
            "slot": gm.r(s, 0xE0).hex(),
            "scr": gm.r(OBS_LO, OBS_HI - OBS_LO).hex(),
            "leafg": gm.r(LEAF_G, 16).hex(),
            "stk": gm.r(STACK + 0x80000 - 0x20, 4).hex(),
        }
        if self.case["entry"] == LODC:
            o["ret_f"] = self.ret_f
            o["ret_v"] = self.ret_v.hex()
        return o


# ---------------- Python model ----------------

def model_case(case, raw, secs):
    """Replicates all six functions' observable effects."""
    ecx = case.get("ecx", 0)
    edx = case.get("edx", 0)
    h = ecx & 0xFF
    slots = [default_slot(i) for i in range(NSLOT)]
    for i, kw in case.get("slots", {}).items():
        slots[i].update(kw)
    recs = [default_rec(i) for i in range(NSLOT)]
    for i, kw in case.get("recs", {}).items():
        recs[i].update(kw)
    s = dict(slots[h])
    trace = []
    # observed window seeded with shipped bytes (or zeros for BSS)
    scr = bytearray(img_rd_or_zero(raw, secs, OBS_LO, OBS_HI - OBS_LO))
    # fixture writes inside the window
    scr[0x22D9140 - OBS_LO:0x22D9144 - OBS_LO] = \
        struct.pack("<f", case.get("g140", 2.0))
    scr[0x22D9144 - OBS_LO:0x22D9148 - OBS_LO] = dw(case.get("g144", 0x11223344))
    scr[0x22D9148 - OBS_LO:0x22D914C - OBS_LO] = \
        struct.pack("<f", case.get("g148", 4.0))
    leaf_init = case.get("leaf_init", [9.0, 8.0, 7.0, 6.0])
    leaf_state = list(leaf_init)
    leaf_c = [img_f(raw, secs, LEAF_C + k * 4) for k in range(4)]
    cvec = case.get("cvec", [1.0, 2.0, 3.0, 4.0])
    bone = case.get("bone", {"v": [10.0, 11.0, 12.0, 13.0]})
    gate = case.get("gate", {"x": 30.0, "y": 31.0, "w": 33.0})
    stk28 = case.get("stk28", 0xDEADBEEF)
    def_f = img_f(raw, secs, DEF_F)

    def put(va, data):
        scr[va - OBS_LO:va - OBS_LO + len(data)] = data
    def putf(va, v):
        put(va, struct.pack("<f", v))

    entry = case["entry"]
    ret_f = 0.0
    gen_ok = (s["i10"] == ecx)

    if entry == LODC:
        ri = sx16(s["w04"])
        r = recs[ri] if 0 <= ri < NSLOT else None
        if not gen_ok or ri == -1 or r is None or r.get("d284", 1) == 0:
            ret_f = def_f
        else:
            mid_ret = case.get("mid_ret", MID_A)
            outr_ret = case.get("outr_ret", BONE)
            e56_ret = case.get("e56_ret", GOBJ)
            rec_va = RECS + ri * 0x740
            trace.append("R%x:%x" % (rec_va & 0xFFFFFFFF,
                                     s["w3c"] & 0xFFFFFFFF))
            if r.get("d18", 0) == 0xFFFFFFFF or r.get("d18", 0) == -1:
                rdi = 0
            else:
                trace.append("e%x" % (r.get("d10", 0) & 0xFFFFFFFF))
                trace.append("m%x:%x" % ((MID_A + ri * 0x100) & 0xFFFFFFFF,
                                         r.get("d18", 0) & 0xFFFFFFFF))
                if mid_ret == 0:
                    rdi = 0
                else:
                    trace.append("o%x:%x" % (mid_ret & 0xFFFFFFFF,
                                             s["w3c"] & 0xFFFFFFFF))
                    rdi = outr_ret
            if rdi == 0 or r.get("d284", 1) == 0:
                ret_f = def_f
            else:
                trace.append("g%x" % (rec_va & 0xFFFFFFFF))
                if r.get("q400", GOBJ) == 0:
                    rax = 0
                else:
                    trace.append("s%x" % (rec_va & 0xFFFFFFFF))
                    rax = e56_ret
                if rax == 0:
                    ret_f = def_f
                else:
                    # vec[0x22D91B0] = const vec (written first)
                    for k, v in enumerate(cvec):
                        putf(0x22D91B0 + k * 4, v)
                    # vec[0x22D91D0] = gate pos + STK
                    gb = [gate.get("x", 30.0), gate.get("y", 31.0),
                          bits2f(stk28), gate.get("w", 33.0)]
                    for k, v in enumerate(gb):
                        putf(0x22D91D0 + k * 4, v)
                    # vec[0x22D91C0] = bone - const
                    gc = [fs(bone["v"][k], cvec[k]) for k in range(4)]
                    for k, v in enumerate(gc):
                        putf(0x22D91C0 + k * 4, v)
                    trace.append("L")
                    leaf_state = list(leaf_c)
                    xmm6, xmm3 = leaf_state[3], leaf_state[0]
                    sqy, sqz, sqx = fm(gc[1], gc[1]), fm(gc[2], gc[2]), \
                        fm(gc[0], gc[0])
                    putf(0x22D91C4, sqy)
                    putf(0x22D91C8, sqz)
                    part = fa(fm(xmm6, sqy), fm(xmm6, sqx))
                    putf(0x22D91AC, part)
                    total = fa(fm(xmm6, sqz), part)
                    putf(0x22D91CC, total)
                    trace.append("q%x" % fbits(total))
                    sqrt_ret = case.get("sqrt_ret", "compute")
                    if sqrt_ret == "compute":
                        dist = f32(math.sqrt(abs(total)))
                    else:
                        dist = bits2f(sqrt_ret)
                    putf(0x22D9198, dist)
                    xmm4 = fa(xmm6, xmm3)
                    putf(0x22D91F0, xmm4)   # pre-subtract store
                    xmm1 = max(fa(xmm3, dist), gb[0])
                    xmm2 = fs(min(gb[1], xmm1), gb[0])
                    xmm2 = fm(xmm2, gb[3])
                    xmm4 = fs(xmm4, xmm2)
                    xmm4 = max(xmm4, xmm3)
                    xmm4 = min(xmm4, xmm6)
                    for k, v in enumerate([xmm4, sqy, sqz, total]):
                        putf(0x22D91C0 + k * 4, v)
                        putf(0x22D8FB0 + k * 4, v)
                    ret_f = xmm4
    elif entry == ACC:
        if gen_ok and s["b40"] & 1:
            if s["b00"]:
                s["f50"] = fa(s["f60"], s["f50"])
                s["f54"] = fa(s["f64"], s["f54"])
                s["b00"] = (s["b00"] - 1) & 0xFF
            if s["b02"]:
                s["f58"] = fa(s["f68"], s["f58"])
                s["f5c"] = fa(s["f6c"], s["f5c"])
                s["b02"] = (s["b02"] - 1) & 0xFF
            if s["b01"]:
                s["f70"] = fa(s["f74"], s["f70"])
                s["b01"] = (s["b01"] - 1) & 0xFF
            if s["b03"]:
                s["f78"] = fa(s["f7c"], s["f78"])
                s["b03"] = (s["b03"] - 1) & 0xFF
            if s["b43"]:
                s["f98"] = fa(s["f9c"], s["f98"])
                s["b43"] = (s["b43"] - 1) & 0xFF
    elif entry == CPY:
        if gen_ok:
            s["f30"] = s["f48"]
            s["f34"] = s["f4c"]
            s["w3a"] = s["w38"]
            s["f48"] = f32(case.get("xmm2", 0.0))
            s["f4c"] = f32(case.get("xmm3", 0.0))
            s["w38"] = s["w3c"] if edx == 0 else s["w3e"]
    elif entry == INIT:
        if gen_ok:
            for k, off in enumerate((0xC0, 0xC4, 0xC8, 0xCC, 0xD0, 0xD4)):
                s["f%02x" % (0x80 + k * 4)] = s["f%02x" % off]
            s["b43"] = edx & 0xFF
            s["f98"] = 0.0
            put(0x22D914C, dw(0x3F800000))
            q = fd(1.0, bits2f(edx))
            put(0x22D9148, dw(edx))
            put(0x22D8F90, qw(0x3F800000))
            s["f9c"] = q
            if edx & 0xFF:
                s["f98"] = fa(q, s["f98"])
                s["b43"] = (edx & 0xFF) - 1
    elif entry == FSYNC:
        if gen_ok:
            a5 = case.get("arg5", default_arg5())
            w32 = a5.get("w32", 0)
            cl = s["b40"]
            if cl & 2:
                s["f50"], s["f54"] = s["fa0"], s["fa4"]
                s["f80"], s["f84"] = s["fa0"], s["fa4"]
                s["b00"] = 0
            if cl & 4:
                s["f70"] = s["fb0"]
                s["f90"] = s["fb0"]
                s["b03"] = 0
            if cl & 8:
                s["f58"], s["f5c"] = s["fa8"], s["fac"]
                s["f88"], s["f8c"] = s["fa8"], s["fac"]
                s["b02"] = 0
            if cl & 0x10:
                s["f48"] = s["fb4"]
                s["f4c"] = s["fb8"]
            if w32 != 0:
                s["fa0"] = bits2f(a5["d4c"])
                s["fa4"] = bits2f(a5["d50"])
                scaled = fm(f32(float(sx16(w32) >> 6)),
                            img_f(raw, secs, FS_MUL))
                s["fb0"] = scaled
                s["fb4"] = bits2f(a5["d58"])
                s["fb8"] = bits2f(a5["d5c"])
                s["fa8"] = bits2f(a5["d10"])
                s["fac"] = bits2f(a5["d54"])
            al = cl
            for wbit, obit in ((0, 1), (1, 2), (3, 3), (2, 4), (4, 5), (5, 6)):
                m = 1 << obit
                al = (al & ~m) | (((w32 >> wbit) & 1) << obit)
            s["b00"] = s["b01"] = s["b02"] = s["b03"] = 0
            s["b40"] = al & 0xFF
    elif entry == CLRE:
        if gen_ok:
            s["b40"] &= 0xFE
    elif entry == LEAF:
        trace.append("L")
        leaf_state = list(leaf_c)

    # ---- serialise model slot (same bytes the fixture plants) ----
    b = bytearray(0xE0)
    struct.pack_into("<I", b, 0x10, s.get("i10", h))
    for name, off in (("w04", 4), ("w38", 0x38), ("w3a", 0x3A),
                      ("w3c", 0x3C), ("w3e", 0x3E)):
        struct.pack_into("<H", b, off, s.get(name, 0) & 0xFFFF)
    for name, off in (("b00", 0), ("b01", 1), ("b02", 2), ("b03", 3),
                      ("b40", 0x40), ("b43", 0x43)):
        b[off] = s.get(name, 0) & 0xFF
    for name, off in (("f08", 8), ("f0c", 0xC), ("f14", 0x14),
                      ("f18", 0x18), ("f2c", 0x2C), ("f30", 0x30),
                      ("f34", 0x34), ("f44", 0x44), ("f48", 0x48),
                      ("f4c", 0x4C), ("f50", 0x50), ("f54", 0x54),
                      ("f58", 0x58), ("f5c", 0x5C), ("f60", 0x60),
                      ("f64", 0x64), ("f68", 0x68), ("f6c", 0x6C),
                      ("f70", 0x70), ("f74", 0x74), ("f78", 0x78),
                      ("f7c", 0x7C), ("f80", 0x80), ("f84", 0x84),
                      ("f88", 0x88), ("f8c", 0x8C), ("f90", 0x90),
                      ("f94", 0x94), ("f98", 0x98), ("f9c", 0x9C),
                      ("fa0", 0xA0), ("fa4", 0xA4), ("fa8", 0xA8),
                      ("fac", 0xAC), ("fb0", 0xB0), ("fb4", 0xB4),
                      ("fb8", 0xB8), ("fbc", 0xBC), ("fc0", 0xC0),
                      ("fc4", 0xC4), ("fc8", 0xC8), ("fcc", 0xCC),
                      ("fd0", 0xD0), ("fd4", 0xD4)):
        struct.pack_into("<f", b, off, s.get(name, 0.0))
    leafg = b"".join(struct.pack("<f", v) for v in leaf_state)
    o = {"trace": trace, "faults": [], "slot": bytes(b).hex(),
         "scr": bytes(scr).hex(), "leafg": leafg.hex(),
         "stk": dw(stk28).hex()}
    if entry == LODC:
        o["ret_f"] = ret_f
        o["ret_v"] = (struct.pack("<f", ret_f) + b"\0" * 12).hex()
    return o


# ---------------- cases ----------------

def sl(i, **kw):
    d = default_slot(i)
    d.update(kw)
    return d


def build_cases():
    C = {}
    base = {"entry": LODC, "ecx": 3}
    C["lodc-happy"] = dict(base)
    C["lodc-gen-bad"] = dict(base, slots={3: {"i10": 99}})
    C["lodc-w04-neg"] = dict(base, slots={3: {"w04": 0xFFFF}})
    C["lodc-d284-0"] = dict(base, recs={3: {"d284": 0}})
    C["lodc-res2-null"] = dict(base, outr_ret=0)
    C["lodc-mid-null"] = dict(base, mid_ret=0)
    C["lodc-gate-null"] = dict(base, e56_ret=0)
    C["lodc-q400-0"] = dict(base, recs={3: {"q400": 0}})
    C["lodc-d18-neg"] = dict(base, recs={3: {"d18": -1}})
    C["lodc-near"] = dict(base, cvec=[10.0, 11.0, 12.0, 13.0])
    C["lodc-far"] = dict(base, cvec=[0.0, 0.0, 0.0, 0.0],
                         bone={"v": [1.0, 50.0, 60.0, 70.0]})
    C["lodc-stk"] = dict(base, stk28=0x12345678)
    # mid-range: dist=35 sits between gate.x=30 and gate.y=100 so the
    # min/max arms land in-range (gate.w=0.1 keeps xmm2 small)
    C["lodc-mid"] = dict(base, cvec=[0.0, 0.0, 0.0, 0.0],
                         bone={"v": [35.0, 0.0, 0.0, 0.0]},
                         gate={"x": 30.0, "y": 100.0, "w": 0.1})
    # w04==-1 but rec[-1] fully planted — a live gen for the arm that
    # follows the (mutated) not-minus-one path
    C["lodc-w04-neg-live"] = dict(base, slots={3: {"w04": 0xFFFF}},
        plants=[(RECS - 0x740 + 0x284, dw(1)),
                (RECS - 0x740 + 0x400, qw(GOBJ)),
                (RECS - 0x740 + 0x10, dw(0x123000)),
                (RECS - 0x740 + 0x18, dw(0)),
                (OBJB + 0x123000 + 0xD98, qw(MID_A))])
    C["acc-on"] = {"entry": ACC, "ecx": 2}
    C["acc-gen-bad"] = {"entry": ACC, "ecx": 2, "slots": {2: {"i10": 99}}}
    C["acc-off"] = {"entry": ACC, "ecx": 2, "slots": {2: {"b40": 0}}}
    C["acc-idle"] = {"entry": ACC, "ecx": 2, "slots":
                     {2: {"b00": 0, "b01": 0, "b02": 0, "b03": 0, "b43": 0}}}
    C["acc-ch0"] = {"entry": ACC, "ecx": 2, "slots":
                    {2: {"b00": 1, "b01": 0, "b02": 0, "b03": 0, "b43": 0}}}
    C["acc-ch43"] = {"entry": ACC, "ecx": 2, "slots":
                     {2: {"b00": 0, "b01": 0, "b02": 0, "b03": 0}}}
    C["cpy-d0"] = {"entry": CPY, "ecx": 1, "edx": 0,
                   "xmm2": 4.5, "xmm3": 5.5}
    C["cpy-d1"] = {"entry": CPY, "ecx": 1, "edx": 7,
                   "xmm2": -1.5, "xmm3": 0.25}
    C["cpy-gen-bad"] = {"entry": CPY, "ecx": 1, "slots": {1: {"i10": 77}}}
    C["init-d0"] = {"entry": INIT, "ecx": 4, "edx": 0}
    C["init-d5"] = {"entry": INIT, "ecx": 4, "edx": 5}
    C["init-gen-bad"] = {"entry": INIT, "ecx": 4, "slots": {4: {"i10": 55}}}
    C["init-dbig"] = {"entry": INIT, "ecx": 4, "edx": 0x3F800000}
    C["init-dmid"] = {"entry": INIT, "ecx": 4, "edx": 0x40000000}
    C["fsync-flags"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                        "slots": {5: {"b40": 0x1F}}}
    C["fsync-plain"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                        "slots": {5: {"b40": 0x01}}}
    C["fsync-w32-0"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                        "arg5": dict(default_arg5(), w32=0)}
    C["fsync-w32-ff"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                         "arg5": dict(default_arg5(), w32=0xFFFF)}
    # w32=0x40: bit6 set — sar ax,6 yields 1, sar ax,7 yields 0
    C["fsync-w32-40"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                         "arg5": dict(default_arg5(), w32=0x0040)}
    C["fsync-gen-bad"] = {"entry": FSYNC, "ecx": 5, "edx": ARG5,
                          "slots": {5: {"i10": 42}}}
    C["clre-on"] = {"entry": CLRE, "ecx": 6, "slots": {6: {"b40": 0xFF}}}
    C["clre-gen-bad"] = {"entry": CLRE, "ecx": 6,
                         "slots": {6: {"i10": 42}}}
    C["leaf-run"] = {"entry": LEAF, "ecx": 0}
    C["leaf-diff"] = {"entry": LEAF, "ecx": 0,
                      "leaf_init": [0.0, 0.0, 0.0, 0.0]}
    return C


# ---------------- mutants ----------------

def B(x): return bytes([x])

MUTS = [
    # fn1 LODC gates + math
    ("m-gendisp",  0x3B599B, B(0x10), B(0x14), "lodc-happy"),
    ("m-gen-je",   0x3B599C, B(0x74), B(0x75), "lodc-happy"),
    ("m-w04-neg",  0x3B59B4, B(0x74), B(0x75), "lodc-w04-neg-live"),
    ("m-d284-je",  0x3B59D7, B(0x74), B(0x75), "lodc-happy"),
    ("m-res2-je",  0x3B59EE, B(0x84), B(0x85), "lodc-happy"),
    ("m-d284b-je", 0x3B5A21, B(0x84), B(0x85), "lodc-happy"),
    ("m-gate-je",  0x3B5A2F, B(0x84), B(0x85), "lodc-happy"),
    ("m-sub-dy",   0x3B5A84, B(0x5C), B(0x58), "lodc-happy"),
    ("m-sq-dy",    0x3B5B07, B(0x59), B(0x58), "lodc-happy"),
    ("m-sum",      0x3B5B35, B(0x58), B(0x5C), "lodc-happy"),
    ("m-fabs",     0x3B5B4B, B(0x54), B(0x55), "lodc-happy"),
    ("m-max",      0x3B5B8F, B(0x5F), B(0x5D), "lodc-mid"),
    ("m-min",      0x3B5B97, B(0x5D), B(0x5F), "lodc-mid"),
    ("m-clamp-hi", 0x3B5BB3, B(0x5D), B(0x5F), "lodc-mid"),
    ("m-ret",      0x3B5BD8, B(0x10), B(0x11), "lodc-happy"),
    # fn2 ACC
    ("m-acc-gen",  0x3B5C15, B(0x85), B(0x84), "acc-on"),
    ("m-acc-en",   0x3B5C1F, B(0x84), B(0x85), "acc-on"),
    ("m-acc-dec0", 0x3B5C31, B(0xC9), B(0xC1), "acc-ch0"),
    ("m-acc-add",  0x3B5C39, B(0x58), B(0x5C), "acc-ch0"),
    ("m-acc-b1",   0x3B5C7E, B(0x74), B(0x75), "acc-on"),
    # fn3 CPY
    ("m-cpy-gen",  0x3B5CF6, B(0x75), B(0x74), "cpy-d0"),
    ("m-cpy-edx",  0x3B5D20, B(0x75), B(0x74), "cpy-d0"),
    ("m-cpy-w3c",  0x3B5D2B, B(0x38), B(0x39), "cpy-d0"),
    # fn4 INIT
    ("m-init-gen", 0x3B5D57, B(0x85), B(0x84), "init-d5"),
    ("m-init-div", 0x3B5DD9, B(0x5E), B(0x59), "init-dmid"),
    ("m-init-tst", 0x3B5DFA, B(0x74), B(0x75), "init-d5"),
    ("m-init-dec", 0x3B5E06, B(0xC8), B(0xC0), "init-d5"),
    # fn5 FSYNC
    ("m-fs-gen",   0x3B5E3A, B(0x85), B(0x84), "fsync-flags"),
    ("m-fs-b1",    0x3B5E47, B(0x74), B(0x75), "fsync-flags"),
    ("m-fs-b4",    0x3B5EDC, B(0x74), B(0x75), "fsync-flags"),
    ("m-fs-w32",   0x3B5EF9, B(0x74), B(0x75), "fsync-flags"),
    ("m-fs-m2",    0x3B5F69, B(0x02), B(0x03), "fsync-w32-ff"),
    ("m-fs-m10",   0x3B5FB6, B(0x10), B(0x20), "fsync-w32-ff"),
    ("m-fs-m40",   0x3B5FF1, B(0x40), B(0x80), "fsync-flags"),
    ("m-fs-sar",   0x3B5F16, B(0x06), B(0x07), "fsync-w32-40"),
    ("m-fs-clr",   0x3B5FEC, B(0x00), B(0x42), "fsync-flags"),
    # fn6 CLRE
    ("m-clre-gen", 0x3B6014, B(0x75), B(0x74), "clre-on"),
    ("m-clre-m",   0x3B6019, B(0xFE), B(0xFC), "clre-on"),
]


def run_native(case):
    raw, secs = load_image()
    w = World(case, raw, secs)
    w.run(case)
    return w.obs()


def run_model(case):
    raw, secs = load_image()
    return model_case(case, raw, secs)


def main():
    cases = build_cases()
    keys = ("trace", "ret_f", "ret_v", "slot", "scr", "leafg", "stk",
            "faults")
    results = {"cases": {}, "mutants": {}, "bad_sites": []}
    fails = 0
    for name, case in cases.items():
        nat = run_native(case)
        mod = run_model(case)
        d = [k for k in keys if k in nat and nat[k] != mod.get(k)]
        results["cases"][name] = "ok" if not d else {"diff": d}
        if d:
            fails += 1
            print("CASE", name, "DIFF", d)
            for k in d:
                print("  nat:", str(nat.get(k))[:170])
                print("  mod:", str(mod.get(k))[:170])
    print("functional: %d/%d" % (len(cases) - fails, len(cases)))

    raw, secs = load_image()
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
        case["patch_bytes"] = list(case.get("patch_bytes", [])) + [(va, mut)]
        try:
            nat = run_native(case)
        except Exception as e:
            print("MUTANT CRASH", mid, repr(e), flush=True)
            results["mutants"][mid] = "crash: %r" % e
            continue
        mod = run_model(case)
        if [k for k in keys if k in nat and nat[k] != mod.get(k)]:
            results["mutants"][mid] = "killed"
        else:
            results["mutants"][mid] = "ALIVE"
            alive += 1
            print("MUTANT ALIVE", mid, flush=True)
    print("mutants: %d/%d killed" % (len(MUTS) - alive, len(MUTS)))
    json.dump(results, open(RESULT, "w"), indent=1)


if __name__ == "__main__":
    main()
