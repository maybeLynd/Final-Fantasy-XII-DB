# EXP-113 shadow-sync-stage-exec
#
# Executes the shipped 'display character : shadow' stage bodies under
# Unicorn against the shipping EXE:
#
#   00428E40  GATE   stage gate: q[0x22C6F28]=array; b[+0x48842]==1 &&
#             b[+0x48843]==0 -> call WALK, then jmp THUNK. else ret.
#   00426420  WALK   same two gates + ecx=d[array+0x48800] head index;
#             loop: rec=array+ecx*0x740; call SYNC(rec);
#             ecx=sx w[rec+4]; until ecx==-1.
#   00426340  SYNC   per-record shadow sync (the body statically read
#             as CharacterRenderRecord_SyncShadowObjects):
#             h114=d[rec+0x114]: ->V1(h,6);  h118=d[rec+0x118]: ->V2(h,0)
#             flag gate d[+0x284]&0x10C4==0x10C4 (bits 2,6,7 low byte +
#             bit12) && w[rec+6]==-1 && !(b[rec+0x2AE]&2):
#               h114 && !(b[+0xC0]&0x18): V1(h,4);
#                 lod = !(b[+0xC0]&2) ? LODC(h) : f[rec+0x27C];
#                 LODS(h,lod)
#               h118 && (b[+0xC0]&0x18)==8: V2(h,1)
#   003B6900  V1     slot=q[0x2B40528]+(h&0xFF)*0xE0; d[+0x10]==h ->
#             b[+0x41]=(b&(edx>>2))|(edx&3)
#   003AFD00  V2     slot=0x2B4F570+(h&0xFF)*0x70; d[+4]==h ->
#             b[+0x20]=(b&0xF0)|(edx&0xF)
#   003B6B80  LODS   slot=q[0x2B40528]+(h&0xFF)*0xE0; d[+0x10]==h ->
#             f[+0x14]=xmm1
#   00521440  THUNK  jmp 003B6020 (PASS — scripted boundary)
#
# Scripted boundaries: 003B5980 LODC (deep computed-LOD pipeline,
#   ~16KB / 130+ calls — planted xmm0 return + trace), 003B6020 PASS
#   (already executed real in EXP-108 — ret-stub + trace).
#
# Run from this directory: python check.py

import ctypes, hashlib, json, struct, sys

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_64, UC_PROT_ALL, Uc
from unicorn.x86_const import UC_X86_REG_RIP, UC_X86_REG_RSP, \
    UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_XMM0

EXE = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe"
SHA = "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
IMG_LO, IMG_HI = 0x120000, 0x2F800000

HEAP  = 0x40000000
STACK = 0x61000000
RETQ  = 0x62000000

GATE  = 0x00428E40
WALK  = 0x00426420
SYNC  = 0x00426340
V1    = 0x003B6900
V2    = 0x003AFD00
LODC  = 0x003B5980
LODS  = 0x003B6B80
THUNK = 0x00521440
PASS  = 0x003B6020

G_ARR  = 0x022C6F28     # q -> character render record array
G_POOL = 0x02B40528     # q -> 0xE0-stride shadow-object pool
POOL2  = 0x02B3F570     # in-image 0x70-stride second pool

ARRAY  = HEAP + 0x000000
POOL   = HEAP + 0x100000
NREC   = 4

def qw(v): return struct.pack("<Q", v)
def dw(v): return struct.pack("<I", v & 0xFFFFFFFF)
def f32(v): return struct.pack("<f", v)


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


def img_slice(raw, secs, va, n):
    rva = va - IMG_LO
    for sva, vs, ra, rs in secs:
        if sva <= rva and rva + n <= sva + rs:
            return raw[ra + rva - sva: ra + rva - sva + n]
    raise KeyError("va %x outside sections" % va)


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


class World:
    def __init__(self, case, raw, secs, patch=()):
        self.case = case
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        gm = self.gm = GuestMem(self.uc)
        gm.map(IMG_LO, IMG_HI - IMG_LO)
        for sva, vs, ra, rs in secs:
            if vs and rs:
                gm.w(IMG_LO + sva, raw[ra:ra + min(rs, vs)])
        gm.map(HEAP, 0x400000)
        gm.map(STACK, 0x100000)
        gm.map(RETQ, 0x1000)
        gm.w(RETQ, b"\xc3" + b"\xcc" * 0xFF)
        for va, data in patch:
            gm.w(va, data)

        # globals
        gm.w(G_ARR, qw(ARRAY))
        gm.w(G_POOL, qw(POOL))
        # array header
        gm.w(ARRAY + 0x48842, bytes([case.get("g1", 1)]))
        gm.w(ARRAY + 0x48843, bytes([case.get("g2", 0)]))
        gm.w(ARRAY + 0x48800, dw(case.get("head", 0)))
        # records
        for i in range(NREC):
            r = case["recs"][i] if i < len(case.get("recs", [])) else {}
            b = ARRAY + i * 0x740
            gm.w(b + 0x4, struct.pack("<h", r.get("next", -1)))
            gm.w(b + 0x6, struct.pack("<h", r.get("w6", 0)))
            gm.w(b + 0x114, dw(r.get("h114", 0)))
            gm.w(b + 0x118, dw(r.get("h118", 0)))
            gm.w(b + 0x284, dw(r.get("d284", 0)))
            gm.w(b + 0x2AE, bytes([r.get("b2ae", 0)]))
            gm.w(b + 0xC0, bytes([r.get("bc0", 0)]))
            gm.w(b + 0x27C, f32(r.get("f27c", 0.0)))
        # 0xE0 pool slots: {slot: (gen, b41, f14)}
        for s, (gen, b41, f14) in case.get("slots", {}).items():
            sb = POOL + s * 0xE0
            gm.w(sb + 0x10, dw(gen))
            gm.w(sb + 0x14, f32(f14))
            gm.w(sb + 0x41, bytes([b41]))
        # 0x70 pool2 slots (in-image): {slot: (gen, b20)}
        for s, (gen, b20) in case.get("slots2", {}).items():
            sb = POOL2 + s * 0x70
            gm.w(sb + 4, dw(gen))
            gm.w(sb + 0x20, bytes([b20]))

        self.trace = []
        self.fault = None
        uc = self.uc

        def hook(uc_, addr, size, _):
            if addr == LODC:
                self.trace.append(("lodc", uc_.reg_read(UC_X86_REG_RCX)))
                uc_.reg_write(UC_X86_REG_XMM0,
                              int.from_bytes(struct.pack("<f", case.get("lodc", 1.5)) + b"\x00" * 12, "little"))
                rsp = uc_.reg_read(UC_X86_REG_RSP)
                ret = struct.unpack("<Q", gm.r(rsp, 8))[0]
                uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
                uc_.reg_write(UC_X86_REG_RIP, ret)
            elif addr == PASS:
                self.trace.append(("pass",))
                rsp = uc_.reg_read(UC_X86_REG_RSP)
                ret = struct.unpack("<Q", gm.r(rsp, 8))[0]
                uc_.reg_write(UC_X86_REG_RSP, rsp + 8)
                uc_.reg_write(UC_X86_REG_RIP, ret)
            elif addr == V1:
                self.trace.append(("v1", uc_.reg_read(UC_X86_REG_RCX),
                                   uc_.reg_read(UC_X86_REG_RDX)))
            elif addr == V2:
                self.trace.append(("v2", uc_.reg_read(UC_X86_REG_RCX),
                                   uc_.reg_read(UC_X86_REG_RDX)))
            elif addr == LODS:
                self.trace.append(("lods", uc_.reg_read(UC_X86_REG_RCX)))
            elif addr == SYNC:
                self.trace.append(("sync",
                                   (uc_.reg_read(UC_X86_REG_RCX) - ARRAY) // 0x740))

        uc.hook_add(UC_HOOK_CODE, hook)

    def run(self):
        uc = self.uc
        uc.reg_write(UC_X86_REG_RSP, STACK + 0x8000)
        uc.reg_write(UC_X86_REG_RIP, GATE)
        gm = self.gm
        gm.w(STACK + 0x8000, qw(RETQ))
        try:
            uc.emu_start(GATE, RETQ, count=20000)
        except Exception as e:
            self.fault = str(e)
            if uc.reg_read(UC_X86_REG_RIP) == RETQ:
                self.fault = None

    def obs(self):
        gm = self.gm
        slots = {}
        for s in self.case.get("slots", {}):
            sb = POOL + s * 0xE0
            slots[s] = (struct.unpack("<f", gm.r(sb + 0x14, 4))[0],
                        gm.r(sb + 0x41, 1)[0])
        slots2 = {}
        for s in self.case.get("slots2", {}):
            sb = POOL2 + s * 0x70
            slots2[s] = gm.r(sb + 0x20, 1)[0]
        return {"trace": [t for t in self.trace],
                "slots": slots, "slots2": slots2, "fault": self.fault}


def model(case):
    """Mirror of the measured semantics; returns (trace, slots, slots2)."""
    trace = []
    slots = {s: [v[2], v[1]] for s, v in case.get("slots", {}).items()}
    slots2 = {s: v[1] for s, v in case.get("slots2", {}).items()}
    gens = {s: v[0] for s, v in case.get("slots", {}).items()}
    gens2 = {s: v[0] for s, v in case.get("slots2", {}).items()}

    def v1(h, edx):
        trace.append(("v1", h, edx))
        s = h & 0xFF
        if gens.get(s) == h:
            slots[s][1] = (slots[s][1] & ((edx >> 2) & 0xFF)) | (edx & 3)
    def v2(h, edx):
        trace.append(("v2", h, edx))
        s = h & 0xFF
        if gens2.get(s) == h:
            slots2[s] = (slots2[s] & 0xF0) | (edx & 0xF)
    def lods(h, val):
        trace.append(("lods", h))
        s = h & 0xFF
        if gens.get(s) == h:
            slots[s][0] = val

    if case.get("g1", 1) == 1 and case.get("g2", 0) == 0:
        i = case.get("head", 0)
        seen = 0
        while i != -1 and i != 0xFFFFFFFF and seen < NREC:
            seen += 1
            r = case["recs"][i]
            trace.append(("sync", i))
            h114, h118 = r.get("h114", 0), r.get("h118", 0)
            if h114:
                v1(h114, 6)
            if h118:
                v2(h118, 0)
            d284 = r.get("d284", 0)
            if (d284 & 0x10C4) == 0x10C4 and \
                    (r.get("w6", 0) & 0xFFFF) == 0xFFFF and \
                    not (r.get("b2ae", 0) & 2):
                bc0 = r.get("bc0", 0)
                if h114 and not (bc0 & 0x18):
                    v1(h114, 4)
                    if not (bc0 & 2):
                        trace.append(("lodc", h114))
                        lod = case.get("lodc", 1.5)
                    else:
                        lod = r.get("f27c", 0.0)
                    lods(h114, lod)
                if h118 and (bc0 & 0x18) == 8:
                    v2(h118, 1)
            i = r.get("next", -1)
        trace.append(("pass",))
    return trace, slots, slots2


def norm_trace(t):
    return t


def check(case, raw, secs, patch=()):
    w = World(case, raw, secs, patch)
    w.run()
    got = w.obs()
    mtr, mslots, mslots2 = model(case)
    exp = {"trace": mtr,
           "slots": {s: (v[0], v[1]) for s, v in mslots.items()},
           "slots2": mslots2, "fault": None}
    return got, exp


# ---------------------------------------------------------------- cases

def h(gen, slot): return (gen << 8) | slot

def base_recs(**kw):
    r = {"next": -1, "w6": 0, "h114": 0, "h118": 0, "d284": 0,
         "b2ae": 0, "bc0": 0, "f27c": 0.0}
    r.update(kw)
    return r

CASES = {
    # gate arms
    "gate-off1":  {"g1": 0, "head": -1},
    "gate-off2":  {"g2": 1, "head": -1},
    "gate-off1b": {"g1": 2, "head": -1},
    "empty":      {"head": -1},
    # walk + sync basics
    "one-null":   {"head": 0, "recs": [base_recs()]},
    "h114-mode":  {"head": 0, "recs": [base_recs(h114=h(5, 3))],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)}},
    "h114-genbad": {"head": 0, "recs": [base_recs(h114=h(5, 3))],
                    "slots": {3: (h(9, 3), 0xF3, 0.0)}},
    "h118-mode":  {"head": 0, "recs": [base_recs(h118=h(4, 7))],
                   "slots2": {7: (h(4, 7), 0x5C)}},
    "h118-genbad": {"head": 0, "recs": [base_recs(h118=h(4, 7))],
                    "slots2": {7: (h(2, 7), 0x5C)}},
    # flag-gate pass variants
    "flag-pass":  {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                      w6=-1)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-const": {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                      w6=-1, bc0=2, f27c=7.5)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-b8":    {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), h118=h(4, 7),
                                      d284=0x10C4, w6=-1, bc0=8)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "slots2": {7: (h(4, 7), 0x5C)},
                   "lodc": 2.25},
    "flag-b18":   {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), h118=h(4, 7),
                                      d284=0x10C4, w6=-1, bc0=0x18)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "slots2": {7: (h(4, 7), 0x5C)},
                   "lodc": 2.25},
    "flag-b10":   {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), h118=h(4, 7),
                                      d284=0x10C4, w6=-1, bc0=0x10)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "slots2": {7: (h(4, 7), 0x5C)},
                   "lodc": 2.25},
    "flag-w6":    {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                      w6=2)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-2ae":   {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                      w6=-1, b2ae=2)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-miss2": {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C0,
                                      w6=-1)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-miss6": {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x1084,
                                      w6=-1)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-miss7": {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x1044,
                                      w6=-1)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    "flag-miss12": {"head": 0,
                    "recs": [base_recs(h114=h(5, 3), d284=0x00C4,
                                       w6=-1)],
                    "slots": {3: (h(5, 3), 0xF3, 0.0)},
                    "lodc": 2.25},
    # chain walk
    "multi":      {"head": 0,
                   "recs": [base_recs(next=1, h114=h(5, 3),
                                      d284=0x10C4, w6=-1),
                            base_recs(next=2),
                            base_recs(next=-1, h118=h(4, 7),
                                      d284=0x10C4, w6=-1, bc0=8)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "slots2": {7: (h(4, 7), 0x5C)},
                   "lodc": 2.25},
    "multi-wrap": {"head": 2,
                   "recs": [base_recs(next=-1, h114=h(5, 3)),
                            base_recs(next=0),
                            base_recs(next=1)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)}},
    # gen-bad inside second block
    "flag-genbad": {"head": 0,
                    "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                       w6=-1)],
                    "slots": {3: (h(9, 3), 0xF3, 0.0)},
                    "lodc": 2.25},
    # b2ae alternative bits
    "flag-2ae4":  {"head": 0,
                   "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                      w6=-1, b2ae=4)],
                   "slots": {3: (h(5, 3), 0xF3, 0.0)},
                   "lodc": 2.25},
    # lodc with distinct value + const arm
    "flag-const2": {"head": 0,
                    "recs": [base_recs(h114=h(5, 3), d284=0x10C4,
                                       w6=-1, bc0=3, f27c=-4.0)],
                    "slots": {3: (h(5, 3), 0xF3, 0.0)},
                    "lodc": 2.25},
}

# ---------------------------------------------------------------- mutants
# (name, va, orig, patch, case)
MUTS = [
    ("m-g1-imm",   0x428E51, 0x01, 0x02, "multi"),
    ("m-g1-jcc",   0x428E52, 0x75, 0x74, "multi"),
    ("m-g2-imm",   0x428E5A, 0x00, 0x01, "multi"),
    ("m-w-head",   0x426441, 0x04, 0x05, "multi-wrap"),
    ("m-w-hcmp",   0x426445, 0xFF, 0xFE, "empty"),
    ("m-w-stride", 0x426456, 0x40, 0x41, "multi"),
    ("m-w-next",   0x42646E, 0x04, 0x06, "multi"),
    ("m-w-ncmp",   0x426471, 0xFF, 0x00, "multi"),
    ("m-s-h114",   0x42634B, 0x14, 0x16, "h114-mode"),
    ("m-s-h118",   0x42635F, 0x18, 0x1A, "h118-mode"),
    ("m-s-d6",     0x426354, 0x06, 0x05, "h114-mode"),
    ("m-s-xor",    0x426367, 0x33, 0xB2, "h118-mode"),  # + patch byte 2
    ("m-s-d284",   0x426370, 0x84, 0x86, "flag-pass"),
    ("m-s-t4",     0x426375, 0x04, 0x08, "flag-pass"),
    ("m-s-w6d",    0x42637F, 0x06, 0x08, "flag-pass"),
    ("m-s-w6i",    0x426380, 0xFF, 0x00, "flag-pass"),
    ("m-s-2ae",    0x42638D, 0x02, 0x04, "flag-2ae4"),
    ("m-s-jns",    0x426392, 0x79, 0x78, "flag-pass"),
    ("m-s-t40",    0x426395, 0x40, 0x20, "flag-pass"),
    ("m-s-bt",     0x42639B, 0x0C, 0x0D, "flag-pass"),
    ("m-s-c0m",    0x4263AE, 0x18, 0x10, "flag-b8"),
    ("m-s-d4",     0x4263B2, 0x04, 0x05, "flag-pass"),
    ("m-s-c0b2",   0x4263C1, 0x02, 0x04, "flag-const"),
    ("m-s-f27c",   0x4263D5, 0x7C, 0x80, "flag-const"),
    ("m-s-cmp8",   0x4263FB, 0x08, 0x09, "flag-b8"),
    ("m-s-d1",     0x4263FF, 0x01, 0x02, "flag-b8"),
    ("m-v1-e0",    0x3B6907, 0xE0, 0xE1, "h114-mode"),
    ("m-v1-gen",   0x3B6915, 0x10, 0x12, "h114-mode"),
    ("m-v1-and3",  0x3B691C, 0x03, 0x07, "h114-mode"),
    ("m-v1-shr",   0x3B691F, 0x02, 0x03, "h114-mode"),
    ("m-v1-fld",   0x3B6923, 0x41, 0x42, "h114-mode"),
    ("m-v2-70",    0x3AFD07, 0x70, 0x71, "h118-mode"),
    ("m-v2-gen",   0x3AFD17, 0x04, 0x06, "h118-mode"),
    ("m-v2-f0",    0x3AFD24, 0xF0, 0xE0, "h118-mode"),
    ("m-v2-cmov",  0x3AFD1A, 0x45, 0x44, "h118-genbad"),
    ("m-lods-14",  0x3B6B9A, 0x14, 0x16, "flag-pass"),
    ("m-lods-gen", 0x3B6B93, 0x10, 0x12, "flag-pass"),
    ("m-thunk",    0x521441, 0xDB, 0xDA, "empty"),
]

# second patch byte for 2-byte mutants
EXTRA = {"m-s-xor": (0x426368, 0xD2, 0x01)}


def main():
    raw, secs = load_image()
    fails = []
    for name, case in CASES.items():
        got, exp = check(case, raw, secs)
        diffs = []
        if got["trace"] != exp["trace"]:
            diffs.append("trace %r != %r" % (got["trace"], exp["trace"]))
        if got["slots"] != exp["slots"]:
            diffs.append("slots %r != %r" % (got["slots"], exp["slots"]))
        if got["slots2"] != exp["slots2"]:
            diffs.append("slots2 %r != %r" % (got["slots2"], exp["slots2"]))
        if got["fault"] != exp["fault"]:
            diffs.append("fault %r != %r" % (got["fault"], exp["fault"]))
        if diffs:
            fails.append(name)
            print("FAIL %s" % name)
            for d in diffs[:6]:
                print("   ", d)
        else:
            print("pass %s" % name)
    print("== %d/%d cases passed" % (len(CASES) - len(fails), len(CASES)))

    killed, alive, badsite = 0, [], []
    for name, va, orig, new, cname in MUTS:
        case = CASES[cname]
        site = img_slice(raw, secs, va, 1)[0]
        patch = [(va, bytes([new]))]
        if name in EXTRA:
            eva, eorig, enew = EXTRA[name]
            site2 = img_slice(raw, secs, eva, 1)[0]
            if site2 != eorig:
                badsite.append((name, eva, site2))
                continue
            patch.append((eva, bytes([enew])))
        if site != orig:
            badsite.append((name, va, site))
            continue
        got, exp = check(case, raw, secs, patch)
        if got == exp:
            alive.append(name)
        else:
            killed += 1
    print("== mutants: %d killed, %d alive, %d badsite"
          % (killed, len(alive), len(badsite)))
    for n in alive:
        print("  ALIVE", n)
    for n, va, site in badsite:
        print("  BADSITE %s @0x%x saw 0x%02x" % (n, va, site))
    json.dump({"cases": len(CASES),
               "pass": len(CASES) - len(fails),
               "fails": fails,
               "mutants": {"killed": killed, "alive": len(alive),
                           "badsite": len(badsite)}},
              open("result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
