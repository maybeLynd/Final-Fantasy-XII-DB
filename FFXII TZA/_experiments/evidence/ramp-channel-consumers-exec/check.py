# EXP-108 ramp-channel-consumers-exec
#
# Executes the SHIPPED bytes of the two unexecuted consumers named in
# CONTRACT-authored-command-ramp-channels section 13 under Unicorn:
#
#   003B6020  PASS    per-frame shadow-draw pass (677 B), no args.
#               head: copy 0x1A0-byte record template (planted at
#               0x2AEA0D0 — BSS) patched with four xmm consts (planted
#               0x2AEDDB0..+0x30) into q[entry+0] of draw-list entry
#               0x2EBEFC0 + 24*d[0x2EBEFF0]; entry+8 += 0x1A0.
#               rsi = 003A1DB0()  (buffer swap; see below)
#               copy 0xA0 template (planted 0x2AEA030) -> rsp+0x20.
#               loop edi=0xA0 slots over q[0x2B40528], stride 0xE0:
#                 !(b[s+0x40]&1)              -> skip   (bit0 = ENABLE)
#                 (b[s+0x41] | d[0x2B40524])&2 -> HIDE -> skip
#                 ecx = d[s+0x10]; rdx = out stack buf
#                 003B62D0(ecx, rdx); eax==0  -> skip
#                 copy 0xA0 rsp+0x20 -> q[rsi+0]; q[rsi+8] += 0xA0
#                 rsi = 003A1DB0()            (alternates entries)
#
#   003B62D0  BLD     shadow-draw record builder (~1.28 KB).
#               ecx = channel id; rdx = out 0xA0 buffer.
#               rbx = u8(ecx)*0xE0 + q[0x2B40528]; d[rbx+0x10] != ecx -> ret 0
#               w[rbx+4] == 0xFFFF -> ret 0
#               rbp = sx16(w[rbx+4])*0x740 + q[0x22C6F28]
#               d[rbp+0x284] == 0 -> ret 0
#               r14 = 00421FF0(rbp, zx(w[rbx+0x3C]))   null -> ret 0
#               r15 = 00421FF0(rbp, zx(w[rbx+0x3E]))   null -> ret 0
#               rsi = 003B6BF0(zx(w[rbx+4]))           null -> ret 0
#               edx = cvt((w[rsi+6]-w[rsi+4])*f[rbx+0x14]) + w[rsi+4]
#               out+0x14 = edx; out+0x6C = d[0xD11580 + edx*4]
#               out+0x10 = 2*(cvt((w[rsi+2]-b[rsi+1])*f14) + b[rsi+1])
#               out+0x30 = d[rsi+8]
#               out+0x20 = f14*f[rsi+0x3C] + f[rsi+0x38]; if edx>1: /= edx-1
#               out+0x10 bounds: <4 or >0x64 -> ret 0 (partial out written)
#               b[rbx+0x40]&0x40: out+0x54=d[r14+0x34], out+0x44=0,
#                   out+0x40 = f[rsi+0x14]+f[rsi+0x10]
#                 else:           out+0x54=00264670(q[rbp+0x108]),
#                   out+0x40=d[rsi+0x10], out+0x44=d[rsi+0x14]
#               out+0x48=d[rsi+0x34], out+0x4C=d[rsi+0x30]
#               out+0x60/64/68 = d[rbx+0x20/24/28]
#               v34 = f[rsi+0x18]*f[rbx+8]*f[rbx+0x44]
#               v38 = f[rsi+0x1C]*f[rbx+8]*f[rbx+0x44]
#               v28 = f[rbx+0xC]*f[rsi+0xC]*1.0*f[rbx+0x2C]*0.5
#               b[rbx+0x43]==0: x4..x9 = slot row f50/54/58/5C/70/78
#                 else: xmm3 = 0046FAE0(f[rbx+0x98], edx=1, r8d=2)
#                       xmm2 = 1.0-xmm3; x4..x9 = interp rows;
#                       b40&0x20 -> x4=f50,x5=f54; xmm3=1,xmm2=0
#               blend (b43==0 path): w38==w3c -> r14.f30/f38 else r15
#               blend (b43!=0):    w3a==w38 -> r14/r15 direct;
#                 w38==w3c -> xmm2*r15+xmm3*r14; else xmm2*r14+xmm3*r15
#               writeback rbx+0xC0..0xD4 = x4,x5,x7,x8,x6,x9
#               x4 += f[rbx+0x48]; x5 += f[rbx+0x4C]; x4,x5 *= f[rbx+0x44]
#               x6 += f[rbp+0x124] + f[rbx+0xBC]
#               out+0x34=x7*v34; out+0x38=x8*v38; out+0x28=x9*v28; out+0x24=x6
#               idx = cvt(f[rbp+0x124]/2pi * 32768) & 0x7FFF
#               sin = LUT_TRIG[idx]; cos = LUT_TRIG[(0x2000+idx)&0x7FFF]
#               out+0x50 += (x4+f18)*cos + x5*sin
#               out+0x58 += x5*cos - (x4+f18)*sin
#               ret 1
#
#   Shallow callees executed real:
#   003A1DB0  swap    edx = d[0x2EBEFF0]; d[0x2EBEFF0] = 1-edx;
#                     rcx = q[ents[old]+0]; edx = (q[ents[old]+8]-rcx)>>4;
#                     0036F360(rcx, edx); ents[new].cursor = ents[new].base;
#                     ret &ents[new].
#   0036F360  fin     n16 = edx headers of 16 B at rcx; last hdr
#                     &0x70000000 == 0x30000000 -> append/overwrite
#                     terminator {0x10000000, 0}; all rip ops hit the
#                     single cell 0x2EBA3F8 -> converges to 0x100.
#   00264670  k3f     rcx==0 or (b[r+3]&0xE0)!=0x60 -> 0.0
#                     else xmm0 = f[q[r+0xB8]+0xD4]
#   0046FAE0  rampLUT row = (3*edx+r8d)*0x1E0 + 0x1F20E60;
#                     idx = cvttss2si((d[0x1F20A97]-1)*xmm0);
#                     POSITIVE overflow clamps to cnt-1; NEGATIVE idx
#                     passes through unclamped (cmovs equalises).
#   003B6BF0  resolve cx==-1 -> 0; rec = sx16(cx)*0x740+q[0x22C6F28];
#                     d[rec+0x284]==0 -> 0 else tail 003E6F70.
#   003E6F70  gate    q[rec+0x400]==0 -> 0 else tail 003E56A0 (stub).
#   00421FF0  res2    ebx = d[rcx+0x18]; -1 -> 0;
#                     rax = 0020E600(d[rcx+0x10]) = q[0x1F83530]+ecx;
#                     rcx = q[rax+0xD98]; rax = 002ED570(rcx, ebx) stub;
#                     rax==0 -> 0 else tail 00370F60(rax, edi) stub.
#   0020E600  base    rax = ecx + q[0x1F83530]  (runtime base — planted)
#
# Scripted boundaries (disclosed — deep object resolvers, not executed):
#   003E56A0  rcx = actor rec -> returns planted OBJ_S (arg captured)
#   002ED570  rcx = q[base+off+0xD98], edx = d[rbp+0x18] -> planted MID
#   00370F60  rcx = MID, edx = orig word -> planted OBJ14/OBJ15 per call
#
# Shipped tables used with ZERO fixture (real .rdata/.data bytes):
#   0xD11580 dword LUT, 0x1F004E0 0x8000-float trig LUT,
#   0x1F20E60 ramp LUT (0x1E0 stride), d[0x1F20A97] row count = 15360,
#   K1/K2 = +-32768.0 @0xD10820/0xD10828, 2pi @0x1CEBC78,
#   consts 1.0 @0x1EFE314, 0.5 @0x1CEBB70.
#
# BSS cells the fixture plants: 0x2B40524 gate, 0x2B40528 slot-table ptr,
# 0x22C6F28 rec-table ptr, 0x2EBEFF0 bufidx, 0x2EBEFC0 entries,
# 0x1F83530 resolver base, 0x2EBA3F8 ring cell, templates
# 0x2AEA0D0/0x2AEA030/0x2AEDDB0.. (all runtime-populated in game).
#
# Trace tokens: W swap-entry, f<base>:<n16> fin-entry, b<ecx>@<rdx>
# bld-entry, R<rbp>:<kind> res2, e<ecx> base, m<mid>:<ebx> mids-stub,
# o<mid>:<kind> outr-stub, r<w04> res1, g<rbp> gate, s<rbp> e56-stub,
# k<rcx> k3f, L<edx>:<r8d>:<xmm0> rampLUT.

import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_HOOK_MEM_UNMAPPED, \
    UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RAX, UC_X86_REG_RCX, \
    UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RIP, UC_X86_REG_RSP, \
    UC_X86_REG_XMM0

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP   = 0x40000000
STACK  = 0x61000000
RETQ   = 0x62000000

PASS   = 0x003B6020
BLD    = 0x003B62D0
SWAP   = 0x003A1DB0        # real — calls FIN
FIN    = 0x0036F360        # real leaf
K3F    = 0x00264670        # real leaf
RLUT   = 0x0046FAE0        # real leaf
RES1   = 0x003B6BF0        # real — tail GATE
GATE   = 0x003E6F70        # real — tail E56 (stub) or ret 0
RES2   = 0x00421FF0        # real — calls BASE, MIDS(stub), tail OUTR(stub)
BASE   = 0x0020E600        # real leaf
E56    = 0x003E56A0        # STUB — deep resolver
MIDS   = 0x002ED570        # STUB — deep resolver
OUTR   = 0x00370F60        # STUB — deep resolver

# BSS globals (runtime-populated — planted by fixture)
G_GATE   = 0x02B40524      # hide gate cell
G_SLOTS  = 0x02B40528      # qword: slot table base (stride 0xE0)
G_RECS   = 0x022C6F28      # qword: actor-rec table base (stride 0x740)
G_BUFIDX = 0x02EBEFF0      # dword: active draw-list entry index
G_ENTS   = 0x02EBEFC0      # 24-byte entries {+0 wr base, +8 cursor, +0x10 x}
G_BASE   = 0x01F83530      # qword: 0020E600 resolver base
G_RING   = 0x02EBA3F8      # 0036F360's single state cell
T_HEAD   = 0x02AEA0D0      # 0x1A0 head-record template (BSS)
T_SLOT   = 0x02AEA030      # 0xA0 slot-record template (BSS)
T_XMM    = 0x02AEDDB0      # four xmm consts (BSS): patch offs D0/E0/F0/100

# heap layout
SLOTS  = HEAP + 0x000000   # 160 x 0xE0
RECS   = HEAP + 0x100000   # 0x740-stride actor records
OBJB   = HEAP + 0x300000   # 0020E600 base — object array
OBJ_S  = HEAP + 0x500000   # rsi object (BLD build source)
OBJ_14 = HEAP + 0x510000   # r14 object (first  OUTR stub return)
OBJ_15 = HEAP + 0x520000   # r15 object (second OUTR stub return)
MID_A  = HEAP + 0x530000   # 002ED570 stub return base (+i*0x100 arg ptr)
K3REC  = HEAP + 0x540000   # kind-3 float record (00264670 source)
K3P    = HEAP + 0x541000   # its +0xB8 target
BUF0   = HEAP + 0x600000   # draw buffer 0
BUF1   = HEAP + 0x700000   # draw buffer 1
OUT    = HEAP + 0x800000   # BLD direct-entry out buffer

NSLOT = 0xA0

# shipped model constants
LUT_RAMP = 0x01F20E60     # ramp LUT, 0x1E0-stride rows
LUT_CNT  = 0x01F20A98     # dword row count (60)
LUT_TRIG = 0x01F004E0     # 0x8000-float trig LUT
LUT_DW   = 0x00D11580     # dword LUT
K1A, K2A = 0x00D10820, 0x00D10828     # +-32768.0
C2A      = 0x01CEBC78                 # 2pi
CA, CB   = 0x01EFE314, 0x01CEBB70     # 1.0, 0.5


def qw(v): return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def hw(v): return struct.pack("<H", v & 0xFFFF)
def s32(v):
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v & 0x80000000 else v
def sx16(v):
    v &= 0xFFFF
    return v - 0x10000 if v & 0x8000 else v
def f32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]
def fbits(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]
def bits2f(b):
    return struct.unpack("<f", struct.pack("<I", b & 0xFFFFFFFF))[0]
def cvt(x):
    """cvttss2si — truncate toward zero."""
    x = f32(x)
    if x != x or x >= 2147483648.0 or x < -2147483649.0:
        return -0x80000000
    return int(x)
def fm(a, b): return f32(f32(a) * f32(b))
def fa(a, b): return f32(f32(a) + f32(b))
def fs(a, b): return f32(f32(a) - f32(b))
def fd(a, b): return f32(f32(a) / f32(b))


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


# default slot field set — a fully-visible, fully-populated slot
def default_slot(i):
    return {
        "i10": i,            # +0x10 self channel id (dword)
        "w04": i,            # +0x04 actor-rec index
        "b40": 0x01,         # +0x40 flags (bit0 ENABLE, bit5 sel, bit6 alt)
        "b41": 0,            # +0x41 hide byte (bit1)
        "b43": 1,            # +0x43 LUT-path flag
        "w38": 0, "w3a": 1, "w3c": 2,   # +0x38/3A/3C word selectors
        "w3e": 3,            # +0x3E second resolver word
        "f08": 1.5, "f0c": 0.5, "f14": 0.25, "f18": 0.75,
        "f2c": 0.4, "f44": 2.0, "f48": 0.1, "f4c": 0.2,
        "f98": 0.6,          # ramp-LUT index float
        "d20": 0x11, "d24": 0x22, "d28": 0x33,
        "f50": 7.0, "f54": 8.0, "f58": 9.0, "f5c": 10.0,
        "f70": 11.0, "f78": 12.0, "f80": 13.0, "f84": 14.0,
        "f88": 15.0, "f8c": 16.0, "f90": 17.0, "f94": 18.0,
        "fbc": 0.05,
    }


def default_rec(i):
    # d10 is a BYTE OFFSET into the 0020E600 object array — stride by a
    # full object page so each rec resolves its own mid-array cell
    return {"d284": 1, "q400": OBJ_S, "d10": i * 0x2000, "d18": 0,
            "f124": 0.5}


def default_sobj():
    """OBJ_S — the build-source object (rsi) the e56 stub returns.
    d10/d14 are dual-use: raw dwords on the kind-3 path, float addends
    on the b40&0x40 path — planted as float bits."""
    return {"b01": 2, "w02": 20, "w04": 1, "w06": 20, "d08": 0xABCDEF01,
            "f0c": 0.6,
            "d10": fbits(0.75), "d14": fbits(0.5),
            "f18": 0.5, "f1c": 0.25,
            "d30": fbits(0.9), "d34": 0x77889900,
            "f38": 0.125, "f3c": 2.0}


def default_robj(tag):
    """OBJ_14/OBJ_15 — the two resolver-result objects (r14/r15)."""
    return {"d30": fbits(0.375 + tag), "d34": 0xD000 + tag,
            "d38": fbits(0.625 + tag)}


def head_template(case):
    t = bytearray(case.get("thead",
              [(0xA0 + (j & 0x5F)) & 0xFF for j in range(0x1A0)]))
    xm = case.get("xmm", [0.5, 1.0, 2.0, -1.0] * 4)
    for k in range(4):
        t[0xD0 + k * 0x10:0xE0 + k * 0x10] = struct.pack(
            "<4f", *xm[k * 4:k * 4 + 4])
    return bytes(t)


def slot_template(case):
    return bytes(case.get("tslot",
             [(0x30 + (j & 0x3F)) & 0xFF for j in range(0xA0)]))


class World:
    def __init__(self, case, raw, secs):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x1000000)
        gm.map(STACK, 0x100000)

        # ---- globals ----
        gm.w(G_GATE, dw(case.get("gate", 0)))
        gm.w(G_SLOTS, qw(SLOTS))
        gm.w(G_RECS, qw(RECS))
        gm.w(G_BUFIDX, dw(case.get("bufidx", 0)))
        bufs = case.get("bufs", [BUF0, BUF1])
        for i in range(2):
            gm.w(G_ENTS + i * 24 + 0x00, qw(bufs[i]))
            gm.w(G_ENTS + i * 24 + 0x08, qw(bufs[i]))
            gm.w(G_ENTS + i * 24 + 0x10, qw(case.get("e16", 0)))
        gm.w(G_BASE, qw(OBJB))
        gm.w(G_RING, dw(case.get("ring", 0)))

        # templates + xmm consts (BSS in game — planted patterns)
        gm.w(T_HEAD, bytes(case.get("thead",
               [(0xA0 + (j & 0x5F)) & 0xFF for j in range(0x1A0)])))
        gm.w(T_SLOT, slot_template(case))
        for k, fv in enumerate(case.get("xmm",
               [0.5, 1.0, 2.0, -1.0] * 4)):
            gm.w(T_XMM + k * 4, struct.pack("<f", fv))

        # ---- slots ----
        slots = case.get("slots", [default_slot(i) for i in range(NSLOT)])
        for i, s in enumerate(slots):
            b = SLOTS + i * 0xE0
            gm.w(b + 0x10, dw(s.get("i10", i)))
            gm.w(b + 0x04, hw(s.get("w04", i) & 0xFFFF))
            gm.w(b + 0x40, bytes([s.get("b40", 0) & 0xFF]))
            gm.w(b + 0x41, bytes([s.get("b41", 0) & 0xFF]))
            gm.w(b + 0x43, bytes([s.get("b43", 0) & 0xFF]))
            gm.w(b + 0x38, hw(s.get("w38", 0)))
            gm.w(b + 0x3A, hw(s.get("w3a", 0)))
            gm.w(b + 0x3C, hw(s.get("w3c", 0)))
            gm.w(b + 0x3E, hw(s.get("w3e", 0)))
            gm.w(b + 0x20, dw(s.get("d20", 0)))
            gm.w(b + 0x24, dw(s.get("d24", 0)))
            gm.w(b + 0x28, dw(s.get("d28", 0)))
            for name, off in (("f08", 8), ("f0c", 0xC), ("f14", 0x14),
                              ("f18", 0x18), ("f2c", 0x2C), ("f44", 0x44),
                              ("f48", 0x48), ("f4c", 0x4C),
                              ("f50", 0x50), ("f54", 0x54), ("f58", 0x58),
                              ("f5c", 0x5C), ("f70", 0x70), ("f78", 0x78),
                              ("f80", 0x80), ("f84", 0x84), ("f88", 0x88),
                              ("f8c", 0x8C), ("f90", 0x90), ("f94", 0x94),
                              ("f98", 0x98), ("fbc", 0xBC)):
                gm.w(b + off, struct.pack("<f", s.get(name, 0.0)))

        # ---- actor records ----
        recs = case.get("recs", [default_rec(i) for i in range(NSLOT)])
        for i, r in enumerate(recs):
            b = RECS + i * 0x740
            gm.w(b + 0x284, dw(r.get("d284", 1)))
            gm.w(b + 0x400, qw(r.get("q400", OBJ_S)))
            gm.w(b + 0x10, dw(r.get("d10", 0)))
            gm.w(b + 0x18, dw(r.get("d18", 0)))
            gm.w(b + 0x108, qw(r.get("q108", K3REC)))
            gm.w(b + 0x124, struct.pack("<f", r.get("f124", 0.0)))

        # ---- resolver object array (0020E600 base) ----
        # res2: rcx = q[OBJB + rec.d10 + 0xD98] -> MIDS stub arg
        for i, r in enumerate(recs):
            gm.w(OBJB + r.get("d10", 0) + 0xD98, qw(MID_A + i * 0x100))

        # ---- stub-returned objects ----
        sobj = case.get("sobj", default_sobj())
        self.sobj = sobj
        gm.w(OBJ_S + 1, bytes([sobj.get("b01", 0) & 0xFF]))
        for name, off in (("w02", 2), ("w04", 4), ("w06", 6)):
            gm.w(OBJ_S + off, hw(sobj.get(name, 0)))
        gm.w(OBJ_S + 8, dw(sobj.get("d08", 0)))
        for name, off in (("d10", 0x10), ("d14", 0x14), ("d30", 0x30),
                          ("d34", 0x34)):
            gm.w(OBJ_S + off, dw(sobj.get(name, 0)))
        for name, off in (("f0c", 0xC), ("f18", 0x18), ("f1c", 0x1C),
                          ("f38", 0x38), ("f3c", 0x3C)):
            gm.w(OBJ_S + off, struct.pack("<f", sobj.get(name, 0.0)))

        robj14 = case.get("robj14", default_robj(1))
        robj15 = case.get("robj15", default_robj(2))
        for obj, ro in ((OBJ_14, robj14), (OBJ_15, robj15)):
            gm.w(obj + 0x30, dw(ro.get("d30", 0)))
            gm.w(obj + 0x34, dw(ro.get("d34", 0)))
            gm.w(obj + 0x38, dw(ro.get("d38", 0)))

        # kind-3 float record for 00264670 (q[rbp+0x108] -> record)
        k3 = case.get("k3", {"pk": 0x60, "f": 0.03125})
        gm.w(K3REC + 3, bytes([k3.get("pk", 0x60) & 0xFF]))
        gm.w(K3REC + 0xB8, qw(K3P))
        gm.w(K3P + 0xD4, struct.pack("<f", k3.get("f", 0.0)))

        self.trace, self.faults, self.fired = [], [], set()
        self.e56_ret = case.get("e56_ret", OBJ_S)
        self.mid_ret = case.get("mid_ret", MID_A)
        self.outr_rets = case.get("outr_rets", None)
        self._outr_n = 0
        for va, data in case.get("plants", []):
            gm.w(va, data)
        for va, data in case.get("patch_bytes", []):
            gm.w(va, data)
        uc = self.uc
        uc.hook_add(UC_HOOK_MEM_UNMAPPED, self.on_bad)
        for va in (E56, MIDS, OUTR):
            uc.hook_add(UC_HOOK_CODE, self.on_call, begin=va, end=va)
        for va in (SWAP, FIN, BLD, K3F, RLUT, RES1, GATE, RES2, BASE):
            uc.hook_add(UC_HOOK_CODE, self.on_watch, begin=va, end=va)

    def on_watch(self, uc, addr, size, _):
        """observe a real callee's entry args — the body runs on."""
        if addr == SWAP:
            self.trace.append("W")
        elif addr == FIN:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("f%x:%x" % (rcx & 0xFFFFFFFF, edx))
        elif addr == BLD:
            ecx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            rdx = uc.reg_read(UC_X86_REG_RDX)
            self.trace.append("b%x@%x" % (ecx, rdx & 0xFFFFFFFF))
        elif addr == K3F:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            self.trace.append("k%x" % (rcx & 0xFFFFFFFF))
        elif addr == RLUT:
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            r8 = uc.reg_read(UC_X86_REG_R8) & 0xFFFFFFFF
            xmm0 = struct.unpack("<f", struct.pack(
                "<I", uc.reg_read(UC_X86_REG_XMM0) & 0xFFFFFFFF))[0]
            self.trace.append("L%x:%x:%g" % (edx, r8, xmm0))
        elif addr == RES1:
            ecx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self.trace.append("r%x" % ecx)
        elif addr == GATE:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            self.trace.append("g%x" % (rcx & 0xFFFFFFFF))
        elif addr == RES2:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("R%x:%x" % (rcx & 0xFFFFFFFF, edx))
        elif addr == BASE:
            ecx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self.trace.append("e%x" % ecx)

    def _pop_ret(self):
        uc = self.uc
        sp = uc.reg_read(UC_X86_REG_RSP)
        back = struct.unpack("<Q", self.gm.r(sp, 8))[0]
        uc.reg_write(UC_X86_REG_RSP, sp + 8)
        uc.reg_write(UC_X86_REG_RIP, back)

    def on_call(self, uc, addr, size, _):
        self.fired.add(addr)
        if addr == E56:
            rcx = uc.reg_read(UC_X86_REG_RCX) & 0xFFFFFFFF
            self.trace.append("s%x" % rcx)
            uc.reg_write(UC_X86_REG_RAX, self.e56_ret)
            self._pop_ret()
        elif addr == MIDS:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("m%x:%x" % (rcx & 0xFFFFFFFF, edx))
            uc.reg_write(UC_X86_REG_RAX, self.mid_ret)
            self._pop_ret()
        elif addr == OUTR:
            rcx = uc.reg_read(UC_X86_REG_RCX)
            edx = uc.reg_read(UC_X86_REG_RDX) & 0xFFFFFFFF
            self.trace.append("o%x:%x" % (rcx & 0xFFFFFFFF, edx))
            rets = self.outr_rets or [OBJ_14, OBJ_15]
            ret = rets[self._outr_n % len(rets)]
            self._outr_n += 1
            uc.reg_write(UC_X86_REG_RAX, ret)
            self._pop_ret()

    def on_bad(self, uc, access, addr, size, value, _):
        self.faults.append(("MEM", hex(addr), "access=%d" % access,
                            "rip=%x" % uc.reg_read(UC_X86_REG_RIP)))
        return False


# ---- model -------------------------------------------------------------------

def _lut_ramp(raw, secs, edx, r8d, xmm0):
    """0046FAE0: row=(3*edx+r8d)*0x1E0; idx=cvt((cnt-1)*x);
    cmovs eax,r9d(=0) clamps negative to 0; jbe/lea clamps to cnt-1."""
    cnt = img_dw(raw, secs, LUT_CNT)
    base = LUT_RAMP + (3 * edx + r8d) * 0x1E0
    idx = cvt(f32((cnt - 1) * f32(xmm0)))
    if idx < 0:
        idx = 0                     # cmovs eax, r9d (r9d == 0)
    if idx > cnt - 1:
        idx = cnt - 1
    return bits2f(img_dw(raw, secs, base + idx * 4))


def _trig(raw, secs, i):
    return img_f(raw, secs, LUT_TRIG + (i & 0x7FFF) * 4)


def _dlut(raw, secs, i):
    return img_dw(raw, secs, LUT_DW + (i & 0xFFFFFFFF) * 4)


def m_bld(case, raw, secs, ecx, rdx, out_init):
    """model of 003B62D0.
    returns (ret, out_bytes|None, wb_bytes|None, trace_tokens)."""
    tr = ["b%x@%x" % (ecx & 0xFFFFFFFF, rdx & 0xFFFFFFFF)]
    slots = case.get("slots", [default_slot(i) for i in range(NSLOT)])
    i = ecx & 0xFF
    s = slots[i]
    if (s.get("i10", i) & 0xFFFFFFFF) != (ecx & 0xFFFFFFFF):
        return 0, None, None, tr
    w04 = sx16(s.get("w04", i))
    if w04 == -1:
        return 0, None, None, tr
    recs = case.get("recs", [default_rec(k) for k in range(NSLOT)])
    r = recs[w04] if 0 <= w04 < len(recs) else {"d284": 0}
    if r.get("d284", 1) == 0:
        return 0, None, None, tr
    rbp = RECS + w04 * 0x740
    outr = case.get("outr_rets", None) or [OBJ_14, OBJ_15]

    def res2(kind, n):
        tr.append("R%x:%x" % (rbp & 0xFFFFFFFF, kind & 0xFFFF))
        if s32(r.get("d18", 0)) == -1:
            return 0
        tr.append("e%x" % (r.get("d10", 0) & 0xFFFFFFFF))
        mid_arg = MID_A + w04 * 0x100
        tr.append("m%x:%x" % (mid_arg & 0xFFFFFFFF,
                              r.get("d18", 0) & 0xFFFFFFFF))
        mid = case.get("mid_ret", MID_A)
        if mid == 0:
            return 0
        tr.append("o%x:%x" % (mid & 0xFFFFFFFF, kind & 0xFFFF))
        return outr[n] if n < len(outr) else 0

    r14 = res2(s.get("w3c", 0), 0)
    if r14 == 0:
        return 0, None, None, tr
    r15 = res2(s.get("w3e", 0), 1)
    if r15 == 0:
        return 0, None, None, tr
    # res1 -> gate -> e56
    tr.append("r%x" % (s.get("w04", i) & 0xFFFF))
    tr.append("g%x" % (rbp & 0xFFFFFFFF))
    if r.get("q400", OBJ_S) == 0:
        return 0, None, None, tr
    tr.append("s%x" % (rbp & 0xFFFFFFFF))
    rsi = case.get("e56_ret", OBJ_S)
    if rsi == 0:
        return 0, None, None, tr

    sobj = case.get("sobj", default_sobj())
    ro14 = case.get("robj14", default_robj(1))
    ro15 = case.get("robj15", default_robj(2))
    k3 = case.get("k3", {"pk": 0x60, "f": 0.03125})

    out = bytearray(out_init)
    xmm1 = f32(s.get("f14", 0.0))
    # span2 on sobj w04/w06 -> out+0x14, out+0x6C
    span2 = s16span = (sobj.get("w06", 0) & 0xFFFF) - \
        (sobj.get("w04", 0) & 0xFFFF)
    edx = cvt(f32(span2 * xmm1)) + (sobj.get("w04", 0) & 0xFFFF)
    struct.pack_into("<I", out, 0x14, edx & 0xFFFFFFFF)
    struct.pack_into("<I", out, 0x6C, _dlut(raw, secs, edx))
    # span1 on sobj b01/w02 -> out+0x10
    b01 = sobj.get("b01", 0) & 0xFF
    span1 = (sobj.get("w02", 0) & 0xFFFF) - b01
    eax = (cvt(f32(span1 * xmm1)) + b01) * 2
    struct.pack_into("<I", out, 0x10, eax & 0xFFFFFFFF)
    struct.pack_into("<I", out, 0x30, sobj.get("d08", 0) & 0xFFFFFFFF)
    v20 = fa(fm(xmm1, sobj.get("f3c", 0.0)), sobj.get("f38", 0.0))
    if edx > 1:
        v20 = fd(v20, f32(float(edx - 1)))
    struct.pack_into("<f", out, 0x20, v20)
    if (eax & 0xFFFFFFFF) < 4 or (eax & 0xFFFFFFFF) > 0x64:
        return 0, bytes(out), None, tr     # partial record written
    # bit6: alternate +0x40/44/54 source
    if s.get("b40", 0) & 0x40:
        struct.pack_into("<I", out, 0x54, ro14.get("d34", 0))
        v40 = fa(bits2f(sobj.get("d14", 0)), bits2f(sobj.get("d10", 0)))
        struct.pack_into("<f", out, 0x40, v40)
        struct.pack_into("<I", out, 0x44, 0)
    else:
        q108 = r.get("q108", K3REC)
        tr.append("k%x" % (q108 & 0xFFFFFFFF))
        if q108 == 0 or (k3.get("pk", 0x60) & 0xE0) != 0x60:
            fk = 0.0
        else:
            fk = f32(k3.get("f", 0.0))
        struct.pack_into("<f", out, 0x54, fk)
        struct.pack_into("<I", out, 0x40, sobj.get("d10", 0))
        struct.pack_into("<I", out, 0x44, sobj.get("d14", 0))
    struct.pack_into("<I", out, 0x48, sobj.get("d34", 0))
    struct.pack_into("<I", out, 0x4C, sobj.get("d30", 0))
    struct.pack_into("<I", out, 0x60, s.get("d20", 0))
    struct.pack_into("<I", out, 0x64, s.get("d24", 0))
    struct.pack_into("<I", out, 0x68, s.get("d28", 0))
    v34 = fm(fm(sobj.get("f18", 0.0), s.get("f08", 0.0)),
             s.get("f44", 0.0))
    v38 = fm(fm(sobj.get("f1c", 0.0), s.get("f08", 0.0)),
             s.get("f44", 0.0))
    struct.pack_into("<f", out, 0x34, v34)
    struct.pack_into("<f", out, 0x38, v38)
    cA = img_f(raw, secs, CA)
    cB = img_f(raw, secs, CB)
    v28 = fm(fm(fm(fm(s.get("f0c", 0.0), sobj.get("f0c", 0.0)), cA),
                s.get("f2c", 0.0)), cB)
    struct.pack_into("<f", out, 0x28, v28)
    # ---- row build ----
    if not s.get("b43", 0):
        x4 = f32(s.get("f50", 0.0)); x5 = f32(s.get("f54", 0.0))
        x7 = f32(s.get("f58", 0.0)); x8 = f32(s.get("f5c", 0.0))
        x6 = f32(s.get("f70", 0.0)); x9 = f32(s.get("f78", 0.0))
        xmm2 = xmm3 = None
        # blend select: w38 vs w3c (r14 if equal else r15)
        if (s.get("w38", 0) & 0xFFFF) == (s.get("w3c", 0) & 0xFFFF):
            bA, bB = ro14.get("d30", 0), ro14.get("d38", 0)
        else:
            bA, bB = ro15.get("d30", 0), ro15.get("d38", 0)
        struct.pack_into("<I", out, 0x50, bA & 0xFFFFFFFF)
        struct.pack_into("<I", out, 0x58, bB & 0xFFFFFFFF)
    else:
        tr.append("L%x:%x:%g" % (1, 2, f32(s.get("f98", 0.0))))
        xmm3 = _lut_ramp(raw, secs, 1, 2, s.get("f98", 0.0))
        xmm1c = img_f(raw, secs, CA)          # 1.0 const at 0x1CEBC7C?
        xmm1c = f32(1.0)
        xmm2 = fs(1.0, xmm3)
        al = s.get("b40", 0) & 0x20
        if al:
            x4 = f32(s.get("f50", 0.0)); x5 = f32(s.get("f54", 0.0))
        else:
            x4 = fa(fm(xmm2, s.get("f80", 0.0)),
                    fm(xmm3, s.get("f50", 0.0)))
            x5 = fa(fm(xmm2, s.get("f84", 0.0)),
                    fm(xmm3, s.get("f54", 0.0)))
        x7 = fa(fm(xmm2, s.get("f88", 0.0)), fm(xmm3, s.get("f58", 0.0)))
        x8 = fa(fm(xmm2, s.get("f8c", 0.0)), fm(xmm3, s.get("f5c", 0.0)))
        x6 = fa(fm(xmm2, s.get("f90", 0.0)), fm(xmm3, s.get("f70", 0.0)))
        x9 = fa(fm(xmm2, s.get("f94", 0.0)), fm(xmm3, s.get("f78", 0.0)))
        if al:
            xmm3 = f32(1.0); xmm2 = f32(0.0)
        w38 = s.get("w38", 0) & 0xFFFF
        w3a = s.get("w3a", 0) & 0xFFFF
        w3c = s.get("w3c", 0) & 0xFFFF
        if w3a == w38:
            if w3c == w38:
                bA, bB = ro14.get("d30", 0), ro14.get("d38", 0)
            else:
                bA, bB = ro15.get("d30", 0), ro15.get("d38", 0)
            struct.pack_into("<I", out, 0x50, bA & 0xFFFFFFFF)
            struct.pack_into("<I", out, 0x58, bB & 0xFFFFFFFF)
        elif w3c == w38:
            b50 = fa(fm(xmm2, bits2f(ro15.get("d30", 0))),
                     fm(xmm3, bits2f(ro14.get("d30", 0))))
            b58 = fa(fm(xmm2, bits2f(ro15.get("d38", 0))),
                     fm(xmm3, bits2f(ro14.get("d38", 0))))
            struct.pack_into("<f", out, 0x50, b50)
            struct.pack_into("<f", out, 0x58, b58)
        else:
            b50 = fa(fm(xmm2, bits2f(ro14.get("d30", 0))),
                     fm(xmm3, bits2f(ro15.get("d30", 0))))
            b58 = fa(fm(xmm2, bits2f(ro14.get("d38", 0))),
                     fm(xmm3, bits2f(ro15.get("d38", 0))))
            struct.pack_into("<f", out, 0x50, b50)
            struct.pack_into("<f", out, 0x58, b58)
    # writeback — pre-transform row
    wb = struct.pack("<6f", x4, x5, x7, x8, x6, x9)
    # post-transform
    x4 = fm(fa(x4, s.get("f48", 0.0)), s.get("f44", 0.0))
    x5 = fm(fa(x5, s.get("f4c", 0.0)), s.get("f44", 0.0))
    x6 = fa(fa(x6, r.get("f124", 0.0)), s.get("fbc", 0.0))
    x7 = fm(x7, v34); x8 = fm(x8, v38); x9 = fm(x9, v28)
    struct.pack_into("<f", out, 0x34, x7)
    struct.pack_into("<f", out, 0x38, x8)
    struct.pack_into("<f", out, 0x28, x9)
    struct.pack_into("<f", out, 0x24, x6)
    # rotation tail
    two_pi = img_f(raw, secs, C2A)
    k1 = img_f(raw, secs, K1A)              # +32768.0
    idxr = cvt(fm(fd(r.get("f124", 0.0), two_pi), k1))
    sin_v = _trig(raw, secs, idxr & 0x7FFF)
    cos_v = _trig(raw, secs, (0x2000 + idxr) & 0x7FFF)
    x4f = fa(x4, s.get("f18", 0.0))
    o50 = fa(fa(fm(x4f, cos_v), fm(x5, sin_v)),
             bits2f(struct.unpack_from("<I", out, 0x50)[0]))
    struct.pack_into("<f", out, 0x50, o50)
    o58 = fa(fs(fm(x5, cos_v), fm(x4f, sin_v)),
             bits2f(struct.unpack_from("<I", out, 0x58)[0]))
    struct.pack_into("<f", out, 0x58, o58)
    return 1, bytes(out), wb, tr


def m_fin(case):
    """model of a direct 0036F360(rcx=ring, edx=n16) call.
    returns (ret, ring_mem, trace). edx>=0x200 overwrites the last
    entry instead of appending — the bound mutation discriminates."""
    rcx = case.get("rcx", BUF0) & 0xFFFFFFFFFFFFFFFF
    edx = case.get("rdx", 0) & 0xFFFFFFFF
    tr = "f%x:%x" % (rcx & 0xFFFFFFFF, edx)
    ring = bytearray(0x4000)
    for va, data in case.get("plants", []):
        off = va - rcx
        if 0 <= off < len(ring):
            ring[off:off + len(data)] = data
    if edx:
        hdr = struct.unpack_from("<I", ring, edx * 16 - 0x10)[0]
        if (hdr & 0x70000000) == 0x30000000:
            dst = edx * 16 if edx < 0x200 else edx * 16 - 0x10
            struct.pack_into("<I", ring, dst, 0x10000000)
            struct.pack_into("<Q", ring, dst + 8, 0)
    # eax at ret = the last G_RING load = edx (loop exits on equal)
    return edx if edx else 0, ring, tr


def m_pass(case, raw, secs):
    """model of 003B6020 — returns (exp_obs, trace_str)."""
    tr = []
    gate = case.get("gate", 0) & 0xFFFFFFFF
    bufs = case.get("bufs", [BUF0, BUF1])
    slots = case.get("slots", [default_slot(i) for i in range(NSLOT)])
    idx = case.get("bufidx", 0) & 1
    wr = [bufs[0], bufs[1]]
    cur = [bufs[0], bufs[1]]
    mem = {bufs[0]: bytearray(0x400), bufs[1]: bytearray(0x400)}

    def fin():
        old = idx
        n16 = (cur[old] - wr[old]) >> 4
        tr.append("f%x:%x" % (wr[old] & 0xFFFFFFFF, n16))
        if n16:
            hdr = struct.unpack_from("<I", mem[wr[old]],
                                     n16 * 16 - 0x10)[0]
            if (hdr & 0x70000000) == 0x30000000:
                dst = n16 * 16 if n16 < 0x200 else n16 * 16 - 0x10
                struct.pack_into("<I", mem[wr[old]], dst, 0x10000000)
                struct.pack_into("<Q", mem[wr[old]], dst + 8, 0)

    def swap():
        nonlocal idx
        tr.append("W")
        fin()
        idx = 1 - idx
        cur[idx] = wr[idx]
        return G_ENTS + idx * 24

    # head template -> current entry base
    mem[wr[idx]][0:0x1A0] = head_template(case)
    cur[idx] += 0x1A0
    rax = swap()
    rdx_bld = STACK + 0x80000 - 0x268 + 0x20
    tslot = slot_template(case)
    wbs = {}
    for i in range(NSLOT):
        s = slots[i]
        if not (s.get("b40", 0) & 1):
            continue                        # eax untouched on disabled slots
        rax = (s.get("b41", 0) | gate) & 0xFFFFFFFF
        if rax & 2:
            continue                        # hidden — eax = b41|gate survives
        ecx = s.get("i10", i) & 0xFFFFFFFF
        ret, outb, wb, btr = m_bld(case, raw, secs, ecx, rdx_bld, tslot)
        tr += btr
        rax = ret
        if ret == 0:
            continue
        mem[wr[idx]][0:0xA0] = outb
        wbs[ecx & 0xFF] = wb
        cur[idx] += 0xA0
        rax = swap()
    exp = {"ret": rax & 0xFFFFFFFFFFFFFFFF,
           "bufidx": idx,
           "ring": 0x100,
           "ents": [[wr[0], cur[0], case.get("e16", 0)],
                    [wr[1], cur[1], case.get("e16", 0)]],
           "buf0": list(mem[bufs[0]][0:0x20]),
           "buf1": list(mem[bufs[1]][0:0x20]),
           "buf0h": list(mem[bufs[0]][0x10:0x14]),
           "buf1h": list(mem[bufs[1]][0x10:0x14]),
           "buf0T": list(mem[bufs[0]][0x190:0x1B0]),
           "buf1T": list(mem[bufs[1]][0x190:0x1B0]),
           }
    return exp, " ".join(tr) or "-", wbs


def run_case(case, raw, secs):
    w = World(case, raw, secs)
    uc = w.uc
    sp = STACK + 0x80000
    w.gm.w(sp, qw(RETQ))
    uc.reg_write(UC_X86_REG_RSP, sp)
    entry = case.get("entry", PASS)
    if entry in (BLD, FIN):
        uc.reg_write(UC_X86_REG_RCX,
                     case.get("rcx", 0) & 0xFFFFFFFFFFFFFFFF)
        uc.reg_write(UC_X86_REG_RDX, case.get("rdx", OUT))
    try:
        uc.emu_start(entry, RETQ, count=800_000)
    except Exception as e:
        w.faults.append(("EMU", str(e), uc.reg_read(UC_X86_REG_RIP)))

    gm = w.gm
    obs = {"ret": uc.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF,
           "bufidx": struct.unpack("<I", gm.r(G_BUFIDX, 4))[0],
           "ring": struct.unpack("<I", gm.r(G_RING, 4))[0]}
    tr = " ".join(w.trace) or "-"
    if entry == PASS:
        obs["ents"] = [
            [struct.unpack("<Q", gm.r(G_ENTS + i * 24 + o, 8))[0]
             for o in (0, 8, 0x10)] for i in range(2)]
        bufs = case.get("bufs", [BUF0, BUF1])
        obs["buf0"] = list(gm.r(bufs[0], 0x20))
        obs["buf1"] = list(gm.r(bufs[1], 0x20))
        obs["buf0h"] = list(gm.r(bufs[0] + 0x10, 4))
        obs["buf1h"] = list(gm.r(bufs[1] + 0x10, 4))
        obs["buf0T"] = list(gm.r(bufs[0] + 0x190, 0x20))
        obs["buf1T"] = list(gm.r(bufs[1] + 0x190, 0x20))
        exp, mtr, wbs = m_pass(case, raw, secs)
        obs["wb"] = [list(gm.r(SLOTS + i * 0xE0 + 0xC0, 0x18))
                     for i in case.get("watch", [])]
        exp["wb"] = [list(wbs[i]) if i in wbs else [0] * 0x18
                     for i in case.get("watch", [])]
        return tr, w.faults, obs, exp, mtr
    elif entry == FIN:
        rcx = case.get("rcx", BUF0)
        edx = case.get("rdx", 0) & 0xFFFFFFFF
        win = max(edx * 16 - 0x10, 0)
        ret_m, ring_m, mtr = m_fin(case)
        obs["finmem"] = list(gm.r(rcx + win, 0x20))
        exp = {"ret": ret_m, "ring": 0x100,
               "finmem": list(ring_m[win:win + 0x20])}
        return tr, w.faults, obs, exp, mtr
    else:
        obs["out"] = list(gm.r(case.get("rdx", OUT), 0xA0))
        ecx = case.get("rcx", 0)
        i = ecx & 0xFF
        obs["wb"] = list(gm.r(SLOTS + i * 0xE0 + 0xC0, 0x18))
        ret, outb, wb, mtr_l = m_bld(case, raw, secs, ecx,
                                     case.get("rdx", OUT), bytes(0xA0))
        exp = {"ret": ret,
               "out": list(outb) if outb is not None else [0] * 0xA0,
               "wb": list(wb) if wb is not None else [0] * 0x18}
        return tr, w.faults, obs, exp, " ".join(mtr_l)


# ---- cases -------------------------------------------------------------------

def _slot(i, **kw):
    d = default_slot(i)
    d.update(kw)
    d["_i"] = i
    return d


def _slots(*specs, fill=0):
    """slot list: all-disabled filler, then per-index overrides."""
    slots = []
    for i in range(NSLOT):
        s = dict(default_slot(i), b40=fill)
        slots.append(s)
    for spec in specs:
        slots[spec.get("_i", spec.get("i10", 0)) & 0xFF].update(spec)
    return slots


def build_cases():
    C = []

    def A(name, **kw):
        C.append(dict(name=name, **kw))

    # ---- BLD direct-entry ----
    A("bld-ok", entry=BLD, rcx=0)
    A("bld-hi-ch", entry=BLD, rcx=0x105,
      slots=_slots(_slot(5, i10=0x105)))
    A("bld-idx-mismatch", entry=BLD, rcx=0,
      slots=_slots(_slot(0, i10=7)))
    A("bld-w04-neg1", entry=BLD, rcx=0,
      slots=_slots(_slot(0, w04=0xFFFF)))
    A("bld-rec284zero", entry=BLD, rcx=0,
      recs=[dict(default_rec(0), d284=0)] +
           [default_rec(i) for i in range(1, NSLOT)])
    A("bld-d18-neg1", entry=BLD, rcx=0,
      recs=[dict(default_rec(0), d18=0xFFFFFFFF)] +
           [default_rec(i) for i in range(1, NSLOT)])
    A("bld-res1-null", entry=BLD, rcx=0, outr_rets=[0, OBJ_15])
    A("bld-res2-null", entry=BLD, rcx=0, outr_rets=[OBJ_14, 0])
    A("bld-q400zero", entry=BLD, rcx=0,
      recs=[dict(default_rec(0), q400=0)] +
           [default_rec(i) for i in range(1, NSLOT)])
    A("bld-e56-null", entry=BLD, rcx=0, e56_ret=0)
    A("bld-size-lo", entry=BLD, rcx=0,
      slots=_slots(_slot(0, f14=4.0)),
      sobj=dict(default_sobj(), w02=0))
    A("bld-size-hi", entry=BLD, rcx=0,
      sobj=dict(default_sobj(), w02=200))
    A("bld-bit6", entry=BLD, rcx=0,
      slots=_slots(_slot(0, b40=0x41)))
    A("bld-nolut", entry=BLD, rcx=0,
      slots=_slots(_slot(0, b43=0, w38=2, w3c=2)))
    A("bld-nolut-r15", entry=BLD, rcx=0,
      slots=_slots(_slot(0, b43=0, w38=0, w3c=2)))
    A("bld-bit5", entry=BLD, rcx=0,
      slots=_slots(_slot(0, b40=0x21)))
    A("bld-blend-eq14", entry=BLD, rcx=0,
      slots=_slots(_slot(0, w38=5, w3a=5, w3c=5)))
    A("bld-blend-eq15", entry=BLD, rcx=0,
      slots=_slots(_slot(0, w38=5, w3a=5, w3c=9)))
    A("bld-blend-swap", entry=BLD, rcx=0,
      slots=_slots(_slot(0, w38=2, w3a=9, w3c=2)))
    A("bld-ramp-lo", entry=BLD, rcx=0,
      slots=_slots(_slot(0, f98=0.0)))
    A("bld-ramp-hi", entry=BLD, rcx=0,
      slots=_slots(_slot(0, f98=4.0)))
    A("bld-ramp-neg", entry=BLD, rcx=0,
      slots=_slots(_slot(0, f98=-0.02)))
    A("bld-k3-badkind", entry=BLD, rcx=0,
      k3={"pk": 0x40, "f": 0.03125})
    A("bld-k3-null", entry=BLD, rcx=0,
      recs=[dict(default_rec(0), q108=0)] +
           [default_rec(i) for i in range(1, NSLOT)])
    A("bld-rec5", entry=BLD, rcx=0,
      slots=_slots(_slot(0, w04=5)))
    A("bld-angle-pi", entry=BLD, rcx=0,
      recs=[dict(default_rec(0), f124=3.1415927)] +
           [default_rec(i) for i in range(1, NSLOT)])

    # ---- PASS entry ----
    A("pass-empty", entry=PASS,
      slots=[dict(default_slot(i), b40=0) for i in range(NSLOT)])
    A("pass-one", entry=PASS,
      slots=_slots(_slot(7)), watch=[7])
    A("pass-hide-local", entry=PASS,
      slots=_slots(_slot(7, b41=2)), watch=[7])
    A("pass-hide-global", entry=PASS, gate=2,
      slots=_slots(_slot(7)), watch=[7])
    A("pass-gate-bit0", entry=PASS, gate=1,
      slots=_slots(_slot(7)), watch=[7])
    A("pass-multi3", entry=PASS,
      slots=_slots(_slot(3), _slot(7), _slot(9)), watch=[3, 7, 9])
    A("pass-bldfail", entry=PASS,
      slots=_slots(_slot(5, i10=9), _slot(9, i10=8)), watch=[5, 9])
    A("pass-cross", entry=PASS,
      slots=_slots(_slot(5, i10=9), _slot(9, i10=9, b40=0, f14=0.5)),
      watch=[5, 9])
    A("pass-terminator", entry=PASS,
      slots=_slots(_slot(7)), watch=[7],
      tslot=bytes([0] * 0x90 + [0x00, 0x00, 0x00, 0x30] +
                  [0] * (0xA0 - 0x94)),
      xmm=[0.5, 1.0, 2.0, -1.0] * 4)
    A("pass-bufidx1", entry=PASS, bufidx=1,
      slots=_slots(_slot(7)), watch=[7])
    A("pass-slot159", entry=PASS,
      slots=_slots(_slot(159)), watch=[159])
    # ---- FIN direct-entry ----
    A("fin-bound", entry=FIN, rcx=BUF0, rdx=0x200,
      plants=[(BUF0 + 0x1FF0, dw(0x30000000)),
              (BUF0 + 0x2000, bytes([0xAA] * 16))])
    return C


def check(tr_o, faults, obs, exp, mtr, name):
    errs = []
    if tr_o != mtr:
        errs.append("trace\n  obs: %s\n  exp: %s" % (tr_o, mtr))
    if faults:
        errs.append("faults: %s" % (faults[:3],))
    for k in exp:
        if obs.get(k) != exp[k]:
            errs.append("%s\n  obs: %s\n  exp: %s" % (k, obs.get(k), exp[k]))
    return errs


def _c(name):
    """retrieve a functional case dict by name."""
    for c in build_cases():
        if c["name"] == name:
            return c
    raise KeyError(name)


# mutant spec: (name, va, orig_hex, new_hex, case_name)
# orig verified against shipped bytes before patching.
MUTANTS = [
    # ---- PASS 003B6020 ----
    ("m-enable-bit", 0x3B6203, "01", "02", "pass-one"),      # enable bit0->bit1
    ("m-hide-mask",  0x3B6215, "02", "04", "pass-hide-local"),# hide bit1->bit2
    ("m-hide-or",    0x3B620E, "0b", "23", "pass-hide-global"),# or->and gate
    ("m-hide-jcc",   0x3B6217, "85", "84", "pass-one"),      # jne->je hide
    ("m-loop-cnt",   0x3B61A6, "a0", "9f", "pass-slot159"),  # 160->159 slots
    ("m-stride",     0x3B62A2, "e0", "e1", "pass-multi3"),   # slot stride
    ("m-recadv",     0x3B6293, "a0", "a8", "pass-one"),      # cursor += 0xA8
    ("m-tpladv",     0x3B6178, "a0", "b0", "pass-empty"),    # template += 0x1B0
    ("m-bldret-jcc", 0x3B622B, "74", "75", "pass-bldfail"),  # copy on ret0
    # ---- BLD 003B62D0 ----
    ("m-idxcmp",     0x3B62F1, "74", "75", "bld-ok"),        # je->jne idx gate
    ("m-w04neg",     0x3B6313, "ff", "00", "bld-ok"),        # -1 -> 0
    ("m-d284",       0x3B6338, "44", "45", "bld-rec284zero"),# cmove->cmovne
    ("m-span2",      0x3B63A7, "2b", "03", "bld-ok"),        # sub->add
    ("m-span1",      0x3B63DC, "2b", "03", "bld-ok"),        # sub->add
    ("m-double",     0x3B63EF, "03", "2b", "bld-ok"),        # add->sub eax,eax
    ("m-boundlo",    0x3B6427, "04", "14", "bld-ok"),        # lo bound 4->20
    ("m-boundhi",    0x3B642C, "64", "0a", "bld-ok"),        # hi bound ->10
    ("m-bit6",       0x3B6462, "40", "20", "bld-bit5"),      # bit6->bit5 test
    ("m-bit5",       0x3B6555, "20", "40", "bld-bit6"),      # bit5->bit6 mask
    ("m-b43",        0x3B6523, "84", "85", "bld-ok"),        # je->jne LUT path
    ("m-blend1",     0x3B6603, "74", "75", "bld-blend-eq14"),# w3a==w38 je->jne
    ("m-blend2",     0x3B660F, "75", "74", "bld-blend-swap"),# w38==w3c jne->je
    ("m-blend3",     0x3B666D, "75", "74", "bld-nolut"),     # nolut blend sel
    ("m-f44",        0x3B64E0, "44", "48", "bld-ok"),        # scale f44->f48
    ("m-trigoff",    0x3B66BE, "20", "10", "bld-ok"),        # cos off 0x2000
    ("m-trigmask",   0x3B677C, "7f", "3f", "bld-angle-pi"),  # mask 0x7fff
    ("m-wboff",      0x3B66B8, "c0", "c4", "bld-ok"),        # wb +0xC0->+0xC4
    ("m-f98",        0x3B652C, "98", "9c", "bld-ok"),        # ramp float off
    ("m-f14",        0x3B63A6, "14", "18", "bld-ok"),        # channel f14->f18
    # ---- callees ----
    ("m-toggle",     0x3A1DC8, "2b", "03", "pass-one"),      # sub->add bufidx
    ("m-cur16",      0x3A1DD8, "08", "10", "pass-one"),      # cursor field
    ("m-tag",        0x36F383, "30", "20", "pass-terminator"),# tag cmp
    ("m-finbnd",     0x36F389, "02", "10", "fin-bound"),     # bound ->0x1000
    ("m-ring",       0x36F3F2, "01", "02", "pass-one"),      # ring 0x100->0x200
    ("m-k3kind",     0x26467C, "60", "40", "bld-ok"),        # kind3 0x60->0x40
    ("m-k3off",      0x26468A, "d4", "d8", "bld-ok"),        # k3 float off
    ("m-rstride",    0x3B6C00, "40", "41", "bld-rec5"),      # rec stride
    ("m-r284",       0x3B6C0F, "84", "88", "bld-ok"),        # validity off
    ("m-g400",       0x3E6F73, "00", "04", "bld-ok"),        # gate +0x400->0x404
    ("m-d18neg",     0x422001, "ff", "fe", "bld-d18-neg1"),  # -1 -> -2
    ("m-d98",        0x422014, "98", "9c", "bld-ok"),        # obj +0xD98->0xD9C
    ("m-baseop",     0x20E603, "03", "2b", "bld-hi-ch"),     # add->sub base
    ("m-rstride2",   0x46FAFC, "e0", "e8", "bld-ok"),        # ramp row stride
    ("m-clampj",     0x46FB25, "76", "77", "bld-ramp-hi"),   # jbe->ja clamp
    ("m-cmovs",      0x46FB21, "48", "49", "bld-ramp-neg"),  # cmovs->cmovns
]


def run_mutants(raw, secs):
    base_cache = {}
    results, nkilled = [], 0
    for name, va, orig, new, cname in MUTANTS:
        case = _c(cname)
        got = img_rd(raw, secs, va, len(bytes.fromhex(orig)))
        assert got == bytes.fromhex(orig), \
            "%s: site bytes %s != %s" % (name, got.hex(), orig)
        if cname not in base_cache:
            base_cache[cname] = run_case(case, raw, secs)
        b_tr, b_f, b_obs, b_exp, b_mtr = base_cache[cname]
        mc = dict(case)
        mc["patch_bytes"] = list(case.get("patch_bytes", [])) + \
            [(va, bytes.fromhex(new))]
        t_tr, t_f, t_obs, t_exp, t_mtr = run_case(mc, raw, secs)
        killed = (t_tr != b_tr) or (t_f != b_f) or (t_obs != b_obs)
        nkilled += killed
        print("%-14s %-16s %s" % (name, cname,
                                  "KILLED" if killed else "SURVIVED"))
        if not killed:
            print("    base: ret=%x tr=%s" % (b_obs["ret"], b_tr[:100]))
            print("    mut : ret=%x tr=%s" % (t_obs["ret"], t_tr[:100]))
        results.append({"name": name, "case": cname, "killed": killed})
    print("mutants: %d/%d killed" % (nkilled, len(MUTANTS)))
    return results


def main():
    raw, secs = load_image()
    cases = build_cases()
    npass = 0
    results = {"exe_sha256": SHA, "cases": [], "mutants": []}
    for case in cases:
        tr, faults, obs, exp, mtr = run_case(case, raw, secs)
        errs = check(tr, faults, obs, exp, mtr, case["name"])
        status = "PASS" if not errs else "FAIL"
        if not errs:
            npass += 1
        print("%-18s %s  ret=%x  %s" % (case["name"], status, obs["ret"],
                                       tr[:90]))
        for e in errs[:6]:
            print("   ", e.replace("\n", "\n    "))
        results["cases"].append({"name": case["name"], "ok": not errs})
    print("cases: %d/%d" % (npass, len(cases)))
    results["mutants"] = run_mutants(raw, secs)
    with open("result.json", "w") as fp:
        json.dump(results, fp, indent=1)


if __name__ == "__main__":
    main()
